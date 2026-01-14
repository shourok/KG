from typing import Dict, Tuple
from kg.neo4j_client import Neo4jClient
from kg.queries import q_candidate_nodes, q_link_exists, q_affinity_bonus
from vne.models import VNR

def kg_vne(client: Neo4jClient, vnr: VNR, k: int = 30) -> Tuple[bool, Dict[str, str]]:
    mapping: Dict[str, str] = {}
    used = set()
    region = vnr.constraints.get("region_preference")

    # Node mapping: prefer affinity with already chosen nodes (hidden relation bonus)
    for vn in vnr.nodes:
        cand = client.run(q_candidate_nodes(), cpu=vn["cpu"], mem=vn["mem"], region=region, k=k)

        best = None
        best_score = -1e9
        for c in cand:
            nid = c["id"]
            if nid in used:
                continue

            # base score: resources
            score = float(c["cpu"]) + 0.2 * float(c["mem"])

            # hidden-inference bonus: affinity with previously selected nodes
            for chosen in used:
                a = client.run(q_affinity_bonus(), a=nid, b=chosen)
                if a and a[0]["c"] > 0:
                    score += 10.0

            if score > best_score:
                best_score = score
                best = nid

        if not best:
            return False, {}
        mapping[vn["id"]] = best
        used.add(best)

    # Link feasibility check (direct link only)
    for vl in vnr.links:
        s = mapping[vl["src"]]
        d = mapping[vl["dst"]]
        res = client.run(q_link_exists(), src=s, dst=d)
        if not res:
            return False, {}
        bw, lat = res[0]["bw"], res[0]["lat"]
        if bw < vl["bw"] or lat > vl["lat"]:
            return False, {}

    return True, mapping
