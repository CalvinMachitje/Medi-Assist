from app.extensions import db

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    name = db.Column(db.String(200))
    role = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')

    staff_member = db.relationship('Employee', backref='leave_requests')

    def __repr__(self):
        return f"<LeaveRequest {self.name} ({self.status})>"
