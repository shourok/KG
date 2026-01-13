from typing import Dict, Any

class VNEBase:
    def embed(self, vnr: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns:
          {
            "status": "accepted" | "rejected",
            "mapping": { "vn_node_id": "substrate_server_id", ... },
            "reason": "..."
          }
        """
        raise NotImplementedError
