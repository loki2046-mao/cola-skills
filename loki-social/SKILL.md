---
name: loki-social
description: 生成 Loki 个人风格的小红书/社交图文。支持4种模式：simple（快速模板）、brand（品牌风格+IP形象）、compress（公众号转小红书）、advanced（108组件高级定制）。当用户需要制作小红书图文、社交卡片、carousel时使用。
author: kude
---

# Loki Social · 赛博小熊猫个人风格社交图文 Skill

> 统一入口，4 种模式路由。把文章、选题、产品说明、教程或观点素材，转成一套能发小红书的图文 PNG。

---

## 4 种模式

| 模式 | 适用场景 | 模板 | 渲染脚本 | 配色 |
|------|---------|------|---------|------|
| **simple** | 轻量快速出图，短选题、固定模板 | `assets/templates/` 6 个 HTML | `scripts/render.sh` | `references/palettes.md`（5 组，simple 专用） |
| **brand** | Loki 品牌风格，IP 形象，三段式填充 | `templates/carousel-v2.html` | 手动 / Cola 截图 | `references/themes.md`（9 套，与 loki-deck 共用） |
| **compress** | 公众号长文 / Newsletter / 长 Markdown 转小红书 | 按内容路由选择 | `scripts/render.mjs` | 按风格模式选择 |
| **advanced** | 复杂内容高级定制，多组件组合 | `templates/xhs-seed.html` | `scripts/render.mjs` | `references/style-modes.md`（10 种风格） |

---

## 模式选择规则

**默认 brand 模式。** 根据用户意图切换：

| 用户信号 | 选择模式 |
|---------|---------|
| 说「快速」「简单」「轻量」 | simple |
| 说「品牌风格」「Loki 风格」 / 无特殊要求 | brand |
| 给了公众号文章 / Newsletter / 长 Markdown | compress |
| 说「复杂」「精细」「高级」「定制」 / 内容多维度 | advanced |

---

## simple 模式 — 轻量快速出图

适合短选题、轻量内容、固定模板 carousel 快速出片。

### 工作流（7 步）

1. **理解内容 & 确定类型** — 读 `references/content-guide.md`（原生文案指南）。从用户输入提取选题/受众/核心情绪/关键信息。根据内容类型，参考 `references/palettes.md` 的决策树选择配色。
2. **研究平台（可选）** — `web_search` 搜索小红书同类爆款，提取封面风格、SEO 关键词。
3. **规划卡片结构** — 读 `references/card-types.md`（7 种卡片组件）。规划 6-9 张卡片序列（封面→正文×N→结尾）。
4. **撰写原生文案** — 按 `references/content-guide.md` 口吻，逐张撰写。不要总结文章，用小红书口吻重新讲。
5. **构建 HTML** — 读 `references/taste.md`（品味准则，生成前必读）+ `references/typography.md`（字体规范）。为每张卡片选模板（`assets/templates/`），注入色板 CSS 变量 + 文案，拼接成单 HTML。
6. **渲染截图** — 读 `scripts/render.sh`，执行 `bash scripts/render.sh /tmp/xhs-cards-{name}.html {output_dir}`。Chrome headless 截图 + 像素级切割。
7. **输出 & 交付** — 报告输出目录、展示封面、提供发布文案（标题 ≤ 20 字 + 正文 + SEO 标签）。

### simple 模式不可变约束

- 3:4（1080×1440px），6-9 张，禁止纯黑，禁止 Inter，禁止渐变背景
- 每页一个观点，尾页 CTA，反 AI 元素 ≥ 1，正文 ≥ 36px

### simple 模式 references 索引

| 文件 | 用途 |
|------|------|
| `references/content-guide.md` | 原生小红书文案写作指南 |
| `references/palettes.md` | 5 组配色系统 + 选色决策树（simple 模式专用） |
| `references/typography.md` | 字体栈 + 字号层级 + 移动端规则 |
| `references/card-types.md` | 7 种卡片组件定义 + 使用决策 |
| `references/taste.md` | 设计品味准则 + 出厂自检清单 |

### simple 模式模板

| 卡片 | 模板文件 |
|------|----------|
| cover | `assets/templates/cover.html` |
| big-statement | `assets/templates/big-statement.html` |
| pain-story | `assets/templates/pain-story.html` |
| feature-list | `assets/templates/feature-list.html` |
| compare | `assets/templates/compare.html` |
| chat-dm | `assets/templates/chat-dm.html` |
| ending | `assets/templates/ending.html` |

---

## brand 模式 — Loki 品牌风格

Loki 品牌风格，三段式填充 + 装饰元素 + IP 形象视觉主体。

### 工作流（6 步）

