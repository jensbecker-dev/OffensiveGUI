import nmap

def nmap_os_scan():
    """
    Perform an Nmap OS scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        dict: A dictionary containing the OS scan results.
    """
    scanner = nmap.PortScanner()
    hosts = input("Enter the target IP address or hostname: ")
    
    try:
        # Perform an OS detection scan (-O)
        scanner.scan(hosts=hosts, arguments='-O -sX')

        os_info = {}
        for host in scanner.all_hosts():
            os_info[host] = {
                'os': scanner[host].get('osmatch', [{}])[0].get('name'),
                'accuracy': scanner[host].get('osmatch', [{}])[0].get('accuracy')
            }
        return os_info
    except:
        # If no OS match found, set default values
        for host in scanner.all_hosts():
            os_info[host] = {
                'os': 'unknown',
                'accuracy': 'unknown'
            }
        return os_info
    
def nmap_udp_scan():
    """
    Perform an Nmap UDP scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing UDP scan results.
    """
    scanner = nmap.PortScanner()
    hosts = input("Enter the target IP address or hostname: ")
    
    try:

        # Perform a UDP scan (-sU)
        scanner.scan(hosts=hosts, arguments='-sU')

        results = []
        for host in scanner.all_hosts():
            for protocol in scanner[host].all_protocols():
                ports = scanner[host][protocol].keys()
                for port in ports:
                    port_info = scanner[host][protocol][port]
                    results.append({
                        'host': host,
                        'port': port,
                        'protocol': protocol,
                        'state': port_info.get('state', 'unknown'),
                        'service': port_info.get('name', 'unknown'),
                        'version': port_info.get('version', 'N/A')
                    })
        return results
    except Exception as e:
        raise RuntimeError(f"Error during Nmap UDP scan: {e}")
    
if __name__ == "__main__":
    nmap_udp_scan()