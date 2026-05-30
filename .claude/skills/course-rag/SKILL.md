---
name: course-rag
description: Query the Software Engineering Economics course RAG service. Requires two arguments: token and question. Example: /course-rag token=cr_xxx 什么是软件成本估算？
---

# Course RAG Skill

使用课程 RAG 服务查询软件工程经济学课程信息。

## 必需参数

此 skill **必须**接收两个参数：

1. **token** — 用户的 RAG 访问 token（`cr_` 开头）
2. **question** — 要查询的课程问题

用法示例：

```
/course-rag token=cr_O6FuXkpG-EpMvUpo_b1yJifrckF4bjtYlnUrQZwumJM 什么是软件成本估算？
```

如果没有提供 token 或问题，应提示用户提供这两个参数，不要自行构造或猜测。

## 服务地址

通过环境变量 `COURSE_RAG_BASE_URL` 配置，默认为 `http://24.233.15.7:9000`。

## 执行流程

1. 从参数中解析 `token` 和 `question`。
2. 如果缺少任一参数，提示用户补全。
3. 使用 token 连接 RAG 服务：

```bash
curl -sS -X POST "$COURSE_RAG_BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$TOKEN\"}"
```

4. 如果返回 `TOKEN_ALREADY_CONNECTED`，告知用户该 token 已有活跃连接，请其断开其他连接或提供另一个 token。
5. 保存返回的 `session_id`。
6. 调用问答接口：

```bash
curl -sS -X POST "$COURSE_RAG_BASE_URL/api/ask" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION_ID" \
  -d "{\"question\":\"$QUESTION\",\"top_k\":6}"
```

7. 查询结束后断开连接：

```bash
curl -sS -X POST "$COURSE_RAG_BASE_URL/api/auth/disconnect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION_ID" >/dev/null
```

## 回答风格

- 默认用中文回答。
- 基于 RAG 返回的 `answer` 和 `sources` 组织回答。
- 末尾附上简洁的"来源"列表，列出相关资料标题和文件名。
- 如果 RAG 返回的信息不足，明确说明课程资料中未找到足够证据。
- 不要声称信息来自课程，除非它出现在 RAG 返回结果中。
