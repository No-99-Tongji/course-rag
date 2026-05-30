import { FormEvent, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api, ApiError } from '../api';

export default function AdminLoginPage() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError('');
    try {
      await api('/api/admin/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
      });
      navigate('/admin');
    } catch (err) {
      const apiError = err as ApiError;
      setError(`${apiError.code}: ${apiError.message}`);
    }
  }

  return (
    <main className="container narrow">
      <section className="card stack">
        <h1>管理员登录</h1>
        <form onSubmit={submit} className="stack">
          <input value={username} onChange={(event) => setUsername(event.target.value)} placeholder="用户名" />
          <input type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="密码" />
          <button disabled={!username || !password}>登录</button>
        </form>
        {error && <div className="error">{error}</div>}
      </section>
    </main>
  );
}
