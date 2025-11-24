from app.extensions import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False)
    hire_date = db.Column(db.String(20))
    availability = db.Column(db.String(20), default='available')
    profile_image = db.Column(db.String(255), default='default.jpg')
    staff_number = db.Column(db.String(50), unique=True, nullable=False, default='TEMPSTAFF')
    specialization = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    theme = db.Column(db.String(20), default='light')

    # Relationships
    created_items = db.relationship('InventoryItem', backref=db.backref('creator', lazy='select'), lazy='select')
    updated_items = db.relationship('InventoryItem', backref=db.backref('updater', lazy='select'), lazy='select')
    helped_patients = db.relationship('HelpedPatient', backref=db.backref('nurse', lazy='select'), lazy='select')
    appointments = db.relationship('Appointment', backref=db.backref('helper', lazy='select'), lazy='select')
    prescriptions = db.relationship('Prescription', backref=db.backref('nurse', lazy='select'), lazy='select')
    shifts = db.relationship('Shift', backref=db.backref('employee', lazy='select'), lazy='select')
    tasks = db.relationship('Task', backref=db.backref('assigned_employee', lazy='select'), lazy='select')

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} ({self.role})>"
