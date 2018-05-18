from zope.schema import Choice

from wise.content.search import db, sql
from z3c.form.field import Fields

from .base import (EmbededForm, ItemDisplay, MarineUnitIDSelectForm,
                   MultiItemDisplayForm)
from .utils import register_form, register_form_section, register_subform
from .vocabulary import SubFormsVocabulary


@register_form
class A81aForm(EmbededForm):
    """ Main form for A81a.

    Allows selecting between Ecosystem, Functional, etc
    """

    title = 'Article 8.1a (Analysis of the environmental status)'

    @property
    def fields(self):
        # TODO: could this be reimplemented with simple vocab?
        theme = Choice(
            __name__='theme',
            title=u"Select theme",
            required=False,
            vocabulary=SubFormsVocabulary(self.__class__)
        )

        return Fields(theme)

    def get_subform(self):
        klass = self.data.get('theme')

        return super(A81aForm, self).get_subform(klass)


# region Ecosystem(s)
@register_subform(A81aForm)
class A81aEcoSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Ecosystem(s)'
    mapper_class = sql.MSFD8aEcosystem

    def get_subform(self):
        return A81aEcoItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aEcoItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aEcosystem
    order_field = 'MSFD8a_Ecosystem_ID'


@register_form_section(A81aEcoItemDisplay)
class A81aEcosystemPressures(ItemDisplay):
    title = 'Pressures and impacts'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aEcosystemPressuresImpact,
                'MSFD8a_Ecosystem',
                self.context.item.MSFD8a_Ecosystem_ID
            )


@register_form_section(A81aEcoItemDisplay)
class A81aEcosystemAsessment(ItemDisplay):
    title = 'Status Asessment'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aEcosystemStatusAssessment,
                'MSFD8a_Ecosystem',
                self.context.item.MSFD8a_Ecosystem_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8aEcosystemStatusIndicator,
            'MSFD8a_Ecosystem_StatusAssessment',
            self.item.MSFD8a_Ecosystem_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]

# endregion Ecosystem


# region Functional Group(s)
@register_subform(A81aForm)
class A81aFunctSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Functional group(s)'
    mapper_class = sql.MSFD8aFunctional

    def get_subform(self):
        return A81aFunctItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aFunctItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aFunctional
    order_field = 'MSFD8a_Functional_ID'


@register_form_section(A81aFunctItemDisplay)
class A81aFunctionalGroupPressures(ItemDisplay):
    title = 'Pressures and impacts'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aFunctionalPressuresImpact,
                'MSFD8a_Functional',
                self.context.item.MSFD8a_Functional_ID
            )


@register_form_section(A81aFunctItemDisplay)
class A81aFunctionalGroupAsessment(ItemDisplay):
    title = 'Status Asessment'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aFunctionalStatusAssessment,
                'MSFD8a_Functional',
                self.context.item.MSFD8a_Functional_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8aFunctionalStatusIndicator,
            'MSFD8a_Functional_StatusAssessment',
            self.item.MSFD8a_Functional_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]
# endregion Functional Group


# region Habitat(s)
@register_subform(A81aForm)
class A81aHabitatSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Habitat(s)'
    mapper_class = sql.MSFD8aHabitat

    def get_subform(self):
        return A81aHabitatItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aHabitatItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aHabitat
    order_field = 'MSFD8a_Habitat_ID'


@register_form_section(A81aHabitatItemDisplay)
class A81aHabitatPressures(ItemDisplay):
    title = 'Pressures and impacts'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aHabitatPressuresImpact,
                'MSFD8a_Habitat',
                self.context.item.MSFD8a_Habitat_ID
            )


@register_form_section(A81aHabitatItemDisplay)
class A81aHabitatAsessment(ItemDisplay):
    title = 'Status Asessment'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aHabitatStatusAssessment,
                'MSFD8a_Habitat',
                self.context.item.MSFD8a_Habitat_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8aHabitatStatusIndicator,
            'MSFD8a_Habitat_StatusAssessment',
            self.item.MSFD8a_Habitat_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]

# endregion Habitat(s)


