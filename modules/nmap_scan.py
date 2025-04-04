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
        'full': '-p-',
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
        if 'scaninfo' in nm.all_scans():
            results['scaninfo'] = nm.all_scans()['scaninfo']
        if 'osmatch' in nm.all_scans():
            results['osmatch'] = nm.all_scans()['osmatch']
        if 'hostnames' in nm.all_scans():
            results['hostnames'] = nm.all_scans()['hostnames']
        if 'tcp' in nm.all_scans():
            results['tcp'] = nm.all_scans()['tcp']
        if 'udp' in nm.all_scans():
            results['udp'] = nm.all_scans()['udp']
        if 'ip' in nm.all_scans():
            results['ip'] = nm.all_scans()['ip']
        if 'hostname' in nm.all_scans():
            results['hostname'] = nm.all_scans()['hostname']
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
                    if scan_type == "quick":
                        port_data = {
                            'state': nm[host][proto][port]['state'],
                            'service': nm[host][proto][port].get('name', 'Unknown')
                        }
                    elif scan_type == "full":
                        port_data = {
                            'state': nm[host][proto][port]['state'],
                            'service': nm[host][proto][port].get('name', 'Unknown'),
                            'version': nm[host][proto][port].get('version', 'Unknown')
                        }
                    elif scan_type == "os":
                        port_data = {
                            'state': nm[host][proto][port]['state'],
                            'service': nm[host][proto][port].get('name', 'Unknown'),
                            'os': host_data['os']
                        }
                    elif scan_type == "service":
                        port_data = {
                            'state': nm[host][proto][port]['state'],
                            'service': nm[host][proto][port].get('name', 'Unknown'),
                            'version': nm[host][proto][port].get('version', 'Unknown')
                        }
                    else:
                        port_data = {
                            'state': nm[host][proto][port]['state'],
                            'service': nm[host][proto][port].get('name', 'Unknown')
                        }
                    if 'name' in nm[host][proto][port]:
                        port_data['service'] = nm[host][proto][port]['name']
                    if 'version' in nm[host][proto][port]:
                        port_data['version'] = nm[host][proto][port]['version']
                    host_data['protocols'][proto][port] = port_data
            results['hosts'].append(host_data)
        return results
    except Exception as e:
        return {'error': str(e)}
