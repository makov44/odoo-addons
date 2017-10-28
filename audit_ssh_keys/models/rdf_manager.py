from SPARQLWrapper import SPARQLWrapper, JSON
import hashlib
from datetime import datetime


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
                dict_result[key] = item[key]["value"]

            query_result.append(dict_result)

        return query_result


class Query:

    hosts = """
            PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
            SELECT DISTINCT ?id  ?uri  ?host 
            WHERE { 
            ?uri a ns1:system_instance;
                     ns1:system_instance.hostname ?host;
                     ns1:system_instance.id ?id . 
            }
            ORDER BY (?id)
            LIMIT %s
            OFFSET %s
            """

    host = """
               PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
               SELECT DISTINCT ?id ?uri  ?host 
               WHERE { 
               ?uri a ns1:system_instance;
                        ns1:system_instance.id %s .
               }
                                            
               """

    users = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                SELECT DISTINCT ?uri  ?user  ?hostUri
                WHERE {
                ?hostUri a ns1:system_instance .
                ?uri a ns1:user;
                     ns1:user.login ?user;
                     ns1:user.system ?hostUri .
                }
                """

    keys = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                SELECT DISTINCT ?uri ?label ?keyHash ?keyType  ?userUri
                WHERE { 
                ?userUri a ns1:user .                       
                ?uri a ns1:ssh_key;
                        ns1:ssh_key.key_type ?keyType;
                        ns1:ssh_key.public_sha1 ?keyHash .
                ?authUri a ns1:authorized_key;
                        ns1:authorized_key.user  ?userUri;
                        ns1:authorized_key.ssh_key ?uri;
                        ns1:authorized_key.label ?label  .                      
                }
                """