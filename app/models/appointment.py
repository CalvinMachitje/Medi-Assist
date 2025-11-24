from app.extensions import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    appointment_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='scheduled')
    reason = db.Column(db.Text)
    created_by_role = db.Column(db.String(20), default='receptionist')
    helper_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    # Relationships
    helper = db.relationship('Employee', backref=db.backref('appointments', lazy='select'))
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy='select'))

    def __repr__(self):
        return f"<Appointment {self.id} - {self.status}>"
