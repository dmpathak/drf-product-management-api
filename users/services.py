from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from projectmanagement.settings import FRONTEND_RESET_PASSWORD_URL
from utils.tasks import send_email

User = get_user_model()


def logout_user(refresh_token: str):
    """
    Que:
        If I log out, access token is still valid… then what’s the point?

    Ans:
        Logout = invalidate refresh token, not access token
        (because using refresh token we can generate new access token without providing credentials again)

    Let's Understand Flow:
    1. Login
        - You get
            {
              "access": "short_lived_token",
              "refresh": "long_lived_token"
            }

    2. Now, Normal usage
        - Client --> sends access token --> API works

    3. If Access token expires
        Frontend detects 401 → calls /token/refresh... (If Not having frontend, need to call it manually)
        - gets new access token
        - user can use access token for APIs to work as usual.

    4. When click Logout
        - Client → calls /logout with refresh token
        - Server → blacklists refresh token

    so, Now user can not generate new access token from refresh token.
    However, user can acces-token until it expires (that's why we should set expire time short)
    after expiry, he needs to enter credentials again (beacause refresh token is blacklisted)


    *** Why Refrest token? ***
    You could Blacklist access tokens too... but it Requires DB/Redis lookup on EVERY request.
    (Because It will check in every-request... access-token in this request is blacklisted or not)

    Which Breaks stateless nature of JWT & its Slower too.
    """
    token = RefreshToken(refresh_token)
    token.blacklist()


def generate_reset_token(user):
    token = PasswordResetTokenGenerator().make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.id))
    return token, uid


def send_password_reset_mail(user):
    """
    With FRONTEND Integrated:
        This mail sending feature is useful with fronend.
        Because, we get below link in mail and when we click...

        FrontEnd will redirect it on its HTML page to set new password.

        and then fronend will call our (auth/reset-password/) API on submit with...
        token, uid & password.

    Without FRONTEND Integrated:
        We need to directly call (auth/reset-password/) API. with...
        token, uid & password.
    """
    token, uid = generate_reset_token(user)

    link = f"{FRONTEND_RESET_PASSWORD_URL}?token={token}&uid={uid}"

    send_email.delay(
        subject="Reset Password",
        message=f"Click here to reset your password:\n{link}",
        recipient_list=[user.email],
    )


def reset_user_password(user, password: str):
    user.set_password(password)
    user.save()


def blacklist_all_user_tokens(user):
    """
    you should blacklist tokens whenever we change any field which is related to auth or added into token payload.
    like...
    - email (added into token payload)
    - password

    Not always needed but can be used based on requirements.
    But, It is good practice.

    WAIT... WAIT... WAIT...
    here, also access token will still valid until its expiry. (same like we did in Logout)
    we blacklisted ll tokens of that user because we were not getting refresh token in API body.
    so, we blocked all tokens of that user.
    """
    for token in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=token)
