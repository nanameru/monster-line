#!/usr/bin/env bash
# ============================================================
#  monster-line  ─  ステータスラインに住むモンスター育成
#  Claude Code を使うたびに経験値が溜まり、進化していく
# ============================================================

MONSTER_HOME="$HOME/.claude/monster"
SAVE_FILE="$MONSTER_HOME/save.json"

mkdir -p "$MONSTER_HOME"

# ─── セーブデータ初期化 ───
if [[ ! -f "$SAVE_FILE" ]]; then
  cat > "$SAVE_FILE" << 'JSON'
{"xp":0,"stage":1,"sessions":0,"last_gain":0,"hatched":"never"}
JSON
fi

save=$(cat "$SAVE_FILE")
xp=$(echo "$save" | /usr/bin/python3 -c "import sys,json;print(json.load(sys.stdin).get('xp',0))" 2>/dev/null || echo 0)
stage=$(echo "$save" | /usr/bin/python3 -c "import sys,json;print(json.load(sys.stdin).get('stage',1))" 2>/dev/null || echo 1)
sessions=$(echo "$save" | /usr/bin/python3 -c "import sys,json;print(json.load(sys.stdin).get('sessions',0))" 2>/dev/null || echo 0)
last_gain=$(echo "$save" | /usr/bin/python3 -c "import sys,json;print(json.load(sys.stdin).get('last_gain',0))" 2>/dev/null || echo 0)
hatched=$(echo "$save" | /usr/bin/python3 -c "import sys,json;print(json.load(sys.stdin).get('hatched','never'))" 2>/dev/null || echo "never")

now=$(date +%s)

# ─── 経験値の獲得（5分に1回） ───
elapsed=$(( now - last_gain ))
if (( elapsed > 300 )); then
  xp=$(( xp + 15 ))
  sessions=$(( sessions + 1 ))
  last_gain=$now

  if [[ "$hatched" == "never" ]]; then
    hatched=$(date +%Y-%m-%d)
  fi

  # ─── 進化チェック ───
  if   (( xp >= 6000 )); then stage=6
  elif (( xp >= 2500 )); then stage=5
  elif (( xp >= 1000 )); then stage=4
  elif (( xp >=  400 )); then stage=3
  elif (( xp >=  100 )); then stage=2
  else                        stage=1
  fi

  /usr/bin/python3 -c "
import json
d={'xp':$xp,'stage':$stage,'sessions':$sessions,'last_gain':$last_gain,'hatched':'$hatched'}
with open('$SAVE_FILE','w') as f: json.dump(d,f)
" 2>/dev/null
fi

# ─── アニメーションフレーム（秒ベース 4フレーム） ───
tick=$(( now % 4 ))

# ─── カラー定義 ───
_c() { printf "\x1b[38;2;%d;%d;%dm" "$1" "$2" "$3"; }
R="\x1b[0m"

# ステージごとのテーマカラー
case $stage in
  1) tint=$(_c 180 180 190) spark=$(_c 230 230 240) accent=$(_c 255 255 220) ;;
  2) tint=$(_c 80 210 120)  spark=$(_c 140 255 170) accent=$(_c 200 255 200) ;;
  3) tint=$(_c 240 160 50)  spark=$(_c 255 200 100) accent=$(_c 255 220 150) ;;
  4) tint=$(_c 200 50 70)   spark=$(_c 255 100 120) accent=$(_c 255 60 80)   ;;
  5) tint=$(_c 60 130 240)  spark=$(_c 120 180 255) accent=$(_c 255 140 40)  ;;
  6) tint=$(_c 255 200 40)  spark=$(_c 255 230 100) accent=$(_c 255 255 180) ;;
esac

soft=$(_c 100 100 110)
txt=$(_c 190 190 200)
dim=$(_c 70 70 80)

# ─── モンスターのアスキーアート（複数行・4フレームアニメーション） ───
# 各ステージは3行のアートを出力する（line_a, line_b, line_c）

