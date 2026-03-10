#!/usr/bin/env python3
"""
monster-line キャラクター ピクセルアート生成スクリプト v7
全ステージ猫！ （目だけの全体像）
超絶可愛いアニメ風の丸っこい猫デザイン（16x16）。
"""

import os

ART_DIR = os.path.join(os.path.dirname(__file__), "assets")

def render_ansi(grid, palette):
    """pixel grid → ANSI half-block art, trailing blank lines trimmed"""
    height = len(grid)
    if height % 2 != 0:
        grid = grid + ["." * len(grid[0])]
        height += 1
    lines = []
    for row in range(0, height, 2):
        line = ""
        for col in range(len(grid[0])):
            top_ch = grid[row][col]
            bot_ch = grid[row+1][col]
            top_color = palette.get(top_ch)
            bot_color = palette.get(bot_ch)
            if top_color is None and bot_color is None:
                line += " "
            elif top_color is None and bot_color is not None:
                r, g, b = bot_color
                line += f"\x1b[38;2;{r};{g};{b}m▄\x1b[0m"
            elif top_color is not None and bot_color is None:
                r, g, b = top_color
                line += f"\x1b[38;2;{r};{g};{b}m▀\x1b[0m"
            elif top_color == bot_color:
                r, g, b = top_color
                line += f"\x1b[38;2;{r};{g};{b}m█\x1b[0m"
            else:
                tr, tg, tb = top_color
                br, bg, bb = bot_color
                line += f"\x1b[38;2;{br};{bg};{bb};48;2;{tr};{tg};{tb}m▄\x1b[0m"
        lines.append(line)
    while lines and lines[-1].strip() == '':
        lines.pop()
    return "\n".join(lines) + "\n"

def save_art(name, content):
    path = os.path.join(ART_DIR, name)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  {name}")

# ═══════════════════════════════════════════════════
#  猫パレット基盤：
#  o: 輪郭(Outline), f: メインの毛色(Fur), w: ハイライト(White/Bright)
#  b: 目の色(Base eye), K: 瞳(Pupil/Black), P: 耳や肉球(Pink)
# ═══════════════════════════════════════════════════

p1 = { 'o':(60,50,60),  'f':(255,248,235), 'w':(255,255,255), 'b':(100,200,255), 'K':(30,30,50),  'P':(255,160,180) } # ぐっすり白猫
p2 = { 'o':(80,40,20),  'f':(255,160,50),  'w':(255,255,255), 'b':(80,220,100),  'K':(40,20,10),  'P':(255,140,160) } # おすわり茶トラ
p3 = { 'o':(40,40,50),  'f':(160,160,170), 'w':(255,255,255), 'b':(240,200,50),  'K':(20,20,30),  'P':(200,120,140) } # てくてくグレー
p4 = { 'o':(10,10,15),  'f':(50,50,60),    'w':(255,255,255), 'b':(200,80,255),  'K':(0,0,0),     'P':(150,80,100)  } # のび〜黒猫
p5 = { 'o':(80,30,50),  'f':(255,140,200), 'w':(255,255,255), 'b':(255,240,100), 'K':(50,15,30),  'P':(255,200,220) } # ぴょんピンク
p6 = { 'o':(100,70,10), 'f':(255,210,60),  'w':(255,255,255), 'b':(255,100,100), 'K':(60,30,10),  'P':(255,150,120) } # ボスねこ黄金

# ─── 1. egg = ぐっすり白猫 (Sleeping, tail twitch) ───
cat1_f0 = [
    "................",
    "...oo......oo...",
    "..oPPo....oPPo..",
    "..offooooooffo..",
    ".ooffffffffffoo.",
    ".offffffffffffo.",
    ".offbwffffbwffo.",
    ".offbKffffbKffo.",
    ".ooffffffffffoo.",
    "..oooffffffooo..",
    "...ooffffffoo...",
    "..ooffffffffoooo",
    "..offfoofffoffoo",
    "..offo.offo.oooo",
    "...oo...oo......",
    "................",
]
cat1_f1 = [
    "................",
    "...oo......oo...",
    "..oPPo....oPPo..",
    "..offooooooffo..",
    ".ooffffffffffoo.",
    ".offffffffffffo.",
    ".offffffffffffo.",
    ".offooffffooffo.",
    ".ooffffffffffoo.",
    "..oooffffffooo..",
    "...ooffffffoooo.",
    "..ooffffffffoo..",
    "..offfoofffoffo.",
    "..offo.offo.offo",
    "...oo...oo...oo.",
    "................",
]
cat1_f2 = [
    "................",
    "...oo......oo...",
    "..oPPo....oPPo..",
    "..offooooooffo..",
    ".ooffffffffffoo.",
    ".offffffffffffo.",
    ".offbwffffbwffo.",
    ".offbKffffbKffo.",
    ".ooffffffffffoo.",
    "..oooffffffoooo.",
    "...ooffffffoo...",
    "..ooffffffffoo..",
    "..offfoofffoffo.",
    "..offo.offo.offo",
    "...oo...oo...oo.",
    "................",
]

