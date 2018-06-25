import csv
import logging
import json

from lxml.etree import parse
from pkg_resources import resource_filename
from sqlalchemy.sql.schema import Table
from sqlalchemy import and_, or_
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from wise.content.search import db, sql, sql2018

from .utils import FORMS, FORMS_2018, FORMS_ART11, LABELS, SUBFORMS
from .a11 import ART11_GlOBALS


def populate_labels():
    csv_labels = {}
    xsd_labels = {}

    csv_f = resource_filename('wise.content',
                              'search/data/MSFDreporting_TermLists.csv')

    with open(csv_f, 'rb') as csvfile:
        csv_file = csv.reader(csvfile, delimiter=',', quotechar='|')

        for row in csv_file:
            if row[0] in csv_labels.keys():
                logger = logging.getLogger('tcpserver')
                logger.warning("Duplicate label in csv file: %s", row[0])

            csv_labels[row[0]] = row[1]

    # """ Read XSD files and populates a vocabulary of term->label

    # Note: there labels are pretty ad-hoc defined in the xsd file as
    # documentation tags, so this method is imprecise.
    # """

    lines = []
    xsd_f = resource_filename('wise.content',
                              'search/data/MSCommon_1p0.xsd')

    e = parse(xsd_f)

    for node in e.xpath('//xs:documentation',
                        namespaces={'xs': "http://www.w3.org/2001/XMLSchema"}):
        text = node.text.strip()
        lines.extend(text.split('\n'))

    for line in lines:

        line = line.strip()

        for splitter in ['=', '\t']:
            eqpos = line.find(splitter)

            if eqpos == -1:
                continue

            if ' ' in line[:eqpos]:
                continue

            label, title = line.split(splitter, 1)

            if label in LABELS:
                logger = logging.getLogger('tcpserver')
                logger.warning("Duplicate label in xsd file: %s", label)

            xsd_labels[label] = title

    LABELS.update(csv_labels)
    LABELS.update(xsd_labels)

    common_labels = len(list(csv_labels.keys()) +
                        list(xsd_labels.keys())) - len(LABELS)

    csv_nr = len(list(csv_labels.keys()))
    xsd_nr = len(list(xsd_labels.keys()))

    print("""Labels count:
    Total labels: %s
    Common_labels: %s
    .csv_nr: %s
    .xsd_nr: %s""" % (len(LABELS), common_labels, csv_nr, xsd_nr))

    return


populate_labels()


class SubFormsVocabulary(SimpleVocabulary):
    """ An hackish vocabulary that retrieves subform names for a form
    """

    # TODO: I'm not sure if this is needed. Its existance needs to be defended

    def __init__(self, form_klass):
        self.form_klass = form_klass
        pass

    def __call__(self, context):
        self.context = context

    @property
    def _terms(self):
        terms = []

        forms = SUBFORMS[self.form_klass]

        for k in forms:
            terms.append(SimpleTerm(k, k.title, k.title))

        terms.sort(key=lambda t: t.title)

        return terms

    @property
    def by_value(self):
        d = {}

        for term in self._terms:
            d[term.value] = term

        return d

    @property
    def by_token(self):
        d = {}

        for term in self._terms:
            d[term.token] = term

        return d


def vocab_from_values(values):
    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in values]
    # TODO fix UnicodeDecodeError
    # Article Indicators, country Lithuania
    try:
        terms.sort(key=lambda t: t.title)
    except UnicodeDecodeError:
        pass
    vocab = SimpleVocabulary(terms)

    return vocab


def vocab_from_values_with_count(values, column):
    dict_count = dict()
    for x in values:
        col = getattr(x, column)
        if col in dict_count:
            dict_count[col] += 1
        else:
            dict_count[col] = 1

    terms = [
        SimpleTerm(x, x, "{} [{}]".format(LABELS.get(x, x), dict_count[x]))
        for x in dict_count.keys()
    ]
    # TODO fix UnicodeDecodeError
    # Article Indicators, country Lithuania
    try:
        terms.sort(key=lambda t: t.title)
    except UnicodeDecodeError:
        pass
    vocab = SimpleVocabulary(terms)

    return vocab


