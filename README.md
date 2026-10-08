# Courses-API


A Django REST Framework API for browsing and managing online courses, with JWT authentication.

## Features

- Categories and courses with auto-generated unique slugs
- Filtering by title, price range, category and instructor, plus search and ordering
- JWT login with email, token refresh and logout (blacklist)
- Staff-only writes; any logged-in user can read
- Rate limiting (stricter on login)

## Tech stack

Django, Django REST Framework, django-filter, djangorestframework-simplejwt

## Setup

```bash
git clone git remote add origin https://github.com/Dev-Bolu/Courses-API.git

cd course-api

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_courses   # optional sample data
python manage.py runserver
```

## Endpoints

Base prefix assumed to be `/api`.

| Method | URL | Access |
|---|---|---|
| POST | `/api/token/` | Public (limited to 5/min) |
| POST | `/api/token/refresh/` | Public |
| POST | `/api/token/blacklist/` | Public |
| GET | `/api/categories/` and `/api/categories/<slug>/` | Logged-in user |
| POST, PUT, PATCH, DELETE | `/api/categories/...` | Staff |
| GET | `/api/courses/` and `/api/courses/<slug>/` | Logged-in user |
| POST, PUT, PATCH, DELETE | `/api/courses/...` | Staff |

Send the access token as `Authorization: Bearer <token>`.

### Course filters

`?title=`, `?min_price=`, `?max_price=`, `?category_slug=`, `?category_name=`,
`?instructor=`, `?search=`, `?ordering=price` (or `-price`, `title`, `id`)

### Example

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'
```