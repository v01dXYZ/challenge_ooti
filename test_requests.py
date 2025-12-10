"""
To run this test suite, you have to create first a user with a username/password.
"""

from http import HTTPStatus

import pytest
import requests
import os
import time

# normally with pytest we should use a conftest.py but I want to keep it as one file.
PORT = os.getenv("DJANGO_SERVER_PORT", 9999)
BASE_URL = f"http://localhost:{PORT}"

URL_TODO = f"{BASE_URL}/todo/"
URL_NOTE = f"{BASE_URL}/note/"
URL_TOKEN = f"{BASE_URL}/login/"


def test_sanity_todo(session):
    data = {
        "status": 0,
        "title": "T0",
    }
    r = session.post(
        URL_TODO,
        json=data,
    )

    assert r.status_code == HTTPStatus.CREATED
    created_todo = r.json()

    for k, v in data.items():
        assert created_todo[k] == v

    r = session.get(
        URL_TODO,
    )
    assert r.status_code == 200
    todos = r.json()

    assert any(el == created_todo for el in todos)


def test_sanity_note(session):
    data = {
        "text": "TXT0",
    }
    r = session.post(
        URL_NOTE,
        json=data,
    )

    assert r.status_code == HTTPStatus.CREATED

    created_note = r.json()

    for k, v in data.items():
        assert created_note[k] == v

    r = session.get(
        URL_NOTE,
    )
    assert r.status_code == HTTPStatus.OK
    notes = r.json()

    assert any(el == created_note for el in notes)


@pytest.fixture
def django_server():
    s = requests.Session()
    for _ in range(3):
        try:
            s.get(URL_TOKEN)
            return
        except requests.exceptions.RequestException:
            time.sleep(1)

    assert False, "Server not available"


@pytest.fixture
def session(django_server):
    s = requests.Session()
    r = s.post(
        URL_TOKEN,
        json={"username": "test", "password": "mypass" * 2},
    )
    token = r.json()["token"]
    s.headers["Authorization"] = " ".join(("Token", token))
    return s
