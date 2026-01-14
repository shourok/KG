import os, json, time
import yaml
import pandas as pd

from kg.neo4j_client import Neo4jClient
from kg.ingest import create_constraints, load_nodes, load_links
from kg.hidden_inference import infer_hidden_relations

from vne.models import VNR
from vne.baseline import baseline_vne
from vne.kg_enhanced import kg_vne

def load_config(path="configs/experiment.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def main():
    cfg = load_config()

    client = Neo4jClient(
        os.environ["NEO4J_URI"],
        os.environ["NEO4J_USER"],
        os.environ["NEO4J_PASSWORD"],
        os.environ.get("NEO4J_DATABASE", "neo4j")
    )

    create_constraints(client)
    load_nodes(client, cfg["substrate"]["nodes_csv"])
    load_links(client, cfg["substrate"]["links_csv"])

    if cfg["kg"]["infer_hidden_relations"]:
        infer_hidden_relations(client)

    results = []
    vnr_folder = cfg["vnr"]["folder"]

    for vfile in cfg["vnr"]["files"]:
        vnr_path = os.path.join(vnr_folder, vfile)
        vnr = VNR.from_dict(json.load(open(vnr_path)))

        for algo in ["baseline", "kg_enhanced"]:
            t0 = time.time()
            if algo == "baseline":
                ok, mapping = baseline_vne(client, vnr)
            else:
                ok, mapping = kg_vne(client, vnr)
            dt = time.time() - t0

            results.append({
                "vnr_id": vnr.id,
                "algo": algo,
                "accepted": int(ok),
                "runtime_sec": dt,
                "mapping": json.dumps(mapping)
            })

    out_csv = cfg["outputs"]["results_csv"]
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    pd.DataFrame(results).to_csv(out_csv, index=False)
    print(f"[OK] Saved results to {out_csv}")

    client.close()

if __name__ == "__main__":
    main()
