"""
This module defines a Flask application for performing nmap scans and rendering results.
"""

from tracemalloc import stop
from typing import final
from flask import Flask, render_template, request, redirect, url_for, flash
from modules.nmap_scan import nmap_service_scan  # Ensure this module exists and is correctly implemented
from modules.nmap_scan import nmap_os_scan  # Import the OS scan function
from modules.nmap_scan import nmap_tcp_scan  # Import the TCP scan function
from modules.nmap_scan import nmap_udp_scan  # Import the UDP scan function
from modules.nmap_scan import nmap_xmas_scan  # Import the Xmas scan function
from modules.nmap_scan import stop_time  # Import the scan time logging function
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'S3Cr3T_K3Y'  # Add a secret key for session management

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
        scan_speed = request.form['scan_speed']
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
        
            if scan_type == 'tcp':
                scan_results = nmap_tcp_scan(target, scan_speed)  # Ensure this function is implemented in nmap_scan.py
                
            elif scan_type == 'udp':
                scan_results = nmap_udp_scan(target, scan_speed)  # Ensure this function is implemented in nmap_scan.py
            
            elif scan_type == 'xmas':
                scan_results = nmap_xmas_scan(target, scan_speed)  # Ensure this function is implemented in nmap_scan.py
            
            elif scan_type == 'service':
                scan_results = nmap_service_scan(target, scan_speed)  # Ensure this function is implemented in nmap_scan.py
                
            elif scan_type == 'os':
                scan_results = nmap_os_scan(target, scan_speed)  # Ensure this function is implemented in nmap_scan.py
                
            else:
                results = []

            final_time_log = stop_time(start_time)  # Calculate the time taken for the scan
            return render_template('nmap.html', target=target, scan_type=scan_type, scan_speed=scan_speed, results=scan_results, final_time_log=final_time_log)
        
        except ValueError as ve:
            flash(str(ve))
            final_time_log = stop_time(start_time)  # Calculate the time taken for the scan
            return render_template('nmap.html', target=target, scan_type=scan_type, scan_speed=scan_speed, results=[], final_time_log=final_time_log)
        except RuntimeError as re:
            flash(str(re))
            return render_template('nmap.html', target=target, scan_type=scan_type, scan_speed=scan_speed, results=[], final_time_log=None)
        
    else:
        flash('Please select a scan type and enter a target.')
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
