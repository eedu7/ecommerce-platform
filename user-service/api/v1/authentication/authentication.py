from fastapi import APIRouter, Depends, status

from app.controllers import AuthController
from app.models import User
from app.schemas.extras.token import Token
from app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from app.schemas.responses.users import UserResponse
from core.factory import Factory

auth_router: APIRouter = APIRouter()


@auth_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> User:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )


@auth_router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )


@auth_router.post("/logout")
async def logout_user():
    """
    Log out the user.

    - **response**: Confirms the user has been logged out.
    """
    # Completion Steps:
    # 1. Invalidate the access and refresh tokens in the database or cache.
    # 2. Add logic to ensure the user cannot use the same tokens again.
    return {
        "message": "You have been logged out.",
    }


@auth_router.post("/refresh-token")
async def refresh_token():
    """
    Refresh the access token using a valid refresh token.

    - **response**: Returns a new access token.
    """
    # Completion Steps:
    # 1. Extract the refresh token from the request.
    # 2. Verify its validity and ensure it hasn't been revoked.
    # 3. Issue a new access token for the user.
    return {
        "message": "You have been refreshed.",
    }


@auth_router.get("/forgot-password")
async def forgot_password():
    """
    Request a password reset link.

    - **email**: User's registered email.
    - **response**: Sends a password reset link to the email.
    """
    # Completion Steps:
    # 1. Accept the user's email.
    # 2. Generate a unique password reset token.
    # 3. Send the reset link with the token to the email.
    return {
        "message": "Forgot your password.",
    }


@auth_router.get("/reset-password")
async def reset_password():
    """
    Reset the user's password.

    - **token**: Password reset token.
    - **new_password**: New password for the user.
    - **response**: Confirms the password has been updated.
    """
    # Completion Steps:
    # 1. Accept the token and new password from the request.
    # 2. Verify the token's validity.
    # 3. Update the password in the database.
    return {
        "message": "Reset your password.",
    }


@auth_router.post("/email-verification")
async def email_verification():
    """
    Send an email verification link to the user.

    - **email**: User's email.
    - **response**: Sends a verification link to the user's email.
    """
    # Completion Steps:
    # 1. Generate an email verification token.
    # 2. Send the token in a verification email.
    return {
        "message": "You are being verified.",
        "task": "Sending an email verification link to the user.",
    }


@auth_router.post("/verify-email")
async def verify_email():
    """
    Verify the user's email using a token.

    - **token**: Email verification token.
    - **response**: Confirms that the email has been verified.
    """
    # Completion Steps:
    # 1. Extract the token from the request.
    # 2. Validate the token and update the user's status to 'verified'.
    return {
        "message": "You are being verified.",
        "task": "Verify the email using the token.",
    }
