# -*- coding: utf-8 -*-
# from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.schema import Choice

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
from .vocabulary import articles_vocabulary, descriptors_vocabulary

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

# TODO: define the tabs selection label for mobile view (see wise-macros.pt)


class StartComplianceView(BrowserView):
    main_forms = MAIN_FORMS
    name = 'compliance-start'


class MainAssessmentForm(BaseEnhancedForm, Form):
    """ Base form for all main compliance view forms

    # mostly similar to .base.MainForm
    """
    implements(IMainForm)
    template = Template('../pt/mainform.pt')        # compliance-main
    ignoreContext = True
    reset_page = False
    subform = None
    subform_content = None
    fields = Fields()
    # css_class = 'compliance-form-main'
    session_name = 'session'

    main_forms = MAIN_FORMS
    _is_save = False

    def __init__(self, context, request):
        Form.__init__(self, context, request)
        self.save_handlers = []

    def add_save_handler(self, handler):
        self.save_handlers.append(handler)

    @buttonAndHandler(u'Apply filters', name='continue')
    def handle_continue(self, action):
        self._is_save = True

    def get_subform(self):
        if self.subform:
            return self.subform(self, self.request)

    def update(self):
        super(MainAssessmentForm, self).update()
        print ("===Doing main form update")
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

        if self._is_save:
            for handler in self.save_handlers:
                handler()


class MainFormWrapper(BaseFormWrapper):
    index = Template('../pt/layout.pt')     # compliance-


class IMemberState(Interface):
    member_state = Choice(
        title=u"Country",
        vocabulary="wise_search_member_states",
        required=False,
    )


class NationalDescriptorForm(MainAssessmentForm):
    assessment_topic = 'GES Descriptor (see term list)'
    fields = Fields(IMemberState)
    name = "comp-national-descriptor"

    form_id = 'wise-compliance-form'

    form_id_top = 'wise-compliance-form-top'

    form_container_class = 'wise-compliance-form-container'

    def get_subform(self):
        return GESDescriptorForm(self, self.request)


NationalDescriptorFormView = wrap_form(NationalDescriptorForm, MainFormWrapper)


class IGESDescriptor(Interface):
    descriptor = Choice(
        title=u"Descriptor",
        vocabulary=descriptors_vocabulary,
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
        vocabulary=articles_vocabulary,
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

    form_name = "national-descriptor-assessment-form"
    render = Template('../pt/container.pt')
    css_class = "left-side-form"

    def update(self):
        super(NationalDescriptorAssessmentForm, self).update()

        # a quick hack to allow splitting up the code reusing the concept of
        # subforms. Some of them are actually views. They're callbables that:
        # - render themselves
        # - answer to the save() method?
        self.subforms = [
            ReportHeaderForm2018(self, self.request),
            ReportData2018(self, self.request),
            AssessmentHeaderForm2018(self, self.request),
            AssessmentDataForm2018(self, self.request)
        ]

        for child in self.subforms:
            child.update()
