export type ApiError = {
  code: string;
  message: string;
};

export type RedeemResponse = {
  token: string;
  message: string;
  derived_invites: string[];
};

export type ConnectResponse = {
  session_id: string;
  expires_at: string;
  heartbeat_interval_seconds: number;
};

export type SearchResult = {
  id: string;
  title: string;
  source: string;
  lesson: string | null;
  topic: string | null;
  kind: string;
  keywords: string[];
  questions: string[];
  content: string;
  score: number;
};

export type AskResponse = {
  answer: string;
  sources: SearchResult[];
};

export type InviteItem = {
  id: number;
  code: string | null;
  kind: string;
  parent_invite_id: number | null;
  created_by_admin_id: number | null;
  redeemed_token_id: number | null;
  redeemed_at: string | null;
  created_at: string;
};

export type TokenItem = {
  id: number;
  token: string | null;
  invite_id: number;
  revoked_at: string | null;
  created_at: string;
  last_used_at: string | null;
  active_session_id: number | null;
  session_expires_at: string | null;
};

export type SessionItem = {
  id: number;
  token_id: number;
  session_id: string;
  created_at: string;
  heartbeat_at: string;
  expires_at: string;
  released_at: string | null;
};

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(path, {
    credentials: 'include',
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    let error: ApiError = { code: String(response.status), message: response.statusText };
    try {
      const data = await response.json();
      error = data.detail || data;
    } catch {
      error.message = await response.text();
    }
    throw error;
  }
  return response.json();
}

export function ragHeaders(token: string, sessionId: string): HeadersInit {
  return {
    Authorization: `Bearer ${token}`,
    'X-Session-Id': sessionId,
  };
}
