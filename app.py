from flask import Flask, render_template, request, redirect, url_for
from modules.nmap_scan import nmap_scan  # Import the nmap_scan function

app = Flask(__name__)

@app.route('/')
def home():
    """
    Render the index.html template for the home page.
    """
    return render_template('index.html')

@app.route('/home')
@app.route('/index')
def home_route():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/nmap', methods=['POST', 'GET'])
def nmap_scan_route():
    """
    Perform an nmap scan using the imported nmap_scan function and render the results.
    """
    if request.method == 'POST':
        target = request.form.get('target', '127.0.0.1')  # Default target is localhost
        options = request.form.get('options', '-sV')      # Default options
        # Perform the nmap scan using the imported function
        raw_result = nmap_scan(target=target, options=options)
        
        # Parse the raw result into a structured format
        parsed_results = []
        for host in raw_result.get('hosts', []):
            for protocol, ports in host.get('protocols', {}).items():
                for port, details in ports.items():
                    parsed_results.append({
                        'port': port,
                        'protocol': protocol,
                        'state': details['state'],
                        'service': details.get('service', 'Unknown')
                    })
            return render_template(
                'nmap.html', results=parsed_results, target=target, options=options
            )
        # If no hosts are found, return an empty result
        return render_template(
            'nmap.html', results=[], target=target, options=options
        )
    else:
        # If the request method is GET, render the nmap.html template without results
        # This is useful for displaying the form without any previous results.
        return render_template('nmap.html', results=None)

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, port=8080)
    