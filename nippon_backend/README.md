# Nippon Medical – Django booking backend

## Setup
    python -m venv venv && source venv/bin/activate      # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    cp .env.example .env                                  # then fill in the values
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

## Endpoints
| Method | URL | Who |
|---|---|---|
| POST | /api/Booking | public (form submit, sends the email) |
| GET | /api/Booking | token required |
| GET/PUT/PATCH/DELETE | /api/Booking/{id} | token required |
| POST | /api/auth/token | `{username,password}` -> `{token}` |
| — | /admin/ | Django admin |

## Gmail App Password
Google Account -> Security -> turn on 2-Step Verification -> App passwords -> create one
for "Mail" -> paste the 16 characters into EMAIL_HOST_PASSWORD in .env.
