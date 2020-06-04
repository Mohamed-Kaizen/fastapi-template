"""Test cases for the manage module."""
from typer.testing import CliRunner

from {{ cookiecutter.project_slug }}.manage import app

runner = CliRunner()


def test_help_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "version" in result.output
    assert "serve" in result.output
    assert "create-superuser" in result.output


def test_version_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "{{ cookiecutter.project_name }}" in result.stdout


def test_create_superuser_succeeds() -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(
        app,
        ["create-superuser"],
        input="{{ cookiecutter.project_slug }}\n{{ cookiecutter.project_slug }}@example.com\n123456\n123456\ny"
    )
    assert result.exit_code == 0
    assert "{{ cookiecutter.project_slug }} hes been created" in result.stdout
