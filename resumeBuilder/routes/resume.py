from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    send_file,
    url_for,
)
from flask_login import current_user, login_required

from extensions import db
from forms import (
    EducationForm,
    ExperienceForm,
    PersonalForm,
    ProjectsForm,
    ResumeMetaForm,
    SkillsForm,
)
from models import Resume
from utils import generate_pdf, render_resume_html, resume_context

resume_bp = Blueprint("resume", __name__, url_prefix="/resume")


def _get_owned(resume_id: int) -> Resume | None:
    return Resume.query.filter_by(id=resume_id, user_id=current_user.id).first()


@resume_bp.route("/dashboard")
@login_required
def dashboard():
    resumes = (
        Resume.query.filter_by(user_id=current_user.id)
        .order_by(Resume.updated_at.desc())
        .all()
    )
    return render_template("resume/dashboard.html", resumes=resumes)


@resume_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = ResumeMetaForm()
    if form.validate_on_submit():
        resume = Resume(
            user_id=current_user.id,
            title=form.title.data.strip(),
            experience_type=form.experience_type.data,
            template=form.template.data,
            font_family=form.font_family.data,
            accent_color=form.accent_color.data,
            full_name=current_user.name,
            email=current_user.email,
        )
        db.session.add(resume)
        db.session.commit()
        flash("Resume created. Fill in your details.", "success")
        return redirect(url_for("resume.edit_personal", resume_id=resume.id))
    return render_template("resume/create.html", form=form)


@resume_bp.route("/<int:resume_id>/edit", methods=["GET", "POST"])
@login_required
def edit_meta(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    form = ResumeMetaForm(obj=resume)
    if form.validate_on_submit():
        resume.title = form.title.data.strip()
        resume.experience_type = form.experience_type.data
        resume.template = form.template.data
        resume.font_family = form.font_family.data
        resume.accent_color = form.accent_color.data
        db.session.commit()
        flash("Template & style saved.", "success")
        return redirect(url_for("resume.preview", resume_id=resume.id))
    return render_template("resume/edit_meta.html", form=form, resume=resume)


@resume_bp.route("/<int:resume_id>/personal", methods=["GET", "POST"])
@login_required
def edit_personal(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    form = PersonalForm(obj=resume)
    if form.validate_on_submit():
        form.populate_obj(resume)
        db.session.commit()
        flash("Personal info saved.", "success")
        return redirect(url_for("resume.edit_skills", resume_id=resume.id))
    return render_template(
        "resume/edit_section.html",
        form=form,
        resume=resume,
        section="Personal Information",
        step=1,
    )


@resume_bp.route("/<int:resume_id>/skills", methods=["GET", "POST"])
@login_required
def edit_skills(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    form = SkillsForm(obj=resume)
    if form.validate_on_submit():
        resume.skills = form.skills.data or ""
        resume.hobbies = form.hobbies.data or ""
        db.session.commit()
        flash("Skills & hobbies saved.", "success")
        return redirect(url_for("resume.edit_education", resume_id=resume.id))
    return render_template(
        "resume/edit_section.html",
        form=form,
        resume=resume,
        section="Technical Skills & Hobbies",
        step=2,
    )


@resume_bp.route("/<int:resume_id>/education", methods=["GET", "POST"])
@login_required
def edit_education(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    form = EducationForm(obj=resume)
    if form.validate_on_submit():
        resume.education = form.education.data or ""
        resume.certifications = form.certifications.data or ""
        db.session.commit()
        flash("Education & certifications saved.", "success")
        return redirect(url_for("resume.edit_projects", resume_id=resume.id))
    return render_template(
        "resume/edit_section.html",
        form=form,
        resume=resume,
        section="Education & Certifications",
        step=3,
    )


@resume_bp.route("/<int:resume_id>/projects", methods=["GET", "POST"])
@login_required
def edit_projects(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    form = ProjectsForm(obj=resume)
    if form.validate_on_submit():
        resume.projects = form.projects.data or ""
        db.session.commit()
        flash("Projects saved.", "success")
        return redirect(url_for("resume.edit_experience", resume_id=resume.id))
    return render_template(
        "resume/edit_section.html",
        form=form,
        resume=resume,
        section="Projects",
        step=4,
    )


@resume_bp.route("/<int:resume_id>/experience", methods=["GET", "POST"])
@login_required
def edit_experience(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    form = ExperienceForm(obj=resume)
    if form.validate_on_submit():
        resume.experience = form.experience.data or ""
        resume.achievements = form.achievements.data or ""
        resume.extracurricular = form.extracurricular.data or ""
        db.session.commit()
        flash("Experience & achievements saved.", "success")
        return redirect(url_for("resume.preview", resume_id=resume.id))
    return render_template(
        "resume/edit_section.html",
        form=form,
        resume=resume,
        section="Experience & Achievements",
        step=5,
        experience_type=resume.experience_type,
    )


@resume_bp.route("/<int:resume_id>/preview")
@login_required
def preview(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))
    html = render_resume_html(resume)
    return render_template(
        "resume/preview.html",
        resume=resume,
        resume_html=html,
        ctx=resume_context(resume),
    )


@resume_bp.route("/<int:resume_id>/pdf")
@login_required
def download_pdf(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))

    html = render_resume_html(resume)
    # Wrap for PDF with print-friendly base
    wrapped = render_template("resume_templates/pdf_wrapper.html", body=html, resume=resume)
    pdf = generate_pdf(wrapped)
    if not pdf:
        flash("PDF generation failed. Please try again.", "error")
        return redirect(url_for("resume.preview", resume_id=resume.id))

    filename = f"{(resume.full_name or 'resume').replace(' ', '_')}_Resume.pdf"
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )


@resume_bp.route("/<int:resume_id>/delete", methods=["POST"])
@login_required
def delete(resume_id):
    resume = _get_owned(resume_id)
    if not resume:
        flash("Resume not found.", "error")
        return redirect(url_for("resume.dashboard"))
    db.session.delete(resume)
    db.session.commit()
    flash("Resume deleted.", "info")
    return redirect(url_for("resume.dashboard"))
