# Museum QR Management System (Django + MySQL)

## Project overview
This project powers a **museum/exhibit QR experience** for visitors and provides an **admin panel** to manage:
- Exhibit categories and exhibit details (English + Malayalam)
- Multiple images per exhibit with captions (English + Malayalam)
- QR codes for each exhibit (QR images generated and saved to `MEDIA_ROOT/qr_codes/`)
- Events and event applications (user registration + admin approval/listing)

The app is built with **Django** and uses a **MySQL** database.

---

## Features
### Visitor-facing
- Browse/view exhibits.
- View exhibit details and images.
- Language toggle between **English (`en`)** and **Malayalam (`ml`)**.
- Scanner page (`scanner.html`) to support QR scanning workflow (template-driven).

### Admin-facing
- Admin login (custom credential list inside `QRapp/views.py`).
- Manage categories:
  - add / edit / delete categories
- Manage exhibits:
  - add exhibits
  - upload multiple images
  - edit exhibit fields + images + captions
  - delete exhibits
  - QR code generation and linking
- Manage events:
  - add events (date/time/duration/image)
  - list events
  - event applications: admin view/listing

---

## Tech stack
- **Backend**: Django (Python)
- **Database**: MySQL
- **QR generation**: `qrcode` Python library
- **Media**: user-uploaded files served from `MEDIA_ROOT` (templates expect `/media/`)
- **Frontend**: server-rendered templates in `QRapp/templates/` (static assets under `QRapp/static/` and `project/static/`)

---

## Prerequisites
1. **Python 3.10+** (project appears compatible with Django 5.x; your environment uses CPython 3.13 artifacts, but normal Python 3.10+ is typically fine)
2. **MySQL Server**
3. MySQL client tools (one of:
   - MySQL Workbench
   - `mysql` CLI
   - phpMyAdmin)

---

## Installation steps
### 1) Create a virtual environment
From the repository root:

```bat
cd "d:/Museum QR Website/project/museumQR"
python -m venv venv
```

Activate it:

```bat
venv\Scripts\activate
```

### 2) Install requirements
```bat
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Configure MySQL database
Your Django settings (`project/museumQR/museumQR/settings.py`) are configured for:
- Engine: `django.db.backends.mysql`
- Database name: `db_qr`
- User: `root`
- Password: *(empty by default in settings)*
- Host: `localhost`
- Port: `3306`

You can override/adjust these values in `museumQR/settings.py`.

> Recommended: create a dedicated MySQL user for this app and update `USER`/`PASSWORD` accordingly.

### 4) Initialize database schema/data
The repository includes a MySQL dump:
- `project/db_qr.sql`

Import it into your MySQL server (examples):

**Using mysql CLI**
```bat
mysql -u root -p db_qr < "d:/Museum QR Website/project/db_qr.sql"
```

**Using phpMyAdmin / MySQL Workbench**
- Create database: `db_qr`
- Run/import the SQL from `project/db_qr.sql`

---

## Django commands
### 1) Apply migrations (recommended)
Even if you imported `db_qr.sql`, you can still run migrations to ensure consistency:

```bat
cd "d:/Museum QR Website/project/museumQR"
python manage.py makemigrations
python manage.py migrate
```

### 2) Create an admin user (optional)
This project uses a **custom admin login** (see “Admin login” below), but Django’s built-in admin auth still exists.

```bat
python manage.py createsuperuser
```

---

## Run server
Start the Django development server:

```bat
python manage.py runserver
```

Then open:
- http://127.0.0.1:8000/

---

## Admin login
The app implements a **custom admin login** in `QRapp/views.py`:
- It uses an internal map of username/password pairs.

Also note:
- `museumQR/settings.py` includes environment variables for:
  - `ADMIN_USERNAME`
  - `ADMIN_PASSWORD`

Depending on the current state of your codebase, you may need one or both:
- If you want to change credentials, prefer editing the custom credential map in `QRapp/views.py`.
- If you want Django user-based staff accounts, use `python manage.py createsuperuser`.

---

## QR code generation workflow
When an admin adds a new exhibit:
1. The admin enters exhibit information and selects a category.
2. The server constructs an **exhibit URL** using a `base_url` defined in `QRapp/views.py`.
3. `generate_qr_code(data, exhibit_id)`:
   - generates a QR image using `qrcode`
   - saves it to:
     - `MEDIA_ROOT/qr_codes/exhibit_<id>.png`
   - returns the relative path like:
     - `qr_codes/exhibit_<id>.png`
4. The exhibit record stores the resulting `qr_code_image` so templates can display it.

**Key location in code**
- `generate_qr_code()` in `QRapp/views.py`
- Output directory: `settings.MEDIA_ROOT/qr_codes`

---

## Project structure
```text
project/museumQR/
  manage.py
  requirements.txt
  db_qr.sql                     (imported into MySQL)
  museumQR/                    (Django project package)
    settings.py
    urls.py
    wsgi.py
    asgi.py
  QRapp/                       (Django app)
    views.py
    models.py
    urls.py
    templates/
    static/
    migrations/
  static/
  media/
    exhibits/                  (exhibit images)
    event_images/             (event images)
    qr_codes/                 (generated QR images)
