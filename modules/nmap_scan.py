import nmap

def nmap_scan(target, options):
    
    """
    Perform an Nmap scan on the specified target with the given options.
    
    Args:
        target (str): The target IP address or hostname to scan.
        options (str): Additional Nmap options as a string.
        
    Returns:
        str: The output of the Nmap scan.
    """
    
    nm = nmap.PortScanner()
    try:
        nm.scan(target, arguments=options)
        scan_results = nm.all_hosts()
        
        output = ""
        for host in scan_results:
            output += f"Host: {host}\n"
            for proto in nm[host].all_protocols():
                output += f"Protocol: {proto}\n"
                ports = nm[host][proto].keys()  # Use keys() to get the list of ports
                for port in ports:
                    output += f"Port: {port}, State: {nm[host][proto][port]['state']}\n"
        
        return output.strip()
    except nmap.PortScannerError as e:
        return f"Error: {e}"
    except Exception as e:
        return str(e)