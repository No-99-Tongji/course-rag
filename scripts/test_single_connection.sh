#!/usr/bin/env bash
# 测试单 token 单连接约束
# 用法: bash scripts/test_single_connection.sh <token> [服务地址]

set -euo pipefail

TOKEN="${1:?用法: bash scripts/test_single_connection.sh <token> [服务地址]}"
BASE_URL="${2:-http://127.0.0.1:9000}"

echo "===== 第一次连接（应该成功） ====="
C1=$(curl -sS -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$TOKEN\"}")
CODE1=$(echo "$C1" | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
BODY1=$(echo "$C1" | sed 's/HTTP_CODE:.*//')
echo "$BODY1" | python3 -m json.tool
echo "HTTP 状态码: $CODE1"

SESSION=$(echo "$BODY1" | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

echo ""
echo "===== 第二次连接（应该返回 409 TOKEN_ALREADY_CONNECTED） ====="
C2=$(curl -sS -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$TOKEN\"}")
CODE2=$(echo "$C2" | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
BODY2=$(echo "$C2" | sed 's/HTTP_CODE:.*//')
echo "$BODY2" | python3 -m json.tool
echo "HTTP 状态码: $CODE2"

echo ""
if [ "$CODE2" = "409" ]; then
  echo "✅ 通过：第二次连接正确返回 409"
else
  echo "❌ 失败：期望 409，实际 $CODE2"
fi

echo ""
echo "===== 释放连接 ====="
curl -sS -X POST "$BASE_URL/api/auth/disconnect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $SESSION" | python3 -m json.tool

echo ""
echo "===== 释放后再次连接（应该成功） ====="
C3=$(curl -sS -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/auth/connect" \
  -H 'Content-Type: application/json' \
  -d "{\"token\":\"$TOKEN\"}")
CODE3=$(echo "$C3" | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
echo "HTTP 状态码: $CODE3"

if [ "$CODE3" = "200" ]; then
  echo "✅ 通过：释放后重新连接成功"
else
  echo "❌ 失败：期望 200，实际 $CODE3"
fi

# 清理
S3=$(echo "$C3" | sed 's/HTTP_CODE:.*//' | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")
curl -sS -X POST "$BASE_URL/api/auth/disconnect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Session-Id: $S3" >/dev/null
