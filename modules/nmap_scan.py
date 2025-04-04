"""
Module for performing Nmap scans using the nmap library.
"""

import nmap


def nmap_scan(target, scan_type):
    """
    Perform an Nmap scan on the specified target with the selected scan type.
    """
    nm = nmap.PortScanner()
    scan_options = {
        'quick': '-T4 -F',
        'full': '-T4 -p-',
        'os': '-O',
        'service': '-sV'
    }
    try:
        options = scan_options.get(scan_type, '-T4')
        if scan_type == 'quick':
            options += ' -sS'
        elif scan_type == 'os':
            options += ' -O'
        elif scan_type == 'service':
            options += ' -sV'
        else:
            options += ' -T4 -F'
        nm.scan(target, arguments=options)
        results = {
            'hosts': [],
            'scan_type': scan_type,
            'options': options,
            'scaninfo': {},
            'osmatch': {},
            'hostnames': {},
            'tcp': {},
            'udp': {},
            'ip': {},
            'hostname': {}
        }
        # Collecting scan results
        if 'scaninfo' in nm.scanstats():
            results['scaninfo'] = nm.scanstats()
        for host in nm.all_hosts():
            if 'osmatch' in nm[host]:
                results['osmatch'][host] = nm[host]['osmatch']
            if 'hostnames' in nm[host]:
                results['hostnames'][host] = nm[host]['hostnames']
            if 'tcp' in nm[host]:
                results['tcp'][host] = nm[host]['tcp']
            if 'udp' in nm[host]:
                results['udp'][host] = nm[host]['udp']
            if 'addresses' in nm[host]:
                results['ip'][host] = nm[host]['addresses']
            if 'hostnames' in nm[host]:
                results['hostname'][host] = nm[host]['hostnames']
        for host in nm.all_hosts():
            host_data = {
                'os': (
                    nm[host]['osmatch'][0]['name']
                    if 'osmatch' in nm[host] and nm[host]['osmatch']
                    else 'Unknown'
                ),
                'address': host,
                'protocols': {}
            }
            for proto in nm[host].all_protocols():
                host_data['protocols'][proto] = {}
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    service = nm[host][proto][port].get('name', 'Unknown')
                    version = nm[host][proto][port].get('version', 'N/A')
                    host_data['protocols'][proto][port] = {
                        'state': state,
                        'service': service,
                        'version': version
                    }
            # Append host data to results
            results['hosts'].append(host_data)
        return results
    except Exception as e:
        return {'error': str(e)}
