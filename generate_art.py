#!/usr/bin/env python3
"""
monster-line キャラクター ピクセルアート生成スクリプト v2
16x16 ピクセルグリッドから ANSI半ブロック文字アートを生成
画像プレビューから改善: 大きな目、明確なシルエット、キャラ毎の個性
"""

import os

ART_DIR = os.path.join(os.path.dirname(__file__), "assets")

def render_ansi(grid, palette):
    """16x16 pixel grid → 8-line ANSI art (using ▄ half-blocks)"""
    lines = []
    for row in range(0, 16, 2):
        line = ""
        for col in range(16):
            top_ch = grid[row][col] if row < len(grid) and col < len(grid[row]) else '.'
            bot_ch = grid[row+1][col] if row+1 < len(grid) and col < len(grid[row+1]) else '.'
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
    return "\n".join(lines) + "\n"


def save_art(name, content):
    path = os.path.join(ART_DIR, name)
    with open(path, 'w') as f:
        f.write(content)
    print(f"  Generated: {name}")


# ═══════════════════════════════════════════════════
#  1. タマゴ (Egg) - 純粋なたまご。顔なし。ヒビ模様のみ。
# ═══════════════════════════════════════════════════
egg_palette = {
    'o': (80, 65, 45),       # outline
    'e': (255, 240, 210),    # shell main
    's': (245, 225, 190),    # shell shade
    'c': (180, 155, 120),    # crack
    'h': (255, 250, 235),    # highlight
}

egg_f0 = [
    "................",
    "......oooo......",
    "....oohhhsoo....",
    "...ohhhhhssso...",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oesscsssseso..",
    "..oesscssseso...",
    "..oesssssseso...",
    "...oesssssso....",
    "....oesssso.....",
    ".....oooooo.....",
    "................",
]

egg_f1 = [
    "................",
    "......oooo......",
    "....oohhhsoo....",
    "...ohhhhhssso...",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oesscsssseso..",
    "..oesscssseso...",
    "..oesssssseso...",
    "...oesssssso....",
    "....oesssso.....",
    ".....oooooo.....",
    "................",
]

egg_f2 = [
    "................",
    "......oooo......",
    "....oohhhsoo....",
    "...ohhhhhssso...",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oessssssseso..",
    "..oesscsssseso..",
    "..oesscssseso...",
    "..oesssssseso...",
    "...oesssssso....",
    "....oesssso.....",
    "......oooooo....",
    "................",
]

# ═══════════════════════════════════════════════════
#  2. スライム (Slime) - ドラクエ風。大きな目＋にっこり口
# ═══════════════════════════════════════════════════
slime_palette = {
    'o': (15, 70, 25),       # outline
    'g': (50, 190, 90),      # body
    'l': (90, 220, 130),     # light body
    'L': (130, 240, 160),    # lightest/top
    'd': (30, 140, 60),      # dark body
    'w': (255, 255, 255),    # eye white
    'k': (20, 20, 30),       # pupil
    'i': (180, 220, 255),    # eye highlight
    'm': (200, 60, 80),      # mouth
    'c': (255, 150, 170),    # cheek
}

slime_f0 = [
    "................",
    "......oggo......",
    ".....oLLLgo.....",
    "....oLLLlggo....",
    "...oLllllgggo...",
    "..olllggggggoo..",
    "..oliwggiwogooo.",
    "..olwkggwkgooo..",
    "..olggggggggoo..",
    "..olggmmmmggoo..",
    "..ocggggggggco..",
    "...odggggggoo...",
    "....odddddoo....",
    ".....oooooo.....",
    "................",
    "................",
]

slime_f1 = [
    "................",
    "................",
    "......oggo......",
    ".....oLLLgo.....",
    "....oLLLlggo....",
    "...oLllllgggo...",
    "..olllggggggoo..",
    "..oliwggiwogooo.",
    "..olwkggwkgooo..",
    "..olggggggggoo..",
    "..olggmmmmggoo..",
    "..ocggggggggco..",
    "...odddddddoo..",
    "....ooooooo.....",
    "................",
    "................",
]

