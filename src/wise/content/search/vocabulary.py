from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from .db import get_area_types, get_member_states, get_regions_subregions
from .utils import FORMS, SUBFORMS


class SubFormsVocabulary(SimpleVocabulary):
    """ An hackish vocabulary that retrieves subform names for a form
    """

    def __init__(self, form_name):
        self._form_name = form_name

    @property
    def _terms(self):
        terms = []

        for n1, n2 in SUBFORMS.keys():
            if n1 == self._form_name:
                terms.append(SimpleTerm(n2, n2, n2))

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
    res = get_member_states()
    terms = [SimpleTerm(x, x, x) for x in res]
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def get_region_subregions_vb_factory(context):
    res = get_regions_subregions()
    terms = [SimpleTerm(x, x, x) for x in res]
    vocab = SimpleVocabulary(terms)

    return vocab


@provider(IVocabularyFactory)
def get_area_type_vb_factory(context):
    res = get_area_types()
    terms = [SimpleTerm(x, x, x) for x in res]
    vocab = SimpleVocabulary(terms)

    return vocab


# ARTICLES = [
#     ('a81c', 'Article 8.1c (Economic and social analysis)'),
# ]

# articles_vocabulary = SimpleVocabulary(
#     [SimpleTerm(a[0], a[0], a[1]) for a in ARTICLES]
# )
#
#
# @provider(IVocabularyFactory)
# def articles_vocabulary_factory(context):
#     return articles_vocabulary


# A81A_THEMES = [
#     'Ecosystem(s)',
#     'Functional group(s)',
#     'Habitat(s)',
#     'Species(s)',
#     'Other(s)',
#     'NIS Inventory',
#     'Physical',
# ]
#
# a81a_themes_vocabulary = SimpleVocabulary(
#     [SimpleTerm(a, a, a) for a in A81A_THEMES]
# )


# @provider(IVocabularyFactory)
# def a81a_themes_vocabulary_factory(context):
#     return vocab


# A81B_THEMES = [
#     'Extraction of fish and shellfish',
#     'Extraction of seaweed, maerl and other',
#     'Harzardous substances',
#     'Hydrological processes',
#     'Marine litter',
#     'Microbial pathogens',
#     'Non-indigenous species',
#     'Underwater noise',
#     'Nutrients',
#     'Physical damage',
#     'Pollutant events',
#     'Acidification',
# ]

# a81b_themes_vocabulary = SimpleVocabulary(
#     [SimpleTerm(a, a, a) for a in A81B_THEMES]
# )


@provider(IVocabularyFactory)
def a81b_themes_vocabulary_factory(context):
    return a81b_themes_vocabulary


@provider(IVocabularyFactory)
def articles_vocabulary_factory(context):
    # TODO: sort terms first
    terms = [SimpleTerm(k, k, v.title) for k, v in FORMS.items()]
    vocab = SimpleVocabulary(terms)

    return vocab
