import os

from flask import Flask, render_template

from config import Config
from extensions import csrf, db, login_manager
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.main import main_bp
from routes.resume import resume_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Ensure SQLite path uses instance folder
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///"):
        db_path = os.path.join(app.instance_path, "resume_forge.db")
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    with app.app_context():
        from models import Resume, User  # noqa: F401

        db.create_all()
        _ensure_admin()

    return app


def _ensure_admin():
    from models import User

    admin_email = os.environ.get("ADMIN_EMAIL", "admin@resumeforge.local")
    admin_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        admin = User(name="Admin", email=admin_email, is_admin=True)
        admin.set_password(admin_pass)
        db.session.add(admin)
        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
