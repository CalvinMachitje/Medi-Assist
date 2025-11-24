from app.extensions import db

class Certification(db.Model):
    __tablename__ = 'certifications'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    name = db.Column(db.String(200))
    staff = db.Column(db.String(200))
    expiry = db.Column(db.String(20))
    days_left = db.Column(db.Integer)

    staff_member = db.relationship('Employee', backref='certifications')

    def __repr__(self):
        return f"<Certification {self.name} for {self.staff}>"
