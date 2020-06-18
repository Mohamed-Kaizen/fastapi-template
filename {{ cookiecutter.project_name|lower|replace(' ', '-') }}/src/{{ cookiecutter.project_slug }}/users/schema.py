"""Collection of pydantic schema."""
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator

from {{ cookiecutter.project_slug }}.settings import settings

from . import pwned, validators  # noqa: I202


class TokenData(BaseModel):
    """Schema for token data."""

    id: UUID
    username: str
    exp: int


class User(BaseModel):
    """Schema for user sign up data."""

    username: str = Field(..., min_length=1, max_length=256)

    password: str = Field(
        ...,
        min_length=settings.MINIMUM_PASSWORD_LENGTH,
        max_length=settings.MAXIMUM_PASSWORD_LENGTH,
    )
    email: EmailStr

    @validator("username")
    def extra_validation_on_username(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the username.

        Args:
            cls: It the same as self
            value: The username value from an input.

        Returns:
            The username if it is valid.
        """
        validators.validate_reserved_name(value=value, exception_class=ValueError)

        validators.validate_confusables(value=value, exception_class=ValueError)

        return value

    @validator("password")
    def extra_validation_on_password(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the password.

        Args:
            cls: It the same as self
            value: The password value from an input.

        Returns:
            The password if it is valid.

        Raises:
            ValueError: If password is pwned or connection error it return 422 status.
        """
        result = pwned.pwned_password(password=value)

        if result is None:
            raise ValueError("Connection error, try again")

        if result > 0:
            raise ValueError(
                f"Oh no — pwned! This password has been seen {result} times before"
            )

        else:
            return value

    @validator("email")
    def extra_validation_on_email(cls: "User", value: str) -> str:  # noqa DAR101
        """Extra Validation for the email.

        Args:
            cls: It the same as self
            value: The email value from an input.

        Returns:
            The email if it is valid.
        """
        local_part, domain = value.split("@")

        validators.validate_reserved_name(value=local_part, exception_class=ValueError)

        validators.validate_confusables_email(
            domain=domain, local_part=local_part, exception_class=ValueError
        )

        return value
