import pytest
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

    assert b"Área Administrativa" in response.data

def test_login_user(client):

    response = client.post(
        "/",
        data={
            "username": "user1",
            "password": "user123"
        },
        follow_redirects=True
    )

    assert b"Área do Usuário" in response.data

def test_invalid_login(client):

    response = client.post(
        "/",
        data={
            "username": "teste",
            "password": "errado"
        },
        follow_redirects=True
    )

    assert b"Usuário ou senha inválidos" in response.data