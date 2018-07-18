from sqlalchemy import and_, or_

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql2018
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, ItemDisplayForm
from .utils import (all_values_from_field, data_to_xls, db_objects_to_dict,
                    pivot_data, register_form_2018)


class Art9Display(ItemDisplayForm):
    css_class = 'left-side-form'
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    show_extra_data = True

    def download_results(self):
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        determination_mc = sql2018.ART9GESGESDetermination

        count, ges_component = db.get_all_records(
            mapper_class,
            self.condition_ges_component
        )
        id_ges_comp = [x.Id for x in ges_component]

        count, ges_determination = db.get_all_records(
            determination_mc,
            determination_mc.IdGESComponent.in_(id_ges_comp)
        )
        id_ges_deter = [x.Id for x in id_ges_comp]

        count, ges_deter_feature = db.get_all_records(
            features_mc,
            features_mc.IdGESDetermination.in_(id_ges_deter)
        )

        count, ges_marine_unit = db.get_all_records(
            sql2018.ART9GESMarineUnit,
            sql2018.ART9GESMarineUnit.IdGESDetermination.in_(id_ges_deter)
        )

        xlsdata = [
            # worksheet title, row data
            ('ART9GESGESComponent', ges_component),
            ('ART9GESGESDetermination', ges_determination),
            ('ART9GESGESDeterminationFeature', ges_deter_feature),
            ('ART9GESMarineUnit', ges_marine_unit),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        determination_mc = sql2018.ART9GESGESDetermination
        country_codes = self.context.context.data.get('country_code', ())
        ges_components = self.context.context.data.get('ges_component', ())
        features = self.context.data.get('feature', ())

        count, id_ges_components = db.get_all_records_join(
            [determination_mc.IdGESComponent,
             features_mc.Feature],
            features_mc,
            features_mc.Feature.in_(features)
        )
        id_ges_components = [x.IdGESComponent for x in id_ges_components]
        id_ges_components = tuple(set(id_ges_components))

        self.condition_ges_component = and_(
            sql2018.ReportedInformation.CountryCode.in_(country_codes),
            mapper_class.GESComponent.in_(ges_components),
            or_(mapper_class.Id.in_(id_ges_components),
                mapper_class.JustificationDelay.is_(None),
                mapper_class.JustificationNonUse.is_(None)
                )
        )

        count, res = db.get_item_by_conditions_joined(
            mapper_class,
            sql2018.ReportedInformation,
            'Id',
            self.condition_ges_component,
            page=page
        )

        if not res:
            return 0, []

        if getattr(res, 'JustificationDelay', 0) \
                or getattr(res, 'JustificationNonUse', 0):
            self.show_extra_data = False

            return count, res

        self.show_extra_data = True
        id_ges_comp = res.Id
        res = db.get_related_record(
            determination_mc,
            'IdGESComponent',
            id_ges_comp
        )

        return res

    def get_extra_data(self):
        if not self.item or not self.show_extra_data:
            return {}

        mc = sql2018.ART9GESMarineUnit
        id_ges_deter = self.item.Id

        marine_units = db.get_unique_from_mapper(
            mc,
            'MarineReportingUnit',
            mc.IdGESDetermination == id_ges_deter
        )

        res = list()

        if marine_units:
            res.append(
                ('Indicators Dataset', {'': marine_units})
            )

        return res


@register_form_2018
class A2018Article9(EmbededForm):
    title = 'Article 9 (GES determination)'
    mapper_class = sql2018.ART9GESGESComponent
    display_klass = Art9Display
    features_mc = sql2018.ART9GESGESDeterminationFeature

    fields = Fields(interfaces.ICountryCodeGESComponents)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['ges_component'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_ges_component(self):
        return all_values_from_field(self, self.fields['ges_component'])


class A2018FeaturesForm(EmbededForm):

    fields = Fields(interfaces.IFeatures)
    fields['feature'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        klass = self.context.display_klass

        return klass(self, self.request)

    def default_feature(self):
        return all_values_from_field(self, self.fields['feature'])


class A2018Art10Display(ItemDisplayForm):
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    css_class = 'left-side-form'
    target_ids = tuple()

    def download_results(self):
        # mapper_class = self.context.context.mapper_class
        target_mc = self.context.context.target_mc

        count, target = db.get_all_records(
            target_mc,
            target_mc.Id.in_(self.target_ids)
        )
        id_marine_units = [x.IdMarineUnit for x in target]

        count, marine_unit = db.get_all_records(
            sql2018.ART10TargetsMarineUnit,
            sql2018.ART10TargetsMarineUnit.Id.in_(id_marine_units)
        )

        count, target_feature = db.get_all_records(
            sql2018.ART10TargetsTargetFeature,
            sql2018.ART10TargetsTargetFeature.IdTarget.in_(self.target_ids)
        )

        s = sql2018.ART10TargetsTargetGESComponent
        count, target_ges = db.get_all_records(
            s,
            s.IdTarget.in_(self.target_ids)
        )

        s = sql2018.ART10TargetsProgressAssessment
        count, target_progress = db.get_all_records(
            s,
            s.IdTarget.in_(self.target_ids)
        )

        xlsdata = [
            # worksheet title, row data
            ('ART10TargetsMarineUnit', marine_unit),
            ('ART10TargetsTarget', target),
            ('ART10TargetsTargetFeature', target_feature),
            ('ART10TargetsTargetGESComponent', target_ges),
            ('ART10TargetsProgressAssessment', target_progress),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        country_codes = self.context.context.data.get('country_code', [])
        marine_units = self.context.context.data.get('marine_reporting_unit',
                                                     [])
        features = self.context.data.get('feature', [])
        ges_components = self.context.data.get('ges_component', [])

        mapper_class = self.context.context.mapper_class
        count, target_ids = db.get_all_records_outerjoin(
            mapper_class,
            sql2018.ReportedInformation,
            and_(mapper_class.MarineReportingUnit.in_(marine_units),
                 sql2018.ReportedInformation.CountryCode.in_(country_codes))
        )

        target_ids = [x.Id for x in target_ids]

        features_ids = db.get_unique_from_mapper(
            sql2018.ART10TargetsTargetFeature,
            'IdTarget',
            sql2018.ART10TargetsTargetFeature.Feature.in_(features)
        )

        s = sql2018.ART10TargetsTargetGESComponent
        ges_components_ids = db.get_unique_from_mapper(
            s,
            'IdTarget',
            s.GESComponent.in_(ges_components)
        )

        target_ids = tuple(set(target_ids)
                           & set(features_ids)
                           & set(ges_components_ids))
        self.target_ids = target_ids

        mc = sql2018.ART10TargetsTarget
        res = db.get_item_by_conditions(
            mc,
            'Id',
            mc.Id.in_(target_ids),
            page=page
        )

        return res

    def get_extra_data(self):
        if not self.item:
            return []

        target_id = self.item.Id
        mc = sql2018.ART10_Targets_ProgressAssessment
        column = 'IdTarget'
        result = db.get_all_columns_from_mapper(
            mc,
            column,
            getattr(mc, column) == target_id
        )

        paremeters = db_objects_to_dict(result)
        paremeters = pivot_data(paremeters, 'Parameter')

        res = [
            ('Parameters', paremeters),
        ]

        return res


@register_form_2018
class A2018Article10(EmbededForm):
    title = 'Article 10 (Targets)'
    mapper_class = sql2018.ART10TargetsMarineUnit
    display_klass = A2018Art10Display
    target_mc = sql2018.ART10TargetsTarget
    features_mc = sql2018.ART10TargetsTargetFeature
    features_relation_column = 'IdTarget'
    ges_components_mc = sql2018.ART10TargetsTargetGESComponent
    ges_components_relation_column = 'IdTarget'

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self,
                                     self.fields['marine_reporting_unit'])


class A2018FeaturesGESComponentsForm(EmbededForm):
    fields = Fields(interfaces.IFeaturesGESComponents)
    fields['feature'].widgetFactory = CheckBoxFieldWidget
    fields['ges_component'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        klass = self.context.display_klass

        return klass(self, self.request)

    def default_feature(self):
        return all_values_from_field(self, self.fields['feature'])

    def default_ges_component(self):
        return all_values_from_field(self, self.fields['ges_component'])


class A2018Art81abDisplay(ItemDisplayForm):
    css_class = 'left-side-form'
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    def download_results(self):
        # mapper_class = self.context.context.mapper_class
        overall_status_mc = self.context.context.features_mc

        count, overall_status = db.get_all_records(
            overall_status_mc,
            self.conditions_overall_status
        )
        id_marine_unit = [x.IdMarineUnit for x in overall_status]
        id_overall_status = [x.Id for x in overall_status]

        count, marine_unit = db.get_all_records(
            sql2018.ART8GESMarineUnit,
            sql2018.ART8GESMarineUnit.Id.in_(id_marine_unit)
        )

        mc = sql2018.ART8GESOverallStatusPressure
        count, overall_status_pressure = db.get_all_records(
            mc,
            mc.IdOverallStatus.in_(id_overall_status)
        )

        mc = sql2018.ART8GESOverallStatusTarget
        count, overall_status_target = db.get_all_records(
            mc,
            mc.IdOverallStatus.in_(id_overall_status)
        )

        mc = sql2018.ART8GESElementStatu
        count, element_status = db.get_all_records(
            mc,
            mc.IdOverallStatus.in_(id_overall_status)
        )
        id_element_status = [x.Id for x in element_status]

        mc = sql2018.ART8GESCriteriaStatu
        count, criteria_status = db.get_all_records(
            mc,
            and_(mc.IdOverallStatus.in_(id_overall_status),
                 mc.IdElementStatus.in_(id_element_status))
        )
        id_criteria_status = [x.Id for x in criteria_status]

        mc = sql2018.ART8GESCriteriaValue
        count, criteria_value = db.get_all_records(
            mc,
            mc.IdCriteriaStatus.in_(id_criteria_status)
        )
        id_criteria_value = [x.Id for x in criteria_value]

        mc = sql2018.ART8GESCriteriaValuesIndicator
        count, criteria_value_ind = db.get_all_records(
            mc,
            mc.IdCriteriaValues.in_(id_criteria_value)
        )

        xlsdata = [
            # worksheet title, row data
            ('ART8GESMarineUnit', marine_unit),
            ('ART8GESOverallStatu', overall_status),
            ('ART8GESOverallStatusPressure', overall_status_pressure),
            ('ART8GESOverallStatusTarget', overall_status_target),
            ('ART8GESElementStatu', element_status),
            ('ART8GESCriteriaStatu', criteria_status),
            ('ART8GESCriteriaValue', criteria_value),
            ('ART8GESCriteriaValuesIndicator', criteria_value_ind),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        countries = self.context.context.data.get('country_code', [])
        mrus = self.context.context.data.get('marine_reporting_unit', [])
        features = self.context.data.get('feature', [])
        ges_components = self.context.data.get('ges_component', [])
        mapper_class = self.context.context.mapper_class
        overall_status_mc = self.context.context.features_mc
        mc_countries = sql2018.ReportedInformation

        conditions = list()

        if countries:
            conditions.append(mc_countries.CountryCode.in_(countries))

        if mrus:
            conditions.append(mapper_class.MarineReportingUnit.in_(mrus))

        count, id_marine_units = db.get_all_records_outerjoin(
            mapper_class,
            mc_countries,
            *conditions
        )
        id_marine_units = [int(x.Id) for x in id_marine_units]

        self.conditions_overall_status = and_(
            overall_status_mc.Feature.in_(features),
            overall_status_mc.GESComponent.in_(ges_components),
            overall_status_mc.IdMarineUnit.in_(id_marine_units)
        )

        res = db.get_item_by_conditions(
            overall_status_mc,
            'Id',
            self.conditions_overall_status,
            page=page
        )

        return res

    def get_extra_data(self):
        if not self.item:
            return {}

        id_overall = self.item.get('Id', 0)
        excluded_columns = ('Id', 'IdOverallStatus')

        pressure_codes = db.get_unique_from_mapper(
            sql2018.ART8GESOverallStatusPressure,
            'PressureCode',
            sql2018.ART8GESOverallStatusPressure.IdOverallStatus == id_overall
        )

        target_codes = db.get_unique_from_mapper(
            sql2018.ART8GESOverallStatusTarget,
            'TargetCode',
            sql2018.ART8GESOverallStatusTarget.IdOverallStatus == id_overall
        )

        element_status = db.get_all_columns_from_mapper(
            sql2018.ART8GESElementStatu,
            'Id',
            sql2018.ART8GESElementStatu.IdOverallStatus == id_overall
        )
        element_status = db_objects_to_dict(element_status,
                                            excluded_columns)
        element_status_pivot = list()

        for x in element_status:
            element = x.pop('Element', None)
            element2 = x.pop('Element2', None)
            x['Element / Element2'] = ' / '.join((element, element2))
            element_status_pivot.append(x)

        element_status_pivot = pivot_data(element_status_pivot,
                                          'Element / Element2')
        # TODO get the Id for the selected element status
        id_elem_status = [x.Id for x in element_status_pivot]

        s = sql2018.ART8GESCriteriaStatu
        conditions = list()
        conditions.append(s.IdOverallStatus == id_overall)

        if element_status_pivot:
            conditions.append(
                s.IdElementStatus.in_(id_elem_status)
            )

        criteria_status = db.get_all_columns_from_mapper(
            sql2018.ART8GESCriteriaStatu,
            'Id',
            *conditions
        )
        criteria_status = db_objects_to_dict(criteria_status,
                                             excluded_columns)
        criteria_status = pivot_data(criteria_status, 'Criteria')

        # TODO get the Id for the selected criteria status
        id_criteria_status = [x.Id for x in criteria_status]
        s = sql2018.ART8GESCriteriaValue
        criteria_value = db.get_all_columns_from_mapper(
            s,
            'Id',
            s.IdCriteriaStatus.in_(id_criteria_status)
        )
        criteria_value = db_objects_to_dict(criteria_value,
                                            excluded_columns)
        criteria_value = pivot_data(criteria_value, 'Parameter')

        # TODO get the Id for the selected criteria value
        id_criteria_value = [x.Id for x in criteria_value]

        s = sql2018.ART8GESCriteriaValuesIndicator
        criteria_value_ind = db.get_unique_from_mapper(
            s,
            'IndicatorCode',
            s.IdCriteriaValues.in_(id_criteria_value)
        )

        res = list()

        if pressure_codes:
            res.append(
                ('Pressure code(s)', {
                    '': [{'PressureCode': x} for x in pressure_codes]
                }))

        if target_codes:
            res.append(
                ('Target code(s)', {
                    '': [{'TargetCode': x} for x in target_codes]
                }))

        if element_status_pivot:
            res.append(
                ('Element Status', element_status_pivot)
            )

        if criteria_status:
            res.append(
                ('Criteria Status', criteria_status)
            )

        if criteria_value:
            res.append(
                ('Criteria Value', criteria_value)
            )

        if criteria_value_ind:
            res.append(
                ('Criteria Value Indicator', {
                    '': [{'IndicatorCode': x} for x in criteria_value_ind]
                }))

        return res


@register_form_2018
class A2018Article81ab(EmbededForm):
    title = 'Article 8.1ab (GES assessments)'
    mapper_class = sql2018.ART8GESMarineUnit
    display_klass = A2018Art81abDisplay
    target_mc = sql2018.ART8GESOverallStatu
    features_mc = sql2018.ART8GESOverallStatu
    features_relation_column = 'Id'
    ges_components_mc = sql2018.ART8GESOverallStatu
    ges_components_relation_column = 'Id'

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self,
                                     self.fields['marine_reporting_unit'])


class A2018Art81cDisplay(ItemDisplayForm):
    css_class = 'left-side-form'
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    id_marine_units = list()

    def download_results(self):
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        features = self.context.data.get('feature', ())

        conditions = list()
        conditions.append(features_mc.IdMarineUnit.in_(self.id_marine_units))

        if features:
            conditions.append(features_mc.Feature.in_(features))

        count, feature = db.get_all_records(
            features_mc,
            *conditions
        )
        id_marine_units = [x.IdMarineUnit for x in feature]
        id_feature = [x.Id for x in feature]

        count, marine_unit = db.get_all_records(
            mapper_class,
            mapper_class.Id.in_(id_marine_units)
        )

        count, feature_nace = db.get_all_records(
            sql2018.ART8ESAFeatureNACE,
            sql2018.ART8ESAFeatureNACE.IdFeature.in_(id_feature)
        )

        count, feature_ges_comp = db.get_all_records(
            sql2018.ART8ESAFeatureGESComponent,
            sql2018.ART8ESAFeatureGESComponent.IdFeature.in_(id_feature)
        )

        count, cost_degradation = db.get_all_records(
            sql2018.ART8ESACostDegradation,
            sql2018.ART8ESACostDegradation.IdFeature.in_(id_feature)
        )
        id_cost_degrad = [x.Id for x in cost_degradation]

        mc = sql2018.ART8ESACostDegradationIndicator
        count, cost_degradation_ind = db.get_all_records(
            mc,
            mc.IdCostDegradation.in_(id_cost_degrad)
        )

        count, uses_activity = db.get_all_records(
            sql2018.ART8ESAUsesActivity,
            sql2018.ART8ESAUsesActivity.IdFeature.in_(id_feature)
        )
        id_uses_act = [x.Id for x in uses_activity]

        mc = sql2018.ART8ESAUsesActivitiesIndicator
        count, uses_activity_ind = db.get_all_records(
            mc,
            mc.IdUsesActivities.in_(id_uses_act)
        )

        mc = sql2018.ART8ESAUsesActivitiesEcosystemService
        count, uses_activity_eco = db.get_all_records(
            mc,
            mc.IdUsesActivities.in_(id_uses_act)
        )

        mc = sql2018.ART8ESAUsesActivitiesPressure
        count, uses_activity_pres = db.get_all_records(
            mc,
            mc.IdUsesActivities.in_(id_uses_act)
        )

        xlsdata = [
            # worksheet title, row data
            ('ART8ESAMarineUnit', marine_unit),
            ('ART8ESAFeature', feature),
            ('ART8ESAFeatureNACE', feature_nace),
            ('ART8ESAFeatureGESComponent', feature_ges_comp),
            ('ART8ESACostDegradation', cost_degradation),
            ('ART8ESACostDegradationIndicator', cost_degradation_ind),
            ('ART8ESAUsesActivity', uses_activity),
            ('ART8ESAUsesActivitiesIndicator', uses_activity_ind),
            ('ART8ESAUsesActEcosystemService', uses_activity_eco),
            ('ART8ESAUsesActivitiesPressure', uses_activity_pres),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        countries = self.context.context.data.get('country_code', ())
        features = self.context.data.get('feature', ())
        mrus = self.context.data.get('marine_reporting_unit', ())
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        mc_countries = sql2018.ReportedInformation

        conditions = list()

        if countries:
            conditions.append(mc_countries.CountryCode.in_(countries))

        if mrus:
            conditions.append(mapper_class.MarineReportingUnit.in_(mrus))

        count, id_marine_units = db.get_all_records_outerjoin(
            mapper_class,
            mc_countries,
            *conditions
        )
        id_marine_units = [int(x.Id) for x in id_marine_units]
        self.id_marine_units = id_marine_units

        res = db.get_item_by_conditions(
            features_mc,
            'Id',
            and_(features_mc.Feature.in_(features),
                 features_mc.IdMarineUnit.in_(id_marine_units)),
            page=page
        )

        return res

    def get_extra_data(self):
        if not self.item:
            return {}

        id_feature = self.item.get('Id', 0)
        excluded_columns = ('Id', 'IdFeature')

        nace_codes = db.get_unique_from_mapper(
            sql2018.ART8ESAFeatureNACE,
            'NACECode',
            sql2018.ART8ESAFeatureNACE.IdFeature == id_feature
        )

        ges_components = db.get_unique_from_mapper(
            sql2018.ART8ESAFeatureGESComponent,
            'GESComponent',
            sql2018.ART8ESAFeatureGESComponent.IdFeature == id_feature
        )

        cost_degradation = db.get_all_columns_from_mapper(
            sql2018.ART8ESACostDegradation,
            'Id',
            sql2018.ART8ESACostDegradation.IdFeature == id_feature
        )
        cost_degradation = db_objects_to_dict(cost_degradation,
                                              excluded_columns)

        ids_cost_degradation = [x.Id for x in cost_degradation]
        mc = sql2018.ART8ESACostDegradationIndicator
        cost_degradation_indicators = db.get_unique_from_mapper(
            mc,
            'IndicatorCode',
            mc.IdCostDegradation.in_(ids_cost_degradation)
        )

        uses_activities = db.get_all_columns_from_mapper(
            sql2018.ART8ESAUsesActivity,
            'Id',
            sql2018.ART8ESAUsesActivity.IdFeature == id_feature
        )
        uses_activities = db_objects_to_dict(uses_activities,
                                             excluded_columns)

        ids_uses_act = [x.Id for x in uses_activities]
        s = sql2018.ART8ESAUsesActivitiesIndicator
        uses_act_indicators = db.get_unique_from_mapper(
            s,
            'IndicatorCode',
            s.IdUsesActivities.in_(ids_uses_act)
        )

        s = sql2018.ART8ESAUsesActivitiesEcosystemService
        uses_act_eco = db.get_unique_from_mapper(
            s,
            'EcosystemServiceCode',
            s.IdUsesActivities.in_(ids_uses_act)
        )

        s = sql2018.ART8ESAUsesActivitiesPressure
        uses_act_pres = db.get_unique_from_mapper(
            s,
            'PressureCode',
            s.IdUsesActivities.in_(ids_uses_act)
        )

        res = list()

        if nace_codes:
            res.append(
                ('NACEcode(s)', {
                    '': [{'NACECode': x} for x in nace_codes]
                }))

        if ges_components:
            res.append(
                ('GEScomponent(s)', {
                    '': [{'GESComponent': x} for x in ges_components]
                }))

        if cost_degradation:
            res.append(
                ('Cost Degradation', {'': cost_degradation})
            )

        if cost_degradation_indicators:
            res.append(
                ('Cost Degradation Indicator(s)', {
                    '': [{'IndicatorCode': x}
                         for x in cost_degradation_indicators]
                }))

        if uses_activities:
            res.append(
                ('Uses Activities', {'': uses_activities})
            )

        if uses_act_indicators:
            res.append(
                ('Uses Activities Indicator(s)', {
                    '': [{'IndicatorCode': x} for x in uses_act_indicators]
                }))

        if uses_act_eco:
            res.append(
                ('Uses Activities Ecosystem Service(s)', {
                    '': [{'EcosystemServiceCode': x} for x in uses_act_eco]
                }))

        if uses_act_pres:
            res.append(
                ('Uses Activities Pressure(s)', {
                    '': [{'PressureCode': x} for x in uses_act_pres]
                }))

        return res


class A2018Features81cForm(EmbededForm):

    fields = Fields(interfaces.IFeatures81c)
    fields['feature'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        klass = self.context.display_klass

        return klass(self, self.request)

    def default_feature(self):
        return all_values_from_field(self, self.fields['feature'])


@register_form_2018
class A2018Article81c(EmbededForm):
    title = 'Article 8.1c (Economic and social analysis)'
    mapper_class = sql2018.ART8ESAMarineUnit
    display_klass = A2018Art81cDisplay
    features_mc = sql2018.ART8ESAFeature

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018Features81cForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self,
                                     self.fields['marine_reporting_unit'])


class A2018IndicatorsGESFeatureMRUForm(EmbededForm):
    fields = Fields(interfaces.IIndicatorsGESFeatureMRU)
    fields['ges_component'].widgetFactory = CheckBoxFieldWidget
    fields['feature'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018IndicatorsDisplay(self, self.request)

    def default_ges_component(self):
        return all_values_from_field(self, self.fields['ges_component'])

    def default_feature(self):
        return all_values_from_field(self, self.fields['feature'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self,
                                     self.fields['marine_reporting_unit'])


class A2018IndicatorsDisplay(ItemDisplayForm):
    title = "Indicator Display Form"
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')
    css_class = 'left-side-form'

    conditions_ind_assess = list()

    def download_results(self):
        if not self.conditions_ind_assess:
            return []
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        ges_components_mc = self.context.context.ges_components_mc
        marine_mc = self.context.context.marine_mc

        count, indicator_assessment = db.get_all_records(
            mapper_class,
            *self.conditions_ind_assess
        )

        ids_indicator = [x.Id for x in indicator_assessment]

        count, indicator_dataset = db.get_all_records(
            sql2018.IndicatorsDataset,
            sql2018.IndicatorsDataset.IdIndicatorAssessment.in_(ids_indicator)
        )

        count, feature_ges_comp = db.get_all_records(
            ges_components_mc,
            ges_components_mc.IdIndicatorAssessment.in_(ids_indicator)
        )
        id_ges_components = [x.Id for x in feature_ges_comp]

        count, feature_feature = db.get_all_records(
            features_mc,
            features_mc.IdGESComponent.in_(id_ges_components)
        )

        count, marine_unit = db.get_all_records(
            marine_mc,
            marine_mc.IdIndicatorAssessment.in_(ids_indicator)
        )

        xlsdata = [
            # worksheet title, row data
            ('IndicatorsIndicatorAssessment', indicator_assessment),
            ('IndicatorsDataset', indicator_dataset),
            ('IndicatorsFeatureFeature', feature_feature),
            ('IndicatorsFeatureGESComponent', feature_ges_comp),
            ('IndicatorsMarineUnit', marine_unit),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        countries = self.context.context.data.get('country_code', ())
        ges_components = self.context.data.get('ges_component', ())
        features = self.context.data.get('feature', ())
        mrus = self.context.data.get('marine_reporting_unit', ())
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        ges_components_mc = self.context.context.ges_components_mc
        marine_mc = self.context.context.marine_mc
        mc_countries = sql2018.ReportedInformation

        conditions = list()

        if countries:
            conditions.append(mc_countries.CountryCode.in_(countries))

        count, ids_indicator = db.get_all_records_outerjoin(
            mapper_class,
            mc_countries,
            *conditions
        )
        ids_indicator_main = [int(x.Id) for x in ids_indicator]

        conditions = list()

        if features:
            conditions.append(features_mc.Feature.in_(features))

        if ges_components:
            conditions.append(
                ges_components_mc.GESComponent.in_(ges_components))
        count, ids_ind_ass = db.get_all_records_outerjoin(
            ges_components_mc,
            features_mc,
            *conditions
        )
        ids_ind_ass_ges = [int(x.IdIndicatorAssessment) for x in ids_ind_ass]

        ids_ind_ass_marine = db.get_unique_from_mapper(
            marine_mc,
            'IdIndicatorAssessment',
            marine_mc.MarineReportingUnit.in_(mrus)
        )
        ids_ind_ass_marine = [int(x) for x in ids_ind_ass_marine]

        conditions = list()

        if ids_ind_ass_marine:
            conditions.append(mapper_class.Id.in_(ids_ind_ass_marine))

        if ids_indicator_main:
            conditions.append(mapper_class.Id.in_(ids_indicator_main))

        if ids_ind_ass_ges:
            conditions.append(mapper_class.Id.in_(ids_ind_ass_ges))

        self.conditions_ind_assess = conditions

        res = db.get_item_by_conditions(
            mapper_class,
            'Id',
            *conditions,
            page=page
        )
        # import pdb; pdb.set_trace()

        return res

    def get_extra_data(self):
        if not self.item:
            return {}

        mc = sql2018.IndicatorsDataset
        id_indicator_assessment = self.item.Id

        indicators_dataset = db.get_all_columns_from_mapper(
            mc,
            'Id',
            mc.IdIndicatorAssessment == id_indicator_assessment
        )
        excluded_columns = ('Id', 'IdIndicatorAssessment')
        indicators_dataset = db_objects_to_dict(indicators_dataset,
                                                excluded_columns)

        res = list()

        if indicators_dataset:
            res.append(
                ('Indicators Dataset', {'': indicators_dataset})
            )

        return res


@register_form_2018
class A2018ArticleIndicators(EmbededForm):
    record_title = 'Article Indicators'
    title = 'Indicators'
    mapper_class = sql2018.IndicatorsIndicatorAssessment
    features_mc = sql2018.IndicatorsFeatureFeature
    ges_components_mc = sql2018.IndicatorsFeatureGESComponent
    marine_mc = sql2018.IndicatorsMarineUnit

    fields = Fields(interfaces.ICountryCode)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018IndicatorsGESFeatureMRUForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])
