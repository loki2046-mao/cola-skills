# 卡片组件库 (Card Types)

每种卡片类型有其独立的 HTML 模板文件，通过 CSS 自定义属性（`var(--bg)`, `var(--text)`, `var(--accent)` 等）注入主题色。

---

## 7 种卡片类型

### 1. cover — 封面

**模板**: `assets/templates/cover.html`
**用途**: 小红书首图，决定点击率
**设计规则**:
- 大标题 80-120px，3-10 字，衬线体 700 字重
- 标题下方 3px 细线（强调色）
- 副标题 36px，次要色
- 锚点金句用 `.highlight`（左边框 + 大字号）
- 页脚只显示页码 `1 / N`
- **缩略图测试**: 缩到 100px 宽仍能看清标题

### 2. big-statement — 大字报

**模板**: `assets/templates/big-statement.html`
**用途**: 一句话冲击力，打破阅读节奏
**设计规则**:
- 文本居中，大面积留白
- 主句 64-72px，衬线体 700 字重
- 对比句可用强调色
- 下方 1-2 行小字说明（32px，次要色）
- 无页脚

### 3. pain-story — 痛点共鸣

**模板**: `assets/templates/pain-story.html`
**用途**: Carousel 第 2-3 张，建立情感连接
**设计规则**:
- 顶部运行标题（24px，`dim` 色，`letter-spacing: 0.08em`）
- H2 标题 44px，点出场景
- 正文 36px，`mid` 色，叙事口吻
- 使用 `.item` 结构组织并列场景：
  ```html
  <div class="item">
    <p class="label">场景标题</p>
    <p class="desc">场景描述</p>
  </div>
  ```
- 底部可加 `.note` 收束（32px）
- 页脚显示页码

### 4. feature-list — 干货列表

**模板**: `assets/templates/feature-list.html`
**用途**: 列出功能/步骤/要点，收藏区
**设计规则**:
- 顶部运行标题
- H2 标题引出列表
- 每项用 `.item` + 左边框（`.item` 默认 `rule` 色边框，可逐项改为 `accent` 色）
- `.label` 36px bold，`.desc` 28px `mid` 色
- 底部可加 `.note` 总结
- "不是画饼，是能照着做的那种" 式收尾
- 页脚显示页码

### 5. compare — 前后对比

**模板**: `assets/templates/compare.html`
**用途**: 展示改前 vs 改后、错误 vs 正确
**设计规则**:
- Flexbox 左右分屏，2px 竖线分隔
- **左侧**（错误/改前）:
  - 底色深一度（`#E0D8CC` 或色板 `dim` 加深）
  - 文字 `mid` 色，略小（30-34px）
  - 标签胶囊：浅色底 + 深色字 + `❌`
- **右侧**（正确/改后）:
  - 底色用色板 `bg`
  - 文字 `text` 色，略大（38-40px）
  - 标签胶囊：`accent` 底 + 白字 + `✅`
  - 核心数字放大：`big-num` 72-96px `accent` 色
- 无页脚

### 6. chat-dm — 对话气泡

**模板**: `assets/templates/chat-dm.html`
**用途**: 展示使用方式、操作步骤、对话范例
**设计规则**:
- 内容居中
- 顶部运行标题
- 中部气泡块（`highlight-bg` 底，圆角 12px，大 padding）
- 气泡内文字 34px，关键词用 `accent` 色
- 气泡下方 1-2 行提示文字（28-30px，`mid` 色）
- 可附加下载链接/仓库地址（24px，`dim` 色）
- 无页脚（或简化页脚）

### 7. ending — CTA 收尾

**模板**: `assets/templates/ending.html`
**用途**: 最后一张，情绪收束 + 行动号召
**设计规则**:
- 内容居中
- 情绪金句 52px，衬线体 700 字重
- 对比句可用 `accent` 色
- 下方引导文字 30px，`mid` 色
- 最底 CTA 文字 24px，`dim` 色
- 包含下载/关注/收藏引导
- 无页码

---

## 卡片使用决策

```
这张卡片要做什么？
├─ 吸引点击            → cover
├─ 一句话砸脸          → big-statement
├─ 让读者觉得"我也是"   → pain-story
├─ 列出干货要点         → feature-list
├─ 展示对比效果         → compare
├─ 演示怎么用           → chat-dm
└─ 收尾号召行动         → ending
```

## 典型 Carousel 结构

```
P1: cover          (勾住注意力)
P2: big-statement  (制造冲突感)
P3: pain-story     (建立共鸣)
P4: feature-list   (解决方案概述)
P5: feature-list   (具体功能/步骤)
P6: compare        (效果对比)
P7: chat-dm        (怎么用/怎么获取)
P8: ending         (情绪收束 + CTA)
```

可根据内容量缩减到 6 张或扩展到 9 张，但保持 P1→P2→P(n-1)→Pn 的结构不变。
