#!/usr/bin/env bash
# 测试邀请码链路：创建原始邀请码 → 兑换 → 用派生码再兑换
# 用法: bash scripts/test_invite_chain.sh <管理员cookie> [服务地址]
# cookie 格式: admin_session=eyJ...

set -euo pipefail

ADMIN_COOKIE="${1:?用法: bash scripts/test_invite_chain.sh <管理员cookie> [服务地址]}"
BASE_URL="${2:-http://127.0.0.1:9000}"

echo "===== 1. 管理员创建原始邀请码 ====="
CREATE=$(curl -sS -X POST "$BASE_URL/api/admin/invites" \
  -H 'Content-Type: application/json' \
  -H "Cookie: $ADMIN_COOKIE")
echo "$CREATE" | python3 -m json.tool
ORIGINAL=$(echo "$CREATE" | python3 -c "import sys,json; print(json.load(sys.stdin)['invite_code'])")
echo "原始邀请码: $ORIGINAL"

echo ""
echo "===== 2. 用户兑换原始邀请码 ====="
REDEEM1=$(curl -sS -X POST "$BASE_URL/api/invites/redeem" \
  -H 'Content-Type: application/json' \
  -d "{\"invite_code\":\"$ORIGINAL\"}")
echo "$REDEEM1" | python3 -m json.tool
TOKEN1=$(echo "$REDEEM1" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
DERIVED=$(echo "$REDEEM1" | python3 -c "import sys,json; [print(c) for c in json.load(sys.stdin).get('derived_invites',[])]")
echo "Token: $TOKEN1"
echo "派生邀请码:"
echo "$DERIVED"

# 取第一个派生码
DERIVED1=$(echo "$DERIVED" | head -1)

echo ""
echo "===== 3. 用第一个派生码兑换 ====="
REDEEM2=$(curl -sS -X POST "$BASE_URL/api/invites/redeem" \
  -H 'Content-Type: application/json' \
  -d "{\"invite_code\":\"$DERIVED1\"}")
echo "$REDEEM2" | python3 -m json.tool
TOKEN2=$(echo "$REDEEM2" | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
HAS_DERIVED=$(echo "$REDEEM2" | python3 -c "import sys,json; d=json.load(sys.stdin).get('derived_invites',[]); print(len(d))")
echo "Token: $TOKEN2"

if [ "$HAS_DERIVED" = "0" ]; then
  echo "✅ 通过：派生码兑换后不再产生新的派生码"
else
  echo "❌ 失败：派生码不应产生新派生码，但返回了 $HAS_DERIVED 个"
fi

echo ""
echo "===== 4. 再次兑换原始邀请码（应该失败 INVITE_REDEEMED） ====="
C=$(curl -sS -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/invites/redeem" \
  -H 'Content-Type: application/json' \
  -d "{\"invite_code\":\"$ORIGINAL\"}")
CODE=$(echo "$C" | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
echo "$C" | sed 's/HTTP_CODE:.*//' | python3 -m json.tool
if [ "$CODE" = "400" ]; then
  echo "✅ 通过：重复兑换返回 400"
else
  echo "❌ 失败：期望 400，实际 $CODE"
fi

echo ""
echo "===== 5. 用错误邀请码兑换（应该失败 INVITE_INVALID） ====="
C=$(curl -sS -w "\nHTTP_CODE:%{http_code}" -X POST "$BASE_URL/api/invites/redeem" \
  -H 'Content-Type: application/json' \
  -d '{"invite_code":"WRONG-CODE-0000"}')
CODE=$(echo "$C" | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
if [ "$CODE" = "400" ]; then
  echo "✅ 通过：错误邀请码返回 400"
else
  echo "❌ 失败：期望 400，实际 $CODE"
fi