# ─── 2. slime = おすわり茶トラ (Sitting/melting round cat) ───
cat2_f0 = [
    "................",
    "................",
    "....oo......oo..",
    "...oPPo....oPPo.",
    "...offooooooffo.",
    ".oofffffffffffoo",
    ".offbwffffbwfffo",
    ".offbKffffbKfffo",
    "oofffffffffffffo",
    "offffffffffffffo",
    "offfofffffffoffo",
    "ooooofffffffoooo",
    "..oooooooooooo..",
    "................",
    "................",
    "................",
]
cat2_f1 = [
    "................",
    "................",
    "....oo......oo..",
    "...oPPo....oPPo.",
    "...offooooooffo.",
    ".oofffffffffffoo",
    ".offfffffffffffo",
    ".offooffffoofffo",
    "oofffffffffffffo",
    "offffffffffffffo",
    "offoooooooooooff",
    "oooooooooooooooo",
    "................",
    "................",
    "................",
    "................",
]
cat2_f2 = [
    "................",
    "....oo......oo..",
    "...oPPo....oPPo.",
    "...offooooooffo.",
    ".oofffffffffffoo",
    ".offbwffffbwfffo",
    ".offbKffffbKfffo",
    "oofffffffffffffo",
    "offffffffffffffo",
    "offooffffffooffo",
    "ooooofffffffoooo",
    "..oooooooooooo..",
    "................",
    "................",
    "................",
    "................",
]

# ─── 3. wolf = てくてくグレー (Walking cat) ───
cat3_f0 = [
    "................",
    ".oo......oo.....",
    "oPPo....oPPo....",
    "offooooooffo....",
    "ooffffffffffoo..",
    "offbwffffbwffo..",
    "offbKffffbKffo..",
    "ooffffffffffoo..",
    ".oooffffffoo....",
    "..ooffffffffoo..",
    "..ooffffffffffoo",
    "..offfo.offfoooo",
    "...ooo...ooo....",
    "................",
    "................",
    "................",
]
cat3_f1 = [
    "................",
    ".oo......oo.....",
    "oPPo....oPPo....",
    "offooooooffo....",
    "ooffffffffffoo..",
    "offffffffffffo..",
    "offooffffooffo..",
    "ooffffffffffoo..",
    ".oooffffffoo....",
    "..ooffffffffoo..",
    "...offffffffffoo",
    "....off..off.ooo",
    "....oo...oo.....",
    "................",
    "................",
    "................",
]
cat3_f2 = [
    "................",
    ".oo......oo.....",
    "oPPo....oPPo....",
    "offooooooffo....",
    "ooffffffffffoo..",
    "offbwffffbwffo..",
    "offbKffffbKffo..",
    "ooffffffffffoo..",
    ".oooffffffoo....",
    "..ooffffffffoo..",
    "....offfffffffoo",
    "....offf.off.ooo",
    "....ooo..oo.....",
    "................",
    "................",
    "................",
]

# ─── 4. demon = のび〜黒猫 (Stretching cat) ───
cat4_f0 = [
    "...oo......oo...",
    "..oPPo....oPPo..",
    "..offooooooffo..",
    ".ooffffffffffoo.",
    ".offbwffffbwffo.",
    ".offbKffffbKffo.",
    ".ooffffffffffoo.",
    "..oooffffffooo..",
    "...offfffffoo...",
    "...offfffffoo...",
    "..oofffffffooo..",
    "..offffffffffo..",
    "..offo....offo..",
    "..ooo......ooo..",
    "................",
    "................",
]
cat4_f1 = [
    "................",
    "...oo......oo...",
    "..oPPo....oPPo..",
    "..offooooooffo..",
    ".ooffffffffffoo.",
    ".offffffffffffo.",
    ".offooffffooffo.",
    ".ooffffffffffoo.",
    "..oooffffffooo..",
    "...offfffffoo...",
    "..oofffffffooo..",
    "..offo....offo..",
    "..ooo......ooo..",
    "................",
    "................",
    "................",
]
cat4_f2 = [
    "................",
    "................",
    "...oo......oo...",
    "..oPPo....oPPo..",
    "..offooooooffo..",
    ".ooffffffffffoo.",
    ".offbwffffbwffo.",
    ".offbKffffbKffo.",
    ".ooffffffffffoo.",
    "..oooffffffooo..",
    ".ooffffffffffoo.",
    ".offo.offo.offo.",
    "..oo...oo...oo..",
    "................",
    "................",
    "................",
]

