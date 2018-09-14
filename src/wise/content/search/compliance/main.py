# -*- coding: utf-8 -*-
from zope.component import getMultiAdapter
from zope.interface import Interface, implements
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from plone.z3cform.layout import wrap_form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.form import Form

from ..base import MainFormWrapper as BaseFormWrapper
from ..base import BaseEnhancedForm, EmbededForm
from ..interfaces import IMainForm
from ..vocabulary import vocab_from_values
from .nat_desc import DeterminationOfGES2012


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
    template = ViewPageTemplateFile('../pt/compliance-main.pt')
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

                # self.subform.update()


class MainFormWrapper(BaseFormWrapper):
    index = ViewPageTemplateFile('../pt/compliance-layout.pt')


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


# def vocab_from_dict(d):
#     """ Build a zope.schema vocabulary from a dict of value: title shape
#     """
#     terms = []
#
#     for k, v in d.items():
#         term = SimpleTerm(k, k, v)
#         terms.append(term)
#
#     return SimpleVocabulary(terms)


def vocab_from_pairs(pairs):
    """ Build a zope.schema vocabulary from pairs of (value(token), title)
    """
    terms = []

    for val, title in pairs:
        term = SimpleTerm(val, val, title)
        terms.append(term)

    return SimpleVocabulary(terms)


def vocab_from_list(values):
    terms = [SimpleTerm(x, x, x) for x in values]

    return SimpleVocabulary(terms)


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


ASSESSED_ARTICLES = (
    ('art3', 'Art. 3(1) Marine waters',),
    ('art4', 'Art. 4/2017 Decision: Marine regions, subregions, and subdivisions '),
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


class IArticle(Interface):
    article = Choice(
        title=u"Article",
        vocabulary=vocab_from_pairs(ASSESSED_ARTICLES),
        required=False,
    )


class ArticleForm(EmbededForm):
    fields = Fields(IArticle)

    def get_subform(self):
        article = self.get_form_data_by_key(self, 'article')
        descriptor = self.get_form_data_by_key(self, 'descriptor')
        member_state = self.get_form_data_by_key(self, 'member_state')

        self.request.form['article'] = article
        # self.request.form['report_type'] = descriptor
        self.request.form['country'] = member_state

        view = getMultiAdapter((self, self.request), name='deter')

        # return DeterminationOfGES2012(self, self.request)
        return view


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
