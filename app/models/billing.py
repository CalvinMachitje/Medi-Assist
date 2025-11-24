from app.extensions import db
from datetime import datetime

class Billing(db.Model):
    __tablename__ = 'billing'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    cost = db.Column(db.Float, default=0.0)
    billing_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

    # Relationships
    patient = db.relationship('Patient', backref=db.backref('billings', lazy='select'))
    appointment = db.relationship('Appointment', backref=db.backref('billing', lazy='select'))

    def __repr__(self):
        return f"<Billing {self.id} - {self.status}>"
