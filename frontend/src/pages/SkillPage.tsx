import { Link } from 'react-router-dom';

export default function SkillPage() {
  return (
    <main className="container stack">
      <section className="card stack">
        <h1>Claude Code Skill 安装与使用</h1>
        <p className="muted">安装 Course RAG Skill 后，可以在 Claude Code 中直接用自然语言查询课程内容。</p>
      </section>

      <section className="card stack">
        <h2>安装方式</h2>

        <h3>方式 1：添加 marketplace（推荐）</h3>
        <p>在 Claude Code 中依次执行：</p>
        <pre>{`/plugin marketplace add https://github.com/No-99-Tongji/course-rag-plugin`}</pre>
        <pre>{`/plugin install course-rag`}</pre>

        <h3>方式 2：本地安装</h3>
        <pre>{`git clone https://github.com/No-99-Tongji/course-rag-plugin.git
/plugin install --plugin-dir course-rag-plugin/course-rag-plugin`}</pre>

        <h3>方式 3：手动复制</h3>
        <pre>{`mkdir -p ~/.claude/skills/course-rag
curl -o ~/.claude/skills/course-rag/SKILL.md https://raw.githubusercontent.com/No-99-Tongji/course-rag-plugin/main/skills/course-rag/SKILL.md`}</pre>
      </section>

      <section className="card stack">
        <h2>配置服务地址</h2>
        <p>安装后需要设置 RAG 服务地址：</p>
        <pre>{`/config COURSE_RAG_BASE_URL=http://${window.location.hostname}:${window.location.port || '9000'}`}</pre>
        <p className="muted">如果服务部署在其他地址，请替换为实际 IP 和端口。</p>
      </section>

      <section className="card stack">
        <h2>使用方式</h2>
        <p>在 Claude Code 中使用 <code>/course-rag</code> 命令，必须提供两个参数：</p>
        <pre>{`/course-rag token=你的token 你的课程问题`}</pre>
        <p>示例：</p>
        <pre>{`/course-rag token=cr_xxxxxxxx 什么是软件成本估算？`}</pre>
        <pre>{`/course-rag token=cr_xxxxxxxx 净现值法适合回答什么决策问题？`}</pre>
      </section>

      <section className="card stack">
        <h2>获取 Token</h2>
        <p>Token 通过邀请码兑换获得：</p>
        <ol>
          <li>前往 <Link to="/redeem">兑换页面</Link></li>
          <li>输入邀请码，点击兑换</li>
          <li>复制返回的 token（只显示一次）</li>
        </ol>
        <p className="muted">如果兑换的是原始邀请码，还会额外获得 2 个派生邀请码，可以分享给其他同学。</p>
      </section>

      <section className="card stack">
        <h2>常见问题</h2>

        <div>
          <h3>提示 TOKEN_ALREADY_CONNECTED</h3>
          <p>说明你的 token 已经在其他地方连接了。需要先断开其他连接，或使用新 token。</p>
        </div>

        <div>
          <h3>提示 TOKEN_INVALID</h3>
          <p>Token 无效或已被撤销。请重新兑换一个。</p>
        </div>

        <div>
          <h3>回答不准确</h3>
          <p>可以尝试更具体地描述问题，或查看 <Link to="/chat">API 使用说明</Link> 了解如何调整 <code>top_k</code> 参数。</p>
        </div>
      </section>
    </main>
  );
}
