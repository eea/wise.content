""" Forms and views for Article 13-14 search
"""

from wise.content.search import db, interfaces, sql
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.field import Fields

from .base import EmbededForm, MainForm


class StartArticle1314Form(MainForm):
    """
    """
    fields = Fields(interfaces.IStartArticles1314)
    name = 'msfd-c3'

    def get_subform(self):
        return MarineUnitIDsForm(self, self.request)

    def get_available_marine_unit_ids(self):
        mc = sql.MSFD13ReportingInfo
        conditions = []

        report_type = self.context.data.get('report_type')

        if report_type:
            conditions.append(mc.ReportType == report_type)

        region = self.context.data.get('Region')

        if region:
            conditions.append(mc.Region == region)


class MarineUnitIDsForm(EmbededForm):
    """ Select the MarineUnitID based on MemberState, Region and Area
    """

    # TODO: properly show only available marine unit ids
    fields = Fields(interfaces.IMarineUnitIDsSelect)
    fields['marine_unit_ids'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):


        if self.data.get('MarineUnitID'):
            conditions.append(mc.MarineUnitID == self.data['MarineUnitID'])

        count, res = db.get_all_records(
            mc.ID,
            *conditions
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


class UniqueCodesForm(EmbededForm):
    """ Select the unique codes
    """

    fields = Fields(interfaces.IA1314UniqueCodes)

    fields['unique_codes'].widgetFactory = CheckBoxFieldWidget

    def get_subform(self):
        return None
        # return MarineUnitIDsForm(self, self.request)