def db_vocab(table, column):
    """ Builds a vocabulary based on unique values in a column table
    """

    if isinstance(table, Table):
        res = db.get_unique_from_table(table, column)
    elif table.__tablename__ == 'MSFD11_MPTypes':
        res = db.get_all_columns_from_mapper(table, column)
        terms = [
            SimpleTerm(x.ID, x.ID, LABELS.get(x.Description, x.Description))

            for x in res
        ]
        terms.sort(key=lambda t: t.title)
        vocab = SimpleVocabulary(terms)

        return vocab
    else:
        res = db.get_unique_from_mapper(table, column)

    res = [x.strip() for x in res]

    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in res]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


def get_json_subform_data(json_str, field_title):
    _form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == field_title
    ]
    data = [
        x['value']
        for x in _form_data[0]
        if x['checked']
    ]
    return data


@provider(IVocabularyFactory)
def get_member_states_vb_factory(context):
    return db_vocab(sql.t_MSFD4_GegraphicalAreasID, 'MemberState')


@provider(IVocabularyFactory)
def get_region_subregions_vb_factory(context):
    return db_vocab(sql.t_MSFD4_GegraphicalAreasID, 'RegionSubRegions')


@provider(IVocabularyFactory)
def get_area_type_vb_factory(context):
    return db_vocab(sql.t_MSFD4_GegraphicalAreasID, 'AreaType')


@provider(IVocabularyFactory)
def articles_vocabulary_factory(context):
    terms = [SimpleTerm(k, k, v.title) for k, v in FORMS.items()]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def monitoring_programme_vb_factory(context):
    return db_vocab(sql.MSFD11MPType, 'ID')


