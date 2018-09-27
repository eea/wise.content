""" Classes and views to implement the National Descriptors compliance page
"""
from collections import defaultdict

from sqlalchemy import and_, or_
from zope.interface import Interface
from zope.schema import Choice, Text
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, sql, sql2018
from z3c.form.field import Fields

from ..base import BaseUtil, EmbededForm
from ..db import switch_session, threadlocals
from ..gescomponents import get_ges_criterions
from .base import Container
from .nd_A8 import Article8
from .nd_A10 import Article10
from .vocabulary import form_structure


def row_to_dict(table, row):
    cols = table.c.keys()
    res = {k: v for k, v in zip(cols, row)}

    return res


class Report2012(BrowserView, Article8, Article10, BaseUtil):

    """ WIP on compliance tables
    """

    # art3 = ViewPageTemplateFile('../pt/compliance-a10.pt')
    art8 = ViewPageTemplateFile('../pt/compliance-a8.pt')
    art9 = ViewPageTemplateFile('../pt/compliance-a9.pt')
    art10 = ViewPageTemplateFile('../pt/compliance-a10.pt')

    # def __init__(self, context, request):
    #     super(Report2012, self).__init__(context, request)

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

        data = self.get_flattened_data(self)

        self.country = data.get('member_state')
        self.descriptor = data.get('descriptor')
        self.article = data.get('article')

        if not self.country:
            return ''

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

        print "Will render report for ", self.article

        template = getattr(self, self.article, None)

        return template and template() or ""


class ReportData2018(BrowserView):
    """ TODO: get code in this
    """

    __call__ = ViewPageTemplateFile('../pt/report-header-display.pt')


class ReportHeaderForm2018(BrowserView):
    """ TODO: get code in this
    """

    def __call__(self):
        return ''

        return 'report header form 2018'


class AssessmentHeaderForm2018(BrowserView):
    """ TODO: get code in this
    """
    def __call__(self):
        return ''

        return 'assessment header form 2018'


def get_default_assessment_value(
        data_assess,
        article,
        feature,
        assess_crit,
        assess_info,
        ges_comp
        ):
    if not data_assess:
        return None

    val = [
        x.Evidence
        for x in data_assess
        if x.MSFDArticle == article and
            x.Feature == feature and
            x.AssessmentCriteria == assess_crit and
            x.AssessedInformation == assess_info and
            x.GESComponent_Target == ges_comp
    ]

    if val:
        return val[0]

    return None


additional_fields = {
    'Summary': 'Description_Summary',
    'Conclusion': 'Conclusion',
    # 'Score': 'Score'
}


