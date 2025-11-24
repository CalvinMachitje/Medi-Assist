# app/blueprints/nurse.py
from flask import Blueprint,session, render_template, request, flash, redirect, url_for, jsonify, Response
from flask_login import login_required, current_user
from app.extensions import db
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.helped_patient import HelpedPatient
from app.models.prescription import Prescription
from app.models.announcement import Announcement
from app.models.emergency_request import EmergencyRequest
from datetime import datetime, date
from sqlalchemy import or_, func
import time
import json
from functools import wraps

bp = Blueprint('nurse', __name__, template_folder='../templates/nurse')

def nurse_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if current_user.role != 'nurse':
            flash('Access denied. Nurse access only.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# =============================================
# 1. NURSE DASHBOARD — Matches your dashboard.html + nurseAssessPatient.html
# =============================================
@bp.route('/dashboard')
@nurse_required
def nurse_dashboard():
    today_str = date.today().strftime('%Y-%m-%d')

    # Today's appointments (assigned to this nurse or unassigned)
    appointments_query = db.session.query(Appointment, Patient)\
        .join(Patient, Appointment.patient_id == Patient.id)\
        .filter(func.date(Appointment.appointment_date) == today_str)\
        .filter(or_(Appointment.helper_id == current_user.id, Appointment.helper_id.is_(None)))\
        .filter(Appointment.status == 'scheduled')\
        .order_by(Appointment.appointment_date)

    appointments = []
    for appt, patient in appointments_query.all():
        appointments.append({
            'id': appt.id,
            'patient_id': patient.id,
            'patient_name': f"{patient.first_name} {patient.last_name}",
            'appointment_date': appt.appointment_date.strftime('%H:%M') if isinstance(appt.appointment_date, datetime) else 'N/A',
            'reason': appt.reason or 'General Checkup'
        })

    emergency_requests = EmergencyRequest.query.filter_by(status='pending').count()

    return render_template('dashboard.html',
                           appointments=appointments,
                           emergency_requests=emergency_requests,
                           todays_patients=len(appointments),
                           new_messages=0,
                           shift_start="08:00",
                           shift_end="16:00",
                           shift_hours_left="4.2",
                           user_details=current_user)


# =============================================
# 2. ASSESS PATIENT
# =============================================
@bp.route('/assess_patient/<int:patient_id>')
@nurse_required
def nurse_assess_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('nurseAssessPatient.html', patient=patient, user_details=current_user)


# =============================================
# 3. VIEW MEDICAL HISTORY
# =============================================
@bp.route('/view_medical_history/<int:patient_id>')
@nurse_required
def nurse_view_medical_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    prescriptions = Prescription.query.filter_by(patient_id=patient_id)\
        .order_by(Prescription.prescribed_date.desc()).all()
    visits = HelpedPatient.query.filter_by(patient_id=patient_id)\
        .order_by(HelpedPatient.helped_timestamp.desc()).all()
    
    return render_template('nurseViewMedicalHistory.html',
                           patient=patient,
                           prescriptions=prescriptions,
                           visits=visits,
                           user_details=current_user)


# =============================================
# 4. PRESCRIBE MEDICATION
# =============================================
@bp.route('/prescribe_medication/<int:patient_id>', methods=['GET', 'POST'])
@nurse_required
def nurse_prescribe_medication(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        try:
            prescription = Prescription(
                patient_id=patient_id,
                nurse_id=current_user.id,
                medication_name=request.form['medication_name'].strip(),
                dosage=request.form['dosage'].strip(),
                instructions=request.form.get('instructions', '').strip(),
                prescribed_date=datetime.utcnow()
            )
            db.session.add(prescription)
            db.session.commit()
            flash('Prescription saved successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error saving prescription.', 'error')
        
        return redirect(url_for('nurse.nurse_view_medical_history', patient_id=patient_id))
    
    return render_template('nursePrescribeMedication.html', patient=patient, user_details=current_user)


# =============================================
# 5. MARK AS HELPED (AJAX)
# =============================================
@bp.route('/mark_helped', methods=['POST'])
@nurse_required
def mark_helped():
    appointment_id = request.form.get('appointment_id')
    appt = Appointment.query.get(appointment_id)
    
    if not appt:
        return jsonify({'success': False, 'category': 'error', 'message': 'Appointment not found'})
    
    appt.status = 'helped'
    
    helped = HelpedPatient(
        patient_id=appt.patient_id,
        nurse_id=current_user.id,
        appointment_date=appt.appointment_date,
        reason=appt.reason,
        helped_timestamp=datetime.utcnow()
    )
    db.session.add(helped)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'category': 'success',
        'message': f"{appt.patient.first_name} marked as helped"
    })


# =============================================
# 6. VIEW ANNOUNCEMENTS
# =============================================
@bp.route('/view_announcements')
@nurse_required
def nurse_view_announcements():
    announcements = Announcement.query.filter(
        or_(Announcement.target_role == 'all', Announcement.target_role == 'nurse')
    ).order_by(Announcement.pinned.desc(), Announcement.timestamp.desc()).all()
    
    return render_template('view_announcement.html', announcements=announcements, user_details=current_user)


# =============================================
# 7. REAL-TIME STREAM (Live dashboard updates)
# =============================================
@bp.route('/stream_waiting_patients')
@nurse_required
def stream_waiting_patients():
    def generate():
        last_id = session.get('last_helped_id', 0)
        while True:
            updates = Appointment.query.filter(
                Appointment.id > last_id,
                Appointment.status == 'helped'
            ).all()
            for u in updates:
                last_id = u.id
                session['last_helped_id'] = last_id
                yield f"data: {json.dumps({'id': u.id, 'status': 'helped'})}\n\n"
            time.sleep(2)
    return Response(generate(), mimetype='text/event-stream')