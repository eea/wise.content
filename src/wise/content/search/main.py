from plone.z3cform.layout import wrap_form
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .a11 import StartArticle11Form
from .a1314 import StartArticle1314Form
from .base import (MAIN_FORMS, EmbededForm, ItemDisplayForm, MainForm,
                   MainFormWrapper)
from .sql_extra import MSCompetentAuthority
from .utils import get_form, scan


class StartView(BrowserView):
    main_forms = MAIN_FORMS
    name = 'msfd-start'


class StartMSCompetentAuthoritiesView(MainForm):
    name = 'msfd-ca'

    fields = Fields(interfaces.IMemberStates)
    fields['member_states'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return CompetentAuthorityItemDisplay(self, self.request)


class CompetentAuthorityItemDisplay(ItemDisplayForm):
    """ The implementation for the Article 9 (GES determination) form
    """
    mapper_class = MSCompetentAuthority
    order_field = 'C_CD'


class StartArticle8910Form(MainForm):
    """ Select one of the article: 8(a,b,c,d)/9/10
    """

    name = 'msfd-c1'

    fields = Fields(interfaces.IArticleSelect)
    session_name = 'session'

    def get_subform(self):
        if self.data['article']:
            return RegionForm(self, self.request)


class RegionForm(EmbededForm):
    """ Select the memberstate, region, area form
    """

    fields = Fields(interfaces.IStartArticles8910)
    fields['region_subregions'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return MemberStatesForm(self, self.request)


class MemberStatesForm(EmbededForm):
    fields = Fields(interfaces.IMemberStates)
    fields['member_states'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return AreaTypesForm(self, self.request)


class AreaTypesForm(EmbededForm):

    fields = Fields(interfaces.IAreaTypes)
    fields['area_types'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        # needed for marine unit ids vocabulary
        # TODO: is this still needed?
        self.data['member_states'] = self.context.data['member_states']
        self.data['region_subregions'] = \
            self.context.context.data['region_subregions']

        return MarineUnitIDsForm(self, self.request)

    def get_available_marine_unit_ids(self):
        return self.subform.get_available_marine_unit_ids()


StartArticle8910View = wrap_form(StartArticle8910Form, MainFormWrapper)


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    fields = Fields(interfaces.IMarineUnitIDsSelect)
    fields['marine_unit_ids'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        data = self.get_main_form().data
        klass = get_form(data['article'])

        return super(MarineUnitIDsForm, self).get_subform(klass)

    def get_available_marine_unit_ids(self):
        marine_unit_ids = self.data.get('marine_unit_ids')

        if marine_unit_ids:
            data = self.data
        else:
            data = {}
            parent = self.context

            # lookup values in the inheritance tree

            for crit in ['area_types', 'member_states', 'region_subregions']:
                data[crit] = getattr(parent, 'get_selected_' + crit)()
                parent = parent.context

        return db.get_marine_unit_ids(**data)


StartArticle11View = wrap_form(StartArticle11Form, MainFormWrapper)
StartArticle1314View = wrap_form(StartArticle1314Form, MainFormWrapper)


class StartArticle89102018Form(MainForm):
    record_title = 'Articles 8, 9, 10'
    name = 'msfd-c4'

    fields = Fields(interfaces.IArticleSelect2018)
    session_name = 'session_2018'

    def get_subform(self):
        article = self.data['article']

        if article:
            if isinstance(article, tuple):
                klass = article[0]
            else:
                klass = article

            return klass(self, self.request)


StartArticle89102018View = wrap_form(StartArticle89102018Form, MainFormWrapper)

# discover and register associated views

scan('a4')
scan('a8ac')
scan('a8b')
scan('a9')
scan('a10')
scan('a89102018')
