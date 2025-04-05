"""
Module for performing nmap scans using the nmap library.
"""

import nmap  # Ensure the python-nmap library is installed


def nmap_service_scan(target):
    """
    Perform an Nmap service scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Perform a service version scan (-sV)
        scanner.scan(hosts=target, arguments='-sV')

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
        raise RuntimeError(f"Error during Nmap scan: {e}")


def nmap_os_scan(target):
    """
    Perform an Nmap OS scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing OS scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Perform an OS detection scan (-O)
        scanner.scan(hosts=target, arguments='-O')

        results = []
        for host in scanner.all_hosts():
            os_info = scanner[host].get('osmatch', [{}])[0]  # Get the first OS match
            results.append({
                'host': host,
                'os_name': os_info.get('name', 'Unknown'),
                'os_accuracy': os_info.get('accuracy', 'N/A'),
                'os_family': os_info.get('osclass', [{}])[0].get('osfamily', 'N/A') if os_info.get('osclass') else 'N/A'
            })
        return results
    except Exception as e:
        raise RuntimeError(f"Error during Nmap OS scan: {e}")