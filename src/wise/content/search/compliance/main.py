# -*- coding: utf-8 -*-
# from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from plone.z3cform.layout import wrap_form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import \
    ViewPageTemplateFile as Template
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from ..base import MainFormWrapper as BaseFormWrapper
from ..base import BaseEnhancedForm, EmbededForm
from ..interfaces import IMainForm
from .base import Container
from .nat_desc import (AssessmentDataForm2018, AssessmentHeaderForm2018,
                       ReportData2018, ReportHeaderForm2018)
from .vocabulary import ASSESSED_ARTICLES

MAIN_FORMS = [
    # view name, (title, explanation)
    ('comp-national-descriptor',
     ('National descriptor assessment',
      'National descriptor MS reports and Commission assessments'),
     ),
    ('comp-regional-descriptor',
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


class MainAssessmentForm(BaseEnhancedForm, Form):
    """ Base form for all main compliance view forms

    # mostly similar to .base.MainForm
    """
    implements(IMainForm)
    template = Template('../pt/compliance-main.pt')
    ignoreContext = True
    reset_page = False
    subform = None
    subform_content = None
    fields = Fields()
    css_class = 'compliance-form-main'
    session_name = 'session'

    main_forms = MAIN_FORMS

    def __init__(self, context, request):
        Form.__init__(self, context, request)

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        pass

    def get_subform(self):
        if self.subform:
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

                # with restore_session():
                # when using different sessions, we will need to restore
                # the self.session current session name
                self.subform_content = self.subform()


class MainFormWrapper(BaseFormWrapper):
    index = Template('../pt/compliance-layout.pt')


class IMemberState(Interface):
    member_state = Choice(
        title=u"Country",
        vocabulary="wise_search_member_states",
        required=False,
    )


class NationalDescriptorForm(MainAssessmentForm):
    assessment_topic = 'GES Descriptor (see term list)'
    fields = Fields(IMemberState)

    # subform_class = GESDescriptorForm

    def get_subform(self):
        return GESDescriptorForm(self, self.request)


NationalDescriptorFormView = wrap_form(NationalDescriptorForm, MainFormWrapper)

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


class IGESDescriptor(Interface):
    descriptor = Choice(
        title=u"Descriptor",
        vocabulary=vocab_from_pairs(GES_DESCRIPTORS),
        required=False,
        default='D5'
    )


class GESDescriptorForm(EmbededForm):
    fields = Fields(IGESDescriptor)

    def get_subform(self):
        return ArticleForm(self, self.request)


class IArticle(Interface):
    article = Choice(
        title=u"Article",
        vocabulary=vocab_from_pairs(ASSESSED_ARTICLES),
        required=False,
    )


class ArticleForm(EmbededForm):
    fields = Fields(IArticle)

    def get_subform(self):
        # def data(k):
        #     return self.get_form_data_by_key(self, k)
        #
        # self.request.form['country'] = data('member_state')
        # self.request.form['article'] = data('article')

        # self.request.form['report_type'] = descriptor
        # TODO: misssing?
        # descriptor = self.get_form_data_by_key(self, 'descriptor')

        # return getMultiAdapter((self, self.request), name='deter')

        return NationalDescriptorAssessmentForm(self, self.request)


class NationalDescriptorAssessmentForm(Container):
    """ Form to create and assess a national descriptor overview
    """
    layout = Template('../pt/container.pt')

    def update(self):
        super(NationalDescriptorAssessmentForm, self).update()

        # a quick hack to allow splitting up the code reusing the concept of
        # subforms. Some of them are actually views. They're callbables that:
        # - render themselves
        # - answer to the save() method?
        self.children = [
            ReportHeaderForm2018(self, self.request),
            ReportData2018(self, self.request),
            AssessmentHeaderForm2018(self, self.request),
            AssessmentDataForm2018(self, self.request)
        ]
