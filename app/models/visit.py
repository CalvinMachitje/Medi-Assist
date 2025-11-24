from app.extensions import db

class Visit(db.Model):
    __tablename__ = 'visits'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    visit_time = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)

    # Relationship
    patient = db.relationship('Patient', backref=db.backref('visits', lazy='select'))

    def __repr__(self):
        return f"<Visit {self.id}>"
