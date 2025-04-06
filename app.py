"""
This module defines a Flask application for performing nmap scans and rendering results.
"""
# Import necessary libraries and modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from modules.nmap_scan import nmap_tcp_scan  # Import the TCP scan function
from modules.nmap_scan import nmap_udp_scan  # Import the UDP scan function
from modules.nmap_scan import nmap_xmas_scan  # Import the Xmas scan function
from modules.nmap_scan import nmap_service_scan  # Ensure this module exists and is correctly implemented
from modules.nmap_scan import nmap_os_scan  # Import the OS scan function
from modules.nmap_scan import stop_time  # Import the scan time logging function
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'S3Cr3T_K3Y'  # Add a secret key for session management

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offsec_gui.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Target model
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_value = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Target {self.target_value}>"

# Define the ScanResult model
class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('target.id'), nullable=False)
    scan_type = db.Column(db.String(50), nullable=False)
    scan_speed = db.Column(db.String(50), nullable=False)
    results = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    target = db.relationship('Target', backref=db.backref('scan_results', lazy=True))

    def __repr__(self):
        return f"<ScanResult {self.scan_type} for Target {self.target_id}>"

# Define a dictionary to store the last action
last_action = {}

@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    """
    Render the index.html template for the home page.
    """
    global last_action
    if request.method == 'POST':
        target_value = request.form['target']
        if target_value:
            new_target = Target(target_value=target_value)
            db.session.add(new_target)
            db.session.commit()
            flash(f'Target {target_value} added successfully!')
            last_action = {
                "target_value": target_value,
                "action": "Added Target",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            flash('Target value cannot be empty.')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        all_targets = Target.query.all()
        return render_template('index.html', targets=all_targets, last_action=last_action)
    return render_template('index.html', last_action=last_action)

@app.route('/nmap', methods=['POST', 'GET'])
def nmap_scan_route():
    """
    Perform an nmap scan using the imported nmap_scan function and render the results.
    """
    global last_action
    targets = Target.query.all()  # Fetch all targets from the database
    if request.method == 'POST':
        target_id = request.form['target']  # Ensure this matches the updated dropdown value
        scan_type = request.form['scan_type']
        scan_speed = request.form['scan_speed']
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            target = Target.query.get_or_404(target_id)  # Fetch target by ID
            if scan_type == 'tcp':
                scan_results = nmap_tcp_scan(target.target_value, scan_speed)
            elif scan_type == 'udp':
                scan_results = nmap_udp_scan(target.target_value, scan_speed)
            elif scan_type == 'xmas':
                scan_results = nmap_xmas_scan(target.target_value, scan_speed)
            elif scan_type == 'service':
                scan_results = nmap_service_scan(target.target_value, scan_speed)
            elif scan_type == 'os':
                scan_results = nmap_os_scan(target.target_value, scan_speed)
            else:
                scan_results = []

            # Ensure scan_results is a list of dictionaries
            if not isinstance(scan_results, list):
                flash("Unexpected scan results format.")
                scan_results = []

            # Save scan results to the database
            new_scan = ScanResult(
                target_id=target.id,
                scan_type=scan_type,
                scan_speed=scan_speed,
                results=str(scan_results)  # Save results as a string
            )
            db.session.add(new_scan)
            db.session.commit()

            # Update last action
            last_action = {
                "target_value": target.target_value,
                "action": f"Performed {scan_type.upper()} Scan",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            final_time_log = stop_time(start_time)  # Calculate the time taken for the scan
            return render_template(
                'nmap.html',
                target=target.target_value,
                scan_type=scan_type,
                scan_speed=scan_speed,
                results=scan_results,
                final_time_log=final_time_log,
                targets=targets
            )
        
        except ValueError as ve:
            flash(str(ve))
            final_time_log = stop_time(start_time)
            return render_template(
                'nmap.html',
                target=target.target_value,
                scan_type=scan_type,
                scan_speed=scan_speed,
                results=[],
                final_time_log=final_time_log,
                targets=targets
            )
        except RuntimeError as re:
            flash(str(re))
            return render_template(
                'nmap.html',
                target=target.target_value,
                scan_type=scan_type,
                scan_speed=scan_speed,
                results=[],
                final_time_log=None,
                targets=targets
            )
    else:
        flash('Please select a scan type and enter a target.')
        return render_template('nmap.html', targets=targets)

@app.route('/targets', methods=['POST', 'GET'])
def targets():
    """
    Render the targets.html template for the targets page and manage target values.
    """
    if request.method == 'POST':
        target_value = request.form['target']
        if target_value:
            new_target = Target(target_value=target_value)
            db.session.add(new_target)
            db.session.commit()
            flash(f'Target {target_value} added successfully!')
        else:
            flash('Target value cannot be empty.')
        return redirect(url_for('targets'))

    all_targets = Target.query.all()
    return render_template('targets.html', targets=all_targets)

# Route to edit a target
@app.route('/edit_target/<int:target_id>', methods=['POST', 'GET'])
def edit_target(target_id):
    """
    Edit a target in the database.
    """
    target_to_edit = Target.query.get_or_404(target_id)
    new_value = request.form.get('new_target_value')  # Use .get() to avoid KeyError
    if new_value:
        target_to_edit.target_value = new_value
        db.session.commit()
        flash(f'Target updated to {new_value} successfully!')
    else:
        flash('New target value cannot be empty.')
    return redirect(url_for('targets'))

# Route to delete a target
@app.route('/delete_target/<int:target_id>', methods=['POST', 'GET'])
def delete_target(target_id):
    """
    Delete a target from the database.
    """
    target_to_delete = Target.query.get_or_404(target_id)
    db.session.delete(target_to_delete)
    db.session.commit()
    flash(f'Target {target_to_delete.target_value} deleted successfully!')
    return redirect(url_for('targets'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database and tables are created
    app.run(debug=True, port=8080)
