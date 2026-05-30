from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from .config import DEFAULT_TOP_K, MAX_TOP_K


class ErrorResponse(BaseModel):
    code: str
    message: str


class RedeemInviteRequest(BaseModel):
    invite_code: str = Field(..., min_length=1, max_length=128)


class RedeemInviteResponse(BaseModel):
    token: str
    message: str
    derived_invites: list[str] = []


class ConnectRequest(BaseModel):
    token: str = Field(..., min_length=1, max_length=256)


class ConnectResponse(BaseModel):
    session_id: str
    expires_at: datetime
    heartbeat_interval_seconds: int


class StatusResponse(BaseModel):
    connected: bool
    expires_at: datetime | None = None


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(DEFAULT_TOP_K, ge=1, le=MAX_TOP_K)


class SearchResult(BaseModel):
    id: str
    title: str
    source: str
    lesson: str | None
    topic: str | None
    kind: str
    keywords: list[str]
    questions: list[str]
    content: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[SearchResult]


class AdminLoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=191)
    password: str = Field(..., min_length=1, max_length=256)


class AdminMeResponse(BaseModel):
    username: str


class CreateInviteResponse(BaseModel):
    invite_code: str
    message: str


class InviteListItem(BaseModel):
    id: int
    kind: str
    parent_invite_id: int | None
    created_by_admin_id: int | None
    redeemed_token_id: int | None
    redeemed_at: datetime | None
    created_at: datetime


class TokenListItem(BaseModel):
    id: int
    invite_id: int
    revoked_at: datetime | None
    created_at: datetime
    last_used_at: datetime | None
    active_session_id: int | None
    session_expires_at: datetime | None = None


class SessionListItem(BaseModel):
    id: int
    token_id: int
    session_id: str
    created_at: datetime
    heartbeat_at: datetime
    expires_at: datetime
    released_at: datetime | None
