"""
To run this test suite, you have to create first a user with a username/password.
"""

from http import HTTPStatus

import pytest
import requests


BASE_URL = "http://localhost:9999"

URL_TODO = f"{BASE_URL}/todo/"
URL_NOTE = f"{BASE_URL}/note/"
URL_TOKEN = f"{BASE_URL}/login/"

def test_sanity_todo(session):
    r = session.post(
        URL_TODO,
        json={
            "id": 0,
            "status": "0",
            "title": "T0",
        },
    )

    assert r.status_code == HTTPStatus.CREATED
    created_todo = r.json()

    r = session.get(
        URL_TODO,
    )
    assert r.status_code == 200
    todos = r.json()

    assert any(el == created_todo for el in todos)

def test_sanity_note(session):
    r = session.post(
        URL_NOTE,
        json={
            "id": 0,
            "status": "0",
            "title": "T0",
        },
    )

    assert r.status_code == HTTPStatus.CREATED
    created_note = r.json()

    r = session.get(
        URL_NOTE,
    )
    assert r.status_code == HTTPStatus.OK
    notes = r.json()

    assert any(el == created_note for el in notes)


@pytest.fixture
def session():
    s = requests.Session()
    r = s.post(
        "http://localhost:9999/login/",
        json={"username": "test", "password": "mypass"*2},
    )
    token = r.json()["token"]
    s.headers["Authorization"] = " ".join(("Token", token))
    return s