```

---

## Admin and user pages
This project is primarily **template-rendered** (no SPA).

### Examples of routes/templates (from views)
- Home / index:
  - `index.html`
- Admin landing:
  - `admin_home.html`
- Admin login:
  - `login.html` (custom admin login handled in views)
- Categories:
  - `admin/add_category.html`
  - `admin/list_category.html`
  - `admin/edit_category.html`
- Exhibits:
  - `admin/add_exhibits.html`
  - `admin/list_exhibits.html`
  - `admin/view_exhibit.html`
  - `admin/edit_exhibits.html`
- Exhibit visitor view:
  - `user_view_exhibit.html`
- Contact / feedback / scanner:
  - `contact.html`
  - `feedback.html`
  - `scanner.html`
- Events:
  - `event_user.html` (user event listing)
  - `user_apply_event.html` (event application)
  - `admin/admin_events.html` (admin add event)
  - `admin/event_applications.html` (admin event apps list)

> Template names are referenced directly by the view functions in `QRapp/views.py`.

---

## Media / static configuration
### MEDIA
`museumQR/settings.py` defines:
- `MEDIA_URL = '/media/'`
- `MEDIA_ROOT = <project>/media`

Files are stored under:
- `project/museumQR/media/exhibits/`
- `project/museumQR/media/event_images/`
- `project/museumQR/media/qr_codes/`

**Note:** Django must be configured to serve media in development.
- This is commonly done in `museumQR/urls.py` using `static(settings.MEDIA_URL, ...)`.

### STATIC
- `STATIC_URL = '/static/'`
- Static files are expected under:
  - `QRapp/static/`
  - and top-level `project/static/`

---

## Common troubleshooting
### 1) MySQL connection errors
- Verify MySQL server is running on `localhost:3306`.
- Ensure database `db_qr` exists.
- Update `DATABASES['default']` in `museumQR/settings.py`:
  - `USER`, `PASSWORD`, `HOST`, `PORT`

### 2) `django.db.utils.OperationalError`
- Credentials mismatch.
- Database not created.
- MySQL user permissions missing.

### 3) Media images not loading
- Confirm `MEDIA_ROOT` points to the correct `media/` directory.
- Confirm `MEDIA_URL` is `/media/`.
- Ensure development URLs serve media (usually in `museumQR/urls.py`).

### 4) QR images missing
- Confirm `MEDIA_ROOT/qr_codes/` exists (it should be auto-created in `generate_qr_code`).
- Ensure `settings.MEDIA_ROOT` is correct.
- Ensure exhibit entries have `qr_code_image` set.

### 5) Templates not found
- Ensure templates directories are correct (project uses `APP_DIRS=True`).
- Confirm `INSTALLED_APPS` includes `QRapp`.

---

## Future improvements
- **Security**
  - Remove hardcoded admin credentials and use Django auth/permissions properly.
  - Use Django’s built-in `User` model for staff/admin.
- **QR base URL**
  - Move the `base_url` in `generate_qr_code()` to environment variables.
- **Consistency**
  - Remove duplicate `admin_home` function definitions in `views.py` (currently `admin_home` appears twice, and `index()` also appears twice).
- **Validation/UI**
  - Add stricter form validation and better error messages for exhibit and event forms.
- **Performance**
  - Optimize exhibit image queries and pagination.

---

## Quick start (copy/paste)
```bat
cd "d:/Museum QR Website/project/museumQR"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

REM Import DB (example)
REM mysql -u root -p db_qr < "d:/Museum QR Website/project/db_qr.sql"

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

