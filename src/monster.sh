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

# ─── モンスター描画（3フレーム歩行 × 左右反転） ───
declare -a art  # 各行のアスキーアート

case $stage in

  1) # ═══ たまご ═══ PixelLab版・コロコロ転がる
    # カラー: ダークブラウン輪郭 / ベージュ本体 / ライトクリーム光沢 / 赤茶模様 / シャドウ
    dk=$(fg 120 80 60); bg=$(fg 230 210 180); lt=$(fg 245 235 215); sp=$(fg 180 100 70); sh=$(fg 200 175 145)
    case $walk_frame in
      0) # 正面
        art[0]="  ${dk}▄▄▄▄▄▄${R}"
        art[1]="${dk}▄${bg}█${lt}██${bg}█${sp}◦${bg}█${dk}▄${R}"
        art[2]="${dk}█${bg}█${sp}◦${bg}██${lt}█${sh}█${dk}█${R}"
        art[3]="${dk}█${sh}██${bg}██${sh}█${dk}█${R}"
        art[4]="  ${dk}▀▀▀▀▀▀${R}"
        ;;
      1) # 少し右に傾く
        art[0]="   ${dk}▄▄▄▄▄▄${R}"
        art[1]=" ${dk}▄${lt}██${bg}██${sp}◦${bg}█${dk}▄${R}"
        art[2]=" ${dk}█${bg}███${lt}█${sh}█${dk}█${R}"
        art[3]=" ${dk}█${sh}█${bg}█${sp}◦${bg}█${sh}█${dk}█${R}"
        art[4]="   ${dk}▀▀▀▀▀▀${R}"
        ;;
      2) # 少し左に傾く
        art[0]=" ${dk}▄▄▄▄▄▄${R}"
        art[1]="${dk}▄${bg}█${sp}◦${bg}██${lt}█${bg}█${dk}▄${R}"
        art[2]="${dk}█${sh}█${lt}█${bg}███${dk}█${R}"
        art[3]="${dk}█${sh}█${bg}█${sp}◦${sh}██${bg}█${dk}█${R}"
        art[4]=" ${dk}▀▀▀▀▀▀${R}"
        ;;
    esac ;;

  2) # ═══ スライム ═══ ぴょんぴょん跳ねて移動
    case $walk_frame in
      0) # 着地
        art[0]="${c1} ▄▄▄${R}"
        art[1]="${c1}█${c2}◕${c1}█${c2}◕${c1}█${R}"
        art[2]="${c1}█${c2} ▽ ${c1}█${R}"
        art[3]="${c1} ▀▀▀${R}"
        ;;
      1) # ジャンプ中
        art[0]="${c1} ▄█▄${R}"
        art[1]="${c1}█${c2}◕▽◕${c1}█${R}"
        art[2]="${c1} ▀█▀${R}"
        art[3]="     "
        ;;
      2) # 着地（つぶれ）
        art[0]="     "
        art[1]="${c1}▄${c2}◕${c1}██${c2}◕${c1}▄${R}"
        art[2]="${c1}█${c2} ◡◡ ${c1}█${R}"
        art[3]="${c1}▀▀▀▀▀▀${R}"
        ;;
    esac ;;

  3) # ═══ ウルフ ═══ とことこ歩く
    if [[ "$facing" == "right" ]]; then
      case $walk_frame in
        0) # 右足前
          art[0]="${c2} ∧ ∧${R}"
          art[1]="${c1} █${c2}◕ω◕${c1}█${c2}~${R}"
          art[2]="${c1} █▀█▀█${R}"
          art[3]="${c1}  ╱  ╲${R}"
          ;;
        1) # 両足揃い
          art[0]="${c2} ∧ ∧${R}"
          art[1]="${c1} █${c2}◕ω◕${c1}█${c2}~${R}"
          art[2]="${c1} █▀██▀█${R}"
          art[3]="${c1}  ╱╲╱╲${R}"
          ;;
        2) # 左足前
          art[0]="${c2} ∧ ∧${R}"
          art[1]="${c1} █${c2}◕ω◕${c1}█${c2}~~${R}"
          art[2]="${c1} █▀█▀█${R}"
          art[3]="${c1} ╲  ╱${R}"
          ;;
      esac
    else # 左向き
      case $walk_frame in
        0)
          art[0]="${c2}  ∧ ∧${R}"
          art[1]="${c2}~${c1}█${c2}◕ω◕${c1}█${R}"
          art[2]="${c1}  █▀█▀█${R}"
          art[3]="${c1}  ╱  ╲${R}"
          ;;
        1)
          art[0]="${c2}  ∧ ∧${R}"
          art[1]="${c2}~${c1}█${c2}◕ω◕${c1}█${R}"
          art[2]="${c1}  █▀██▀█${R}"
          art[3]="${c1}  ╱╲╱╲${R}"
          ;;
        2)
          art[0]="${c2}  ∧ ∧${R}"
          art[1]="${c2}~~${c1}█${c2}◕ω◕${c1}█${R}"
          art[2]="${c1}  █▀█▀█${R}"
          art[3]="${c1}  ╲  ╱${R}"
          ;;
      esac
    fi ;;

  4) # ═══ アクマ ═══ 翼をバサバサさせながら浮遊移動
    case $walk_frame in
      0) # 翼上
        art[0]="${c2} ☆${c1}▼▼${c2}☆${R}"
        art[1]="${c3}╱${c1}█${c2}◣皿◣${c1}█${c3}╲${R}"
        art[2]="${c1}  ████${R}"
        art[3]="${c1}  █▀ ▀█${R}"
        ;;
      1) # 翼中
        art[0]="${c2} ★${c1}▼▼${c2}★${R}"
        art[1]="${c1}}█${c2}◣益◣${c1}█{${R}"
        art[2]="${c1}  ████${R}"
        art[3]="${c1}   ▀▀${R}"
        ;;
      2) # 翼下
        art[0]="${c2} ☆${c1}▼▼${c2}☆${R}"
        art[1]="${c3}╲${c1}█${c2}◣皿◣${c1}█${c3}╱${R}"
        art[2]="${c1}  ████${R}"
        art[3]="${c1}  █▀ ▀█${R}"
        ;;
    esac ;;

  5) # ═══ リュウ ═══ 翼を羽ばたかせながら歩く＋炎
    if [[ "$facing" == "right" ]]; then
      case $walk_frame in
        0)
          art[0]="${c2} /▲${c1}◇◇${c2}▲\\${R}"
          art[1]="${c1}  █${c2}◇ᴗ◇${c1}█▸${R}"
          art[2]="${c1}  ██████${R}"
          art[3]="${c1}  █▀█ █▀█${R}"
          ;;
        1)
          art[0]="${c2}/▲ ${c1}◇◇${c2} ▲\\${R}"
          art[1]="${c1}  █${c2}◇ᴗ◇${c1}█▸${c3}~≈${R}"
          art[2]="${c1}  ██████${R}"
          art[3]="${c1}  █▀██▀█${R}"
          ;;
        2)
          art[0]="${c2} /▲${c1}◇◇${c2}▲\\${R}"
          art[1]="${c1}  █${c2}◇ᴗ◇${c1}█▸${c3}彡${R}"
          art[2]="${c1}  ██████${R}"
          art[3]="${c1}   █▀█▀${R}"
          ;;
      esac
    else
      case $walk_frame in
        0)
          art[0]="${c2} /▲${c1}◇◇${c2}▲\\${R}"
          art[1]="${c1}  ◂█${c2}◇ᴗ◇${c1}█${R}"
          art[2]="${c1}  ██████${R}"
          art[3]="${c1}  █▀█ █▀█${R}"
          ;;
        1)
          art[0]="${c2}/▲ ${c1}◇◇${c2} ▲\\${R}"
          art[1]="${c3}≈~${c1}◂█${c2}◇ᴗ◇${c1}█${R}"
          art[2]="${c1}  ██████${R}"
          art[3]="${c1}  █▀██▀█${R}"
          ;;
        2)
          art[0]="${c2} /▲${c1}◇◇${c2}▲\\${R}"
          art[1]="${c3}彡${c1}◂█${c2}◇ᴗ◇${c1}█${R}"
          art[2]="${c1}  ██████${R}"
          art[3]="${c1}   █▀█▀${R}"
          ;;
      esac
    fi ;;

  6) # ═══ シンリュウ ═══ 光の粒子を撒きながら浮遊
    case $walk_frame in
      0)
        art[0]="${c2}  ✦${c1}◇◇${c2}✦${R}"
        art[1]="${c2}.*${c1}█${c2}≖ᴗ≖${c1}█${c2}*.${R}"
        art[2]="${c2}✧${c1}██████${c2}✧${R}"
        art[3]="${c3} ⋰⋱${c2}▀▀${c3}⋰⋱${R}"
        ;;
      1)
        art[0]="${c2} ✧ ${c1}◇◇${c2} ✧${R}"
        art[1]="${c2}*.${c1}█${c2}≖‿≖${c1}█${c2}.*${R}"
        art[2]="${c2} ✦${c1}████${c2}✦${R}"
        art[3]="${c3}  ⋱⋰${c2}▀▀${c3}⋱⋰${R}"
        ;;
      2)
        art[0]="${c2}✦  ${c1}◇◇${c2}  ✦${R}"
        art[1]="${c2}·*${c1}█${c2}≖ᴗ≖${c1}█${c2}*·${R}"
        art[2]="${c2}✧${c1}██████${c2}✧${R}"
        art[3]="${c3}⋰⋱⋰${c2}▀▀${c3}⋱⋰⋱${R}"
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
# art[4]がある場合は5行、ない場合は4行
if [[ -n "${art[4]:-}" ]]; then
  printf "%b%b    %b\n%b%b    %b\n%b%b    %b\n%b%b\n%b%b\n%b" \
    "$pad" "${art[0]}" "$info_0" \
    "$pad" "${art[1]}" "$info_1" \
    "$pad" "${art[2]}" "$info_2" \
    "$pad" "${art[3]}" \
    "$pad" "${art[4]}" \
    "$floor"
else
  printf "%b%b    %b\n%b%b    %b\n%b%b    %b\n%b%b\n%b" \
    "$pad" "${art[0]}" "$info_0" \
    "$pad" "${art[1]}" "$info_1" \
    "$pad" "${art[2]}" "$info_2" \
    "$pad" "${art[3]}" \
    "$floor"
fi
