"""
This module defines a Flask application for performing nmap scans and rendering results.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from modules.nmap_scan import nmap_service_scan  # Ensure this module exists and is correctly implemented
from modules.nmap_scan import nmap_os_scan  # Import the OS scan function
from modules.nmap_scan import nmap_udp_scan  # Import the UDP scan function
from modules.nmap_scan import nmap_xmas_scan  # Import the Xmas scan function

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
        target = request.form['target']
        scan_type = request.form['scan_type']
        try:
            if scan_type == 'service':
                scan_results = nmap_service_scan(target)
                
            elif scan_type == 'os':
                scan_results = nmap_os_scan(target)  # Ensure this function is implemented in nmap_scan.py
                
            elif scan_type == 'tcp':
                scan_results = nmap_service_scan(target)
                
            elif scan_type == 'udp':
                scan_results = nmap_udp_scan(target)  # Ensure this function is implemented in nmap_scan.py
            
            elif scan_type == 'xmas':
                scan_results = nmap_xmas_scan(target)  # Ensure this function is implemented in nmap_scan.py
                
            else:
                scan_results = []

            return render_template('nmap.html', results=scan_results, target=target, scan_type=scan_type)
        except Exception as e:
            return render_template('nmap.html', error=str(e), target=target, scan_type=scan_type)
    else:
        return render_template('nmap.html')
    
@app.route('/targets', methods=['POST', 'GET'])
def targets():
    """
    Render the targets.html template for the targets page.
    """
    if request.method == 'POST':
        target = request.form['target']
        flash(f'Target {target} added successfully!')
        return redirect(url_for('targets'))
    return render_template('targets.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)