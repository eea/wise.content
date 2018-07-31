
from plone.z3cform.layout import wrap_form
from wise.content.search import interfaces
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .a11 import StartArticle11Form
from .a1314 import StartArticle1314Form
from .base import EmbededForm, MainForm, MainFormWrapper
from .utils import (all_values_from_field, default_value_from_field, get_form,
                    scan)


class StartArticle8910Form(MainForm):
    """ Select one of the article: 8(a,b,c,d)/9/10
    """

    name = 'msfd-c1'

    fields = Fields(interfaces.IArticleSelect)
    session_name = 'session'

    def get_subform(self):

        if self.data['article']:
            return MemberRegionAreaForm(self, self.request)

    def default_article(self):
        return default_value_from_field(self, self.fields['article'])


class MemberRegionAreaForm(EmbededForm):
    """ Select the memberstate, region, area form
    """

    fields = Fields(interfaces.IStartArticles8910)

    fields['member_states'].widgetFactory = CheckBoxFieldWidget
    fields['region_subregions'].widgetFactory = CheckBoxFieldWidget
    fields['area_types'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return MarineUnitIDsForm(self, self.request)

    def default_member_states(self):
        return all_values_from_field(self, self.fields['member_states'])

    def default_region_subregions(self):
        return all_values_from_field(self, self.fields['region_subregions'])

    def default_area_types(self):
        return all_values_from_field(self, self.fields['area_types'])


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

    def default_marine_unit_ids(self):
        return all_values_from_field(self.context,
                                     self.fields['marine_unit_ids'])


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

    def default_article(self):
        return default_value_from_field(self, self.fields['article'])


StartArticle89102018View = wrap_form(StartArticle89102018Form, MainFormWrapper)

# discover and register associated views

scan('a8ac')
scan('a8b')
scan('a9')
scan('a10')
scan('a89102018')
