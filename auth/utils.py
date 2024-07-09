from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_AUTH_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


cookie_transport = CookieTransport(cookie_name="mycookie", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)
