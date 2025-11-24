from app.extensions import db

class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    date = db.Column(db.String(20))
    enrolled = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<TrainingSession {self.title}>"
