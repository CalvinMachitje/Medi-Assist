from app.extensions import db
from datetime import datetime
from app.models.appointment import Appointment

class SelfBookedAppointment(db.Model):
    __tablename__ = 'self_booked_appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(200), nullable=False)
    patient_phone = db.Column(db.String(20))
    patient_email = db.Column(db.String(120))
    appointment_date = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.Text)
    doctor_staff_number = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self): return f"<SelfBook {self.patient_name}>"
