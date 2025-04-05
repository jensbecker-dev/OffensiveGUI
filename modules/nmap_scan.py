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
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

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
        raise RuntimeError(f"Error during Nmap service scan: {e}")


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
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

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

def nmap_tcp_scan(target):
    """
    Perform an Nmap TCP scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing TCP scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform a TCP scan (-sS)
        scanner.scan(hosts=target, arguments='-sS')

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
        raise RuntimeError(f"Error during Nmap TCP scan: {e}")

def nmap_udp_scan(target):
    """
    Perform an Nmap UDP scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing UDP scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform a UDP scan (-sU)
        scanner.scan(hosts=target, arguments='-sU')

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
    
def nmap_xmas_scan(target):
    """
    Perform an Nmap Xmas scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing Xmas scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform a Xmas scan (-sX)
        scanner.scan(hosts=target, arguments='-sX')

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
        raise RuntimeError(f"Error during Nmap Xmas scan: {e}") 