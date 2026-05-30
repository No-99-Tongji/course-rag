import { Link } from 'react-router-dom';

export default function ChatPage() {
  return (
    <main className="container stack">
      <section className="card stack">
        <h1>课程 RAG API 使用说明</h1>
        <p>还没有 token？先去 <Link to="/redeem">兑换 token</Link>。</p>
      </section>

      <section className="card stack">
        <h2>1. 用 token 建立连接</h2>
        <p>一个 token 同时只能建立一个活跃连接。如果已有连接，第二次连接会返回 <code>TOKEN_ALREADY_CONNECTED</code>。</p>
        <pre>{`curl -X POST <RAG服务地址>/api/auth/connect \\
  -H 'Content-Type: application/json' \\
  -d '{"token":"你的token"}'`}</pre>
        <p>成功后保存返回的 <code>session_id</code>。</p>
      </section>

      <section className="card stack">
        <h2>2. 调用问答 API</h2>
        <pre>{`curl -X POST <RAG服务地址>/api/ask \\
  -H 'Content-Type: application/json' \\
  -H 'Authorization: Bearer 你的token' \\
  -H 'X-Session-Id: sess_xxx' \\
  -d '{"question":"软件工程经济学是什么？","top_k":6}'`}</pre>
      </section>

      <section className="card stack">
        <h2>3. 调用检索 API</h2>
        <pre>{`curl '<RAG服务地址>/api/search?q=软件成本估算&top_k=5' \\
  -H 'Authorization: Bearer 你的token' \\
  -H 'X-Session-Id: sess_xxx'`}</pre>
      </section>

      <section className="card stack">
        <h2>4. 保持连接</h2>
        <p>客户端应按连接接口返回的 <code>heartbeat_interval_seconds</code> 定期发送心跳，否则 session 过期后需要重新连接。</p>
        <pre>{`curl -X POST <RAG服务地址>/api/auth/heartbeat \\
  -H 'Authorization: Bearer 你的token' \\
  -H 'X-Session-Id: sess_xxx'`}</pre>
      </section>

      <section className="card stack">
        <h2>5. 释放连接</h2>
        <pre>{`curl -X POST <RAG服务地址>/api/auth/disconnect \\
  -H 'Authorization: Bearer 你的token' \\
  -H 'X-Session-Id: sess_xxx'`}</pre>
      </section>
    </main>
  );
}
