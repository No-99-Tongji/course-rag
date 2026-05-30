#!/usr/bin/env bash
# 测试基本流程：兑换邀请码 → 连接 → 问答 → 释放
# 用法: bash scripts/test_basic.sh <邀请码> [服务地址]

set -euo pipefail

INVITE_CODE="${1:?用法: bash scripts/test_basic.sh <邀请码> [服务地址]}"
BASE_URL="${2:-http://127.0.0.1:9000}"

echo "===== 1. 兑换邀请码 ====="
REDEEM=$(curl -sS -X POST "$BASE_URL/api/invites/redeem" \
  -H 'Content-Type: application/json' \
  -d "{\"invite_code\":\"$INVITE_CODE\"}")
echo "$REDEEM" | python3 -m json.tool

TOKEN=$(echo "$REDEEM" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
DERIVED=$(echo "$REDEEM" | python3 -c "import sys,json; print('\n'.join(json.load(sys.stdin).get('derived_invites',[])))")
echo ""
echo "Token: $TOKEN"
if [ -n "$DERIVED" ]; then
  echo "派生邀请码:"
  echo "$DERIVED"
fi

echo ""
echo "===== 2. 建立连接 ====="
CONNECT=$(curl -sS -X POST "$BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$TOKEN\"}")
echo "$CONNECT" | python3 -m json.tool
SESSION=$(echo "$CONNECT" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

echo ""
echo "===== 3. 问答: 软件工程经济学是什么？ ====="
curl -sS -X POST "$BASE_URL/api/ask" \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION" \
  -d '{"question":"软件工程经济学是什么？","top_k":3}' | python3 -m json.tool

echo ""
echo "===== 4. 检索: 净现值法 ====="
curl -sS "$BASE_URL/api/search?q=净现值法&top_k=3" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION" | python3 -m json.tool

echo ""
echo "===== 5. 释放连接 ====="
curl -sS -X POST "$BASE_URL/api/auth/disconnect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION" | python3 -m json.tool
