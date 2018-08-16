""" Forms and views for Article 13-14 search
"""

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, ItemDisplayForm, MainForm
from .db import get_all_records
from .utils import all_values_from_field, data_to_xls, default_value_from_field


class StartArticle1314Form(MainForm):
    """
    """
    fields = Fields(interfaces.IStartArticles1314)
    name = 'msfd-c3'
    record_title = 'Articles 13 & 14'
    session_name = 'session'

    def get_subform(self):
        return MemberStatesForm(self, self.request)

    def default_report_type(self):
        return default_value_from_field(self, self.fields['report_type'])

    def default_region(self):
        return default_value_from_field(self, self.fields['region'])


class MemberStatesForm(EmbededForm):
    fields = Fields(interfaces.IMemberStates)

    def get_available_marine_unit_ids(self):
        mc = sql.MSFD13ReportingInfo
        conditions = []

        report_type = self.data.get('report_type')

        if report_type:
            conditions.append(mc.ReportType == report_type)

        region = self.data.get('region')

        if region:
            conditions.append(mc.Region == region)

        res = db.get_unique_from_mapper(mc, 'MarineUnitID', *conditions)

        return (len(res), res)

    def get_subform(self):
        return None

    def get_subform(self):
        return MarineUnitIDsForm(self, self.request)

    def default_member_states(self):
        return all_values_from_field(self, self.fields['member_states'])


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    # TODO: properly show only available marine unit ids
    fields = Fields(interfaces.IMarineUnitIDsSelect)
    fields['marine_unit_ids'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        mc = sql.MSFD13ReportingInfo

        count, res = db.get_all_records(
            mc.ID,
            mc.MarineUnitID.in_(self.data.get('marine_unit_ids', []))
        )
        self.data['report_ids'] = [x[0] for x in res]

        mc = sql.MSFD13Measure

        count, res = db.get_all_records(
            mc,
            mc.ReportID.in_(self.data['report_ids'])
        )
        res = set([(x.UniqueCode, x.Name) for x in set(res)])
        self.data['unique_codes'] = sorted(res)

        return UniqueCodesForm(self, self.request)

    def default_marine_unit_ids(self):
        return all_values_from_field(self.context,
                                     self.fields['marine_unit_ids'])


class UniqueCodesForm(EmbededForm):
    """ Select the unique codes
    """

    fields = Fields(interfaces.IA1314UniqueCodes)

    fields['unique_codes'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return A1314ItemDisplay(self, self.request)

    def default_unique_codes(self):
        return all_values_from_field(self.context,
                                     self.fields['unique_codes'])


class A1314ItemDisplay(ItemDisplayForm):
    """ The implementation for the Article 9 (GES determination) form
    """
    extra_data_template = ViewPageTemplateFile('pt/extra-data-item.pt')
    pivot_template = ViewPageTemplateFile('pt/extra-data-pivot.pt')

    css_class = "left-side-form"

    mapper_class = sql.MSFD13MeasuresInfo
    order_field = 'ID'

    def download_results(self):
        muids = self.context.data.get('unique_codes', [])
        count, data = get_all_records(
            self.mapper_class,
            self.mapper_class.UniqueCode.in_(muids)
        )

        report_ids = [row.ReportID for row in data]
        mc_report = sql.MSFD13ReportInfoFurtherInfo
        count, data_report = get_all_records(
            mc_report,
            mc_report.ReportID.in_(report_ids)
        )

        xlsdata = [
            ('MSFD11ReferenceSubProgramme', data),  # worksheet title, row data
            ('MSFD13ReportInfoFurtherInfo', data_report),
        ]

        return data_to_xls(xlsdata)

    def get_db_results(self):
        page = self.get_page()
        mc = self.mapper_class

        count, item, extra_data = db.get_collapsed_item(
            mc,
            self.order_field,
            [{'InfoType': ['InfoText']}],
            mc.UniqueCode.in_(self.context.data.get('unique_codes', [])),
            page=page,
        )
        # print(extra_data)
        self.extra_data = extra_data.items()

        return [count, item]

    def get_extra_data(self):
        if not self.item:
            return {}

        report_id = self.item.ReportID
        mc = sql.MSFD13ReportInfoFurtherInfo

        count, item = db.get_related_record(mc, 'ReportID', report_id)

        return ('Report info', item)

    def extras(self):
        html = self.pivot_template(extra_data=self.extra_data)

        return self.extra_data_template() + html
