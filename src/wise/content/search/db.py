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
    table = sql.t_MSFD4_GegraphicalAreasID
    col = table.c.MarineUnitID

    sess = session()
    res = sess.query(col).filter(
        table.c.MemberState == data['member_state'],
        table.c.RegionSubRegions == data['region_subregion'],
        table.c.AreaType == data['area_type'],
    )

    return [x[0] for x in res]


def get_a9_descriptors(marine_unit_id, page=0):
    sess = session()
    q = sess.query(sql.MSFD9Descriptor).filter_by(
        MarineUnitID=marine_unit_id
    ).order_by(sql.MSFD9Descriptor.MSFD9_Descriptor_ID)

    total = q.count()
    print("Total rows" + str(total))
    res = q.offset(page).first()

    return res

    # import pdb; pdb.set_trace()

#     conn = connection()
#     res = conn.execute(text("""
# SELECT *
# FROM MSFD9_Descriptors
# WHERE
# MarineUnitID = :marine_unit_id
# ORDER BY MSFD9_Descriptor_ID
# OFFSET :page ROWS
# FETCH NEXT 1 ROWS ONLY
# """), marine_unit_id=marine_unit_id, page=page)

    return res


def get_a9_feature_impacts(msfd9_descriptor_id):
    conn = connection()
    res = conn.execute(text("""
SELECT DISTINCT FeatureType, FeaturesPressuresImpacts
FROM MarineDB.dbo.MSFD9_Features
WHERE MSFD9_Descriptor = :descriptor_id
;
"""), descriptor_id=msfd9_descriptor_id)

    return res


def get_a10_targets(marine_unit_id, page=0):
    # sess = session()
    # q = sess.query(sql.MSFD10Target).filter_by(
    #     MarineUnitID=marine_unit_id
    # ).order_by(sql.MSFD10Target.MSFD10_Target_ID)
    #
    # total = q.count()
    # print("Total rows" + str(total))
    # res = q.offset(page).first()
    #
    # return res

    conn = connection()
    res = conn.execute(text("""
SELECT MSFD10_Targets.*, MSFD10_DESCrit.GESDescriptorsCriteriaIndicators
FROM MSFD10_Targets
JOIN MSFD10_DESCrit
    ON MSFD10_Targets.MSFD10_Target_ID = MSFD10_DESCrit.MSFD10_Target
WHERE
MSFD10_Targets.MarineUnitID = :marine_unit_id
ORDER BY MSFD10_Targets.MSFD10_Target_ID
OFFSET :page ROWS
FETCH NEXT 1 ROWS ONLY
"""), marine_unit_id=marine_unit_id, page=page)

    # TODO: the MSFD10_DESCrit is not ORM mapped yet
    # this is a temporary hack to overcome this

    # import pdb; pdb.set_trace()

    row = next(res)
    keys = res.keys()
    res = dict(zip(keys, row))
    gdci = res.pop('GESDescriptorsCriteriaIndicators')
    obj = sql.MSFD10Target(**res)
    obj.GESDescriptorsCriteriaIndicators = gdci

    return obj


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