class AssessmentDataForm2018(Container, BaseUtil):
    """ The assessment form for 2018
    """

    def __init__(self, context, request):
        super(AssessmentDataForm2018, self).__init__(context, request)
        main_form = self.get_main_form()
        main_form.add_save_handler(self.handle_save)
        self.subforms = []   # make subforms discoverable for saving

    def handle_save(self):
        # TODO: build records from the subforms
        print "Saving assessment form data"
        data = {}
        child_data = {}
        parent_data = self.get_flattened_data(self)

        for form in self.subforms:
            # import pdb; pdb.set_trace()
            data.update(form.data)

        for children in self.children:
            if hasattr(children, 'data'):
                child_data.update(children.data)

        # save in COM_General
        d_general = {}

        # TODO get Reporting_historyId
        d_general['Reporting_historyId'] = 48
        d_general['CountryCode'] = parent_data['member_state']

        d_general['AssessmentTopic'] = self.context.assessment_topic
        d_general['MSFDArticle'] = parent_data['article']

        # TODO get DateReportDue, ReportBy etc...
        d_general['DateReportDue'] = u'2011-01-15'
        d_general['ReportBy'] = u'Commission'
        d_general['SourceFile'] = ''
        d_general['DateReported'] = ''
        d_general['DateAssessed'] = ''
        d_general['Assessors'] = ''
        d_general['CommissionReport'] = ''

        mc = sql2018.COMGeneral
        if self.general_id:
            d_general['Id'] = [unicode(self.general_id)]
        # import pdb; pdb.set_trace()
        self.general_id = db.save_record(mc, **d_general)

        # import pdb; pdb.set_trace()

        # get COM_assessments data
        all_features_reported = parent_data['feature_reported']

        for feature_reported in all_features_reported:

            @switch_session
            def func():
                threadlocals.session_name = 'session_2018'

                count, res = db.get_all_records(
                    sql2018.COMAssessment,
                    and_(sql2018.COMAssessment.COM_GeneralId == self.general_id,
                         sql2018.COMAssessment.Feature == feature_reported)
                )
                return res

            assessment_data = func()

            # save in COM_Assessment
            for k, v in data.items():
                if not v:
                    continue

                d = {}

                # TODO get COM_GeneralId
                # d['COM_GeneralId'] = 12
                d['COM_GeneralId'] = self.general_id
                d['MSFDArticle'] = parent_data['article']
                d['Feature'] = feature_reported

                d['AssessmentCriteria'], d['AssessedInformation'], \
                    d['GESComponent_Target'] = k.split('_')

                # import pdb; pdb.set_trace()

                if d['GESComponent_Target'] in additional_fields.keys():
                    import pdb; pdb.set_trace()
                    field_name = d.pop('GESComponent_Target')
                    d[additional_fields[field_name]] = v
                else:
                    field_name = 'GESComponent_Target'
                    d['Evidence'] = v

                # TODO
                # 1 - create separate entry in COM_Assessments table for
                #   every Marine Unit ID ??????
                # 2 - save records one by one, or many at once

                for mru in parent_data['marine_unit_ids']:
                    d['MarineUnit'] = mru

                    id_assess = [
                        unicode(x.Id)
                        for x in assessment_data
                        if x.MarineUnit == mru and
                           x.AssessedInformation == d['AssessedInformation'] and
                           x.AssessmentCriteria == d['AssessmentCriteria'] and
                           getattr(x, field_name) == d.get(field_name)
                    ]

                    if id_assess:
                        d['Id'] = id_assess
                    # import pdb; pdb.set_trace()
                    db.save_record(sql2018.COMAssessment, **d)

        print data
        print child_data
        print parent_data

    def _build_subforms(self, tree):
        """ Build a form of options from a tree of options
        """
        base_name = tree.name
        # TODO: get list of descriptors?
        data = self.get_flattened_data(self)
        child_data = {}
        for children in self.children:
            if hasattr(children, 'data'):
                child_data.update(children.data)

        descriptor = data['descriptor']
        descriptor_criterions = get_ges_criterions(descriptor)

        forms = []

        # check if article was already assessed
        @switch_session
        def func():
            threadlocals.session_name = 'session_2018'

            mc = sql2018.COMGeneral
            conditions = []
            conditions.append(mc.CountryCode == data['member_state'])
            conditions.append(mc.AssessmentTopic == u'National summary')
            conditions.append(mc.MSFDArticle == data['article'])
            count, res = db.get_all_records(
                mc,
                *conditions
            )
            if not count:
                return [], None
            else:
                general_id = res[0].Id
                cnt, assess_data = db.get_all_records(
                    sql2018.COMAssessment,
                    sql2018.COMAssessment.COM_GeneralId == res[0].Id
                )
                return assess_data, general_id

        data_assess, self.general_id = func()

        # import pdb; pdb.set_trace()

        for row in tree.children:
            row_name = row.name

            form = EmbededForm(self, self.request)

            form.form_name = 'form' + row_name
            fields = []

            form.title = '{}: {}'.format(base_name, row_name)

            for crit in descriptor_criterions:
                # print crit

                field_title = u'{} {}: {}'.format(base_name, row_name,
                                                  crit.title)
                field_name = '{}_{}_{}'.format(base_name, row_name, crit.id)
                # choices = [''] + [x.name for x in row.children]
                choices = [x.name for x in row.children]
                terms = [SimpleTerm(c, i, c) for i, c in enumerate(choices)]

                default = get_default_assessment_value(
                    data_assess,
                    data['article'],  # MSFDArticle
                    data['feature_reported'],  # Feature
                    base_name,  # AssessmentCriteria
                    row_name,  # AssessedInformation
                    crit.id  # GESComponent_Target
                )

                # import pdb; pdb.set_trace()

                field = Choice(
                    title=field_title,
                    __name__=field_name,
                    vocabulary=SimpleVocabulary(terms),
                    required=False,
                    default=default,
                )
                fields.append(field)

            for f in additional_fields.keys():
                _title = u'{}: {} {}'.format(base_name, row_name, f)
                _name = '{}_{}_{}'.format(base_name, row_name, f)
                _field = Text(
                    title=_title,
                    __name__=_name,
                    required=False,
                )

                fields.append(_field)

            form.fields = Fields(*fields)

            forms.append(form)

        # print 'Forms', forms

        return forms

    def build_forms(self):
        article = self.get_flattened_data(self)['article'].capitalize()
        try:
            article = form_structure[article]
        except KeyError:    # article is not in form structure yet
            return
        assessment_criterias = article.children

        for criteria in assessment_criterias:
            subforms = self._build_subforms(criteria)

            for subform in subforms:
                self.subforms.append(subform)

    def render_subforms(self):
        out = u''

        for form in self.subforms:
            out += form()

        out = u'<div class="collapsed-container">{}</div>'.format(out)

        return out

    def update(self):
        print ("====Doing assessment data form update")
        self.children = [
            # BasicAssessmentDataForm2018(self, self.request),
            self.render_subforms,
            SummaryAssessmentDataForm2018(self, self.request),
        ]

        self.build_forms()


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
