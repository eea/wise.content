from zope.interface import implements, provider
from zope.schema.interfaces import IContextSourceBinder, IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from wise.content.search import db

from .utils import FORMS, SUBFORMS


class SubFormsVocabulary(SimpleVocabulary):
    """ An hackish vocabulary that retrieves subform names for a form
    """

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


@provider(IVocabularyFactory)
def get_member_states_vb_factory(context):
    res = db.get_member_states()
    terms = [SimpleTerm(x, x, x) for x in res]
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def get_region_subregions_vb_factory(context):
    res = db.get_regions_subregions()
    terms = [SimpleTerm(x, x, x) for x in res]
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def get_area_type_vb_factory(context):
    res = db.get_area_types()
    terms = [SimpleTerm(x, x, x) for x in res]
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def articles_vocabulary_factory(context):
    # TODO: sort terms first
    terms = [SimpleTerm(k, k, v.title) for k, v in FORMS.items()]
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def marine_unit_id_vocab_factory(context):
    data = context.data
    ids = db.get_marine_unit_ids(**data)
    terms = [SimpleTerm(x, x, x) for x in ids]

    return SimpleVocabulary(terms)
