---
name: loki-design-system
description: Loki 品牌设计系统 — 共享基础层。所有视觉 Skill（loki-deck/loki-social/loki-wechat-pipeline）的品牌规范单一来源（SSOT）。当用户明确要求查看品牌规范或做品牌审计时直接调用。
---
# loki-design-system · 赛博小熊猫 Loki 品牌设计系统

**定位：** 这是所有视觉 Skill 的共享基础层（Shared Base Layer），不是常规调用型 Skill。loki-deck、loki-social、loki-wechat-pipeline 等视觉 Skill 在生成内容时引用本系统的 brand-dna.md、scene-*.md 等规范文件。

**直接调用场景：**
- 用户要求查看品牌规范/设计系统
- 做品牌审计
- 创建新的视觉场景规范
- 其他视觉 Skill 未覆盖的场景需要手动调用设计系统

---

## 目录

```
loki-design-system/
├── SKILL.md                       ← 工作流入口（你在看这个）
├── assets/
│   ├── base.html                  ← 通用骨架（字体+CSS变量+Reset+工具类）★必读
│   └── loki-face.svg              ← 品牌 Logo SVG
├── templates/
│   ├── landing-page.html          ← Landing Page 完整骨架
│   ├── slides.html                ← 横向翻页 Slides 骨架
│   └── card.html                  ← 单页卡片/封面骨架
└── references/
    ├── brand-dna.md               ← ★核心：品牌基因（颜色/字体/IP/气质/禁用）
    ├── design-dna.md              ← ★核心：视觉指纹（质感/光线/构图/情绪/排版直觉）
    ├── scene-mapping.md           ← ★必读：内容类型→布局/底色/组件映射表（全场景索引）
    ├── scene-all.md               ← 10个场景总览表（组件数/状态/快速索引）
    ├── scene-landing.md           ← ★场景一：个人主页（5个组件+完整HTML）
    ├── scene-product.md           ← ★场景二：产品介绍页（6个组件+完整HTML）
    ├── scene-slides.md            ← ★场景三：演讲Slides（8种页型+完整HTML+节奏约束）
    ├── scene-rednote.md           ← ★场景六/七：小红书卡片（8种+完整HTML+手机字号基准）
    ├── scene-report.md            ← ★场景八：数据报告/横评（7种组件+苹绣等级色+MyTake苹综）
    ├── loki-spec.md               ← 完整规范（写作/封面IP互动/工作逻辑/设计DNA）
    ├── cover-templates.md         ← 公众号封面 3 种模板
    ├── article-components.md      ← 文章排版 12 个组件（含完整 HTML）
    ├── product-ui.md              ← 产品 UI 规范
    └── checklist.md               ← 质量检查清单 P0/P1/P2
```

---

## 工作流（严格按顺序，不能跳步）

### Step 0 · 判断场景（必读 scene-mapping.md）

**先读 `references/scene-mapping.md`**——它定义了不同内容类型对应什么底色方案、布局节奏、组件选择。**不同场景用不同的架构，不允许把个人主页的架构套在产品介绍上。**

| 用户要做什么 | 用哪个模板 | 必读哪个场景文件 |
|------------|-----------|----------------------|
| Landing Page / 个人主页 | `templates/landing-page.html` | **scene-landing.md** |
| 产品介绍页 / 工具介绍 | `assets/base.html` | **scene-product.md** |
| 演讲 Slides / PPT | `templates/slides.html` | **scene-slides.md** |
| 公众号封面图 | `templates/card.html` | cover-templates.md |
| 公众号文章排版 | `assets/base.html` | article-components.md |
| 小红书卡片系列 | `assets/base.html` | **scene-rednote.md** |
| 数据报告 / 工具横评 | `assets/base.html` | **scene-report.md** |

### Step 1 · 读模板和品牌基因

1. Read `assets/base.html` — CSS 变量、字体加载、工具类全在里面
2. Read `references/brand-dna.md` — 颜色系统、字体规则、禁用色
3. Read 对应场景的 template 文件

**不能省略这步。直接凭记忆写 = 颜色写错、字体漏加载。**

### Step 2 · Fork 模板，不从零写

- 以对应 `templates/*.html` 为起点
- 只修改：标题文字、段落内容、项目名称、链接地址
- **不允许**：改 CSS 变量名、改字体族、加没有在 brand-dna.md 里的颜色

### Step 3 · 执行禁忌检查（写完后必做）

```bash
# 检查禁用色
grep -nE "#000000|#ffffff|#FFFFFF|#6C63FF|#a855f7|#00FF88|#0066FF" index.html

# 检查字体是否加载
grep -c "fontsapi.zeoseven\|Smiley Sans" index.html  # 应 ≥ 1
grep -c "Space+Grotesk\|Space Grotesk" index.html    # 应 ≥ 1

# 检查有没有直接写裸 hex（不通过 var()）
grep -nE "color:\s*#[0-9A-Fa-f]" index.html | grep -v "var(" | head -10
```

### Step 4 · 对照 P0 清单自检

读 `references/checklist.md`，P0 全过才能交付。

### Step 5 · 交付

- 单文件 HTML，浏览器直接打开
- 在回复中说明：用了哪个模板、哪些地方做了定制、有没有用辅助色及原因

---

## 核心规则（10条，背下来）

1. **所有颜色用 CSS 变量**：`var(--amber)` 不是 `#C87A45`。直接写 hex = 违规
2. **标题只用得意黑**：`font-family: var(--font-display)`
3. **数字大字报用 Space Grotesk 200**：超细字重是辨识度的来源，不能改成 400
4. **眉头标签（eyebrow）全大写 + 极细 + 0.18em 字间距**：这是品牌识别点之一
5. **底色暖系**：浅底 `var(--warm)` / 深底 `var(--dark)`，绝不用 `#fff` 或 `#000`
6. **禁用蓝紫渐变、Glassmorphism、Neon 色**：出现即返工
7. **深浅区块必须交替**：连续两个深色区 = 节奏死，必须插入浅色区
8. **非对称布局优于对称**：作品卡片/内容区要有大小对比，不是等宽格
9. **字号要有极端反差**：标题大的时候副标题要极细极小，不能中庸
10. **发布后不加 emoji**：任何输出到外部的内容不带 emoji

---

## 快速色彩速查

```css
/* 最常用的那几个，背下来 */
--amber:       #C87A45   /* 橙，品牌主色 */
--dark:        #1A1816   /* 深底 */
--paper:       #FDFAF5   /* 纸白 */
--warm:        #F5F0E8   /* 暖米背景 */
--smoke:       #6B8590   /* 烟青，冷色辅助 */
--text-muted:  #9A9085   /* 元信息灰 */
--text-sub:    #6B6157   /* 副标题灰 */
```

---

## 字体加载代码（复制粘贴用）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
```

---

## 原始设计文件

Claude Design 原始 HTML 文件位于品牌资料目录中。
包含：品牌配色系统.html、字体方案v3.html、产品UI规范.html、封面模板.html 等。
需要参考设计细节直接读取这些文件。
