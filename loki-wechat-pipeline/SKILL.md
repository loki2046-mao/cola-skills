---
name: loki-wechat-pipeline
description: >
  公众号全链路工作台。从写作到发布一条龙：写作→封面→排版→编辑器→发布。
  当用户说"写文章""写公众号""排版""公众号排版""做封面""标题方案""飞书转公众号"
  "公众号编辑器""可视化编辑""全流程"时使用。覆盖 Loki 公众号风格写作、
  封面设计与标题方案、微信公众号排版、可视化块编辑器、飞书文档转公众号直发。
author: kude
---

# Loki 公众号全链路工作台

这是一个分层工作台，覆盖公众号从写作到发布的完整链路。每一层可独立调用，也可全链路运行。

**五层模块：**

1. **写作层** — 按 Loki 风格写/润色公众号文章
2. **封面层** — 标题方案 + 21:9 封面生图提示词
3. **排版层** — 公众号后台可粘贴的成品排版 HTML
4. **编辑器层** — 可视化块编辑器（端口 8790）
5. **发布层** — 飞书文档→公众号后台直发管线

---

## 路由判断

根据用户意图进入对应模块：

| 用户说的话 | 进入模块 | 读取/执行 |
|-----------|---------|----------|
| "写文章""写公众号""用我的风格写""润色" | 写作层 | 读 `references/writing/` |
| "做封面""标题方案""封面设计""21:9提示词" | 封面层 | 读 `references/cover/cover-design-rules.md` |
| "排版""公众号排版""微信排版""推文套版" | 排版层 | 读 `references/typesetting/` |
| "排版编辑器""可视化编辑""飞书转公众号排版" | 编辑器层 | 启动 web 编辑器（端口 8790） |
| "飞书转公众号""发布""直发""灌进后台" | 发布层 | 跑 `scripts/` 管线脚本 |
| "全流程" | 全链路 | 写作→封面→排版→发布 |

**优先级规则：** 如果用户同时提到多个模块（如"写完帮我排版"），按写作→封面→排版→发布顺序串联执行。如果用户只说一个环节，只执行那个环节。

---

## 模块一：写作层

按 Loki 公众号风格写/润色文章。这个模块是一份"证据包"，不是规则清单——47 篇精读积累，照着例子写比照着规则写更接近她本人。

### 核心原则

**清醒有人味，专业但不端着。** 像朋友聊天但有信息密度，有态度但不说教，承认自己的局限不装懂，关注"落地"和"普通人能用"。

### 必读文件

1. **`references/writing/loki-voice-examples.md`** — 语音范例 A–JJ（35 个）、核心写法原则、AI vs Loki 对照表、测试标准。这是写作层的核心依据，照着感觉写比照着规则写更接近她本人。
2. **`references/writing/article-type-patterns.md`** — 各类型文章的具体结构模板（测评/实验/效率/教育/开发记录/AI观察）
3. **`references/writing/representative-references.md`** — 精选参考原文片段
4. **`references/writing/draft-template-with-image-slots.md`** — 含图片槽位的起草模板

### 格式硬规则（无例外）

1. **禁用无序列表**（圆点 ·）：一律改有序列表
2. **禁用一切双引号**（中文"……"和英文"…"）：框词语用【】
3. **标点节奏**：句号密度过高会产生 AI 式机械切碎感——用～！？……来调节呼吸。一段话里句号不超过 2-3 个
4. **禁用破折号**（——）：用逗号、句号或【】重组
5. **书名号/产品名/短语**：全用【】
6. **禁用「不是……而是……」等一切「不是X，Y」句型**：前后句分开也算，最高优先级硬规则
7. **禁用「愣了一下」类 AI 情绪标注词**：换成触发行为
8. **生图提示词必须用中文**
9. Cola/栖迟在 Loki 文章里用女字旁的「她」

### AI 语气黑名单（一出现立刻删）

`不是……而是……` · `毫无疑问` · `值得我们深思` · `这正是……的原因所在` · `在这个时代`（开头）· `我们应该……` · `随着……的发展` · `与此同时` · `不仅如此` · `综上所述` · `总而言之` · `赋能` · `日新月异` · 连续三四字一句号的切碎节奏 · 每段结尾都有小结 · 三点结构的有序观点

### 图片规则

1. 所有图片尺寸：16:9
2. 所有图片规格：4K
3. 所有图片提示词：中文
4. 每张图要有可读的中文文字嵌在设计里
5. 全文图片保持统一视觉语言
6. Loki 代表色：赤铜 **#B8623C**

---

## 模块二：封面层

