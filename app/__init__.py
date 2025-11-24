# app/__init__.py
from flask import Flask, render_template, flash
from flask_login import LoginManager
from jinja2 import TemplateNotFound
from markupsafe import Markup
import logging

# Local imports
from .config import config
from .extensions import db, login_manager, migrate, bcrypt, csrf, cache
from .blueprints.auth import bp as auth_bp
from .blueprints.admin import bp as admin_bp
from .blueprints.receptionist import bp as recep_bp
from .blueprints.doctor import bp as doctor_bp
from .blueprints.nurse import bp as nurse_bp
from .blueprints.manager import bp as manager_bp
from .blueprints.public import bp as public_bp

# Import models for Flask-Migrate & relationships
from .models.employee import Employee
from .models.patient import Patient
from .models.appointment import Appointment
from .models.prescription import Prescription
from .models.announcement import Announcement
from .models.emergency_request import EmergencyRequest
from .models.inventory import InventoryItem, InventoryLog

# app/__init__.py
def create_app(config_name='development'):
    app = Flask(__name__)
    
    if config_name == 'development':
        app.config.from_object('app.config.DevelopmentConfig')
    elif config_name == 'production':
        app.config.from_object('app.config.ProductionConfig')
    else:
        app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)

    # Register blueprints with proper prefixes
    app.register_blueprint(auth_bp)  # /login, /register, etc.
    app.register_blueprint(admin_bp)
    app.register_blueprint(recep_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(nurse_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(manager_bp)

    # Custom Jinja2 filters
    @app.template_filter('nl2br')
    def nl2br(value):
        if not value:
            return ''
        return Markup(value.replace('\n', '<br>\n'))

    @app.template_filter('datetime')
    def format_datetime(value, format='%d %B %Y %H:%M'):
        if not value:
            return 'Never'
        from datetime import datetime
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except:
                return value
        return value.strftime(format)

    @app.template_filter('currency')
    def currency_filter(amount):
        if amount is None:
            return "R0.00"
        return f"R{amount:,.2f}"

    # Global error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        flash('You do not have permission to access this page.', 'error')
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(e):
        db.session.rollback()
        logging.exception("Server Error")
        return render_template('errors/500.html'), 500

    @app.errorhandler(TemplateNotFound)
    def template_not_found(e):
        flash(f"Template missing: {e.name}", 'error')
        return render_template('errors/404.html'), 404

    # Context processor for common variables
    @app.context_processor
    def inject_user():
        from flask_login import current_user
        return dict(current_user=current_user)

    @app.context_processor
    def inject_now():
        from datetime import datetime
        return dict(now=datetime.now())

    # Log app startup
    with app.app_context():
        app.logger.info(f"Medi-Assist™ started in {config_name.upper()} mode")
        app.logger.info(f"Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')}")

    return app