slime_f2 = [
    "................",
    ".....oggggo.....",
    "....oLLLlggo....",
    "...oLLlllgggo...",
    "..oLlllllgggoo..",
    "..olliwggiwogoo.",
    "..ollwkggwkgooo.",
    "..ollgggggggooo.",
    "..ollggmmmggooo.",
    "...ocgggggggco..",
    "....odggggoo....",
    ".....oddddoo....",
    "......ooooo.....",
    "................",
    "................",
    "................",
]

# ═══════════════════════════════════════════════════
#  3. ウルフ (Wolf) - 正面顔。大きな耳。黄色い目。白いマズル。
# ═══════════════════════════════════════════════════
wolf_palette = {
    'o': (40, 30, 25),       # outline
    'f': (150, 130, 100),    # fur main
    'l': (180, 160, 130),    # fur light
    'd': (100, 85, 65),      # fur dark
    'w': (235, 225, 210),    # white muzzle
    'W': (255, 255, 255),    # eye white
    'k': (25, 25, 30),       # eye/nose dark
    'e': (240, 200, 50),     # eye yellow
    'n': (30, 25, 25),       # nose
    'p': (200, 140, 110),    # inner ear
    'r': (190, 70, 70),      # tongue
    'b': (210, 195, 175),    # belly light
}

wolf_f0 = [
    "..od........do..",
    "..ofd.oooo.dfo..",
    "..ofpdo..odpfo..",
    "..ofpfooooofpfo.",
    ".ooffllffllffoo.",
    ".oofWefffWefooo.",
    ".oofkefffkefoo..",
    "..offwwwnwwfo...",
    "..ofwwwwwwwfo...",
    "..ofwwwrwwwfo...",
    "...ofwwwwwfo....",
    "...offfffffo....",
    "...offbbbffo....",
    "..ofo.ooo.ofo...",
    "..oo..ooo..oo...",
    "................",
]

wolf_f1 = [
    "..od........do..",
    "..ofd.oooo.dfo..",
    "..ofpdo..odpfo..",
    "..ofpfooooofpfo.",
    ".ooffllffllffoo.",
    ".oofWefffWefooo.",
    ".oofkefffkefoo..",
    "..offwwwnwwfo...",
    "..ofwwwwwwwfo...",
    "..ofwwwrwwwfo...",
    "...ofwwwwwfo....",
    "...offfffffo....",
    "...offbbbffo....",
    "...ofo.ooo.ofo..",
    "...oo..ooo..oo..",
    "................",
]

wolf_f2 = [
    "..od........do..",
    "..ofd.oooo.dfo..",
    "..ofpdo..odpfo..",
    "..ofpfooooofpfo.",
    ".ooffllffllffoo.",
    ".oofWefffWefooo.",
    ".oofkefffkefoo..",
    "..offwwwnwwfo...",
    "..ofwwwwwwwfo...",
    "..ofwwwrwwwfo...",
    "...ofwwwwwfo....",
    "...offfffffo....",
    "...offbbbffo....",
    "..ofo.ooo..ofo..",
    "..oo..ooo...oo..",
    "................",
]

# ═══════════════════════════════════════════════════
#  4. アクマ (Demon) - 大きな角、コウモリ翼、牙
# ═══════════════════════════════════════════════════
demon_palette = {
    'o': (50, 15, 25),       # outline
    'r': (200, 45, 65),      # body red
    'R': (230, 80, 100),     # light red
    'd': (150, 30, 50),      # dark red
    'h': (120, 50, 140),     # horn purple
    'H': (90, 35, 110),      # horn dark
    'w': (100, 50, 150),     # wing
    'W': (130, 70, 170),     # wing light
    'e': (255, 230, 50),     # eye yellow
    'k': (30, 15, 15),       # pupil
    'm': (255, 255, 255),    # teeth white
    't': (180, 60, 80),      # tail
    'c': (255, 160, 180),    # cheek
    'p': (170, 35, 55),      # belly
}

