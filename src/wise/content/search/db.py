import threading

from zope.sqlalchemy import register

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text

DB = "mssql+pymssql://SA:bla3311!@msdb/MarineDB"        # MarineDB

metadata = MetaData()

threadlocals = threading.local()


def connection():
    if hasattr(threadlocals, 'connection'):
        return threadlocals.connection

    session = _make_session()
    threadlocals.connection = session.connection()

    return threadlocals.connection


def _make_session():
    engine = create_engine(DB)
    Session = scoped_session(sessionmaker(bind=engine))
    register(Session, keep_session=True)

    return Session()


def get_member_states():
    """ Returns a list of member states. Used in Articles 8, 9 and 10 searches
    """

    conn = connection()
    res = conn.execute("""
SELECT DISTINCT MemberState
FROM MSFD4_GegraphicalAreasID
ORDER BY MemberState ASC
    """)

    return [x['MemberState'] for x in res]


def get_regions_subregions():
    """ Returns a list of regions and subregions.
    """

    conn = connection()
    res = conn.execute("""
SELECT DISTINCT RegionSubRegions
FROM MSFD4_GegraphicalAreasID
ORDER BY RegionSubRegions ASC
    """)

    conn = connection()
    res = conn.execute("""
SELECT DISTINCT RegionSubRegions
FROM MSFD4_GegraphicalAreasID
ORDER BY RegionSubRegions ASC
    """)

    return [x['RegionSubRegions'] for x in res]


def get_area_types():
    """ Returns a list of area types.
    """

    conn = connection()
    res = conn.execute("""
SELECT DISTINCT AreaType
FROM MSFD4_GegraphicalAreasID
ORDER BY AreaType ASC
    """)

    return [x['AreaType'] for x in res]


def get_marine_unit_id(**data):
    conn = connection()
    res = conn.execute(text("""
SELECT MarineUnitID
FROM MSFD4_GegraphicalAreasID
WHERE
    MemberState = :member_state AND
    RegionSubRegions = :region_subregion AND
    AreaType = :area_type
"""), **data)

    uid = res.first()

    return uid and uid[0] or None


def get_a9_descriptors(marine_unit_id, page=0):
    conn = connection()
    res = conn.execute(text("""
SELECT *
FROM MSFD9_Descriptors
WHERE
MarineUnitID = :marine_unit_id
ORDER BY MSFD9_Descriptor_ID
OFFSET :page ROWS
FETCH NEXT 1 ROWS ONLY
"""), marine_unit_id=marine_unit_id, page=page)

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

    return res


def get_a10_feature_targets(target_id):
    conn = connection()
    res = conn.execute(text("""
SELECT DISTINCT FeatureType, PhysicalChemicalHabitatsFunctionalPressures, Topic
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
