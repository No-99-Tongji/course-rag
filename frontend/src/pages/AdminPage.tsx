import { ReactNode, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, ApiError, InviteItem, SessionItem, TokenItem } from '../api';

export default function AdminPage() {
  const navigate = useNavigate();
  const [invites, setInvites] = useState<InviteItem[]>([]);
  const [tokens, setTokens] = useState<TokenItem[]>([]);
  const [sessions, setSessions] = useState<SessionItem[]>([]);
  const [newInvite, setNewInvite] = useState('');
  const [error, setError] = useState('');

  async function load() {
    try {
      await api('/api/admin/me');
      const [inviteData, tokenData, sessionData] = await Promise.all([
        api<InviteItem[]>('/api/admin/invites'),
        api<TokenItem[]>('/api/admin/tokens'),
        api<SessionItem[]>('/api/admin/sessions'),
      ]);
      setInvites(inviteData);
      setTokens(tokenData);
      setSessions(sessionData);
    } catch (err) {
      const apiError = err as ApiError;
      if (apiError.code === 'ADMIN_UNAUTHORIZED') navigate('/admin/login');
      else setError(`${apiError.code}: ${apiError.message}`);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function createInvite() {
    setError('');
    setNewInvite('');
    try {
      const data = await api<{ invite_code: string; message: string }>('/api/admin/invites', { method: 'POST' });
      setNewInvite(data.invite_code);
      await load();
    } catch (err) {
      const apiError = err as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    }
  }

  async function revokeToken(id: number) {
    await api(`/api/admin/tokens/${id}/revoke`, { method: 'POST' });
    await load();
  }

  async function disconnectSession(id: number) {
    await api(`/api/admin/sessions/${id}/disconnect`, { method: 'POST' });
    await load();
  }

  async function logout() {
    await api('/api/admin/logout', { method: 'POST' });
    navigate('/admin/login');
  }

  return (
    <main className="container stack">
      <section className="card row-between">
        <div>
          <h1>管理员控制台</h1>
          <p className="muted">管理原始邀请码、token 与连接。</p>
        </div>
        <button type="button" onClick={logout}>退出登录</button>
      </section>
      {error && <div className="error">{error}</div>}
      <section className="card stack">
        <div className="row-between">
          <h2>邀请码</h2>
          <button type="button" onClick={createInvite}>生成原始邀请码</button>
        </div>
        {newInvite && (
          <div className="success">
            <p className="warning">原始邀请码只显示一次，请立即复制。</p>
            <div className="code-row"><code>{newInvite}</code><button onClick={() => navigator.clipboard.writeText(newInvite)}>复制</button></div>
          </div>
        )}
        <Table headers={['ID', '邀请码', '类型', '父邀请码', '已兑换 token', '兑换时间', '创建时间']} rows={invites.map((invite) => [
          invite.id,
          invite.code ? <CopyValue value={invite.code} /> : '-',
          invite.kind,
          invite.parent_invite_id || '-',
          invite.redeemed_token_id || '-',
          formatTime(invite.redeemed_at),
          formatTime(invite.created_at),
        ])} />
      </section>
      <section className="card stack">
        <h2>Token</h2>
        <Table headers={['ID', 'Token', '邀请码', '状态', '活跃连接', '过期时间', '创建时间', '操作']} rows={tokens.map((token) => [
          token.id,
          token.token ? <CopyValue value={token.token} /> : '-',
          token.invite_id,
          token.revoked_at ? '已撤销' : '有效',
          token.active_session_id || '-',
          formatTime(token.session_expires_at),
          formatTime(token.created_at),
          <button disabled={Boolean(token.revoked_at)} onClick={() => revokeToken(token.id)}>撤销</button>,
        ])} />
      </section>
      <section className="card stack">
        <h2>连接</h2>
        <Table headers={['ID', 'Token', 'Session', '心跳', '过期', '释放', '操作']} rows={sessions.map((session) => [
          session.id,
          session.token_id,
          session.session_id.slice(0, 14) + '...',
          formatTime(session.heartbeat_at),
          formatTime(session.expires_at),
          formatTime(session.released_at),
          <button disabled={Boolean(session.released_at)} onClick={() => disconnectSession(session.id)}>释放</button>,
        ])} />
      </section>
    </main>
  );
}

function CopyValue({ value }: { value: string }) {
  return (
    <div className="inline-secret">
      <code>{value}</code>
      <button type="button" onClick={() => navigator.clipboard.writeText(value)}>复制</button>
    </div>
  );
}

function Table({ headers, rows }: { headers: string[]; rows: ReactNode[][] }) {
  return (
    <div className="table-wrap">
      <table>
        <thead><tr>{headers.map((header) => <th key={header}>{header}</th>)}</tr></thead>
        <tbody>{rows.map((row, index) => <tr key={index}>{row.map((cell, cellIndex) => <td key={cellIndex}>{cell}</td>)}</tr>)}</tbody>
      </table>
    </div>
  );
}

function formatTime(value: string | null) {
  return value ? new Date(value).toLocaleString() : '-';
}
