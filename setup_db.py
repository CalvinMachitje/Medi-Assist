# setup_db.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

# Initialize Flask app
app = Flask(__name__)

# SQLite configuration
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///E:/my projects/Medi-Assist/medi_assist.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Import all your models here
from app.models.employee import Employee
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.prescription import Prescription
from app.models.visit import Visit
from app.models.emergency_request import EmergencyRequest
from app.models.message import Message
from app.models.system_setting import SystemSetting
from app.models.preference import Preference
from app.models.announcement import Announcement
from app.models.payment import Payment
from app.models.notification import Notification
from app.models.helped_patient import HelpedPatient
from app.models.self_booked_appointment import SelfBookedAppointment
from app.models.walkin_queue import WalkinQueue
from app.models.audit_log import AuditLog
from app.models.task import Task
from app.models.clinic_report import ClinicReport
from app.models.inventory import InventoryItem, InventoryLog
from app.models.billing import Billing
from app.models.certification import Certification
from app.models.training_session import TrainingSession
from app.models.performance_review import PerformanceReview
from app.models.leave_request import LeaveRequest
from app.models.attendance import Attendance
from app.models.shift import Shift

# Create all tables safely
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("All tables created successfully!")

