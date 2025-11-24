from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, TextAreaField, DateField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('doctor', 'Doctor'), ('nurse', 'Nurse'), ('receptionist', 'Receptionist')], validators=[DataRequired()])
    terms = BooleanField('I accept terms', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_role(self, field):
        if field.data not in ['admin', 'doctor', 'nurse', 'receptionist']:
            raise ValidationError('Invalid role.')

class AppointmentForm(FlaskForm):
    patient_name = StringField('Patient Name', validators=[DataRequired(), Length(min=2, max=100)])
    patient_phone = StringField('Phone Number', validators=[Length(max=15)])
    patient_email = EmailField('Email', validators=[Email()])
    date = DateTimeField('Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    reason = StringField('Reason', validators=[Length(max=500)])
    submit = SubmitField('Book Appointment')

class SearchForm(FlaskForm):
    search_term = StringField('Search Term', validators=[DataRequired()])
    submit = SubmitField('Search')

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[('', 'Choose'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = StringField('Address')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Email()])
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    medical_history = TextAreaField('Medical History')
    allergies = TextAreaField('Allergies')
    current_medications = TextAreaField('Current Medications')
    submit = SubmitField('Register Patient')

class PatientBookAppointmentForm(FlaskForm):
    patient_name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    patient_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    patient_email = EmailField('Email', validators=[DataRequired(), Email()])
    date = DateTimeField('Date & Time', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    reason = TextAreaField('Reason', validators=[Length(max=500)])
    submit = SubmitField('Book Appointment')