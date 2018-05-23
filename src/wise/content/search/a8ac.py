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


# Article 8.1c
@register_form
class A81cForm(MarineUnitIDSelectForm):
    """ Main form for A81c.

    Class for Article 8.1c Economic and social analysis
    """
    title = '8.1c (Economic and social analysis)'
    mapper_class = sql.MSFD8cUs

    def get_subform(self):
        return A81cEconomicItemDisplay(self, self.request)


class A81cEconomicItemDisplay(MultiItemDisplayForm):
    """ Group the multiple items together for A8.1c
    """
    mapper_class = sql.MSFD8cUs
    order_field = 'MSFD8c_Uses_ID'

    # TODO: need to filter on topic


@register_form_section(A81cEconomicItemDisplay)
class A81cEconomicPressures(ItemDisplay):
    title = 'Pressures produces by the activities'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8cPressure,
                'MSFD8c_Uses_ID',
                self.context.item.MSFD8c_Uses_ID
            )


@register_form_section(A81cEconomicItemDisplay)
class A81aEconomicDependencies(ItemDisplay):
    title = 'Dependencies of activities on features'

    def get_db_results(self):
        if self.context.item:
            return db.get_related_record(
                sql.MSFD8cDepend,
                'MSFD8c_Uses_ID',
                self.context.item.MSFD8c_Uses_ID
            )
