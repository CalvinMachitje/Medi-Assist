from app.extensions import db
from datetime import datetime

class HelpedPatient(db.Model):
    __tablename__ = 'helped_patients'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    appointment_date = db.Column(db.String(50))
    helped_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)

    nurse = db.relationship('Employee', backref='helped_patients', lazy=True)

    def __repr__(self):
        return f"<Helped {self.id}>"