# ─── 5. dragon = ぴょんピンク (Jumping cat) ───
cat5_f0 = [
    "................",
    ".....oo......oo.",
    "....oPPo....oPPo",
    "....offooooooffo",
    "...oofffffffffoo",
    "...offbwffffbwff",
    "...offbKffffbKff",
    "...ooffffffffffo",
    "....oooffffffooo",
    ".....ooffffffoo.",
    "....oofffffffooo",
    "o...offo...offo.",
    "oo..ooo.....ooo.",
    "ooo.............",
    "................",
    "................",
]
cat5_f1 = [
    ".....oo......oo.",
    "....oPPo....oPPo",
    "....offooooooffo",
    "...oofffffffffoo",
    "...offfffffffffo",
    "...offooffffooff",
    "...ooffffffffffo",
    "....oooffffffooo",
    ".....ooffffffoo.",
    "....oofffffffooo",
    "...ooofff.oooo..",
    "..oo..ooo.......",
    ".oo.............",
    "oo..............",
    "................",
    "................",
]
cat5_f2 = [
    "................",
    "................",
    "....oo......oo..",
    "...oPPo....oPPo.",
    "...offooooooffo.",
    "..ooffffffffffoo",
    "..offbwffffbwffo",
    "..offbKffffbKffo",
    "..ooffffffffffoo",
    "...oooffffffooo.",
    "....ooffffffoo..",
    ".ooooofffoooffoo",
    ".ooo.offo.oooo..",
    ".....ooo........",
    "................",
    "................",
]

# ─── 6. goddragon = ボスねこ黄金 (Action running cat) ───
cat6_f0 = [
    "................",
    "..oo......oo....",
    ".oPPo....oPPo...",
    ".offooooooffo...",
    "ooffffffffffoo..",
    "offbwffffbwffo..",
    "offbKffffbKffo..",
    "ooffffffffffoo..",
    ".oooffffffoo....",
    "..ooffffffffoo..",
    "...offffffffffoo",
    "....offffooffooo",
    ".....offf.offfoo",
    ".....ooo...ooooo",
    "................",
    "................",
]
cat6_f1 = [
    "................",
    "................",
    "..oo......oo....",
    ".oPPo....oPPo...",
    ".offooooooffo...",
    "ooffffffffffoo..",
    "offffffffffffo..",
    "offooffffooffo..",
    "ooffffffffffoo..",
    ".oooffffffoo....",
    "..ooffffffffoo..",
    "...offffffffffoo",
    "oo.offf...offfoo",
    "ooo.ooo...ooooo.",
    "................",
    "................",
]
cat6_f2 = [
    "................",
    "..oo......oo....",
    ".oPPo....oPPo...",
    ".offooooooffo...",
    "ooffffffffffoo..",
    "offbwffffbwffo..",
    "offbKffffbKffo..",
    "ooffffffffffoo..",
    ".oooffffffoo....",
    "..ooffffffffoo..",
    "..ooffffffoooo..",
    ".ooofffffooooo..",
    ".oooofff..offo..",
    ".....ooo...ooo..",
    "................",
    "................",
]

# ═══════════════════════════════════════════════════
#  生成実行
# ═══════════════════════════════════════════════════
characters = [
    ("egg",       p1, [cat1_f0, cat1_f1, cat1_f2]),
    ("slime",     p2, [cat2_f0, cat2_f1, cat2_f2]),
    ("wolf",      p3, [cat3_f0, cat3_f1, cat3_f2]),
    ("demon",     p4, [cat4_f0, cat4_f1, cat4_f2]),
    ("dragon",    p5, [cat5_f0, cat5_f1, cat5_f2]),
    ("goddragon", p6, [cat6_f0, cat6_f1, cat6_f2]),
]

os.makedirs(ART_DIR, exist_ok=True)

if __name__ == '__main__':
    for name, palette, frames in characters:
        print(f"[{name}]")
        art = render_ansi(frames[0], palette)
        save_art(f"{name}_clean.txt", art)
        save_art(f"{name}_ansi.txt", art)
        for i, frame in enumerate(frames):
            art = render_ansi(frame, palette)
            save_art(f"{name}_f{i}_clean.txt", art)
    print("\nDone!")
