#!/usr/bin/env bash
# 测试管理员接口
# 用法: bash scripts/test_admin.sh <用户名> <密码> [服务地址]

set -euo pipefail

USERNAME="${1:?用法: bash scripts/test_admin.sh <用户名> <密码> [服务地址]}"
PASSWORD="${2:?缺少密码参数}"
BASE_URL="${3:-http://127.0.0.1:9000}"

echo "===== 1. 管理员登录 ====="
LOGIN=$(curl -sS -D /tmp/admin_headers.txt -X POST "$BASE_URL/api/admin/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USERNAME\",\"password\":\"$PASSWORD\"}")
echo "$LOGIN" | python3 -m json.tool

COOKIE=$(grep -oi 'set-cookie: admin_session=[^;]*' /tmp/admin_headers.txt | cut -d= -f2 | head -1)
if [ -z "$COOKIE" ]; then
  echo "登录失败，未获取到 cookie"
  exit 1
fi
echo "Cookie: admin_session=$COOKIE"

echo ""
echo "===== 2. 创建原始邀请码 ====="
CREATE=$(curl -sS -X POST "$BASE_URL/api/admin/invites" \
  -H 'Content-Type: application/json' \
  -H "Cookie: admin_session=$COOKIE")
echo "$CREATE" | python3 -m json.tool

echo ""
echo "===== 3. 查看所有邀请码 ====="
curl -sS "$BASE_URL/api/admin/invites" \
  -H "Cookie: admin_session=$COOKIE" | python3 -m json.tool

echo ""
echo "===== 4. 查看所有 token ====="
curl -sS "$BASE_URL/api/admin/tokens" \
  -H "Cookie: admin_session=$COOKIE" | python3 -m json.tool

echo ""
echo "===== 5. 查看所有连接 ====="
curl -sS "$BASE_URL/api/admin/sessions" \
  -H "Cookie: admin_session=$COOKIE" | python3 -m json.tool

echo ""
echo "===== 6. 退出登录 ====="
curl -sS -X POST "$BASE_URL/api/admin/logout" \
  -H "Cookie: admin_session=$COOKIE" | python3 -m json.tool
