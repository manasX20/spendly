# Spec: Login and Logout

## Overview
Implement login and logout so registered users can authenticate with their email
and password and end their session cleanly. This step upgrades the existing
`GET /login` stub to a full `GET|POST /login` handler, wires up the already-present
`logout` stub, and adds a `get_user_by_email()` helper to the DB layer. Together
they complete the core authentication loop started in Step 02 (Registration).

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, hashed passwords in DB, `session['user_id']` convention)

## Routes
- `GET /login` — renders `login.html` — public
- `POST /login` — validates credentials, sets session, redirects to `/profile` on success or re-renders form on failure — public
- `GET /logout` — clears session, redirects to `/` — logged-in (no hard guard needed yet, safe to call when logged out too)

## Database changes
No new tables or columns. The existing `users` table is sufficient.

## Templates
- **Modify:** `templates/login.html`
  - Fix hardcoded `action="/login"` to `action="{{ url_for('login') }}"`
  - Pre-fill the email field on failed login: `value="{{ email or '' }}"`

## Files to change
- `app.py`
  - Change `@app.route("/login")` to `@app.route("/login", methods=["GET", "POST"])`
  - Add POST handler: read email/password from form, call `get_user_by_email()`,
    verify hash with `check_password_hash`, set `session["user_id"]`, redirect to `/profile`
  - On bad credentials: re-render `login.html` with `error` and `email` context
  - Implement `GET /logout`: call `session.clear()`, redirect to `url_for("landing")`
  - Add `check_password_hash` to the werkzeug import (already imports `generate_password_hash` via db.py — import it directly in app.py)
  - Import `get_user_by_email` from `database.db`
- `database/db.py`
  - Add `get_user_by_email(email)` — returns a `sqlite3.Row` or `None`
- `templates/login.html`
  - Fix hardcoded action URL
  - Add `value="{{ email or '' }}"` to the email `<input>`

## Files to create
No new files.

## New dependencies
No new pip packages. Uses:
- `werkzeug.security.check_password_hash` (already installed)
- `flask.session` (already imported)

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — no f-strings in SQL
- Password verification with `werkzeug.security.check_password_hash`; never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- On failed login, show a **generic** error ("Invalid email or password") — never reveal
  which field was wrong
- After successful login, set `session["user_id"]` then redirect to `/profile`
- Logout must call `session.clear()` (not just `session.pop`) to wipe the entire session
- `get_user_by_email()` belongs in `database/db.py`; hash comparison belongs in the route
- The `email` value must be passed back to the template on failed login so the field stays populated

## Definition of done
- [ ] `GET /login` renders the login form (existing behaviour preserved)
- [ ] Submitting valid credentials sets `session["user_id"]` and redirects to `/profile`
- [ ] Submitting an unknown email shows "Invalid email or password" and does not crash
- [ ] Submitting the correct email with the wrong password shows "Invalid email or password"
- [ ] The email field is pre-filled after a failed attempt
- [ ] `GET /logout` clears the session and redirects to the landing page
- [ ] Visiting `/logout` when already logged out redirects to landing without error
- [ ] No plaintext passwords are logged or returned in any response
