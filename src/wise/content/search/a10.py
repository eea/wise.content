from wise.content.search import db, sql

from .base import ItemDisplayForm, MarineUnitIDSelectForm
from .utils import pivot_data, register_form


@register_form
class A10Form(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 10 form
    """

    title = 'Article 10 (Targets)'
    mapper_class = sql.MSFD10Target

    def get_subform(self):
        return A10ItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A10ItemDisplay(ItemDisplayForm):
    """ The implementation of the Article 10 fom
    """
    mapper_class = sql.MSFD10Target
    order_field = 'MSFD10_Target_ID'

#     # TODO: the MSFD10_DESCrit is not ORM mapped yet
#     # this query is not finished!!!!

    def get_extra_data(self):
        if not self.item:
            return {}

        target_id = self.item.MSFD10_Target_ID

        res = db.get_a10_feature_targets(target_id)
        ft = pivot_data(res, 'FeatureType')

        return [
            ('Feature Type', ft),
        ]
