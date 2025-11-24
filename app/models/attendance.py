from app.extensions import db

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.String(20))
    status = db.Column(db.String(20))  # e.g., present, absent, late

    staff_member = db.relationship('Employee', backref='attendance_records')

    def __repr__(self):
        return f"<Attendance {self.staff_id} - {self.date} ({self.status})>"
