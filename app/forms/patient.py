from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField, EmailField
from wtforms.validators import DataRequired, Email

class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    gender = SelectField('Gender', choices=[('', 'Choose'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = StringField('Address')
    phone = StringField('Phone')
    email = EmailField('Email', validators=[Email()])
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    medical_history = TextAreaField('Medical History')
    allergies = TextAreaField('Allergies')
    current_medications = TextAreaField('Current Medications')
    submit = SubmitField('Register Patient')