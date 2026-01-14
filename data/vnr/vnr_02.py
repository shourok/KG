{
  "id": "vnr_02",
  "nodes": [
    {"id": "v1", "cpu": 12, "mem": 24, "role": "vr_app"},
    {"id": "v2", "cpu": 10, "mem": 20, "role": "media_cache"},
    {"id": "v3", "cpu": 8,  "mem": 16, "role": "security_gateway"}
  ],
  "links": [
    {"src": "v1", "dst": "v2", "bw": 30, "lat": 7},
    {"src": "v2", "dst": "v3", "bw": 25, "lat": 8}
  ],
  "constraints": {
    "region_preference": "edge",
    "privacy_level": "high",
    "latency_target_ms": 7
  }
}