# region Species(s)
@register_subform(A81aForm)
class A81aSpeciesSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Species(s)'
    mapper_class = sql.MSFD8aSpecy

    def get_subform(self):
        return A81aSpeciesItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aSpeciesItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aSpecy
    order_field = 'MSFD8a_Species_ID'


@register_form_section(A81aSpeciesItemDisplay)
class A81aSpeciesPressures(ItemDisplay):
    title = 'Pressures and impacts'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aSpeciesPressuresImpact,
                'MSFD8a_Species',
                self.context.item.MSFD8a_Species_ID
            )


@register_form_section(A81aSpeciesItemDisplay)
class A81aSpeciesAsessment(ItemDisplay):
    title = 'Status Asessment'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aSpeciesStatusAssessment,
                'MSFD8a_Species',
                self.context.item.MSFD8a_Species_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8aSpeciesStatusIndicator,
            'MSFD8a_Species_StatusAssessment',
            self.item.MSFD8a_Species_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]

# endregion Species(s)


# region Other(s)
@register_subform(A81aForm)
class A81aOtherSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Other(s)'
    mapper_class = sql.MSFD8aOther

    def get_subform(self):
        return A81aOtherItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aOtherItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aOther
    order_field = 'MSFD8a_Other_ID'
# TODO
# MSFD8aOtherPressuresImpact table is missing?
# @register_form_section(A81aOtherItemDisplay)
# class A81aOtherPressures(ItemDisplay):
#     title = 'Pressures and impacts'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8aOtherPressuresImpact,
#                 'MSFD8a_Other',
#                 self.context.item.MSFD8a_Other_ID
#             )


@register_form_section(A81aOtherItemDisplay)
class A81aOtherAsessment(ItemDisplay):
    title = 'Status Asessment'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8aOtherStatusAssessment,
                'MSFD8a_Other',
                self.context.item.MSFD8a_Other_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8aOtherStatusIndicator,
            'MSFD8a_Other_StatusAssessment',
            self.item.MSFD8a_Other_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]

# endregion Other(s)


# region Nis Inventory(s)
@register_subform(A81aForm)
class A81aNisSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'NIS Inventory'
    mapper_class = sql.MSFD8aNISInventory

    def get_subform(self):
        return A81aNisItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aNisItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aNISInventory
    order_field = 'MSFD8a_NISInventory_ID'

    # def get_db_results(self):
    #     # if self.context.item:
    #         return db.get_related_record(
    #             self.mapper_class,
    #             'MarineUnitID',
    #             self.item.MSFD8a_NISInventory_ID
    #         )

# endregion Nis Inventory(s)


# region Physical
@register_subform(A81aForm)
class A81aPhysicalSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1a form
    """
    title = 'Physical'
    mapper_class = sql.MSFD8aPhysical

    def get_subform(self):
        return A81aPhysicalItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A81aPhysicalItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1a
    """
    mapper_class = sql.MSFD8aPhysical
    order_field = 'MSFD8a_Physical_ID'

    # def get_db_results(self):
    #     # if self.context.item:
    #         return db.get_related_record(
    #             self.mapper_class,
    #             'MarineUnitID',
    #             self.item.MSFD8a_NISInventory_ID
    #         )

# endregion Physical


@register_form
class A81bForm(EmbededForm):
    """ Main form for A81b.

    Allows selecting between Extraction of fish, seaweed, etc
    """

    title = 'Article 8.1b (Analysis of pressure impacts)'

    @property
    def fields(self):
        # TODO: could this be reimplemented with simple vocab?
        theme = Choice(
            __name__='theme',
            title=u"Select theme",
            required=False,
            vocabulary=SubFormsVocabulary(self.__class__)
        )

        return Fields(theme)

    def get_subform(self):
        klass = self.data.get('theme')

        return super(A81bForm, self).get_subform(klass)


# region Extraction of fish and shellfish
class A81bExtractionFishItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bExtractionFishShellfish
    order_field = 'MSFD8b_ExtractionFishShellfish_ID'


@register_subform(A81bForm)
class A81bExtractionFishSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Extraction of fish and shellfish'
    mapper_class = sql.MSFD8bExtractionFishShellfish

    def get_subform(self):
        return A81bExtractionFishItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bExtractionFishItemDisplay)
