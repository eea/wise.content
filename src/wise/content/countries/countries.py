from Products.Five.browser import BrowserView
import json
import datetime

from wise.msfd import db
from wise.msfd.sql_extra import MSCompetentAuthority
from wise.msfd.sql import t_MSFDCommon
from wise.msfd.utils import db_objects_to_dict
from wise.msfd.base import BaseUtil

class Countries(BrowserView):

    def countries(self):
        self.request.response.setHeader("Access-Control-Allow-Origin", "*")
        self.request.response.setHeader("Content-Type", "application/json")

        db.threadlocals.session_name = "2012"

        data = db_objects_to_dict(db.get_all_records(MSCompetentAuthority)[1])
        commons = db.get_all_records(t_MSFDCommon)

        json_data = [];
        countries = [];
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
                    nice_ca['country'] = [item[3] for item in commons[1] if item[2] == elem[1]][0]
                    found = False
                    for country in countries:
                        if country['name'] == nice_ca['country']:
                            found = True
                            country['count'] += 1
                    if not found:
                        country = {'name': nice_ca['country'], 'checked': False, 'count': 1, 'code': elem[1]};
                        countries.append(country)
                nice_doc.append(nice_elem);
            nice_ca['fields'] = nice_doc;
            json_data.append(nice_ca);
        result = {}
        result['countries'] = sorted(countries, key=lambda x: x['name'])
        result['competentauthorities'] = json_data
        return json.dumps(result)

