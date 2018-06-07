from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, ItemDisplay, ItemDisplayForm, MainForm, MultiItemDisplayForm
from .utils import register_form_art11, register_form_section, pivot_data


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
class A11MonitoringProgrammeForm(ItemDisplayForm):
    """
    """
    title = "Monitoring Programmes"
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    mapper_class = sql.MSFD11MonitoringProgramme
    order_field = 'ID'
    css_class = 'left-side-form'

    def get_db_results(self):
        page = self.get_page()
        klass_join = sql.MSFD11MP
        needed_ID = self.get_mp_type_ids()

        if needed_ID:
            return db.get_item_by_conditions_joined(
                self.mapper_class,
                klass_join,
                self.order_field,
                klass_join.MPType.in_(needed_ID),
                page=page
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        monitoring_programme_id = self.item.ID

        mapper_class = sql.MSFD11MonitoringProgrammeList
        column = 'MonitoringProgramme'
        result_programme_list = db.get_all_columns_from_mapper(
            mapper_class,
            column,
            getattr(mapper_class, column) == monitoring_programme_id
        )

        marine_units = db.get_unique_from_mapper(
            sql.MSFD11Q6aRelevantTarget,
            'RelevantTarget',
            sql.MSFD11Q6aRelevantTarget.MonitoringProgramme == monitoring_programme_id
        )

        targets = db.get_unique_from_mapper_join(
            sql.MSFD11MarineUnitID,
            'MarineUnitID',
            sql.MSFD11MonitoringProgrammeMarineUnitID,
            'ID',
            sql.MSFD11MonitoringProgrammeMarineUnitID.MonitoringProgramme == monitoring_programme_id
        )

        # element_names = pivot_data(result_programme_list, 'ElementName')

        res = []
        tars = {
            '':
            [{'GESDescriptorsCriteriaIndicators': x[0]} for x in res]
        }

        return [
            ('Marine Unit(s)', res),
            ('Target(s)', res),
        ]


    def get_mp_type_ids(self):
        return self.context.data.get('monitoring_programme_types', [])




@register_form_art11
class A11MonitorSubprogrammeForm(ItemDisplayForm):

    title = "Monitoring Subprogrammes"

    # fields = Fields(interfaces.I11Subprogrammes)

    extra_data_template = ViewPageTemplateFile('pt/extra-data-item.pt')
    mapper_class = sql.MSFD11ReferenceSubProgramme
    order_field = "ID"
    css_class = 'left-side-form'

    def get_db_results(self):
        page = self.get_page()
        needed_ids = self.context.data.get('monitoring_programme_types', [])
        klass_join = sql.MSFD11MP

        if needed_ids:
            # return db.get_unique_from_mapper_join(
            #     self.mapper_class,
            #     'SubMonitoringProgrammeName',
            #     klass_join,
            #     self.order_field,
            #     klass_join.MPType.in_(needed_ids),
            #     page=page
            # )
            return db.get_item_by_conditions_joined(
                self.mapper_class,
                klass_join,
                self.order_field,
                klass_join.MPType.in_(needed_ids),
                page=page
            )

    # TODO data from columns SubMonitoringProgrammeID and Q4g_SubProgrammeID
    # do not match, SubMonitoringProgrammeID contains spaces
    def get_extra_data(self):
        if not self.item:
            return {}

        subprogramme_id = self.item.SubMonitoringProgrammeID
        mc = sql.MSFD11SubProgramme

        count, item = db.get_related_record(mc, 'Q4g_SubProgrammeID', subprogramme_id)
        if item:
            self.subprogramme = getattr(item, 'ID')
        else:
            self.subprogramme = 0

        return 'Subprogramme info', item

        # return [
        #     ('Subprogramme info', {'test': item}),
        # ]


@register_form_section(A11MonitorSubprogrammeForm)
class A11MPElements(ItemDisplay):
    title = "Element(s) monitored"

    mapper_class = sql.MSFD11Q9aElementMonitored

    # TODO not finished, implement to return a list with values
    def get_db_results(self):
        result = db.get_unique_from_mapper(
            self.mapper_class,
            'Q9a_ElementMonitored',
            self.mapper_class.SubProgramme == self.context.subprogramme
        )
        return 0, []


@register_form_section(A11MonitorSubprogrammeForm)
class A11MPParameters(ItemDisplay):
    title = "Parameter(s) monitored"

    mapper_class = sql.MSFD11Q9bMeasurementParameter

    # TODO not finished, implement return part
    def get_db_results(self):
        result = db.get_all_columns_from_mapper(
            self.mapper_class,
            'ID',
            self.mapper_class.SubProgramme == self.context.subprogramme
        )
        return 0, []