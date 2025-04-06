"""
This module defines a Flask application for performing nmap scans and rendering results.
export FLASK_APP=app.py  # On Linux/Mac
set FLASK_APP=app.py     # On Windows
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from modules.nmap_scan import nmap_tcp_scan, nmap_udp_scan, nmap_xmas_scan, nmap_service_scan, nmap_os_scan, stop_time
from modules.target_mon import run_target_monitor
import json
from datetime import datetime

app= Flask(__name__)
app.secret_key = 'S3Cr3T_K3Y'

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offsec_gui.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Define the Target model
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_value = db.Column(db.String(255), nullable=False)
    scan_results = db.relationship('ScanResult', backref='target', lazy=True, cascade="all, delete-orphan")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

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

    def __repr__(self):
        return f"<ScanResult {self.scan_type} for Target {self.target_id}>"

# Define the ActionLog model
class ActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_value = db.Column(db.String(255), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ActionLog {self.action} on {self.target_value}>"

# Define a dictionary to store the last action
last_action = {}


@app.route('/target_monitor', methods=['GET'])
def target_monitor():
    """
    Monitor target activities and display results on the dashboard.
    """
    targets = Target.query.all()
    if not targets:
        flash("No targets available to monitor.")
        return redirect(url_for('home'))

    # Run the target monitor
    monitor_results = []
    for target in targets:
        result = run_target_monitor([target.target_value])[0]  # Get the first result
        result['added_time'] = target.timestamp.strftime("%Y-%m-%d %H:%M:%S")  # Add timestamp
        monitor_results.append(result)

    return render_template(
        'index.html',
        targets=targets,
        monitor_results=monitor_results,
        last_action=last_action,
        action_logs=ActionLog.query.order_by(ActionLog.timestamp.desc()).limit(10).all()
    )

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
            # Log the action
            new_log = ActionLog(target_value=target_value, action="Added Target")
            db.session.add(new_log)
            db.session.commit()
        else:
            flash('Target value cannot be empty.')
        return redirect(url_for('home'))
    
    if request.method == 'GET':
        targets = [target.target_value for target in Target.query.all()]
        if not targets:
            flash("No targets available to monitor.")
            return redirect(url_for('home'))

        # Run the target monitor
        monitor_results = run_target_monitor(targets)

        return render_template(
            'index.html',
            targets=Target.query.all(),
            monitor_results=monitor_results,
            last_action=last_action,
            action_logs=ActionLog.query.order_by(ActionLog.timestamp.desc()).limit(10).all()
        )
    
    all_targets = Target.query.all()
    action_logs = ActionLog.query.order_by(ActionLog.timestamp.desc()).limit(10).all()  # Fetch the last 10 actions
    return render_template('index.html', targets=all_targets, last_action=last_action, action_logs=action_logs)

@app.route('/nmap', methods=['POST', 'GET'])
def nmap_scan_route():
    """
    Perform an nmap scan using the imported nmap_scan function and render the results.
    """
    global last_action
    targets = Target.query.all()
    if request.method == 'POST':
        target_id = request.form['target']
        scan_type = request.form['scan_type']
        scan_speed = request.form['scan_speed']
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            target = Target.query.get_or_404(target_id)
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

            if not isinstance(scan_results, list):
                flash("Unexpected scan results format.")
                scan_results = []

            new_scan = ScanResult(
                target_id=target.id,
                scan_type=scan_type,
                scan_speed=scan_speed,
                results=str(scan_results)
            )
            db.session.add(new_scan)
            db.session.commit()

            last_action = {
                "target_value": target.target_value,
                "action": f"Performed {scan_type.upper()} Scan",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Log the action
            new_log = ActionLog(target_value=target.target_value, action=f"Performed {scan_type.upper()} Scan")
            db.session.add(new_log)
            db.session.commit()

            final_time_log = stop_time(start_time)
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
        except RuntimeError as re:
            flash(str(re))
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

@app.route('/edit_target/<int:target_id>', methods=['POST', 'GET'])
def edit_target(target_id):
    """
    Edit a target in the database.
    """
    target_to_edit = Target.query.get_or_404(target_id)
    new_value = request.form.get('new_target_value')
    if new_value:
        target_to_edit.target_value = new_value
        db.session.commit()
        flash(f'Target updated to {new_value} successfully!')
    else:
        flash('New target value cannot be empty.')
    return redirect(url_for('targets'))

@app.route('/delete_target/<int:target_id>', methods=['POST', 'GET'])
def delete_target(target_id):
    """
    Delete a target from the database.
    """
    target_to_delete = Target.query.get_or_404(target_id)
    db.session.delete(target_to_delete)
    db.session.commit()
    flash(f'Target {target_to_delete.target_value} deleted successfully!')
    # Log the action
    new_log = ActionLog(target_value=target_to_delete.target_value, action="Deleted Target")
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('targets'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)