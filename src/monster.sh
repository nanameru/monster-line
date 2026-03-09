#!/usr/bin/env bash
# ============================================================
#  monster-line  ─  たまごっち風モンスター育成ステータスライン
#  Claude Code を使うたびに経験値が溜まり、進化していく
#  モンスターは画面内を左右に歩き回る！
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
# 3フレーム歩行サイクル（0,1,2,1,0,1,2,1...）
walk_frame=$(( now % 3 ))

# 位置: 10秒かけて右に行って左に戻る (0→7→0)
pos_cycle=$(( now % 10 ))
if (( pos_cycle <= 5 )); then
  pos=$pos_cycle         # 0,1,2,3,4,5 → 右へ
  facing="right"
else
  pos=$(( 10 - pos_cycle )) # 4,3,2,1,0 → 左へ
  facing="left"
fi

# ─── カラーヘルパー ───
fg() { printf "\x1b[38;2;%d;%d;%dm" "$1" "$2" "$3"; }
R="\x1b[0m"

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
ground=$(fg 60 60 65)

# ─── スペーサー（位置に応じたインデント） ───
pad=""
for (( i=0; i<pos; i++ )); do pad+=" "; done

# ─── 地面（足場）を描画 ───
floor="${ground}▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔${R}"

# ─── モンスター描画（アウトライン方式・3フレーム歩行） ───
declare -a art

