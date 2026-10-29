# ResumeForge

A **Python-only** web resume builder built with Flask.

Create fresher or experienced resumes, pick from 5 templates, customize fonts & colors, preview live, save, and download as PDF. Includes an optional admin panel.

## Features

1. **Account** — Register / login, save multiple resumes  
2. **Personal info** — Name, contact, links, summary  
3. **Skills & projects** — Technical skills, project title/description/tech, certifications  
4. **Experience** — Fresher / experienced mode, internships, work history, achievements, extracurriculars, hobbies  
5. **Templates** — Professional, Modern, Simple, Fresher Focus, Executive + font & accent color  
6. **Preview & PDF** — Live preview, edit anytime, PDF download  
7. **Admin** — User list, admin toggle, delete users, dashboard stats  

## Quick start

```bash
cd resumeBuilder
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Default admin

- Email: `admin@resumeforge.local`  
- Password: `admin123`  

Override with env vars `ADMIN_EMAIL` and `ADMIN_PASSWORD` before first run.

## How to fill multi-line fields

Use one entry per line with `|` separators:

| Section | Format |
|--------|--------|
| Education | `Degree \| Institute \| Year \| Score` |
| Certifications | `Name \| Issuer \| Year` |
| Projects | `Title \| Description \| Technologies` |
| Experience | `Role \| Company \| Duration \| Description` |
| Achievements / Extracurricular | one item per line |
| Skills / Hobbies | comma-separated |

## Stack

- Flask, Flask-Login, Flask-SQLAlchemy, Flask-WTF  
- SQLite database  
- xhtml2pdf for PDF generation  

## Project layout

```
app.py              # Application factory
config.py           # Settings
models.py           # User & Resume models
forms.py            # WTForms
utils.py            # Parsing + PDF helpers
routes/             # Auth, resume builder, admin, landing
templates/          # UI + 5 resume layouts
static/css/         # Site styles
```
