#!/usr/bin/env bash
# ============================================================
#  monster-line セットアップスクリプト
#  Claude Code のステータスラインにモンスターを召喚する
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude/monster.sh"
SETTINGS="$HOME/.claude/settings.json"

echo ""
echo "  ╔══════════════════════════════════╗"
echo "  ║   monster-line  セットアップ     ║"
echo "  ╚══════════════════════════════════╝"
echo ""

# ─── 依存チェック ───
if ! command -v python3 &>/dev/null; then
  echo "  ✗ python3 が必要です"
  exit 1
fi

echo "  ✓ 依存チェック OK"

# ─── スクリプトをコピー ───
cp "$SCRIPT_DIR/src/monster.sh" "$DEST"
chmod +x "$DEST"
echo "  ✓ monster.sh → $DEST"

# ─── モンスターデータディレクトリ作成 ───
mkdir -p "$HOME/.claude/monster/art"
echo "  ✓ セーブデータ領域を作成"

# ─── アートファイルをコピー ───
for f in egg slime wolf demon dragon goddragon; do
  if [[ -f "$SCRIPT_DIR/assets/${f}_clean.txt" ]]; then
    cp "$SCRIPT_DIR/assets/${f}_clean.txt" "$HOME/.claude/monster/art/${f}.txt"
  fi
done
echo "  ✓ モンスターアート → ~/.claude/monster/art/"

# ─── settings.json を更新 ───
if [[ -f "$SETTINGS" ]]; then
  # 既存の設定をバックアップ
  cp "$SETTINGS" "${SETTINGS}.monster-bak"
  echo "  ✓ 既存設定をバックアップ → settings.json.monster-bak"

  # Python で安全に JSON を更新
  /usr/bin/python3 << 'PYEOF'
import json, sys

path = sys.argv[1] if len(sys.argv) > 1 else ""
settings_path = __import__("os").path.expanduser("~/.claude/settings.json")

with open(settings_path, "r") as f:
    settings = json.load(f)

settings["statusLine"] = {
    "type": "command",
    "command": 'bash "$HOME/.claude/monster.sh"'
}

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
PYEOF
else
  # 新規作成
  /usr/bin/python3 << 'PYEOF'
import json, os

settings_path = os.path.expanduser("~/.claude/settings.json")
settings = {
    "statusLine": {
        "type": "command",
        "command": 'bash "$HOME/.claude/monster.sh"'
    }
}

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2, ensure_ascii=False)
PYEOF
fi

echo "  ✓ Claude Code 設定を更新"

echo ""
echo "  ╭────────────────────────────────────╮"
echo "  │  セットアップ完了！                │"
echo "  │  Claude Code を再起動すると        │"
echo "  │  モンスターが現れます  ( ○ )       │"
echo "  ╰────────────────────────────────────╯"
echo ""
