from SPARQLWrapper import SPARQLWrapper, JSON
import json
from datetime import datetime
import re


class RdfStore:

    def __init__(self):
        self.sparql = SPARQLWrapper("http://rdf.getdyl.com:8890/sparql")

    def execute(self, query):
        query_result = []
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        for item in  results["results"]["bindings"]:
            dict_result = {'create_uid': (1, 'Administrator'),
                           'create_date': str(datetime.now()),
                           'write_uid': (1, 'Administrator'),
                           'write_date': str(datetime.now())}
            for key in item:
                if key == 'name':
                    dict_result["display_name"] = item[key]["value"]

                if key == 'id':
                    dict_result[key] = int(item[key]["value"])
                elif '_json' in key:
                    new_key = re.sub('_json$', '', key)
                    dict_result[new_key] = json.loads(item[key]["value"])
                else:
                    dict_result[key] = item[key]["value"]



            query_result.append(dict_result)

        return query_result


