def build_connectivity_intent(app_id: str, ingress: str, egress: str, priority: int = 100):
    # Minimal ONOS intent payload (illustrative)
    return {
        "type": "PointToPointIntent",
        "appId": app_id,
        "priority": priority,
        "ingressPoint": ingress,
        "egressPoint": egress
    }
