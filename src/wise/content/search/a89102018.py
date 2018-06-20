from z3c.form.field import Fields
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from wise.content.search import db, interfaces, sql2018
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from .utils import (all_values_from_field, data_to_xls, db_objects_to_dict,
                    default_value_from_field, pivot_data, register_form_art11,
                    register_form_section, register_form_2018)

from .base import (EmbededForm, ItemDisplay,
                   ItemDisplayForm, MultiItemDisplayForm)

from sqlalchemy import and_, or_


class Art9Display(ItemDisplayForm):
    css_class = 'left-side-form'

    def get_db_results(self):
        page = self.get_page()
        mapper_class = self.context.context.mapper_class
        features_mc = self.context.context.features_mc
        ges_deter_mc = sql2018.ART9GESGESDetermination
        country_codes = self.context.context.data.get('country_code', ())
        ges_components = self.context.context.data.get('ges_component', ())
        features = self.context.data.get('feature', ())

        count, res = db.get_item_by_conditions_joined(
            mapper_class,
            sql2018.ReportedInformation,
            'Id',
            and_(sql2018.ReportedInformation.CountryCode.in_(country_codes),
                 mapper_class.GESComponent.in_(ges_components)),
            page=page
        )
        # import pdb;pdb.set_trace()
        if getattr(res, 'JustificationDelay', 0) \
                or getattr(res, 'JustificationNonUse', 0):
            return count, res

        condition = list()
        if features:
            ges_deter_ids = db.get_unique_from_mapper(
                features_mc,
                'IdGESDetermination',
                features_mc.Feature.in_(features)
            )
            ges_deter_ids = [int(x) for x in ges_deter_ids]
            condition.append(ges_deter_mc.Id.in_(ges_deter_ids))

        # res = db.get_item_by_conditions()
        # TODO finish this

        return 0, []


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

    def get_db_results(self):
        page = self.get_page()
        country_codes = self.context.context.data.get('country_code', [])
        marine_units = self.context.context.data.get('marine_reporting_unit', [])
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

        ges_components_ids = db.get_unique_from_mapper(
            sql2018.ART10TargetsTargetGESComponent,
            'IdTarget',
            sql2018.ART10TargetsTargetGESComponent.GESComponent.in_(ges_components)
        )

        target_ids = tuple(set(target_ids) & set(features_ids) & set(ges_components_ids))

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
    features_mc = sql2018.ART10TargetsTargetFeature
    ges_components_mc = sql2018.ART10TargetsTargetGESComponent

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    mc_features = sql2018.ART10TargetsTargetFeature
    mc_ges_components = sql2018.ART10TargetsTargetGESComponent

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self, self.fields['marine_reporting_unit'])


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

    def get_db_results(self):
        return 0, []


@register_form_2018
class A2018Article81ab(EmbededForm):
    title = 'Article 8.1ab (GES assessments)'
    mapper_class = sql2018.ART8GESMarineUnit
    display_klass = A2018Art81abDisplay

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self, self.fields['marine_reporting_unit'])


class A2018Art81cDisplay(ItemDisplayForm):
    css_class = 'left-side-form'

    def get_db_results(self):
        return 0, []


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
        return A2018FeaturesForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self, self.fields['marine_reporting_unit'])


class A2018IndicatorsDisplay(ItemDisplayForm):
    css_class = 'left-side-form'

    def get_db_results(self):
        return 0, []



@register_form_2018
class A2018ArticleIndicators(EmbededForm):
    title = 'Indicators'
    mapper_class = sql2018.IndicatorsIndicatorAssessment
    display_klass = A2018IndicatorsDisplay
    features_mc = sql2018.IndicatorsFeatureFeature
    ges_components_mc = sql2018.IndicatorsFeatureGESComponent

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self, self.fields['marine_reporting_unit'])