@provider(IVocabularyFactory)
def monitoring_programme_info_types(context):
    terms = [SimpleTerm(v, k, v.title) for k, v in FORMS_ART11.items()]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def art11_country(context):
    if not hasattr(context, 'subform'):
        mp_type_ids = context.context.get_mp_type_ids()
    else:
        mp_type_ids = context.get_mp_type_ids()

    mon_ids = db.get_unique_from_mapper(
        sql.MSFD11MP,
        'MON',
        sql.MSFD11MP.MPType.in_(mp_type_ids)
    )

    res = db.get_unique_from_mapper(
        sql.MSFD11MON,
        'MemberState',
        sql.MSFD11MON.ID.in_(mon_ids)
    )
    res = [x.strip() for x in res]

    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in res]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def art11_country_ms(context):
    if not hasattr(context, 'subform'):
        mp_type_ids = context.context.get_mp_type_ids()
        mptypes_subprog = ART11_GlOBALS.get(
            'get_mptypes_subprog',
            context.context.subform.get_mptypes_subprog)
    else:
        mptypes_subprog = ART11_GlOBALS.get(
            'get_mptypes_subprog',
            context.subform.get_mptypes_subprog)
        mp_type_ids = context.get_mp_type_ids()

    submonprog_ids = []
    for x in mp_type_ids:
        submonprog_ids.append(mptypes_subprog[int(x)])

    submonprog_ids = tuple([item for sublist in submonprog_ids for item in sublist])

    # import pdb;pdb.set_trace()

    res = db.get_unique_from_mapper(
        sql.MSFD11MONSub,
        'MemberState',
        sql.MSFD11MONSub.SubProgramme.in_(submonprog_ids)
    )
    res = [x.strip() for x in res]

    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in res]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def art11_region(context):
    if not hasattr(context, 'subform'):
        json_str = json.loads(context.json())
        mp_type_ids = context.context.get_mp_type_ids()
    else:
        json_str = json.loads(context.subform.json())
        mp_type_ids = context.get_mp_type_ids()
    countries_form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == 'Country'
    ]
    countries = [
        country['value']
        for country in countries_form_data[0]
        if country['checked']
    ]

    mon_ids = db.get_unique_from_mapper(
        sql.MSFD11MP,
        'MON',
        sql.MSFD11MP.MPType.in_(mp_type_ids)
    )

    if countries:
        condition = and_(
            sql.MSFD11MON.MemberState.in_(countries),
            sql.MSFD11MON.ID.in_(mon_ids)
        )
    else:
        condition = sql.MSFD11MON.ID.in_(mon_ids)

    res = db.get_unique_from_mapper(
        sql.MSFD11MON,
        'Region',
        condition
    )
    res = [x.strip() for x in res]

    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in res]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def art11_region_ms(context):
    if not hasattr(context, 'subform'):
        json_str = json.loads(context.json())
        mp_type_ids = context.context.get_mp_type_ids()
        mptypes_subprog = ART11_GlOBALS.get(
            'get_mptypes_subprog',
            context.context.subform.get_mptypes_subprog)
    else:
        json_str = json.loads(context.subform.json())
        mptypes_subprog = ART11_GlOBALS.get(
            'get_mptypes_subprog',
            context.subform.get_mptypes_subprog)
        mp_type_ids = context.get_mp_type_ids()

    countries_form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == 'Country'
    ]
    countries = [
        country['value']
        for country in countries_form_data[0]
        if country['checked']
    ]

    submonprog_ids = []
    for x in mp_type_ids:
        submonprog_ids.append(mptypes_subprog[int(x)])

    submonprog_ids = tuple([item for sublist in submonprog_ids for item in sublist])

    if countries:
        condition = and_(
            sql.MSFD11MONSub.MemberState.in_(countries),
            sql.MSFD11MONSub.SubProgramme.in_(submonprog_ids)
        )
    else:
        condition = sql.MSFD11MONSub.SubProgramme.in_(submonprog_ids)

    res = db.get_unique_from_mapper(
        sql.MSFD11MONSub,
        'Region',
        condition
    )
    res = [x.strip() for x in res]

    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in res]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def art11_marine_unit_id(context):
    if not hasattr(context, 'subform'):
        json_str = json.loads(context.json())
        # mp_type_ids = context.context.get_mp_type_ids()
    else:
        json_str = json.loads(context.subform.json())
        # mp_type_ids = context.get_mp_type_ids()
    countries_form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == 'Country'
    ]
    countries = [
        country['value']
        for country in countries_form_data[0]
        if country['checked']
    ]
    regions_form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == 'Region'
    ]
    regions = [
        region['value']
        for region in regions_form_data[0]
        if region['checked']
    ]

    if countries and regions:
        mon_ids = db.get_unique_from_mapper(
            sql.MSFD11MON,
            'ID',
            and_(sql.MSFD11MON.MemberState.in_(countries),
                 sql.MSFD11MON.Region.in_(regions))

        )
    elif countries:
        mon_ids = db.get_unique_from_mapper(
            sql.MSFD11MON,
            'ID',
            sql.MSFD11MON.MemberState.in_(countries)
        )
    else:
        mon_ids = db.get_unique_from_mapper(
            sql.MSFD11MON,
            'ID'
        )

    mon_ids = [str(x).strip() for x in mon_ids]

    mon_prog_ids = db.get_unique_from_mapper(
        sql.MSFD11MP,
        'MonitoringProgramme',
        and_(sql.MSFD11MP.MON.in_(mon_ids)
             # ,sql.MSFD11MP.MPType.in_(mp_type_ids)
             )
    )
    mon_prog_ids = [x.strip() for x in mon_prog_ids]

    count, marine_units = db.get_all_records_outerjoin(
        sql.MSFD11MarineUnitID,
        sql.MSFD11MonitoringProgrammeMarineUnitID,
        sql.MSFD11MonitoringProgrammeMarineUnitID.MonitoringProgramme.in_(mon_prog_ids)
    )

    terms = [SimpleTerm(x.MarineUnitID, x.MarineUnitID, x.MarineUnitID) for x in marine_units]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def art11_marine_unit_id_ms(context):
    if not hasattr(context, 'subform'):
        json_str = json.loads(context.json())
        mp_type_ids = context.context.get_mp_type_ids()
        mptypes_subprog = ART11_GlOBALS.get(
            'get_mptypes_subprog',
            context.context.subform.get_mptypes_subprog)
    else:
        json_str = json.loads(context.subform.json())
        mptypes_subprog = ART11_GlOBALS.get(
            'get_mptypes_subprog',
            context.subform.get_mptypes_subprog)
        mp_type_ids = context.get_mp_type_ids()

    countries_form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == 'Country'
    ]
    countries = [
        country['value']
        for country in countries_form_data[0]
        if country['checked']
    ]
    regions_form_data = [
        field['options']
        for field in json_str['fields']
        if field['label'] == 'Region'
    ]
    regions = [
        region['value']
        for region in regions_form_data[0]
        if region['checked']
    ]

    submonprog_ids = []
    for x in mp_type_ids:
        submonprog_ids.append(mptypes_subprog[int(x)])

    submonprog_ids = tuple([item for sublist in submonprog_ids for item in sublist])

    if countries and regions:
        subprogramme_ids = db.get_unique_from_mapper(
            sql.MSFD11MONSub,
            'SubProgramme',
            and_(sql.MSFD11MONSub.MemberState.in_(countries),
                 sql.MSFD11MONSub.Region.in_(regions),
                 sql.MSFD11MONSub.SubProgramme.in_(submonprog_ids))

        )
    elif countries:
        subprogramme_ids = db.get_unique_from_mapper(
            sql.MSFD11MONSub,
            'SubProgramme',
            and_(sql.MSFD11MONSub.MemberState.in_(countries),
                 sql.MSFD11MONSub.SubProgramme.in_(submonprog_ids))
        )
    else:
        subprogramme_ids = db.get_unique_from_mapper(
            sql.MSFD11MONSub,
            'SubProgramme',
            sql.MSFD11MONSub.SubProgramme.in_(submonprog_ids)
        )

    subprogramme_ids = [int(x) for x in subprogramme_ids]

    q4g_subprogids_1 = db.get_unique_from_mapper(
        sql.MSFD11SubProgramme,
        'Q4g_SubProgrammeID',
        sql.MSFD11SubProgramme.ID.in_(subprogramme_ids)
    )
    q4g_subprogids_2 = db.get_unique_from_mapper(
        sql.MSFD11SubProgrammeIDMatch,
        'MP_ReferenceSubProgramme',
        sql.MSFD11SubProgrammeIDMatch.Q4g_SubProgrammeID.in_(q4g_subprogids_1)
    )

    mc_ref_sub = sql.MSFD11ReferenceSubProgramme
    mp_from_ref_sub = db.get_unique_from_mapper(
        sql.MSFD11ReferenceSubProgramme,
        'MP',
        or_(mc_ref_sub.SubMonitoringProgrammeID.in_(q4g_subprogids_1),
            mc_ref_sub.SubMonitoringProgrammeID.in_(q4g_subprogids_2)
            )
    )
    mp_from_ref_sub = [int(x) for x in mp_from_ref_sub]

    mon_prog_ids = db.get_unique_from_mapper(
        sql.MSFD11MP,
        'MonitoringProgramme',
        sql.MSFD11MP.ID.in_(mp_from_ref_sub)
    )

    mc_ = sql.MSFD11MonitoringProgrammeMarineUnitID
    count, marine_units = db.get_all_records_outerjoin(
        sql.MSFD11MarineUnitID,
        mc_,
        mc_.MonitoringProgramme.in_(mon_prog_ids)
    )

    terms = [
        SimpleTerm(x.MarineUnitID, x.MarineUnitID, x.MarineUnitID)
        for x in marine_units
    ]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    # import pdb; pdb.set_trace()

    return vocab


