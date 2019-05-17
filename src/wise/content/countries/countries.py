import json
from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import defer

from Products.Five.browser import BrowserView
from wise.msfd import db, sql2018
from wise.msfd.base import BaseUtil
from wise.msfd.sql import t_MSFDCommon
from wise.msfd.sql_extra import MSCompetentAuthority
from wise.msfd.utils import db_objects_to_dict


def default(obj):
    if isinstance(obj, datetime):
        return {'_isoformat': obj.isoformat()}

    return super().default(obj)

class CountrySearch(BrowserView):
    """ A search listing for countries and associated information.
    """

    def _get_areas(self, mrus):
        for rec in mrus:
            area = {
                'Type': 'Area',
                'Title': rec.MarineReportingUnitId,
                'CountryCode': rec.CountryCode,
                'Country': self.countries[rec.CountryCode],
                'fields': {
                    'Area': rec.Area,
                },
            }
            yield(area)

    def _get_regions(self, mrus):
        for rec in mrus:
            region = {
                'MRUId': rec.MarineReportingUnitId,
                'CountryCode': rec.CountryCode,
                'Country': self.countries[rec.CountryCode],
                'Type': 'Region',
                'Title': rec.MarineReportingUnitId,
                'fields': {
                    'Region': rec.Region
                },
            }
            yield(region)

    def _get_mrus(self, mrus):
        for rec in mrus:
            mrus = {
                'CountryCode': rec.CountryCode,
                'Country': self.countries[rec.CountryCode],
                'Type': 'Marine Reporting Unit',
                'Title': rec.MarineReportingUnitId,
                'fields': {
                    'Description': rec.Description
                },
            }
            yield(mrus)

    @db.use_db_session('2018')
    def _get_countries(self):
        count, recs = db.get_all_records(sql2018.LCountry)

        return {r.Code: r.Country for r in recs}

    def results(self):

        results = []

        self.countries = self._get_countries()

        mrus = self._query_mru()

        results.extend(self._get_areas(mrus))
        results.extend(self._get_regions(mrus))
        results.extend(self._get_cas())
        results.extend(self._get_mrus(mrus))

        self.request.response.setHeader("Access-Control-Allow-Origin", "*")
        self.request.response.setHeader("Content-Type", "application/json")

        return json.dumps({'results': results}, default=default)

    @db.use_db_session('2012')
    def _get_cas(self):
        """ Get the Competent Authorities """

        util = BaseUtil()
        db.threadlocals.session_name = "2012"
        results = db.get_all_records(MSCompetentAuthority)[1]
        data = db_objects_to_dict(results)

        for row in data:
            rec = {
                'Type': 'Competent Authority',
                'CountryCode': row['C_CD'],
                'Country': row['Country'],
                'Title': row['MSCACode'],
                'fields': {},
            }

            blacklist = ['C_CD', 'Country', 'Import_Time', 'Import_FileName']

            for k, v in row.items():
                del row[k]

                if k not in blacklist:
                    row[util.name_as_title(k)] = v

            rec['fields'] = row

            yield rec

    @db.use_db_session('2018')
    def _query_mru(self):
        sess = db.session()

        return sess.query(sql2018.MarineReportingUnit).options(defer('SHAPE'))
