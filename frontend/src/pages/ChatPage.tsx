import { FormEvent, useEffect, useState } from 'react';
import { api, ApiError, AskResponse, ConnectResponse, ragHeaders } from '../api';

const TOKEN_KEY = 'course-rag-token';
const SESSION_KEY = 'course-rag-session';
const EXPIRES_KEY = 'course-rag-session-expires';

export default function ChatPage() {
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY) || '');
  const [sessionId, setSessionId] = useState(localStorage.getItem(SESSION_KEY) || '');
  const [expiresAt, setExpiresAt] = useState(localStorage.getItem(EXPIRES_KEY) || '');
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<AskResponse | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!token || !sessionId) return;
    const timer = window.setInterval(() => {
      api('/api/auth/heartbeat', { method: 'POST', headers: ragHeaders(token, sessionId) }).catch(() => undefined);
    }, 60_000);
    return () => window.clearInterval(timer);
  }, [token, sessionId]);

  async function connect(event: FormEvent) {
    event.preventDefault();
    setError('');
    try {
      const data = await api<ConnectResponse>('/api/auth/connect', {
        method: 'POST',
        body: JSON.stringify({ token }),
      });
      setSessionId(data.session_id);
      setExpiresAt(data.expires_at);
      localStorage.setItem(TOKEN_KEY, token);
      localStorage.setItem(SESSION_KEY, data.session_id);
      localStorage.setItem(EXPIRES_KEY, data.expires_at);
    } catch (err) {
      const apiError = err as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    }
  }

  async function disconnect() {
    if (token && sessionId) {
      await api('/api/auth/disconnect', { method: 'POST', headers: ragHeaders(token, sessionId) }).catch(() => undefined);
    }
    setSessionId('');
    setExpiresAt('');
    localStorage.removeItem(SESSION_KEY);
    localStorage.removeItem(EXPIRES_KEY);
  }

  async function ask(event: FormEvent) {
    event.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    setError('');
    setAnswer(null);
    try {
      const data = await api<AskResponse>('/api/ask', {
        method: 'POST',
        headers: ragHeaders(token, sessionId),
        body: JSON.stringify({ question, top_k: 6 }),
      });
      setAnswer(data);
    } catch (err) {
      const apiError = err as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    } finally {
      setLoading(false);
    }
  }

  const connected = Boolean(token && sessionId);

  return (
    <main className="container">
      <section className="card stack">
        <h1>课程 RAG 助手</h1>
        {!connected ? (
          <form onSubmit={connect} className="stack">
            <p className="muted">使用兑换得到的 token 建立连接后才能访问 RAG 服务。一个 token 同时只能有一个活跃连接。</p>
            <input value={token} onChange={(event) => setToken(event.target.value)} placeholder="输入 token" />
            <button disabled={!token.trim()}>连接</button>
          </form>
        ) : (
          <div className="connection">
            <span>已连接，过期时间：{new Date(expiresAt).toLocaleString()}</span>
            <button type="button" onClick={disconnect}>断开连接</button>
          </div>
        )}
        {error && <div className="error">{error}</div>}
      </section>

      {connected && (
        <section className="card stack">
          <div className="examples">
            {['软件工程经济学是什么？', '如何进行软件成本估算？', '净现值法适合回答什么决策问题？'].map((text) => (
              <button key={text} type="button" onClick={() => setQuestion(text)}>{text}</button>
            ))}
          </div>
          <form onSubmit={ask} className="stack">
            <textarea value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="输入你的课程问题..." />
            <button disabled={loading || !question.trim()}>{loading ? '检索中...' : '提问'}</button>
          </form>
        </section>
      )}

      {answer && (
        <section className="stack">
          <article className="card answer">{answer.answer}</article>
          {answer.sources.map((source, index) => (
            <article className="card source" key={source.id}>
              <h3>资料 {index + 1}: {source.title}</h3>
              <div className="muted">来源：{source.source}{source.lesson ? ` | 章节：${source.lesson}` : ''}{source.topic ? ` | 主题：${source.topic}` : ''} | 分数：{source.score.toFixed(3)}</div>
              <pre>{source.content}</pre>
            </article>
          ))}
        </section>
      )}
    </main>
  );
}
