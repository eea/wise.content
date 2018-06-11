from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, sql

from .base import ItemDisplayForm, MarineUnitIDSelectForm
from .utils import data_to_xls, pivot_query, register_form


@register_form
class A10Form(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 10 form
    """

    title = 'Article 10 (Targets)'
    mapper_class = sql.MSFD10Target

    def get_subform(self):
        return A10ItemDisplay(self, self.request)

    def download_results(self):
        muids = self.get_marine_unit_ids()
        count, data = db.get_all_records(
            self.mapper_class, self.mapper_class.MarineUnitID.in_(muids)
        )

        xlsdata = [
            ('MSFD10Target', data),      # worksheet title, row data
        ]

        return data_to_xls(xlsdata)


class A10ItemDisplay(ItemDisplayForm):
    """ The implementation of the Article 10 fom
    """

    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    mapper_class = sql.MSFD10Target
    order_field = 'MSFD10_Target_ID'

    # TODO: the MSFD10_DESCrit is not ORM mapped yet
    # this query is not finished!!!!

    def get_extra_data(self):
        if not self.item:
            return {}

        target_id = self.item.MSFD10_Target_ID

        t = sql.t_MSFD10_FeaturesPressures
        c, res = db.get_table_records([
            t.c.FeatureType,
            t.c.PhysicalChemicalHabitatsFunctionalPressures,
        ], t.c.MSFD10_Target == target_id)
        ft = pivot_query(res, 'FeatureType')

        res = db.get_a10_criteria_indicators(target_id)

        t = sql.t_MSFD10_DESCrit
        c, res = db.get_table_records(
            [t.c.GESDescriptorsCriteriaIndicators],
            t.c.MSFD10_Target == target_id
        )
        fr = pivot_query(res, 'GESDescriptorsCriteriaIndicators')

        return [
            ('Feature Type', ft),
            ('Criteria Indicators', fr),
        ]
