from app.extensions import db
from datetime import datetime

class WalkinQueue(db.Model):
    __tablename__ = 'walkin_queue'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default='medium')
    reason = db.Column(db.Text)
    arrived_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    status = db.Column(db.String(20), default='waiting')

    patient = db.relationship('Patient', backref=db.backref('walkin_entries', lazy='select'))

    def __repr__(self):
        return f"<Walkin {self.patient_name}>"
