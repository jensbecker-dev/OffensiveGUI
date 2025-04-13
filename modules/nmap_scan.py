"""
Module for performing nmap scans using the nmap library.
"""

import nmap  # Ensure the python-nmap library is installed
from datetime import datetime

OS_ICONS = {
    "Windows": "fa-windows",
    "Linux": "fa-linux",
    "Mac OS": "fa-apple",
    "Unix": "fa-terminal",
    "Unknown": "fa-question-circle"
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
        scan_args = f"-sU -T{scan_speed} -vv" if scan_speed else "-sU -vv"
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
        scan_args = f"-sX -T{scan_speed} -vv" if scan_speed else "-sX -vv"
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
        scan_args = f"-sF -T{scan_speed} -vv" if scan_speed else "-sF -vv"
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
        scan_args = f"-sA -T{scan_speed} -vv" if scan_speed else "-sA -vv"
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
        scan_args = f"-sN -T{scan_speed} -vv" if scan_speed else "-sN -vv"
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
        scan_args = f"-sW -T{scan_speed} -vv" if scan_speed else "-sW -vv"
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
        scan_args = f"-sV -T{scan_speed} -vv" if scan_speed else "-sV -vv"
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
        dict: A dictionary containing OS scan results.
    """

    OS_ICONS = {
        "Windows": "fa-windows",
        "Linux": "fa-linux",
        "Mac OS": "fa-apple",
        "Unix": "fa-terminal",
        "Unknown": "fa-question-circle"
    }

    scanner = nmap.PortScanner()
    try:
        # Validate the target to ensure it's not empty
        if not target:
            raise ValueError("Target cannot be empty.")

        # Perform an OS detection scan (-O)
        scan_args = f"-O -T{scan_speed} -vv" if scan_speed else "-O -vv"
        scanner.scan(hosts=target, arguments=scan_args)

        results = []
        for host in scanner.all_hosts():
            os_info = scanner[host].get('osmatch', [])
            if os_info:
                os_name = os_info[0].get('name', 'unknown')
                os_accuracy = os_info[0].get('accuracy', 'unknown')
                os_family = os_info[0].get('os_class', 'unknown')
                os_version = os_info[0].get('os_version', 'unknown')
                os_vendor = os_info[0].get('os_vendor', 'unknown')
                os_results = {
                    'host': host,
                    'os_name': os_name,
                    'os_accuracy': os_accuracy,
                    'os_family': os_family,
                    'os_version': os_version,
                    'os_vendor': os_vendor
                }
                results.append(os_results)
            else:
                results.append({
                    'host': host,
                    'os_name': 'unknown',
                    'os_accuracy': 'unknown',
                    'os_family': 'unknown',
                    'os_version': 'unknown',
                    'os_vendor': 'unknown',
                })
            
        return results
    except ValueError as ve:
        raise ve
    except nmap.PortScannerError as pse:
        raise RuntimeError(f"Nmap PortScannerError: {pse}")
    except Exception as e:
        raise RuntimeError(f"Error during Nmap OS scan: {e}")