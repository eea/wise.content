# -*- coding: utf-8 -*-

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


form_structure = L(
    'articles', [
        L('Art4'),
        L('Art8'),
        L('Art9', [
            L('Adequacy', [
                L('CriteriaUsed', [
                    L('Primary criterion used'),
                    L('Primary criterion replaced with secondary criterion'),
                    L('Primary criterion not used'),
                    L('Secondary criterion used'),
                    L('Secondary criterion used instead of primary criterion'),
                    L('Secondary criterion not used'),
                    L('2010 criterion/indicator used'),
                    L('2010 criterion/indicator not used'),
                    L('Other criterion (indicator) used'),
                    L('Not relevant'),
                ]),
                L('GESQualitative', [
                    L('Adapted from Annex I definition'),
                    L('Adapted from 2017 Decision'),
                    L('Adapted from 2010 Decision'),
                    L('Not relevant'),
                ]),
                L('GESQuantitative', [
                    L('Threshold values per MRU'),
                    L('No threshold values'),
                    L('Not relevant'),
                ]),
                L('GESAmbition', [
                    L('No GES extent threshold defined'),
                    L('Proportion value per MRU set'),
                    L('No proportion value set'),
                ]),
            ]),
            L('Coherence', [
                L('CriteriaUsed', [
                    L('Criterion used by all MS in region'),
                    L('Criterion used by ≥75% MS in region'),
                    L('Criterion used by ≥50% MS in region'),
                    L('Criterion used by ≥25% MS in region'),
                    L('Criterion used by ≤25% MS in region'),
                    L('Criterion used by all MS in subregion'),
                ]),
                L('GESQualitative', [
                    L('High'),
                    L('Moderate'),
                    L('Poor'),
                    L('Not relevant'),
                ]),
                L('GESQuantitative', [
                    L('All MS in region use EU (Directive, Regulation or Decision) values'),
                    L('All MS in region use regional (RSC) values'),
                    L('All MS in region use EU (WFD coastal) and regional (RSC offshore) values'),
                    L('All MS in region use EU (WFD coastal); and national (offshore) values'),
                    L('All MS in region use national values'),
                    L('Some MS in region use EU (Directive, Regulation or Decision) values and some MS use national values'),
                    L('Some MS in region use regional (RSC) values and some MS use national values'),
                    L('Not relevant'),
                ]),
                L('GESAmbition', [
                    L('GES extent value same/similar for all MS in region'),
                    L('GES extent value varies between MS in region'),
                    L('GES extent threshold varies markedly between MS'),
                    L('GES extent threshold not reported'),
                    L('GES proportion value same/similar for all MS in region'),
                    L('GES proportion value varies between MS in region'),
                    L('GES proportion value varies markedly between MS'),
                    L('GES proportion value not reported'),
                    L('Not relevant'),
                ]),
            ]),
        ]),
        L('Art10'),
    ])
