import json, random, os

def gen_vnr(idx: int) -> dict:
    nodes = random.randint(2, 8)
    links = max(1, nodes - 1)

    vnr = {
        "vnr_id": f"VNR_{idx:03d}",
        "service_type": random.choice(["VR_ROOM", "IOT_SLICE", "VIDEO_ANALYTICS"]),
        "region_preference": random.choice(["edge-zone", "core-zone"]),
        "qos": {
            "latency_ms": random.choice([5, 10, 20]),
            "bandwidth_mbps": random.choice([50, 100, 500, 1000, 2000])
        },
        "security": {
            "isolation": random.choice([True, False]),
            "encryption": random.choice(["none", "tls13"])
        },
        "vn_nodes": [],
        "vn_links": []
    }

    for i in range(nodes):
        vnr["vn_nodes"].append({
            "id": f"v{i+1}",
            "cpu": random.choice([1, 2, 4, 8]),
            "mem_gb": random.choice([2, 4, 8, 16])
        })

    # simple chain
    for i in range(links):
        vnr["vn_links"].append({
            "src": f"v{i+1}",
            "dst": f"v{i+2}",
            "bandwidth_mbps": vnr["qos"]["bandwidth_mbps"],
            "latency_ms": vnr["qos"]["latency_ms"]
        })

    return vnr

if __name__ == "__main__":
    out_dir = os.path.dirname(__file__)
    for i in range(1, 21):
        vnr = gen_vnr(i)
        with open(os.path.join(out_dir, f"vnr_{i:02d}.json"), "w", encoding="utf-8") as f:
            json.dump(vnr, f, indent=2)
    print("Generated 20 VNRs.")
