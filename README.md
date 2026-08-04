<div align="center">

# 🎓 MySchool App — Backend

**A Django REST API powering a school platform for exam papers, corrections, subjects, chapters and exercises.**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-red?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/Auth-Simple%20JWT-black?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-Unlicensed-lightgrey?style=for-the-badge)](#-license)

</div>

---

## 📖 About

**MySchool_AppBackend** is the API server for a school/education platform. It handles user
authentication (with email verification and JWT), and exposes CRUD endpoints to manage
**exam papers (sujets)**, their **corrections** (with optional video walkthroughs),
**subjects & chapters**, **filière/level classes**, and **exercises**.

It is built with **Django** + **Django REST Framework**, uses **JWT** (via
`djangorestframework-simplejwt`) for stateless authentication, **Djoser**-style flows for
email verification/password reset, and is CORS-ready for a separate frontend
(web or Flutter mobile app).

---

## ✨ Features

- 🔐 **Custom email-based authentication** — registration, email verification, login, logout, password change & reset, JWT access/refresh tokens
- 📄 **Exam papers management** — `Subject`, `ExamType` (Anglophone/Francophone subsystem), `Paper` (with file upload), `ExamSubject`
- ✅ **Corrections** — correction sheets linked to a paper, plus optional **correction videos** (file or external URL)
- 🏫 **Filière & Levels** — `OptionModel` (filière/option), `Level`, `SubjectLevel`
- 📚 **Subjects & Chapters** — `Subject`, `Chapter`, `SubjectChapter` mapping
- 📝 **Exercises** — exercises with difficulty rating (1–5) linked to a subject
- 🌍 **CORS enabled** for web/mobile frontends (Vite, Flutter web, etc.)
- 🗂️ **Media/file uploads** for papers, correction sheets and videos
- 🧩 **Modular Django apps** — one app per domain, each with its own `models`, `serializers`, `views`, `urls`

---

## 🏗️ Project Structure

```
MySchool_AppBackend/
├── SchoolApp/               # Project settings, root URLs, WSGI/ASGI
├── authentication/          # Custom User model, JWT auth, email verification
├── api/                     # Placeholder / shared API app
├── sujetsExam/               # Subjects, exam types, exam papers
├── corrections/              # Corrections & correction videos
├── filiereClass/             # Filières (options) & levels
├── subjectChapters/           # Subjects & chapters
├── exercise/                  # Exercises
├── manage.py
├── Pipfile / Pipfile.lock
└── db.school3                 # SQLite database (dev)
```

---

## 🛠️ Tech Stack

| Layer          | Technology                                              |
|----------------|-----------------------------------------------------------|
| Language       | Python 3.12                                              |
| Framework      | Django 6.0                                                |
| API            | Django REST Framework                                     |
| Auth           | `djangorestframework-simplejwt`, `djoser`                 |
| CORS           | `django-cors-headers`                                     |
| Config         | `python-decouple`                                          |
| Database       | SQLite (dev) — swappable for PostgreSQL/MySQL in production |
| Storage        | Local `FileSystemStorage`, optional S3-compatible (MinIO) via `django-storages` |
| Package mgmt   | Pipenv                                                     |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.12**
- [Pipenv](https://pipenv.pypa.io/) (or `pip` + `venv`)

### 1. Clone the repository

```bash
git clone <repo-url>
cd MySchool_AppBackend
```

### 2. Install dependencies

The `Pipfile` currently only lists `django`; the project actually also relies on
DRF, Simple JWT, Djoser, CORS headers, decouple and (optionally) S3 storage.
Install everything with:

```bash
pipenv install django djangorestframework djangorestframework-simplejwt djoser django-cors-headers python-decouple django-storages
pipenv shell
```

> Prefer plain `pip`? Create a virtualenv and run the same `pip install ...` command instead.

### 3. Configure environment variables

Create a `.env` file at the project root (loaded via `python-decouple`):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
FRONTEND_URL=http://localhost:3000
```

> ⚠️ The email settings (`EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`) are currently hard-coded
> in `SchoolApp/settings.py`. For any real deployment, move these into environment
> variables and rotate the exposed credentials immediately.

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for the Django admin)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 🔌 API Overview

All endpoints are prefixed as configured in `SchoolApp/urls.py`. JWT protected
endpoints expect an `Authorization: Bearer <access_token>` header.

### 🔐 Authentication — `/api/auth/`

| Method | Endpoint                              | Description                          |
|--------|----------------------------------------|---------------------------------------|
| POST   | `register/`                            | Register a new user                   |
| POST   | `verify-email/`                        | Verify email via token                |
| POST   | `resend-verification/`                 | Resend verification email             |
| POST   | `login/`                                | Log in, returns JWT access/refresh    |
| GET    | `profile/`                              | Get the authenticated user's profile  |
| POST   | `change-password/`                      | Change password                       |
| POST   | `send-reset-password-email/`            | Request a password reset email        |
| POST   | `reset-password/<uid>/<token>/`         | Confirm password reset                |
| POST   | `logout/`                                | Log out                               |
| POST   | `auth/token/refresh/`                    | Refresh an access token               |

### 📄 Exam Papers — `/api/sujets/`

| Method | Endpoint                    | Description                          |
|--------|-------------------------------|----------------------------------------|
| GET/POST | `examType/`, `examTypes/`   | Manage exam types (Anglophone/Francophone) |
| GET/POST | `papercrud/`, `paper/`       | Create/manage exam papers              |
| GET    | `paperone/<id>/`               | Retrieve a single paper                |
| GET    | `papers/`                       | List all papers                        |
| GET    | `paperdownload/<id>/`           | Download a paper file                  |
| GET/POST | `subjectcrud/`                | Manage subjects                        |
| GET    | `subjectsE/`                    | Subjects for a given exam type         |

### ✅ Corrections — `/api/corrections/`

| Method | Endpoint                          | Description                    |
|--------|-------------------------------------|---------------------------------|
| GET/POST/PUT/DELETE | `correction/`, `correction/<id>/` | Manage corrections           |
| GET    | `correctionl/`, `correctionl/<id>/`  | List / detail corrections       |
| GET/POST/PUT/DELETE | `video/`, `video/<id>/`        | Manage correction videos       |
| GET    | `videol/`, `videol/<id>/`            | List / detail correction videos |

### 🏫 Filière & Levels — `/api/filiereClass/`

| Method | Endpoint                         | Description         |
|--------|------------------------------------|-----------------------|
| GET/POST/PUT/DELETE | `option/`, `option/<id>/`     | Manage filière options |
| GET    | `options/`, `options/<id>/`         | List / detail options  |
| GET/POST/PUT/DELETE | `level/`, `level/<id>/`       | Manage levels          |
| GET    | `levels/`, `levels/<id>/`           | List / detail levels   |

### 📚 Subjects & Chapters — `/api/subjectChapters/`

| Method | Endpoint                           | Description          |
|--------|---------------------------------------|-------------------------|
| GET/POST/PUT/DELETE | `subject/`, `subject/<id>/`      | Manage subjects         |
| GET    | `subjects/`, `subjects/<id>/`          | List / detail subjects  |
| GET/POST/PUT/DELETE | `chapter/`, `chapter/<id>/`      | Manage chapters         |
| GET    | `chapters/`, `chapters/<id>/`          | List / detail chapters  |

### 📝 Exercises — `/api/exercise/`

| Method | Endpoint                                 | Description        |
|--------|---------------------------------------------|-----------------------|
| GET/POST/PUT/DELETE | `exercisec/`, `exercisec/<id>/`        | Manage exercises      |
| GET    | `exercises/`, `exercises/<id>/`              | List / detail exercises |

---

## 🔒 Authentication Flow

1. **Register** → `POST /api/auth/register/` (email, name, surname, telephone, role, password)
2. A **verification link** is emailed to the user (`is_verified` starts as `False`)
3. **Verify** → `POST /api/auth/verify-email/` — marks the account verified and returns JWT tokens
4. **Login** → `POST /api/auth/login/` — returns `access` and `refresh` tokens
5. Use the `access` token as `Authorization: Bearer <token>` on protected endpoints
6. **Refresh** expired access tokens via `POST /api/auth/auth/token/refresh/`

Tokens are configured via `SIMPLE_JWT` in `SchoolApp/settings.py`:
- Access token lifetime: **1 hour**
- Refresh token lifetime: **5 days** (rotated & blacklisted after use)

---

## 🗄️ Data Model Overview

```
Subject ──< Paper ──< Correction ──< Videos
   │
   ├──< ExamSubject >── ExamType
   ├──< SubjectChapter >── Chapter
   └──< SubjectLevel >── Level ── OptionModel
   │
   └──< Exercise
```

- **User** (custom, email-based) — role, verification status, profile info
- **Subject / ExamType / Paper / ExamSubject** — exam papers catalog
- **Correction / Videos** — corrections tied to a paper, with optional video content
- **OptionModel / Level / SubjectLevel** — filière/class structure
- **Chapter / SubjectChapter** — chapters mapped to subjects
- **Exercise** — practice exercises with a difficulty level

---

## ⚙️ Configuration Notes

- **Database**: SQLite by default (`db.school3`). Swap the `DATABASES` setting in
  `SchoolApp/settings.py` for PostgreSQL/MySQL in production.
- **File storage**: local filesystem by default; an S3-compatible (MinIO) backend
  is pre-configured under `STORAGES["minio"]` if you want to move media off-disk.
- **CORS**: `CORS_ALLOW_ALL_ORIGINS = True` is set for development convenience —
  restrict this to your actual frontend origin(s) before deploying.

---

## 🧪 Running Tests

Each app ships a `tests.py`. Run the full suite with:

```bash
python manage.py test
```

---

## 🗺️ Roadmap / Ideas

- [ ] Pin actual dependencies in `Pipfile` (DRF, Simple JWT, Djoser, CORS headers, decouple)
- [ ] Add OpenAPI/Swagger documentation (e.g. `drf-spectacular`)
- [ ] Add pagination & filtering to list endpoints
- [ ] Restrict `CORS_ALLOWED_ORIGINS` for production

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome. Feel free to open an
issue or submit a pull request.

## 📄 License

No license file is currently included in this repository. Add one (MIT, Apache-2.0, etc.)
to clarify usage terms for contributors and users.

---

<div align="center">
Made with 🐍 Django for education.
</div>
