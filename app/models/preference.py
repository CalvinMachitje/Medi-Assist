from app.extensions import db

class Preference(db.Model):
    __tablename__ = 'preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    staff_number = db.Column(db.String(50), unique=True)
    theme = db.Column(db.String(20), default='dark')

    def __repr__(self):
        return f"<Pref {self.staff_number}>"