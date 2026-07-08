---
name: xhs-card-generator
description: >
  简单小红书图文卡片生成器，适合短选题、轻量内容、固定模板 carousel 快速出图。
  支持 5 种配色主题、7 种卡片组件、6-9 张自动排版、HTML 渲染 + 截图输出。
  Use for simple RedNote cards when the user wants quick template output. Do not use for 公众号长文、
  Markdown 长文、Skill 演示、证据截图型图文、复杂审美定制或需要标题/正文/tag 完整策划的任务；
  those should use xiaohongshu-card-designer.
author: kude
---

# 小红书图文卡片生成器 (XHS Card Generator)

将用户选题和内容转化为小红书风格的多页图文卡片（Carousel），HTML 渲染 + 无头浏览器截图 → 输出 PNG。

---

## 工作流程（7 步）

### 第一步：理解内容 & 确定类型

Read `references/content-guide.md`（原生文案指南）。

从用户输入中提取：
- **选题/主题**：这篇文章要讲什么？
- **目标受众**：给谁看的？（应届生/职场人/宝妈/学生/…）
- **核心情绪**：钩子是什么？（焦虑/好奇/共鸣/反常识/…）
- **关键信息**：核心观点、数据、案例、步骤

根据选题确定内容类型，参考 `references/palettes.md` 的决策树选择配色：

| 内容类型 | 配色 | 示例选题 |
|----------|------|----------|
| 知识/职场/深度 | editorial-warm | 简历技巧、面试攻略、行业分析 |
| AI/科技/编程 | tech-dark | AI 工具推荐、编程教程、产品评测 |
| 生活方式/美食 | lifestyle-warm | 旅行攻略、好物分享、家居 |
| 时尚/美妆/创意 | bold-creative | 穿搭、护肤、设计灵感 |
| 读书/情绪/治愈 | literary-calm | 书单、心理、情绪日记 |

---

### 第二步：研究平台（可选但推荐）

如果选题需要了解平台现状（如某个领域的爆款风格、竞品分析），使用 `web_search` 搜索：

```
小红书 [选题关键词] 爆款 图文 排版 2026
```

提取：封面风格、常用 Emoji、SEO 关键词、典型开篇句式。

---

### 第三步：规划卡片结构

Read `references/card-types.md`（卡片组件库）。

根据内容类型和核心情绪，规划 6-9 张卡片的序列。典型结构：

```
P1: cover          → 封面，情绪钩子，3-10 字大标题
P2: big-statement  → 一句话制造冲突感/反常识
P3: pain-story     → 痛点场景，建立「我也是」共鸣
P4: feature-list   → 解决方案/功能概述
P5: feature-list   → 具体步骤/详细要点
P6: compare        → 效果对比（可选，如果有 before/after）
P7: chat-dm        → 怎么用/怎么获取
P8: ending         → 情绪收束 + CTA（下载/关注/收藏）
```

少于 7 张时可合并：P3+P4 合并、P5+P6 合并。
多于 8 张时：扩展 feature-list 或增加 chat-dm 变体。

---

### 第四步：撰写原生文案

按照 `references/content-guide.md` 的口吻要求，逐张卡片撰写文案：

- **不要总结文章** — 用小红书的口吻重新讲
- 每张卡片只讲一件事
- 口语化：带情绪、允许不完整句式、用括号内心戏
- 封面标题 3-10 字，用 SEO 关键词
- 准备发布正文（标题 ≤ 20 字 + 正文 + 5-10 个 SEO 标签）

---

### 第五步：构建 HTML

Read `references/taste.md`（品味准则）— **生成任何 HTML 前必须读完**。

Read `references/palettes.md` — 确认选中的色板。

Read `references/typography.md` — 确认字体和字号层级。

为每一张卡片选择合适的模板文件（`assets/templates/` 目录下），将第四步的文案填入：

| 卡片 | 模板文件 |
|------|----------|
| cover | `assets/templates/cover.html` |
| big-statement | `assets/templates/big-statement.html` |
| pain-story | `assets/templates/pain-story.html` |
| feature-list | `assets/templates/feature-list.html` |
| compare | `assets/templates/compare.html` |
| chat-dm | `assets/templates/chat-dm.html` |
| ending | `assets/templates/ending.html` |

构建方法：
1. 读取模板文件
2. 将色板的 CSS 变量注入 `:root {}`
3. 将文案填入模板的 HTML 插槽
4. 将所有卡片拼接成一个 HTML 文件（每张卡用 `.page` 包裹，`page-break-after: always`）
5. 写入 `/tmp/xhs-cards-{name}.html`

**关键约束**：
- 一套卡片底色必须一致（所有 `.page` 使用同一 `var(--bg)`）
- 封面和 ending 不显示运行标题
- 续页卡（P2-Pn）显示运行标题（24px，`dim` 色）
- 页码格式：`{当前页} / {总页数}`

---

### 第六步：渲染截图

Read `scripts/render.sh` — 使用 Chrome headless 截图。

```bash
bash scripts/render.sh /tmp/xhs-cards-{name}.html {output_dir}
```

渲染过程：
1. Chrome headless 截图整页 → `full-page.png`
2. 像素级边界检测切割 → `card-01.png` ... `card-NN.png`

像素切割规则：扫描 x=4（接近左边缘，避开文字），R 通道 > 200 为卡片区域，≤ 200 为间距。

---

### 第七步：输出 & 交付

1. 报告输出目录和文件数量
2. 展示封面缩略图（如能读取）
3. 提供发布用文案：标题（≤ 20 字）+ 正文 + SEO 标签
4. 建议发布时间和场景

---

## 不可变约束

以下规则不可被用户偏好覆盖：

1. **3:4 (1080×1440px)** — 唯一比例，不允许其他
2. **6-9 张** — 卡片数量区间
3. **禁止纯黑** — 任何情况下不使用 `#000000`
4. **禁止 Inter 字体** — 任何情况下不加载 Inter
5. **禁止渐变背景** — 使用暖色固体底色
6. **每页一个观点** — 不在一张卡里塞多个主题
7. **尾页 CTA** — 最后一张必须有行动号召
8. **反 AI 元素** — 每套至少一个（手写/括号戏/不完美留白）
9. **正文 ≥ 36px** — 移动端可读底线
10. **缩略图测试** — 封面缩至 100px 宽仍能看清

---

## 快速示例

用户输入：
> 帮我把这个选题做成小红书图文：帮应届生用 AI 找求职方向

Agent 流程：
1. 确定类型：知识/职场 → editorial-warm 色板
2. 搜索小红书同类内容 → 了解爆款模式
3. 规划 8 张：cover → big-statement → pain-story → feature-list × 2 → compare → chat-dm → ending
4. 写原生文案（口语化，带情绪）
5. 构建 HTML（注入 editorial-warm 色板）
6. Chrome headless 截图 + 切割
7. 输出 8 张 PNG + 发布文案

---

## 参考文件索引

| 文件 | 用途 |
|------|------|
| `references/content-guide.md` | 原生小红书文案写作指南 |
| `references/palettes.md` | 5 组配色系统 + 选色决策树 |
| `references/typography.md` | 字体栈 + 字号层级 + 移动端规则 |
| `references/card-types.md` | 7 种卡片组件定义 + 使用决策 |
| `references/taste.md` | 设计品味准则 + 出厂自检清单 |
| `assets/templates/*.html` | HTML 模板文件 |
| `scripts/render.sh` | Chrome headless 渲染脚本 |
