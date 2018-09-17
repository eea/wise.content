""" Classes and views to implement the National Descriptors compliance page
"""
from collections import defaultdict

from sqlalchemy import and_, or_
from zope.interface import Interface
from zope.schema import Text, TextLine

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, sql  # , sql2018
from z3c.form.field import Fields

from ..base import BaseUtil, EmbededForm
from ..db import switch_session, threadlocals
from .base import Container
from .nd_A8 import Article8
from .nd_A10 import Article10
from .vocabulary import ASSESSED_ARTICLES, form_structure


def row_to_dict(table, row):
    cols = table.c.keys()
    res = {k: v for k, v in zip(cols, row)}

    return res


class DeterminationOfGES2012(BrowserView, Article8, Article10):
    """ WIP on compliance tables
    """

    art3 = ViewPageTemplateFile('../pt/compliance-a10.pt')
    art8 = ViewPageTemplateFile('../pt/compliance-a8.pt')
    art9 = ViewPageTemplateFile('../pt/compliance-a9.pt')
    art10 = ViewPageTemplateFile('../pt/compliance-a10.pt')

    def __init__(self, context, request):
        self.country = request.form.get('country', 'LV')
        self.descriptor = request.form.get('report_type', 'D5')
        self.article_template = request.form.get('article', 'art9')
        super(DeterminationOfGES2012, self).__init__(context, request)

    def get_country_name(self):
        count, obj = db.get_item_by_conditions(
            sql.MSFD11CommonLabel,
            'ID',
            sql.MSFD11CommonLabel.value == self.country,
            sql.MSFD11CommonLabel.group == 'list-countries',
        )

        return obj.Text

    def get_regions(self):
        t = sql.t_MSFD4_GegraphicalAreasID
        count, res = db.get_all_records(
            t,
            t.c.MemberState == self.country
        )

        res = [row_to_dict(t, r) for r in res]
        regions = set([x['RegionSubRegions'] for x in res])

        return regions

    def get_ges_descriptors(self):
        m = sql.MSFDFeaturesOverview
        res = db.get_unique_from_mapper(
            m, 'RFCode',
            m.FeatureType == 'GES descriptor'
        )

        return res

    def get_ges_descriptor_label(self, ges):
        count, obj = db.get_item_by_conditions(
            sql.MSFD11CommonLabel,
            'ID',
            sql.MSFD11CommonLabel.value == ges,
            sql.MSFD11CommonLabel.group == 'list-MonitoringProgramme',
        )

        if obj:
            return obj.Text

    def get_marine_unit_ids(self):
        t = sql.t_MSFD4_GegraphicalAreasID
        count, res = db.get_all_records(
            t,
            t.c.MemberState == self.country
        )

        res = [row_to_dict(t, r) for r in res]
        muids = set([x['MarineUnitID'] for x in res])

        return sorted(muids)

    def get_ges_criterions(self, descriptor):
        nr = descriptor[1:]
        m = sql.MSFDFeaturesOverview
        res = db.get_unique_from_mapper(
            m, 'RFCode',
            or_(
                and_(m.RFCode.like('{}.%'.format(nr)),
                     m.FeatureType == 'GES criterion',),
                and_(m.RFCode.like('{}'.format(descriptor)),
                     m.FeatureType == 'GES descriptor')
            ),
            m.FeatureRelevant == 'Y',
            m.FeatureReported == 'Y',
        )

        return res

    def get_indicators_with_feature_pressures(self, muids, criterions):
        # returns a dict key Indicator, value: list of feature pressures
        # {u'5.2.2-indicator 5.2C': set([u'Transparency', u'InputN_Psubst']),
        t = sql.t_MSFD9_Features
        count, res = db.get_all_records(
            t,
            t.c.MarineUnitID.in_(muids),
        )
        res = [row_to_dict(t, r) for r in res]

        indicators = defaultdict(set)

        for row in res:
            rf = row['ReportingFeature']
            indicators[rf].add(row['FeaturesPressuresImpacts'])

        res = {}

        for k, v in indicators.items():
            flag = False

            for crit in criterions:
                if k.startswith(crit):
                    flag = True

            if flag:
                res[k] = v

        return res

    def get_criterion_labels(self, criterions):
        count, res = db.get_all_records(
            sql.MSFD11CommonLabel,
            sql.MSFD11CommonLabel.value.in_(criterions),
            sql.MSFD11CommonLabel.group.in_(('list-GESIndicator',
                                             'list-GESCriteria')),
        )

        return [(x.value, x.Text) for x in res]

    def get_indicator_descriptors(self, muids, available_indicators):
        count, res = db.get_all_records(
            sql.MSFD9Descriptor,
            sql.MSFD9Descriptor.MarineUnitID.in_(muids),
            sql.MSFD9Descriptor.ReportingFeature.in_(available_indicators)
        )

        return res

    def get_ges_descriptions(self, indicators):
        res = {}

        for indic in indicators:
            res[indic.ReportingFeature] = indic.DescriptionGES

        return res

    def get_descriptors_for_muid(self, muid):
        return sorted(
            [x for x in self.indicator_descriptors if x.MarineUnitID == muid],
            key=lambda o: o.ReportingFeature
        )

    @switch_session
    def __call__(self):
        threadlocals.session_name = 'session'

        # descriptor = 'D5'
        # descriptor_prefix = descriptor[1:]

        self.country_name = self.get_country_name()
        self.regions = self.get_regions()

        # TODO: optimize this with a single function and a single query (w/
        # JOIN)
        self.descriptors = self.get_ges_descriptors()
        self.descs = {}

        for d in self.descriptors:
            self.descs[d] = self.get_ges_descriptor_label(d)
        self.desc_label = self.descs.get(self.descriptor,
                                         'Descriptor Not Found')

        self.muids = self.get_marine_unit_ids()

        self.criterions = self.get_ges_criterions(self.descriptor)

        # {u'5.2.2-indicator 5.2C': set([u'Transparency', u'InputN_Psubst']),
        self.indic_w_p = self.get_indicators_with_feature_pressures(
            self.muids, self.criterions
        )

        self.criterion_labels = dict(
            self.get_criterion_labels(self.criterions)
        )
        # add D5 criterion to the criterion lists too
        self.criterion_labels.update({self.descriptor: self.desc_label})

        self.indicator_descriptors = self.get_indicator_descriptors(
            self.muids, self.indic_w_p.keys()
        )

        # indicator_ids = self.indics.keys()
        # res = self.get_ges_descriptions(self.indicators)
        # self.ges_descriptions = {k: v
        #                          for k, v in res.items()
        #                          if k in indicator_ids}

        # TODO create a function for this
        self.crit_lab_indics = defaultdict(list)

        for crit_lab in self.criterion_labels.keys():
            self.crit_lab_indics[crit_lab] = []

            for ind in self.indic_w_p.keys():
                norm_ind = ind.split('-')[0]

                if crit_lab == norm_ind:
                    self.crit_lab_indics[crit_lab].append(ind)

            if not self.crit_lab_indics[crit_lab]:
                self.crit_lab_indics[crit_lab].append('')
        self.crit_lab_indics[u'GESOther'] = ['']

        self.colspan = len([item
                            for sublist in self.crit_lab_indics.values()

                            for item in sublist])

        # Article 8 stuff
        # self.art8data = self.get_data_reported('BAL- LV- AA- 001',
        # self.descriptor)

        template = getattr(self, self.article_template)

        return template


