from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..auth import (
    admin_cookie_kwargs,
    create_admin_jwt,
    error,
    generate_invite_code,
    hash_secret,
    now_utc,
    require_admin,
    verify_password,
)
from ..db import get_session
from ..models import Admin, InviteCode, Token, TokenSession
from ..schemas import (
    AdminLoginRequest,
    AdminMeResponse,
    CreateInviteResponse,
    InviteListItem,
    SessionListItem,
    TokenListItem,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=AdminMeResponse)
async def login(payload: AdminLoginRequest, response: Response, session: Annotated[AsyncSession, Depends(get_session)]) -> AdminMeResponse:
    result = await session.execute(select(Admin).where(Admin.username == payload.username))
    admin = result.scalar_one_or_none()
    if admin is None or not verify_password(payload.password, admin.password_hash):
        raise error(status.HTTP_401_UNAUTHORIZED, "ADMIN_UNAUTHORIZED", "管理员用户名或密码错误。")
    admin.last_login_at = now_utc()
    await session.commit()
    response.set_cookie("admin_session", create_admin_jwt(admin), **admin_cookie_kwargs())
    return AdminMeResponse(username=admin.username)


@router.post("/logout")
async def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("admin_session", path="/")
    return {"status": "ok"}


@router.get("/me", response_model=AdminMeResponse)
async def me(admin_payload: Annotated[dict, Depends(require_admin)]) -> AdminMeResponse:
    return AdminMeResponse(username=str(admin_payload["username"]))


@router.post("/invites", response_model=CreateInviteResponse)
async def create_invite(
    admin_payload: Annotated[dict, Depends(require_admin)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CreateInviteResponse:
    code = generate_invite_code()
    invite = InviteCode(
        code_hash=hash_secret(code),
        kind="original",
        created_by_admin_id=int(admin_payload["sub"]),
    )
    session.add(invite)
    await session.commit()
    return CreateInviteResponse(invite_code=code, message="原始邀请码只会显示一次，请立即复制保存。")


@router.get("/invites", response_model=list[InviteListItem])
async def list_invites(
    _: Annotated[dict, Depends(require_admin)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[InviteListItem]:
    result = await session.execute(select(InviteCode).order_by(InviteCode.created_at.desc(), InviteCode.id.desc()))
    return [
        InviteListItem(
            id=invite.id,
            kind=invite.kind,
            parent_invite_id=invite.parent_invite_id,
            created_by_admin_id=invite.created_by_admin_id,
            redeemed_token_id=invite.redeemed_token_id,
            redeemed_at=invite.redeemed_at,
            created_at=invite.created_at,
        )
        for invite in result.scalars().all()
    ]


@router.get("/tokens", response_model=list[TokenListItem])
async def list_tokens(
    _: Annotated[dict, Depends(require_admin)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[TokenListItem]:
    result = await session.execute(select(Token).order_by(Token.created_at.desc(), Token.id.desc()))
    tokens = result.scalars().all()
    session_ids = [token.active_session_id for token in tokens if token.active_session_id]
    sessions_by_id: dict[int, TokenSession] = {}
    if session_ids:
        sessions_result = await session.execute(select(TokenSession).where(TokenSession.id.in_(session_ids)))
        sessions_by_id = {token_session.id: token_session for token_session in sessions_result.scalars().all()}
    return [
        TokenListItem(
            id=token.id,
            invite_id=token.invite_id,
            revoked_at=token.revoked_at,
            created_at=token.created_at,
            last_used_at=token.last_used_at,
            active_session_id=token.active_session_id,
            session_expires_at=sessions_by_id[token.active_session_id].expires_at if token.active_session_id in sessions_by_id else None,
        )
        for token in tokens
    ]


@router.post("/tokens/{token_id}/revoke")
async def revoke_token(
    token_id: int,
    _: Annotated[dict, Depends(require_admin)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, str]:
    token = await session.get(Token, token_id)
    if token is None:
        raise error(status.HTTP_404_NOT_FOUND, "TOKEN_INVALID", "Token 不存在。")
    token.revoked_at = now_utc()
    token.active_session_id = None
    await session.commit()
    return {"status": "ok"}


@router.get("/sessions", response_model=list[SessionListItem])
async def list_sessions(
    _: Annotated[dict, Depends(require_admin)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[SessionListItem]:
    result = await session.execute(select(TokenSession).order_by(TokenSession.created_at.desc(), TokenSession.id.desc()))
    return [
        SessionListItem(
            id=token_session.id,
            token_id=token_session.token_id,
            session_id=token_session.session_id,
            created_at=token_session.created_at,
            heartbeat_at=token_session.heartbeat_at,
            expires_at=token_session.expires_at,
            released_at=token_session.released_at,
        )
        for token_session in result.scalars().all()
    ]


@router.post("/sessions/{session_id}/disconnect")
async def disconnect_session(
    session_id: int,
    _: Annotated[dict, Depends(require_admin)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, str]:
    token_session = await session.get(TokenSession, session_id)
    if token_session is None:
        raise error(status.HTTP_404_NOT_FOUND, "TOKEN_NOT_CONNECTED", "连接不存在。")
    token_session.released_at = now_utc()
    token = await session.get(Token, token_session.token_id)
    if token and token.active_session_id == token_session.id:
        token.active_session_id = None
    await session.commit()
    return {"status": "ok"}
