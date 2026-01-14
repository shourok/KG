def q_candidate_nodes():
    return """
    MATCH (n:Node)
    WHERE n.cpu >= $cpu AND n.mem >= $mem
    AND ($region IS NULL OR n.region = $region)
    RETURN n.id AS id, n.cpu AS cpu, n.mem AS mem, n.region AS region
    ORDER BY n.cpu DESC, n.mem DESC
    LIMIT $k
    """

def q_link_exists():
    return """
    MATCH (a:Node {id:$src})-[l:LINK]->(b:Node {id:$dst})
    RETURN l.bw AS bw, l.lat AS lat
    """

def q_affinity_bonus():
    return """
    MATCH (a:Node {id:$a})-[:AFFINITY]->(b:Node {id:$b})
    RETURN COUNT(*) AS c
    """
