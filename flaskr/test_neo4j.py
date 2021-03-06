from __future__ import print_function

# Uncomment to run this module directly. TODO LMTW comment out.
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# End of uncomment.

import unittest
from neo4j.v1 import GraphDatabase, basic_auth, CypherError

class Neo4jTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

        
    def test_neo4j(self):
        
        local = False
        password = "lucy" if local else "neo4j"
        
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", password))
        session = driver.session()

        # Password handling taken from https://github.com/robinedwards/django-neomodel
        try:
            result = session.run("MATCH (a:Person) WHERE a.name = {name} "
                                "RETURN a.name AS name, a.title AS title",
                                {"name": "Crick"})
        except CypherError as ce:
            if 'The credentials you provided were valid, but must be changed before you can use this instance' in str(ce):
                new_password = 'test'
                session.run("CALL dbms.changePassword({password})", {'password': new_password})
                print("New database with no password set, setting password to 'test'")
            else:
                raise ce

        # run the test
        session.run("CREATE (a:Person {name: {name}, title: {title}})",
                    {"name": "Crick", "title": "Professor"})
        result = session.run("MATCH (a:Person) WHERE a.name = {name} "
                            "RETURN a.name AS name, a.title AS title",
                            {"name": "Crick"})
        for record in result:
            print("%s %s" % (record["title"], record["name"]))
        assert record["title"] == "Professor"
        assert record["name"] == "Crick"

        # clean up
        session.run("MATCH (a:Person) WHERE a.name = {name} "
                    "DETACH DELETE a",
                    {"name": "Crick"})
        session.close()

if __name__ == '__main__':
    unittest.main()