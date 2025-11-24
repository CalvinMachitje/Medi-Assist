# app/models/walkin_queue.py
from app.extensions import db
from datetime import datetime

class WalkinQueue(db.Model):
    __tablename__ = 'walkin_queue'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    patient_name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, emergency
    reason = db.Column(db.Text, nullable=True)
    arrived_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # THIS WAS MISSING IN YOUR OLD MODEL
    status = db.Column(db.String(20), default='waiting')  # waiting, called, helped

    # Relationship
    patient = db.relationship('Patient', backref='walkin_entries')

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient_name,
            'priority': self.priority,
            'reason': self.reason or '',
            'arrived_at': self.arrived_at.isoformat(),
            'status': self.status
        }