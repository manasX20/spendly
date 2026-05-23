"""
Unit tests for login and logout — Step 03.

Each test gets a fresh in-memory DB via the `client` fixture in conftest.py.
The seeded test user is: test@example.com / password123
"""

# ------------------------------------------------------------------ #
# GET /login                                                           #
# ------------------------------------------------------------------ #

def test_login_get_renders_form(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Sign in" in response.data


# ------------------------------------------------------------------ #
# POST /login — happy path                                            #
# ------------------------------------------------------------------ #

def test_login_valid_credentials_redirects_to_profile(client):
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 302
    assert "/profile" in response.headers["Location"]


def test_login_valid_credentials_sets_session(client):
    with client.session_transaction() as sess:
        assert "user_id" not in sess

    client.post(
        "/login",
        data={"email": "test@example.com", "password": "password123"},
    )

    with client.session_transaction() as sess:
        assert "user_id" in sess


# ------------------------------------------------------------------ #
# POST /login — bad credentials                                       #
# ------------------------------------------------------------------ #

def test_login_wrong_password_shows_error(client):
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_wrong_password_does_not_set_session(client):
    client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
    )
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_login_unknown_email_shows_generic_error(client):
    response = client.post(
        "/login",
        data={"email": "nobody@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


def test_login_unknown_email_does_not_reveal_which_field_failed(client):
    wrong_email = client.post(
        "/login",
        data={"email": "nobody@example.com", "password": "password123"},
    )
    wrong_password = client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
    )
    # Both failure modes must show the identical error string — no field enumeration
    assert b"Invalid email or password" in wrong_email.data
    assert b"Invalid email or password" in wrong_password.data


def test_login_empty_credentials_shows_error(client):
    response = client.post("/login", data={"email": "", "password": ""})
    assert response.status_code == 200
    assert b"Invalid email or password" in response.data


# ------------------------------------------------------------------ #
# POST /login — email pre-fill on failure                             #
# ------------------------------------------------------------------ #

def test_login_email_prefilled_after_wrong_password(client):
    response = client.post(
        "/login",
        data={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert b"test@example.com" in response.data


def test_login_email_prefilled_after_unknown_email(client):
    response = client.post(
        "/login",
        data={"email": "nobody@example.com", "password": "anything"},
    )
    assert b"nobody@example.com" in response.data


# ------------------------------------------------------------------ #
# GET /logout                                                          #
# ------------------------------------------------------------------ #

def test_logout_redirects_to_landing(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] in ("/", "http://localhost/")


def test_logout_clears_session(client):
    client.post(
        "/login",
        data={"email": "test@example.com", "password": "password123"},
    )
    with client.session_transaction() as sess:
        assert "user_id" in sess

    client.get("/logout")

    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_without_session_does_not_crash(client):
    response = client.get("/logout")
    assert response.status_code == 302