render_monster() {
  case $stage in

    1) # ─── たまご ─ ゆらゆら揺れて光が走る ───
      case $tick in
        0)
          line_a="    ${tint}╭───╮${R}"
          line_b="    ${tint}│${spark} ○ ${tint}│${R}"
          line_c="    ${tint}╰───╯${R}"
          ;;
        1)
          line_a="     ${tint}╭───╮${R}"
          line_b="     ${tint}│${accent}◎${spark} ·${tint}│${R}"
          line_c="     ${tint}╰───╯${R}"
          ;;
        2)
          line_a="    ${tint}╭───╮${R}"
          line_b="    ${tint}│${spark} · ${accent}◎${tint}│${R}"
          line_c="    ${tint}╰───╯${R}"
          ;;
        3)
          line_a="   ${tint}╭───╮${R}"
          line_b="   ${tint}│ ${accent}◉${spark} ·${tint}│${R}"
          line_c="   ${tint}╰───╯${R}"
          ;;
      esac ;;

    2) # ─── スライム ─ ぷるぷる弾む ───
      case $tick in
        0)
          line_a="    ${tint}╭─◠─╮${R}"
          line_b="    ${tint}│${spark}◕‿◕${tint}│${R}"
          line_c="    ${tint}╰───╯${R}"
          ;;
        1)
          line_a="   ${tint}╭──◠──╮${R}"
          line_b="   ${tint}│${spark} ◕‿◕ ${tint}│${R}"
          line_c="   ${tint}╰─────╯${R}"
          ;;
        2)
          line_a="    ${tint}╭─◠─╮${R}"
          line_b="    ${tint}│${spark}◕⌄◕${tint}│${R}"
          line_c="    ${tint}╰───╯${R}"
          ;;
        3)
          line_a="   ${tint}╭──◠──╮${R}"
          line_b="   ${tint}│${spark} ◕⌄◕ ${tint}│${R}"
          line_c="   ${tint}╰─────╯${R}"
          ;;
      esac ;;

    3) # ─── ウルフ ─ 耳がぴくぴく、しっぽ振る ───
      case $tick in
        0)
          line_a="   ${spark}∧ ∧${R}"
          line_b="   ${tint}(・ω・)${spark}~${R}"
          line_c="   ${tint} /  \\${R}"
          ;;
        1)
          line_a="   ${spark}∧ ˅${R}"
          line_b="   ${tint}(・ω・)${spark}~~${R}"
          line_c="   ${tint} /  \\${R}"
          ;;
        2)
          line_a="   ${spark}˅ ∧${R}"
          line_b="   ${tint}(・ω・)${spark}~${R}"
          line_c="   ${tint} /  \\${R}"
          ;;
        3)
          line_a="   ${spark}∧ ∧${R}"
          line_b="   ${tint}(・ω・)${spark}~~${R}"
          line_c="   ${tint} /  \\${R}"
          ;;
      esac ;;

    4) # ─── アクマ ─ 翼をはためかせ、角が光る ───
      case $tick in
        0)
          line_a="  ${accent}† ${spark}∨∨${accent} †${R}"
          line_b="  ${tint}}${accent}(▼皿▼)${tint}{${R}"
          line_c="   ${tint} /||\\${R}"
          ;;
        1)
          line_a="  ${accent}†${spark} ∨∨ ${accent}†${R}"
          line_b=" ${tint}} ${accent}(▼皿▼) ${tint}{${R}"
          line_c="   ${tint}  /||\\${R}"
          ;;
        2)
          line_a="  ${accent}‡ ${spark}∨∨${accent} ‡${R}"
          line_b="  ${tint}]${accent}(▼益▼)${tint}[${R}"
          line_c="   ${tint} /||\\${R}"
          ;;
        3)
          line_a="  ${accent}‡${spark} ∨∨ ${accent}‡${R}"
          line_b=" ${tint}] ${accent}(▼益▼) ${tint}[${R}"
          line_c="   ${tint}  /||\\${R}"
          ;;
      esac ;;

    5) # ─── リュウ ─ 翼を広げて炎を吐く ───
      case $tick in
        0)
          line_a="  ${spark}/\\ ${tint}◇◇${spark} /\\${R}"
          line_b="  ${tint}  (◇ᴗ◇)>${R}"
          line_c="  ${tint}  /╱ ╲\\${R}"
          ;;
        1)
          line_a=" ${spark}/\\  ${tint}◇◇${spark}  /\\${R}"
          line_b="  ${tint}  (◇ᴗ◇)>${accent}~${R}"
          line_c="  ${tint}  /╱ ╲\\${R}"
          ;;
        2)
          line_a="  ${spark}/\\ ${tint}◇◇${spark} /\\${R}"
          line_b="  ${tint}  (◇ᴗ◇)>${accent}≈~${R}"
          line_c="  ${tint}  /╱ ╲\\${R}"
          ;;
        3)
          line_a=" ${spark}/\\  ${tint}◇◇${spark}  /\\${R}"
          line_b="  ${tint}  (◇ᴗ◇)>${accent}彡≈${R}"
          line_c="  ${tint}  /╱ ╲\\${R}"
          ;;
      esac ;;

    6) # ─── シンリュウ ─ 神々しいオーラと光の粒子 ───
      case $tick in
        0)
          line_a=" ${accent}  ✦  ${spark}◇◇${accent}  ✦${R}"
          line_b=" ${accent}.*${tint}(≖ᴗ≖)${accent}*.${R}"
          line_c=" ${spark} ✧ ${dim}⋰⋱⋰${spark} ✧${R}"
          ;;
        1)
          line_a=" ${accent} ✧ ${spark}◇◇${accent} ✧${R}"
          line_b=" ${accent}*.${tint}(≖‿≖)${accent}.*${R}"
          line_c=" ${spark}  ✦${dim}⋱⋰⋱${spark}✦${R}"
          ;;
        2)
          line_a=" ${accent}  ✦  ${spark}◇◇${accent}  ✦${R}"
          line_b=" ${accent}·*${tint}(≖ᴗ≖)${accent}*·${R}"
          line_c=" ${spark} ✧ ${dim}⋰⋱⋰${spark} ✧${R}"
          ;;
        3)
          line_a=" ${accent} ✧  ${spark}◇◇${accent}  ✧${R}"
          line_b=" ${accent}*·${tint}(≖‿≖)${accent}·*${R}"
          line_c=" ${spark}  ✦${dim}⋱⋰⋱${spark}✦${R}"
          ;;
      esac ;;
  esac
}

