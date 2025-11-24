# app/blueprints/manager.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.announcement import Announcement
from app.models.employee import Employee
from app.models.inventory import InventoryItem
from datetime import datetime
from functools import wraps

bp = Blueprint('manager', __name__, template_folder='../templates/manager')

def manager_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'manager':
            flash('Access denied. Manager privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# 1. Manager Dashboard
@bp.route('/dashboard')
@manager_required
def dashboard():
    staff = Employee.query.filter_by(active=True).all()
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', staff=staff, announcements=announcements)


# 2. Executive Report
@bp.route('/executive_report')
@manager_required
def executive_report():
    kpi = {
        'revenue': 485000.00,
        'expenses': 298000.00,
        'patients': 1923,
        'avg_per_patient': 252.20
    }
    return render_template('executive_report.html', kpi=kpi)


# 3. Inventory Management
@bp.route('/inventory')
@manager_required
def inventory():
    items = InventoryItem.query.all()
    low_stock = [i for i in items if i.quantity <= i.min_stock]
    return render_template('inventory.html', inventory=items, low_stock_alerts=low_stock)


# 4. Manage Staff
@bp.route('/manage_staff')
@manager_required
def manage_staff():
    staff = Employee.query.filter(Employee.role != 'manager').all()
    return render_template('manage_staff.html', staff=staff)


# 5. Staff Scheduling (FullCalendar)
@bp.route('/staff_scheduling')
@manager_required
def staff_scheduling():
    staff = Employee.query.filter_by(active=True).all()
    return render_template('staff_scheduling.html', staff=staff)


# 6. View Announcements
@bp.route('/view_announcements')
@manager_required
def view_announcements():
    announcements = Announcement.query.filter(
        Announcement.target_role.in_(['all', 'manager'])
    ).order_by(Announcement.pinned.desc(), Announcement.timestamp.desc()).all()
    return render_template('view_announcements.html', announcements=announcements)  # or manager_view_announcements.html


# 7. Send Announcement / Message
@bp.route('/send_message', methods=['POST'])
@manager_required
def send_message():
    title = request.form.get('title', 'Clinic Update')
    message = request.form.get('message', '').strip()
    target_role = request.form.get('target_role', 'all')
    pinned = bool(request.form.get('pinned'))

    if not message:
        return jsonify(success=False, message="Message is required"), 400

    ann = Announcement(
        title=title,
        message=message,
        author=f"{current_user.first_name} {current_user.last_name}",
        target_role=target_role,
        pinned=pinned,
        category=request.form.get('category', 'general')
    )
    db.session.add(ann)
    db.session.commit()

    return jsonify(success=True, message="Announcement posted!")


# 8. API: Staff List for FullCalendar
@bp.route('/api/staff_list')
@manager_required
def api_staff_list():
    staff = Employee.query.filter_by(active=True).all()
    return jsonify([{
        'id': s.id,
        'name': f"{s.first_name} {s.last_name}",
        'role': s.role.capitalize(),
        'staff_number': s.staff_number
    } for s in staff])


# 9. Update Shift (FullCalendar)
@bp.route('/update_shift', methods=['POST'])
@manager_required
def update_shift():
    data = request.get_json()
    if not data:
        return jsonify(error="Invalid data"), 400

    # Here you would save to a Shift model
    # For now: log and return success
    print("Shift Update:", data)
    return jsonify(success=True, message="Shift saved")

@bp.route('/staff-counseling')
@login_required
def staff_counseling():
    return render_template('staff_counseling.html')