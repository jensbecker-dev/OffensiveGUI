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
        result = nmap_scan(target=target, options=options)
        return render_template(
            'nmap.html', result=result, target=target, options=options
        )
    return render_template('nmap.html', result=None)

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, port=8080)