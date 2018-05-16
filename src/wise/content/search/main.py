from plone.z3cform.layout import wrap_form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import interfaces
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields

from .base import EmbededForm, MainForm
from .utils import get_form, scan


class StartArticle8910Form(MainForm):
    """ Select the memberstate, region, area form
    """

    fields = Fields(interfaces.IStartArticles8910)

    fields['member_states'].widgetFactory = CheckBoxFieldWidget
    fields['region_subregions'].widgetFactory = CheckBoxFieldWidget
    fields['area_types'].widgetFactory = CheckBoxFieldWidget

    def update(self):
        super(StartArticle8910Form, self).update()

        self.data, errors = self.extractData()

        if not errors and all(self.data.values()):
            self.subform = MarineUnitIDsForm(self, self.request)


StartArticle8910View = wrap_form(StartArticle8910Form)


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    fields = Fields(interfaces.IMarineUnitIDsSelect)

    def get_subform(self):
        return ArticleSelectForm(self, self.request)


class ArticleSelectForm(EmbededForm):
    """ Select one of the article: 8(a,b,c,d)/9/10
    """

    fields = Fields(interfaces.IArticleSelect)

    def get_subform(self):
        klass = get_form(self.data['article'])

        return super(ArticleSelectForm, self).get_subform(klass)


# discover and register associated views
scan('a8')
scan('a9')
scan('a10')
