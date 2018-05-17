from plone.z3cform.layout import wrap_form
from wise.content.search import interfaces
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, MainForm
from .utils import get_form, scan


class StartArticle8910Form(MainForm):
    """ Select one of the article: 8(a,b,c,d)/9/10
    """

    name = 'msfd-c1'

    fields = Fields(interfaces.IArticleSelect)

    def get_subform(self):

        if self.data['article']:
            return MemberRegionAreaForm(self, self.request)


class MemberRegionAreaForm(EmbededForm):
    """ Select the memberstate, region, area form
    """

    fields = Fields(interfaces.IStartArticles8910)

    fields['member_states'].widgetFactory = CheckBoxFieldWidget
    fields['region_subregions'].widgetFactory = CheckBoxFieldWidget
    fields['area_types'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return MarineUnitIDsForm(self, self.request)


StartArticle8910View = wrap_form(StartArticle8910Form)


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    # TODO: properly show only available marine unit ids
    fields = Fields(interfaces.IMarineUnitIDsSelect)

    def get_subform(self):
        data = self.get_main_form().data
        klass = get_form(data['article'])

        return super(MarineUnitIDsForm, self).get_subform(klass)


class StartArticle11Form(MainForm):
    """
    """
    name = 'msfd-c2'


StartArticle11View = wrap_form(StartArticle11Form)


class StartArticle1314Form(MainForm):
    """
    """
    name = 'msfd-c3'


StartArticle1314View = wrap_form(StartArticle1314Form)

# discover and register associated views
scan('a8')
scan('a9')
scan('a10')
