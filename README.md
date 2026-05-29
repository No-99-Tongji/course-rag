# 课程 RAG 系统

这是一个面向软件工程经济学课程资料的 RAG Web 服务，已整合：

- 网课视频音轨转录结构化语料：`data/processed/rag_corpus/`
- PPT 与规范 PDF 解析 Markdown：`data/processed/pdf_markdown/`
- 原始 PDF：`data/raw/pdfs/`
- 原始视频转录：`data/raw/video_transcripts/`

系统使用 `sentence-transformers` 的多语言 embedding 模型 `intfloat/multilingual-e5-small` 做向量检索，因此中文问题也可以召回英文 PPT/PDF 语料；配置 OpenAI 兼容接口后，会基于检索结果生成自然语言回答。

## 目录结构

```text
app/                         FastAPI 应用
static/                      Web 页面
scripts/build_index.py       构建文档索引
scripts/build_embeddings.py  构建多语言向量索引
data/raw/                    原始资料
data/processed/              处理后的 Markdown / JSONL 语料
data/index/                  生成的检索索引，运行脚本后出现
pyproject.toml                uv 项目依赖配置
Dockerfile                   容器部署配置
docker-compose.yml           Docker Compose 部署配置
```

## 本地运行

```bash
uv sync
uv run python scripts/build_index.py
uv run python scripts/build_embeddings.py
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

打开：`http://localhost:8000`

## 配置

项目通过 `.env` 文件配置环境变量。首次使用请复制示例：

```bash
cp .env.example .env
```

然后编辑 `.env` 填入实际密钥。

### Embedding 模型

默认使用本地 `intfloat/multilingual-e5-small` 模型，无需密钥。如需使用 Qwen Embedding 服务（中文语义更强），在 `.env` 中设置：

```env
EMBEDDING_PROVIDER=qwen
DASHSCOPE_API_KEY=你的DashScope API Key
```

切换 embedding 后需要重建索引：

```bash
uv run python scripts/build_index.py
uv run python scripts/build_embeddings.py
```

### 大模型问答

不配置 `OPENAI_API_KEY` 时，系统返回检索到的课程资料摘要。若要生成综合回答，在 `.env` 中设置：

```env
OPENAI_API_KEY=你的密钥
OPENAI_BASE_URL=https://你的兼容接口地址/v1
OPENAI_MODEL=gpt-4o-mini
```

## Docker 部署

在服务器上准备 `.env` 文件（参考 `.env.example`），然后：

```bash
docker compose up -d --build
```

访问服务器：`http://服务器IP:8000`

更新 `.env` 后重新启动：

```bash
docker compose up -d --build
```

## API

### 健康检查

```bash
curl http://localhost:8000/health
```

### 检索

```bash
curl 'http://localhost:8000/api/search?q=软件成本估算&top_k=5'
```

### 问答

```bash
curl -X POST http://localhost:8000/api/ask \
  -H 'Content-Type: application/json' \
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
