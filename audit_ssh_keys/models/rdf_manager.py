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


class Query:

    hosts = """
            PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
            SELECT DISTINCT ?id  ?name 
            WHERE { 
            ?hostUri a ns1:system_instance;
                     ns1:system_instance.hostname ?name;
                     ns1:system_instance.id ?id . 
            }
            ORDER BY (?id)
            LIMIT %s
            OFFSET %s
            """

    host = """
               PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
               SELECT DISTINCT ?id  ?name  (concat('[' , group_concat(distinct ?userId; separator=','), ']') as ?users_ids_json)
               WHERE { 
                   ?hostUri a ns1:system_instance;
                        ns1:system_instance.id ?id;
                        ns1:system_instance.hostname ?name .                       
                   ?userUri a ns1:user;
                         ns1:user.system ?hostUri;
                         ns1:system_instance.id  ?userId .
                   FILTER(?id in %s)              
               }
               GROUP BY ?id ?name
                                            
               """

    user = """
              PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
              SELECT DISTINCT ?id  ?name  ?host_id (concat('[' , group_concat(distinct ?key_id; separator=','), ']') as ?keys_ids_json)
              WHERE { 
                  ?hostUri a ns1:system_instance;
                       ns1:system_instance.id ?host_id .  
                  ?userUri a ns1:user;
                       ns1:system_instance.id ?id;
                       ns1:user.system ?hostUri;
                       ns1:user.login  ?name .
                  ?keyUri a ns1:ssh_key;
                       ns1:system_instance.id ?key_id;
                       ns1:ssh_key.key_type ?keyType;
                       ns1:ssh_key.public_sha1 ?keyHash .
                  ?authUri a ns1:authorized_key;
                       ns1:authorized_key.user  ?userUri;
                       ns1:authorized_key.ssh_key ?keyUri;
                       ns1:authorized_key.label ?label  .                         
                  
                  FILTER(?id in %s)              
              }
              GROUP BY ?id  ?name  ?host_id

              """

    users = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                SELECT DISTINCT ?id  ?name  ?host_id
                WHERE {
                    ?hostUri a ns1:system_instance;
                            ns1:system_instance.id  ?host_id .
                    ?userUri a ns1:user;
                         ns1:user.login ?user;
                         ns1:user.system ?hostUri;
                         ns1:system_instance.id  ?id .
                 }
                 ORDER BY (?id)
                 LIMIT %s
                 OFFSET %s
                """

    key = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                SELECT DISTINCT ?id ?user_id ?name ?key_hash ?key_type
                WHERE { 
                    ?userUri a ns1:user;
                            ns1:system_instance.id  ?user_id .                       
                    ?keyUri a ns1:ssh_key;
                            ns1:ssh_key.key_type ?key_type;
                            ns1:ssh_key.public_sha1 ?key_hash; 
                            ns1:system_instance.id  ?id .
                    ?authUri a ns1:authorized_key;
                            ns1:authorized_key.user  ?userUri;
                            ns1:authorized_key.ssh_key ?keyUri;
                            ns1:authorized_key.label ?name  . 
                    FILTER(?id in %s)                        
                }
                ORDER BY (?id)               
                """

    keys = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                SELECT DISTINCT ?id ?user_id ?name ?key_hash ?key_type
                WHERE { 
                    ?userUri a ns1:user:
                            ns1:system_instance.id  ?user_id .                        
                    ?keyUri a ns1:ssh_key;
                            ns1:ssh_key.key_type ?key_type;
                            ns1:ssh_key.public_sha1 ?key_hash; 
                            ns1:system_instance.id  ?id .
                    ?authUri a ns1:authorized_key;
                            ns1:authorized_key.user  ?userUri;
                            ns1:authorized_key.ssh_key ?keyUri;
                            ns1:authorized_key.label ?name  .                      
                }
                ORDER BY (?id)
                LIMIT %s
                OFFSET %s
                """