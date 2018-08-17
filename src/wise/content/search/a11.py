from sqlalchemy import and_, or_

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import (EmbededForm, ItemDisplay, ItemDisplayForm, MainForm,
                   MultiItemDisplayForm)
from .utils import (all_values_from_field, data_to_xls, db_objects_to_dict,
                    default_value_from_field, pivot_data, register_form_art11,
                    register_form_section)

ART11_GlOBALS = dict()


class StartArticle11Form(MainForm):
    """
    """

    record_title = 'Article 11'
    name = 'msfd-c2'
    fields = Fields(interfaces.IStartArticle11)
    fields['monitoring_programme_types'].widgetFactory = CheckBoxFieldWidget
    session_name = 'session'

    def get_subform(self):
        klass = self.data.get('monitoring_programme_info_types')

        return klass(self, self.request)

    def extractData(self):
        """ Override to be able to provide defaults
        """
        data, errors = super(MainForm, self).extractData()

        for k, v in data.items():
            if not v:
                default = getattr(self, 'default_' + k, None)

                if default:
                    values = default()

                    if isinstance(values, tuple):
                        value, token = values
                    else:
                        value = token = values
                    data[k] = value
                    widget = self.widgets[k]
                    widget.value = token
                    widget.update()

        return data, errors

    def get_mp_type_ids(self):
        return self.data.get('monitoring_programme_types', [])

    def default_monitoring_programme_types(self):
        return all_values_from_field(self,
                                     self.fields['monitoring_programme_types'])

    def default_monitoring_programme_info_types(self):
        return default_value_from_field(
            self, self.fields['monitoring_programme_info_types']
        )


