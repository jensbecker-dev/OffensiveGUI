from scapy.all import sr1, IP, ICMP

def check_target_status(target):
    """
    Check if a target is online, offline, or unreachable using ICMP (ping).
    """
    try:
        response = sr1(IP(dst=target)/ICMP(), timeout=2, verbose=0)
        if response:
            return {"target": target, "status": "Online"}
        else:
            return {"target": target, "status": "Offline"}
    except Exception as e:
        return {"target": target, "status": f"Unreachable ({str(e)})"}

def run_target_monitor(targets):
    """
    Monitor the status of a list of targets and return the results.
    """
    results = []
    for target in targets:
        result = check_target_status(target)
        results.append(result)

    return results