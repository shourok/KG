def infer_hidden_relations(client):
    client.run("""
    MATCH (a:Node),(b:Node)
    WHERE a.region=b.region AND a.id<>b.id
    MERGE (a)-[:AFFINITY]->(b)
    """)
