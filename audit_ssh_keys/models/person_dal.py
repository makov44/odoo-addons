import logging
from rdflib import plugin, Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF
import hashlib
from . import rdf_manager
from . import query

rdf_store = rdf_manager.RdfStore()
nsys = Namespace('http://rdf.siliconbeach.io/schema/sys/v1/')
dyl = Namespace('http://rdf.dyl.com/data/env/staging/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')

hc = hashlib.sha1()
_logger = logging.getLogger(__name__)
_query = query.Person


class PersonDal:
    def select_all(self, offset, limit):
        return rdf_store.execute(_query.get_persons % (limit, offset))

    def select_by_ids(self, ids):
        str_ids = '(' + ''.join([str(item) + ',' for item in ids]) + ')'
        return rdf_store.execute(_query.get_persons_by_ids % (str.rstrip(str_ids, ',)') + ')'))

    def insert(self, person):
        graph = Graph()
        person_uri = URIRef(str(dyl["person"]) + "/" + person.first_name + "/" + person.last_name)
        hc.update(str(person_uri).encode('utf-8'))
        _id = int(hc.hexdigest()[:8], 16)
        graph.add((person_uri, RDF.type, nsys['person']))
        graph.add((person_uri, nsys['first_name'], Literal(person.first_name)))
        graph.add((person_uri, nsys['last_name'], Literal(person.last_name)))
        graph.add((person_uri, nsys['id'], Literal(_id)))
        if person.title:
            graph.add((person_uri, nsys['title'], Literal(person.title)))
        rdf_store.insert(graph)
        return _id

    def update(self, _id, _object):
        rdf_store.update(_id, _object)

    def delete(self, ids):
        rdf_store.delete_class(ids)