def marine_unit_id_vocab(ids):
    count, res = db.get_marine_unit_id_names(ids)

    terms = []

    for id, label in res:
        if label:
            label = u'%s (%s)' % (label, id)
        else:
            label = id
        terms.append(SimpleTerm(id, id, label))
        terms.sort(key=lambda t: t.title)

    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def marine_unit_ids_vocab_factory(context):
    """ A list of MarineUnitIds based on geodata selected
    """

    if hasattr(context, 'get_available_marine_unit_ids'):
        count, ids = context.get_available_marine_unit_ids()

    else:
        data = context.data
        count, ids = db.get_marine_unit_ids(**data)

    return marine_unit_id_vocab(sorted(ids))


@provider(IVocabularyFactory)
def marine_unit_id_vocab_factory(context):
    """ A list of MarineUnitIds taken from parent form selection
    """
    ids = context.subform.get_available_marine_unit_ids()

    return marine_unit_id_vocab(sorted(ids))


@provider(IVocabularyFactory)
def a1314_report_types(context):
    return db_vocab(sql.MSFD13ReportingInfo, 'ReportType')


@provider(IVocabularyFactory)
def a1314_regions(context):
    return db_vocab(sql.MSFD13ReportingInfo, 'Region')


@provider(IVocabularyFactory)
def a1314_unique_codes(context):
    codes = context.data.get('unique_codes')
    terms = [
        SimpleTerm(code, code, u'%s - %s' % (code, name))

        for code, name in codes
    ]
    terms.sort(key=lambda t: t.title)

    return SimpleVocabulary(terms)


