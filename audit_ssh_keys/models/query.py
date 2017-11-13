class Host:
    get_hosts = """
            PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
            SELECT ?id  ?name ?environment
            WHERE { 
            ?uri a ns1:host;
                     ns1:name ?name;
                     ns1:id ?id . 
             OPTIONAL {?uri ns1:environment ?environment .}
            }
            ORDER BY (?id)
            LIMIT %s
            OFFSET %s
            """

    get_hosts_by_ids = """
               PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
               SELECT ?id  ?name ?environment
               WHERE { 
                ?uri a ns1:host;
                         ns1:name ?name;
                         ns1:id ?id . 
                 OPTIONAL {?uri ns1:environment ?environment}
                 FILTER(?id in %s)  
                }
               """


class User:
    get_users = """
              PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
              SELECT ?id  ?name  ?description
              WHERE { 
                  ?uri a ns1:user;              
                       ns1:id ?id;                    
                       ns1:name ?name;
                       ns1:active_id %s .
                  OPTIONAL {?uri ns1:description ?description . }
              }
              ORDER BY (?id)
              LIMIT %s
              OFFSET %s
              """

    get_users_by_ids = """
              PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
              SELECT ?id  ?name  ?description
              WHERE { 
                  ?uri a ns1:user;              
                       ns1:id ?id;                    
                       ns1:name ?name .                      
                  OPTIONAL {?uri ns1:description ?description . }
                  FILTER(?id in %s)                               
              }
              """


class Key:
    get_keys = """
                  PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                  SELECT ?id  ?name  ?key_type ?key_hash ?description
                  WHERE { 
                      ?uri a ns1:key;              
                           ns1:id ?id;                    
                           ns1:name ?name;
                           ns1:key_type ?key_type;
                           ns1:key_hash ?key_hash;
                           ns1:active_id %s .
                      OPTIONAL {?uri ns1:description ?description . }
                  }
                  ORDER BY (?id)
                  LIMIT %s
                  OFFSET %s
                  """

    get_keys_by_ids = """
                  PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                  SELECT ?id  ?name  ?description
                  WHERE { 
                       ?uri a ns1:key;              
                           ns1:id ?id;                    
                           ns1:name ?name;
                           ns1:key_type ?key_type;
                           ns1:key_hash ?key_hash.                                               
                      OPTIONAL {?uri ns1:description ?description . }
                      FILTER(?id in %s)                               
                  }
                  """


class Person:
    get_persons = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>             
                SELECT ?id  ?first_name ?last_name ?title 
                WHERE { 
                      ?uri a ns1:person;
                             ns1:first_name ?first_name;
                             ns1:last_name ?last_name;                            
                             ns1:id ?id .                        
                      
                      OPTIONAL {?uri ns1:title ?title . }  
                }
                ORDER BY (?id)
                LIMIT %s
                OFFSET %s
                """

    get_persons_by_ids = """
                   PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>                 
                   SELECT ?id  (concat(?first_name , ' ',  ?last_name) as ?name) ?first_name ?last_name ?title 
                   WHERE { 
                      ?uri a ns1:person;
                             ns1:first_name ?first_name;
                             ns1:last_name ?last_name;                            
                             ns1:id ?id .                        
                      
                      OPTIONAL {?uri ns1:title ?title . }                    
                      FILTER(?id in %s)              
                   }
                   """


class Workstation:
    get_workstations = """
                PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>              
                SELECT ?id  ?name ?key_name ?key
                WHERE { 
                    ?uri a ns1:workstation;
                             ns1:name  ?name;
                             ns1:key_name ?key_name;
                             ns1:key ?key;
                             ns1:active_id %s;                   
                             ns1:id  ?id . 
                }
                ORDER BY (?id)
                LIMIT %s
                OFFSET %s
                """

    get_workstations_by_ids = """
                   PREFIX ns1: <http://rdf.siliconbeach.io/schema/sys/v1/>
                   SELECT ?id  ?name ?key_name ?key
                   WHERE { 
                        ?uri a ns1:workstation;
                             ns1:name  ?name;
                             ns1:key_name ?key_name;
                             ns1:key ?key;                    
                             ns1:id  ?id .  
                      FILTER(?id in %s)              
                   }
                   """
