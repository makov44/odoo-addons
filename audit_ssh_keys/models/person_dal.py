import logging
from rdflib import plugin, Graph, Literal, URIRef, Namespace
from rdflib.namespace import RDF
import hashlib
from . import rdf_manager

rdf_store = rdf_manager.RdfStore()
nsys = Namespace('http://rdf.siliconbeach.io/schema/sys/v1/')
dyl = Namespace('http://rdf.dyl.com/data/env/staging/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')

hc = hashlib.sha1()
_logger = logging.getLogger(__name__)


class PersonDal:
    def insert(self, person):
        graph = Graph()
        person_uri = URIRef(str(dyl["person"]) + "/" + person.first_name + "/" + person.last_name)
        hc.update(str(person_uri).encode('utf-8'))
        _id = int(hc.hexdigest()[:8], 16)
        graph.add((person_uri, RDF.type, foaf['Person']))
        graph.add((person_uri, foaf['first_name'], Literal(person.first_name)))
        graph.add((person_uri, foaf['last_name'], Literal(person.last_name)))
        graph.add((person_uri, nsys['system_instance.id'], Literal(_id)))
        if person.title:
            graph.add((person_uri, foaf['title'], Literal(person.title)))
            rdf_store.insert(graph)
        return _id

    def update(self, _id, person):
        rdf_store.update(_id, person)

    def delete(self, _id):
        rdf_store.delete_class(_id)
