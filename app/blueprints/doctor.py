# app/blueprints/doctor.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.extensions import db
from app.models.patient import Patient
from app.models.prescription import Prescription
from app.models.appointment import Appointment
from app.models.emergency_request import EmergencyRequest
from app.models.announcement import Announcement
from datetime import datetime, date
from functools import wraps

bp = Blueprint('doctor', __name__, template_folder='../templates/doctor')

def doctor_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'doctor':
            flash('Access denied. This area is for doctors only.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# 1. DOCTOR DASHBOARD
@bp.route('/dashboard')
@doctor_required
def doctor_dashboard():
    today = date.today()
    appointments_today = db.session.query(Appointment, Patient)\
        .join(Patient, Appointment.patient_id == Patient.id)\
        .filter(
            Appointment.doctor_id == current_user.id,
            db.func.date(Appointment.appointment_date) == today
        ).all()

    patients_today = []
    for appt, patient in appointments_today:
        patients_today.append({
            'patient_id': patient.id,
            'patient_name': f"{patient.first_name} {patient.last_name}",
            'appointment_time': appt.appointment_date.strftime('%H:%M') if appt.appointment_date else 'TBD',
            'reason': appt.reason or 'General Consultation'
        })

    return render_template(
        'doctor_dashboard.html',
        patients_today=patients_today,
        patients=Patient.query.all(),
        total_patients=Patient.query.count(),
        chronic_patients=Patient.query.filter(Patient.medical_history.ilike('%chronic%')).count(),
        now=datetime.now()
    )


# 2. EMERGENCY CENTER
@bp.route('/emergency')
@doctor_required
def emergency_center():
    requests = EmergencyRequest.query.filter_by(status='pending')\
        .order_by(EmergencyRequest.priority.desc(), EmergencyRequest.requested_at.desc()).all()
    return render_template('emergency.html', emergency_requests=requests)


# 3. MARK EMERGENCY AS RESPONDED (AJAX)
@bp.route('/mark_emergency_responded', methods=['POST'])
@doctor_required
def mark_emergency_responded():
    data = request.get_json()
    if not data or 'emergency_id' not in data:
        return jsonify(success=False, message='Invalid request'), 400
    
    req = EmergencyRequest.query.get(data['emergency_id'])
    if req and req.status == 'pending':
        req.status = 'responded'
        req.responded_by = current_user.id
        req.responded_at = datetime.utcnow()
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


# 4. VIEW PATIENT PROFILE
@bp.route('/view_patient/<int:patient_id>')
@doctor_required
def view_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    prescriptions = Prescription.query.filter_by(patient_id=patient_id)\
        .order_by(Prescription.prescribed_date.desc()).all()
    return render_template('view_patient.html', patient=patient, prescriptions=prescriptions)


# 5. WRITE NEW PRESCRIPTION
@bp.route('/prescription/<int:patient_id>', methods=['GET', 'POST'])
@doctor_required
def prescription_page(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        medication = request.form.get('medication', '').strip()
        instructions = request.form.get('instructions', '').strip()
        
        if not medication or not instructions:
            flash('Both medication and instructions are required.', 'error')
        else:
            prescription = Prescription(
                patient_id=patient_id,
                doctor_id=current_user.id,
                medication_name=medication,
                dosage=instructions,
                prescribed_date=datetime.utcnow()
            )
            db.session.add(prescription)
            db.session.commit()
            flash('Prescription created successfully!', 'success')
            return redirect(url_for('doctor.view_patient', patient_id=patient_id))
    
    return render_template('prescription_page.html', patient=patient)


# 6. PRINT PRESCRIPTION (Print-Friendly Page)
@bp.route('/print_prescription/<int:prescription_id>')
@doctor_required
def print_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    if prescription.doctor_id != current_user.id:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('doctor.doctor_dashboard'))
    return render_template('print_prescription.html', presc=prescription)


# 7. DOCTOR REPORT (NEW PAGE)
@bp.route('/report')
@doctor_required
def doctor_report():
    reports = db.session.query(Appointment, Patient)\
        .join(Patient).filter(Appointment.doctor_id == current_user.id)\
        .order_by(Appointment.appointment_date.desc()).limit(50).all()
    
    formatted_reports = []
    for appt, patient in reports:
        formatted_reports.append({
            'patient_name': f"{patient.first_name} {patient.last_name}",
            'appointment_date': appt.appointment_date.strftime('%Y-%m-%d %H:%M') if appt.appointment_date else 'N/A',
            'status': appt.status,
            'reason': appt.reason or 'Not specified'
        })
    
    return render_template('doctor_report.html', reports=formatted_reports)


# 8. VIEW ANNOUNCEMENTS (NEW PAGE)
@bp.route('/view_announcements')
@doctor_required
def doctor_view_announcements():
    announcements = Announcement.query.filter(
        Announcement.target_role.in_(['all', 'doctor'])
    ).order_by(Announcement.pinned.desc(), Announcement.timestamp.desc()).all()
    
    return render_template('doctor_view_announcements.html', announcements=announcements)


# 9. ALL APPOINTMENTS LIST (NEW PAGE)
@bp.route('/appointments')
@doctor_required
def doctor_appointments():
    appointments = db.session.query(Appointment, Patient)\
        .join(Patient).filter(Appointment.doctor_id == current_user.id)\
        .order_by(Appointment.appointment_date.desc()).all()
    
    formatted = []
    for appt, patient in appointments:
        formatted.append({
            'id': appt.id,
            'patient_name': f"{patient.first_name} {patient.last_name}",
            '-patient_id': patient.id,
            'appointment_date': appt.appointment_date,
            'status': appt.status.capitalize(),
            'reason': appt.reason or 'General'
        })
    
    return render_template('doctor_appointments.html', appointments=formatted)