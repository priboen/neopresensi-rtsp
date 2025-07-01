from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class CCTVSchedule(db.Model):
    __tablename__ = 'cctv_schedules'  # Nama tabel sesuai dengan NestJS

    uuid = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    cctv_id = db.Column(db.String(36), db.ForeignKey('cctv_configs.uuid'), nullable=False)
    day = db.Column(db.String(50), nullable=False, unique=True)
    check_in_time = db.Column(db.Time, nullable=False)
    check_out_time = db.Column(db.Time, nullable=False)

    # Relasi ke CCTVConfig
    cctv_config = db.relationship('CCTVConfig', backref=db.backref('schedules', lazy=True))

    # Relasi ke Attendance
    attendances = db.relationship('Attendance', backref='cctv_schedule', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CCTVSchedule {self.uuid} - {self.day}>"
