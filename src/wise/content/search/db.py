import os
import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.relationships import RelationshipProperty
from zope.sqlalchemy import register

from eea.cache import cache
from wise.content.search import sql
from wise.content.search.utils import db_result_key, pivot_query

env = os.environ.get
DSN = env('MSFDURI', 'mssql+pymssql://SA:bla3311!@msdb')
DBS = {
    'session': env('MSFD_db_default', 'MarineDB'),
    'session_2018': env('MSFD_db_2018', 'MSFD2018_test')
}

# DBS = {
#     'session': env('MSFD_db_default', 'MarineDB'),
#     'session_2018': env('MSFD_db_2018', 'MSFD2018_sandbox')
# }

USE_DB = 'USE {}'

threadlocals = threading.local()


def session():
    session_name = getattr(threadlocals, 'session_name')

    print "Using session", session_name, DSN
    print "DBS", DBS

    if hasattr(threadlocals, session_name):
        return getattr(threadlocals, session_name)

    session = _make_session(DSN)
    session.execute(USE_DB.format(DBS[session_name]))
    session.rollback()
    setattr(threadlocals, session_name, session)

    return session


def switch_session(func):
    """ Decorator to save the session name and switch back after function runs
    """

    def inner(*args, **kwargs):
        saved_session = getattr(threadlocals, 'session_name', None)

        res = func(*args, **kwargs)

        threadlocals.session_name = saved_session

        return res

    return inner


def _make_session(dsn):
    engine = create_engine(dsn, pool_recycle=1800)
    Session = scoped_session(sessionmaker(bind=engine))
    register(Session, keep_session=True)

    return Session()


@cache(db_result_key)
def get_unique_from_table(table, column):
    """ Retrieves unique values for a column table
    """
    col = getattr(table.c, column)

    sess = session()
    res = sess.query(col).distinct().order_by(col)

    return sorted([x[0] for x in res])


@cache(db_result_key)
def get_unique_from_mapper(mapper_class, column, *conditions):
    """ Retrieves unique values for a mapper class
    """
    col = getattr(mapper_class, column)

    sess = session()
    res = sess.query(col)\
        .filter(*conditions)\
        .distinct()\
        .order_by(col)

    return [unicode(x[0]).strip() for x in res]


# @cache(db_result_key)
def get_unique_from_mapper_join(
        mapper_class,
        column,
        klass_join,
        order_field,
        *conditions,
        **kwargs):
    """ Retrieves unique values for a mapper class
    """
    page = kwargs.get('page', 0)
    col = getattr(mapper_class, column)

    sess = session()
    q = sess.query(col).join(klass_join).filter(
        *conditions
    ).order_by(order_field)

    total = q.count()
    item = q.offset(page).limit(1).first()

    return [total, item]


@cache(db_result_key)
def get_all_columns_from_mapper(mapper_class, column, *conditions):
    """ Retrieves all columns for a mapper class
    """
    col = getattr(mapper_class, column)

    sess = session()
    res = sess.query(mapper_class).filter(*conditions).order_by(col)

    return_value = [x for x in res]

    return return_value


def get_marine_unit_ids(**data):
    """ Return a list of available MarineUnitIDs for the query
    """
    table = sql.t_MSFD4_GegraphicalAreasID
    col = table.c.MarineUnitID

    sess = session()

    conditions = []

    if 'member_states' in data:
        conditions.append(table.c.MemberState.in_(data['member_states']))

    if 'marine_unit_ids' in data:
        return len(data['marine_unit_ids']), data['marine_unit_ids']

    # import pdb; pdb.set_trace()

    # if 'region_subregions' in data:
    #     conditions.append(table.c.RegionSubRegions.in_(
    #         data['region_subregions']))
    #
    # if 'region_subregions' in data:
    #     conditions.append(table.c.RegionSubRegions.in_(
    #         data['region_subregions']))

    query = sess.query(col).filter(
        *conditions
        # table.c.RegionSubRegions.in_(data['region_subregions']),
        # table.c.AreaType.in_(data['area_types']),
    )

    l = sorted([x[0] for x in query])

    return (query.count(), l)


# def group(l, p):
#     res = defaultdict(list)
#
#     for row in l:
#         pass
#
#     return l


