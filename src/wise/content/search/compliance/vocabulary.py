# -*- coding: utf-8 -*-

import csv

from pkg_resources import resource_filename
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from .base import Leaf as L

ASSESSED_ARTICLES = (
    ('art3', 'Art. 3(1) Marine waters',),
    ('art4', 'Art. 4/2017 Decision: Marine regions, subregions, '
     'and subdivisions '),
    ('art5', '(MRUs)', ),
    ('art6', 'Art. 6 Regional cooperation', ),
    ('art7', 'Art. 7 Competent authorities', ),
    ('art8', 'Art. 8 Initial assessment (and Art. 17 updates)', ),
    ('art9', 'Art. 9 Determination of GES (and Art. 17 updates) ', ),
    ('art10', 'Art. 10 Environmental targets (and Art. 17 updates)', ),
    ('art11', 'Art. 11 Monitoring programmes (and Art. 17 updates)', ),
    ('art13', 'Art. 13 Programme of measures (and Art. 17 updates)', ),
    ('art14', 'Art. 14 Exceptions (and Art. 17 updates)', ),
    ('art18', 'Art. 18 Interim report on programme of measures', ),
    ('art19', 'Art. 19(3) Access to data', ),
)


def parse_forms_file():
    csv_f = resource_filename('wise.content',
                              'search/data/forms.tsv')
    # hierarchy = [
    #     'MSFD article', 'AssessmentCriteria', 'AssessedInformation',
    #     'Evidence'
    # ]

    res = L('articles')

    with open(csv_f, 'rb') as csvfile:
        csv_file = csv.reader(csvfile, delimiter='\t')

        l1, l2, l3, l4 = None, None, None, None     # the 4 columns

        for row in csv_file:
            if not row:
                continue
            article, criteria, information, evidence = row

            l4 = L(evidence)

            if l3 is None or l3.name != information:
                l3 = L(information, [l4])
            else:
                l3.children.append(l4)

            if l2 is None or l2.name != criteria:
                l2 = L(criteria, [l3])
            else:
                l2.children.append(l3)

            if l1 is None or l1.name != article:
                l1 = L(article, [l2])
                res.children.append(l1)
            else:
                l1.children.append(l2)

    print res.children

    return res


form_structure = parse_forms_file()

# form_structure = L(
#     'articles', [
#         L('Art4', [
#             L('Adequacy', [
#                 L('MRUscales2017Decision', [
#                     L('Follow scales in 2017 Decision'),
#                     L('Partially follow scales in 2017 Decision'),
#                     L('Do not follow scales in 2017 Decision'),
#                     L('Not relevant'),
#                 ]),
#             ]),
#             L('Consistency', [
#             ]),
#             L('Coherence', [
#             ]),
#         ]),
#         L('Art8'),
#         L('Art9', [
#             L('Adequacy', [
#                 L('CriteriaUsed', [
#                     L('Primary criterion used'),
#                     L('Primary criterion replaced with secondary criterion'),
#                     L('Primary criterion not used'),
#                     L('Secondary criterion used'),
#                     L('Secondary criterion used instead of primary criterion'),
#                     L('Secondary criterion not used'),
#                     L('2010 criterion/indicator used'),
#                     L('2010 criterion/indicator not used'),
#                     L('Other criterion (indicator) used'),
#                     L('Not relevant'),
#                 ]),
#                 L('GESQualitative', [
#                     L('Adapted from Annex I definition'),
#                     L('Adapted from 2017 Decision'),
#                     L('Adapted from 2010 Decision'),
#                     L('Not relevant'),
#                 ]),
#                 L('GESQuantitative', [
#                     L('Threshold values per MRU'),
#                     L('No threshold values'),
#                     L('Not relevant'),
#                 ]),
#                 L('GESAmbition', [
#                     L('No GES extent threshold defined'),
#                     L('Proportion value per MRU set'),
#                     L('No proportion value set'),
#                 ]),
#             ]),
#             L('Coherence', [
#                 L('CriteriaUsed', [
#                     L('Criterion used by all MS in region'),
#                     L('Criterion used by ≥75% MS in region'),
#                     L('Criterion used by ≥50% MS in region'),
#                     L('Criterion used by ≥25% MS in region'),
#                     L('Criterion used by ≤25% MS in region'),
#                     L('Criterion used by all MS in subregion'),
#                 ]),
#                 L('GESQualitative', [
#                     L('High'),
#                     L('Moderate'),
#                     L('Poor'),
#                     L('Not relevant'),
#                 ]),
#                 L('GESQuantitative', [
#                     L('All MS in region use EU (Directive, Regulation or Decision) values'),
#                     L('All MS in region use regional (RSC) values'),
#                     L('All MS in region use EU (WFD coastal) and regional (RSC offshore) values'),
#                     L('All MS in region use EU (WFD coastal); and national (offshore) values'),
#                     L('All MS in region use national values'),
#                     L('Some MS in region use EU (Directive, Regulation or Decision) values and some MS use national values'),
#                     L('Some MS in region use regional (RSC) values and some MS use national values'),
#                     L('Not relevant'),
#                 ]),
#                 L('GESAmbition', [
#                     L('GES extent value same/similar for all MS in region'),
#                     L('GES extent value varies between MS in region'),
#                     L('GES extent threshold varies markedly between MS'),
#                     L('GES extent threshold not reported'),
#                     L('GES proportion value same/similar for all MS in region'),
#                     L('GES proportion value varies between MS in region'),
#                     L('GES proportion value varies markedly between MS'),
#                     L('GES proportion value not reported'),
#                     L('Not relevant'),
#                 ]),
#             ]),
#         ]),
#         L('Art10'),
#     ])


# TODO: sort this vocabulary (somehow)
GES_DESCRIPTORS = (
    ('D1', 'D1 Biodiversity'),
    ('D1 Birds', 'D1 Biodiversity – birds'),
    ('D1 Cephalopods', 'D1 Biodiversity –  cephalopods'),
    ('D1 Fish', 'D1 Biodiversity – fish'),
    ('D1 Mammals', 'D1 Biodiversity – mammals'),
    ('D1 Pelagic habitats', 'D1 Biodiversity – pelagic habitats'),
    ('D1 Reptiles', 'D1 Biodiversity – reptiles'),
    ('D2', 'D2 Non-indigenous species'),
    ('D3', 'D3 Commercial fish and shellfish'),
    ('D4/D1', 'D4 Food webs/D1 Biodiversity - ecosystems'),
    ('D5', 'D5 Eutrophication'),
    ('D6/D1', 'D6 Sea-floor integrity/D1 Biodiversity - benthic habitats'),
    ('D7', 'D7 Hydrographical changes'),
    ('D8', 'D8 Contaminants'),
    ('D9', 'D9 Contaminants in seafood'),
    ('D10', 'D10 Marine litter'),
    ('D11', 'D11 Energy, incl. underwater noise'),
)


def vocab_from_pairs(pairs):
    """ Build a zope.schema vocabulary from pairs of (value(token), title)
    """
    terms = []

    for val, title in pairs:
        term = SimpleTerm(val, val, title)
        terms.append(term)

    return SimpleVocabulary(terms)


def vocab_from_list(values):
    return SimpleVocabulary([SimpleTerm(x, x, x) for x in values])


descriptors_vocabulary = vocab_from_pairs(GES_DESCRIPTORS)
articles_vocabulary = vocab_from_pairs(ASSESSED_ARTICLES)