为「赛博小熊猫Loki」公众号生成封面标题方案和 21:9 生图提示词。

### 必读文件

**`references/cover/cover-design-rules.md`** — 封面设计系统完整规则，包含：选题分类判定（深底/浅底）、标题生成规则、封面构图系统、IP 互动模板、色彩硬约束、提示词输出模板、执行流程、质量自检清单。

### 快速入口

- "帮我做封面，文章是关于 xxx 的" → 全流程执行
- "只要标题方案" → 只执行 Step 1–3
- "只要提示词" → 用户提供标题，直接执行 Step 4–5

---

## 模块三：排版层

将文章内容和图片排成公众号后台可粘贴的成品 HTML。

### 核心原则

**内容保真铁律（最高优先级）：** 排版时不修改用户的文字内容和图片内容。排版只做视觉结构化（分段、加标题层级、加强调样式），不做文字编辑。

### 必读文件

1. **`references/typesetting/theme-index.md`** — 主题索引与配色体系（12 套配色单一来源）。选主题必读。
2. **`references/typesetting/components.md`** — 组件库（配色与组件分离，所有主题共用一份组件库）
3. **`references/typesetting/wechat-safe-layout-recipes.md`** — 补充参考（配色、深浅色兼容规则、SVG 排版原则、图片编排规则、包边规则、视频说明卡、文末关注引导图等）
4. **`references/typesetting/article-handoff-template.md`** — 交接模板
5. **`references/typesetting/wps-feishu-handoff-guide.md`** — WPS/飞书交接指南
6. **`references/typesetting/video-and-follow-rules.md`** — 视频处理与文末关注引导图规则
7. **`references/typesetting/demo-svg-article.svg`** — SVG 排版演示

### 工作流程要点

1. 判断文章类型和节奏
2. 判断实现模式：原生稳定 / SVG 交互 / 整篇 SVG-first
3. **选主题**：读 `references/typesetting/theme-index.md`，据文章题材推荐最契合的主题，让用户确认
4. **读组件库**：读 `references/typesetting/components.md`，后续生成完全依据组件库，HTML 一律从中取
5. 规划图片插入点
6. 按配方选组件组合 → 装配 HTML
7. **智能排版处理**（必须做）：章节自动编号、正文关键词逐段下划线、中文全角标点、签名区去重合并
8. 生成最终结果
9. 运行校验脚本（见下方校验步骤）

### `<span leaf="">` 包裹铁律（必须执行）

所有文字节点必须用 `<span leaf="">文字</span>` 包裹。这是公众号粘贴后样式不丢失的命门。

### 校验步骤（强制）

生成最终 HTML 后，**必须运行校验脚本**，ERROR 清零才交付：

```bash
python3 /Users/kude/.cola/skills/loki-wechat-pipeline/scripts/validate_gzh_html.py <生成的.html路径>
```

图片 base64 内嵌（复制粘贴兼容）：

```bash
python3 /Users/kude/.cola/skills/loki-wechat-pipeline/scripts/embed_images.py <HTML路径>
```

组件库源头检查：

```bash
python3 /Users/kude/.cola/skills/loki-wechat-pipeline/scripts/component_lint.py /Users/kude/.cola/skills/loki-wechat-pipeline/
```

### 文末关注引导图

默认固定尾图：`assets/signature.png`（相对于本 SKILL.md 所在目录）

---

## 模块四：编辑器层

可视化块编辑器，支持飞书文档一键转排版 + 块级编辑 + 6 种色系切换。**用户确认仍在使用 8790 端口的可视化编辑器。**

### 本地依赖

- Python 3.10+
- lark-cli（已配置飞书认证）

### 色系

6 种可选色系：赤铜橙（默认）、青石蓝、松绿、玫瑰红、琥珀黄、石墨灰

### 执行流程

1. **调用排版引擎：**

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/feishu_to_copy_page.py \
  --url "<飞书链接>" \
  --wechat \
  --theme "<色系名>" \
  --output-dir "<输出目录>"
```

2. **复制编辑器页面到输出目录：**

```bash
cp ~/.cola/skills/loki-wechat-pipeline/scripts/web/editor.html "<输出目录>/editor.html"
```

3. **启动本地服务并打开编辑器（端口 8790）：**

```bash
cd "<输出目录>"
python3 -m http.server 8790 &
open "http://localhost:8790/editor.html"
```

### 编辑器服务器

也可启动独立编辑器服务：

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/editor_server.py --port 8790
```

编辑器支持：从飞书公开文档直接导入、载入已有 article.json、手工编辑内容块、上下移动/复制/删除、右侧实时预览、一键保存导出 copy.html。

