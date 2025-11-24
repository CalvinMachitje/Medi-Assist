from app.extensions import db

class Shift(db.Model):
    __tablename__ = 'staff_schedule'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    shift_date = db.Column(db.Date, nullable=False)
    shift_type = db.Column(db.String(20), nullable=False)  # morning, afternoon, night
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, absent
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship
    employee = db.relationship('Employee', backref=db.backref('shifts', lazy='select'))

    def __repr__(self):
        return f"<Shift {self.employee_id} - {self.shift_date} ({self.shift_type})>"
