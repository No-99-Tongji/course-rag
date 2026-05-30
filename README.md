# 课程 RAG 系统

这是一个面向软件工程经济学课程资料的 RAG Web 服务，已整合：

- 网课视频音轨转录结构化语料：`data/processed/rag_corpus/`
- PPT 与规范 PDF 解析 Markdown：`data/processed/pdf_markdown/`
- 原始 PDF：`data/raw/pdfs/`
- 原始视频转录：`data/raw/video_transcripts/`

系统使用向量检索，支持本地多语言 embedding 或 Qwen `text-embedding-v4`。服务现在需要先用邀请码兑换 token，再用 token 建立唯一活跃连接后访问 RAG。

## 目录结构

```text
app/                         FastAPI 应用
frontend/                    React 前端源码
static/                      React 构建产物
scripts/build_index.py       构建文档索引
scripts/build_embeddings.py  构建向量索引
data/raw/                    原始资料
data/processed/              处理后的 Markdown / JSONL 语料
data/index/                  生成的检索索引
pyproject.toml               uv 项目依赖配置
Dockerfile                   容器部署配置
docker-compose.yml           Docker Compose 部署配置
```

## 配置

首次使用请复制示例：

```bash
cp .env.example .env
```

至少需要配置：

```env
DATABASE_URL=mysql+aiomysql://course_rag:你的密码@mysql:3306/course_rag
ADMIN_BOOTSTRAP_USERNAME=admin
ADMIN_BOOTSTRAP_PASSWORD=你的管理员初始密码
ADMIN_JWT_SECRET=一个长随机字符串
```

如需使用 Qwen Embedding 服务：

```env
EMBEDDING_PROVIDER=qwen
DASHSCOPE_API_KEY=你的DashScope API Key
```

切换 embedding 后需要重建索引：

```bash
uv run python scripts/build_index.py
uv run python scripts/build_embeddings.py
```

## 本地开发

Python 后端：

```bash
uv sync
uv run python scripts/build_index.py
uv run python scripts/build_embeddings.py
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

React 前端：

```bash
npm install --prefix frontend
npm run dev --prefix frontend
```

生产构建前端：

```bash
npm run build --prefix frontend
```

## Docker 部署

在服务器上准备 `.env` 文件，然后：

```bash
docker compose up -d --build
```

访问服务器：`http://服务器IP:8000`

首次启动时，如果 `.env` 中设置了 `ADMIN_BOOTSTRAP_PASSWORD`，系统会创建初始管理员账号。登录 `/admin/login` 后可以生成原始邀请码。

## 使用流程

1. 管理员登录 `/admin/login`。
2. 在 `/admin` 生成原始邀请码，并复制保存。
3. 用户访问 `/redeem`，用邀请码兑换 token。
4. 如果兑换的是原始邀请码，系统会同时返回 2 个派生邀请码。
5. 用户访问 `/chat`，输入 token 建立连接后使用 RAG。
6. 一个 token 同时只能有一个活跃连接；如果已有连接，第二次连接会返回 `TOKEN_ALREADY_CONNECTED`。

## API

### 健康检查

```bash
curl http://localhost:8000/health
```

### 兑换邀请码

```bash
curl -X POST http://localhost:8000/api/invites/redeem \
  -H 'Content-Type: application/json' \
  -d '{"invite_code":"XXXX-XXXX-XXXX-XXXX"}'
```

### 建立 token 连接

```bash
curl -X POST http://localhost:8000/api/auth/connect \
  -H 'Content-Type: application/json' \
  -d '{"token":"cr_xxx"}'
```

### 问答

```bash
curl -X POST http://localhost:8000/api/ask \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer cr_xxx' \
  -H 'X-Session-Id: sess_xxx' \
  -d '{"question":"软件工程经济学是什么？","top_k":6}'
```

## 更新语料

1. 更新 `data/processed/rag_corpus/index.jsonl` 或 `data/processed/pdf_markdown/*.md`。
2. 重新构建索引：

```bash
uv run python scripts/build_index.py
uv run python scripts/build_embeddings.py
```

Docker 部署时重新构建镜像：

```bash
docker compose up -d --build
```
