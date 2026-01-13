from vne.models import VNR
def kg_vne(client, vnr: VNR):
    mapping = {}
    for vn in vnr.nodes:
        res = client.run("""
        MATCH (n:Node)
        WHERE n.cpu >= $cpu AND n.mem >= $mem
        RETURN n.id LIMIT 1
        """, cpu=vn["cpu"], mem=vn["mem"])
        if not res:
            return False, {}
        mapping[vn["id"]] = res[0]["n.id"]
    return True, mapping