# Articles 8, 9, 10
# reporting year 2018
@provider(IVocabularyFactory)
def articles_vocabulary_factory_2018(context):
    terms = [SimpleTerm(v, k, v.title) for k, v in FORMS_2018.items()]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def a2018_country(context):
    # import pdb;pdb.set_trace()
    if hasattr(context, 'subform'):
        context_orig = context
        context = context.subform

    mapper_class = context.mapper_class
    # mapper_class = getattr(context, 'mapper_class', context.subform.mapper_class)

    count, res = db.get_all_records_join(
        [
            mapper_class.Id,
            sql2018.ReportedInformation.CountryCode
        ],
        sql2018.ReportedInformation
    )
    # count, res = db.get_all_records_outerjoin(
    #     sql2018.ReportedInformation,
    #     mapper_class
    # )

    # res = [x.CountryCode for x in res]
    # res = list(set(res))

    return vocab_from_values_with_count(res, 'CountryCode')


@provider(IVocabularyFactory)
def a2018_marine_reporting_unit(context):
    if hasattr(context, 'subform'):
        context_orig = context
        context = context.subform

    json_str = json.loads(context.json())
    mapper_class = context.mapper_class

    countries = get_json_subform_data(json_str, 'Country Code')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))

    count, res = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    # res = [x.MarineReportingUnit for x in res]
    res = ['MarineReportingUnit%s' % x for x in range(0, 10)]

    # import pdb;pdb.set_trace()

    return vocab_from_values(res)


@provider(IVocabularyFactory)
def a2018_ges_component_art9(context):
    if hasattr(context, 'subform'):
        context_orig = context
        context = context.subform

    json_str = json.loads(context.json())
    mapper_class = context.mapper_class

    countries = get_json_subform_data(json_str, 'Country Code')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))

    count, res = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    # res = [x.GESComponent for x in res]
    res = ['GesComponent%s' % x for x in range(0, 10)]

    return vocab_from_values(res)


@provider(IVocabularyFactory)
def a2018_feature_art9(context):
    if not hasattr(context, 'features_mc'):
        context_orig = context
        context = context.context

    mapper_class = context.mapper_class
    features_mc = context.features_mc
    json_str = json.loads(context.json())

    countries = get_json_subform_data(json_str, 'Country Code')
    ges_components = get_json_subform_data(json_str, 'GES Component')

    mc_countries = sql2018.ReportedInformation
    conditions = list()
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))
    if ges_components:
        conditions.append(mapper_class.GESComponent.in_(ges_components))

    count, id_marine_units = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    id_ges_components = [int(x.Id) for x in id_marine_units]

    count, ids_ges_determination = db.get_all_records_join(
        [sql2018.ART9GESGESDetermination.IdGESComponent,
         sql2018.ART9GESGESDeterminationFeature.Feature],
        sql2018.ART9GESGESDeterminationFeature,
        sql2018.ART9GESGESDetermination.IdGESComponent.in_(id_ges_components)
    )
    res = [x.Feature for x in ids_ges_determination]
    res = tuple(set(res))

    res = ['%s%s' % (features_mc.__name__, x) for x in range(0, 10)]
    return vocab_from_values(res)


