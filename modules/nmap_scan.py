"""
Module for performing nmap scans using the nmap library.
"""

import nmap  # Ensure the python-nmap library is installed
from datetime import datetime

OS_ICONS = {
    "Windows": "fa-windows",  # FontAwesome Icon für Windows
    "Linux": "fa-linux",      # FontAwesome Icon für Linux
    "Mac OS": "fa-apple",     # FontAwesome Icon für MacOS
    "Unix": "fa-terminal",    # FontAwesome Icon für Unix
    "Unknown": "fa-question-circle"  # Standard-Icon für unbekannte Systeme
}

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
    
def nmap_fin_scan(target, scan_speed):
    """
    Perform an Nmap FIN scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing FIN scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform a FIN scan (-sF)
        scan_args = f"-sF -T{scan_speed}" if scan_speed else "-sF"
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
                        'reason': port_info.get('reason', 'N/A'),  # Include reason for state
                        'service': port_info.get('name', 'unknown'),
                        'version': port_info.get('version', 'N/A')
                    })
            # Add host-specific information if no ports are found
            if not results:
                results.append({
                    'host': host,
                    'state': scanner[host].get('status', {}).get('state', 'unknown'),
                    'reason': scanner[host].get('status', {}).get('reason', 'N/A')
                })
        return results
    except Exception as e:
        raise RuntimeError(f"Error during Nmap FIN scan: {e}")

def nmap_ack_scan(target, scan_speed):
    """
    Perform an Nmap ACK scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing ACK scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform an ACK scan (-sA)
        scan_args = f"-sA -T{scan_speed}" if scan_speed else "-sA"
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
                        'reason': port_info.get('reason', 'N/A'),  # Include reason for state
                        'service': port_info.get('name', 'unknown'),
                        'version': port_info.get('version', 'N/A')
                    })
            # Add host-specific information if no ports are found
            if not results:
                results.append({
                    'host': host,
                    'state': scanner[host].get('status', {}).get('state', 'unknown'),
                    'reason': scanner[host].get('status', {}).get('reason', 'N/A')
                })
        return results
    except Exception as e:
        raise RuntimeError(f"Error during Nmap ACK scan: {e}")

def nmap_null_scan(target, scan_speed):
    """
    Perform an Nmap Null scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing Null scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform a Null scan (-sN)
        scan_args = f"-sN -T{scan_speed}" if scan_speed else "-sN"
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
        raise RuntimeError(f"Error during Nmap Null scan: {e}")

def nmap_window_scan(target, scan_speed):
    """
    Perform an Nmap Window scan on the given target.

    Args:
        target (str): The target IP address or hostname.

    Returns:
        list: A list of dictionaries containing Window scan results.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform a Window scan (-sW)
        scan_args = f"-sW -T{scan_speed}" if scan_speed else "-sW"
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
                        'reason': port_info.get('reason', 'N/A'),  # Include reason for state
                        'service': port_info.get('name', 'unknown'),
                        'version': port_info.get('version', 'N/A')
                    })
            # Add host-specific information if no ports are found
            if not results:
                results.append({
                    'host': host,
                    'state': scanner[host].get('status', {}).get('state', 'unknown'),
                    'reason': scanner[host].get('status', {}).get('reason', 'N/A')
                })
        return results
    except Exception as e:
        raise RuntimeError(f"Error during Nmap Window scan: {e}")

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
        list: A list of dictionaries containing OS scan results with icons.
    """
    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform an OS scan (-O)
        scan_args = f"-O -T{scan_speed}" if scan_speed else "-O"
        scanner.scan(hosts=target, arguments=scan_args)

        results = []
        for host in scanner.all_hosts():
            os_matches = scanner[host].get('osmatch', [])
            for os_match in os_matches:
                os_name = os_match.get('name', 'Unknown')
                os_icon = OS_ICONS.get(os_name.split()[0], OS_ICONS["Unknown"])  # Match OS-Familie
                results.append({
                    'host': host,
                    'os_name': os_name,
                    'os_icon': os_icon,
                    'accuracy': os_match.get('accuracy', 'N/A')
                })
        return results
    except Exception as e:
        raise RuntimeError(f"Error during Nmap OS scan: {e}")