@register_form_art11
class A11MonitoringProgrammeForm(EmbededForm):
    title = "Monitoring Programmes"

    fields = Fields(interfaces.IMonitoringProgramme)
    fields['country'].widgetFactory = CheckBoxFieldWidget
    fields['region'].widgetFactory = CheckBoxFieldWidget
    fields['marine_unit_id'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A11MonProgDisplay(self, self.request)

    def default_country(self):
        return all_values_from_field(self, self.fields['country'])

    def default_region(self):
        return all_values_from_field(self, self.fields['region'])

    def default_marine_unit_id(self):
        return all_values_from_field(self, self.fields['marine_unit_id'])

    def get_monitoring_programme_ids(self):
        # import pdb;pdb.set_trace()
        countries = self.data.get('country', [])
        regions = self.data.get('region', [])
        marine_unit_id = self.data.get('marine_unit_id', [])
        mp_type_ids = self.context.get_mp_type_ids()

        mon_ids = db.get_unique_from_mapper(
            sql.MSFD11MON,
            'ID',
            and_(sql.MSFD11MON.MemberState.in_(countries),
                 sql.MSFD11MON.Region.in_(regions))
        )
        mon_prog_ids_from_MP = db.get_unique_from_mapper(
            sql.MSFD11MP,
            'MonitoringProgramme',
            and_(sql.MSFD11MP.MON.in_(mon_ids),
                 sql.MSFD11MP.MPType.in_(mp_type_ids)
                 )
        )
        mon_prog_ids_from_MP = [int(elem) for elem in mon_prog_ids_from_MP]

        count, mon_prog_ids = db.get_all_records_outerjoin(
            sql.MSFD11MonitoringProgrammeMarineUnitID,
            sql.MSFD11MarineUnitID,
            sql.MSFD11MarineUnitID.MarineUnitID.in_(marine_unit_id)
        )
        mon_prog_ids = [row.MonitoringProgramme for row in mon_prog_ids]

        result = tuple(set(mon_prog_ids_from_MP) & set(mon_prog_ids))

        if not result:
            result = tuple(mon_prog_ids_from_MP + mon_prog_ids)

        return result


class A11MonProgDisplay(ItemDisplayForm):
    title = "Monitoring Programmes display"

    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    mapper_class = sql.MSFD11MonitoringProgramme
    order_field = 'ID'
    css_class = 'left-side-form'

    def download_results(self):
        mp_type_ids = self.context.context.get_mp_type_ids()
        mon_prog_ids = self.context.get_monitoring_programme_ids()

        klass_join_mp = sql.MSFD11MP
        count_mp, data_mp = db.get_all_records_outerjoin(
            self.mapper_class,
            klass_join_mp,
            and_(klass_join_mp.MPType.in_(mp_type_ids),
                 klass_join_mp.MonitoringProgramme.in_(mon_prog_ids)),
        )

        mp_ids = [row.ID for row in data_mp]

        mapper_class_mpl = sql.MSFD11MonitoringProgrammeList
        count_mpl, data_mpl = db.get_all_records(
            mapper_class_mpl,
            mapper_class_mpl.MonitoringProgramme.in_(mp_ids)
        )

        mapper_class_mpmid = sql.MSFD11MonitoringProgrammeMarineUnitID
        count_mpmid, data_mpmid = db.get_all_records_join(
            [
                mapper_class_mpmid.ID,
                mapper_class_mpmid.MonitoringProgramme,
                sql.MSFD11MarineUnitID.MarineUnitID
            ],
            sql.MSFD11MarineUnitID,
            mapper_class_mpmid.MonitoringProgramme.in_(mp_ids)
        )

        mapper_class_rt = sql.MSFD11Q6aRelevantTarget
        count_mpl, data_rt = db.get_all_records(
            mapper_class_rt,
            mapper_class_rt.MonitoringProgramme.in_(mp_ids)
        )

        xlsdata = [
            # worksheet title, row data
            ('MSFD11MonitoringProgramme', data_mp),
            ('MSFD11MonitoringProgrammeList', data_mpl),
            ('MSFD11MonitorProgMarineUnitID', data_mpmid),
            ('MSFD11Q6aRelevantTarget', data_rt),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):

        page = self.get_page()
        klass_join = sql.MSFD11MP
        needed_ID = self.context.context.get_mp_type_ids()
        mon_prog_ids = self.context.get_monitoring_programme_ids()

        # import pdb;pdb.set_trace()

        if needed_ID:
            return db.get_item_by_conditions_joined(
                self.mapper_class,
                klass_join,
                self.order_field,
                and_(klass_join.MPType.in_(needed_ID),
                     klass_join.MonitoringProgramme.in_(mon_prog_ids)),
                page=page
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        monitoring_programme_id = self.item.ID

        excluded_columns = ('MonitoringProgramme', 'ID')
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

        element_names = db_objects_to_dict(result_programme_list,
                                           excluded_columns)
        element_names = pivot_data(element_names, 'ElementName')

        res = [
            ('Element Names', element_names),
        ]

        if marine_units:
            res.append(
                ('Marine Unit(s)', {
                    '': [{'MarineUnitIDs': x} for x in marine_units]
                }))

        if targets:
            res.append(
                ('Target(s)', {
                    '': [{'Relevant Targets': x} for x in targets]
                }))

        return res


@register_form_art11
class A11MonitorSubprogrammeForm(EmbededForm):
    title = "Monitoring Subprogrammes"

    fields = Fields(interfaces.IMonitoringSubprogramme)
    fields['country'].widgetFactory = CheckBoxFieldWidget
    fields['region'].widgetFactory = CheckBoxFieldWidget
    fields['marine_unit_id'].widgetFactory = CheckBoxFieldWidget

    # create a mapping between
    # MPTypes - SubProgramme
    @property
    def get_mptypes_subprog(self):
        mapping = ART11_GlOBALS.get('get_mptypes_subprog', None)

        if mapping:
            return mapping

        mptypes = db.get_all_columns_from_mapper(sql.MSFD11MPType, 'ID')
        mapper_dict = dict()

        for row in mptypes:
            mpid = row.ID
            value = row.Value  # MP_D8, MP_D1_4_6_SeabedHabitats
            mp_ids = db.get_unique_from_mapper(
                sql.MSFD11MP,
                'ID',
                sql.MSFD11MP.MPType == mpid
            )
            sub_mon_prog_ids_1 = db.get_unique_from_mapper(
                sql.MSFD11ReferenceSubProgramme,
                'SubMonitoringProgrammeID',
                sql.MSFD11ReferenceSubProgramme.MP.in_(mp_ids)
            )
            sub_mon_prog_ids_2 = db.get_unique_from_mapper(
                sql.MSFD11SubProgrammeIDMatch,
                'Q4g_SubProgrammeID',
                sql.MSFD11SubProgrammeIDMatch.MP_Type == value
            )
            sub_mon_prog_ids_3 = db.get_unique_from_mapper(
                sql.MSFD11SubProgrammeIDMatch,
                'Q4g_SubProgrammeID',
                sql.MSFD11SubProgrammeIDMatch.MP_ReferenceSubProgramme.in_(
                    sub_mon_prog_ids_1
                )
            )
            sub_mon_prog_ids_all = (sub_mon_prog_ids_1 + sub_mon_prog_ids_2
                                    + sub_mon_prog_ids_3)

            subprogramme_ids = db.get_unique_from_mapper(
                sql.MSFD11SubProgramme,
                'ID',
                sql.MSFD11SubProgramme.Q4g_SubProgrammeID.in_(
                    sub_mon_prog_ids_all)
            )
            subprogramme_ids = [int(x) for x in subprogramme_ids]
            mapper_dict.update({mpid: subprogramme_ids})

        ART11_GlOBALS.update({'get_mptypes_subprog': mapper_dict})

        return mapper_dict

    def get_subform(self):
        return A11MonSubDisplay(self, self.request)

    def default_country(self):
        return all_values_from_field(self, self.fields['country'])

    def default_region(self):
        return all_values_from_field(self, self.fields['region'])

    def default_marine_unit_id(self):
        return all_values_from_field(self, self.fields['marine_unit_id'])


class A11MonSubDisplay(MultiItemDisplayForm):

    title = "Monitoring Subprogramme display"

    # fields = Fields(interfaces.I11Subprogrammes)

    mapper_class = sql.MSFD11ReferenceSubProgramme
    order_field = "ID"
    css_class = 'left-side-form'

    # extra_data_template = ViewPageTemplateFile('pt/extra-data-item.pt')

    def download_results(self):
        mp_type_ids = self.context.context.get_mp_type_ids()
        countries = self.context.data.get('country', [])
        regions = self.context.data.get('region', [])
        marine_unit_id = self.context.data.get('marine_unit_id', [])

        count, mon_prog_ids = db.get_all_records_outerjoin(
            sql.MSFD11MonitoringProgrammeMarineUnitID,
            sql.MSFD11MarineUnitID,
            sql.MSFD11MarineUnitID.MarineUnitID.in_(marine_unit_id)
        )
        mon_prog_ids = [row.MonitoringProgramme for row in mon_prog_ids]
        mp_ids = db.get_unique_from_mapper(
            sql.MSFD11MP,
            'ID',
            sql.MSFD11MP.MonitoringProgramme.in_(mon_prog_ids)
        )

        subprogramme_ids = db.get_unique_from_mapper(
            sql.MSFD11MONSub,
            'SubProgramme',
            and_(sql.MSFD11MONSub.MemberState.in_(countries),
                 sql.MSFD11MONSub.Region.in_(regions))
        )
        subprogramme_ids = [int(i) for i in subprogramme_ids]

        q4g_subprogids_1 = db.get_unique_from_mapper(
            sql.MSFD11SubProgramme,
            'Q4g_SubProgrammeID',
            sql.MSFD11SubProgramme.ID.in_(subprogramme_ids)
        )
        q4g_subprogids_2 = db.get_unique_from_mapper(
            sql.MSFD11SubProgrammeIDMatch,
            'MP_ReferenceSubProgramme',
            sql.MSFD11SubProgrammeIDMatch.Q4g_SubProgrammeID.in_(q4g_subprogids_1)
        )

        klass_join_mp = sql.MSFD11MP
        count_rsp, data_rsp = db.get_all_records_outerjoin(
            self.mapper_class,
            klass_join_mp,
            and_(klass_join_mp.MPType.in_(mp_type_ids),
                 self.mapper_class.MP.in_(mp_ids),
                 or_(self.mapper_class.SubMonitoringProgrammeID.in_(q4g_subprogids_1),
                     self.mapper_class.SubMonitoringProgrammeID.in_(q4g_subprogids_2))
                 ),
        )

        submonitor_programme_ids = [row.SubMonitoringProgrammeID
                                    for row in data_rsp]

        mapper_class_sp = sql.MSFD11SubProgramme
        count_sp, data_sp = db.get_all_records(
            mapper_class_sp,
            mapper_class_sp.Q4g_SubProgrammeID.in_(submonitor_programme_ids)
        )

        subprograme_ids = [row.ID for row in data_sp]

        mapper_class_em = sql.MSFD11Q9aElementMonitored
        count_em, data_em = db.get_all_records(
            mapper_class_em,
            mapper_class_em.SubProgramme.in_(subprograme_ids)
        )

        mapper_class_mp = sql.MSFD11Q9bMeasurementParameter
        count_mp, data_mp = db.get_all_records(
            mapper_class_mp,
            mapper_class_mp.SubProgramme.in_(subprograme_ids)
        )

        xlsdata = [
            # worksheet title, row data
            ('MSFD11ReferenceSubProgramme', data_rsp),
            ('MSFD11SubProgramme', data_sp),
            ('MSFD11Q9aElementMonitored', data_em),
            ('MSFD11Q9bMeasurementParameter', data_mp),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        # needed_ids = self.context.data.get('monitoring_programme_types', [])
        needed_ids = self.context.context.get_mp_type_ids()
        klass_join = sql.MSFD11MP

        countries = self.context.data.get('country', [])
        regions = self.context.data.get('region', [])
        marine_unit_id = self.context.data.get('marine_unit_id', [])

        count, mon_prog_ids = db.get_all_records_outerjoin(
            sql.MSFD11MonitoringProgrammeMarineUnitID,
            sql.MSFD11MarineUnitID,
            sql.MSFD11MarineUnitID.MarineUnitID.in_(marine_unit_id)
        )
        mon_prog_ids = [row.MonitoringProgramme for row in mon_prog_ids]
        mp_ids = db.get_unique_from_mapper(
            sql.MSFD11MP,
            'ID',
            sql.MSFD11MP.MonitoringProgramme.in_(mon_prog_ids)
        )

        # import pdb;pdb.set_trace()

        subprogramme_ids = db.get_unique_from_mapper(
            sql.MSFD11MONSub,
            'SubProgramme',
            and_(sql.MSFD11MONSub.MemberState.in_(countries),
                 sql.MSFD11MONSub.Region.in_(regions))
        )
        subprogramme_ids = [int(i) for i in subprogramme_ids]

        q4g_subprogids_1 = db.get_unique_from_mapper(
            sql.MSFD11SubProgramme,
            'Q4g_SubProgrammeID',
            sql.MSFD11SubProgramme.ID.in_(subprogramme_ids)
        )
        q4g_subprogids_2 = db.get_unique_from_mapper(
            sql.MSFD11SubProgrammeIDMatch,
            'MP_ReferenceSubProgramme',
            sql.MSFD11SubProgrammeIDMatch.Q4g_SubProgrammeID.in_(q4g_subprogids_1)
        )

        if needed_ids:
            return db.get_item_by_conditions_joined(
                self.mapper_class,
                klass_join,
                self.order_field,
                and_(klass_join.MPType.in_(needed_ids),
                     self.mapper_class.MP.in_(mp_ids),
                     or_(self.mapper_class.SubMonitoringProgrammeID.in_(q4g_subprogids_1),
                         self.mapper_class.SubMonitoringProgrammeID.in_(q4g_subprogids_2))
                     ),
                page=page
            )


@register_form_section(A11MonSubDisplay)
class A11MPExtraInfo(ItemDisplay):
    title = "SubProgramme Info"

    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    # TODO data from columns SubMonitoringProgrammeID and Q4g_SubProgrammeID
    # do not match, SubMonitoringProgrammeID contains spaces
    def get_db_results(self):
        if not self.context.item:
            return {}

        subprogramme_id = self.context.item.SubMonitoringProgrammeID
        mc = sql.MSFD11SubProgramme

        count, item = db.get_related_record(
            mc, 'Q4g_SubProgrammeID', subprogramme_id)

        if not item:
            subprogramme_id = db.get_unique_from_mapper(
                sql.MSFD11SubProgrammeIDMatch,
                'Q4g_SubProgrammeID',
                sql.MSFD11SubProgrammeIDMatch.MP_ReferenceSubProgramme == subprogramme_id
            )
            count, item = db.get_related_record(
                mc, 'Q4g_SubProgrammeID', subprogramme_id)

        if item:
            self.subprogramme = getattr(item, 'ID')
        else:
            self.subprogramme = 0

        page = self.get_page()

        return page, item

    def get_extra_data(self):
        mapper_class_element = sql.MSFD11Q9aElementMonitored
        elements_monitored = db.get_all_columns_from_mapper(
            mapper_class_element,
            'Q9a_ElementMonitored',
            mapper_class_element.SubProgramme == self.subprogramme
        )

        mapper_class_measure = sql.MSFD11Q9bMeasurementParameter
        parameters_measured = db.get_all_columns_from_mapper(
            mapper_class_measure,
            'ID',
            mapper_class_measure.SubProgramme == self.subprogramme
        )
        excluded_columns = ('ID', 'SubProgramme')
        parameters_measured = db_objects_to_dict(parameters_measured,
                                                 excluded_columns)
        # parameters_measured = pivot_data(parameters_measured, 'SubProgramme')

        return [
            ('Elements monitored', {
                '': [
                    {'ElementMonitored': x.Q9a_ElementMonitored}

                    for x in elements_monitored
                ]
            }),
            ('Parameters measured', {'': parameters_measured}),
        ]
