from app.extensions import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    reason = db.Column(db.Text)
    created_by_role = db.Column(db.String(20), default='receptionist')
    helper_id = db.Column(db.String(50))  # staff_number

    # Relationship from original
    helper = db.relationship('Employee', foreign_keys=[helper_id],
                             primaryjoin="Appointment.helper_id == Employee.staff_number",
                             backref='assigned_appointments', lazy=True)

    def __repr__(self):
        return f"<Appointment {self.id} - {self.status}>"