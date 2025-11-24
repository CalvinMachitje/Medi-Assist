# app/blueprints/admin.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_login import login_required, current_user
from app.extensions import db
from app.models.employee import Employee
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.announcement import Announcement
from app.models.system_setting import SystemSetting
from datetime import datetime, date
from sqlalchemy import func, extract
import json

bp = Blueprint('admin', __name__, template_folder='../templates/admin')

def admin_required(f):
    from functools import wraps
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Admin access only.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# =============================================
# 1. ADMIN DASHBOARD
# =============================================
@bp.route('/dashboard')
@admin_required
def admin_dashboard():
    total_users = Employee.query.count() + Patient.query.count()
    active_staff = Employee.query.filter(Employee.availability == 'available').count()
    system_alerts = 0  # You can expand this later

    uptime_days = 42  # Placeholder
    uptime_hours = 10
    db_status = "Healthy"
    recent_login_count = 28
    last_backup_time = "2 hours ago"
    security_warnings = 0

    return render_template('admin_dashboard.html',
                           total_users=total_users,
                           active_staff=active_staff,
                           system_alerts=system_alerts,
                           uptime_days=uptime_days,
                           uptime_hours=uptime_hours,
                           db_status=db_status,
                           recent_login_count=recent_login_count,
                           last_backup_time=last_backup_time,
                           security_warnings=security_warnings)


# =============================================
# 2. ADMIN REPORT WITH CHARTS
# =============================================
@bp.route('/report')
@admin_required
def admin_report():
    # Counts
    total_users = Employee.query.count() + Patient.query.count()
    total_doctors = Employee.query.filter_by(role='doctor').count()
    total_nurses = Employee.query.filter_by(role='nurse').count()
    total_receptionists = Employee.query.filter_by(role='receptionist').count()
    total_patients = Patient.query.count()

    # Appointments
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly_appointments_total = Appointment.query.filter(
        extract('month', Appointment.appointment_date) == current_month,
        extract('year', Appointment.appointment_date) == current_year
    ).count()

    pending_appointments = Appointment.query.filter_by(status='scheduled').count()
    completed_appointments = Appointment.query.filter_by(status='helped').count()
    missed_appointments = Appointment.query.filter_by(status='missed').count()
    monthly_revenue = 125000  # Placeholder

    # Chart Data
    staff_pie_data = {
        'labels': ['Doctors', 'Nurses', 'Receptionists', 'Managers'],
        'data': [total_doctors, total_nurses, total_receptionists, Employee.query.filter_by(role='manager').count()]
    }

    appointment_bar_data = {
        'labels': ['Pending', 'Completed', 'Missed'],
        'data': [pending_appointments, completed_appointments, missed_appointments]
    }

    # Monthly trend (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        month = (current_month - i - 1) % 12 + 1
        year = current_year if (current_month - i) > 0 else current_year - 1
        count = Appointment.query.filter(
            extract('month', Appointment.appointment_date) == month,
            extract('year', Appointment.appointment_date) == year
        ).count()
        monthly_data.append(count)

    return render_template('admin_report.html',
                           total_users=total_users,
                           total_doctors=total_doctors,
                           total_nurses=total_nurses,
                           total_receptionists=total_receptionists,
                           total_patients=total_patients,
                           monthly_appointments_total=monthly_appointments_total,
                           pending_appointments=pending_appointments,
                           completed_appointments=completed_appointments,
                           missed_appointments=missed_appointments,
                           monthly_revenue=monthly_revenue,
                           staff_pie_data_json=json.dumps(staff_pie_data),
                           appointment_bar_data_json=json.dumps(appointment_bar_data),
                           monthly_appointments_data_json=json.dumps({
                               'labels': ['6mo ago', '5mo ago', '4mo ago', '3mo ago', '2mo ago', 'This month'],
                               'data': monthly_data
                           }))


# =============================================
# 3. MANAGE ANNOUNCEMENTS
# =============================================
@bp.route('/announcements', methods=['GET', 'POST'])
@admin_required
def admin_announcements():
    if request.method == 'POST':
        announcement = Announcement(
            title=request.form['title'],
            message=request.form['message'],
            category=request.form['category'],
            author=f"{current_user.first_name} {current_user.last_name}",
            target_role=request.form['target_role'],
            pinned='pinned' in request.form,
            timestamp=datetime.utcnow()
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created!', 'success')

    announcements = Announcement.query.order_by(
        Announcement.pinned.desc(), Announcement.timestamp.desc()
    ).all()

    return render_template('admin_announcements.html', announcements=announcements)


# =============================================
# 4. MANAGE USERS
# =============================================
@bp.route('/manage_users')
@admin_required
def manage_users():
    employees = Employee.query.filter(Employee.role != 'admin').all()
    return render_template('manage_users.html', employees=employees)


# =============================================
# 5. SYSTEM SETTINGS
# =============================================
@bp.route('/system_settings', methods=['GET', 'POST'])
@admin_required
def system_settings():
    settings = SystemSetting.query.first() or SystemSetting()

    if request.method == 'POST':
        settings.clinic_name = request.form.get('clinic_name', 'Township Clinic')
        settings.clinic_address = request.form.get('clinic_address', '')
        settings.clinic_contact = request.form.get('clinic_contact', '')
        settings.clinic_logo = request.form.get('clinic_logo', '')
        settings.branding_color = request.form.get('branding_color', '#000000')
        settings.operating_hours = request.form.get('operating_hours', '9:00 AM - 5:00 PM')
        settings.holiday_calendar = request.form.get('holiday_calendar', '')

        db.session.add(settings)
        db.session.commit()
        flash('Settings saved!', 'success')

    return render_template('system_settings.html', system_settings=settings.__dict__)

@bp.route('/system')
@login_required
def system_guides():
    return render_template('system_guides.html')

@bp.route('/staff-counseling')
@login_required
def staff_counseling():
    return render_template('staff_counseling.html')
# Register in __init__.py
# from app.blueprints.admin import bp as admin_bp
# app.register_blueprint(admin_bp, url_prefix='/admin')