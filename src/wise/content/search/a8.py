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

#region Ecosystem(s)
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
#endregion Ecosystem


#region Functional Group(s)
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
            self.item.MSFD8a_Ecosystem_StatusAssessment_ID
        )
        # ft = pivot_data(res, 'FeatureType')

        return [
            ('Status Indicator', {'Feature': item}),
        ]
#endregion Functional Group


#region Habitat(s)
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

#endregion Habitat(s)