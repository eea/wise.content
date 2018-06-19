from z3c.form.field import Fields
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from wise.content.search import db, interfaces, sql2018

from .utils import (all_values_from_field, data_to_xls, db_objects_to_dict,
                    default_value_from_field, pivot_data, register_form_art11,
                    register_form_section, register_form_2018)

from .base import (EmbededForm, ItemDisplay, ItemDisplayForm, MainForm,
                   MultiItemDisplayForm)


@register_form_2018
class A2018Article9(EmbededForm):
    title = 'Article 9 (GES determination)'
    mapper_class = sql2018.ART9GESGESComponent

    fields = Fields(interfaces.ICountryCodeGESComponents)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['ges_component'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return Art9Display(self, self.request)


class Art9Display(ItemDisplayForm):
    pass


@register_form_2018
class A2018Article10(EmbededForm):
    title = 'Article 10 (Targets)'
    mapper_class = sql2018.ART10TargetsMarineUnit

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
        return None


@register_form_2018
class A2018Article81ab(EmbededForm):
    title = 'Article 8.1ab (GES assessments)'
    mapper_class = sql2018.ART8GESMarineUnit

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self, self.fields['marine_reporting_unit'])


@register_form_2018
class A2018Article81c(EmbededForm):
    title = 'Article 8.1c (Economic and social analysis)'
    mapper_class = sql2018.ART8ESAMarineUnit

    fields = Fields(interfaces.ICountryCodeMarineReportingUnits)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget
    fields['marine_reporting_unit'].widgetFactory = CheckBoxFieldWidget

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])

    def default_marine_reporting_unit(self):
        return all_values_from_field(self, self.fields['marine_reporting_unit'])


@register_form_2018
class A2018ArticleIndicators(EmbededForm):
    title = 'Indicators'
    mapper_class = sql2018.IndicatorsIndicatorAssessment

    fields = Fields(interfaces.ICountryCode)
    fields['country_code'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A2018FeaturesGESComponentsForm(self, self.request)

    def default_country_code(self):
        return all_values_from_field(self, self.fields['country_code'])
