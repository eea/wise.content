# -*- coding: utf-8 -*-

""" Module to generate the feature list based on terms
"""

import csv
from collections import defaultdict

from pkg_resources import resource_filename
from zope.schema.vocabulary import SimpleVocabulary

from z3c.formwidget.optgroup.widget import OptgroupTerm


def parse_features_file():
    csv_f = resource_filename('wise.content',
                              'search/data/features.tsv')

    res = defaultdict(list)
    with open(csv_f, 'rb') as csvfile:
        csv_file = csv.reader(csvfile, delimiter='\t')

        for row in csv_file:
            if not (len(row) == 8 and row[-1].lower() == 'y'):
                continue
            res[row[0]].append((row[1], row[2]))

    return res


FEATURES = parse_features_file()


def get_feature_terms():
    terms = []
    seen = []

    for group_name, features in FEATURES.items():
        for (key, title) in features:
            if key in seen:
                continue
            seen.append(key)
            term = OptgroupTerm(value=key, token=key, title=title,
                                optgroup=group_name)
            terms.append(term)

    return terms


features_vocabulary = SimpleVocabulary(get_feature_terms())
