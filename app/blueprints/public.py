# app/blueprints/public.py
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from app.extensions import db
from app.models.employee import Employee
from app.models.appointment import Appointment
from datetime import datetime

bp = Blueprint('public', __name__, template_folder='../templates/homepage')

# === FORMS ===
class BookAppointmentForm(FlaskForm):
    patient_name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    patient_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    patient_email = StringField('Email', validators=[Email(), Length(max=100)])
    date = DateTimeField('Preferred Date & Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    reason = TextAreaField('Reason for Visit', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Book Appointment')


# === ROUTES ===
@bp.route('/')
def home():
    return render_template('/defaultPage.html')

@bp.route('/about')
def about():
    return render_template('/about.html')

@bp.route('/contact')
def contact():
    return render_template('/contact.html')

@bp.route('/services/consultations')
def consultation_homepage():
    return render_template('/consultations.html')

@bp.route('/emergency')
def emergency_homepage():
    return render_template('/emergency.html')

@bp.route('/services/vaccinations')
def vaccinations_homepage():
    return render_template('/vaccinations.html')

@bp.route('/book-appointment', methods=['GET', 'POST'])
def patient_book_appointment():
    form = BookAppointmentForm()
    doctors = Employee.query.filter_by(role='doctor', active=True).all()
    success_data = None

    if form.validate_on_submit():
        try:
            appt = Appointment(
                patient_name=form.patient_name.data,
                patient_phone=form.patient_phone.data,
                patient_email=form.patient_email.data or None,
                appointment_date=form.date.data,
                reason=form.reason.data,
                status='pending',
                created_at=datetime.utcnow()
            )
            db.session.add(appt)
            db.session.commit()

            success_data = {
                'date': form.date.data.strftime('%d %B %Y at %H:%M'),
                'doctor': 'Assigned Soon'
            }
            flash('Appointment booked successfully! We will confirm soon.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error booking appointment. Please try again.', 'error')

    return render_template('book_appointment.html', 
                         form=form, 
                         doctors=doctors, 
                         success_data=success_data)

@bp.route('/login')
def login_page():
    from app.blueprints.auth import LoginForm
    form = LoginForm()
    return render_template('/homepage/login_page.html', form=form)