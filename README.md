# Courses API

A Django REST Framework API for browsing and managing online courses, with JWT authentication and role-based write access.

![Sample API output](output.png)

## Features

- Categories and courses with auto-generated unique slugs (slug-based lookup)
- Filtering by title, price range, category, and instructor, plus search and ordering
- Custom user model that logs in with **email**; emails are normalized to lowercase so `Ada@x.com` and `ada@x.com` can't become two accounts
- JWT authentication with short-lived access tokens (5 minutes), refresh token rotation, and logout through token blacklisting
- Read access for any logged-in user; create, update, and delete for staff only
- Rate limiting: 20 requests/minute for anonymous users, 100/minute for authenticated users, and a stricter 5/minute on login
- Query optimization with `select_related` and `prefetch_related` to avoid N+1 queries
- Safe deletes: a category that still has courses can't be deleted (the API returns `409 Conflict` with a clear message)
- Page-number pagination (10 items per page)

## Tech stack

Django, Django REST Framework, django-filter, djangorestframework-simplejwt

## Data model

- **Category:** `name`, `slug` (unique, auto-generated)
- **Course:** `category` (protected foreign key), `title`, `instructor`, `price` (non-negative), `description`, `slug` (unique, auto-generated)

## Setup

```bash
git clone https://github.com/Dev-Bolu/Courses-API.git
cd Courses-API

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_courses   # optional sample data
python manage.py runserver
```

## Authentication

Log in with your email and password to get an access token and a refresh token. Send the access token with every request:

```
Authorization: Bearer <access_token>
```

Access tokens expire after 5 minutes. Use the refresh endpoint to get a new one. Refresh tokens are rotated on use, and the old one is blacklisted.

## Endpoints

Base prefix: `/api`

| Method | URL | Access |
| --- | --- | --- |
| POST | `/api/token/` | Public (limited to 5/min) |
| POST | `/api/token/refresh/` | Public |
| POST | `/api/token/blacklist/` | Public |
| GET | `/api/categories/` and `/api/categories/<slug>/` | Logged-in user |
| POST, PUT, PATCH, DELETE | `/api/categories/...` | Staff |
| GET | `/api/courses/` and `/api/courses/<slug>/` | Logged-in user |
| POST, PUT, PATCH, DELETE | `/api/courses/...` | Staff |

### Course filters

`?title=`, `?min_price=`, `?max_price=`, `?category_slug=`, `?category_name=`, `?instructor=`, `?search=`, `?ordering=price` (or `-price`, `title`, `id`), `?page=`

Search covers title, instructor, description, and category name.

## Examples

Log in:

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "you@example.com", "password": "yourpassword"}'
```

List courses under $50, cheapest first:

```bash
curl "http://localhost:8000/api/courses/?max_price=50&ordering=price" \
  -H "Authorization: Bearer <access_token>"
```

## Author

Akanbi Boluwatife Emmanuel — [GitHub](https://github.com/Dev-Bolu)
