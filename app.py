"""
This module defines a Flask application for performing nmap scans and rendering results.
"""

from flask import Flask, render_template, request
from modules.nmap_scan import nmap_scan  # Ensure this module exists and is correctly implemented

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    """
    Render the index.html template for the home page.
    """
    return render_template('index.html')

@app.route('/nmap', methods=['POST', 'GET'])
def nmap_scan_route():
    """
    Perform an nmap scan using the imported nmap_scan function and render the results.
    """
    if request.method == 'POST':
        target = request.form.get('target', '')
        scan_type = request.form.get('scan_type', 'quick')

        try:
            # Perform the nmap scan
            raw_result = nmap_scan(target=target, scan_type=scan_type)

            # Parse the results for rendering
            parsed_results = []
            for host in raw_result.get('hosts', []):
                host_ip = host.get('ip', target)
                for protocol, ports in host.get('protocols', {}).items():
                    for port, details in ports.items():
                        parsed_results.append({
                            'host': host_ip,
                            'port': port,
                            'protocol': protocol,
                            'state': details.get('state', 'Unknown'),
                            'service': details.get('service', 'Unknown'),
                            'version': details.get('version', 'N/A') if scan_type == 'service' else None,
                            'os': host.get('os', 'N/A') if scan_type == 'os' else None
                        })

            return render_template(
                'nmap.html',
                results={'hosts': parsed_results},
                target=target,
                scan_type=scan_type,
                scan_types=['quick', 'full', 'os', 'service'],
                error=None
            )

        except Exception as e:
            # Handle errors and display them in the template
            return render_template(
                'nmap.html',
                results=None,
                target=target,
                scan_type=scan_type,
                scan_types=['quick', 'full', 'os', 'service'],
                error=str(e)
            )

    # Render the page with default values for GET requests
    return render_template(
        'nmap.html',
        results=None,
        target=None,
        scan_type=None,
        scan_types=['quick', 'full', 'os', 'service'],
        error=None
    )

if __name__ == '__main__':
    app.run(debug=True, port=8080)