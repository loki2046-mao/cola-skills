> **⚠️ 本文件为 simple 模式（轻量快速版）专用配色系统。** brand 模式请使用 `references/themes.md` 的 9 套配色主题。
>
> 两者不要混用：palettes.md 的 5 组配色用于 assets/templates/ 的快速模板；themes.md 的 9 套主题用于 carousel-v2.html 品牌风格模板。

# 配色系统 (Palette System)

## 全局色彩法则

所有卡片必须遵守 ljg-card 的 **90/8/2 法则**：
- **90%** — 中性底色（背景、大面积留白）
- **8%** — 结构色（分割线、页码、标注、次要文字）
- **2%** — 强调色（标题关键词、核心数据、CTA 高亮）

## 硬性禁令

- ❌ 禁止纯黑 `#000000` → 用 `#1D1D1F` 或 `#1A1A1A`
- ❌ 禁止 AI 紫蓝渐变（`#667eea → #764ba2` 等）
- ❌ 禁止过饱和强调色（饱和度 > 80%）
- ❌ 禁止冷暖色混用 — 同一套卡片内严格统一色调
- ❌ 禁止渐变背景 — 2026 趋势是暖色固体 + 微妙纹理

## 5 组预设色板

每组包含：`bg`（底色）、`text`（正文）、`mid`（次要文字）、`dim`（注释/页码）、`accent`（强调色）、`rule`（分割线）。

---

### 1. editorial-warm（编辑暖色）— 默认

适合：知识干货、深度思考、职场、个人成长

| Token | 色值 | 用途 |
|-------|------|------|
| `bg` | `#FAF8F4` | 卡片底色 |
| `text` | `#1D1D1F` | 标题/正文 |
| `mid` | `#6E6E73` | 次要文字 |
| `dim` | `#ACACB0` | 注释/页码 |
| `accent` | `#7C6853` | 强调色 |
| `rule` | `#E5E5EA` | 分割线 |
| `highlight-bg` | `#F3F0EB` | 高亮块底 |

---

### 2. tech-dark（科技深色）

适合：AI/科技、编程、数码产品、数据分析

| Token | 色值 | 用途 |
|-------|------|------|
| `bg` | `#1A1A2E` | 卡片底色 |
| `text` | `#EAEAEC` | 标题/正文 |
| `mid` | `#8E8E9A` | 次要文字 |
| `dim` | `#5A5A68` | 注释/页码 |
| `accent` | `#4A90D9` | 强调色 |
| `rule` | `#2A2A3E` | 分割线 |
| `highlight-bg` | `#222240` | 高亮块底 |

---

### 3. lifestyle-warm（生活方式暖色）

适合：生活方式、美食、旅行、家居、情感

| Token | 色值 | 用途 |
|-------|------|------|
| `bg` | `#FBF6F0` | 卡片底色 |
| `text` | `#3A3028` | 标题/正文 |
| `mid` | `#8B7D6E` | 次要文字 |
| `dim` | `#BFB0A0` | 注释/页码 |
| `accent` | `#C4A484` | 强调色 |
| `rule` | `#E8DDD0` | 分割线 |
| `highlight-bg` | `#F5EDE2` | 高亮块底 |

---

### 4. bold-creative（创意撞色）

适合：时尚美妆、创意设计、潮流趋势、Z 世代

| Token | 色值 | 用途 |
|-------|------|------|
| `bg` | `#FAF8F4` | 卡片底色 |
| `text` | `#1D1D1F` | 标题/正文 |
| `mid` | `#6E6E73` | 次要文字 |
| `dim` | `#ACACB0` | 注释/页码 |
| `accent` | `#FF6B35` | 强调色（活力橙） |
| `rule` | `#E5E5EA` | 分割线 |
| `highlight-bg` | `#FFF0E8` | 高亮块底 |

---

### 5. literary-calm（文艺柔和）

适合：读书笔记、诗歌、情绪文字、心理、治愈

| Token | 色值 | 用途 |
|-------|------|------|
| `bg` | `#F4F2ED` | 卡片底色 |
| `text` | `#3A3530` | 标题/正文 |
| `mid` | `#8B8578` | 次要文字 |
| `dim` | `#BFBAAE` | 注释/页码 |
| `accent` | `#7D8C6E` | 强调色（橄榄绿） |
| `rule` | `#E5E2DA` | 分割线 |
| `highlight-bg` | `#EEEAE2` | 高亮块底 |

---

## 选色决策树

```
内容类型？
├─ 知识/职场/深度思考 → editorial-warm
├─ AI/科技/编程     → tech-dark
├─ 生活方式/美食/旅行 → lifestyle-warm
├─ 时尚/美妆/创意    → bold-creative
├─ 读书/情绪/治愈    → literary-calm
└─ 不确定            → editorial-warm（默认）
```

## CSS 自定义属性注入

生成 HTML 时，将选中色板的 token 注入为 CSS 变量：

```css
:root {
  --bg: {{bg}};
  --text: {{text}};
  --mid: {{mid}};
  --dim: {{dim}};
  --accent: {{accent}};
  --rule: {{rule}};
  --highlight-bg: {{highlight-bg}};
}
```
