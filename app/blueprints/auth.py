from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db, bcrypt
from app.models.employee import Employee
from app.models.audit_log import AuditLog
from app.forms.auth import LoginForm
from functools import wraps
from datetime import datetime
import random, string

bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username_input = form.username.data.strip()
        password = form.password.data
        remember = form.remember.data

        user = Employee.query.filter_by(email=username_input).first() or Employee.query.filter_by(staff_number=username_input).first()
        if user and user.active and user.check_password(password):
            login_user(user, remember=remember)
            session.clear()
            session.permanent = True
            session['user_id'] = user.staff_number
            session['staff_number'] = user.staff_number
            session['username'] = f"{user.first_name} {user.last_name}"
            session['role'] = user.role
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S SAST')
            session['profile_image'] = user.profile_image or 'default.jpg'

            flash('Login successful!', 'success')
            role = user.role.lower()
            redirect_map = {
                'receptionist': 'receptionist.dashboard',
                'admin': 'admin.dashboard',
                'doctor': 'doctor.dashboard',
                'nurse': 'nurse.dashboard',
                'manager': 'manager.dashboard'
            }
            endpoint = redirect_map.get(role)
            if endpoint:
                return redirect(url_for(endpoint))
        flash('Invalid username, password, or account inactive.', 'error')

    return render_template('login_page.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    # From original logout logic
    if current_user.role in ['doctor', 'nurse']:
        current_user.availability = 'unavailable'
        db.session.commit()
    logout_user()
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/create_user', methods=['POST'])
def create_user():
    # From original create_user route (admin only)
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    # CSRF check from original
    if not request.form.get('csrf_token'):
        return jsonify({'success': False, 'message': 'CSRF missing'}), 403

    data = request.form
    first_name = data.get('first_name').strip()
    last_name = data.get('last_name').strip()
    email = data.get('email').strip().lower()
    role = data.get('role')

    if not all([first_name, last_name, email, role]):
        return jsonify({'success': False, 'message': 'All fields required'}), 400

    valid_roles = ['doctor', 'nurse', 'receptionist', 'manager']
    if role not in valid_roles:
        return jsonify({'success': False, 'message': 'Invalid role'}), 400

    user = Employee.query.filter_by(email=email).first()
    if user:
        return jsonify({'success': False, 'message': 'Email in use'}), 400

    # Generate staff number from original
    max_num = db.session.query(db.func.max(db.func.cast(db.func.substr(Employee.staff_number, 6), db.Integer))).scalar() or 0
    staff_number = f"STAFF{str(max_num + 1).zfill(3)}"

    temp_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    hashed_password = bcrypt.generate_password_hash(temp_password).decode('utf-8')

    new_user = Employee(staff_number=staff_number, first_name=first_name, last_name=last_name, email=email, password_hash=hashed_password, role=role, active=True)
    db.session.add(new_user)
    db.session.commit()

    # Audit log from original
    audit = AuditLog(action='create_user', performed_by=session['username'], target_user=staff_number, details=f"Created {role}: {temp_password}", timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db.session.add(audit)
    db.session.commit()

    return jsonify({'success': True, 'staff_number': staff_number, 'temp_password': temp_password, 'message': f'{role.capitalize()} created! Password: {temp_password}'})

@bp.route('/delete_user', methods=['POST'])
def delete_user():
    # From original delete_user
    if session.get('role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    user_id = request.form.get('user_id')
    reason = request.form.get('reason')

    user = Employee.query.get(user_id)
    if not user or user.role == 'admin':
        return jsonify({'success': False, 'message': 'Cannot delete'}), 403

    db.session.delete(user)
    db.session.commit()

    audit = AuditLog(action='delete_user', performed_by=session['username'], target_user=user.staff_number, details=reason, timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    db.session.add(audit)
    db.session.commit()

    return jsonify({'success': True, 'message': 'User deleted'})