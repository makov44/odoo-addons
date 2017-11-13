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

    def update(self, _id, _object):
        result = self.get_uri(_id)
        if len(result) == 0:
            return
        uri = result[0]['uri']
        if uri is None:
            return
        for key, value in _object.items():
            if not isinstance(value, str):
                continue
            graph = Graph()
            graph.add((URIRef(uri), nsys[key], Literal("___object___")))
            self.delete(graph)

        graph = Graph()
        for key, value in _object.items():
            if not isinstance(value, str):
                continue
            graph.add((URIRef(uri), nsys[key], Literal(value)))
        self.insert(graph)

    def delete(self, graph):
        result = graph.serialize(format='nt').decode("utf-8")
        result = result.replace('\"___object___\"', '?object')
        result = result.replace('\"___predicate___\"', '?predicate')
        query = """  WITH %s
                     DELETE { %s } 
                     WHERE  { %s }                               
                     """ % (GRAPH_NAME, result, result)
        self.execute(query)

    def delete_class(self, ids):
        for _id in ids:
            graph = Graph()
            result = self.get_uri(_id)
            if len(result) == 0:
                continue
            uri = result[0]['uri']
            if uri is None:
                continue
            graph.add((URIRef(uri), Literal("___predicate___"), Literal("___object___")))
            self.delete(graph)

    def get_uri(self, _id):
        query = """  PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                     SELECT ?uri FROM %s
                     WHERE 
                     {
                       ?uri ns1:id %s . 
                     }            
                     """ % (GRAPH_NAME, _id)
        return self.execute(query)