### 色系快速匹配

- "橙色""默认""赤铜" → 赤铜橙
- "蓝色""冷色""科技感" → 青石蓝
- "绿色""清新""自然" → 松绿
- "红色""粉色""温柔" → 玫瑰红
- "黄色""明亮""活力" → 琥珀黄
- "灰色""简约""商务" → 石墨灰

---

## 模块五：发布层

飞书文档→公众号后台直发管线。目标不是做预览稿，而是做微信公众号后台真的能吃进去的版本。

### 核心原则

1. 不走"自由 HTML 网页→微信富文本"旧路
2. 直接按"微信兼容子集"生成发布包
3. 先保证结构和可编辑性，再追装饰
4. 图片永远走后台原生上传

### 三步流程

**Step 1. 抽取飞书原文：**

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/extract_public_feishu_doc.py \
  --url "公开飞书文档链接"
```

**Step 2. 生成微信原生发布包：**

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/build_wechat_native_from_feishu.py \
  --input "/绝对路径/feishu-extracted.json"
```

**Step 3. 自动灌进公众号后台：**

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/publish_to_wechat.py \
  --manifest "/绝对路径/.wechat-publish-package-wechat-native/manifest.json" \
  --save-draft \
  --keep-open \
  --verbose
```

### 单命令入口

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/run_feishu_wechat_pipeline.py \
  --url "公开飞书文档链接" \
  --save-draft \
  --keep-open \
  --verbose
```

### WPS 笔记入口

```bash
python3 ~/.cola/skills/loki-wechat-pipeline/scripts/build_from_wps_note.py
```

### 输出验收标准

1. 微信后台里正文是可编辑的
2. 图片是后台原生图片，能点开
3. 标题、小节、引语、正文不会糊成一坨
4. 不出现全文大面积脏底和奇怪底纹

---

## 共享规则

### 配色统一

全链路配色统一以 `references/typesetting/theme-index.md` 的 12 套配色为准（单一来源）。封面层的赤铜品牌色 #B8623C 与排版层主题色系互不冲突，但写文章时提到的图片主色应与最终排版主题协调。

### span leaf 铁律

排版层和编辑器层生成的 HTML，所有文字节点必须用 `<span leaf="">` 包裹。这是公众号粘贴后样式不丢失的命门。

### 校验脚本必须跑

排版层交付前必须运行 `scripts/validate_gzh_html.py`，ERROR 清零。这是硬约束，不是建议。

### 内容保真

全链路中，排版层和发布层都不修改用户的文字内容和图片内容。文字编辑只在写作层完成。

---

## 目录结构

```
loki-wechat-pipeline/
├── SKILL.md                          ← 本文件，统一入口
├── references/
│   ├── writing/
│   │   ├── loki-voice-examples.md
│   │   ├── article-type-patterns.md
│   │   ├── representative-references.md
│   │   └── draft-template-with-image-slots.md
│   ├── typesetting/
│   │   ├── theme-index.md
│   │   ├── components.md
│   │   ├── wechat-safe-layout-recipes.md
│   │   ├── video-and-follow-rules.md
│   │   ├── article-handoff-template.md
│   │   ├── wps-feishu-handoff-guide.md
│   │   └── demo-svg-article.svg
│   └── cover/
│       └── cover-design-rules.md
├── scripts/
│   ├── validate_gzh_html.py          ← 排版校验
│   ├── embed_images.py              ← 图片 base64 内嵌
│   ├── component_lint.py            ← 组件库源头检查
│   ├── feishu_to_copy_page.py       ← 飞书→排版引擎
│   ├── editor_server.py             ← 可视化编辑器服务
│   ├── extract_public_feishu_doc.py ← 飞书原文抽取
│   ├── build_wechat_native_from_feishu.py
│   ├── build_wechat_native_package.py
│   ├── build_wechat_publish_package.py
│   ├── build_from_wps_note.py
│   ├── paste_copy_html.py
│   ├── publish_to_wechat.py
│   ├── run_feishu_wechat_pipeline.py
│   ├── README.md
│   └── web/
│       ├── editor.html
│       ├── editor.css
│       └── editor.js
└── assets/
    └── signature.png                ← 文末关注引导图
```

---

**版本：** 1.0
**创建时间：** 2026-07-10
**合并自：** writing-loki-wechat-articles · cover-design-system · typesetting-wechat-articles · wechat-layout-editor · publishing-feishu-wechat-articles · loki-writing-style（已删除，内容被 writing 层完全覆盖）
