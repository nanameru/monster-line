#!/usr/bin/env python3
"""
monster-line キャラクター ピクセルアート生成スクリプト v6
全ステージ猫！ 全体像で目だけあり。動きがある可愛いバージョン。
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
    # Trim trailing blank lines
    while lines and lines[-1].strip() == '':
        lines.pop()
    return "\n".join(lines) + "\n"


def save_art(name, content):
    path = os.path.join(ART_DIR, name)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  {name}")


# ═══════════════════════════════════════════════════
#  共通パレット
# ═══════════════════════════════════════════════════
cat_palette = {
    'o': (45, 45, 50),     # Outline
    'f': (255, 255, 255),  # Fur (White)
    'k': (15, 15, 25),     # Eye center
    'P': (255, 150, 180),  # Pink (Ears/Paws)
    'd': (220, 220, 230),  # Shadow fur
}

# ─── 1. egg = ぐっすりねこ (Sleeping cat) ───
p1 = cat_palette.copy(); p1['b'] = (100, 200, 255) # light blue
cat1_f0 = [
    "................",
    "................",
    "................",
    "...ooo....ooo...",
    "..oPPo...oPPo...",
    ".oofffoooofffoo.",
    "ooffffffffffffoo",
    "ooffoffffffoffoo",
    ".ooffffffffffffo",
    "..oooooooooooo..",
]
cat1_f1 = [
    "................",
    "................",
    "................",
    "...ooo....ooo...",
    "..oPPo...oPPo...",
    ".oofffoooofffoo.",
    "ooffffffffffffoo",
    "ooffbffffffbffoo",
    ".offkffffffkffo.",
    "..oooooooooooo..",
]
cat1_f2 = [
    "................",
    "................",
    "................",
    "...ooo....ooo...",
    "..oPPo...oPPo...",
    ".oofffoooofffoo.",
    "ooffffffffffffoo",
    "ooffbffffffbffoo",
    ".offkffffffkffo.",
    "..oooooooooooo..",
]

# ─── 2. slime = おすわりねこ (Sitting cat) ───
p2 = cat_palette.copy(); p2['b'] = (255, 180, 50) # Orange
cat2_f0 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "..ofoooffooofo..",
    "...oooooooooo...",
]
cat2_f1 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    "oooffffffffffoo.",
    "oofoooffooofo...",
    ".ooooooooooo....",
]
cat2_f2 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffooo",
    "...ofoooffooofoo",
    "....ooooooooooo.",
]

# ─── 3. wolf = てくてくねこ (Walking cat) ───
p3 = cat_palette.copy(); p3['b'] = (50, 200, 100) # Green
cat3_f0 = [
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "..offffffffffffo",
    "..ofooofffffffoo",
    "...oo..oooooooo.",
]
cat3_f1 = [
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "..offffffffffffo",
    "..ofoooff..offoo",
    "...oo..oo...ooo.",
]
cat3_f2 = [
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "..offffffffffffo",
    "..offoooff.ofoo.",
    "...ooo..oo..oo..",
]

# ─── 4. demon = のび〜ねこ (Stretching cat) ───
p4 = cat_palette.copy(); p4['b'] = (200, 100, 255) # Purple
cat4_f0 = [
    ".......ooo..ooo.",
    "......oPPo..oPPo",
    ".....oofffoofffo",
    "....ooffffffffff",
    "...ooffbffffffbf",
    "..oofffkffffffkf",
    ".ooffffffffffffo",
    "oofffffffffffoo.",
    "ofoooff..offoo..",
    "ooo..oo...ooo...",
]
cat4_f1 = [
    "......ooo..ooo..",
    ".....oPPo..oPPo.",
    "....oofffoofffoo",
    "...ooffffffffffo",
    "..ooffbffffffbfo",
    ".oofffkffffffkfo",
    "ooffffffffffffo.",
    "offfffffffffoo..",
    "ofoooff..offoo..",
    "ooo..oo...ooo...",
]
cat4_f2 = [
    ".....ooo..ooo...",
    "....oPPo..oPPo..",
    "...oofffoofffoo.",
    "..ooffffffffffoo",
    ".ooffbffffffbffo",
    ".ooffkffffffkffo",
    ".ooffffffffffffo",
    "..offffffffffoo.",
    "..ofoooff..offoo",
    "...oo..oo...ooo.",
]

# ─── 5. dragon = ぴょんねこ (Jumping cat) ───
p5 = cat_palette.copy(); p5['b'] = (255, 100, 100) # Red/Pink
cat5_f0 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "oofffooffoooffoo",
    ".ooo..oooo..ooo.",
]
cat5_f1 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "..offffffffffoo.",
    "...oooooooooo...",
]
cat5_f2 = [
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffoo.",
    "..offffffffffoo.",
    "..ofoooffooofo..",
    "...ooo..oo..oo..",
]

# ─── 6. goddragon = ダッシュねこ (Running cat) ───
p6 = cat_palette.copy(); p6['b'] = (255, 230, 50) # Gold
cat6_f0 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    "..ooffffffffffoo",
    "ooooffooofffffoo",
    "..ooo...ooooooo.",
]
cat6_f1 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    ".ooffffffffffooo",
    ".offoooffffffooo",
    "..ooo..ooooooo..",
]
cat6_f2 = [
    "................",
    "....ooo..ooo....",
    "...oPPo..oPPo...",
    "..oofffoofffoo..",
    ".ooffffffffffoo.",
    ".offbffffffbffo.",
    ".offkffffffkffo.",
    "..ooffffffffffoo",
    "..offoooffffffoo",
    "...ooo..ooooooo.",
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
