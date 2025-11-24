from flask import Flask, render_template
from .config import config
from .extensions import db, login_manager, migrate, bcrypt, csrf, cache
from .blueprints.auth import bp as auth_bp
from .blueprints.admin import bp as admin_bp
from .blueprints.receptionist import bp as recep_bp
from .blueprints.doctor import bp as doctor_bp
from .blueprints.nurse import bp as nurse_bp
from .blueprints.manager import bp as manager_bp
from .models import *  # All models

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in.'
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(recep_bp, url_prefix='/reception')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(nurse_bp, url_prefix='/nurse')
    app.register_blueprint(manager_bp, url_prefix='/manager')

    # Error handlers from original
    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(jinja2.exceptions.TemplateNotFound)
    def template_not_found(e):
        flash(f"Template {e.name} missing.", 'error')
        return render_template('errors/404.html'), 404

    # Jinja filters from original
    app.jinja_env.filters['nl2br'] = lambda v: Markup(v.replace('\n', '<br>\n')) if v else ''
    app.jinja_env.filters['datetime'] = lambda d, f: datetime.strptime(d, '%Y-%m-%d %H:%M:%S').strftime(f) if d else 'N/A'

    return app