demon_f0 = [
    "..Hh........hH..",
    "..oh.oooooo.ho..",
    ".oo.orRRRRro.oo.",
    ".oo.orRRRRro.oo.",
    "oWo.orekerro.oWo",
    "oWoorrkrrrrooowo",
    "owo.orcrrcrro.oo",
    "owoorrrmrrrroo..",
    ".o.orrrmmrrrooo.",
    ".ooorrddddrro...",
    "...orrpppprroo..",
    "...orrrrrrrrooo.",
    "...oorrddrro.t..",
    "....oro.orooto..",
    "....oo..oo.oo...",
    "................",
]

demon_f1 = [
    "..Hh........hH..",
    "..oh.oooooo.ho..",
    ".oo.orRRRRro.oo.",
    ".oo.orRRRRro.oo.",
    "oWo.orekerro.oWo",
    "oWoorrkrrrrooowo",
    "owo.orcrrcrro.oo",
    "owoorrrmrrrroo..",
    ".o.orrrmmrrrooo.",
    ".ooorrddddrro...",
    "...orrpppprroo..",
    "...orrrrrrrrooo.",
    "...oorrddrro..t.",
    "....oro.oro.oto.",
    "....oo..oo..oo..",
    "................",
]

demon_f2 = [
    "..Hh........hH..",
    "..oh.oooooo.ho..",
    ".oo.orRRRRro.oo.",
    ".oo.orRRRRro.oo.",
    "oWo.orekerro.oWo",
    "oWoorrkrrrrooowo",
    "owo.orcrrcrro.oo",
    "owoorrrmrrrroo..",
    ".o.orrrmmrrrooo.",
    ".ooorrddddrro...",
    "...orrpppprroo..",
    "...orrrrrrrro...",
    "...oorrddrroo.t.",
    "...oro..oro.oto.",
    "...oo...oo..oo..",
    "................",
]

# ═══════════════════════════════════════════════════
#  5. リュウ (Dragon) - 横向きドラゴン。長い首、翼、火
# ═══════════════════════════════════════════════════
dragon_palette = {
    'o': (10, 35, 70),       # outline
    'b': (45, 110, 210),     # body blue
    'l': (80, 155, 245),     # light blue
    'L': (120, 185, 255),    # lightest blue
    'd': (25, 70, 150),      # dark blue
    'w': (140, 200, 255),    # wing membrane
    'W': (100, 170, 240),    # wing darker
    's': (60, 130, 195),     # scale
    'e': (255, 210, 50),     # eye
    'k': (15, 15, 25),       # pupil
    'n': (200, 225, 255),    # belly
    'f': (255, 130, 30),     # fire orange
    'F': (255, 60, 20),      # fire red
    'Y': (255, 220, 80),     # fire yellow
    'h': (35, 80, 170),      # horn
    't': (55, 120, 200),     # tail
}

dragon_f0 = [
    "wWo..........oWw",
    "wWWo..ohho..oWWw",
    ".wWo.oblbbo.oWw.",
    ".oo.oblLLlbo.oo.",
    ".oo.obeklkebo.o.",
    "...oobbbkbbbbo..",
    "...oobbbbbbbbo..",
    "...oobbbssbbbo..",
    "....obbbbbbbo...",
    "....obddddbo....",
    "....obnnnnbo....",
    "....obbbbbbot...",
    ".....obdboo.ot..",
    "....obo.obo..oo.",
    "....oo...oo.....",
    "................",
]

dragon_f1 = [
    "wWo..........oWw",
    "wWWo..ohho..oWWw",
    ".wWo.oblbbo.oWw.",
    ".oo.oblLLlbo.oo.",
    ".oo.obeklkebo.o.",
    "...oobbbkbbbbo..",
    "...oobbbbbbbbo..",
    "...oobbbssbbbo..",
    "....obbbbbbbo...",
    "....obddddbo....",
    "....obnnnnbo....",
    "....obbbbbbot...",
    ".....obdboo..ot.",
    "....obo.obo..oo.",
    "....oo...oo.....",
    "................",
]

dragon_f2 = [
    "wWo..........oWw",
    "wWWo..ohho..oWWw",
    ".wWo.oblbbo.oWw.",
    ".oo.oblLLlbo.oo.",
    ".oo.obeklkebo.o.",
    "...oobbbkbbbbo..",
    "...oobbbbbbbbo..",
    "...oobbbssbbbo..",
    "....obbbbbbbo...",
    "....obddddbo....",
    "....obnnnnbo....",
    "....obbbbbbot...",
    ".....obdboo.ot..",
    "...obo..obo..oo.",
    "...oo....oo.....",
    "................",
]