class A81aExtractionFishAssessment(ItemDisplay):
    title = 'Asessment of extraction'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bExtractionFishShellfishAssesment,
                'MSFD8b_ExtractionFishShellfish',
                self.context.item.MSFD8b_ExtractionFishShellfish_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bExtractionFishShellfishAssesmentIndicator,
            'MSFD8b_ExtractionFishShellfish_Assesment',
            self.item.MSFD8b_ExtractionFishShellfish_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]


#  TODO
# MSFD8bExtractionFishShellfishActivity is not directly related to
# MSFD8b_ExtractionFishShellfish table
# needs to be joined with MSFD8bExtractionFishShellfishActivityDescription
# table first
# @register_form_section(A81bExtractionFishItemDisplay)
# class A81bExtractionFishActivities(ItemDisplay):
#     title = 'Activities producing'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bExtractionFishShellfishActivity,
#                 'MSFD8b_ExtractionFishShellfish',
#                 self.context.item.MSFD8b_ExtractionFishShellfish_ID
#             )


@register_form_section(A81bExtractionFishItemDisplay)
class A81bExtractionFishImpacts(ItemDisplay):
    title = 'Impacts produced'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bExtractionFishShellfishSumInfo2ImpactedElement,
                'MSFD8b_ExtractionFishShellfish',
                self.context.item.MSFD8b_ExtractionFishShellfish_ID
            )
# endregion Extraction of fish and shellfish


# region Extraction of seaweed, maerl and other
class A81bExtractionSeaweedItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bExtractionSeaweedMaerlOther
    order_field = 'MSFD8b_ExtractionSeaweedMaerlOther_ID'


@register_subform(A81bForm)
class A81bExtractionSeaweedSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Extraction of seaweed, maerl and other'
    mapper_class = sql.MSFD8bExtractionSeaweedMaerlOther

    def get_subform(self):
        return A81bExtractionSeaweedItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bExtractionSeaweedItemDisplay)
class A81aExtractionSeaweedAssessment(ItemDisplay):
    title = 'Asessment of extraction'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bExtractionSeaweedMaerlOtherAssesment,
                'MSFD8b_ExtractionSeaweedMaerlOther',
                self.context.item.MSFD8b_ExtractionSeaweedMaerlOther_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bExtractionSeaweedMaerlOtherAssesmentIndicator,
            'MSFD8b_ExtractionSeaweedMaerlOther_Assesment',
            self.item.MSFD8b_ExtractionSeaweedMaerlOther_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]

# TODO
# MSFD8bExtractionSeaweedMaerlOtherActivity is not directly related to
# MSFD8b_ExtractionSeaweedMaerlOther table
# needs to be joined with MSFD8bExtractionSeaweedMaerlOtherActivityDescription
# table first
# @register_form_section(A81bExtractionSeaweedItemDisplay)
# class A81bExtractionSeaweedActivities(ItemDisplay):
#     title = 'Activities producing'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bExtractionSeaweedMaerlOtherActivity,
#                 'MSFD8b_ExtractionSeaweedMaerlOther',
#                 self.context.item.MSFD8b_ExtractionSeaweedMaerlOther_ID
#             )


@register_form_section(A81bExtractionSeaweedItemDisplay)
class A81bExtractionSeaweedImpacts(ItemDisplay):
    title = 'Impacts produced'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bExtractionSeaweedMaerlOtherSumInfo2ImpactedElement,
                'MSFD8b_ExtractionSeaweedMaerlOther',
                self.context.item.MSFD8b_ExtractionSeaweedMaerlOther_ID
            )
# endregion Extraction of seaweed, maerl and other


# region Hazardous substances
class A81bHazardousItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bHazardousSubstance
    order_field = 'MSFD8b_HazardousSubstances_ID'


@register_subform(A81bForm)
class A81bHazardousSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Hazardous substances'
    mapper_class = sql.MSFD8bHazardousSubstance

    def get_subform(self):
        return A81bHazardousItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bHazardousItemDisplay)
