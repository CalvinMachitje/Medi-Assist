from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.announcement import Announcement
from app.models.employee import Employee
from app.models.audit_log import AuditLog
from datetime import datetime
from functools import wraps

bp = Blueprint('admin', __name__, template_folder='../templates/admin')

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # From original admin_dashboard logic
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()
    users = Employee.query.filter_by(active=True).all()
    audits = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()
    return render_template('dashboard.html', announcements=announcements, users=users, audits=audits)

@bp.route('/announcements', methods=['GET', 'POST'])
@login_required
@admin_required
def announcements():
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get('message')
        category = request.form.get('category')
        target_role = request.form.get('target_role', 'all')
        pinned = request.form.get('pinned') == 'on'

        if not all([title, message, category]):
            flash('Required fields missing.', 'error')
            return redirect(url_for('admin.announcements'))

        ann = Announcement(title=title, message=message, category=category, author=current_user.username, pinned=pinned, target_role=target_role)
        db.session.add(ann)
        db.session.commit()
        flash('Announcement created!', 'success')

    anns = Announcement.query.order_by(Announcement.pinned.desc(), Announcement.timestamp.desc()).all()
    return render_template('announcement.html', announcements=anns)

@bp.route('/system_settings', methods=['GET', 'POST'])
@login_required
@admin_required
def system_settings():
    # From original system_settings
    settings = SystemSetting.query.first()
    if request.method == 'POST':
        # Save settings from form
        flash('Settings saved.', 'success')
        return redirect(url_for('admin.system_settings'))
    return render_template('systemSettings.html', system_settings=settings)