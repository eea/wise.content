from Products.Five.browser import BrowserView
import json
import datetime

from wise.msfd import db
from wise.msfd.sql_extra import MSCompetentAuthority
from wise.msfd.sql import t_MSFDCommon
from wise.msfd.sql2018 import MarineReportingUnit
from wise.msfd.utils import db_objects_to_dict
from wise.msfd.base import BaseUtil


class Countries(BrowserView):
    @db.use_db_session('2012')
    def get_2012_data(self):
        db.threadlocals.session_name = "2012"
        data = db_objects_to_dict(
            db.get_all_records(MSCompetentAuthority)[1])
        commons = db.get_all_records(t_MSFDCommon)

        json_data = []
        countries = []
        bu = BaseUtil()
        for doc in data:
            nice_ca = {}
            nice_doc = []
            for elem in doc.items():
                nice_elem = {}
                nice_elem['key'] = elem[0]
                nice_elem['name'] = bu.name_as_title(elem[0])
                if isinstance(elem[1], datetime.datetime):
                    nice_elem['value'] = str(elem[1])
                else:
                    nice_elem['value'] = elem[1]

                if elem[0] == 'C_CD':
                    nice_ca['country'] = [item[3]
                                          for item in commons[1] if item[2] == elem[1]][0]
                    found = False
                    for country in countries:
                        if country['name'] == nice_ca['country']:
                            found = True
                            country['count'] += 1
                    if not found:
                        country = {
                            'name': nice_ca['country'], 'checked': False, 'count': 1, 'code': elem[1]}
                        countries.append(country)
                nice_doc.append(nice_elem)
            nice_ca['fields'] = nice_doc
            json_data.append(nice_ca)
        result = {}
        result['countries'] = sorted(countries, key=lambda x: x['name'])
        result['competentauthorities'] = json_data

        return result

    @db.use_db_session('2018')
    def get_2018_data(self):
        db.threadlocals.session_name = "2018"
        MRUs = db.get_all_records(MarineReportingUnit)[1]
        MRU_data = {}
        for MRU in MRUs:
            if not MRU_data.get(MRU.CountryCode):
                MRU_data[MRU.CountryCode] = []
            MRU_data[
                MRU.CountryCode].append({'Area': MRU.Area,
                                         'MRUId': MRU.MarineReportingUnitId,
                                         'Region': MRU.Region})
        return MRU_data

    def countries(self):
        results = []
        countries_vocab = {}
        rough_data = {}
        self.request.response.setHeader("Access-Control-Allow-Origin", "*")
        self.request.response.setHeader("Content-Type", "application/json")
        rough_data['y2012'] = self.get_2012_data().copy()
        rough_data['y2018'] = self.get_2018_data()

        for country in rough_data['y2012']['countries']:
            countries_vocab[country['code']] = country['name']

        for CA in rough_data['y2012']['competentauthorities']:
            CA_result = {
                'type': 'CompetentAuthority',
                'country': CA['country'],
                'keyvalues': CA['fields']}
            results.append(CA_result)

        for CountryCode in rough_data['y2018'].keys():
            if CountryCode in countries_vocab.keys():
                results_2018 = [{
                    'type': 'Area', 'country': countries_vocab[CountryCode],
                    'keyvalues': [].append(
                        rough_data['y2018'][CountryCode][i]['Area']
                        for i in rough_data['y2018'][CountryCode])
                }, {
                    'type': 'MRUId', 'country': countries_vocab[CountryCode],
                    'keyvalues': [].append(
                        rough_data['y2018'][CountryCode][i]['MRUId']
                        for i in rough_data['y2018'][CountryCode])
                }, {
                    'type': 'Region', 'country': countries_vocab[CountryCode],
                    'keyvalues': [].append(
                        rough_data['y2018'][CountryCode][i]['Region']
                        for i in rough_data['y2018'][CountryCode])
                }]
            results.extend(results_2018)

        results_JSON = {'results': results}
        return json.dumps(results_JSON)