1. **内容路由器（动手前必做）** — 先分析内容，不要直接动手。判断内容类型 → 选配色 → 选版式 → 选 IP 形象状态 → 规划版式序列（封面→正文×N→结尾）。

   | 内容类型 | 推荐配色 | 推荐版式 | IP形象 |
   |---------|---------|---------|--------|
   | 工具评测 | 墨黑信号 / 电光蓝黄 | 网格选择 + 图文混排 + 清单详情 | 兴奋+电脑 |
   | 知识分享 | 墨黑信号 / 灰蓝深度 | 要点列表 + 金句 + 数据大字 | 演示姿势 |
   | 生活分享 | 暖米咖啡 / 鼠尾草知识分子 | 封面 + 图文混排 + 结尾 | 酷+手机 |
   | 情感叙事 | 酒红夜幕 / 焦糖深蓝 | 金句 + 引用插入 + 杂志导读 | 思考 |
   | 教程步骤 | 墨黑信号 / 电光蓝黄 | 步骤 + 要点列表 + 清单详情 | 写作 |
   | 对比评测 | 摇滚墨水 / 墨黑信号 | 对比 + 网格选择 | 思考 |
   | 娱乐社交 | 糖果粉紫 / 梦幻紫调 | 网格选择 + 对比 + 步骤 | 庆祝 |

2. **规划版式序列** — 一篇通常 6-10 张。版式交替规则：不连续 2 张同类型、长文版式（X04/X05/X06）和精简版式（X02/X03）交替、深浅卡片交替。

3. **生成预览** — 给用户配色选择 + 版式序列 + IP 形象规划 + 预览 HTML。用户确认后才进入正式版。

4. **生成正式版** — 拷贝 `templates/carousel-v2.html`，从 `references/themes.md` 替换 CSS 变量，从 `references/layouts.md` 粘贴版式代码块，插入 IP 形象。

5. **截图切割** — 见 `references/screenshot-sop.md`。Chrome headless 全页截图 + 像素级边界检测切割。

6. **自检** — 读 `references/checklist.md`，逐项检查。

### brand 模式配色系统（9 套主题）

与 loki-deck 共用。完整色值见 `references/themes.md`。

| # | 主题 | 底色 | 主色 | 适合 |
|---|------|------|------|------|
| 01 | 墨黑信号 | #0A0A0A | #FF5E1A | 正式/科技/工具 |
| 02 | 暖米咖啡 | #F5EFE6 | #C44536 | 个人IP/生活 |
| 03 | 电光蓝黄 | #0A1A3A | #FFD60A | 科技/工具/干货 |
| 04 | 糖果粉紫 | #FFF0F5 | #FF3D7F | 娱乐/社交 |
| 05 | 深海青金 | #0F2027 | #E8A040 | 摄影/旅行/叙事 |
| 06 | 鼠尾草灰绿 | #E8EDE6 | #7A8B6F | 生活/家居/心理 |
| 07 | 焦糖深蓝 | #1A1420 | #D4885A | 深度/文化/影评 |
| 08 | 极简黑白 | #FAFAF8 | #0A0A0A | 专业/知识/设计 |
| 09 | 暖米咖啡+橙 | #F5EFE6 | #FF5E1A | 混合/通用 |

V2 模板支持 `.theme-xxx` 主题切换（在 `<body>` 或容器上加 class 即可切换配色，无需改 CSS 变量）。

### brand 模式版式系统（7 种）

| # | 版式 | 用途 |
|---|------|------|
| X01 | 封面·居中大字 | 吸引点击 |
| X02 | 要点列表·编号卡片 | 核心要点 |
| X03 | 金句·橙底大字 | 情绪锚点 |
| X04 | 杂志导读·双栏+总结框 | 深度长文 |
| X05 | 引用插入·长文+Pull Quote | 叙事+引用 |
| X06 | 卡片拼接·3横条 | 多点论述 |
| X07 | 结尾·CTA | 关注引导 |

完整 HTML 代码块见 `references/layouts.md`。排版填充法则见 `references/layout-fill-principles.md`。

### brand 模式 references 索引

| 文件 | 用途 |
|------|------|
| `references/themes.md` | 9 套配色主题完整色值（→ loki-deck 共用） |
| `references/layouts.md` | 7 种版式完整 HTML（V2） |
| `references/layout-fill-principles.md` | 排版填充法则（三段式+装饰填空+Horror Vacui） |
| `references/screenshot-sop.md` | 截图切割 SOP |
| `references/checklist.md` | 质量检查清单 |

---

## compress 模式 — 公众号长文转小红书

适合公众号文章 / Newsletter / 长 Markdown 转小红书图文。

### 工作流

