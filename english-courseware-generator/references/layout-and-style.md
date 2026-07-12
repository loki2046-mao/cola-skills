# 排版与风格系统

## 目录

1. [ZONE 排版系统](#zone-排版系统)
2. [画幅与分区](#画幅与分区)
3. [风格预设](#风格预设)
4. [色彩系统](#色彩系统)
5. [字体规则](#字体规则)
6. [边框与装饰](#边框与装饰)

---

## ZONE 排版系统

每张课件图用 ZONE 系统划分区域。ZONE 是在提示词中描述画面布局的核心方法，让生图模型理解每个区域的位置和内容。

### 基本三层结构

```
┌─────────────────────────┐
│       ZONE 1            │  顶部标题区 — Header
│   [课程标题 + 装饰]       │
├─────────────────────────┤
│                         │
│       ZONE 2            │  主内容区 — 组件内容
│   [组件1] [组件2]        │
│   [组件3] [组件4]        │
│                         │
├─────────────────────────┤
│       ZONE 3            │  底部区 — Footer
│   [slogan + 页码]        │
└─────────────────────────┘
```

### 多组件时的 ZONE 2 细分

当 ZONE 2 内有多个组件时，按 sub-zone 划分：

**2个组件（左右分）**：
```
ZONE 2a — 左半区：组件1
ZONE 2b — 右半区：组件2
```

**2个组件（上下分）**：
```
ZONE 2a — 上半区：组件1
ZONE 2b — 下半区：组件2
```

**3个组件**：
```
ZONE 2a — 上区（横跨）：组件1
ZONE 2b — 左下：组件2
ZONE 2c — 右下：组件3
```

**4个组件（2×2 grid）**：
```
ZONE 2a — 左上：组件1
ZONE 2b — 右上：组件2
ZONE 2c — 左下：组件3
ZONE 2d — 右下：组件4
```

### ZONE 描述模板

每个 ZONE 在提示词中这样描述：

```
ZONE [编号] — [位置描述]:
[区域内容描述]。包含以下文字："[具体文字内容逐字写入]"。
[视觉风格描述：边框、背景色、排列方式]。
```

---

## 画幅与分区

### 3:4 竖版（推荐，最适合课件）

```
┌───────────┐
│  ZONE 1   │  高度占比 10-15%
├───────────┤
│           │
│           │  高度占比 70-80%
│  ZONE 2   │  可放2-4个组件
│           │
│           │
├───────────┤
│  ZONE 3   │  高度占比 8-12%
└───────────┘
```

### 16:9 横版

```
┌──────────────────────────┐
│        ZONE 1            │  高度 12-15%
├──────────┬───────────────┤
│          │               │
│  ZONE 2a │   ZONE 2b     │  高度 70-78%
│          │               │
├──────────┴───────────────┤
│        ZONE 3            │  高度 8-12%
└──────────────────────────┘
```

### 1:1 正方

```
┌───────────────┐
│   ZONE 1      │  高度 12%
├───────────────┤
│               │
│   ZONE 2      │  高度 76%，建议只放1-2个组件
│               │
├───────────────┤
│   ZONE 3      │  高度 12%
└───────────────┘
```

---

## 风格预设

### cute_cartoon（默认，低龄首选）

```
色彩：马卡龙色系 — 柔粉、浅蓝、嫩绿、奶黄、薰衣草紫
边框：全圆角，粗线条，手绘感描边
字体：圆润可爱的无衬线体，粗体
背景：纯色或淡淡图案，不要太花
角色：Q版可爱风，大头小身
装饰：星星、爱心、小爪印、彩虹、云朵
```

提示词关键词：
```
cute cartoon style, pastel colors, rounded corners, playful and child-friendly, soft shadows, thick outlines, kawaii aesthetic, sticker-like illustrations
```

### flat_design（现代简洁）

```
色彩：高对比纯色 — 深蓝、亮橙、翠绿、纯白
边框：直角，细线，干净
字体：现代无衬线，中等粗细
背景：纯色或几何色块
角色：扁平插画风，简洁线条
装饰：几何图形、色块、图标
```

提示词关键词：
```
flat design style, bold solid colors, clean geometric shapes, sharp edges, modern minimal illustration, vector art style, no gradients, high contrast
```

### hand_drawn（温馨文艺）

```
色彩：暖色调 — 米色、暖棕、柔和橙红、草绿
边框：手绘线条，不规则，有温度
字体：手写体风格，温暖
背景：纸张质感、方格本、横线本
角色：手绘插画风，温暖笔触
装饰：手绘星星、涂鸦、胶带、便签
```

提示词关键词：
```
hand-drawn style, warm colors, sketchy outlines, paper texture, colored pencil aesthetic, cozy and warm, handwritten fonts, doodle decorations
```

---

## 色彩系统

### 按课程类型推荐

| 课程类型 | 推荐色彩 | 气质 |
|----------|----------|------|
| 词汇课 | Pastel 马卡龙 | 活泼轻松 |
| 对话课 | Warm + Vibrant 暖明快 | 温暖友好 |
| 语法课 | Cool Blue + White 冷蓝白 | 清晰理性 |
| 游戏课 | Vibrant 明快高对比 | 趣味刺激 |
| 复习课 | Muted 柔和 | 专注平静 |
| 阅读课 | Warm Neutral 暖中性 | 温馨阅读 |

### 主题色彩参考

| 主题 | 主色 | 辅色 |
|------|------|------|
| 疯狂动物城 | 动物城蓝 + 暖橙 | 草绿、灰蓝 |
| 小猪佩奇 | 粉红 | 浅蓝、红 |
| 原创水果王国 | 水果色彩（红橙黄绿紫） | 嫩绿 |
| 原创海洋世界 | 深蓝 + 浅蓝 | 珊瑚橙、海绿 |
| 原创太空冒险 | 深紫 + 银白 | 亮蓝、星黄 |

### 色彩描述模板

在提示词中这样描述色彩：
```
Color palette: [main color] background with [secondary color] accents. 
[accent color] for key elements and borders. 
Text in [dark color] for readability. 
Overall [mood] and [age-appropriate] feel.
```

---

## 字体规则

### 英文字体描述（用于提示词）

**推荐**：
- `rounded sans-serif` — 可爱圆润，适合低龄
- `bold playful sans-serif` — 活泼粗体，适合标题
- `clean geometric sans-serif` — 现代简洁，适合练习题
- `handwritten style font` — 手写感，适合 hand_drawn 风格
- `chunky letterforms` — 粗胖字母，适合词汇卡

**禁止指定**：商业字体名（Comic Sans MS、Helvetica 等），用风格描述替代。

### 中文字体描述

- `rounded Chinese font style` — 圆体，可爱
- `bold Chinese heading style` — 粗黑体标题
- `handwritten Chinese style` — 手写中文

### 文字大小层级

| 层级 | 用途 | 相对大小 |
|------|------|----------|
| 标题 | 课程主标题 | 最大（画面高度8-12%） |
| 副标题 | 课程中文名 | 标题的60% |
| 正文 | 词汇、题目 | 标题的40-50% |
| 辅助 | 翻译、提示 | 标题的30% |
| 微型 | 页码、标注 | 标题的20% |

---

## 边框与装饰

### 卡片边框

| 风格 | 边框描述 |
|------|----------|
| cute_cartoon | `rounded corners, thick outline, soft shadow` |
| flat_design | `sharp corners, thin border, no shadow` |
| hand_drawn | `sketchy hand-drawn border, slightly irregular` |

### 分隔线

组件之间的分隔：
- 虚线 `dashed dividing line`
- 圆点线 `dotted divider`
- 色块分隔 `color block separator`
- 装饰性分隔（爪印、星星排列）`decorative divider with [theme element]`

### 装饰元素

按主题选择装饰元素，写死在提示词中：

| 主题类型 | 装饰元素 |
|----------|----------|
| 动物城/动物 | paw prints, animal silhouettes, trees, leaves |
| 水果/食物 | fruit icons, drops, leaves |
| 海洋/水 | bubbles, waves, shells, fish |
| 太空/科技 | stars, planets, rockets, gears |
| 节日 | 节日相关图标 |
| 通用 | stars, hearts, clouds, rainbows |
