from .base import EmbededForm, ItemDisplayForm
from plone.app.textfield.widget import RichTextWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql2018
from z3c.form.browser.text import TextWidget, TextFieldWidget
from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.button import buttonAndHandler
from z3c.form.field import Fields


def register_compliance_module(klass):

    class ComplianceModuleMain(klass):
        # template = ViewPageTemplateFile('pt/compliance.pt')

        def get_subform(self):
            # TODO access restriction
            # only show if the user is allowed to see compliance module
            return ComplianceModule(self, self.request)

        def update(self):
            super(klass, self).update()
            # self.compliance_content = ComplianceModule(self, self.request)
            self.subform = self.get_subform()

    return ComplianceModuleMain


class ComplianceModule(EmbededForm):
    css_class = 'only-left-side-form'
    # template = ViewPageTemplateFile('pt/compliance.pt')
    fields = Fields(interfaces.IComplianceModule)
    actions = None
    reset_page = False

    def get_subform(self):
        return ComplianceDisplay(self, self.request)

    # def update(self):
    #     super(ComplianceModule, self).update()
    #     self.subform = self.get_subform()


class ComplianceDisplay(ItemDisplayForm):

    template = ViewPageTemplateFile('pt/compliance-display-form.pt')
    data_template = ViewPageTemplateFile('pt/compliance-item-display.pt')
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    # css_class = 'left-side-form'
    # css_class = 'compliance-display'

    def get_db_results(self):
        return 0, {}

    def get_extra_data(self):
        res = list()
        res.append(
            ('Some data from file ', {
                '': [{'Data': "Text here _%s" % x} for x in range(2)]
            }))

        return res

    def get_subform(self):
        return ComplianceAssessment(self, self.request)

    def update(self):
        super(ComplianceDisplay, self).update()
        self.subform = self.get_subform()
        del self.widgets['page']


class ComplianceAssessment(EmbededForm):
    # css_class = 'only-left-side-form'
    fields = Fields(interfaces.IComplianceAssessment)
    # fields['com_assessment'].widgetFactory = TextWidget

    mc_com_assessments = 'COM_assessments'
    mc_assessments_comments = 'Assessments_comments'

    @buttonAndHandler(u'Save assessment', name='save_assessment')
    def save_assessment(self, action):
        data, errors = self.extractData()
        assessment = data.get('com_assessment', '')
        import pdb;pdb.set_trace()
        if assessment:
            # TODO save assessment to DB
            reporting_history_id = self.context.item.get('Id', '')
            assessment_id = db.get_all_records(
                self.mc_com_assessments,
                self.mc_com_assessments.Reporting_historyID == reporting_history_id
            )
            values = dict()
            values['Reporting_historyID'] = reporting_history_id
            values['Article'] = ''
            values['GEScomponent'] = ''
            values['Feature'] = ''
            values['assessment_criteria'] = assessment

            if assessment_id:
                conditions = list()
                conditions.append(
                    self.mc_com_assessments.Reporting_historyID == reporting_history_id
                )
                db.update_record(self.mc_com_assessments, *conditions, **values)
            else:
                db.insert_record(self.mc_com_assessments, **values)

    @buttonAndHandler(u'Save comment', name='save_comment')
    def save_comment(self, action):
        data, errors = self.extractData()
        comment = data.get('assessment_comment', '')
        import pdb;pdb.set_trace()
        if comment:
            # TODO save comment to DB
            com_assessmentsId = self.context.item.get('Id', '')
            comment_id = db.get_all_records(
                self.mc_assessments_comments,
                self.mc_assessments_comments.COM_assessmentsID == com_assessmentsId
            )
            values = dict()
            values['COM_assessmentsID'] = com_assessmentsId
            values['organisation'] = ''
            values['Comment'] = comment

            if comment_id:
                conditions = list()
                conditions.append(
                    self.mc_assessments_comments.COM_assessmentsID == com_assessmentsId
                )
                db.update_record(self.mc_assessments_comments, **values)
            else:
                db.insert_record(self.mc_com_assessments, **values)

    def update(self):
        super(ComplianceAssessment, self).update()
        self.data, errors = self.extractData()

    def extractData(self):
        data, errors = super(ComplianceAssessment, self).extractData()

        return data, errors
