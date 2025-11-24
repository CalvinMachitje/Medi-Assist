# app/blueprints/manager.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.announcement import Announcement
from app.models.employee import Employee
from app.models.audit_log import AuditLog
from datetime import datetime
from functools import wraps

bp = Blueprint('manager', __name__, template_folder='../templates/manager')

def manager_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'manager':
            flash('Access denied.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@bp.route('/dashboard')
@login_required
@manager_required
def dashboard():
    staff = Employee.query.filter_by(active=True).all()
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()
    return render_template('dashboard.html', staff=staff, announcements=announcements)


@bp.route('/manager_send_message', methods=['POST'])
@login_required
@manager_required
def manager_send_message():
    msg_type = request.form.get('msg_type', 'announcement')
    title = request.form.get('title', 'Announcement')
    message = request.form.get('message')
    target_role = request.form.get('target_role', 'all')
    pinned = 'pinned' in request.form

    if not message:
        return jsonify({'success': False, 'message': 'Message required'}), 400

    if msg_type == 'announcement':
        ann = Announcement(
            title=title,
            message=message,
            author=f"{current_user.first_name} {current_user.last_name}",
            target_role=target_role,
            pinned=pinned,
            category='general'
        )
        db.session.add(ann)
        db.session.commit()

    flash('Message sent successfully!', 'success')
    return jsonify({'success': True, 'message': 'Sent!'})


@bp.route('/update_shift', methods=['POST'])
@login_required
@manager_required
def update_shift():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    employee_id = data.get('employee_id')
    shift_date = data.get('shift_date')
    shift_type = data.get('shift_type')
    shift_id = data.get('id')

    if not all([employee_id, shift_date, shift_type]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Example conflict check (you can expand with a real Shift model later)
    # For now, just check if employee already has a shift on that date
    conflict = db.session.execute(
        db.select(Employee).where(
            Employee.id == employee_id,
            db.func.date(Employee.hire_date) == shift_date  # placeholder logic
        )
    ).scalar()

    if conflict:
        return jsonify({'error': 'Shift conflict! Employee already scheduled.'}), 409

    # Here you would save to a Shift table — placeholder success
    # shift = Shift(employee_id=employee_id, date=shift_date, type=shift_type, ...)
    # db.session.add(shift)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Shift updated successfully'}), 200


@bp.route('/api/staff_list')
@login_required
@manager_required
def staff_list():
    staff = Employee.query.filter_by(active=True).all()
    return jsonify([
        {
            'staff_number': s.staff_number,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'role': s.role,
            'availability': s.availability
        } for s in staff
    ])