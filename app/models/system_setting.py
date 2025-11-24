from app.extensions import db

class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    backup_frequency = db.Column(db.String(50))

    def __repr__(self):
        return f"<Setting {self.backup_frequency}>"