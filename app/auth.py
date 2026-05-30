from __future__ import annotations

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Cookie, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import ADMIN_JWT_EXPIRE_SECONDS, ADMIN_JWT_SECRET, COOKIE_SECURE, TOKEN_SESSION_TTL_SECONDS
from .models import Admin, Token, TokenSession

password_hasher = PasswordHasher()

ERROR_MESSAGES = {
    "INVITE_INVALID": "邀请码不存在或无效。",
    "INVITE_REDEEMED": "此邀请码已经被兑换。",
    "TOKEN_INVALID": "Token 不存在、无效或已被撤销。",
    "TOKEN_ALREADY_CONNECTED": "此 token 已有活跃连接，不能再次建立连接。",
    "TOKEN_NOT_CONNECTED": "此 token 当前没有有效连接，请先连接后再访问 RAG 服务。",
    "ADMIN_UNAUTHORIZED": "管理员未登录或登录已过期。",
}


def now_utc() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def error(status_code: int, code: str, message: str | None = None) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message or ERROR_MESSAGES[code]})


def hash_secret(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False


def generate_invite_code() -> str:
    raw = secrets.token_urlsafe(12).replace("_", "").replace("-", "").upper()[:16]
    return "-".join(raw[index : index + 4] for index in range(0, 16, 4))


def generate_token() -> str:
    return "cr_" + secrets.token_urlsafe(32)


def generate_session_id() -> str:
    return "sess_" + secrets.token_urlsafe(32)


def create_admin_jwt(admin: Admin) -> str:
    expires_at = now_utc() + timedelta(seconds=ADMIN_JWT_EXPIRE_SECONDS)
    return jwt.encode({"sub": str(admin.id), "username": admin.username, "exp": expires_at}, ADMIN_JWT_SECRET, algorithm="HS256")


def decode_admin_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, ADMIN_JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise error(status.HTTP_401_UNAUTHORIZED, "ADMIN_UNAUTHORIZED") from exc


async def get_bearer_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise error(status.HTTP_401_UNAUTHORIZED, "TOKEN_INVALID")
    return authorization.split(" ", 1)[1].strip()


async def validate_token_session(
    session: AsyncSession,
    token_value: str,
    session_id: str | None,
) -> tuple[Token, TokenSession]:
    if not session_id:
        raise error(status.HTTP_409_CONFLICT, "TOKEN_NOT_CONNECTED")

    result = await session.execute(select(Token).where(Token.token_hash == hash_secret(token_value)))
    token = result.scalar_one_or_none()
    if token is None or token.revoked_at is not None:
        raise error(status.HTTP_401_UNAUTHORIZED, "TOKEN_INVALID")

    result = await session.execute(select(TokenSession).where(TokenSession.session_id == session_id))
    token_session = result.scalar_one_or_none()
    current_time = now_utc()
    if (
        token_session is None
        or token_session.token_id != token.id
        or token_session.released_at is not None
        or token_session.expires_at <= current_time
        or token.active_session_id != token_session.id
    ):
        raise error(status.HTTP_409_CONFLICT, "TOKEN_NOT_CONNECTED")

    token.last_used_at = current_time
    token_session.heartbeat_at = current_time
    token_session.expires_at = current_time + timedelta(seconds=TOKEN_SESSION_TTL_SECONDS)
    await session.commit()
    return token, token_session


async def require_admin(admin_token: Annotated[str | None, Cookie(alias="admin_session")] = None):
    if not admin_token:
        raise error(status.HTTP_401_UNAUTHORIZED, "ADMIN_UNAUTHORIZED")
    payload = decode_admin_jwt(admin_token)
    return payload


def constant_time_equal(left: str, right: str) -> bool:
    return hmac.compare_digest(left, right)


def admin_cookie_kwargs() -> dict[str, object]:
    return {
        "httponly": True,
        "secure": COOKIE_SECURE,
        "samesite": "lax",
        "max_age": ADMIN_JWT_EXPIRE_SECONDS,
        "path": "/",
    }