# ═══════════════════════════════════════════════════
#  6. シンリュウ (God Dragon) - 金色、王冠、オーラ
# ═══════════════════════════════════════════════════
goddragon_palette = {
    'o': (90, 65, 10),       # outline gold-dark
    'g': (255, 200, 50),     # body gold
    'l': (255, 225, 100),    # light gold
    'L': (255, 240, 150),    # lightest gold
    'd': (200, 150, 30),     # dark gold
    'w': (255, 235, 130),    # wing light
    'W': (230, 185, 50),     # wing mid
    's': (220, 170, 35),     # scales
    'e': (255, 50, 50),      # eye red
    'k': (30, 10, 10),       # pupil
    'n': (255, 245, 200),    # belly
    'h': (210, 155, 25),     # horn
    'a': (255, 255, 220),    # aura/crown
    'c': (100, 200, 255),    # crystal/gem
    't': (220, 165, 25),     # tail
    'C': (160, 230, 255),    # crystal bright
}

goddragon_f0 = [
    "wWo...aCCCa..oWw",
    "wWWoh.oggo.hoWWw",
    ".wWo.ogLlgo.oWw.",
    ".oo.ogLcLlgo.oo.",
    ".oo.ogeklkego.o.",
    "...oogggkggggo..",
    "...ooggggggggoo.",
    "...oogggsssggo..",
    "....oggggggggo..",
    "....ogddddgo....",
    "....ognnnngoo...",
    "....oggggggot...",
    ".....ogddgoo.ot.",
    "....ogo..ogo.oo.",
    "....oo....oo....",
    "................",
]

goddragon_f1 = [
    "wWo...aCCCa..oWw",
    "wWWoh.oggo.hoWWw",
    ".wWo.ogLlgo.oWw.",
    ".oo.ogLcLlgo.oo.",
    ".oo.ogeklkego.o.",
    "...oogggkggggo..",
    "...ooggggggggoo.",
    "...oogggsssggo..",
    "....oggggggggo..",
    "....ogddddgo....",
    "....ognnnngoo...",
    "....oggggggot...",
    ".....ogddgoo..ot",
    "....ogo..ogo..oo",
    "....oo....oo....",
    "................",
]

goddragon_f2 = [
    "wWo...aCCCa..oWw",
    "wWWoh.oggo.hoWWw",
    ".wWo.ogLlgo.oWw.",
    ".oo.ogLcLlgo.oo.",
    ".oo.ogeklkego.o.",
    "...oogggkggggo..",
    "...ooggggggggoo.",
    "...oogggsssggo..",
    "....oggggggggo..",
    "....ogddddgo....",
    "....ognnnngoo...",
    "....oggggggooto.",
    ".....ogddgoo.ot.",
    "...ogo...ogo.oo.",
    "...oo.....oo....",
    "................",
]

# ═══════════════════════════════════════════════════
#  生成実行
# ═══════════════════════════════════════════════════
characters = [
    ("egg",       egg_palette,       [egg_f0, egg_f1, egg_f2]),
    ("slime",     slime_palette,     [slime_f0, slime_f1, slime_f2]),
    ("wolf",      wolf_palette,      [wolf_f0, wolf_f1, wolf_f2]),
    ("demon",     demon_palette,     [demon_f0, demon_f1, demon_f2]),
    ("dragon",    dragon_palette,    [dragon_f0, dragon_f1, dragon_f2]),
    ("goddragon", goddragon_palette, [goddragon_f0, goddragon_f1, goddragon_f2]),
]

os.makedirs(ART_DIR, exist_ok=True)

if __name__ == '__main__':
    for name, palette, frames in characters:
        print(f"\n[{name}]")
        art = render_ansi(frames[0], palette)
        save_art(f"{name}_clean.txt", art)
        save_art(f"{name}_ansi.txt", art)
        for i, frame in enumerate(frames):
            art = render_ansi(frame, palette)
            save_art(f"{name}_f{i}_clean.txt", art)
    print("\nAll art generated!")