class ReportData2018(BrowserView):
    def __call__(self):
        return 'report data 2018'


class ReportHeaderForm2018(EmbededForm):
    def __call__(self):
        return 'report header form 2018'


class AssessmentHeaderForm2018(BrowserView):
    def __call__(self):
        return 'assessment header form 2018'


class AssessmentDataForm2018(Container):
    """
    """
    def build_form(self):
        article = form_structure['Art9']
        assessment_criterias = article.children

        for criteria in assessment_criterias:
            pass

        import pdb; pdb.set_trace()

        return lambda: 'bla'

    def update(self):
        self.children = [
            BasicAssessmentDataForm2018(self, self.request),
            self.build_form(),
            SummaryAssessmentDataForm2018(self, self.request),
        ]


class IBasicAssessmentData2018(Interface):
    """ The basic fields for the assessment data for 2018
    """
    reporting_area = TextLine(title=u'Reporting Area')
    feature_reported = TextLine(title=u'Reporting Area')


class BasicAssessmentDataForm2018(EmbededForm):
    """
    """
    def __init__(self, context, request):
        super(BasicAssessmentDataForm2018, self).__init__(context, request)
        fields = [IBasicAssessmentData2018]
        self.fields = Fields(*fields)


class ISummaryAssessmentData2018(Interface):
    assessment_summary = Text(title=u'Assessment summary')
    recommendations = Text(title=u'Recomandations')


class SummaryAssessmentDataForm2018(EmbededForm):
    """
    """
    def __init__(self, context, request):
        super(SummaryAssessmentDataForm2018, self).__init__(context, request)
        fields = [ISummaryAssessmentData2018]
        self.fields = Fields(*fields)