class A81aHazardousAssessment(ItemDisplay):
    title = 'Asessment of hazardous substances'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bHazardousSubstancesAssesment,
                'MSFD8b_HazardousSubstances',
                self.context.item.MSFD8b_HazardousSubstances_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bHazardousSubstancesAssesmentIndicator,
            'MSFD8b_HazardousSubstances_Assesment',
            self.item.MSFD8b_HazardousSubstances_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]

#  TODO
# MSFD8bHazardousSubstancesActivity is not directly related to
# MSFD8b_HazardousSubstances table
# needs to be joined with MSFD8bHazardousSubstancesActivityDescription table
# first
# @register_form_section(A81bHazardousItemDisplay)
# class A81bHazardousActivities(ItemDisplay):
#     title = 'Activities producing hazardous substances'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bHazardousSubstancesActivity,
#                 'MSFD8b_HazardousSubstances',
#                 self.context.item.MSFD8b_HazardousSubstances_ID
#             )


@register_form_section(A81bHazardousItemDisplay)
class A81bHazardousImpacts(ItemDisplay):
    title = 'Impacts produced by the hazardous substances'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bHazardousSubstancesSumInfo2ImpactedElement,
                'MSFD8b_HazardousSubstances',
                self.context.item.MSFD8b_HazardousSubstances_ID
            )
# endregion Hazardous substances


# region Hydrological processes
class A81bHydroItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bHydrologicalProcess
    order_field = 'MSFD8b_HydrologicalProcesses_ID'


@register_subform(A81bForm)
class A81bHydroSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Hydrological processes'
    mapper_class = sql.MSFD8bHydrologicalProcess

    def get_subform(self):
        return A81bHydroItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bHydroItemDisplay)
class A81aHydroAssessment(ItemDisplay):
    title = 'Asessment of hydrological processes'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bHydrologicalProcessesAssesment,
                'MSFD8b_HydrologicalProcesses',
                self.context.item.MSFD8b_HydrologicalProcesses_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bHydrologicalProcessesAssesmentIndicator,
            'MSFD8b_HydrologicalProcesses_Assesment',
            self.item.MSFD8b_HydrologicalProcesses_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]

#  TODO
# MSFD8bHydrologicalProcessesActivity is not directly related to
# MSFD8b_HydrologicalProcesses table
# needs to be joined with MSFD8bHydrologicalProcessesActivityDescription table
# first
# @register_form_section(A81bHydroItemDisplay)
# class A81bHydroActivities(ItemDisplay):
#     title = 'Activities producing hydrological processes'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bHydrologicalProcessesActivity,
#                 'MSFD8b_HydrologicalProcesses',
#                 self.context.item.MSFD8b_HydrologicalProcesses_ID
#             )


@register_form_section(A81bHydroItemDisplay)
class A81bHydroImpacts(ItemDisplay):
    title = 'Impacts produced by the hydrological processes'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bHydrologicalProcessesSumInfo2ImpactedElement,
                'MSFD8b_HydrologicalProcesses',
                self.context.item.MSFD8b_HydrologicalProcesses_ID
            )
# endregion Hydrological processes


# region Marine litter
class A81bMarineLitterItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bLitter
    order_field = 'MSFD8b_Litter_ID'


@register_subform(A81bForm)
class A81bMarineLitterSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Marine litter'
    mapper_class = sql.MSFD8bLitter

    def get_subform(self):
        return A81bMarineLitterItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bMarineLitterItemDisplay)
class A81aMarineLitterAssessment(ItemDisplay):
    title = 'Asessment of marine litter'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bLitterAssesment,
                'MSFD8b_Litter',
                self.context.item.MSFD8b_Litter_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bLitterAssesmentIndicator,
            'MSFD8b_Litter_Assesment',
            self.item.MSFD8b_Litter_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]

#  TODO
# MSFD8bLitterActivity is not directly related to
# MSFD8b_Litter table
# needs to be joined with MSFD8bLitterActivityDescription table first
# @register_form_section(A81bHydroItemDisplay)
# class A81bMarineLitterActivities(ItemDisplay):
#     title = 'Activities producing marine litter'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bLitterActivity,
#                 'MSFD8b_Litter',
#                 self.context.item.MSFD8b_Litter_ID
#             )


