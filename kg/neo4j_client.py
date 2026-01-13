from neo4j import GraphDatabase
class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    def run(self, query, **params):
        with self.driver.session() as session:
            return list(session.run(query, params))
    def close(self):
        self.driver.close()
