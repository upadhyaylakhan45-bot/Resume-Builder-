from flask import Blueprint, render_template
from flask_login import current_user

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html", logged_in=True)
    return render_template("index.html", logged_in=False)


@main_bp.route("/templates-gallery")
def templates_gallery():
    templates = [
        {
            "id": "professional",
            "name": "Professional",
            "desc": "Classic layout with clear hierarchy — ideal for most roles.",
            "type": "Both",
        },
        {
            "id": "modern",
            "name": "Modern",
            "desc": "Bold sidebar accent and contemporary spacing.",
            "type": "Both",
        },
        {
            "id": "simple",
            "name": "Simple",
            "desc": "Minimal and clean — ATS-friendly single column.",
            "type": "Both",
        },
        {
            "id": "fresher",
            "name": "Fresher Focus",
            "desc": "Highlights projects, skills, and education for new grads.",
            "type": "Fresher",
        },
        {
            "id": "executive",
            "name": "Executive",
            "desc": "Experience-first layout for senior and experienced profiles.",
            "type": "Experienced",
        },
    ]
    return render_template("templates_gallery.html", templates=templates)
