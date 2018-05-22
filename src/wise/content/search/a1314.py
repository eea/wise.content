""" Forms and views for Article 13-14 search
"""

from wise.content.search import interfaces
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, MainForm


class StartArticle1314Form(MainForm):
    """
    """
    fields = Fields(interfaces.IStartArticles1314)
    name = 'msfd-c3'

    def get_subform(self):
        return UniqueCodesForm(self, self.request)


class UniqueCodesForm(EmbededForm):
    """ Select the unique codes
    """

    fields = Fields(interfaces.IA1314UniqueCodes)

    fields['unique_codes'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return None
        # return MarineUnitIDsForm(self, self.request)