1. **读取来源 & 确定目标** — 读取用户提供的长文。提取目标读者、核心痛点、作者真实视角、可信证据。不要直接总结成卡片，先找出「传播刀口」。
2. **读 `references/wechat-to-rednote.md`** — 把内容分成：图片承担 hook / proof / action，正文承载背景/细节/使用说明，置顶评论承载复制模板/安装说明/长链接，应删掉的重复铺垫。
3. **内容路由** — 读 `references/content-router.md`，判断内容类型和主辅风格。输出内部规划：Content type / Primary style / Secondary style / Evidence required / Page plan。
4. **选风格模式** — 读 `references/style-modes.md`，从 10 个风格模式中选 1 主 + 最多 2 辅。
5. **选组件** — 读 `references/component-library.md`，为每页选组件。每页只承担一个传播任务。
6. **写原生文案** — 读 `references/copy-rules.md`。文案要像人写的，优先保留原文里有个人判断、体感、真实经验的句子。
7. **构建 HTML & 渲染** — 读 `references/render-workflow.md`。以 `templates/xhs-seed.html` 为起点生成 `index.html`，用 `scripts/render.mjs` 渲染。
8. **检查 & 迭代** — 检查封面、证据页、文字最密页、CTA 页和末页。

### compress 模式不可变约束

- 图片最多承载 7-9 个传播点；其他内容必须进入正文或置顶评论
- 不把长文切成 9 张摘要
- 不 fake 截图、数据、产品输出
- 输出前必须给标题、正文、标签

### compress 模式 references 索引

| 文件 | 用途 |
|------|------|
| `references/wechat-to-rednote.md` | 公众号长文/Markdown 长文转小红书的压缩流程 |
| `references/content-router.md` | 内容类型识别和风格路由 |
| `references/style-modes.md` | 10 种视觉风格和字体/色彩/适用场景 |
| `references/component-library.md` | 组件库，当前 108 个可组合组件 |
| `references/copy-rules.md` | 小红书文案、标题、正文、标签规则 |
| `references/render-workflow.md` | HTML 生成、Playwright/Chrome 渲染和 QA |

---

## advanced 模式 — 108 组件高级定制

适合复杂内容、多维度信息、需要精细组件组合的高级定制。

### 工作流

与 compress 模式的工作流相同（步骤 1-8），区别在于：

- compress 模式侧重「长文压缩」，advanced 模式侧重「组件精细组合」
- 内容不限于长文，可以是产品说明、Skill 演示、案例复盘、教程、观点素材
- 更强调组件多样性和证据呈现方式

### advanced 模式核心 references

| 文件 | 用途 |
|------|------|
| `references/component-library.md` | 108 个可组合组件（核心） |
| `references/style-modes.md` | 10 种视觉风格模式 |
| `references/content-router.md` | 内容类型识别和风格路由 |
| `references/copy-rules.md` | 小红书文案、标题、正文、标签规则 |
| `references/render-workflow.md` | HTML 生成、Playwright/Chrome 渲染和 QA |

### advanced 模式模板 & 渲染

- 种子模板：`templates/xhs-seed.html`
- 渲染脚本：`node scripts/render.mjs xhs-<slug>`

---

## IP 形象组件库

与 loki-deck 共用。9 种状态的小熊猫形象。

**目录**：`templates/ip-library/`（→ `../../loki-deck/templates/ip-library` 共用）。使用相对路径 `ip-library/loki-original-3d.png` 引用。

| 状态 | 文件名 | 适合卡片 |
|------|--------|----------|
| 原始3D | `loki-original-3d.png` | 封面 |
| 演示 | `loki-presenting.png` | 知识分享 |
| 写作 | `loki-writing.png` | 教程 |
| 兴奋+电脑 | `loki-excited-laptop.png` | 工具评测 |
| 思考 | `loki-thinking.png` | 深度/对比 |
| 庆祝 | `loki-celebrating.png` | 结尾/成就 |
| 酷+手机 | `loki-cool-phone.png` | 日常/生活 |
| 困倦+咖啡 | `loki-sleepy-coffee.png` | 效率/加班 |
| 英雄展示 | `loki-hero-pose.png` | 品牌/展示/封面 |

---

## 共享规则

### 截图 SOP

所有模式截图切割流程统一参考 `references/screenshot-sop.md`：
1. Chrome headless 全页截图
2. 像素级边界检测（扫描每行像素找色块边界）
3. 按边界切割成单独卡片图片
4. 输出到 output/ 目录

### 配色统一

- **brand 模式**：用 `references/themes.md` 的 9 套配色（与 loki-deck 共用）
- **simple 模式**：用 `references/palettes.md` 的 5 组配色（simple 专用，不要与 themes.md 混用）
- **compress / advanced 模式**：用 `references/style-modes.md` 的 10 种风格模式中的配色

### 通用设计元素

与 loki-deck 共用：品牌标识 / 进度条 / 页码 / 噪点 / 光晕 / 色条 / 标签角标 / 霓虹点 / 引用线 / 关键词高亮。

### 字体方案