@register_form_section(A81bMarineLitterItemDisplay)
class A81bMarineLitterImpacts(ItemDisplay):
    title = 'Impacts produced by the marine litter'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bLitterSumInfo2ImpactedElement,
                'MSFD8b_Litter',
                self.context.item.MSFD8b_Litter_ID
            )
# endregion Marine litter


# region Microbial pathogens
class A81bMicrobialItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bMicrobialPathogen
    order_field = 'MSFD8b_MicrobialPathogens_ID'


@register_subform(A81bForm)
class A81bMicrobialSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Microbial pathogens'
    mapper_class = sql.MSFD8bMicrobialPathogen

    def get_subform(self):
        return A81bMicrobialItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bMicrobialItemDisplay)
class A81aMicrobialAssessment(ItemDisplay):
    title = 'Asessment of microbial pathogens'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bMicrobialPathogensAssesment,
                'MSFD8b_MicrobialPathogens',
                self.context.item.MSFD8b_MicrobialPathogens_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bMicrobialPathogensAssesmentIndicator,
            'MSFD8b_MicrobialPathogens_Assesment',
            self.item.MSFD8b_MicrobialPathogens_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]


#  TODO
# MSFD8bMicrobialPathogensActivity is not directly related to
# MSFD8b_MicrobialPathogens table
# needs to be joined with MSFD8bMicrobialPathogensActivityDescription table first
# @register_form_section(A81bMicrobialItemDisplay)
# class A81bMicrobialActivities(ItemDisplay):
#     title = 'Activities producing microbial pathogens'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bMicrobialPathogensActivity,
#                 'MSFD8b_MicrobialPathogens',
#                 self.context.item.MSFD8b_MicrobialPathogens_ID
#             )


# TODO
# missing table MSFD8bMicrobialPathogenSumInfo2ImpactedElement ??
# @register_form_section(A81bMicrobialItemDisplay)
# class A81bMicrobialImpacts(ItemDisplay):
#     title = 'Impacts produced by the microbial pathogens'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bMicrobialPathogenSumInfo2ImpactedElement,
#                 'MSFD8b_MicrobialPathogens',
#                 self.context.item.MSFD8b_MicrobialPathogens_ID
#             )
# endregion Microbial pathogens


# region Non-indigenous species
class A81bNonIndigenousItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1b
    """
    mapper_class = sql.MSFD8bNI
    order_field = 'MSFD8b_NIS_ID'


@register_subform(A81bForm)
class A81bNonIndigenousSubForm(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 8.1b form
    """
    title = 'Non-indigenous species'
    mapper_class = sql.MSFD8bNI

    def get_subform(self):
        return A81bNonIndigenousItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


@register_form_section(A81bNonIndigenousItemDisplay)
class A81aNonIndigenousAssessment(ItemDisplay):
    title = 'Asessment of non-indigenous species'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bNISAssesment,
                'MSFD8b_NIS',
                self.context.item.MSFD8b_NIS_ID
            )

    def get_extra_data(self):
        if not self.item:
            return {}

        count, item = db.get_related_record(
            sql.MSFD8bNISAssesmentIndicator,
            'MSFD8b_NIS_Assesment',
            self.item.MSFD8b_NIS_Assesment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Assesment Indicator', {'Feature': item}),
        ]


#  TODO
# MSFD8bNISActivity is not directly related to
# MSFD8b_NIS table
# needs to be joined with MSFD8bNISActivityDescription table first
# @register_form_section(A81bNonIndigenousItemDisplay)
# class A81bNonIndigenousActivities(ItemDisplay):
#     title = 'Activities producing non-indigenous species'
#
#     def get_db_results(self):
#         if self.context.item:
#             return db.get_related_record(
#                 sql.MSFD8bNISActivity,
#                 'MSFD8b_NIS',
#                 self.context.item.MSFD8b_NIS_ID
#             )


@register_form_section(A81bNonIndigenousItemDisplay)
class A81bNonIndigenousImpacts(ItemDisplay):
    title = 'Impacts produced by non-indigenous species'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8bNISSumInfo2ImpactedElement,
                'MSFD8b_NIS',
                self.context.item.MSFD8b_NIS_ID
            )
# endregion Non-indigenous species