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
        scanner.scan(hosts=hosts, arguments='-O -p- -vv')

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
    
if __name__ == "__main__":
    nmap_os_scan()