from .base import EmbededForm, ItemDisplayForm
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.browser.text import TextWidget, TextFieldWidget
from wise.content.search import db, interfaces, sql2018
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ComplianceModule(EmbededForm):
    template = ViewPageTemplateFile('pt/compliance.pt')
    fields = Fields(interfaces.IComplianceModule)
    actions = None

    def get_subform(self):
        return ComplianceDisplay(self, self.request)


class ComplianceDisplay(ItemDisplayForm):

    template = ViewPageTemplateFile('pt/compliance-display-form.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    # css_class = 'left-side-form'

    def get_subform(self):
        # TODO access restriction
        # only show if the user is allowed to see compliance module
        return ComplianceAssessment(self, self.request)

    def update(self):
        super(ComplianceDisplay, self).update()
        self.subform = self.get_subform()

        # del self.widgets['page']

    def get_db_results(self):
        return 0, {}

    def get_extra_data(self):
        res = list()
        res.append(
            ('Test data(s)', {
                '': [{'Test': "Test%s" % x} for x in range(2)]
            }))

        return res


class ComplianceAssessment(EmbededForm):
    css_class = 'only-left-side-form'
    fields = Fields(interfaces.IComplianceAssessment)

    @buttonAndHandler(u'Save assessment', name='save_ass')
    def save_assessment(self, action):
        import pdb;pdb.set_trace()
        pass

    @buttonAndHandler(u'Save comment', name='save_comm')
    def save_comment(self, action):
        import pdb; pdb.set_trace()
        pass
