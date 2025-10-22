# Nordot

画像をNordカラースキーム（青と黒）のドット絵に変換するツール

## インストール

```bash
pip install Pillow numpy
```

## 使い方

```bash
python nordot.py <入力画像> [出力画像] [ピクセルサイズ] [隙間サイズ]
```

### 例

```bash
# 基本
python nord_pixel_art.py photo.jpg

# ピクセルサイズ指定
python nord_pixel_art.py photo.jpg output.png 16

# 隙間を空ける（ドット絵風）
python nord_pixel_art.py photo.jpg output.png 8 2
```

## パラメータ

- **入力画像**: 変換する画像ファイル（必須）
- **出力画像**: 保存先（デフォルト: `nord_pixel_art.png`）
- **ピクセルサイズ**: ドットの大きさ（デフォルト: `8`）
- **隙間サイズ**: ピクセル間の隙間（デフォルト: `0`、推奨: `1-3`）

## カラーパレット

Nordカラースキームの青と黒系6色を使用:
- Nord0-3: Polar Night（黒系4色）
- Nord9-10: Frost（青系2色）
