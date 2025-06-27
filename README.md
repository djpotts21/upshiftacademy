# UpShift Academy

UpShift Academy is a modern **Django-based Learning Management System (LMS)** designed to teach coding through modular programmes, interactive lessons, and auto-graded coding challenges. Built for learners, educators, and community-driven initiatives.

## Features

- **Modular Structure** — Courses are broken down into Programmes, Units, Lessons, and Modules. Each piece is reusable and adaptable.
- **Live Coding Challenges** — Integrated in-browser code editor with automatic grading (powered by Judge0).
- **Admin-Friendly** — Create, update, and manage your curriculum with Django's admin panel.
- **User Authentication** — Secure login, registration, and email confirmation with `django-allauth`.
- **Dynamic Image Uploads** — Drag-and-drop image sorting for content-rich drops and lessons.
- **Docker-Ready** — Optional Docker support for local development and deployment.

## Tech Stack

- **Backend:** Django 5+
- **Frontend:** Bootstrap 5, HTMX
- **Database:** PostgreSQL (recommended), SQLite (local/dev)
- **Code Execution:** Judge0 API
- **Others:** SCSS for custom styling, `django-allauth`, `python-decouple`

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/upshift-academy.git
cd upshift-academy
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
JUDGE0_API_URL=https://secure.judge0.com
```

### 5. Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

## Running Tests

```bash
python manage.py test
```

## Project Structure

```
upshift-academy/
├── core/                # Core app with models: Programme, Unit, Lesson, Module
├── challenges/          # Coding challenge functionality
├── users/               # User profiles, registration
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # Uploaded images/files
├── manage.py
└── requirements.txt
```

## Development Notes

- SCSS is compiled manually using `npm` or `sass`. Customize Bootstrap via SCSS partials.
- Judge0 API requires an external service key for secure code execution.
- Email confirmation uses `django-allauth`. Configure email backend in `.env`.

## Roadmap

- [x] Modular learning system
- [x] Code challenge integration
- [ ] Learner progress dashboard
- [ ] Course certification
- [ ] Instructor role management
- [ ] Community features (discussion boards, peer reviews)

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

## License

[MIT](LICENSE)

---

> Empowering the next generation of developers – one challenge at a time.
