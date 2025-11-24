# app/models/shift.py
from app.extensions import db

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    date = db.Column(db.String(20))
    type = db.Column(db.String(20))  # morning, night, off