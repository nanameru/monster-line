#!/usr/bin/env python3
"""
monster-line キャラクター ピクセルアート生成スクリプト
16x16 ピクセルグリッドから ANSI半ブロック文字アートを生成
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
#  1. タマゴ (Egg)
# ═══════════════════════════════════════════════════
egg_palette = {
    'o': (60, 50, 40),      # outline dark
    'e': (255, 240, 210),   # egg shell light
    's': (240, 220, 180),   # egg shell mid
    'c': (200, 180, 140),   # crack color
    'h': (255, 200, 180),   # highlight
    'p': (255, 180, 200),   # pink spot
    'b': (200, 230, 255),   # blue spot
}

egg_f0 = [
    "................",
    "......oeeo......",
    ".....oesseo.....",
    "....oesshseo....",
    "...oesshhsseo...",
    "...oesssssseoo..",
    "...oesccssseo...",
    "..oescssssseo...",
    "..oessscssseoo..",
    "..oessssssseo...",
    "..oesssspsseoo..",
    "..oessbsssseo...",
    "...oessssseo....",
    "...oessssseo....",
    "....ooessoo.....",
    "......ooo.......",
]

egg_f1 = [
    "................",
    "......oeeo......",
    ".....oesseo.....",
    "....oesshseo....",
    "...oesshhsseo...",
    "...oesssssseoo..",
    "...oesccssseo...",
    "..oescssssseo...",
    "..oessscssseoo..",
    "..oessssssseo...",
    "..oesssspsseoo..",
    "..oessbsssseo...",
    "...oessssseo....",
    "...oessssseo....",
    "....ooessoo.....",
    ".......ooo......",
]

egg_f2 = [
    "................",
    "......oeeo......",
    ".....oesseo.....",
    "....oesshseo....",
    "...oesshhsseo...",
    "...oesssssseoo..",
    "...oesccssseo...",
    "..oescssssseo...",
    "..oessscssseoo..",
    "..oessssssseo...",
    "..oesssspsseoo..",
    "..oessbsssseo...",
    "...oessssseo....",
    "...oessssseo....",
    "....ooessoo.....",
    "......ooo.......",
]

# ═══════════════════════════════════════════════════
#  2. スライム (Slime)
# ═══════════════════════════════════════════════════
slime_palette = {
    'o': (20, 80, 30),       # outline
    'g': (60, 200, 100),     # body green
    'l': (100, 230, 140),    # light green
    'd': (40, 160, 70),      # dark green
    'w': (255, 255, 255),    # eye white
    'k': (30, 30, 40),       # eye pupil
    'm': (180, 60, 80),      # mouth
    'h': (150, 255, 180),    # highlight
    'c': (220, 80, 100),     # cheek
}

slime_f0 = [
    "................",
    "......oggo......",
    "....ogglgggo....",
    "...oglllggggoo..",
    "..ogllgggggggo..",
    "..ogwkggwkgggo..",
    ".ogggggmgggggo..",
    ".ogcgggggggcgo..",
    ".ogggggggggggoo.",
    ".odggggggggggoo.",
    ".odggggggggggo..",
    "..odggggggggo...",
    "...oddgggddo....",
    "....ooodooo.....",
    "................",
    "................",
]

slime_f1 = [
    "................",
    "................",
    "......oggo......",
    "....ogglgggo....",
    "...oglllggggoo..",
    "..ogllgggggggo..",
    "..ogwkggwkgggo..",
    ".ogggggmgggggo..",
    ".ogcgggggggcgo..",
    ".ogggggggggggoo.",
    ".odggggggggggoo.",
    "..odggggggggo...",
    "...oddgggddo....",
    "....ooodooo.....",
    "................",
    "................",
]

slime_f2 = [
    "................",
    ".....ogggo......",
    "...ogglggggo....",
    "..ogllllggggo...",
    ".ogllllggggggo..",
    ".ogwkgggwkgggo..",
    ".oggggggmggggo..",
    ".ogcggggggcggo..",
    "..oggggggggggo..",
    "..odgggggggggo..",
    "...odggggggo....",
    "....odddddo.....",
    ".....ooooo......",
    "................",
    "................",
    "................",
]

# ═══════════════════════════════════════════════════
#  3. ウルフ (Wolf)
# ═══════════════════════════════════════════════════
wolf_palette = {
    'o': (50, 40, 35),       # outline
    'f': (160, 140, 110),    # fur main
    'l': (190, 170, 140),    # fur light
    'd': (120, 100, 75),     # fur dark
    'w': (230, 220, 200),    # white belly/muzzle
    'k': (30, 30, 30),       # eye/nose
    'e': (220, 180, 50),     # eye yellow
    'n': (40, 30, 30),       # nose
    'p': (180, 130, 100),    # inner ear
    't': (200, 190, 170),    # teeth
    'r': (180, 60, 60),      # tongue
}

wolf_f0 = [
    ".od..........do.",
    ".ofd.o....o.dfo.",
    ".ofpdo....odpfo.",
    ".ofpfo.oo.ofpfo.",
    "oofflooddoollfo.",
    "oofflekffkellfoo",
    "oofffoknkoffffoo",
    ".offwwwnwwwffo..",
    "..ofwwwrwwwfo...",
    "..offwwwwwffo...",
    "...offffffo.....",
    "...offffffo.....",
    "...offdddffo....",
    "..ofo.of.ofo....",
    "..oo..oo..oo....",
    "................",
]

wolf_f1 = [
    ".od..........do.",
    ".ofd.o....o.dfo.",
    ".ofpdo....odpfo.",
    ".ofpfo.oo.ofpfo.",
    "oofflooddoollfo.",
    "oofflekffkellfoo",
    "oofffoknkoffffoo",
    ".offwwwnwwwffo..",
    "..ofwwwrwwwfo...",
    "..offwwwwwffo...",
    "...offffffo.....",
    "...offffffo.....",
    "...offdddffo....",
    "...ofo.of.ofo...",
    "...oo..oo..oo...",
    "................",
]

wolf_f2 = [
    ".od..........do.",
    ".ofd.o....o.dfo.",
    ".ofpdo....odpfo.",
    ".ofpfo.oo.ofpfo.",
    "oofflooddoollfo.",
    "oofflekffkellfoo",
    "oofffoknkoffffoo",
    ".offwwwnwwwffo..",
    "..ofwwwrwwwfo...",
    "..offwwwwwffo...",
    "...offffffo.....",
    "...offffffo.....",
    "...offdddffo....",
    "..ofo.of..ofo...",
    "..oo..oo...oo...",
    "................",
]

# ═══════════════════════════════════════════════════
#  4. アクマ (Demon)
# ═══════════════════════════════════════════════════
demon_palette = {
    'o': (60, 20, 30),       # outline
    'r': (190, 40, 60),      # body red
    'd': (150, 30, 50),      # dark red
    'l': (220, 70, 90),      # light red
    'h': (100, 40, 120),     # horn purple
    'w': (80, 50, 130),      # wing purple
    'e': (255, 240, 50),     # eye yellow
    'k': (30, 20, 20),       # pupil
    'm': (255, 255, 255),    # mouth/teeth
    't': (160, 60, 80),      # tail
    'p': (220, 100, 120),    # cheek
}

demon_f0 = [
    "..oh.........ho.",
    ".ohh..ooo..hho..",
    ".oh..orrrro.oho.",
    "oo..orlllrro..oo",
    "ow.orrekerlro.wo",
    "ow.orrrkrrrrooow",
    "ow.oprrrrrrpro.o",
    "owoorrmmmrrroo..",
    ".o.orrrrrrrroo..",
    ".ooorrddddrro...",
    "...orrrrrrrro...",
    "...orrrrrrrroo..",
    "...oordddro.t...",
    "....oro.orooto..",
    "....oo..oo.oto..",
    "...........oo...",
]

demon_f1 = [
    "..oh.........ho.",
    ".ohh..ooo..hho..",
    ".oh..orrrro.oho.",
    "oo..orlllrro..oo",
    "ow.orrekerlro.wo",
    "ow.orrrkrrrrooow",
    "ow.oprrrrrrpro.o",
    "owoorrmmmrrroo..",
    ".o.orrrrrrrroo..",
    ".ooorrddddrro...",
    "...orrrrrrrro...",
    "...orrrrrrrroo..",
    "...oordddro..t..",
    "....oro.oro.oto.",
    "....oo..oo..oto.",
    "............oo..",
]

demon_f2 = [
    "..oh.........ho.",
    ".ohh..ooo..hho..",
    ".oh..orrrro.oho.",
    "oo..orlllrro..oo",
    "ow.orrekerlro.wo",
    "ow.orrrkrrrrooow",
    "ow.oprrrrrrpro.o",
    "owoorrmmmrrroo..",
    ".o.orrrrrrrroo..",
    ".ooorrddddrro...",
    "...orrrrrrrro...",
    "...orrrrrrrroo..",
    "...oordddro.t...",
    "...oro.oro.oto..",
    "...oo..oo..oto..",
    "...........oo...",
]

# ═══════════════════════════════════════════════════
#  5. リュウ (Dragon)
# ═══════════════════════════════════════════════════
dragon_palette = {
    'o': (15, 40, 80),       # outline
    'b': (50, 120, 220),     # body blue
    'l': (80, 160, 255),     # light blue
    'd': (30, 80, 160),      # dark blue
    'w': (120, 180, 255),    # wing membrane
    's': (70, 140, 200),     # scales
    'e': (255, 200, 50),     # eye
    'k': (20, 20, 30),       # pupil
    'n': (200, 220, 255),    # belly light
    'f': (255, 120, 30),     # fire
    'r': (255, 60, 20),      # fire red
    'y': (255, 200, 80),     # fire yellow
    'h': (40, 90, 180),      # horn
    't': (60, 130, 210),     # tail
}

dragon_f0 = [
    "..oh.........ho.",
    ".ohh..obbo..hho.",
    ".oh.oblllbbo.ho.",
    "oo.oblllllbbooo.",
    "ow.obekbeklbo.wo",
    "owobbbnnbbbbooow",
    "ow.obbbbbbbbo.oo",
    "owoobbsssbbbooo.",
    "oo.obbbbbbbboo..",
    "..oobbddddbbo...",
    "...obbbbbbbboo..",
    "...obbbbbbbboo..",
    "...oobbddbo.t...",
    "....obo.obootoo.",
    "....oo..oo.oo...",
    "................",
]

dragon_f1 = [
    "..oh.........ho.",
    ".ohh..obbo..hho.",
    ".oh.oblllbbo.ho.",
    "oo.oblllllbbooo.",
    "ow.obekbeklbo.wo",
    "owobbbnnbbbbooow",
    "ow.obbbbbbbbo.oo",
    "owoobbsssbbbooo.",
    "oo.obbbbbbbboo..",
    "..oobbddddbbo...",
    "...obbbbbbbboo..",
    "...obbbbbbbboo..",
    "...oobbddbo..t..",
    "....obo.obo.oto.",
    "....oo..oo..oo..",
    "................",
]

dragon_f2 = [
    "..oh.........ho.",
    ".ohh..obbo..hho.",
    ".oh.oblllbbo.ho.",
    "oo.oblllllbbooo.",
    "ow.obekbeklbo.wo",
    "owobbbnnbbbbooow",
    "ow.obbbbbbbbo.oo",
    "owoobbsssbbbooo.",
    "oo.obbbbbbbboo..",
    "..oobbddddbbo...",
    "...obbbbbbbbo...",
    "...obbbbbbbboo..",
    "...oobbddboo.t..",
    "...obo.obo..oto.",
    "...oo..oo...oo..",
    "................",
]

# ═══════════════════════════════════════════════════
#  6. シンリュウ (God Dragon)
# ═══════════════════════════════════════════════════
goddragon_palette = {
    'o': (100, 70, 10),      # outline gold-dark
    'g': (255, 200, 50),     # body gold
    'l': (255, 230, 100),    # light gold
    'd': (200, 150, 30),     # dark gold
    'w': (255, 240, 150),    # wing light
    's': (230, 180, 40),     # scales
    'e': (255, 50, 50),      # eye red
    'k': (30, 10, 10),       # pupil
    'n': (255, 245, 200),    # belly
    'h': (220, 160, 30),     # horn
    'a': (255, 255, 200),    # aura/halo
    'f': (255, 100, 30),     # fire
    'r': (255, 50, 20),      # fire red
    'c': (180, 220, 255),    # crystal/jewel
    't': (230, 170, 30),     # tail
}

goddragon_f0 = [
    ".aoh....a....hoa",
    "aohh.aoggoa.hhoa",
    ".oh.ogllllggo.ho",
    "oo.ogllnllggooo.",
    "ow.ogekceglgo.wo",
    "owogggnnggggooow",
    "ow.ogssgssgo..oo",
    "owooggsssgggoo..",
    "oo.oggggggggooo.",
    "..ooggddddggo...",
    "...oggggggggooo.",
    "...oggggggggoo..",
    "...ooggddgoo.t..",
    "....ogo.ogo.oto.",
    "....oo..oo..oo..",
    "................",
]

goddragon_f1 = [
    "..oh....a....ho.",
    "aohh.aoggoa.hhoa",
    ".oh.ogllllggo.ho",
    "oo.ogllnllggooo.",
    "ow.ogekceglgo.wo",
    "owogggnnggggooow",
    "ow.ogssgssgo..oo",
    "owooggsssgggoo..",
    "oo.oggggggggooo.",
    "..ooggddddggo...",
    "...oggggggggooo.",
    "...oggggggggoo..",
    "...ooggddgoo..t.",
    "....ogo.ogo..oto",
    "....oo..oo...oo.",
    "................",
]

goddragon_f2 = [
    "a.oh.....a...hoa",
    "aohh.aoggoa.hhoa",
    ".oh.ogllllggo.ho",
    "oo.ogllnllggooo.",
    "ow.ogekceglgo.wo",
    "owogggnnggggooow",
    "ow.ogssgssgo..oo",
    "owooggsssgggoo..",
    "oo.oggggggggooo.",
    "..ooggddddggo...",
    "...oggggggggo...",
    "...oggggggggoo..",
    "...ooggddgo..t..",
    "...ogo.ogo..oto.",
    "...oo..oo...oo..",
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

for name, palette, frames in characters:
    print(f"\n[{name}]")
    # clean (default = frame 0)
    art = render_ansi(frames[0], palette)
    save_art(f"{name}_clean.txt", art)
    # ANSI version (same)
    save_art(f"{name}_ansi.txt", art)
    # 3 animation frames
    for i, frame in enumerate(frames):
        art = render_ansi(frame, palette)
        save_art(f"{name}_f{i}_clean.txt", art)

print("\nAll art generated!")
