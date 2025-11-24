from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.walkin_queue import WalkinQueue
from app.forms.patient import PatientForm, SearchForm
from app.extensions import db
from app.forms.appointment import AppointmentForm
from datetime import datetime

bp = Blueprint('receptionist', __name__, template_folder='../templates/receptionist')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'receptionist':
        flash('Access denied.', 'error')
        return redirect(url_for('auth.login'))
    appointments = Appointment.query.filter_by(status='scheduled').all()
    walkins = WalkinQueue.query.all()
    return render_template('dashboard.html', appointments=appointments, walkins=walkins)

@bp.route('/search_patient', methods=['GET', 'POST'])
@login_required
def search_patient():
    form = SearchForm()
    patients = []
    if form.validate_on_submit():
        search_term = form.search_term.data.strip()
        patients = Patient.query.filter(Patient.first_name.ilike(f'%{search_term}%') | Patient.last_name.ilike(f'%{search_term}%') | Patient.id.ilike(f'%{search_term}%')).order_by(Patient.id.desc()).all()
    return render_template('search_patient.html', form=form, patients=patients)

@bp.route('/add_patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data.strftime('%Y-%m-%d'),
            gender=form.gender.data,
            address=form.address.data,
            phone=form.phone.data,
            email=form.email.data,
            emergency_contact_name=form.emergency_contact_name.data,
            emergency_contact_phone=form.emergency_contact_phone.data,
            medical_history=form.medical_history.data,
            allergies=form.allergies.data,
            current_medications=form.current_medications.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registered!', 'success')
        return redirect(url_for('receptionist.search_patient'))
    return render_template('patient_registration.html', form=form)

@bp.route('/add_walkin', methods=['GET'])
@login_required
def add_walkin():
    # From original add_walkin
    patient_id = request.args.get('patient_id')
    patient = Patient.query.get(patient_id)
    if not patient:
        flash('Patient not found.', 'error')
        return redirect(url_for('receptionist.search_patient'))
    # Add to queue logic
    walkin = WalkinQueue(patient_id=patient.id, patient_name=f"{patient.first_name} {patient.last_name}", priority='medium', reason='Walk-in', arrived_at=datetime.now().strftime('%Y-%m-%d %H:%M'))
    db.session.add(walkin)
    db.session.commit()
    flash('Walk-in added!', 'success')
    return redirect(url_for('receptionist.dashboard'))

@bp.route('/cancel_appointment', methods=['POST'])
@login_required
def cancel_appointment():
    appointment_id = request.form.get('appointment_id')
    appt = Appointment.query.get(appointment_id)
    if appt:
        appt.status = 'cancelled'
        db.session.commit()
        flash('Appointment cancelled.', 'success')
    else:
        flash('Appointment not found.', 'error')
    return redirect(url_for('receptionist.dashboard'))

@bp.route('/assign_staff', methods=['POST'])
@login_required
def assign_staff():
    # From original assign_staff
    appointment_id = request.form.get('appointment_id')
    staff_id = request.form.get('staff_id')
    appt = Appointment.query.get(appointment_id)
    if appt:
        appt.helper_id = staff_id
        appt.status = 'assigned'
        db.session.commit()
        flash('Staff assigned.', 'success')
    return redirect(url_for('receptionist.dashboard'))

@bp.route('/reschedule_appointment', methods=['POST'])
@login_required
def reschedule_appointment():
    # From original reschedule
    appointment_id = request.form.get('appointment_id')
    new_time = request.form.get('new_time')
    appt = Appointment.query.get(appointment_id)
    if appt and appt.status == 'scheduled':
        appt.appointment_date = new_time
        appt.status = 'scheduled'
        db.session.commit()
        flash('Rescheduled!', 'success')
    return redirect(url_for('receptionist.dashboard'))