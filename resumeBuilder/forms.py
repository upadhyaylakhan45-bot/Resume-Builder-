from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=128)]
    )
    confirm = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match")],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")


class ResumeMetaForm(FlaskForm):
    title = StringField("Resume Title", validators=[DataRequired(), Length(max=160)])
    experience_type = SelectField(
        "Profile Type",
        choices=[("fresher", "Fresher"), ("experienced", "Experienced")],
        validators=[DataRequired()],
    )
    template = SelectField(
        "Template",
        choices=[
            ("professional", "Professional"),
            ("modern", "Modern"),
            ("simple", "Simple"),
            ("fresher", "Fresher Focus"),
            ("executive", "Executive"),
        ],
        validators=[DataRequired()],
    )
    font_family = SelectField(
        "Font",
        choices=[
            ("Georgia", "Georgia"),
            ("Times New Roman", "Times New Roman"),
            ("Garamond", "Garamond"),
            ("Helvetica", "Helvetica"),
            ("Arial", "Arial"),
            ("Calibri", "Calibri"),
            ("Verdana", "Verdana"),
        ],
        validators=[DataRequired()],
    )
    accent_color = StringField(
        "Accent Color",
        default="#0F4C5C",
        validators=[DataRequired(), Length(max=20)],
    )
    submit = SubmitField("Save & Continue")


class PersonalForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=120)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=180)])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    location = StringField("Location", validators=[Optional(), Length(max=120)])
    linkedin = StringField("LinkedIn", validators=[Optional(), Length(max=200)])
    github = StringField("GitHub", validators=[Optional(), Length(max=200)])
    website = StringField("Website / Portfolio", validators=[Optional(), Length(max=200)])
    summary = TextAreaField("Professional Summary", validators=[Optional(), Length(max=2000)])
    submit = SubmitField("Save Personal Info")


class SkillsForm(FlaskForm):
    skills = TextAreaField(
        "Technical Skills (comma-separated)",
        validators=[Optional(), Length(max=2000)],
        description="e.g. Python, Flask, SQL, React, AWS",
    )
    hobbies = TextAreaField(
        "Hobbies (comma-separated)",
        validators=[Optional(), Length(max=1000)],
    )
    submit = SubmitField("Save Skills & Hobbies")


class EducationForm(FlaskForm):
    education = TextAreaField(
        "Education (one per line: Degree | Institute | Year | Score)",
        validators=[Optional(), Length(max=4000)],
        description="B.Tech CSE | ABC University | 2024 | 8.5 CGPA",
    )
    certifications = TextAreaField(
        "Certifications (one per line: Name | Issuer | Year)",
        validators=[Optional(), Length(max=4000)],
        description="AWS Cloud Practitioner | Amazon | 2025",
    )
    submit = SubmitField("Save Education & Certifications")


class ProjectsForm(FlaskForm):
    projects = TextAreaField(
        "Projects (one per line: Title | Description | Technologies)",
        validators=[Optional(), Length(max=8000)],
        description="Resume Builder | Built a Python web app for resumes | Flask, SQLAlchemy",
    )
    submit = SubmitField("Save Projects")


class ExperienceForm(FlaskForm):
    experience = TextAreaField(
        "Internships / Work Experience (one per line: Role | Company | Duration | Description)",
        validators=[Optional(), Length(max=8000)],
        description="Software Intern | Acme | Jun 2024 - Aug 2024 | Built APIs in Flask",
    )
    achievements = TextAreaField(
        "Achievements (one per line)",
        validators=[Optional(), Length(max=4000)],
    )
    extracurricular = TextAreaField(
        "Extracurricular Activities (one per line)",
        validators=[Optional(), Length(max=4000)],
    )
    submit = SubmitField("Save Experience & Achievements")
