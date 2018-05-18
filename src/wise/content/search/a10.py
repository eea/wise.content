from wise.content.search import sql

from .base import ItemDisplayForm, MarineUnitIDSelectForm
from .db import get_all_records
from .utils import data_to_xls, register_form


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
        count, data = get_all_records(
            self.mapper_class, self.mapper_class.MarineUnitID.in_(muids)
        )

        return data_to_xls(data)


class A10ItemDisplay(ItemDisplayForm):
    """ The implementation of the Article 10 fom
    """
    mapper_class = sql.MSFD10Target
    order_field = 'MSFD10_Target_ID'

#     # TODO: the MSFD10_DESCrit is not ORM mapped yet
#     # this query is not finished!!!!

    # def get_extra_data(self):
    #     if not self.item:
    #         return {}
    #
    #     target_id = self.item.MSFD10_Target_ID
    #
    #     res = db.get_a10_feature_targets(target_id)
    #     ft = pivot_data(res, 'FeatureType')
    #
    #     return [
    #         ('Feature Type', ft),
    #     ]
