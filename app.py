"""
This module defines a Flask application for performing nmap scans and rendering results.
export FLASK_APP=app.py  # On Linux/Mac
set FLASK_APP=app.py     # On Windows
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from modules.nmap_scan import nmap_tcp_scan, nmap_udp_scan, nmap_xmas_scan, nmap_service_scan, nmap_os_scan, nmap_fin_scan, nmap_ack_scan, nmap_window_scan, nmap_null_scan
from modules.nmap_scan import stop_time
from modules.target_mon import run_target_monitor
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///offensivegui.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

class DatabaseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text, nullable=False)
    target_value = db.Column(db.String(100), nullable=True)  # Neue Spalte für das Target

# Define the Target model
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target_value = db.Column(db.String(100), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=True)  # Neue Spalte

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
            # Log the action
            new_log = DatabaseLog(action="Added Target", details=f"Target {target_value} added.")
            db.session.add(new_log)
            db.session.commit()
        else:
            flash('Target value cannot be empty.')
        return redirect(url_for('home'))
    
    elif request.method == 'POST':
        target_id = request.form['delete']
        target_to_delete = Target.query.get_or_404(target_id)
        db.session.delete(target_to_delete)
        db.session.commit()
        flash(f'Target {target_to_delete.target_value} deleted successfully!')
        # Log the action
        new_log = DatabaseLog(action="Deleted Target", details=f"Target {target_to_delete.target_value} deleted.")
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        all_targets = Target.query.all()
        active_target_values = [target.target_value for target in all_targets]

        # Run monitoring for active targets
        monitor_results = run_target_monitor(active_target_values)

        # Fetch updated monitor results for active targets only
        action_logs = (
            DatabaseLog.query.order_by(DatabaseLog.timestamp.desc())
            .limit(8)  # Fetch the last 8 actions
            .all()
        )

        return render_template(
            'index.html',
            title="Dashboard - Offensive GUI",
            nav_links=[
                {"name": "Home", "url": url_for('home')},
                {"name": "Nmap Scans", "url": url_for('nmap_scan_route')},
                {"name": "Targets", "url": url_for('targets')}
            ],
            targets=all_targets,
            monitor_results=monitor_results,
            last_action=last_action,
            action_logs=action_logs
        )

@app.route('/nmap', methods=['POST', 'GET'])
def nmap_scan_route():
    """
    Perform an nmap scan using the imported nmap_scan function and render the results.
    """
    global last_action

    if request.method == 'POST':
        # Check if a target is selected
        if 'target' not in request.form:
            flash('Please select a target.')
            return redirect(url_for('nmap_scan_route'))

        target_id = request.form['target']
        scan_type = request.form['scan_type']
        scan_speed = request.form['scan_speed']
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Fetch the selected target from the database
            target = Target.query.get_or_404(target_id)

            # Initialize scan_results with a default value
            scan_results = []

            # Perform the scan based on the selected type
            if scan_type == 'tcp':
                scan_results = nmap_tcp_scan(target.target_value, scan_speed)
            elif scan_type == 'udp':
                scan_results = nmap_udp_scan(target.target_value, scan_speed)
            elif scan_type == 'xmas':
                scan_results = nmap_xmas_scan(target.target_value, scan_speed)
            elif scan_type == 'fin':
                scan_results = nmap_fin_scan(target.target_value, scan_speed)
            elif scan_type == 'ack':
                scan_results = nmap_ack_scan(target.target_value, scan_speed)
            elif scan_type == 'null':
                scan_results = nmap_null_scan(target.target_value, scan_speed)
            elif scan_type == 'window':
                scan_results = nmap_window_scan(target.target_value, scan_speed)
            elif scan_type == 'service':
                scan_results = nmap_service_scan(target.target_value, scan_speed)
            elif scan_type == 'os':
                scan_results = nmap_os_scan(target.target_value, scan_speed)

                        # If OS scan is not selected, include OS information if relevant
            if scan_type != 'os':
                os_results = nmap_os_scan(target.target_value, scan_speed)
                for result in scan_results:
                    for os_result in os_results:
                        if result['host'] == os_result['host']:
                            result['os_name'] = os_result.get('os_name', 'Unknown')
                            result['os_family'] = os_result.get('os_family', 'Unknown')
                            result['os_vendor'] = os_result.get('os_vendor', 'Unknown')

            if not isinstance(scan_results, list):
                flash("Unexpected scan results format.")
                scan_results = []

            # Log the action
            last_action = {
                "target_value": target.target_value,
                "action": f"Performed {scan_type.upper()} Scan",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            new_log = DatabaseLog(
                action=f"Performed {scan_type.upper()} Scan",
                details=f"Scan on {target.target_value}.",
                target_value=target.target_value
            )
            db.session.add(new_log)
            db.session.commit()

            # Calculate the scan time
            final_time_log = stop_time(start_time)

            # Fetch all targets and their status after the scan
            all_targets = Target.query.all()
            active_target_values = [target.target_value for target in all_targets]
            monitor_results = run_target_monitor(active_target_values)

            return render_template(
                'nmap.html',
                target=target.target_value,
                scan_type=scan_type,
                scan_speed=scan_speed,
                results=scan_results,
                final_time_log=final_time_log,
                targets=all_targets,
                monitor_results=monitor_results
            )
        
        except ValueError as ve:
            flash(str(ve))
        except RuntimeError as re:
            flash(str(re))

    # Default GET route
    all_targets = Target.query.all()
    active_target_values = [target.target_value for target in all_targets]
    monitor_results = run_target_monitor(active_target_values)

    return render_template(
        'nmap.html',
        targets=all_targets,
        monitor_results=monitor_results
    )

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
            # Log the action
            new_log = DatabaseLog(action="Added Target", details=f"Target {target_value} added.")
            db.session.add(new_log)
            db.session.commit()
        else:
            flash('Target value cannot be empty.')
        return redirect(url_for('targets'))

    all_targets = Target.query.all()

    return render_template('targets.html', targets=all_targets)

@app.route('/edit_target/<int:target_id>', methods=['POST'])
def edit_target(target_id):
    target = Target.query.get_or_404(target_id)
    new_value = request.form['target_value']
    old_value = target.target_value
    target.target_value = new_value
    target.last_updated = datetime.utcnow()
    db.session.commit()

    # Log the action
    new_log = DatabaseLog(
        action="Edited Target",
        details=f"Target changed from {old_value} to {new_value}.",
        target_value=new_value  # Speichern des neuen Targets im Log
    )
    db.session.add(new_log)
    db.session.commit()

    flash(f"Target updated successfully!", "success")
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
    new_log = DatabaseLog(action="Deleted Target", details=f"Target {target_to_delete.target_value} deleted.")
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for('targets'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    db_logs = DatabaseLog.query.order_by(DatabaseLog.timestamp.desc()).all()
    return render_template('settings.html', db_logs=db_logs)

@app.route('/delete_database', methods=['POST'])
def delete_database():
    """
    Delete the entire database and all its data.
    """
    try:
        Target.query.delete()
        DatabaseLog.query.delete()
        db.session.commit()

        # Log the action
        new_log = DatabaseLog(
            action="Delete Database",
            details="All data in the database was deleted."
        )
        db.session.add(new_log)
        db.session.commit()

        flash("Database deleted successfully!", "danger")
    except Exception as e:
        flash(f"An error occurred while deleting the database: {str(e)}", "danger")
    return redirect(url_for('settings'))

@app.route('/recreate_database', methods=['POST'])
def recreate_database():
    """
    Recreate the database structure.
    """
    try:
        db.drop_all()
        db.create_all()
        db.session.commit()

        # Log the action
        new_log = DatabaseLog(
            action="Recreate Database",
            details="Database structure recreated."
        )
        db.session.add(new_log)
        db.session.commit()

        flash("Database recreated successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while recreating the database: {str(e)}", "danger")
    return redirect(url_for('settings'))

@app.route('/create_example_targets', methods=['POST'])
def create_example_targets():
    try:
        # Add 3 example targets
        example_targets = [
            Target(target_value="127.0.0.1"),
            Target(target_value="192.168.1.1"),
            Target(target_value="example.com"),
        ]
        db.session.add_all(example_targets)
        db.session.commit()

        # Log the action
        new_log = DatabaseLog(
            action="Create Example Targets",
            details="3 example targets created for testing purposes."
        )
        db.session.add(new_log)
        db.session.commit()

        flash("3 example targets created successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while creating example targets: {str(e)}", "danger")

    return redirect(url_for('settings'))

@app.route('/clear_all_targets', methods=['POST'])
def clear_all_targets():
    """
    Clear all targets from the database.
    """
    try:
        # Delete all targets
        Target.query.delete()
        db.session.commit()

        # Log the action
        new_log = DatabaseLog(
            action="Clear All Targets",
            details="All targets were deleted from the database."
        )
        db.session.add(new_log)
        db.session.commit()

        flash("All targets cleared successfully!", "danger")
    except Exception as e:
        flash(f"An error occurred while clearing targets: {str(e)}", "danger")

    return redirect(url_for('settings'))

@app.route('/add_target', methods=['POST'])
def add_target():
    target_value = request.form['target']
    if target_value:
        new_target = Target(target_value=target_value)
        db.session.add(new_target)
        db.session.commit()

        # Log the action
        new_log = DatabaseLog(
            action="Added Target",
            details=f"Target {target_value} was added.",
            target_value=target_value  # Speichern des Targets im Log
        )
        db.session.add(new_log)
        db.session.commit()

        flash(f"Target {target_value} added successfully!", "success")
    else:
        flash("Target value cannot be empty.", "danger")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)