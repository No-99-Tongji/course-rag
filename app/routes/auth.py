from __future__ import annotations

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import (
    error,
    generate_invite_code,
    generate_session_id,
    generate_token,
    get_bearer_token,
    hash_secret,
    now_utc,
    validate_token_session,
)
from ..config import TOKEN_HEARTBEAT_INTERVAL_SECONDS, TOKEN_SESSION_TTL_SECONDS
from ..db import get_session
from ..models import InviteCode, Token, TokenSession
from ..schemas import ConnectRequest, ConnectResponse, RedeemInviteRequest, RedeemInviteResponse, StatusResponse

router = APIRouter(prefix="/api", tags=["auth"])


def unique_invite() -> str:
    return generate_invite_code()


@router.post("/invites/redeem", response_model=RedeemInviteResponse)
async def redeem_invite(request: RedeemInviteRequest, session: Annotated[AsyncSession, Depends(get_session)]) -> RedeemInviteResponse:
    code_hash = hash_secret(request.invite_code.strip())
    async with session.begin():
        result = await session.execute(select(InviteCode).where(InviteCode.code_hash == code_hash).with_for_update())
        invite = result.scalar_one_or_none()
        if invite is None:
            raise error(status.HTTP_400_BAD_REQUEST, "INVITE_INVALID")
        if invite.redeemed_at is not None:
            raise error(status.HTTP_400_BAD_REQUEST, "INVITE_REDEEMED")

        raw_token = generate_token()
        token = Token(token_hash=hash_secret(raw_token), token=raw_token, invite_id=invite.id)
        session.add(token)
        await session.flush()

        invite.redeemed_token_id = token.id
        invite.redeemed_at = now_utc()

        derived_invites: list[str] = []
        if invite.kind == "original":
            for _ in range(2):
                code = unique_invite()
                derived_invites.append(code)
                session.add(InviteCode(code_hash=hash_secret(code), code=code, kind="derived", parent_invite_id=invite.id))

    return RedeemInviteResponse(
        token=raw_token,
        derived_invites=derived_invites,
        message="此 token 无法再次查看，请尽快复制并妥善保存。",
    )


@router.post("/auth/connect", response_model=ConnectResponse)
async def connect_token(
    payload: ConnectRequest,
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ConnectResponse:
    token_hash = hash_secret(payload.token.strip())
    current_time = now_utc()
    async with session.begin():
        result = await session.execute(select(Token).where(Token.token_hash == token_hash).with_for_update())
        token = result.scalar_one_or_none()
        if token is None or token.revoked_at is not None:
            raise error(status.HTTP_401_UNAUTHORIZED, "TOKEN_INVALID")

        if token.active_session_id is not None:
            result = await session.execute(select(TokenSession).where(TokenSession.id == token.active_session_id).with_for_update())
            active_session = result.scalar_one_or_none()
            if active_session and active_session.released_at is None and active_session.expires_at > current_time:
                raise error(status.HTTP_409_CONFLICT, "TOKEN_ALREADY_CONNECTED")
            if active_session and active_session.released_at is None:
                active_session.released_at = current_time
            token.active_session_id = None

        expires_at = current_time + timedelta(seconds=TOKEN_SESSION_TTL_SECONDS)
        token_session = TokenSession(
            token_id=token.id,
            session_id=generate_session_id(),
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            heartbeat_at=current_time,
            expires_at=expires_at,
        )
        session.add(token_session)
        await session.flush()
        token.active_session_id = token_session.id
        token.last_used_at = current_time

    return ConnectResponse(
        session_id=token_session.session_id,
        expires_at=expires_at,
        heartbeat_interval_seconds=TOKEN_HEARTBEAT_INTERVAL_SECONDS,
    )


@router.post("/auth/heartbeat", response_model=StatusResponse)
async def heartbeat(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_value: Annotated[str, Depends(get_bearer_token)],
    x_session_id: Annotated[str | None, Header()] = None,
) -> StatusResponse:
    _, token_session = await validate_token_session(session, token_value, x_session_id)
    return StatusResponse(connected=True, expires_at=token_session.expires_at)


@router.post("/auth/disconnect", response_model=StatusResponse)
async def disconnect(
    session: Annotated[AsyncSession, Depends(get_session)],
    token_value: Annotated[str, Depends(get_bearer_token)],
    x_session_id: Annotated[str | None, Header()] = None,
) -> StatusResponse:
    token, token_session = await validate_token_session(session, token_value, x_session_id)
    current_time = now_utc()
    token_session.released_at = current_time
    token.active_session_id = None
    await session.commit()
    return StatusResponse(connected=False)
