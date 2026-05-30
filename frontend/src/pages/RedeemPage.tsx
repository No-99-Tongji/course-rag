import { FormEvent, useState } from 'react';
import { api, ApiError, RedeemResponse } from '../api';

export default function RedeemPage() {
  const [inviteCode, setInviteCode] = useState('');
  const [result, setResult] = useState<RedeemResponse | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);
    try {
      const data = await api<RedeemResponse>('/api/invites/redeem', {
        method: 'POST',
        body: JSON.stringify({ invite_code: inviteCode }),
      });
      setResult(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container narrow">
      <section className="card">
        <h1>兑换 RAG Token</h1>
        <p className="muted">输入邀请码兑换 token。token 只显示一次，请立即复制。</p>
        <form onSubmit={submit} className="stack">
          <input value={inviteCode} onChange={(event) => setInviteCode(event.target.value)} placeholder="请输入邀请码" />
          <button disabled={!inviteCode.trim() || loading}>{loading ? '兑换中...' : '兑换'}</button>
        </form>
        {error && <div className="error">{error}</div>}
      </section>
      {result && (
        <section className="card success stack">
          <h2>兑换成功</h2>
          <p className="warning">{result.message}</p>
          <CodeBlock label="Token" value={result.token} />
          {result.derived_invites.length > 0 && (
            <div className="stack">
              <h3>派生邀请码</h3>
              <p className="warning">这些派生邀请码也只显示一次，请立即复制。</p>
              {result.derived_invites.map((code) => <CodeBlock key={code} label="派生邀请码" value={code} />)}
            </div>
          )}
        </section>
      )}
    </main>
  );
}

function CodeBlock({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="label">{label}</div>
      <div className="code-row">
        <code>{value}</code>
        <button type="button" onClick={() => navigator.clipboard.writeText(value)}>复制</button>
      </div>
    </div>
  );
}
