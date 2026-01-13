import json, os
from kg.neo4j_client import Neo4jClient
from kg.ingest import load_nodes, load_links
from kg.hidden_inference import infer_hidden_relations
from vne.kg_enhanced import kg_vne
from vne.models import VNR
client = Neo4jClient(
    os.environ["NEO4J_URI"],
    os.environ["NEO4J_USER"],
    os.environ["NEO4J_PASSWORD"]
)
load_nodes(client, "data/substrate/nodes.csv")
load_links(client, "data/substrate/links.csv")
infer_hidden_relations(client)
vnr = VNR(json.load(open("data/vnr/vnr_01.json")))
accepted, mapping = kg_vne(client, vnr)
print("Accepted:", accepted)
print("Mapping:", mapping)
