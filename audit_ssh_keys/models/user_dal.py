import logging
from rdflib import Graph, Literal, URIRef, Namespace
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
_query = query.User()


class UserDal:
    def select_all(self, active_id, offset, limit):
        return rdf_store.execute(_query.get_users % (active_id, limit, offset))

    def select_by_ids(self, ids):
        str_ids = '(' + ''.join([str(item) + ',' for item in ids]) + ')'
        return rdf_store.execute(_query.get_users_by_ids % (str.rstrip(str_ids, ',)') + ')'))

    def insert(self, data):
        graph = Graph()
        uri = URIRef(str(dyl["user"]) + "/" + data['name'])
        hc.update(str(uri).encode('utf-8'))
        _id = int(hc.hexdigest()[:8], 16)
        graph.add((uri, RDF.type, nsys['user']))
        graph.add((uri, nsys['id'], Literal(_id)))
        for key in data:
            if data[key]:
                graph.add((uri, nsys[key], Literal(data[key])))
        rdf_store.insert(graph)
        return _id

    def update(self, _id, _object):
        rdf_store.update(_id, _object)

    def delete(self, ids):
        rdf_store.delete_class(ids)
