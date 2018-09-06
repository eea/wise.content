from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, sql

from .base import ItemDisplay, ItemDisplayForm, MarineUnitIDSelectForm
from .sql_extra import MSFD4GeographicalAreaID, MSFD4GeograpicalAreaDescription
from .utils import (data_to_xls, db_objects_to_dict, pivot_data, register_form,
                    register_form_section, register_subform)
from six import string_types
from io import BytesIO
from plone.intelligenttext.transforms import convertWebIntelligentPlainTextToHtml
import datetime

LABELS = {}                        # vocabulary of labels

@register_form
class A4Form(MarineUnitIDSelectForm):
    """ Main form for A4.
    """

    record_title = title = \
        'Article 4 (Geographic areas & regional cooperation)'
    mapper_class = MSFD4GeographicalAreaID

    def get_subform(self):
        return A4ItemDisplay(self, self.request)


class A4ItemDisplay(ItemDisplayForm):
    """ The implementation of the Article 10 fom
    """

    mapper_class = MSFD4GeographicalAreaID
    order_field = 'MarineUnitID'

    extra_data_template = ViewPageTemplateFile('pt/extra-data-simple.pt')
    extra_data_pivot = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    def get_extra_data(self):
        if not self.item:
            return []

        blacklist = ['MSFD4_RegionalCooperation_ID',
                     'MSFD4_RegionalCooperation_Import',
                     'MSFD4_GeograpicalAreasDescription_Import',
                     ]

        import_id = self.item.MSFD4_GegraphicalAreasID_Import
        m = MSFD4GeograpicalAreaDescription
        [desc] = db.get_all_columns_from_mapper(
            m,
            'MSFD4_GeograpicalAreasDescription_Import',
            m.MSFD4_GeograpicalAreasDescription_Import == import_id
        )
        desc_html = self.data_template(item=desc, blacklist=blacklist)

        total, imported = db.get_item_by_conditions(
            sql.MSFD4Import,
            'MSFD4_Import_ID',
            sql.MSFD4Import.MSFD4_Import_ID == import_id
        )
        assert total == 1

        m = sql.MSFD4RegionalCooperation
        coops = db.get_all_columns_from_mapper(
            m,
            'MSFD4_RegionalCooperation_ID',
            m.MSFD4_Import == imported
        )

        rows = db_objects_to_dict(coops, excluded_columns=blacklist)
        
        for row in rows:
            for prop in row:
                row[prop] = convertWebIntelligentPlainTextToHtml(row[prop])

        regcoop = pivot_data(rows, 'RegionsSubRegions')
        pivot_html = self.extra_data_pivot(extra_data=[
            ('Regional Cooperation', regcoop),
        ])

        return [
            ('Area description', desc_html),
            ('', pivot_html)
        ]

    """Overwrite print_value of utils.py """
    def print_value(self, value):
        if not value:
            return value

        if isinstance(value, string_types):
            if value in LABELS:
                tmpl = '<span title="{}">{}</span>'
                try:
                    ret = tmpl.format(value, LABELS[value])
                except UnicodeEncodeError as e:
                    ret = tmpl.format(value, LABELS[value].encode('utf-8'))
                except Exception as e:
                    ret = tmpl.format(value, unicode(LABELS[value]))

                return ret

            return value

        base_values = string_types + (int, datetime.datetime, list)

        if not isinstance(value, base_values):
            # TODO: right now we're not showing complex, table-like values
            # Activate below to show tables
            # return self.value_template(item=value)

            return None
            # return '&lt;hidden&gt;'

        return value