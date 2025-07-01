from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  # Nama tabel sesuai dengan NestJS

    uuid = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    face_embedding = db.Column(db.Text, nullable=True)
    role = db.Column(db.String(50), nullable=False, default='teacher')
    photo_url = db.Column(db.String(255), nullable=True)

    # Relasi dengan Attendance
    attendances = db.relationship('Attendance', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.uuid} - {self.username}>"
