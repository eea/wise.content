import threading

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text
from zope.sqlalchemy import register

from wise.content.search import sql

DB = "mssql+pymssql://SA:bla3311!@msdb/MarineDB"        # MarineDB

threadlocals = threading.local()


def connection():
    if hasattr(threadlocals, 'connection'):
        return threadlocals.connection

    session = _make_session()
    threadlocals.connection = session.connection()

    return threadlocals.connection


def session():
    if hasattr(threadlocals, 'session'):
        return threadlocals.session

    session = _make_session()
    threadlocals.session = session

    return session


def _make_session():
    engine = create_engine(DB)
    Session = scoped_session(sessionmaker(bind=engine))
    register(Session, keep_session=True)

    return Session()


def get_member_states():
    """ Returns a list of member states. Used in Articles 8, 9 and 10 searches
    """
    table = sql.t_MSFD4_GegraphicalAreasID
    col = table.c.MemberState

    sess = session()
    res = sess.query(col).distinct().order_by(col)

    return [x[0] for x in res]


def get_regions_subregions():
    """ Returns a list of regions and subregions.
    """
    table = sql.t_MSFD4_GegraphicalAreasID
    col = table.c.RegionSubRegions

    sess = session()
    res = sess.query(col).distinct().order_by(col)

    return [x[0] for x in res]


def get_area_types():
    """ Returns a list of area types.
    """

    table = sql.t_MSFD4_GegraphicalAreasID
    col = table.c.AreaType

    sess = session()
    res = sess.query(col).distinct().order_by(col)

    return [x[0] for x in res]


def get_marine_unit_ids(**data):
    """ Return a list of available MarineUnitIDs for the query
    """
    table = sql.t_MSFD4_GegraphicalAreasID
    col = table.c.MarineUnitID

    sess = session()
    query = sess.query(col).filter(
        table.c.MemberState.in_(data['member_states']),
        table.c.RegionSubRegions.in_(data['region_subregions']),
        table.c.AreaType.in_(data['area_types']),
    )

    l = [x[0] for x in query]

    return (query.count(), l)


def get_a9_available_marine_unit_ids(marine_unit_ids):
    """ Returns a list of which muid is available, of the ones provided
    """
    sess = session()
    q = sess.query(sql.MSFD9Descriptor.MarineUnitID).filter(
        sql.MSFD9Descriptor.MarineUnitID.in_(marine_unit_ids)
    ).distinct()

    total = q.count()

    return [total, q]


def get_a9_descriptors(marine_unit_id, page=0):
    sess = session()
    q = sess.query(sql.MSFD9Descriptor).filter(
        sql.MSFD9Descriptor.MarineUnitID == marine_unit_id
    ).order_by(sql.MSFD9Descriptor.MSFD9_Descriptor_ID)

    total = q.count()
    item = q.offset(page).limit(1).first()

    return [total, item]


def get_a9_feature_impacts(msfd9_descriptor_id):
    conn = connection()
    res = conn.execute(text("""
SELECT DISTINCT FeatureType, FeaturesPressuresImpacts
FROM MarineDB.dbo.MSFD9_Features
WHERE MSFD9_Descriptor = :descriptor_id
;
"""), descriptor_id=msfd9_descriptor_id)

    return res


def get_a10_available_marine_unit_ids(marine_unit_ids):
    """ Returns a list of which muid is available, of the ones provided

    TODO: implement specific to A10
    """
    sess = session()
    q = sess.query(sql.MSFD10Target.MarineUnitID).filter(
        sql.MSFD10Target.MarineUnitID.in_(marine_unit_ids)
    ).distinct()

    total = q.count()

    return [total, q]


def get_a10_targets(marine_unit_id, page=0):
    sess = session()
    q = sess.query(sql.MSFD10Target).filter_by(
        MarineUnitID=marine_unit_id
    ).order_by(sql.MSFD10Target.MSFD10_Target_ID)

    total = q.count()
    item = q.offset(page).limit(1).first()

    # TODO: the MSFD10_DESCrit is not ORM mapped yet
    # this query is not finished!!!!

    return [total, item]

#     conn = connection()
#     res = conn.execute(text("""
# SELECT MSFD10_Targets.*, MSFD10_DESCrit.GESDescriptorsCriteriaIndicators
# FROM MSFD10_Targets
# JOIN MSFD10_DESCrit
#     ON MSFD10_Targets.MSFD10_Target_ID = MSFD10_DESCrit.MSFD10_Target
# WHERE
# MSFD10_Targets.MarineUnitID = :marine_unit_id
# ORDER BY MSFD10_Targets.MSFD10_Target_ID
# OFFSET :page ROWS
# FETCH NEXT 1 ROWS ONLY
# """), marine_unit_id=marine_unit_id, page=page)

    # this is a temporary hack to overcome this
    # row = next(res)
    # keys = res.keys()
    # res = dict(zip(keys, row))
    # gdci = res.pop('GESDescriptorsCriteriaIndicators')
    # obj = sql.MSFD10Target(**res)
    # obj.GESDescriptorsCriteriaIndicators = gdci


def get_a10_feature_targets(target_id):
    conn = connection()
    res = conn.execute(text("""
SELECT DISTINCT FeatureType, PhysicalChemicalHabitatsFunctionalPressures
FROM MarineDB.dbo.MSFD10_FeaturesPressures
WHERE MSFD10_Target = :target_id
"""), target_id=target_id)

    return res


def get_a10_criteria_indicators(target_id):
    conn = connection()
    res = conn.execute(text("""
SELECT DISTINCT FeatureType, PhysicalChemicalHabitatsFunctionalPressures
FROM MarineDB.dbo.MSFD10_FeaturesPressures
WHERE MSFD10_Target = :target_id
"""), target_id=target_id)

    return res


def get_a81a_ecosystem(marine_unit_id, page=0):
    klass = sql.MSFD8aEcosystem

    sess = session()
    q = sess.query(klass).filter(
        klass.MarineUnitID == marine_unit_id
    ).order_by(
        klass.MSFD8a_Ecosystem_ID
    )

    total = q.count()
    item = q.offset(page).limit(1).first()

    return [total, item]


def get_related_record(klass, column, rel_id):
    sess = session()
    q = sess.query(klass).filter(
        getattr(klass, column) == rel_id
    )
    item = q.first()

    return [q.count(), item]


# def get_a81a_ecosystem_pressureimpacts(rel_id, page=0):
#     klass = sql.MSFD8aEcosystemPressuresImpact
#
#     sess = session()
#     q = sess.query(klass).filter(
#         klass.MSFD8a_Ecosystem == rel_id
#     ).one()
#     item = q.first()
#
#     return [1, item]
# _pressure_impacts
