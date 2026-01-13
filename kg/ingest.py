import csv
from kg.neo4j_client import Neo4jClient
def load_nodes(client, path):
    with open(path) as f:
        for r in csv.DictReader(f):
            client.run("""
            MERGE (n:Node {id:$id})
            SET n.cpu=$cpu, n.mem=$mem, n.region=$region
            """, **r)
def load_links(client, path):
    with open(path) as f:
        for r in csv.DictReader(f):
            client.run("""
            MATCH (a:Node {id:$src}), (b:Node {id:$dst})
            MERGE (a)-[:LINK {bw:$bw, lat:$lat}]->(b)
            """, **r)
