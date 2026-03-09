#!/usr/bin/env bash
# ============================================================
#  monster-line  ─  たまごっち風モンスター育成ステータスライン
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

# ─── セーブデータ読み込み（python3で一括パース） ───
read_save() {
  /usr/bin/python3 -c "
import json,sys
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

  # ─── 進化判定 ───
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

# ─── アニメーションフレーム ───
tick=$(( now % 4 ))

# ─── カラーヘルパー ───
fg() { printf "\x1b[38;2;%d;%d;%dm" "$1" "$2" "$3"; }
R="\x1b[0m"

# ─── ステージカラーパレット ───
case $stage in
  1) c1=$(fg 200 200 210) c2=$(fg 255 255 230) c3=$(fg 160 160 175) label="タマゴ" ;;
  2) c1=$(fg 60 200 100)  c2=$(fg 120 255 150) c3=$(fg 40 160 70)   label="スライム" ;;
  3) c1=$(fg 220 170 60)  c2=$(fg 255 210 100) c3=$(fg 180 130 30)  label="ウルフ" ;;
  4) c1=$(fg 190 40 60)   c2=$(fg 255 80 100)  c3=$(fg 140 20 40)   label="アクマ" ;;
  5) c1=$(fg 50 120 220)  c2=$(fg 100 170 255) c3=$(fg 255 130 30)  label="リュウ" ;;
  6) c1=$(fg 255 200 30)  c2=$(fg 255 240 120) c3=$(fg 200 160 20)  label="シンリュウ" ;;
esac

ui=$(fg 90 90 100)
tx=$(fg 180 180 190)

# ─── たまごっち風ドット絵モンスター（5行 x 4フレーム） ───
# 出力は lines 配列に格納される
declare -a lines

