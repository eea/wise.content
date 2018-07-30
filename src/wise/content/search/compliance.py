from .base import EmbededForm, ItemDisplayForm
from plone.app.textfield.widget import RichTextWidget
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields
from z3c.form.browser.text import TextWidget, TextFieldWidget
from z3c.form.browser.textarea import TextAreaWidget
from wise.content.search import db, interfaces, sql2018
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


def register_compliance_module(klass):

    class ComplianceModuleMain(klass):
        template = ViewPageTemplateFile('pt/compliance.pt')
        # compliance_content = None

        def update(self):
            super(klass, self).update()
            self.compliance_content = ComplianceModule(self, self.request)

    return ComplianceModuleMain


class ComplianceModule(EmbededForm):
    css_class = 'compliance-module'
    # template = ViewPageTemplateFile('pt/compliance.pt')
    fields = Fields(interfaces.IComplianceModule)
    # actions = None

    def get_subform(self):
        return ComplianceDisplay(self, self.request)

    def update(self):
        super(ComplianceModule, self).update()
        self.subform = self.get_subform()


class ComplianceDisplay(ItemDisplayForm):

    template = ViewPageTemplateFile('pt/compliance-display-form.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    # css_class = 'left-side-form'
    css_class = 'compliance-display'

    def get_subform(self):
        # TODO access restriction
        # only show if the user is allowed to see compliance module
        return ComplianceAssessment(self, self.request)

    def update(self):
        super(ComplianceDisplay, self).update()
        self.subform = self.get_subform()

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
    # css_class = 'only-left-side-form'
    fields = Fields(interfaces.IComplianceAssessment)
    # fields['com_assessment'].widgetFactory = TextWidget

    @buttonAndHandler(u'Save assessment', name='save_ass')
    def save_assessment(self, action):
        data, errors = self.extractData()
        import pdb;pdb.set_trace()

    @buttonAndHandler(u'Save comment', name='save_comm')
    def save_comment(self, action):
        data, errors = self.extractData()
        import pdb; pdb.set_trace()

    def update(self):
        super(ComplianceAssessment, self).update()
        self.data, errors = self.extractData()
        # import pdb;pdb.set_trace()

    def extractData(self):
        # import pdb;pdb.set_trace()
        return super(ComplianceAssessment, self).extractData()

