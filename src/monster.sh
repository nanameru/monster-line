#!/usr/bin/env bash
# ============================================================
#  monster-line  ─  たまごっち風モンスター育成ステータスライン
#  Claude Code を使うたびに経験値が溜まり、進化していく
#  モンスターは画面内を左右に歩き回る！
#  chafa で生成したピクセルアートで描画
# ============================================================

MONSTER_HOME="$HOME/.claude/monster"
SAVE_FILE="$MONSTER_HOME/save.json"
ART_DIR="$MONSTER_HOME/art"

mkdir -p "$MONSTER_HOME" "$ART_DIR"

# ─── セーブデータ初期化 ───
if [[ ! -f "$SAVE_FILE" ]]; then
  cat > "$SAVE_FILE" << 'JSON'
{"xp":0,"stage":1,"sessions":0,"last_gain":0,"hatched":"never"}
JSON
fi

# ─── セーブデータ読み込み ───
read_save() {
  /usr/bin/python3 -c "
import json
with open('$SAVE_FILE') as f: d=json.load(f)
print(d.get('xp',0))
print(d.get('stage',1))
print(d.get('sessions',0))
print(d.get('last_gain',0))
print(d.get('hatched','never'))
" 2>/dev/null
}

IFS=$'\n' read -r -d '' xp stage sessions last_gain hatched < <(read_save && printf '\0') || true
xp=${xp:-0}; stage=${stage:-1}; sessions=${sessions:-0}; last_gain=${last_gain:-0}; hatched=${hatched:-never}

now=$(date +%s)

# ─── 経験値の獲得（5分に1回） ───
elapsed=$(( now - last_gain ))
if (( elapsed > 300 )); then
  xp=$(( xp + 15 ))
  sessions=$(( sessions + 1 ))
  last_gain=$now
  [[ "$hatched" == "never" ]] && hatched=$(date +%Y-%m-%d)

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

# ─── 歩行アニメーション計算 ───
walk_frame=$(( now % 3 ))

# 位置: 10秒かけて右に行って左に戻る (0→5→0)
pos_cycle=$(( now % 10 ))
if (( pos_cycle <= 5 )); then
  pos=$pos_cycle
else
  pos=$(( 10 - pos_cycle ))
fi

# バウンスアニメーション（フレームごとに上下）
case $walk_frame in
  0) bounce=0 ;;
  1) bounce=1 ;;
  2) bounce=0 ;;
esac

# ─── カラーヘルパー ───
fg() { printf "\x1b[38;2;%d;%d;%dm" "$1" "$2" "$3"; }
R="\x1b[0m"

# ─── ステージ情報 ───
case $stage in
  1) c1=$(fg 225 200 170) c2=$(fg 245 235 215) label="タマゴ"     art_file="egg"       ;;
  2) c1=$(fg 60 200 100)  c2=$(fg 120 255 150) label="スライム"   art_file="slime"     ;;
  3) c1=$(fg 180 150 100) c2=$(fg 220 200 160) label="ウルフ"     art_file="wolf"      ;;
  4) c1=$(fg 190 40 60)   c2=$(fg 255 80 100)  label="アクマ"     art_file="demon"     ;;
  5) c1=$(fg 50 120 220)  c2=$(fg 100 170 255) label="リュウ"     art_file="dragon"    ;;
  6) c1=$(fg 255 200 30)  c2=$(fg 255 240 120) label="シンリュウ" art_file="goddragon" ;;
esac

ui=$(fg 90 90 100)
tx=$(fg 180 180 190)

# ─── スペーサー ───
pad=""
for (( i=0; i<pos; i++ )); do pad+=" "; done

# ─── 進化ゲージ ───
evo_gauge() {
  local lo hi pct filled empty bar i
  case $stage in
    1) lo=0;    hi=100  ;;
    2) lo=100;  hi=400  ;;
    3) lo=400;  hi=1000 ;;
    4) lo=1000; hi=2500 ;;
    5) lo=2500; hi=6000 ;;
    6) printf "${c2}★ MAX ★${R}"; return ;;
  esac

  pct=$(( (xp - lo) * 100 / (hi - lo) ))
  (( pct > 100 )) && pct=100
  filled=$(( pct * 8 / 100 ))
  empty=$(( 8 - filled ))

  bar=""
  for (( i=0; i<filled; i++ )); do bar+="■"; done
  for (( i=0; i<empty;  i++ )); do bar+="□"; done
  printf "%s %d%%" "$bar" "$pct"
}

# ─── 最終出力 ───
lv=$(( xp / 15 + 1 ))
gauge=$(evo_gauge)

# 情報パネル
info_0="${c2}${label}${R} ${ui}Lv.${lv}${R}"
if (( stage < 6 )); then
  info_1="${ui}EVO ${c1}${gauge}${R}"
else
  info_1="${gauge}"
fi
info_2="${tx}${xp}${ui}xp${R} ${ui}│${R} ${tx}${sessions}${ui}回${R}"

# ─── アートファイル読み込み＆描画 ───
art_path="$ART_DIR/${art_file}.txt"

if [[ -f "$art_path" ]]; then
  # chafa生成のANSIアートを使用
  line_num=0
  total_lines=8

  # バウンス効果: フレーム1の時は空行を先頭に1行追加
  if (( bounce == 1 )); then
    printf "\n"
  fi

  while IFS= read -r line; do
    if (( line_num == 0 )); then
      printf "%s%s   %b\n" "$pad" "$line" "$info_0"
    elif (( line_num == 1 )); then
      printf "%s%s   %b\n" "$pad" "$line" "$info_1"
    elif (( line_num == 2 )); then
      printf "%s%s   %b\n" "$pad" "$line" "$info_2"
    else
      printf "%s%s\n" "$pad" "$line"
    fi
    (( line_num++ ))
  done < "$art_path"

  # バウンスしていない時は末尾に空行追加（高さ揃え）
  if (( bounce == 0 )); then
    printf "\n"
  fi
else
  # アートファイルが見つからない場合のフォールバック
  printf "%b%s Lv.%d  %dxp\n" "$c2" "$label" "$lv" "$xp"
fi
