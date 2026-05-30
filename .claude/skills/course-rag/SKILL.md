---
name: course-rag
description: Query the Software Engineering Economics course RAG service for course facts, definitions, concepts, slides, transcript content, and citations. Use when the user asks about this course or wants information from the course materials.
---

# Course RAG Skill

Use this skill to answer questions from the local Software Engineering Economics course RAG service.

## What this skill does

It calls the course RAG HTTP API, retrieves relevant course chunks, and uses the returned answer and sources to respond with course-grounded information.

## Required environment

The RAG service must be running and reachable.

Defaults:

- `COURSE_RAG_BASE_URL`: `http://127.0.0.1:8000`
- `COURSE_RAG_TOKEN`: required unless the user provides a token in the prompt

The token is obtained from the course RAG invite-code flow. A token can only have one active connection at a time.

## Workflow

1. Determine the user's course question from the prompt.
2. Get the token:
   - Prefer `COURSE_RAG_TOKEN` from the environment.
   - If unavailable, ask the user for a token.
   - Do not invent or guess a token.
3. Connect to the RAG service:

```bash
curl -sS -X POST "$COURSE_RAG_BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$COURSE_RAG_TOKEN\"}"
```

4. If the response is `TOKEN_ALREADY_CONNECTED`, tell the user that this token already has an active connection and ask them to disconnect the other client or provide another token.
5. Save the returned `session_id`.
6. Ask the RAG service:

```bash
curl -sS -X POST "$COURSE_RAG_BASE_URL/api/ask" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $COURSE_RAG_TOKEN" \
  -H "X-Session-Id: $SESSION_ID" \
  -d "{\"question\":\"$QUESTION\",\"top_k\":6}"
```

7. Disconnect after the query:

```bash
curl -sS -X POST "$COURSE_RAG_BASE_URL/api/auth/disconnect" \
  -H "Authorization: Bearer $COURSE_RAG_TOKEN" \
  -H "X-Session-Id: $SESSION_ID" >/dev/null
```

## Response style

- Answer in Chinese by default unless the user asks otherwise.
- Ground the answer in the returned `answer` and `sources` fields.
- Include a concise "来源" section listing the most relevant source titles and filenames.
- If the RAG service returns insufficient information, say that the course materials do not contain enough evidence.
- Do not claim information comes from the course unless it appears in the returned RAG result.

## Robust curl helper

For normal use, prefer this single shell snippet because it safely JSON-encodes the question and always disconnects if connection succeeds:

```bash
python - <<'PY'
import json
import os
import sys
import urllib.error
import urllib.request

base_url = os.getenv("COURSE_RAG_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
token = os.getenv("COURSE_RAG_TOKEN")
question = os.getenv("COURSE_RAG_QUESTION") or " ".join(sys.argv[1:])

if not token:
    raise SystemExit("COURSE_RAG_TOKEN is not set")
if not question:
    raise SystemExit("Question is empty")

def request(path, payload=None, headers=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        base_url + path,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST" if payload is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return exc.code, json.loads(body)
        except json.JSONDecodeError:
            return exc.code, {"detail": body}

status, connected = request("/api/auth/connect", {"token": token})
if status != 200:
    print(json.dumps(connected, ensure_ascii=False, indent=2))
    raise SystemExit(1)

session_id = connected["session_id"]
try:
    status, answer = request(
        "/api/ask",
        {"question": question, "top_k": 6},
        {"Authorization": f"Bearer {token}", "X-Session-Id": session_id},
    )
    print(json.dumps(answer, ensure_ascii=False, indent=2))
    raise SystemExit(0 if status == 200 else 1)
finally:
    request(
        "/api/auth/disconnect",
        {},
        {"Authorization": f"Bearer {token}", "X-Session-Id": session_id},
    )
PY
```

Set `COURSE_RAG_QUESTION` before running the helper, or pass the question as command arguments.
