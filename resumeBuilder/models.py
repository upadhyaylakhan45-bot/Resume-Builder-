from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship(
        "Resume", backref="owner", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(160), default="My Resume")
    experience_type = db.Column(db.String(20), default="fresher")  # fresher | experienced
    template = db.Column(db.String(40), default="professional")
    font_family = db.Column(db.String(60), default="Georgia")
    accent_color = db.Column(db.String(20), default="#0F4C5C")

    # Personal
    full_name = db.Column(db.String(120), default="")
    email = db.Column(db.String(180), default="")
    phone = db.Column(db.String(40), default="")
    location = db.Column(db.String(120), default="")
    linkedin = db.Column(db.String(200), default="")
    github = db.Column(db.String(200), default="")
    website = db.Column(db.String(200), default="")
    summary = db.Column(db.Text, default="")

    # JSON-ish text fields (stored as text for simplicity)
    skills = db.Column(db.Text, default="")  # comma-separated
    education = db.Column(db.Text, default="")  # JSON string
    projects = db.Column(db.Text, default="")  # JSON string
    certifications = db.Column(db.Text, default="")  # JSON string
    experience = db.Column(db.Text, default="")  # JSON string (internships / jobs)
    achievements = db.Column(db.Text, default="")  # JSON string
    extracurricular = db.Column(db.Text, default="")  # JSON string
    hobbies = db.Column(db.Text, default="")  # comma-separated

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
