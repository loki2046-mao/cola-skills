# 小红书图文卡片截图 SOP

> 适用场景：用 HTML 生成多张 1080×1440 卡片，用 Chrome headless 截整页后切割为单张图片。

---

## 第一步：生成整页截图

```bash
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --screenshot="$OUT/full-page.png" \
  --window-size=1080,<足够高的值，如12000> \
  --force-device-scale-factor=2 \
  --virtual-time-budget=6000 \
  "$HTML_URL" 2>/dev/null
```

- `--force-device-scale-factor=2`：输出是 2x，实际宽度为 2160px，卡片高度为 2880px
- `--virtual-time-budget=6000`：等字体和动画加载完
- window-size 高度设够大，不要让页面被截断

---

## 第二步：用像素级边界检测切割（⚠️ 核心，不能用固定偏移量估算）

**绝对不要用固定 offset 手算**——字体加载、label 行高、gap 都会有几像素偏差，7张卡片累积下来落款会跑到下一张顶部。

正确做法：**扫描页面左侧固定列的像素颜色，检测卡片实际起止行**：

```python
from PIL import Image
import numpy as np

img = Image.open(f"{OUT}/full-page.png")
arr = np.array(img)

# 取 x=100（左边缘，远离内容噪点）这一列的 R 通道
# body 背景 #111 → R≈17，卡片内容 R>20
col = arr[:, 100, 0]

card_bounds = []
in_card = False
for y in range(len(col)):
    if not in_card and col[y] > 20:
        card_start = y
        in_card = True
    elif in_card and col[y] <= 20:
        card_bounds.append((card_start, y))
        in_card = False

# 过滤掉太短的（label 行、gap 行），只保留真正的卡片（高度接近 2880）
card_bounds = [(y0, y1) for y0, y1 in card_bounds if (y1 - y0) > 2000]
```

然后按检测到的真实边界裁图：

```python
for i, (y0, y1) in enumerate(card_bounds):
    card = img.crop((0, y0, 2160, y1))
    card_resized = card.resize((1080, 1440), Image.LANCZOS)
    card_resized.save(f"{OUT}/card-{i+1}.png", "PNG")
```

---

## HTML 模板注意事项

- `body` 背景必须是深色（`#111` 或更暗），与卡片颜色有足够对比，才能被像素扫描识别
- 卡片之间的 gap 不小于 `40px`（2x 后 80px），确保有足够暗行分隔
- 落款（`.brand`）和进度点（`.dots`）都用 `position: absolute` 固定在卡片内部，不要依赖外层容器

---

## 错误记录（2026-06-10）

**问题**：第一次用固定 offset 估算（`pad_top + i * block_h`），累积偏移导致落款跑到下一张卡顶部，进度点被压在上一张底部。

**修复**：改用像素级边界扫描，7张卡片全部精准裁切。

---

> 更新时间：2026-06-10
