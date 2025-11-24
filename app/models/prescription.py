from app.extensions import db

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    nurse_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    medication_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    prescribed_date = db.Column(db.String(20), nullable=False)

    nurse = db.relationship('Employee', backref='prescriptions', lazy=True)

    def __repr__(self):
        return f"<Prescription {self.medication_name}>"