@provider(IVocabularyFactory)
def a2018_feature_art81c(context):
    if not hasattr(context, 'features_mc'):
        context_orig = context
        context = context.context

    mapper_class = context.mapper_class
    features_mc = context.features_mc
    json_str = json.loads(context.json())

    countries = get_json_subform_data(json_str, 'Country Code')
    mrus = get_json_subform_data(json_str, 'Marine Reporting Unit')

    mc_countries = sql2018.ReportedInformation
    conditions = list()
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))
    if mrus:
        conditions.append(mapper_class.MarineReportingUnit.in_(mrus))

    count, id_marine_units = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    id_marine_units = [int(x.Id) for x in id_marine_units]

    res = db.get_unique_from_mapper(
        features_mc,
        'Feature',
        features_mc.IdMarineUnit.in_(id_marine_units)
    )

    res = ['%s%s' % (features_mc.__name__, x) for x in range(0, 10)]
    return vocab_from_values(res)


@provider(IVocabularyFactory)
def a2018_feature(context):
    # import pdb;pdb.set_trace()
    if not hasattr(context, 'features_mc'):
        context_orig = context
        context = context.context

    mapper_class = context.mapper_class
    features_mc = context.features_mc
    features_rel_col = context.features_relation_column
    target_mc = context.target_mc
    json_str = json.loads(context.json())

    countries = get_json_subform_data(json_str, 'Country Code')
    mrus = get_json_subform_data(json_str, 'Marine Reporting Unit')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))
    if mrus:
        conditions.append(mapper_class.MarineReportingUnit.in_(mrus))

    count, id_marine_units = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    id_marine_units = [int(x.Id) for x in id_marine_units]

    id_targets = db.get_unique_from_mapper(
        target_mc,
        'Id',
        target_mc.IdMarineUnit.in_(id_marine_units)
    )

    res = db.get_unique_from_mapper(
        features_mc,
        'Feature',
        getattr(features_mc, features_rel_col).in_(id_targets)
    )

    res = ['Feature%s' % x for x in range(0, 10)]
    return vocab_from_values(res)


@provider(IVocabularyFactory)
def a2018_ges_component(context):
    # import pdb;pdb.set_trace()
    if not hasattr(context, 'ges_components_mc'):
        context_orig = context
        context = context.context

    mapper_class = context.mapper_class
    features_mc = context.features_mc
    features_rel_col = context.features_relation_column
    ges_components_mc = context.ges_components_mc
    ges_comp_rel_col = context.ges_components_relation_column
    target_mc = context.target_mc
    json_str = json.loads(context.json())
    json_str_subform = json.loads(context.subform.json())

    countries = get_json_subform_data(json_str, 'Country Code')
    mrus = get_json_subform_data(json_str, 'Marine Reporting Unit')
    features = get_json_subform_data(json_str_subform, 'Features')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))
    if mrus:
        conditions.append(mapper_class.MarineReportingUnit.in_(mrus))

    count, id_marine_units = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    id_marine_units = [int(x.Id) for x in id_marine_units]

    conditions = []
    conditions.append(target_mc.IdMarineUnit.in_(id_marine_units))
    if features:
        id_features = db.get_unique_from_mapper(
            features_mc,
            features_rel_col,
            features_mc.Feature.in_(features)
        )
        conditions.append(target_mc.Id.in_(id_features))

    id_targets = db.get_unique_from_mapper(
        target_mc,
        'Id',
        *conditions
    )

    res = db.get_unique_from_mapper(
        ges_components_mc,
        'GESComponent',
        getattr(ges_components_mc, ges_comp_rel_col).in_(id_targets)
    )

    res = ['GesComponent%s' % x for x in range(0, 10)]
    return vocab_from_values(res)