# ─── ステージ名 ───
stage_name() {
  case $stage in
    1) echo "タマゴ"   ;;
    2) echo "スライム" ;;
    3) echo "ウルフ"   ;;
    4) echo "アクマ"   ;;
    5) echo "リュウ"   ;;
    6) echo "シンリュウ" ;;
  esac
}

# ─── 進化ゲージ ───
evo_gauge() {
  local cur_xp=$1
  local lo hi pct filled empty bar i

  case $stage in
    1) lo=0;    hi=100  ;;
    2) lo=100;  hi=400  ;;
    3) lo=400;  hi=1000 ;;
    4) lo=1000; hi=2500 ;;
    5) lo=2500; hi=6000 ;;
    6) printf "MAX"; return ;;
  esac

  pct=$(( (cur_xp - lo) * 100 / (hi - lo) ))
  (( pct > 100 )) && pct=100

  filled=$(( pct * 6 / 100 ))
  empty=$(( 6 - filled ))

  bar=""
  for (( i=0; i<filled; i++ )); do bar+="■"; done
  for (( i=0; i<empty;  i++ )); do bar+="□"; done

  printf "%s %d%%" "$bar" "$pct"
}

# ─── 出力を組み立て ───
render_monster
name=$(stage_name)
gauge=$(evo_gauge "$xp")
lv=$(( xp / 15 + 1 ))

# モンスターアート（3行）の右側に情報を付ける
info_a="${spark}${name}${R} ${soft}Lv.${lv}${R}"

if (( stage < 6 )); then
  info_b="${soft}EVO ${tint}${gauge}${R}"
  info_c="${txt}${xp}xp${R} ${soft}│${R} ${txt}${sessions}回${R}"
else
  info_b="${spark}★ ${gauge} ★${R}"
  info_c="${txt}${xp}xp${R} ${soft}│${R} ${txt}${sessions}回${R}"
fi

printf "%b  %b\n%b  %b\n%b  %b" \
  "$line_a" "$info_a" \
  "$line_b" "$info_b" \
  "$line_c" "$info_c"
