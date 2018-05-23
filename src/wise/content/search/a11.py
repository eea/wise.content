from z3c.form.browser.checkbox import CheckBoxFieldWidget

from .base import EmbededForm, MainForm
from z3c.form.field import Fields
from wise.content.search import interfaces

class StartArticle11Form(MainForm):
    """
    """
    name = 'msfd-c2'

    fields = Fields(interfaces.IStartArticle11)

    fields['monitoring_programme_types'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return MonitoringProgrammeTypesForm(self, self.request)


class MonitoringProgrammeTypesForm(EmbededForm):
    """
    """

def get_subform(self):
        return MonitorTypeForm(self, self.request)



def MonitorTypeForm(EmbededForm):
    def get_subform(self):
        return None
