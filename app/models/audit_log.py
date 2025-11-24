from app.extensions import db

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text, nullable=False)
    performed_by = db.Column(db.String(50), nullable=False)
    target_user = db.Column(db.String(50))
    details = db.Column(db.Text)
    timestamp = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Audit {self.action}>"