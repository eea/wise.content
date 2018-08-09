from collections import defaultdict
from pprint import pprint

from zope.interface import Interface, implements, provider
from zope.schema import Choice  # , List
from zope.schema.interfaces import IVocabularyFactory

from plone.z3cform.layout import FormWrapper, wrap_form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, sql, sql2018
from z3c.form.field import Fields
from z3c.form.form import Form

from .db import threadlocals
from .vocabulary import db_vocab, vocab_from_values


class MainFormWrapper(FormWrapper):
    """ Override mainform wrapper to be able to return XLS file
    """

    index = ViewPageTemplateFile('pt/layout.pt')

    def __init__(self, context, request):
        FormWrapper.__init__(self, context, request)
        threadlocals.session_name = self.form.session_name

    # def render(self):
    #    if 'text/html' not in self.request.response.getHeader('Content-Type'):
    #         return self.contents
    #
    #     return super(MainFormWrapper, self).render()


class IComplianceForm(Interface):
    country = Choice(
        title=u"Country",
        vocabulary="compliance_countries",
        required=True
    )
    report_type = Choice(
        title=u"Report Type",
        vocabulary="compliance_report_types",
        required=True,
    )


class ComplianceForm(Form):
    """ The main forms need to inherit from this clas
    """

    implements(IComplianceForm)
    template = ViewPageTemplateFile('pt/complianceform.pt')
    ignoreContext = True
    reset_page = False
    subform = None
    fields = Fields(IComplianceForm)
    session_name = 'session_2018'

    # @buttonAndHandler(u'Apply filters', name='continue')
    # def handle_continue(self, action):
    #     self.reset_page = True


ComplianceFormView = wrap_form(ComplianceForm, MainFormWrapper)


@provider(IVocabularyFactory)
def compliance_countries(context):
    return db_vocab(sql2018.ReportingHistory, 'CountryCode')


@provider(IVocabularyFactory)
def compliance_report_types(context):
    return vocab_from_values([])


def row_to_dict(table, row):
    cols = table.c.keys()
    res = {k: v for k, v in zip(cols, row)}

    return res


class DeterminationOfGES2012(BrowserView):
    country = 'LV'

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
            m.FeatureType == 'GES criterion',
            m.RFCode.like('{}.%'.format(nr)),
            m.FeatureRelevant == 'Y',
            m.FeatureReported == 'Y',
        )

        return res

    def get_grouped_indicators_feature_pressure(self, muids, criterions):
        # returns a dict key Indicator, value: list of feature pressures
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
            sql.MSFD11CommonLabel.group == 'list-GESIndicator',
        )

        return [(x.value, x.Text) for x in res]

    def get_indicator_descriptors(self, muids):
        count, res = db.get_all_records(
            sql.MSFD9Descriptor,
            sql.MSFD9Descriptor.MarineUnitID.in_(muids),
            # sql.MSFD9Descriptor.group == 'list-GESIndicator',
        )

        return res

    def get_ges_descriptions(self, indicators):
        res = {}

        for indic in indicators:
            res[indic.ReportingFeature] = indic.DescriptionGES

        return res

    def __call__(self):
        threadlocals.session_name = 'session'
        self.country_name = self.get_country_name()
        self.regions = self.get_regions()

        # TODO: optimize this with a single function and a single query (w/
        # JOIN)
        self.descriptors = self.get_ges_descriptors()
        self.descs = [(d, self.get_ges_descriptor_label(d))
                      for d in self.descriptors]

        self.muids = self.get_marine_unit_ids()

        desc = 'D5'
        self.criterions = self.get_ges_criterions(desc)

        self.indics = self.get_grouped_indicators_feature_pressure(
            self.muids, self.criterions)

        self.criterion_labels = dict(
            self.get_criterion_labels(self.criterions)
        )

        self.indicators = self.get_indicator_descriptors(self.muids)

        indicator_ids = self.indics.keys()
        res = self.get_ges_descriptions(self.indicators)
        self.ges_descriptions = {k: v
                                 for k, v in res.items() if k in indicator_ids}

        return self.index()
