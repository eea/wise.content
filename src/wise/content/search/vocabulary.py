from lxml.etree import parse
from pkg_resources import resource_filename
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from wise.content.search import db, sql

from .utils import FORMS, SUBFORMS

LABELS = {}


def populate_labels():
    lines = []
    f = resource_filename('wise.content',
                          'search/data/MSCommon_1p0.xsd')
    e = parse(f)

    for node in e.xpath('//xs:documentation',
                        namespaces={'xs': "http://www.w3.org/2001/XMLSchema"}):
        text = node.text.strip()
        lines.extend(text.split('\n'))

    for line in lines:
        line = line.strip()
        eqpos = line.find('=')

        if eqpos == -1:
            continue

        if ' ' in line[:eqpos]:
            continue

        label, title = line.split('=', 1)

        if label in LABELS:
            continue

        LABELS[label] = title

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
    res = db.get_unique_from_table(table, column)
    terms = [SimpleTerm(x, x, LABELS.get(x, x)) for x in res]
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
    # TODO: sort terms first
    terms = [SimpleTerm(k, k, v.title) for k, v in FORMS.items()]
    terms.sort()
    vocab = SimpleVocabulary(terms)
    #import pdb; pdb.set_trace()

    return vocab


@provider(IVocabularyFactory)
def marine_unit_ids_vocab_factory(context):
    """ A list of MarineUnitIds based on geodata selected
    """
    data = context.data
    count, ids = db.get_marine_unit_ids(**data)
    terms = [SimpleTerm(x, x, x) for x in ids]

    return SimpleVocabulary(terms)


@provider(IVocabularyFactory)
def marine_unit_id_vocab_factory(context):
    """ A list of MarineUnitIds taken from parent form selection
    """
    ids = context.subform.get_available_marine_unit_ids()
    terms = [SimpleTerm(x, x, x) for x in ids]

    return SimpleVocabulary(terms)


# labels_vocabulary = SimpleVocabulary([SimpleTerm(k, k, v) for k, v in
#                                       LABELS.items()])
#
# def labels_vocabulary_factory(context):
#     return labels_vocabulary
