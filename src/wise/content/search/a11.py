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

        mapper_class_mp_list = sql.MSFD11MonitoringProgrammeList
        column = 'MonitoringProgramme'
        result_programme_list = db.get_all_columns_from_mapper(
            mapper_class_mp_list,
            column,
            getattr(mapper_class_mp_list, column) == monitoring_programme_id
        )

        mapper_class_target = sql.MSFD11Q6aRelevantTarget
        targets = db.get_unique_from_mapper(
            mapper_class_target,
            'RelevantTarget',
            getattr(mapper_class_target, column) == monitoring_programme_id
        )

        mapper_class_mp_marine = sql.MSFD11MonitoringProgrammeMarineUnitID
        total, marine_units = db.get_unique_from_mapper_join(
            sql.MSFD11MarineUnitID,
            'MarineUnitID',
            mapper_class_mp_marine,
            'ID',
            getattr(mapper_class_mp_marine, column) == monitoring_programme_id
        )

        # element_names = pivot_data(result_programme_list, 'ElementName')


        # import pdb;pdb.set_trace()

        return [
            # ('Element Names TEST', {
            #     'Name1': [{'Other Data Here': x} for x in marine_units],
            #     'Name2': [{'Other Data Here': x} for x in marine_units],
            #     'Name3': [{'Other Data Here1': '1234'}, {'Other Data Here2': '123'}]
            # }),
            ('Element Names', {
                "_".join((str(x.ID), x.ElementName)):
                    [{'subgroup': x.subgroup}] for x in result_programme_list
            }),
            ('Marine Unit(s)', {
                '': [{'MarineUnitIDs': x} for x in marine_units]
            }),
            ('Target(s)', {
                '': [{'Relevant Targets': x} for x in targets]
            }),
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


@register_form_section(A11MonitorSubprogrammeForm)
class A11MPElements(ItemDisplay):
    title = "Element(s) monitored"

    mapper_class = sql.MSFD11Q9aElementMonitored

    data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    # TODO not finished, implement to return a list with values
    def get_db_results(self):
        result = db.get_unique_from_mapper(
            self.mapper_class,
            'Q9a_ElementMonitored',
            self.mapper_class.SubProgramme == self.context.subprogramme
        )
        return [
            ('Element(s) monitored', {
                '':
                    [{'Q9a_ElementMonitored': x} for x in result]
            }),
        ]


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