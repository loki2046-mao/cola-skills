---
name: xiaohongshu-card-designer
description: >
  Creates content-aware Xiaohongshu/Rednote carousel posts from articles, scripts, product notes, Skill demos,
  case studies, tutorials, and opinion drafts. Use when the user asks to turn long-form content into 小红书图文,
  generate Rednote cards, create a carousel with title/body/tags, show evidence screenshots, adapt a 公众号文章
  or newsletter draft, convert a Markdown long article into 小红书, or design visually varied social cards for 小红书.
  Routes content through long-form compression, style modes, components, copy, HTML, PNG export, visual QA,
  and platform-ready title/caption/hashtags.
author: kude
---

# Xiaohongshu Card Designer

把文章、产品说明、Skill 演示、案例复盘、教程或观点素材，转成一套能发小红书的图文 PNG，并同时给出标题、正文和标签。

这个 Skill 的核心不是套模板，而是先判断内容类型，再选择视觉风格、组件组合和证据呈现方式。

## Output

默认交付：

- 6-9 张小红书 3:4 图文卡片，尺寸 `1080 x 1440`
- 一个 `index.html`
- 一个 `output/` 文件夹，含可直接发布的 PNG
- 发布标题、正文、置顶评论/安装说明、标签组合
- 视觉检查说明

## Workflow

### 1. Read Source And Determine Goal

读取用户提供的文章、Markdown、文案、截图、产品说明或本地文件。

提取：
- 目标读者
- 核心痛点
- 作者真实视角
- 能证明内容可信的证据
- 必须出现的产品、Skill、项目或截图
- 不适合放进图片、应该放正文/评论区的信息

如果用户只给长文，不要直接总结成卡片；先找出这篇内容真正的“传播刀口”。

如果来源是公众号长文、公众号定稿、Newsletter、长 Markdown 文章，先读取 `references/wechat-to-rednote.md`，把内容分成：
- 图片里要承担的 hook / proof / action
- 正文承载的背景、细节和使用说明
- 置顶评论承载的复制模板、安装说明或长链接
- 应该删掉的重复铺垫

必须先形成「Article knife / Audience / What images carry / What caption carries / Evidence pages / Page plan」内部规划，再进入风格选择。

### 2. Route Content

读取 `references/content-router.md`，判断内容类型和主辅风格。

必须输出一个内部规划：

```text
Content type:
Primary style:
Secondary style:
Evidence required:
Page plan:
```

若内容同时属于「公众号长文」和「Skill/工具演示」，优先按公众号压缩流程抽传播刀口，再按 Skill/工具演示补证据页。不要让安装教程抢掉封面。

### 3. Choose Style Modes

读取 `references/style-modes.md`。

从 10 个风格模式中选择 1 个主风格和最多 2 个辅风格。不要一套图只换颜色；风格要影响组件、排版、字体、证据呈现和节奏。

风格选择必须写清楚：
- 背景基调：明亮清透 / 深色工作台 / 证据白底 / 其他
- 禁用项：本次不能出现的颜色、组件和表达
- 统一项：整套共用的页眉、页脚、字体、边框、截图窗口语言

### 4. Select Components

读取 `references/component-library.md`。

为每一页选择组件，不要重复同一种“大标题 + 正文 + 卡片”的结构。每页只能承担一个传播任务：钩子、共鸣、证据、对比、流程、案例、安装、CTA。

组件不是只写名字。每页计划里要写：
- 主组件
- 证据/视觉锚点
- 该页不能承载的内容
- 该页如果信息太密要移到正文的内容

### 5. Write Native Rednote Copy

读取 `references/copy-rules.md`。

文案要像人写的，不像 AI 总结。优先保留用户原文里有个人判断、体感、真实经验的句子。把解释压缩到卡片，把细节放到正文。

### 6. Build HTML And Render PNG

读取 `references/render-workflow.md`。

使用 `assets/xhs-seed.html` 作为起点，生成任务文件夹：

```text
xhs-<slug>/
  index.html
  assets/
  output/
```

使用 `scripts/render.mjs` 渲染：

```bash
node ./scripts/render.mjs xhs-<slug>
```

如果当前 Node 环境找不到 Playwright，使用系统 Chrome 或 Codex 运行时依赖作为 fallback，具体见 `references/render-workflow.md`。

### 7. Inspect And Iterate

至少检查封面、证据页、文字最密页、安装/CTA 页和最后一页。

检查：
- 封面 100px 宽仍能看懂
- 是否真的展示了内容/产品/Skill 的能力
- 是否有证据截图或证据式组件
- 文字是否像小红书，而不是公众号摘要
- 配色是否丰富但不乱
- 每页是否一个重点
- 标题、正文、标签是否能直接发布
- 整套是否像一组图，而不是 9 个模板拼起来
- 背景是否明亮、有精神；如果出现旧纸、淡黄、土橙、低端复古感，必须重做底色
- 证据截图/模拟报告是否完整可读，不得截半句、截半张、糊成装饰

## Non-Negotiables

- 不生成纯文字 PPT 式图文
- 不用一个模板套完整篇文章
- 不把安装命令堆在图片里，除非用户明确要教程卡
- 不 fake 截图、数据、产品输出；证据式组件必须来自用户素材、真实输出或清楚标注为 mock
- 不让 AI 味的总结句占据封面
- 不使用纯黑、纯白、荧光色、高饱和渐变、廉价贴纸风、旧纸黄底、土橙大色块
- 小红书封面优先痛点/反常识/真实视角，工具名通常放副标题或第 3 页以后
- 公众号长文转小红书时，图片最多承载 7-9 个传播点；其他内容必须进入正文或置顶评论，不许把长文切成 9 张摘要
- 输出前必须给标题、正文、标签；只给 PNG 不算完成

## Reference Index

| File | Use |
|------|-----|
| `references/content-router.md` | 内容类型识别和风格路由 |
| `references/wechat-to-rednote.md` | 公众号长文/Markdown 长文转小红书的压缩流程 |
| `references/style-modes.md` | 10 种视觉风格和字体/色彩/适用场景 |
| `references/component-library.md` | 组件库，当前 108 个可组合组件 |
| `references/copy-rules.md` | 小红书文案、标题、正文、标签规则 |
| `references/render-workflow.md` | HTML 生成、Playwright/Chrome 渲染和 QA |
| `assets/xhs-seed.html` | 可复制的 HTML 种子模板 |
| `scripts/render.mjs` | PNG 渲染脚本 |
