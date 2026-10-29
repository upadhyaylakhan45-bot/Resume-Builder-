import json
from io import BytesIO

from flask import render_template
from xhtml2pdf import pisa


def parse_pipe_lines(raw: str, fields: list[str]) -> list[dict]:
    """Parse 'a | b | c' lines into list of dicts keyed by fields."""
    items = []
    if not raw:
        return items
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        item = {}
        for i, field in enumerate(fields):
            item[field] = parts[i] if i < len(parts) else ""
        items.append(item)
    return items


def parse_simple_lines(raw: str) -> list[str]:
    if not raw:
        return []
    return [ln.strip() for ln in raw.strip().splitlines() if ln.strip()]


def parse_csv(raw: str) -> list[str]:
    if not raw:
        return []
    return [p.strip() for p in raw.split(",") if p.strip()]


def resume_context(resume) -> dict:
    return {
        "resume": resume,
        "skills": parse_csv(resume.skills),
        "hobbies": parse_csv(resume.hobbies),
        "education": parse_pipe_lines(
            resume.education, ["degree", "institute", "year", "score"]
        ),
        "certifications": parse_pipe_lines(
            resume.certifications, ["name", "issuer", "year"]
        ),
        "projects": parse_pipe_lines(
            resume.projects, ["title", "description", "technologies"]
        ),
        "experience": parse_pipe_lines(
            resume.experience, ["role", "company", "duration", "description"]
        ),
        "achievements": parse_simple_lines(resume.achievements),
        "extracurricular": parse_simple_lines(resume.extracurricular),
    }


TEMPLATE_MAP = {
    "professional": "resume_templates/professional.html",
    "modern": "resume_templates/modern.html",
    "simple": "resume_templates/simple.html",
    "fresher": "resume_templates/fresher.html",
    "executive": "resume_templates/executive.html",
}


def render_resume_html(resume) -> str:
    template_name = TEMPLATE_MAP.get(resume.template, TEMPLATE_MAP["professional"])
    return render_template(template_name, **resume_context(resume))


def generate_pdf(html: str) -> BytesIO | None:
    result = BytesIO()
    pdf = pisa.CreatePDF(html, dest=result, encoding="utf-8")
    if pdf.err:
        return None
    result.seek(0)
    return result


def dumps_lines(items: list) -> str:
    """Helper if we ever need to serialize structured data back."""
    return json.dumps(items)
