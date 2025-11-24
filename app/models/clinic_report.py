from app.extensions import db

class ClinicReport(db.Model):
    __tablename__ = 'clinic_reports'

    id = db.Column(db.Integer, primary_key=True)
    report_date = db.Column(db.Date, default=db.func.current_date())
    patients_seen = db.Column(db.Integer, default=0)
    revenue = db.Column(db.Float, default=0.0)
    expenses = db.Column(db.Float, default=0.0)
    staff_on_duty = db.Column(db.Integer, default=0)
    low_stock_items = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<ClinicReport {self.report_date}>"
