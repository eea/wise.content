import csv
import logging
import json

from lxml.etree import parse
from pkg_resources import resource_filename
from sqlalchemy.sql.schema import Table
from sqlalchemy import and_
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from wise.content.search import db, sql

from .utils import FORMS, FORMS_ART11, LABELS, SUBFORMS


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


# TODO not used, delete this later
@provider(IVocabularyFactory)
def monitoring_subprogramme_names(context):
    terms = [SimpleTerm(v, k, v.title) for k, v in FORMS_ART11.items()]
    terms.sort(key=lambda t: t.title)
    vocab = SimpleVocabulary(terms)

    return vocab


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

    # import pdb; pdb.set_trace()

    return vocab


@provider(IVocabularyFactory)
def art11_region(context):
    if not hasattr(context, 'subform'):
        json_str = json.loads(context.json())
        mp_type_ids = context.context.get_mp_type_ids()
    else:
        json_str = json.loads(context.subform.json())
        mp_type_ids = context.get_mp_type_ids()
    countries_form_data = [field['options'] for field in json_str['fields'] if field['label'] == 'Country']
    countries = [country['value'] for country in countries_form_data[0] if country['checked']]

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
def art11_marine_unit_id(context):
    if not hasattr(context, 'subform'):
        json_str = json.loads(context.json())
    else:
        json_str = json.loads(context.subform.json())
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
        sql.MSFD11MP.MON.in_(mon_ids)
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
