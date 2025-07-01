from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class CCTVConfig(db.Model):
    __tablename__ = 'cctv_configs'  # Nama tabel yang sama dengan di NestJS

    uuid = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    rtsp_url = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=True)

    # Relasi dengan CCTVSchedule
    cctv_schedules = db.relationship('CCTVSchedule', backref='cctv_config', lazy=True)

    def __repr__(self):
        return f"<CCTVConfig {self.uuid} - {self.name}>"