"""Test cases for the view module."""
import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from {{ cookiecutter.project_slug }}.main import app
from {{ cookiecutter.project_slug }}.settings import settings
from {{ cookiecutter.project_slug }}.users.models import User


@pytest.fixture()
def client() -> Generator:
    """Tortoise-orm fixture."""
    initializer(modules=settings.DB_MODELS)
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    """Event loop."""
    yield client.task.get_loop()


async def create_user() -> None:
    """Creating user for test."""
    user = User(username="{{ cookiecutter.project_slug }}", email="{{ cookiecutter.project_slug }}@{{ cookiecutter.project_slug }}.com")
    password = "@Sdf5fg7hj458h"
    user.set_password(plain_password=password)
    await user.save()


def test_login(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    """It exits with a status code of 200."""
    event_loop.run_until_complete(create_user())
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/", data="username={{ cookiecutter.project_slug }}&password=@Sdf5fg7hj458h", headers=headers
    )
    assert response.status_code == 200


def test_login_incorrect_password(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 401."""
    event_loop.run_until_complete(create_user())
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/", data="username={{ cookiecutter.project_slug }}&password=1234567899mn", headers=headers
    )
    assert response.status_code == 401


def test_login_incorrect(
    client: TestClient, event_loop: asyncio.AbstractEventLoop
) -> None:
    """It exits with a status code of 401."""
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    response = client.post(
        "/users/login/", data="username={{ cookiecutter.project_slug }}&password=@Sdf5fg7hj458h", headers=headers
    )
    assert response.status_code == 401


def test_sign_up_as_success(client: TestClient) -> None:
    """It exits with a status code of 201."""
    headers = {"Content-type": "application/json"}
    data = {
        "username": "{{ cookiecutter.project_slug }}",
        "password": "@Sdf5fg7hj458h",
        "email": "{{ cookiecutter.project_slug }}@{{ cookiecutter.project_slug }}.com",
    }
    response = client.post("/users/", json=data, headers=headers)

    assert response.json() == {"detail": "user has been created"}
    assert response.status_code == 201


def test_sign_up_fail(client: TestClient) -> None:
    """It exits with a status code of 422."""
    data = {
        "username": "admin",
        "password": "123456admin",
        "email": "admin@admin.com",
    }
    response = client.post("/users/", json=data)

    assert response.status_code == 422
