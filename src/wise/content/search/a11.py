from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, ItemDisplay, MainForm, MultiItemDisplayForm
from .utils import register_form_art11, register_form_section


class StartArticle11Form(MainForm):
    """
    """
    name = 'msfd-c2'
    fields = Fields(interfaces.IStartArticle11)
    fields['monitoring_programme_types'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        klass = self.data.get('monitoring_programme_info_types')

        return klass(self, self.request)


@register_form_art11
class A11MonitoringProgrammeForm(MultiItemDisplayForm):
    """
    """
    title = "Monitoring Programmes"
    mapper_class = sql.MSFD11MonitoringProgramme
    order_field = 'ID'
    css_class = 'left-side-form'

    def get_db_results(self):
        page = self.get_page()
        klass_join = sql.MSFD11MP
        needed_ID = self.context.data.get('monitoring_programme_types', [])

        if needed_ID:
            return db.get_item_by_conditions_joined(
                self.mapper_class,
                klass_join,
                self.order_field,
                klass_join.MPType.in_(needed_ID),
                page=page
            )

    def get_mp_type_ids(self):
        return self.context.data.get('monitoring_programme_types', [])


@register_form_section(A11MonitoringProgrammeForm)
class A11MPMarineUnit(ItemDisplay):
    title = "Marine Unit(s)"

    def get_db_results(self):
        return 0, []


@register_form_section(A11MonitoringProgrammeForm)
class A11MPTarget(ItemDisplay):
    title = "Target(s)"

    def get_db_results(self):
        return 0, []


@register_form_art11
class MonitorSubprogrammeForm(EmbededForm):

    title = "Monitoring Subprogrammes"

    # fields = Fields(interfaces.IStartArticles1314)

    def get_subform(self):
        return None
