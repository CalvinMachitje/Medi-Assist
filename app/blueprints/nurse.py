from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.emergency_request import EmergencyRequest
from app.models.patient import Patient
from app.models.helped_patient import HelpedPatient
from datetime import datetime
from app.extensions import db

bp = Blueprint('nurse', __name__, template_folder='../templates/nurse')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'nurse':
        flash('Access denied.', 'error')
        return redirect(url_for('auth.login'))
    emergencies = EmergencyRequest.query.order_by(EmergencyRequest.request_time.desc()).all()
    emergencies_list = [{'id': er.id, 'patient_id': er.patient_id, 'first_name': p.first_name, 'last_name': p.last_name, 'reason': er.reason, 'request_time': er.request_time, 'status': er.status} for er in emergencies for p in [Patient.query.get(er.patient_id)] if p]
    return render_template('dashboard.html', emergency_requests=emergencies_list)

@bp.route('/toggle_availability', methods=['POST'])
@login_required
def toggle_availability():
    new_status = request.form.get('status')
    if new_status in ['available', 'unavailable']:
        current_user.availability = new_status
        db.session.commit()
        notification = f"{current_user.first_name} {current_user.last_name} ({current_user.role}) is now {new_status}."
        # Add to messages or notifications
        flash(f'Availability set to {new_status}.', 'success')
    return jsonify({'success': True, 'message': f'Availability set to {new_status}.'})

@bp.route('/emergency_request', methods=['POST'])
@login_required
def emergency_request():
    patient_id = request.form.get('patient_id')
    reason = request.form.get('reason')
    if patient_id and reason:
        er = EmergencyRequest(patient_id=patient_id, reason=reason, status='pending')
        db.session.add(er)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Emergency submitted!'})
    return jsonify({'success': False, 'message': 'Missing fields.'}), 400

@bp.route('/update_emergency_request/<int:request_id>', methods=['POST'])
@login_required
def update_emergency_request(request_id):
    status = request.form.get('status')
    er = EmergencyRequest.query.get(request_id)
    if er and status in ['pending', 'in_progress', 'resolved']:
        er.status = status
        db.session.commit()
        return jsonify({'success': True, 'message': f'Status updated to {status}.'})
    return jsonify({'success': False, 'message': 'Not found.'}), 404