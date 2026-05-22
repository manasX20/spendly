# Spec: Registration

## Overview
Implement user registration so a visitor can create a Spendly account with
their name, email, and password. This step wires the existing `POST /register`
form in `register.html` to a real route handler that validates input, hashes
the password, inserts the new user, and starts a session. It is the first step
that touches Flask sessions and is a prerequisite for every authenticated page.

## Depends on
- Step 01 — Database Setup (users table and `get_db()` must exist)

## Routes
- `GET /register` — Already implemented; renders `register.html` — public
- `POST /register` — **New** — validates form, creates user, redirects to `/dashboard` (or `/login` on error) — public

## Database changes
No new tables or columns. The `users` table created in Step 01 is sufficient.

## Templates
- **Modify:** `templates/register.html`
  - Change `<form action="/register">` to use `url_for('register')` (already uses `/register` — confirm method is POST)
  - The `{% if error %}` block is already present; no structural changes needed
  - Re-render the form with the submitted `name` and `email` values pre-filled on validation errors (add `value="{{ name or '' }}"` and `value="{{ email or '' }}"`)

## Files to change
- `app.py` — add `POST /register` handler; add `app.secret_key`; import `session`, `redirect`, `request`, `flash` from flask; import `create_user` from `database.db`
- `database/db.py` — add `create_user(name, email, password)` helper
- `templates/register.html` — pre-fill name/email on error; ensure form uses `url_for('register')`

## Files to create
No new files.

## New dependencies
No new pip packages. Uses:
- `werkzeug.security.generate_password_hash` (already installed)
- `flask.session` (built-in)

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before storing
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `app.secret_key` must be set before any session usage; use a hard-coded dev secret for now (e.g. `"spendly-dev-secret"`) — a single string literal, not an env var
- On duplicate email, catch `sqlite3.IntegrityError` and re-render the form with an error message — never expose raw exception text to the user
- After successful registration, start a session (`session['user_id'] = new_id`) and redirect to `/login` (dashboard is not built yet)
- Validate server-side: name non-empty, email non-empty, password at least 8 characters — return a user-friendly error string if any check fails
- `create_user()` belongs in `database/db.py`, not inline in the route

## Definition of done
- [ ] Submitting the form with valid data creates a new row in the `users` table with a hashed password
- [ ] Successful registration redirects the user (no 200 with empty body)
- [ ] Submitting with a duplicate email shows an inline error message and does not crash
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] Submitting with a blank name or email shows a validation error
- [ ] The name and email fields are re-populated after a failed submission
- [ ] The app starts without errors after adding `secret_key`
- [ ] No plaintext passwords appear anywhere in the database
