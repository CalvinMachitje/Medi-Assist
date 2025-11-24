# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# THIS IS THE MISSING LINE — ADD IT!
@login_manager.user_loader
def load_user(user_id):
    from app.models.employee import Employee
    return Employee.query.get(int(user_id))

# Optional: nice login message + redirect
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'