@provider(IVocabularyFactory)
def a2018_ges_component_ind(context):
    if not hasattr(context, 'mapper_class'):
        context_orig = context
        context = context.context

    json_str = json.loads(context.json())
    mapper_class = context.mapper_class
    ges_comp_mc = context.ges_components_mc

    countries = get_json_subform_data(json_str, 'Country Code')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))

    count, ids_indicator = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    ids_indicator = [int(x.Id) for x in ids_indicator]

    # res = db.get_unique_from_mapper(
    #     ges_comp_mc,
    #     'GESComponent',
    #     ges_comp_mc.IdIndicatorAssessment.in_(ids_indicator)
    # )

    count, res = db.get_all_records(
        ges_comp_mc,
        ges_comp_mc.IdIndicatorAssessment.in_(ids_indicator)
    )

    # import pdb;pdb.set_trace()
    # res = ['GESComponent%s' % x for x in range(0, 10)]
    return vocab_from_values_with_count(res, 'GESComponent')


@provider(IVocabularyFactory)
def a2018_feature_ind(context):
    if not hasattr(context, 'mapper_class'):
        context_orig = context
        context = context.context

    json_str = json.loads(context.json())
    json_str_subform = json.loads(context.subform.json())
    mapper_class = context.mapper_class
    ges_comp_mc = context.ges_components_mc
    features_mc = context.features_mc

    countries = get_json_subform_data(json_str, 'Country Code')
    ges_components = get_json_subform_data(json_str_subform, 'GES Component')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))

    count, ids_indicator = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    ids_indicator = [int(x.Id) for x in ids_indicator]

    conditions = list()
    conditions.append(ges_comp_mc.IdIndicatorAssessment.in_(ids_indicator))
    if ges_components:
        conditions.append(ges_comp_mc.GESComponent.in_(ges_components))

    ids_ges_comp = db.get_unique_from_mapper(
        ges_comp_mc,
        'Id',
        *conditions
    )
    ids_ges_comp = [int(x) for x in ids_ges_comp]

    # res = db.get_unique_from_mapper(
    #     features_mc,
    #     'Feature',
    #     features_mc.IdGESComponent.in_(ids_ges_comp)
    # )

    count, res = db.get_all_records(
        features_mc,
        features_mc.IdGESComponent.in_(ids_ges_comp)
    )

    # import pdb;pdb.set_trace()
    # res = ['Feature%s' % x for x in range(0, 10)]
    return vocab_from_values_with_count(res, 'Feature')


@provider(IVocabularyFactory)
def a2018_mru_ind(context):
    if not hasattr(context, 'mapper_class'):
        context_orig = context
        context = context.context

    json_str = json.loads(context.json())
    json_str_subform = json.loads(context.subform.json())
    mapper_class = context.mapper_class
    ges_comp_mc = context.ges_components_mc
    features_mc = context.features_mc
    marine_mc = context.marine_mc

    countries = get_json_subform_data(json_str, 'Country Code')
    ges_components = get_json_subform_data(json_str_subform, 'GES Component')
    features = get_json_subform_data(json_str_subform, 'Features')

    mc_countries = sql2018.ReportedInformation
    conditions = []
    if countries:
        conditions.append(mc_countries.CountryCode.in_(countries))

    count, ids_indicator = db.get_all_records_outerjoin(
        mapper_class,
        mc_countries,
        *conditions
    )
    ids_indicator = [int(x.Id) for x in ids_indicator]

    conditions = list()
    if features:
        conditions.append(features_mc.Feature.in_(features))
    if ges_components:
        conditions.append(ges_comp_mc.GESComponent.in_(ges_components))
    count, ids_ind_ass = db.get_all_records_outerjoin(
        ges_comp_mc,
        features_mc,
        *conditions
    )
    ids_ind_ass = [int(x.IdIndicatorAssessment) for x in ids_ind_ass]

    ids_indicator = tuple(set(ids_indicator) & set(ids_ind_ass))

    count, marine_units = db.get_all_records_join(
        [mapper_class.Id, marine_mc.MarineReportingUnit],
        marine_mc,
        mapper_class.Id.in_(ids_indicator),
    )
    res = marine_units
    # res = [x.MarineReportingUnit for x in marine_units]
    # res = tuple(set(res))

    # res = db.get_unique_from_mapper(
    #     marine_mc,
    #     'MarineReportingUnit',
    #     marine_mc.IdIndicatorAssessment.in_(ids_ges_comp)
    # )

    # res = ['MarineReportingUnit%s' % x for x in range(0, 10)]
    return vocab_from_values_with_count(res, 'MarineReportingUnit')