draw_monster() {
  case $stage in

    1) # ═══ たまご ═══ ゆらゆら揺れて中の光が動く
      case $tick in
        0)
          lines[0]="${c1}    ▄████▄${R}"
          lines[1]="${c1}   █${c3}░░░░░░${c1}█${R}"
          lines[2]="${c1}  █${c3}░░${c2}◦${c3}░░░${c1}█${R}"
          lines[3]="${c1}   █${c3}░░░░░░${c1}█${R}"
          lines[4]="${c1}    ▀████▀${R}"
          ;;
        1)
          lines[0]="${c1}     ▄████▄${R}"
          lines[1]="${c1}    █${c3}░░░░░░${c1}█${R}"
          lines[2]="${c1}   █${c3}░░░${c2}◎${c3}░░${c1}█${R}"
          lines[3]="${c1}    █${c3}░░░░░░${c1}█${R}"
          lines[4]="${c1}     ▀████▀${R}"
          ;;
        2)
          lines[0]="${c1}    ▄████▄${R}"
          lines[1]="${c1}   █${c3}░░░░░░${c1}█${R}"
          lines[2]="${c1}  █${c3}░░░░${c2}◦${c3}░${c1}█${R}"
          lines[3]="${c1}   █${c3}░░░░░░${c1}█${R}"
          lines[4]="${c1}    ▀████▀${R}"
          ;;
        3)
          lines[0]="${c1}   ▄████▄${R}"
          lines[1]="${c1}  █${c3}░░░░░░${c1}█${R}"
          lines[2]="${c1}  █${c3}░${c2}◎${c3}░░░░${c1}█${R}"
          lines[3]="${c1}  █${c3}░░░░░░${c1}█${R}"
          lines[4]="${c1}   ▀████▀${R}"
          ;;
      esac ;;

    2) # ═══ スライム ═══ ぷるぷる伸縮する
      case $tick in
        0)
          lines[0]="${c1}     ▄███▄${R}"
          lines[1]="${c1}    █${c2} ◕ ${c1}█${c2} ◕ ${c1}█${R}"
          lines[2]="${c1}    █${c2}  ▽  ${c1}█${R}"
          lines[3]="${c1}     █████${R}"
          lines[4]="${c3}      ▀▀▀${R}"
          ;;
        1)
          lines[0]="${c1}    ▄█████▄${R}"
          lines[1]="${c1}   █${c2} ◕  ${c1}█${c2}  ◕ ${c1}█${R}"
          lines[2]="${c1}   █${c2}   ▽   ${c1}█${R}"
          lines[3]="${c1}    ███████${R}"
          lines[4]="${c3}     ▀▀▀▀▀${R}"
          ;;
        2)
          lines[0]="${c1}     ▄███▄${R}"
          lines[1]="${c1}    █${c2} ◕ ${c1}█${c2} ◕ ${c1}█${R}"
          lines[2]="${c1}    █${c2}  ◡  ${c1}█${R}"
          lines[3]="${c1}     █████${R}"
          lines[4]="${c3}      ▀▀▀${R}"
          ;;
        3)
          lines[0]="${c1}    ▄█████▄${R}"
          lines[1]="${c1}   █${c2} ◕  ${c1}█${c2}  ◕ ${c1}█${R}"
          lines[2]="${c1}   █${c2}   ◡   ${c1}█${R}"
          lines[3]="${c1}    ███████${R}"
          lines[4]="${c3}     ▀▀▀▀▀${R}"
          ;;
      esac ;;

    3) # ═══ ウルフ ═══ 耳ぴくぴく＋しっぽ振り
      case $tick in
        0)
          lines[0]="${c2}  ∧     ∧${R}"
          lines[1]="${c1}  █${c2}◕${c1}██${c2}◕${c1}█${R}"
          lines[2]="${c1}  █${c2} ω ${c1}█${c2}~${R}"
          lines[3]="${c1}  █████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█ █${c3}▀${c1}█${R}"
          ;;
        1)
          lines[0]="${c2}  ∧     ˅${R}"
          lines[1]="${c1}  █${c2}◕${c1}██${c2}◕${c1}█${R}"
          lines[2]="${c1}  █${c2} ω ${c1}█${c2}~~${R}"
          lines[3]="${c1}  █████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█ █${c3}▀${c1}█${R}"
          ;;
        2)
          lines[0]="${c2}  ˅     ∧${R}"
          lines[1]="${c1}  █${c2}◕${c1}██${c2}◕${c1}█${R}"
          lines[2]="${c1}  █${c2} ω ${c1}█${c2}~${R}"
          lines[3]="${c1}  █████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█ █${c3}▀${c1}█${R}"
          ;;
        3)
          lines[0]="${c2}  ∧     ∧${R}"
          lines[1]="${c1}  █${c2}◕${c1}██${c2}◕${c1}█${R}"
          lines[2]="${c1}  █${c2} ω ${c1}█${c2}~~~${R}"
          lines[3]="${c1}  █████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█ █${c3}▀${c1}█${R}"
          ;;
      esac ;;

    4) # ═══ アクマ ═══ 翼バサバサ＋角が光る
      case $tick in
        0)
          lines[0]="${c2}  ☆ ${c1}▼▼${c2} ☆${R}"
          lines[1]="${c1} }█${c2}◣${c1}██${c2}◣${c1}█{${R}"
          lines[2]="${c1}  █${c2}  皿 ${c1}█${R}"
          lines[3]="${c1}  ██████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
        1)
          lines[0]="${c2}  ★ ${c1}▼▼${c2} ★${R}"
          lines[1]="${c1}}${c3}╲${c1}█${c2}◣${c1}██${c2}◣${c1}█${c3}╱${c1}{${R}"
          lines[2]="${c1}  █${c2} 益  ${c1}█${R}"
          lines[3]="${c1}  ██████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
        2)
          lines[0]="${c2}  ☆ ${c1}▼▼${c2} ☆${R}"
          lines[1]="${c1} ]█${c2}◣${c1}██${c2}◣${c1}█[${R}"
          lines[2]="${c1}  █${c2}  皿 ${c1}█${R}"
          lines[3]="${c1}  ██████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
        3)
          lines[0]="${c2}  ★ ${c1}▼▼${c2} ★${R}"
          lines[1]="${c1}]${c3}╲${c1}█${c2}◣${c1}██${c2}◣${c1}█${c3}╱${c1}[${R}"
          lines[2]="${c1}  █${c2} 益  ${c1}█${R}"
          lines[3]="${c1}  ██████${R}"
          lines[4]="${c1}  █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
      esac ;;

    5) # ═══ リュウ ═══ 翼を広げて炎を吐く
      case $tick in
        0)
          lines[0]="${c2} /▲${c1}  ◇◇  ${c2}▲\\${R}"
          lines[1]="${c1}   █${c2}◇${c1}██${c2}◇${c1}█${R}"
          lines[2]="${c1}   █${c2} ᴗ ${c1}█▸${R}"
          lines[3]="${c1}   ██████${R}"
          lines[4]="${c1}   █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
        1)
          lines[0]="${c2}/▲ ${c1}  ◇◇  ${c2} ▲\\${R}"
          lines[1]="${c1}   █${c2}◇${c1}██${c2}◇${c1}█${R}"
          lines[2]="${c1}   █${c2} ᴗ ${c1}█▸${c3}~${R}"
          lines[3]="${c1}   ██████${R}"
          lines[4]="${c1}   █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
        2)
          lines[0]="${c2} /▲${c1}  ◇◇  ${c2}▲\\${R}"
          lines[1]="${c1}   █${c2}◇${c1}██${c2}◇${c1}█${R}"
          lines[2]="${c1}   █${c2} ᴗ ${c1}█▸${c3}≈~${R}"
          lines[3]="${c1}   ██████${R}"
          lines[4]="${c1}   █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
        3)
          lines[0]="${c2}/▲ ${c1}  ◇◇  ${c2} ▲\\${R}"
          lines[1]="${c1}   █${c2}◇${c1}██${c2}◇${c1}█${R}"
          lines[2]="${c1}   █${c2} ᴗ ${c1}█▸${c3}彡≈${R}"
          lines[3]="${c1}   ██████${R}"
          lines[4]="${c1}   █${c3}▀${c1}█  █${c3}▀${c1}█${R}"
          ;;
      esac ;;

    6) # ═══ シンリュウ ═══ 神々しいオーラ＋光の粒子
      case $tick in
        0)
          lines[0]="${c2} ✦ ${c1} ◇◇ ${c2} ✦${R}"
          lines[1]="${c2}.*${c1}█${c2}≖${c1}██${c2}≖${c1}█${c2}*.${R}"
          lines[2]="${c1}  █${c2} ᴗ ${c1}█${R}"
          lines[3]="${c2}✧${c1}██████${c2}✧${R}"
          lines[4]="${c3} ⋰⋱ ${c2}▀▀${c3} ⋰⋱${R}"
          ;;
        1)
          lines[0]="${c2}✧  ${c1} ◇◇ ${c2}  ✧${R}"
          lines[1]="${c2}*.${c1}█${c2}≖${c1}██${c2}≖${c1}█${c2}.*${R}"
          lines[2]="${c1}  █${c2} ‿ ${c1}█${R}"
          lines[3]="${c2} ✦${c1}████${c2}✦${R}"
          lines[4]="${c3}  ⋱⋰${c2}▀▀${c3}⋱⋰${R}"
          ;;
        2)
          lines[0]="${c2} ✦ ${c1} ◇◇ ${c2} ✦${R}"
          lines[1]="${c2}·*${c1}█${c2}≖${c1}██${c2}≖${c1}█${c2}*·${R}"
          lines[2]="${c1}  █${c2} ᴗ ${c1}█${R}"
          lines[3]="${c2}✧${c1}██████${c2}✧${R}"
          lines[4]="${c3} ⋰⋱ ${c2}▀▀${c3} ⋰⋱${R}"
          ;;
        3)
          lines[0]="${c2}  ✧${c1} ◇◇ ${c2}✧${R}"
          lines[1]="${c2}*·${c1}█${c2}≖${c1}██${c2}≖${c1}█${c2}·*${R}"
          lines[2]="${c1}  █${c2} ‿ ${c1}█${R}"
          lines[3]="${c2} ✦${c1}████${c2}✦${R}"
          lines[4]="${c3}  ⋱⋰${c2}▀▀${c3}⋱⋰${R}"
          ;;
      esac ;;

  esac
}

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

# ─── 描画 ───
draw_monster

lv=$(( xp / 15 + 1 ))
gauge=$(evo_gauge)

# モンスター5行の右に情報を配置
info_0="${c2}${label}${R} ${ui}Lv.${lv}${R}"
info_1=""
if (( stage < 6 )); then
  info_2="${ui}EVO ${c1}${gauge}${R}"
else
  info_2="${gauge}"
fi
info_3="${tx}${xp}${ui}xp${R} ${ui}│${R} ${tx}${sessions}${ui}回${R}"
info_4=""

printf "%b   %b\n%b   %b\n%b   %b\n%b   %b\n%b   %b" \
  "${lines[0]}" "$info_0" \
  "${lines[1]}" "$info_1" \
  "${lines[2]}" "$info_2" \
  "${lines[3]}" "$info_3" \
  "${lines[4]}" "$info_4"
