# -*- coding: utf-8 -*-

""" Module to generate the feature list based on terms
"""

import csv
from collections import defaultdict

from pkg_resources import resource_filename
from zope.schema.vocabulary import SimpleVocabulary

from z3c.formwidget.optgroup.widget import OptgroupTerm

from .db import get_all_records, threadlocals, switch_session
from .sql import t_MSFD9_Features
from .vocabulary import LABELS

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


def get_feature_terms_old():
    terms = []
    seen = []

    for group_name, features in FEATURES.items():
        if 'activity' in group_name.lower():
            continue

        for (key, title) in features:
            if key in seen:
                continue
            seen.append(key)
            term = OptgroupTerm(value=key, token=key, title=title,
                                optgroup=group_name)
            terms.append(term)

    return terms


@switch_session
def get_feature_terms():
    threadlocals.session_name = 'session'

    terms = []
    seen = []

    count, db_res = get_all_records(
        t_MSFD9_Features
    )
    # res = defaultdict(list)

    for row in db_res:
        feature = row[4]
        impact = row[2]
        if impact in seen or feature is None:
            continue

        seen.append(impact)
        # res[feature].append(impact)
        label = LABELS.get(impact, impact)
        label_split = label.split(':')
        label_final = label_split[1].strip() if len(label_split) > 1 else label

        term = OptgroupTerm(value=impact, token=impact,
                            title=label_final,
                            optgroup=feature)
        terms.append(term)

    return terms


features_vocabulary = SimpleVocabulary(get_feature_terms())
