#!/usr/bin/env bash
# 批量测试多个课程问题的 RAG 效果
# 用法: bash scripts/test_batch_queries.sh <token> [服务地址] [top_k]

set -euo pipefail

TOKEN="${1:?用法: bash scripts/test_batch_queries.sh <token> [服务地址] [top_k]}"
BASE_URL="${2:-http://127.0.0.1:9000}"
TOP_K="${3:-6}"

QUESTIONS=(
  "软件工程经济学是什么？"
  "如何进行软件成本估算？"
  "净现值法适合回答什么决策问题？"
  "什么是资金时间价值？"
  "软件工程经济学有哪些研究对象？"
  "软件工程经济学有哪些经济分析方法？"
  "什么是足够好原则？"
  "软件项目的可行性分析是什么？"
  "什么是软件工程经济学的三个原则？"
  "风险分析在软件项目中有什么作用？"
)

echo "连接服务..."
CONNECT=$(curl -sS -X POST "$BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$TOKEN\"}")
SESSION=$(echo "$CONNECT" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")
echo "Session: $SESSION"
echo ""

for i in "${!QUESTIONS[@]}"; do
  Q="${QUESTIONS[$i]}"
  echo "================================================================"
  echo "问题 $((i+1))/${#QUESTIONS[@]}: $Q"
  echo "================================================================"

  RESULT=$(curl -sS -X POST "$BASE_URL/api/ask" \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN" \
    -H "X-Session-Id: $SESSION" \
    -d "{\"question\":\"$Q\",\"top_k\":$TOP_K}")

  echo "$RESULT" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print()
print('【回答】')
print(data.get('answer', '')[:300])
print()
print('【来源】')
for s in data.get('sources', []):
    print(f\"  [{s['score']:.3f}] {s['title']} ({s['source']})\")
"
  echo ""
done

echo "释放连接..."
curl -sS -X POST "$BASE_URL/api/auth/disconnect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION" >/dev/null
echo "完成"
