# 排版系统 (Typography System)

## 字体栈

### 中文优先

```css
--font-serif: 'Noto Serif SC', 'Songti SC', 'STSong', 'SimSun', serif;
--font-sans: 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', system-ui, sans-serif;
--font-mono: 'SF Mono', 'JetBrains Mono', 'Consolas', monospace;
--font-hand: 'Ma Shan Zheng', 'ZCOOL KuaiLe', 'Long Cang', cursive;
```

### 使用规则
- **封面大标题**：`--font-serif`（衬线体有质感）
- **正文**：`--font-sans`（清晰可读）
- **金句/高亮**：`--font-serif`（增加分量感）
- **代码/数据**：`--font-mono`
- **反 AI 手写点缀**：`--font-hand`（不用于大段正文）

## 硬性禁令

- ❌ **严禁 Inter 字体** — AI 生成内容的头号视觉标志
- ❌ 禁止纯黑 `#000000` — 用 `#1D1D1F` 或 `#1A1A1A`
- ❌ 禁止标题靠单纯放大建立层级 — 用字重和颜色

## 字号层级

基于 1080px 宽度画布，DPR 2x。手机端缩放约 2.8 倍（1080→390），正文 ≥ 36px 确保移动端可读。

| 层级 | 角色 | 字号 | 行高 | 字重 |
|------|------|------|------|------|
| H0 | 封面主标题 | 80-120px | 1.12-1.18 | 700 |
| H1 | 内页标题 | 56-84px | 1.15-1.25 | 600-700 |
| H2 | 章节标题 | 42-52px | 1.25-1.4 | 600 |
| body | 正文 | 36-42px | 1.6-1.7 | 400 |
| highlight | 金句/高亮 | 40-48px | 1.5-1.55 | 500 |
| small | 标注/说明 | 24-28px | 1.4-1.5 | 400-500 |
| meta | 页码/运行标题 | 20-24px | 1.3 | 400 |
| num-big | 大数字（对比卡） | 72-96px | 1.0 | 700 |

## 尺寸约束

- 正文最大行宽：**56-65ch**（约 600-700px）
- 标题最大行宽：不受限（允许撑满）
- 标题 `letter-spacing: -0.02em 至 -0.03em`（稍微紧凑）
- 正文 `letter-spacing: normal`
- 运行标题 `letter-spacing: 0.08em`（稍微松散）

## "越大越细"规则 (Guizang 原则)

当标题字号 > 72px 时，字重必须 ≤ 400。避免又大又粗的"砸脸"效果。

例外：封面主标题（H0）可以用 700 字重 + 最大字号，因为封面需要冲击力。

## 移动端可读性自检

生成卡片后必须确认：
- 正文 ≥ 36px（1080 ÷ 2.8 ≈ 390px 屏幕，36 ÷ 2.8 ≈ 13px，可读底线）
- 标注 ≥ 24px
- 页码 ≥ 20px
- 没有超过 65ch 的正文行（太宽会丢失阅读位置）

## 字体加载

HTML 模板头部加载 Google Fonts：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap" rel="stylesheet">
```

- 用 `font-display: swap` 避免 FOIT
- 中文 web font 体积大，`--virtual-time-budget=10000` 留足加载时间