与 loki-deck 共用：Noto Sans SC 900 / Noto Serif SC 300 italic / Space Grotesk 700/200 / JetBrains Mono 500 / 得意黑(装饰)。标题字体规范以 loki-design-system/references/brand-dna.md 为唯一真相源。

---

## 核心设计原则

1. **反AI味**：文字要填满画面，不要缩在角落
2. **大文字量**：信息密度要够，分块化排版
3. **视觉重心居中**：不要习惯性排左上方
4. **版式交替**：不要全是同一种版式
5. **噪点必须覆盖**：打破AI光滑感
6. **IP形象有目的**：放IP是为了品牌识别，不是填空
7. **进度条给通关感**：10%→100%
8. **不用emoji**
9. **三段式垂直分配**（必读 `references/layout-fill-principles.md`）：顶部标题区25%→中部主视觉区50%→底部辅助区25%，每段都有内容，禁止下半部空白
10. **装饰元素填空**：任何空白区域用几何图形/纹理/色块/小图标填充，没有纯空白
11. **IP形象是视觉主体**：占画面30-50%，不是小角标
12. **色块满版分段**：用满版色块切割画面，色块本身填满空间
13. **Horror Vacui**：每个角落都有东西，靠网格组织不杂乱

---

## 传播刀口论

图片承担 hook / proof / action，正文承担细节：

- **封面**（hook）：吸引点击，大字+IP
- **正文**（proof）：信息密度，分块化
- **金句**（hook×2）：情绪锚点，适合转发
- **结尾**（action）：CTA引导

---

## 资源文件导览

```
loki-social/
├── SKILL.md                          ← 统一入口，4 种模式路由
├── templates/
│   ├── carousel-v2.html              ← brand 模式 V2 模板（三段式填充+装饰元素+IP视觉主体）★推荐
│   ├── carousel.html                 ← brand 模式 V1 模板（旧版式）
│   ├── xhs-seed.html                 ← advanced/compress 模式种子模板
│   └── ip-library/                   → loki-deck/templates/ip-library（共用）
├── references/
│   ├── themes.md                    → loki-deck/references/themes.md（9 套配色，brand 模式用）
│   ├── layouts.md                    ← 7 种版式完整 HTML（V2，brand 模式）
│   ├── layout-fill-principles.md     ← 排版填充法则（三段式+装饰填空+Horror Vacui）
│   ├── screenshot-sop.md             ← 截图切割 SOP（所有模式共用）
│   ├── checklist.md                  ← 质量检查清单（brand 模式）
│   ├── content-router.md             ← 内容类型识别和风格路由（compress/advanced 模式）
│   ├── style-modes.md                ← 10 种视觉风格和字体/色彩/适用场景（compress/advanced 模式）
│   ├── component-library.md          ← 108 个可组合组件（compress/advanced 模式）
│   ├── copy-rules.md                 ← 小红书文案、标题、正文、标签规则（compress/advanced 模式）
│   ├── wechat-to-rednote.md          ← 公众号长文/Markdown 长文转小红书（compress 模式）
│   ├── render-workflow.md            ← HTML 生成、渲染和 QA（compress/advanced 模式）
│   ├── content-guide.md              ← 原生小红书文案写作指南（simple 模式）
│   ├── card-types.md                 ← 7 种卡片组件定义（simple 模式）
│   ├── palettes.md                   ← 5 组配色系统（simple 模式专用）
│   ├── taste.md                      ← 设计品味准则 + 出厂自检（simple 模式）
│   └── typography.md                 ← 字体栈 + 字号层级（simple 模式）
├── scripts/
│   ├── render.sh                     ← Chrome headless 渲染脚本（simple 模式）
│   └── render.mjs                    ← Playwright/Chrome PNG 渲染脚本（compress/advanced 模式）
└── assets/
    └── templates/                    ← simple 模式 HTML 模板
        ├── cover.html
        ├── big-statement.html
        ├── pain-story.html
        ├── feature-list.html
        ├── compare.html
        ├── chat-dm.html
        └── ending.html
```

---

## 产物命名规范

- 卡片图文件：`loki-social-{模式}-{版式编号}-{主题名}-{日期}.png`
- 示例：`loki-social-brand-X01-caramel-20260705.png`、`loki-social-simple-cover-editorial-20260705.png`

---

## 迭代与优化

用户会不断发送新的参考素材（小红书截图/GitHub开源地址/别人的Skill），根据这些素材持续优化：

- 新版式 → 添加到 `references/layouts.md`
- 新配色 → 添加到 `references/themes.md`（brand 模式）或 `references/palettes.md`（simple 模式）
- 新 IP 状态 → 生成后添加到 `ip-library/`
- 新切割方法 → 更新 `references/screenshot-sop.md`
- 新组件 → 添加到 `references/component-library.md`
- 新风格模式 → 添加到 `references/style-modes.md`
