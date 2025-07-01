from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Attendance(db.Model):
    __tablename__ = 'attendances'  # Nama tabel sesuai dengan NestJS

    uuid = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    cctv_schedule_id = db.Column(db.String(36), db.ForeignKey('cctv_schedules.uuid'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.uuid'), nullable=False)
    check_in = db.Column(db.Time, nullable=False)
    check_out = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(50), nullable=False)

    # Relasi ke CCTVSchedule dan User
    cctv_schedule = db.relationship('CCTVSchedule', backref=db.backref('attendances', lazy=True))
    user = db.relationship('User', backref=db.backref('attendances', lazy=True))

    def __repr__(self):
        return f"<Attendance {self.uuid} - {self.user_id}>"
