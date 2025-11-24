from app.extensions import db

class PerformanceReview(db.Model):
    __tablename__ = 'performance_reviews'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    name = db.Column(db.String(200))
    role = db.Column(db.String(100))
    score = db.Column(db.Integer)
    last_review = db.Column(db.String(20))

    staff_member = db.relationship('Employee', backref='performance_reviews')

    def __repr__(self):
        return f"<PerformanceReview {self.name} - {self.score}>"
