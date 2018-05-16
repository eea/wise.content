from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, sql

from .base import ItemDisplayForm, MarineUnitIDSelectForm
from .utils import pivot_data, register_form


@register_form
class A9Form(MarineUnitIDSelectForm):
    """ Select the MarineUnitID for the Article 9 form
    """

    title = 'Article 9 (GES determination)'
    mapper_class = sql.MSFD9Descriptor

    def get_subform(self):
        return A9ItemDisplay(self, self.request)

    def download_results(self):
        # make results available for download
        # TODO: to be implemented
        pass


class A9ItemDisplay(ItemDisplayForm):
    """ The implementation for the Article 9 (GES determination) form
    """
    extra_data_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    mapper_class = sql.MSFD9Descriptor
    order_field = 'MSFD9_Descriptor_ID'

    def get_extra_data(self):
        if not self.item:
            return {}

        desc_id = self.item.MSFD9_Descriptor_ID

        res = db.get_a9_feature_impacts(desc_id)
        res = pivot_data(res, 'FeatureType')

        return [
            ('Feature Types', res)
        ]
