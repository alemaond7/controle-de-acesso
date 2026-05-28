import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

@pytest.fixture
def client():

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_login_admin(client):

    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "admin123"
        },
        follow_redirects=True
    )

    texto = response.get_data(as_text=True)

    assert "Área Administrativa" in texto

def test_login_user(client):

    response = client.post(
        "/",
        data={
            "username": "user1",
            "password": "user123"
        },
        follow_redirects=True
    )

    texto = response.get_data(as_text=True)

    assert "Área do Usuário" in texto

def test_invalid_login(client):

    response = client.post(
        "/",
        data={
            "username": "teste",
            "password": "errado"
        },
        follow_redirects=True
    )

    texto = response.get_data(as_text=True)

    assert "Usuário ou senha inválidos" in texto