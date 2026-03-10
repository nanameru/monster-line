#!/usr/bin/env python3
"""
monster-line キャラクター ピクセルアート生成スクリプト v5
全ステージ猫！ 小さく全身を表示、遊んでいる感じ
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
#  共通: o=outline, f=fur, l=light fur, k=eye, p=inner ear
# ═══════════════════════════════════════════════════

# ─── 1. こたま (Cream kitten - sitting, pawing at something) ───
cat1_palette = {
    'o': (160, 135, 90),
    'f': (255, 240, 210),
    'l': (255, 250, 235),
    'k': (40, 40, 50),
    'p': (245, 190, 190),
    't': (255, 235, 200),
}

cat1_f0 = [
    ".....oo.oo......",
    ".....olfflo.....",
    ".....okffkofo...",
    "......offffooo..",
    "......offffo....",
    ".....off..fo.t..",
    "......oo..oo.o..",
]

cat1_f1 = [
    ".....oo.oo.fo...",
    ".....olfflooo...",
    ".....okffko.....",
    "......offffo....",
    "......offffo....",
    ".....off..fo.t..",
    "......oo..oo.o..",
]

cat1_f2 = [
    ".....oo.oo......",
    ".....olfflo.....",
    ".....okffko.....",
    "......offffo....",
    "......offffo....",
    ".....off.ofo.t..",
    "......oo.oo..o..",
]

# ─── 2. こねこ (Orange kitten - running/chasing) ───
cat2_palette = {
    'o': (165, 95, 20),
    'f': (245, 170, 65),
    'l': (255, 205, 110),
    'k': (40, 35, 30),
    'p': (245, 185, 185),
    't': (240, 155, 50),
}

cat2_f0 = [
    "....oo.oo.......",
    "....olfflo......",
    "....okffko......",
    ".....offffot....",
    ".....offffo.....",
    "....of..fo......",
    "....oo..oo......",
]

cat2_f1 = [
    "....oo.oo.......",
    "....olfflo......",
    "....okffko......",
    ".....offffo.....",
    ".....offffot....",
    "....of.ofo......",
    "....oo.oo.......",
]

cat2_f2 = [
    "....oo.oo.......",
    "....olfflo......",
    "....okffko.fo...",
    ".....offffooo...",
    ".....offffo.....",
    "....of..fo......",
    "....oo..oo......",
]

# ─── 3. さんぽ (Grey tabby - walking/trotting) ───
cat3_palette = {
    'o': (80, 80, 90),
    'f': (155, 155, 165),
    'l': (195, 195, 205),
    'd': (115, 115, 125),
    'k': (40, 40, 55),
    'p': (200, 165, 165),
    't': (145, 145, 155),
}

cat3_f0 = [
    ".....oo.oo......",
    ".....oldflo.....",
    ".....okffko.....",
    "....ooffffooo...",
    "...of......fot..",
    "...oo......oo.o.",
]

cat3_f1 = [
    ".....oo.oo......",
    ".....oldflo.....",
    ".....okffko.....",
    "...oooffffooo...",
    "...of......fo.t.",
    "...oo......oo.o.",
]

cat3_f2 = [
    ".....oo.oo......",
    ".....oldflo.....",
    ".....okffko.....",
    "....ooffffooo...",
    "....of....fo..t.",
    "....oo....oo..o.",
]

# ─── 4. ハンター (Black cat - crouching/pouncing) ───
cat4_palette = {
    'o': (25, 25, 30),
    'f': (60, 60, 65),
    'l': (90, 90, 100),
    'k': (110, 225, 100),    # green eyes!
    'p': (155, 105, 105),
    't': (55, 55, 60),
}

cat4_f0 = [
    "................",
    "....oo.oo.......",
    "....olfflo......",
    "....okffko......",
    ".....offffffft..",
    "...ooffffffffft.",
    "...of.....of.ot.",
    "...oo.....oo.o..",
]

cat4_f1 = [
    "................",
    "....oo.oo.......",
    "....olfflo......",
    "....okffko......",
    ".....offfffft...",
    "..oooffffffffft.",
    "...of....of..ot.",
    "...oo....oo...o.",
]

cat4_f2 = [
    "................",
    "..oo.oo.........",
    "..olfflo........",
    "..okffko........",
    "...offffffffft..",
    ".....of...of.ot.",
    ".....oo...oo.o..",
]

# ─── 5. にんじゃ (Blue-grey cat - jumping) ───
cat5_palette = {
    'o': (60, 70, 90),
    'f': (135, 155, 180),
    'l': (175, 195, 220),
    'k': (40, 40, 60),
    'p': (195, 165, 175),
    't': (125, 145, 170),
}

cat5_f0 = [
    ".....oo.oo......",
    ".....olfflo.....",
    ".....okffko.....",
    "......offfft....",
    "......offfft....",
    ".....off.off....",
    "......oo..oo....",
]

cat5_f1 = [
    "...oo.oo........",
    "...olfflo.......",
    "...okffko.......",
    "....offfft......",
    ".....ff.ff......",
    "................",
]

cat5_f2 = [
    ".......oo.oo....",
    ".......olfflo...",
    ".......okffko...",
    "........offfft..",
    "........offfft..",
    ".......off.off..",
    "........oo..oo..",
]

# ─── 6. ボスねこ (Golden cat - full sprint) ───
cat6_palette = {
    'o': (155, 125, 25),
    'f': (245, 205, 85),
    'l': (255, 235, 140),
    'k': (50, 35, 20),
    'p': (225, 175, 155),
    't': (235, 195, 70),
}

cat6_f0 = [
    "...oo.oo........",
    "...olfflo.......",
    "...okffko.......",
    "....offffffffft.",
    "....offffffffft.",
    "...of.....of.ot.",
    "...oo.....oo.o..",
]

cat6_f1 = [
    "...oo.oo........",
    "...olfflo.......",
    "...okffko.......",
    "....offffffffft.",
    "....offffffffft.",
    ".....of.of....ot",
    ".....oo.oo....o.",
]

cat6_f2 = [
    "...oo.oo........",
    "...olfflo.......",
    "...okffko.......",
    "....offffffffft.",
    "....offffffffft.",
    "......of...of.ot",
    "......oo...oo.o.",
]

# ═══════════════════════════════════════════════════
#  生成実行
# ═══════════════════════════════════════════════════
characters = [
    ("egg",       cat1_palette, [cat1_f0, cat1_f1, cat1_f2]),
    ("slime",     cat2_palette, [cat2_f0, cat2_f1, cat2_f2]),
    ("wolf",      cat3_palette, [cat3_f0, cat3_f1, cat3_f2]),
    ("demon",     cat4_palette, [cat4_f0, cat4_f1, cat4_f2]),
    ("dragon",    cat5_palette, [cat5_f0, cat5_f1, cat5_f2]),
    ("goddragon", cat6_palette, [cat6_f0, cat6_f1, cat6_f2]),
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