# @cache(db_result_key)
def get_collapsed_item(mapper_class, order_field, collapses, *conditions,
                       **kwargs):
    """ Group items
    """
    page = kwargs.get('page', 0)
    sess = session()

    order_field = getattr(mapper_class, order_field)
    cols = []
    blacklist = []

    for d in collapses:
        for k, v in d.items():
            blacklist.append(k)
            blacklist.extend(v)

    for name, var in vars(mapper_class).items():
        if name in blacklist:
            continue

        if name.startswith('_'):
            continue

        if getattr(var, 'primary_key', False) is True:
            continue

        prop = var.property

        if isinstance(prop, RelationshipProperty):
            continue

        cols.append(name)

    mapped_cols = [getattr(mapper_class, n) for n in cols]
    q = sess.query(*mapped_cols).filter(*conditions).distinct()
    all_items = q.all()
    total = len(all_items)
    item_values = all_items[page]
    # print("Item values", item_values)
    # item = q.offset(page).limit(1).first()
    # total = q.count()

    collapse_conditions = [mc == v for mc, v in zip(mapped_cols, item_values)]
    item = mapper_class(**{c: v for c, v in zip(cols, item_values)})

    extra_data = {}

    for d in collapses:
        for k, cs in d.items():
            cols = [k] + cs
            c_cols = [getattr(mapper_class, c) for c in cols]
            q = sess.query(*c_cols).filter(*collapse_conditions)
            extra_data[k] = pivot_query(q, k)

    return [total, item, extra_data]


# @cache(db_result_key)
def get_item_by_conditions(mapper_class, order_field, *conditions, **kwargs):
    """Paged retrieval of items based on conditions
    """

    page = kwargs.get('page', 0)
    sess = session()
    order_field = getattr(mapper_class, order_field)
    q = sess.query(mapper_class).filter(
        *conditions
    ).order_by(order_field)

    total = q.count()
    item = q.offset(page).limit(1).first()

    return [total, item]


# @cache(db_result_key)
def get_item_by_conditions_joined(
        mapper_class,
        klass_join,
        order_field,
        *conditions,
        **kwargs):
    # Paged retrieval of items based on conditions with joining two tables
    page = kwargs.get('page', 0)
    sess = session()
    order_field = getattr(mapper_class, order_field)
    q = sess.query(mapper_class).join(klass_join).filter(
        *conditions
    ).order_by(order_field)

    total = q.count()
    item = q.offset(page).limit(1).first()

    return [total, item]


# @cache(db_result_key)
def get_table_records(columns, *conditions, **kwargs):
    order_by = kwargs.get('order_by')
    sess = session()
    q = sess.query(*columns).filter(*conditions)

    if order_by:
        q = q.order_by(order_by)

    total = q.count()

    return total, q


@cache(db_result_key)
def get_available_marine_unit_ids(marine_unit_ids, klass):
    """ Returns a list of which muid is available, of the ones provided
    """
    sess = session()
    q = sess.query(klass.MarineUnitID).filter(
        klass.MarineUnitID.in_(marine_unit_ids)
    ).order_by(klass.MarineUnitID).distinct()

    total = q.count()
    q = [x for x in q]

    return [total, q]


@cache(db_result_key)
def get_marine_unit_id_names(marine_unit_ids):
    """ Returns tuples of (id, label) based on the marine_unit_ids
    """
    sess = session()
    t = sql.t_MSFD4_GegraphicalAreasID

    q = sess.query(t.c.MarineUnitID, t.c.MarineUnits_ReportingAreas)\
        .filter(t.c.MarineUnitID.in_(marine_unit_ids))\
        .order_by(t.c.MarineUnits_ReportingAreas)\
        .distinct()

    total = q.count()
    q = [x for x in q]

    return [total, q]


# @cache(db_result_key)
def get_related_record(klass, column, rel_id):
    sess = session()
    q = sess.query(klass).filter(
        getattr(klass, column) == rel_id
    )
    item = q.first()

    return [q.count(), item]


# @cache(db_result_key)
def get_related_record_join(klass, klass_join, column, rel_id):
    sess = session()
    q = sess.query(klass).join(klass_join).filter(
        getattr(klass_join, column) == rel_id
    )
    item = q.first()

    return [q.count(), item]


@cache(db_result_key)
def get_all_records(mapper_class, *conditions):
    sess = session()
    q = sess.query(mapper_class).filter(*conditions)
    count = q.count()
    q = [x for x in q]

    return [count, q]


@cache(db_result_key)
def get_all_records_outerjoin(mapper_class, klass_join, *conditions):
    sess = session()
    q = sess.query(mapper_class).outerjoin(klass_join).filter(*conditions)
    count = q.count()
    q = [x for x in q]

    return [count, q]


@cache(db_result_key)
def get_all_records_join(columns, klass_join, *conditions):
    sess = session()
    q = sess.query(*columns).join(klass_join).filter(*conditions)
    count = q.count()
    q = [x for x in q]

    return [count, q]


def update_record(mapper_class, *conditions, **values):
    # TODO check how to update rows
    sess = session()
    sess.update(mapper_class).where(*conditions)\
        .values(**values)


def insert_record(mapper_class, **values):
    # TODO check how to insert rows
    sess = session()
    sess.insert(mapper_class).values(**values)


def compliance_art8_join(columns, mc_join1, mc_join2, *conditions):
    sess = session()
    q = sess.query(*columns).outerjoin(mc_join1).outerjoin(mc_join2).filter(*conditions)
    count = q.count()
    q = [x for x in q]

    return [count, q]
