class Host:
    get_hosts = """
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

    get_host_users = """
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


class User:
    get_user_keys = """
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

    get_users = """
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


class Key:
    get_key = """
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

    get_keys = """
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


class Person:
    get_persons = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                SELECT DISTINCT ?id  ?first_name ?last_name ?title 
                WHERE { 
                ?personUri a foaf:Person;
                         foaf:firstName ?first_name;
                         foaf:lastName ?last_name;
                         foaf:title ?title;
                         ns1:system_instance.id  ?id .                         
                          
                }
                ORDER BY (?id)
                LIMIT %s
                OFFSET %s
                """

    get_person_workstations = """
                   PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                   SELECT DISTINCT ?id  ?first_name ?last_name ?title  (concat('[' , group_concat(distinct ?workstation_id; separator=','), ']') as ?workstation_ids_json)
                   WHERE { 
                      ?personUri a foaf:Person;
                             foaf:firstName ?first_name;
                             foaf:lastName ?last_name;
                             foaf:title ?title;
                             ns1:system_instance.id ?id .                        
                      ?workstationUri a ns1:workstation;
                             ns1:workstation.person ?personUri;
                             ns1:system_instance.id  ?workstation_id .
                      FILTER(?id in %s)              
                   }
                   GROUP BY ?id ?first_name ?last_name ?title 

                   """
