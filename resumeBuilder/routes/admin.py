from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from extensions import db
from models import Resume, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)

    return decorated


@admin_bp.route("/")
@admin_required
def dashboard():
    total_users = User.query.count()
    total_resumes = Resume.query.count()
    fresher_count = Resume.query.filter_by(experience_type="fresher").count()
    experienced_count = Resume.query.filter_by(experience_type="experienced").count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(8).all()
    template_stats = (
        db.session.query(Resume.template, db.func.count(Resume.id))
        .group_by(Resume.template)
        .all()
    )
    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_resumes=total_resumes,
        fresher_count=fresher_count,
        experienced_count=experienced_count,
        recent_users=recent_users,
        template_stats=template_stats,
    )


@admin_bp.route("/users")
@admin_required
def users():
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("admin.users"))
    if user.id == current_user.id:
        flash("You cannot change your own admin status.", "error")
        return redirect(url_for("admin.users"))
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f"Admin status updated for {user.email}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("admin.users"))
    if user.id == current_user.id:
        flash("You cannot delete your own account from admin.", "error")
        return redirect(url_for("admin.users"))
    db.session.delete(user)
    db.session.commit()
    flash("User account deleted.", "info")
    return redirect(url_for("admin.users"))
