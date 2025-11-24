from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user
from app.models.appointment import Appointment
from app.models.patient import Patient
from datetime import datetime, timedelta
from app.extensions import db

bp = Blueprint('doctor', __name__, template_folder='../templates/doctor')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'doctor':
        flash('Access denied.', 'error')
        return redirect(url_for('auth.login'))
    employee_id = current_user.id
    reports = db.session.query(Appointment, Patient).join(Patient).filter(Appointment.helper_id == current_user.staff_number, Appointment.appointment_date >= (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')).order_by(Appointment.appointment_date.desc()).all()
    reports_list = [{'id': a.id, 'patient_name': f"{p.first_name} {p.last_name}", 'appointment_date': a.appointment_date, 'status': a.status, 'reason': a.reason or 'N/A'} for a, p in reports]
    return render_template('dashboard.html', reports=reports_list)

@bp.route('/doctor_report')
@login_required
def doctor_report():
    # From original doctor_report
    employee_id = current_user.id
    reports = db.session.query(Appointment, Patient).join(Patient).filter(Appointment.helper_id == current_user.staff_number, Appointment.appointment_date >= (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')).order_by(Appointment.appointment_date.desc()).all()
    reports_list = [{'id': a.id, 'patient_name': f"{p.first_name} {p.last_name}", 'appointment_date': a.appointment_date, 'status': a.status, 'reason': a.reason or 'N/A'} for a, p in reports]
    return render_template('doctor_report.html', reports=reports_list)