"""Collection of utils."""
from {{ cookiecutter.project_slug }}.settings import settings


def make_password_hash(*, password: str) -> str:
    """Turn a plain-text password into a hash for database storage.

    Args:
        password: plain text

    Example:
        >>> from {{ cookiecutter.project_slug }}.users import utils
        >>> hashed_password = utils.make_password_hash(password="raw password")
        >>> len(hashed_password) > 0
        True
        >>> type(hashed_password) == str
        True

    Returns:
        Hash string
    """
    return settings.PASSWORD_CONTEXT.hash(password)


def verify_password(*, plain_password: str, hashed_password: str) -> bool:
    """Verify plain-text password.

    Args:
        plain_password: plain text
        hashed_password: hashed string

    Example:
        >>> from {{ cookiecutter.project_slug }}.users import utils
        >>> hashed_password = utils.make_password_hash(password="raw password")
        >>> utils.verify_password(plain_password="raw password", hashed_password=hashed_password) # noqa: B950
        True

    Returns:
        bool
    """
    return settings.PASSWORD_CONTEXT.verify(plain_password, hashed_password)
