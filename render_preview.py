#!/usr/bin/env python3
"""
現在のキャラクターをPNG画像にレンダリングするスクリプト
各キャラの16x16ピクセルグリッドを拡大して見やすくする
"""

from PIL import Image, ImageDraw, ImageFont
import os
import sys

# generate_art.py からデータを読み込む
sys.path.insert(0, os.path.dirname(__file__))
from generate_art import characters

PIXEL_SIZE = 16  # 1ピクセルあたりのサイズ
PADDING = 20
BG_COLOR = (30, 30, 35)  # ダーク背景
LABEL_HEIGHT = 40

labels = {
    'cutecat': 'キュートねこ (Cute Cat)',
    'egg': 'こたま (Kotama)',
    'slime': 'こねこ (Koneko)',
    'wolf': 'さんぽ (Sanpo)',
    'demon': 'ハンター (Hunter)',
    'dragon': 'にんじゃ (Ninja)',
    'goddragon': 'ボスねこ (Boss Cat)',
}

def render_character(grid, palette, pixel_size=PIXEL_SIZE):
    """16x16 pixel grid → PIL Image"""
    w = 16 * pixel_size
    h = 16 * pixel_size
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for row_idx, row in enumerate(grid):
        for col_idx, ch in enumerate(row):
            if ch in palette:
                color = palette[ch]
                x0 = col_idx * pixel_size
                y0 = row_idx * pixel_size
                draw.rectangle([x0, y0, x0 + pixel_size - 1, y0 + pixel_size - 1], fill=color)
    return img


def main():
    # 全キャラクターを1枚にまとめる
    char_w = 16 * PIXEL_SIZE + PADDING * 2
    char_h = 16 * PIXEL_SIZE + LABEL_HEIGHT + PADDING * 2

    cols = 4
    rows = 2
    total_w = cols * char_w + PADDING
    total_h = rows * char_h + PADDING

    canvas = Image.new('RGB', (total_w, total_h), BG_COLOR)
    draw = ImageDraw.Draw(canvas)

    for idx, (name, palette, frames) in enumerate(characters):
        col = idx % cols
        row = idx // cols
        x_offset = PADDING + col * char_w
        y_offset = PADDING + row * char_h

        # ラベル描画
        label = labels.get(name, name)
        try:
            font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", 18)
        except:
            font = ImageFont.load_default()
        draw.text((x_offset, y_offset), label, fill=(255, 255, 255), font=font)

        # キャラクター描画
        char_img = render_character(frames[0], palette)
        canvas.paste(char_img, (x_offset, y_offset + LABEL_HEIGHT), char_img)

    out_path = os.path.join(os.path.dirname(__file__), "preview_all.png")
    canvas.save(out_path)
    print(f"Preview saved: {out_path}")

    # 個別キャラも保存
    for name, palette, frames in characters:
        char_img = render_character(frames[0], palette, pixel_size=32)
        bg = Image.new('RGB', (16*32 + 40, 16*32 + 40), BG_COLOR)
        bg.paste(char_img, (20, 20), char_img)
        path = os.path.join(os.path.dirname(__file__), f"preview_{name}.png")
        bg.save(path)
        print(f"  Saved: {path}")


if __name__ == '__main__':
    main()
