from app.extensions import db

class WalkinQueue(db.Model):
    __tablename__ = 'walkin_queue'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), nullable=False)
    patient_name = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text)
    arrived_at = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Walkin {self.patient_name}>"