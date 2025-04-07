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
from datetime import datetime

app = Flask(__name__)
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

# Define the MonitorResult model
class MonitorResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    added_time = db.Column(db.DateTime, default=datetime.utcnow)

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
            new_log = ActionLog(target_value=target_value, action="Added Target")
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
        new_log = ActionLog(target_value=target_to_delete.target_value, action="Deleted Target")
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        all_targets = Target.query.all()
        active_target_values = [target.target_value for target in all_targets]

        # Run monitoring for active targets
        monitor_results = run_target_monitor(active_target_values)

        # Update or insert monitoring results into the database
        for result in monitor_results:
            if result['target'] in active_target_values:  # Ensure the target exists in the database
                existing_result = MonitorResult.query.filter_by(target=result['target']).first()
                if existing_result:
                    existing_result.status = result['status']
                    existing_result.added_time = datetime.utcnow()
                else:
                    new_result = MonitorResult(target=result['target'], status=result['status'])
                    db.session.add(new_result)
        db.session.commit()

        # Fetch updated monitor results for active targets only
        monitor_results_to_display = MonitorResult.query.filter(
            MonitorResult.target.in_(active_target_values)
        ).order_by(MonitorResult.added_time.desc()).limit(8).all()  # Fetch the last 8 targets

        action_logs = (
            ActionLog.query.order_by(ActionLog.timestamp.desc())
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
            monitor_results=monitor_results_to_display,
            last_action=last_action,
            action_logs=action_logs
        )

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
            # Log the action
            new_log = ActionLog(target_value=target_value, action="Added Target")
            db.session.add(new_log)
            db.session.commit()
        else:
            flash('Target value cannot be empty.')
        return redirect(url_for('targets'))

    all_targets = Target.query.all()
    monitor_results = {result.target: result for result in MonitorResult.query.all()}  # Fetch monitor results

    # Combine target data with monitor results
    targets_with_status = [
        {
            "id": target.id,
            "target_value": target.target_value,
            "status": monitor_results[target.target_value].status if target.target_value in monitor_results else "Unknown",
            "last_updated": monitor_results[target.target_value].added_time if target.target_value in monitor_results else "N/A"
        }
        for target in all_targets
    ]

    return render_template('targets.html', targets=targets_with_status)

@app.route('/edit_target/<int:target_id>', methods=['POST', 'GET'])
def edit_target(target_id):
    """
    Edit a target in the database.
    """
    target_to_edit = Target.query.get_or_404(target_id)
    new_value = request.form.get('new_target_value')
    if new_value:
        old_value = target_to_edit.target_value
        target_to_edit.target_value = new_value
        db.session.commit()
        flash(f'Target updated to {new_value} successfully!')
        # Log the action
        new_log = ActionLog(target_value=old_value, action=f"Edited Target to {new_value}")
        db.session.add(new_log)
        db.session.commit()
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

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    """
    Render the settings.html template for the settings page.
    """
    return render_template('settings.html')

@app.route('/delete_database', methods=['POST'])
def delete_database():
    """
    Delete the entire database and all its data.
    """
    try:
        db.drop_all()
        db.session.commit()
        flash("Database deleted successfully!", "success")
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
        flash("Database recreated successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while recreating the database: {str(e)}", "danger")
    return redirect(url_for('settings'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)