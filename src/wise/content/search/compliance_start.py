# -*- coding: utf-8 -*-

from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.schema import Choice

from plone.z3cform.layout import wrap_form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from .base import MainFormWrapper as BaseFormWrapper
from .base import BaseEnhancedForm, EmbededForm
from .interfaces import IMainForm
from .vocabulary import vocab_from_values

# assessment_environmental_status_A = [
#     ('Yes',
#      'Yes, based on threshold value and, where appropriate, proportion
#      value'),
#     ('Yes-LowRisk',
#      'Yes, based on low risk'),
#     ('No',
#      'No, based on threshold value and, where appropriate, proportion
#      value'),
#     ('Unknown',	'Unknown'),
#     ('NotAssessed',	'Not assessed'),
# ]


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

MAIN_FORMS = [
    # view name, (title, explanation)
    ('comp-national-descriptor-assessment',
     ('National descriptor assessment',
      'National descriptor MS reports and Commission assessments'),
     ),
    ('comp-regional-descriptor-assessment',
     ('Regional descriptor assessments',
      'Regional descriptor MS reports and Commission assessments'),
     ),
    ('comp-national-overviews',
     ('National overviews',
      'National overview for an MS'),
     ),
    ('comp-regional-overviews',
     ('Regional overviews',
      'Regional overview for all MS in a region',),
     ),
]


class StartComplianceView(BrowserView):
    main_forms = MAIN_FORMS
    name = 'compliance-start'


class IMemberState(Interface):
    member_state = Choice(
        title=u"Country",
        vocabulary="wise_search_member_states",
        required=False,
        default='',
    )


class MainAssessmentForm(BaseEnhancedForm, Form):
    # mostly similar to .base.MainForm
    implements(IMainForm)
    template = ViewPageTemplateFile('pt/compliance-start.pt')
    ignoreContext = True
    reset_page = False
    subform = None
    subform_content = None
    fields = Fields(IMemberState)
    css_class = 'compliance-form-main'
    session_name = 'session'

    main_forms = MAIN_FORMS

    def __init__(self, context, request):
        Form.__init__(self, context, request)

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        pass

    def get_subform(self):
        return self.subform(self, self.request)

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


class NationalDescriptorForm(MainAssessmentForm):
    assessment_topic = 'GES Descriptor (see term list)'

    subform_class = ArticleSelectForm


NationalDescriptorFormView = wrap_form(NationalDescriptorForm, MainFormWrapper)



# - assessment topic
#     - national descriptors
#         - choose country
#             - choose article
#                 - 2012 data
#                 - 2018 data
#             - fill in general data
#             - choose descriptor
#     - regional descriptors
#     - national overviews
#     - regional overviews