case $stage in

  1) # ═══ たまご ═══ コロコロ転がる
    e=$(fg 225 200 170); h=$(fg 250 240 220); sp=$(fg 185 115 75)
    case $walk_frame in
      0)
        art[0]="    ${e}__${R}"
        art[1]="   ${e}/${h}  ${sp} ${e}\\${R}"
        art[2]="  ${e}(${h} ${sp}°${h}   ${e})${R}"
        art[3]="  ${e}(${h}   ${sp}° ${e})${R}"
        art[4]="   ${e}\\${h}___${e}/${R}"
        ;;
      1)
        art[0]="    ${e}__${R}"
        art[1]="   ${e}/${h}    ${e}\\${R}"
        art[2]="  ${e}(${h}  ${sp}°${h}  ${e})${R}"
        art[3]="  ${e}(${h} ${sp}°${h}   ${e})${R}"
        art[4]="   ${e}\\${h}___${e}/${R}"
        ;;
      2)
        art[0]="    ${e}__${R}"
        art[1]="   ${e}/${sp} ${h}   ${e}\\${R}"
        art[2]="  ${e}(${h}   ${sp}° ${e})${R}"
        art[3]="  ${e}(${h} ${sp}°${h}   ${e})${R}"
        art[4]="   ${e}\\${h}___${e}/${R}"
        ;;
    esac ;;

  2) # ═══ スライム ═══ ぴょんぴょん跳ねる
    s1=$(fg 80 200 110); s2=$(fg 140 255 170); s3=$(fg 60 180 80)
    case $walk_frame in
      0)
        art[0]="   ${s1}___${R}"
        art[1]="  ${s1}(${s2} ◕‿◕ ${s1})${R}"
        art[2]="  ${s1}/${s2}       ${s1}\\${R}"
        art[3]="  ${s3}‾‾‾‾‾‾‾‾‾${R}"
        ;;
      1)
        art[0]="    ${s1}__${R}"
        art[1]="   ${s1}(${s2}◕‿◕${s1})${R}"
        art[2]="   ${s1}/${s2}     ${s1}\\${R}"
        art[3]="             "
        ;;
      2)
        art[0]="  ${s1}____${R}"
        art[1]=" ${s1}(${s2} ◕ ◡ ◕ ${s1})${R}"
        art[2]=" ${s1}/${s2}         ${s1}\\${R}"
        art[3]=" ${s3}‾‾‾‾‾‾‾‾‾‾‾${R}"
        ;;
    esac ;;

  3) # ═══ ウルフ ═══ とことこ歩く
    w1=$(fg 220 170 60); w2=$(fg 255 210 100)
    if [[ "$facing" == "right" ]]; then
      case $walk_frame in
        0)
          art[0]="  ${w2}/\\   /\\${R}"
          art[1]="  ${w1}( ${w2}•ω•${w1} )${w2}~${R}"
          art[2]="  ${w1} /|  |\\${R}"
          art[3]="  ${w1}  |  |${R}"
          ;;
        1)
          art[0]="  ${w2}/\\   /\\${R}"
          art[1]="  ${w1}( ${w2}•ω•${w1} )${w2}~~${R}"
          art[2]="  ${w1} /|  |\\${R}"
          art[3]="  ${w1} / \\/ \\${R}"
          ;;
        2)
          art[0]="  ${w2}/\\   /\\${R}"
          art[1]="  ${w1}( ${w2}•ω•${w1} )${w2}~${R}"
          art[2]="  ${w1} /|  |\\${R}"
          art[3]="  ${w1} |    |${R}"
          ;;
      esac
    else
      case $walk_frame in
        0)
          art[0]="  ${w2}/\\   /\\${R}"
          art[1]="  ${w2}~${w1}( ${w2}•ω•${w1} )${R}"
          art[2]="   ${w1}/|  |\\${R}"
          art[3]="   ${w1} |  |${R}"
          ;;
        1)
          art[0]="  ${w2}/\\   /\\${R}"
          art[1]=" ${w2}~~${w1}( ${w2}•ω•${w1} )${R}"
          art[2]="   ${w1}/|  |\\${R}"
          art[3]="   ${w1}/ \\/ \\${R}"
          ;;
        2)
          art[0]="  ${w2}/\\   /\\${R}"
          art[1]="  ${w2}~${w1}( ${w2}•ω•${w1} )${R}"
          art[2]="   ${w1}/|  |\\${R}"
          art[3]="   ${w1}|    |${R}"
          ;;
      esac
    fi ;;

  4) # ═══ アクマ ═══ 翼バサバサ浮遊
    d1=$(fg 190 40 60); d2=$(fg 255 80 100); d3=$(fg 140 20 40)
    case $walk_frame in
      0)
        art[0]="  ${d2} Y    Y${R}"
        art[1]="  ${d1}{( ${d2}▼皿▼${d1} )}${R}"
        art[2]="   ${d1} |${d3}////|${R}"
        art[3]="   ${d1}(_|  |_)${R}"
        ;;
      1)
        art[0]="  ${d2}  Y  Y${R}"
        art[1]=" ${d3}/{d1}( ${d2}▼益▼${d1} )${d3}\\${R}"
        art[2]="   ${d1} |${d3}////|${R}"
        art[3]="   ${d1}  |  |${R}"
        ;;
      2)
        art[0]="  ${d2} Y    Y${R}"
        art[1]=" ${d3}\\${d1}( ${d2}▼皿▼${d1} )${d3}/${R}"
        art[2]="   ${d1} |${d3}////|${R}"
        art[3]="   ${d1}(_|  |_)${R}"
        ;;
    esac ;;

  5) # ═══ リュウ ═══ 翼羽ばたき＋炎
    r1=$(fg 50 120 220); r2=$(fg 100 170 255); r3=$(fg 255 140 40)
    if [[ "$facing" == "right" ]]; then
      case $walk_frame in
        0)
          art[0]=" ${r2}/\\${r1}  ^  ${r2}/\\${R}"
          art[1]="  ${r1}( ${r2}◇${r1}ᴗ${r2}◇ ${r1})${r3}>${R}"
          art[2]="  ${r1} /|    |\\${R}"
          art[3]="  ${r1}  |    |${R}"
          ;;
        1)
          art[0]="${r2}/\\ ${r1}  ^  ${r2} /\\${R}"
          art[1]="  ${r1}( ${r2}◇${r1}ᴗ${r2}◇ ${r1})${r3}>~≈${R}"
          art[2]="  ${r1} /|    |\\${R}"
          art[3]="  ${r1} / \\  / \\${R}"
          ;;
        2)
          art[0]=" ${r2}/\\${r1}  ^  ${r2}/\\${R}"
          art[1]="  ${r1}( ${r2}◇${r1}ᴗ${r2}◇ ${r1})${r3}>彡${R}"
          art[2]="  ${r1} /|    |\\${R}"
          art[3]="  ${r1} |      |${R}"
          ;;
      esac
    else
      case $walk_frame in
        0)
          art[0]="  ${r2}/\\${r1}  ^  ${r2}/\\${R}"
          art[1]="   ${r3}<${r1}( ${r2}◇${r1}ᴗ${r2}◇ ${r1})${R}"
          art[2]="   ${r1} /|    |\\${R}"
          art[3]="   ${r1}  |    |${R}"
          ;;
        1)
          art[0]=" ${r2}/\\ ${r1}  ^  ${r2} /\\${R}"
          art[1]="${r3}≈~<${r1}( ${r2}◇${r1}ᴗ${r2}◇ ${r1})${R}"
          art[2]="   ${r1} /|    |\\${R}"
          art[3]="   ${r1} / \\  / \\${R}"
          ;;
        2)
          art[0]="  ${r2}/\\${r1}  ^  ${r2}/\\${R}"
          art[1]="${r3}彡<${r1}( ${r2}◇${r1}ᴗ${r2}◇ ${r1})${R}"
          art[2]="   ${r1} /|    |\\${R}"
          art[3]="   ${r1} |      |${R}"
          ;;
      esac
    fi ;;

  6) # ═══ シンリュウ ═══ 神々しいオーラ
    g1=$(fg 255 200 30); g2=$(fg 255 240 120); g3=$(fg 200 160 20)
    case $walk_frame in
      0)
        art[0]=" ${g2}✧${g1} /\\  ^  /\\ ${g2}✧${R}"
        art[1]="  ${g1}( ${g2}≖ ᴗ ≖${g1} )${g2}*${R}"
        art[2]=" ${g2}✦${g1} /|      |\\ ${g2}✦${R}"
        art[3]="  ${g3}(_|      |_)${R}"
        ;;
      1)
        art[0]="  ${g2}✦${g1}/\\  ^  /\\${g2}✦${R}"
        art[1]="  ${g1}( ${g2}≖ ‿ ≖${g1} )${g2}·${R}"
        art[2]="  ${g2}✧${g1}/|      |\\${g2}✧${R}"
        art[3]="  ${g3} (_|    |_)${R}"
        ;;
      2)
        art[0]="${g2}✧  ${g1}/\\  ^  /\\ ${g2} ✧${R}"
        art[1]="  ${g2}*${g1}( ${g2}≖ ᴗ ≖${g1} )${R}"
        art[2]=" ${g2}✦${g1} /|      |\\ ${g2}✦${R}"
        art[3]="  ${g3}(_|      |_)${R}"
        ;;
    esac ;;

esac

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

# 左にモンスター（pad でインデント）、右に情報
if [[ -n "${art[4]:-}" ]]; then
  printf "%b%b   %b\n%b%b   %b\n%b%b   %b\n%b%b\n%b%b\n%b" \
    "$pad" "${art[0]}" "$info_0" \
    "$pad" "${art[1]}" "$info_1" \
    "$pad" "${art[2]}" "$info_2" \
    "$pad" "${art[3]}" \
    "$pad" "${art[4]}" \
    "$floor"
else
  printf "%b%b   %b\n%b%b   %b\n%b%b   %b\n%b%b\n%b" \
    "$pad" "${art[0]}" "$info_0" \
    "$pad" "${art[1]}" "$info_1" \
    "$pad" "${art[2]}" "$info_2" \
    "$pad" "${art[3]}" \
    "$floor"
fi
