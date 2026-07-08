#!/bin/bash
# 小红书图文卡片渲染脚本
# 用法: bash render.sh <html_file> <output_dir>
# 依赖: Google Chrome (headless mode), Python 3 + Pillow + numpy

set -e

HTML_FILE="$1"
OUTPUT_DIR="$2"

if [ -z "$HTML_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "用法: bash render.sh <html_file> <output_dir>"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -f "$CHROME" ]; then
  CHROME=$(which google-chrome 2>/dev/null || which google-chrome-stable 2>/dev/null || which chromium 2>/dev/null || echo "")
fi
if [ -z "$CHROME" ]; then
  echo "错误: 找不到 Chrome/Chromium"
  exit 1
fi

# Step 1: 截图整页
echo "📷 截图整页..."
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --screenshot="$OUTPUT_DIR/full-page.png" \
  --window-size=1080,14400 \
  --force-device-scale-factor=2 \
  --virtual-time-budget=12000 \
  "file://$HTML_FILE" 2>/dev/null

# Step 2: 像素级边界检测切割
echo "✂️ 切割卡片..."
python3 << PYEOF
from PIL import Image
import numpy as np

img = Image.open("$OUTPUT_DIR/full-page.png")
arr = np.array(img)

# 扫描左边缘 (x=4, 避免文字干扰)，取完整 RGB 三通道
col = arr[:, 4, :3]

bounds = []
inside = False
for y in range(len(col)):
    if not inside:
        r, g, b = col[y][:3]  # RGB 通道
        # 计算与 body 背景色 #1a1a1a 的差异
        diff = abs(int(r) - 0x1a) + abs(int(g) - 0x1a) + abs(int(b) - 0x1a)
        if diff > 60:  # 与背景差异大于阈值，是卡片区域
            inside = True
            start = y
    else:
        r, g, b = col[y][:3]
        diff = abs(int(r) - 0x1a) + abs(int(g) - 0x1a) + abs(int(b) - 0x1a)
        if diff <= 60:
            bounds.append((start, y))
            inside = False

# 过滤: 只保留高度 > 1000px 的真实卡片
bounds = [(y0, y1) for y0, y1 in bounds if (y1 - y0) > 1000]

for i, (y0, y1) in enumerate(bounds):
    card = img.crop((0, y0, img.width, y1))
    card.save(f"$OUTPUT_DIR/card-{i+1:02d}.png")

print(f"完成: {len(bounds)} 张卡片 → $OUTPUT_DIR/")
PYEOF

echo "✅ 渲染完成"
