from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class VNR:
    id: str
    nodes: List[Dict[str, Any]]
    links: List[Dict[str, Any]]
    constraints: Dict[str, Any]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "VNR":
        return VNR(
            id=d["id"],
            nodes=d["nodes"],
            links=d["links"],
            constraints=d.get("constraints", {})
        )
