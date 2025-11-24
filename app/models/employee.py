from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(20), nullable=False)
    hire_date = db.Column(db.String(20))
    availability = db.Column(db.String(20), default='available')
    profile_image = db.Column(db.String(255), default='default.jpg')
    staff_number = db.Column(db.String(50), unique=True, nullable=False, default='TEMPSTAFF')
    specialization = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships from original
    patients = db.relationship('Patient', backref='employee', lazy=True)
    appointments = db.relationship('Appointment', foreign_keys='Appointment.helper_id',
                                   primaryjoin="Employee.staff_number == Appointment.helper_id",
                                   backref='assigned_helper', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Employee {self.staff_number} - {self.role}>"