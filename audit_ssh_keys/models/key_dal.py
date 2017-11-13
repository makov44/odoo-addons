import logging
from rdflib import Graph, Literal, URIRef, Namespace, XSD
from rdflib.namespace import RDF
import hashlib
from . import rdf_manager
from . import query
from .import helper

rdf_store = rdf_manager.RdfStore()
nsys = Namespace('http://rdf.siliconbeach.io/schema/sys/v1/')
dyl = Namespace('http://rdf.dyl.com/data/env/staging/')
foaf = Namespace('http://xmlns.com/foaf/0.1/')

_logger = logging.getLogger(__name__)
_query = query.Key()
_user_query = query.User()


class KeyDal:
    def select_all(self, active_id, offset, limit):
        return rdf_store.execute(_query.get_keys % (active_id, limit, offset))

    def select_by_ids(self, ids):
        str_ids = '(' + ''.join([str(item) + ',' for item in ids]) + ')'
        return rdf_store.execute(_query.get_keys_by_ids % (str.rstrip(str_ids, ',)') + ')'))

    def insert(self, data):
        users = rdf_store.execute(_user_query.get_users_by_ids % ('(' + str(data['active_id']) + ')'))
        user_name = any(users) and users[0] and users[0]['name']
        graph = Graph()
        uri = URIRef(str(dyl["key"]) + "/" + user_name + "/" + data['name'])
        _id = helper.generate_id(uri)
        graph.add((uri, RDF.type, nsys['key']))
        graph.add((uri, nsys['id'], Literal(_id, datatype=XSD.unsignedLong)))
        for key in data:
            if data[key]:
                graph.add((uri, nsys[key], Literal(data[key])))
        rdf_store.insert(graph)
        return _id

    def update(self, _id, _object):
        rdf_store.update(_id, _object)

    def delete(self, ids):
        rdf_store.delete_class(ids)
