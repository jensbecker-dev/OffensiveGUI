"""
This module defines a Flask application for performing nmap scans and rendering results.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from modules.nmap_scan import nmap_service_scan  # Ensure this module exists and is correctly implemented
from modules.nmap_scan import nmap_os_scan  # Import the OS scan function

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
        scan_type = request.form['scan_type']  # Get the selected scan type from the dropdown
        try:
            if scan_type == 'service':
                scan_results = nmap_service_scan(target)
            elif scan_type == 'os':
                scan_results = nmap_os_scan(target)
                return render_template('nmap.html', results=scan_results, target=target, scan_type=scan_type)
            else:
                raise ValueError("Invalid scan type selected.")
            return render_template('nmap.html', results=scan_results, target=target, scan_type=scan_type)
        except Exception as e:
            return render_template('nmap.html', error=str(e), target=target, scan_type=scan_type)
    else:
        return render_template('nmap.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)