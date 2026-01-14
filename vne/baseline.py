# vne/baseline.py
"""
Baseline VNE (KG-based WITHOUT hidden-relation inference)

Meaning of "baseline" here:
- We still use Neo4j as the substrate "database" (nodes/links stored as graph).
- We DO NOT use any inferred/hidden edges such as :AFFINITY, :SAME_REGION,
  :LOW_LAT_PATH, semantic similarity edges, etc.
- Decisions are made only from explicit substrate attributes and explicit :LINK
  relationships (capacity/latency), i.e., "what is directly stored" in the KG.

Pipeline:
1) Candidate substrate node selection from explicit node attributes (cpu, mem, region)
2) Greedy node mapping (largest-demand-first)
3) Virtual link feasibility check using explicit substrate links only (direct LINK)
   (You can later extend this to multi-hop shortest path, but keep baseline simple.)
"""

from __future__ import annotations

from typing import Dict, Tuple, Optional, Any, List
from kg.neo4j_client import Neo4jClient
from vne.models import VNR


def _candidate_nodes_query() -> str:
    # Explicit attributes only: cpu, mem, region (no inferred edges)
    return """
    MATCH (n:Node)
    WHERE toFloat(n.cpu) >= toFloat($cpu)
      AND toFloat(n.mem) >= toFloat($mem)
      AND ($region IS NULL OR n.region = $region)
    RETURN n.id AS id, toFloat(n.cpu) AS cpu, toFloat(n.mem) AS mem
    ORDER BY cpu DESC, mem DESC
    LIMIT $k
    """


def _direct_link_query() -> str:
    # Explicit substrate link only: (a)-[:LINK]->(b) and optional reverse
    return """
    MATCH (a:Node {id:$src})-[l:LINK]->(b:Node {id:$dst})
    RETURN toFloat(l.bw) AS bw, toFloat(l.lat) AS lat
    UNION
    MATCH (a:Node {id:$src})<-[l:LINK]-(b:Node {id:$dst})
    RETURN toFloat(l.bw) AS bw, toFloat(l.lat) AS lat
    LIMIT 1
    """


def baseline_vne(
    client: Neo4jClient,
    vnr: VNR,
    k: int = 25,
    region: Optional[str] = None,
) -> Tuple[bool, Dict[str, str]]:
    """
    Args:
        client: Neo4j client connection
        vnr: VNR object with fields:
             - vnr.nodes: list of {"id", "cpu", "mem", ...}
             - vnr.links: list of {"src", "dst", "bw", "lat", ...}
             - vnr.constraints: dict (optional)
        k: shortlist size for candidate substrate nodes per virtual node
        region: optional region constraint override; if None, tries vnr.constraints

    Returns:
        accepted (bool), mapping (dict: virtual_node_id -> substrate_node_id)
    """
    mapping: Dict[str, str] = {}
    used_substrate: set[str] = set()

    region_pref = region if region is not None else vnr.constraints.get("region_preference")

    # 1) Node embedding (greedy; largest demand first)
    vnodes_sorted: List[Dict[str, Any]] = sorted(
        vnr.nodes,
        key=lambda n: (float(n.get("cpu", 0)), float(n.get("mem", 0))),
        reverse=True,
    )

    cand_q = _candidate_nodes_query()
    for vn in vnodes_sorted:
        cpu_req = float(vn.get("cpu", 0))
        mem_req = float(vn.get("mem", 0))

        candidates = client.run(
            cand_q,
            cpu=cpu_req,
            mem=mem_req,
            region=region_pref,
            k=int(k),
        )

        chosen = None
        for c in candidates:
            sid = c["id"]
            if sid not in used_substrate:
                chosen = sid
                break

        if chosen is None:
            return False, {}

        mapping[vn["id"]] = chosen
        used_substrate.add(chosen)

    # 2) Link embedding feasibility (direct-link check ONLY)
    link_q = _direct_link_query()
    for vl in vnr.links:
        src_v = vl["src"]
        dst_v = vl["dst"]

        # if node mapping failed (should not happen), reject
        if src_v not in mapping or dst_v not in mapping:
            return False, {}

        src_s = mapping[src_v]
        dst_s = mapping[dst_v]

        res = client.run(link_q, src=src_s, dst=dst_s)
        if not res:
            return False, {}

        bw_avail = float(res[0]["bw"])
        lat_avail = float(res[0]["lat"])

        bw_req = float(vl.get("bw", 0))
        lat_req = float(vl.get("lat", float("inf")))

        if bw_avail < bw_req or lat_avail > lat_req:
            return False, {}

    return True, mapping
