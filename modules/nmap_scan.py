"""
Module for performing nmap scans using the nmap library.
"""

import nmap  # Ensure the python-nmap library is installed
from datetime import datetime

def stop_time(start_time):
    """
    Calculate the time taken for a scan.

    Args:
        start_time (str): The start time of the scan in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        str: The time taken for the scan in seconds.
    """
    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.now()
    return str((end - start).total_seconds())

def nmap_tcp_scan(target, scan_speed):
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
        
        scan_args = f"-sS -T{scan_speed}" if scan_speed else "-sS"
        scanner.scan(hosts=target, arguments=scan_args)

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

def nmap_udp_scan(target, scan_speed):
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
        scan_args = f"-sU -T{scan_speed}" if scan_speed else "-sU"
        scanner.scan(hosts=target, arguments=scan_args)

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
    
def nmap_xmas_scan(target, scan_speed):
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
        scan_args = f"-sX -T{scan_speed}" if scan_speed else "-sX"
        scanner.scan(hosts=target, arguments=scan_args)

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

def nmap_service_scan(target, scan_speed):
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
        scan_args = f"-sV -T{scan_speed}" if scan_speed else "-sV"
        scanner.scan(hosts=target, arguments=scan_args)

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

def nmap_os_scan(target, scan_speed):
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
        scan_args = f"-O -T{scan_speed}" if scan_speed else "-O"

        scanner.scan(hosts=target, arguments=scan_args)

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