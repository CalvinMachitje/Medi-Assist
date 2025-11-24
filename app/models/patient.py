from app.extensions import db
from datetime import datetime

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    emergency_contact_name = db.Column(db.String(50))
    emergency_contact_phone = db.Column(db.String(20))
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    clinic = db.Column(db.String(50), default='Clinic A')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')

    # Relationships
    visits = db.relationship('Visit', backref=db.backref('patient', lazy='select'), lazy='select')
    appointments = db.relationship('Appointment', backref=db.backref('patient', lazy='select'), lazy='select')
    payments = db.relationship('Payment', backref=db.backref('patient', lazy='select'), lazy='select')
    prescriptions = db.relationship('Prescription', backref=db.backref('patient', lazy='select'), lazy='select')
    helped_patients = db.relationship('HelpedPatient', backref=db.backref('patient', lazy='select'), lazy='select')
    walkin_entries = db.relationship('WalkinQueue', backref=db.backref('patient', lazy='select'), lazy='select')

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"
