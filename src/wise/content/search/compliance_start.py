# -*- coding: utf-8 -*-

from UserDict import UserDict

from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.schema import Choice

from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from .base import MainFormWrapper as BaseFormWrapper
from .base import BaseEnhancedForm, EmbededForm
from .interfaces import IMainForm
from .vocabulary import vocab_from_values

# definition of what pages we need to implement
COMPLIANCE_PAGES = [
    # title, explanation
    ('National descriptor assessment',
     'National descriptor MS reports and Commission assessments'),
    ('Regional descriptor assessments',
     'Regional descriptor MS reports and Commission assessments'),
    ('National overviews', 'National overview for an MS'),
    ('Regional overviews', 'Regional overview for all MS in a region',),
]

assessment_environmental_status_A = [
    ('Yes',
     'Yes, based on threshold value and, where appropriate, proportion value'),
    ('Yes-LowRisk',
     'Yes, based on low risk'),
    ('No',
     'No, based on threshold value and, where appropriate, proportion value'),
    ('Unknown',	'Unknown'),
    ('NotAssessed',	'Not assessed'),
]


ASSESSMENT_TOPICS = [
    'National summary',
    'Regional summary',
    'GES Descriptor (see term list)',
    'Horizontal targets',
    'Horizontal measures',
    'Geographic areas',
    'Regional cooperation',
]


ASSESSED_ARTICLES = [
    'Art. 3(1) Marine waters',
    'Art. 4/2017 Decision: Marine regions, subregions, and subdivisions '
    '(MRUs)',
    'Art. 6 Regional cooperation',
    'Art. 7 Competent authorities',
    'Art. 8 Initial assessment (and Art. 17 updates)',
    'Art. 9 Determination of GES (and Art. 17 updates) ',
    'Art. 10 Environmental targets (and Art. 17 updates)',
    'Art. 11 Monitoring programmes (and Art. 17 updates)',
    'Art. 13 Programme of measures (and Art. 17 updates)',
    'Art. 14 Exceptions (and Art. 17 updates)',
    'Art. 18 Interim report on programme of measures',
    'Art. 19(3) Access to data',
]


REPORTING_DEADLINES = [
    '20110115',
    '20121015',
    '20141015',
    '20160331',
    '20181015',
    '20181231',
    '20201015',
    '20220331',
    '20241015',
]


class IMainAssessmentForm(Interface):
    member_state = Choice(
        title=u"Country",
        vocabulary="wise_search_member_states",
        required=False,
        default='',
    )


class MainAssessmentForm(BaseEnhancedForm, Form):
    implements(IMainForm)
    template = ViewPageTemplateFile('pt/compliance-start.pt')
    ignoreContext = True
    reset_page = False
    subform = None
    subform_content = None
    fields = Fields(IMainAssessmentForm)
    css_class = 'compliance-form-main'
    session_name = 'session'

    main_forms = (
        ('compliance-start', ('Compliance', '')),
    )

    def __init__(self, context, request):
        Form.__init__(self, context, request)

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        pass

    def get_subform(self):
        return AssessmentTopicForm(self, self.request)

    def update(self):
        super(MainAssessmentForm, self).update()
        self.data, self.errors = self.extractData()

        has_values = self.data.values() and all(self.data.values())

        if has_values:
            self.subform = self.get_subform()

            if self.subform:
                # we need to update and "execute" the subforms to be able to
                # discover them, because the decision process regarding
                # discovery is done in the update() method of subforms
                self.subform_content = self.subform()
                # self.subform.update()


class MainFormWrapper(BaseFormWrapper):
    index = ViewPageTemplateFile('pt/compliance-layout.pt')


MainAssessmentFormView = wrap_form(MainAssessmentForm, MainFormWrapper)


class IAssessmentTopic(Interface):
    """
    """
    assessment_topic = Choice(
        title=u"Assessment topic",
        vocabulary=vocab_from_values(ASSESSMENT_TOPICS),
        required=False,
    )


class AssessmentTopicForm(EmbededForm):
    """ Select the memberstate, region, area form
    """

    fields = Fields(IAssessmentTopic)

    def get_subform(self):
        return ArticleForm(self, self.request)


class IArticleForm(Interface):
    """
    """
    assessed_article = Choice(
        title=u"Assessed article",
        vocabulary=vocab_from_values(ASSESSED_ARTICLES),
        required=False,
    )


class ArticleForm(EmbededForm):
    """
    """

    fields = Fields(IArticleForm)

    def get_subform(self):
        return ReportingDeadlineForm(self, self.request)


class IReportingDeadline(Interface):
    """
    """
    reporting_deadline = Choice(
        title=u"Reporting deadline",
        vocabulary=vocab_from_values(REPORTING_DEADLINES),
        required=False,
    )


class ReportingDeadlineForm(EmbededForm):
    """
    """

    fields = Fields(IReportingDeadline)

    def get_subform(self):
        return AssessmentDisplayForm(self, self.request)


class AssessmentDisplayForm(EmbededForm):
    """
    """
    template = ViewPageTemplateFile('pt/assessment_display.pt')

    def get_assessed_article(self):
        parent = self
        article = None

        while True:
            if not hasattr(parent, 'data'):
                return []
            article = parent.data.get('assessed_article')

            if article:
                break
            else:
                parent = parent.context

        return article

    def update(self):
        res = super(AssessmentDisplayForm, self).update()
        self.contents = ''
        article = self.get_assessed_article()

        if article == 'Art. 8 Initial assessment (and Art. 17 updates)':
            self.contents = getMultiAdapter((self, self.request),
                                            name='deter')()

        return res


class Leaf(object):
    """ A generic leaf in a tree. Behaves somehow like a tree
    """

    children = ()

    def __init__(self, name, children=None):
        self.name = name
        self.children = [Leaf(c) for c in (children or ())]

    def __getitem__(self, name):
        for c in self.children:
            if c.name == name:
                return c
        raise KeyError

    def __setitem__(self, name, v):
        v.name = name
        self.children.append(v)


# evidences_criteria = [
#     'Primary criterion used',
#     'Primary criterion replaced with secondary criterion',
#     'Primary criterion not used',
#     'Secondary criterion used',
#     'Secondary criterion used instead of primary criterion',
#     'Secondary criterion not used',
#     '2010 criterion/indicator used',
#     '2010 criterion/indicator not used',
#     'Other criterion (indicator) used',
#     'Not relevant',
# ]

# art9_assessment_criterias = ['Adequacy', 'Coherence']

L = Leaf    # short alias

hierarchy = [
    'MSFD article', 'AssessmentCriteria', 'AssessedInformation', 'Evidence'
]

articles = L(
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
