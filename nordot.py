#!/usr/bin/env python3
"""
画像をNordカラースキーム（青と黒）のドット絵に変換するスクリプト
"""
import sys
from PIL import Image
import numpy as np

# Nordカラースキーム（青系と黒）
NORD_COLORS = [
    (46, 52, 64),      # Nord0 (Polar Night - 最も暗い)
    (59, 66, 82),      # Nord1 (Polar Night)
    (67, 76, 94),      # Nord2 (Polar Night)
    (76, 86, 106),     # Nord3 (Polar Night - 最も明るい)
    (94, 129, 172),    # Nord9 (Frost - 青)
    (129, 161, 193),   # Nord10 (Frost - 明るい青)
]

def closest_nord_color(rgb):
    """最も近いNordカラーを見つける"""
    min_dist = float('inf')
    closest = NORD_COLORS[0]

    for nord_color in NORD_COLORS:
        dist = sum((a - b) ** 2 for a, b in zip(rgb, nord_color))
        if dist < min_dist:
            min_dist = dist
            closest = nord_color

    return closest

def convert_to_pixel_art(image_path, output_path, pixel_size=8, gap=0):
    """画像をNordカラーのドット絵に変換"""
    # 画像を開く
    img = Image.open(image_path).convert('RGB')

    # リサイズ（ドット絵化）
    width, height = img.size
    new_width = width // pixel_size
    new_height = height // pixel_size

    # 縮小してからアップスケール
    img_small = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Nordカラーに変換
    pixels = np.array(img_small)
    nord_pixels = np.zeros_like(pixels)

    for i in range(new_height):
        for j in range(new_width):
            nord_pixels[i, j] = closest_nord_color(tuple(pixels[i, j]))

    # 新しい画像を作成
    nord_img = Image.fromarray(nord_pixels.astype('uint8'), 'RGB')

    if gap > 0:
        # 隙間ありバージョン
        effective_pixel_size = pixel_size - gap
        final_width = new_width * pixel_size
        final_height = new_height * pixel_size

        # 背景色（最も暗いNord色）で初期化
        final_img = Image.new('RGB', (final_width, final_height), NORD_COLORS[0])

        # 各ピクセルを隙間を空けて描画
        for i in range(new_height):
            for j in range(new_width):
                color = tuple(nord_pixels[i, j])
                x = j * pixel_size
                y = i * pixel_size

                # ピクセルを描画（隙間分小さく）
                for py in range(effective_pixel_size):
                    for px in range(effective_pixel_size):
                        final_img.putpixel((x + px, y + py), color)
    else:
        # 隙間なしバージョン（従来通り）
        final_img = nord_img.resize((new_width * pixel_size, new_height * pixel_size),
                                    Image.Resampling.NEAREST)

    # 保存
    final_img.save(output_path)
    print(f"変換完了: {output_path}")
    print(f"元のサイズ: {width}x{height}")
    print(f"ドット絵サイズ: {new_width}x{new_height} ({pixel_size}x{pixel_size}ピクセル)")
    if gap > 0:
        print(f"ピクセル間の隙間: {gap}px")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python nord_pixel_art.py <入力画像> [出力画像] [ピクセルサイズ] [隙間サイズ]")
        print("例: python nord_pixel_art.py input.jpg output.png 8 2")
        print("    隙間サイズ: ピクセル間の隙間（0=なし、1-3推奨）")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "nord_pixel_art.png"
    pixel_size = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    gap = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    convert_to_pixel_art(input_path, output_path, pixel_size, gap)
