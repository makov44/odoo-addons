from SPARQLWrapper import SPARQLWrapper, JSON
import json
from datetime import datetime
import re
import logging
from rdflib import plugin, Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF
import hashlib
from SPARQLWrapper import SPARQLWrapper, JSON, BASIC

nsys = Namespace('http://rdf.siliconbeach.io/schema/sys/v1/')
dyl = Namespace('http://rdf.dyl.com/data/env/staging/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')
GRAPH_NAME = '<http://rdf.siliconbeach.io/store/audit_rdf>'

hc = hashlib.sha1()
_logger = logging.getLogger(__name__)


class RdfStore:
    def __init__(self):
        self.sparql = SPARQLWrapper("http://rdf.getdyl.com:8890/sparql")
        self.sparql.setHTTPAuth(BASIC)
        self.sparql.setCredentials('dba', 'dba')

    def execute(self, query):
        query_result = []
        try:
            self.sparql.setQuery(query)
            self.sparql.setReturnFormat(JSON)
            results = self.sparql.query().convert()

            for item in results["results"]["bindings"]:
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
                if 'callret-0' in item:
                    _logger.info("Result of execute operation: " + item['callret-0']['value'])
        except Exception as e:
            _logger.error(e)
            raise e

        return query_result

    def insert(self, graph):
        result = graph.serialize(format='nt').decode("utf-8")
        query = """               
                       INSERT INTO %s
                       {
                          %s
                       }            
                       """ % (GRAPH_NAME, result)
        self.execute(query)

    def delete(self, graph):
        result = graph.serialize(format='nt').decode("utf-8")
        result = result.replace('\"___object___\"', '?object')
        result = result.replace('\"___predicate___\"', '?predicate')
        query = """  WITH %s
                     DELETE { %s } 
                     WHERE  { %s }                               
                     """ % (GRAPH_NAME, result, result)
        self.execute(query)

    def get_uri(self, _id):
        query = """  PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                     SELECT ?uri FROM %s
                     WHERE 
                     {
                       ?uri ns1:system_instance.id %s . 
                     }            
                     """ % (GRAPH_NAME, _id)
        return self.execute(query)

    def build_workstation(self, person, workstation, graph):
        person_uri = URIRef(str(dyl["person"]) + "/" + + person.first_name + "/" + person.last_name)
        workstation_uri = URIRef(str(person_uri) + '/user/' + workstation.name)
        hc.update(str(workstation_uri).encode('utf-8'))
        _id = int(hc.hexdigest()[:8], 16)
        graph.add((workstation_uri, RDF.type, nsys['workstation']))
        graph.add((workstation_uri, nsys['workstation.name'], Literal(workstation.name)))
        graph.add((workstation_uri, nsys['workstation.key_name'], Literal(workstation.key_name)))
        graph.add((workstation_uri, nsys['workstation.key'], Literal(workstation.key)))
        graph.add((workstation_uri, nsys['workstation.key'], Literal(workstation.key)))
        graph.add((workstation_uri, nsys['system_instance.id'], Literal(_id)))
        return _id

        # def build_key(self, useruri, data, graph):
        #     hc.update(data['public_key'].encode('utf-8'))
        #     keyhash = hc.hexdigest()
        #     keyuri = dyl['ssh_key/public_key_' + keyhash]
        #     hc.update(str(keyuri).encode('utf-8'))
        #     graph.add((keyuri, RDF.type, nsys['ssh_key']))
        #     graph.add((keyuri, nsys['ssh_key.key_type'], Literal(data['type'])))
        #     graph.add((keyuri, nsys['ssh_key.public_sha1'], Literal(keyhash)))
        #     graph.add((keyuri, nsys['system_instance.id'], Literal(int(hc.hexdigest()[:8], 16))))
        #     authuri = URIRef(str(useruri) + '/authorized_key/' + keyhash)
        #     graph.add((authuri, RDF.type, nsys['authorized_key']))
        #     graph.add((authuri, nsys['authorized_key.user'], useruri))
        #     graph.add((authuri, nsys['authorized_key.ssh_key'], keyuri))
        #     try:
        #         graph.add((authuri, nsys['authorized_key.label'], Literal(data['label'])))
        #     except KeyError:
        #         pass
