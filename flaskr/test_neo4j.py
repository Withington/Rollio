# Uncomment to run this module directly. TODO LMTW comment out.
#import sys, os
#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# End of uncomment.

import unittest

from neo4j.v1 import GraphDatabase, basic_auth

# TODO LMTW set password
# encrypted set to false due to Travis SSL bug Jul17 - https://github.com/neo4j/neo4j/issues/9233#issuecomment-300943889
#driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "lucy"), encrypted=False)
driver = GraphDatabase.driver("bolt://localhost:7474", auth=basic_auth("neo4j", "neo4j"), encrypted=False)

class Neo4jTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_data(self):

        session = driver.session()
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