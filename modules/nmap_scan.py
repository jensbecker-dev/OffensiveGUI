import nmap

def nmap_scan(target, options):
    """
    Perform an Nmap scan on the specified target with the given options.
    """
    nm = nmap.PortScanner()
    try:
        nm.scan(target, arguments=options)
        results = {'hosts': []}
        for host in nm.all_hosts():
            host_data = {
                'address': host,
                'protocols': {}
            }
            for proto in nm[host].all_protocols():
                host_data['protocols'][proto] = {}
                for port in nm[host][proto].keys():
                    host_data['protocols'][proto][port] = {
                        'state': nm[host][proto][port]['state'],
                        'service': nm[host][proto][port].get('name', 'Unknown')
                    }
            results['hosts'].append(host_data)
        return results
    except Exception as e:
        return {'error': str(e)}