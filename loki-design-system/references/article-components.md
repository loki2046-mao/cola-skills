# 文章排版组件 · article-components.md
> 12 个可复用组件，用于公众号文章 HTML。预览宽度 560px，模拟微信实际阅读宽度。
> 所有组件共用 brand-dna.md 的配色和字体，直接复制进排版编辑器用。

---

## 01 · 文章头部 ARTICLE HEADER

用于文章最顶部：标签 → 标题 → 元信息

```html
<div style="display: flex; gap: 8px; margin-bottom: 16px;">
  <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 3px 10px;
    background: rgba(200,122,69,0.1); color: #C87A45; border: 1px solid #C87A45;">AI 工具</span>
  <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 3px 10px;
    background: #EBE4D6; color: #3A342D;">实测</span>
</div>
<h1 style="font-family: 'Smiley Sans Oblique', sans-serif; font-size: 28px; line-height: 1.25; margin-bottom: 10px;">
  标题在这里
</h1>
<div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #9A9085;
  display: flex; gap: 8px; align-items: center; letter-spacing: 0.04em;">
  <span>2026.05.22</span>
  <span style="color: #DDD2BD;">·</span>
  <span>阅读 6 分钟</span>
  <span style="color: #DDD2BD;">·</span>
  <span style="color: #7A8458;">★★★★☆ 推荐</span>
</div>
```

规范：品牌色标签边框 `1px #C87A45`；标题 `Smiley Sans Oblique 28px`；元信息 `mono 10px #9A9085`

---

## 02 · 段标题 SECTION HEADING

文章内内容分段

```html
<div style="display: flex; align-items: center; gap: 10px;
  padding-bottom: 10px; border-bottom: 1px solid #EBE4D6; margin-bottom: 16px;">
  <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px;
    color: #C87A45; font-weight: 600;">#03</span>
  <span style="font-size: 18px; font-weight: 600;">段标题文字</span>
</div>
```

规范：序号 `mono 12px #C87A45`；标题 `sans 18px 600`；底线 `1px #EBE4D6`

---

## 03 · 引用框 QUOTE BLOCK

引用观点、重要信息、作者 take

```html
<div style="border-left: 2px solid #C87A45; padding: 12px 16px;
  background: rgba(200,122,69,0.06); margin-bottom: 16px;">
  <div style="font-size: 14px; line-height: 1.7; color: #3A342D;">
    引用内容在这里，可以用高亮：
    <span style="background: linear-gradient(transparent 65%, rgba(200,122,69,0.2) 65%);
      padding: 0 2px;">这是高亮的关键词</span>
  </div>
</div>
```

规范：左线 `2px #C87A45`；底色 `#C87A45 6% opacity`；高亮用下划线渐变

---

## 04 · Prompt 展示框 PROMPT BOX

展示可复制的 Prompt 或代码块

```html
<div style="border-left: 2px solid #C87A45; overflow: hidden; margin-bottom: 16px;">
  <div style="padding: 8px 14px; background: #F5F0E8;
    display: flex; justify-content: space-between; align-items: center;
    border-bottom: 1px solid #EBE4D6;">
    <span style="font-size: 13px; font-weight: 600;">Prompt 标题</span>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #9A9085;">Claude 3.5+ · v1.0</span>
  </div>
  <div style="background: #1A1816; color: #EBE4D6; padding: 14px 16px;
    font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 1.8;">
    <span style="color: #D9A87A;">&lt;role&gt;</span><br>
    Prompt 内容<br>
    <span style="color: #D9A87A;">&lt;/role&gt;</span>
  </div>
  <div style="padding: 6px 14px; background: #252220;
    display: flex; justify-content: space-between; align-items: center;">
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #6B6157;">by 赛博小熊猫 Loki</span>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #C87A45;">复制 Prompt →</span>
  </div>
</div>
```

规范：头部暖米底；代码区 `#1A1816` 暗底；XML标签用 `#D9A87A`；底部深暗 `#252220`

---

## 05 · 截图框 SCREENSHOT FRAME

展示测试结果截图，有 macOS 风格装饰头

```html
<div style="border: 1px solid #EBE4D6; overflow: hidden; margin-bottom: 16px;">
  <div style="display: flex; gap: 4px; padding: 6px 10px;
    border-bottom: 1px solid #EBE4D6; background: #F5F0E8; align-items: center;">
    <span style="width: 8px; height: 8px; border-radius: 50%; background: #D99882;"></span>
    <span style="width: 8px; height: 8px; border-radius: 50%; background: #D9A87A;"></span>
    <span style="width: 8px; height: 8px; border-radius: 50%; background: #A8B08A;"></span>
    <span style="font-family: 'JetBrains Mono', monospace; margin-left: auto;
      font-size: 9px; color: #9A9085;">2026.05.22 · Claude 3.5</span>
  </div>
  <!-- 图片放这里，或者占位符 -->
  <img src="截图路径.png" style="width: 100%; display: block;" />
  <div style="padding: 6px 10px; border-top: 1px solid #EBE4D6;
    font-size: 11px; color: #6B6157; display: flex; justify-content: space-between;">
    <span>图注文字</span>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #9A9085;">截图</span>
  </div>
</div>
```

---

## 06 · 评分卡 RATING CARD

工具横评、评分汇总

```html
<div style="border: 1px solid #EBE4D6; padding: 16px 20px;
  display: flex; justify-content: space-between; align-items: flex-start;
  background: #fff; margin-bottom: 8px;">
  <div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
      color: #C87A45; margin-bottom: 4px;">工具名称</div>
    <div style="font-size: 16px; font-weight: 700; margin-bottom: 4px;">Claude</div>
    <div style="font-size: 12px; color: #6B6157; line-height: 1.6;">核心优势简评</div>
  </div>
  <div style="text-align: right; flex-shrink: 0; margin-left: 16px;">
    <div style="color: #C87A45; font-size: 16px; margin-bottom: 4px;">★★★★☆</div>
    <div style="font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #9A9085;">4/5</div>
  </div>
</div>
```

---

## 07 · My Take 评论块

作者个人观点，绿色系区分

```html
<div style="border-left: 3px solid #7A8458; padding: 12px 14px;
  background: rgba(122,132,88,0.06); margin-bottom: 16px;">
  <div style="font-family: 'Space Grotesk', sans-serif; font-size: 9px;
    color: #7A8458; letter-spacing: 0.1em; margin-bottom: 4px;">MY TAKE</div>
  <div style="font-size: 14px; line-height: 1.7; color: #3A342D;">
    作者评论内容
  </div>
</div>
```

规范：左线 `3px #7A8458`（苔绿）；底色 6% opacity；标签 `Space Grotesk`

---

## 08 · 分割线 DIVIDER

```html
<!-- 简单分割 -->
<div style="height: 1px; background: #EBE4D6; margin: 32px 0;"></div>

<!-- 带文字分割 -->
<div style="display: flex; align-items: center; gap: 12px; margin: 32px 0;">
  <div style="flex: 1; height: 1px; background: #EBE4D6;"></div>
  <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
    color: #9A9085; letter-spacing: 0.1em;">§</span>
  <div style="flex: 1; height: 1px; background: #EBE4D6;"></div>
</div>
```

---

## 09 · 信息标注 INFO BADGE

行内标注，不打断阅读流

```html
<!-- 推荐 -->
<span style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
  padding: 2px 8px; background: rgba(200,122,69,0.1);
  color: #C87A45; border: 1px solid rgba(200,122,69,0.3);">推荐</span>

<!-- 注意 -->
<span style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
  padding: 2px 8px; background: #EBE4D6; color: #6B6157;">注意</span>
```

---

## 10 · 工具卡片 TOOL CARD

单个工具介绍、推荐工具列表

```html
<div style="border: 1px solid #EBE4D6; padding: 16px 20px;
  background: #FDFAF5; margin-bottom: 12px;">
  <div style="display: flex; justify-content: space-between;
    align-items: flex-start; margin-bottom: 8px;">
    <div>
      <div style="font-size: 16px; font-weight: 700; margin-bottom: 2px;">工具名</div>
      <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
        color: #C87A45;">官网链接</div>
    </div>
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px;
      padding: 3px 10px; background: #EBE4D6; color: #3A342D; flex-shrink: 0;">免费</span>
  </div>
  <div style="font-size: 13px; color: #3A342D; line-height: 1.7;">一句话描述这个工具能干什么</div>
</div>
```

---

## 11 · 步骤列表 STEP LIST

教程类文章的步骤展示

```html
<div style="margin-bottom: 16px;">
  <div style="display: flex; gap: 14px; align-items: flex-start; margin-bottom: 12px;">
    <span style="font-family: 'JetBrains Mono', monospace; font-size: 12px;
      color: #C87A45; font-weight: 600; flex-shrink: 0; margin-top: 2px;">01</span>
    <div>
      <div style="font-size: 15px; font-weight: 600; margin-bottom: 4px;">步骤标题</div>
      <div style="font-size: 13px; color: #6B6157; line-height: 1.6;">步骤说明</div>
    </div>
  </div>
</div>
```

---

## 12 · 结尾关注区 CTA FOOTER

文章末尾的品牌 + 关注引导

```html
<div style="border-top: 2px solid #EBE4D6; padding-top: 20px; margin-top: 32px;
  display: flex; align-items: center; gap: 14px;">
  <svg width="36" height="36" viewBox="0 0 32 32" fill="none">
    <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
      stroke="#C87A45" stroke-width="1.8" fill="none"/>
    <circle cx="8" cy="9" r="2.4" stroke="#C87A45" stroke-width="1.8" fill="none"/>
    <circle cx="24" cy="9" r="2.4" stroke="#C87A45" stroke-width="1.8" fill="none"/>
    <path d="M10 15Q12 17 13.5 15" stroke="#C87A45" stroke-width="1.8" stroke-linecap="round" fill="none"/>
    <path d="M22 15Q20 17 18.5 15" stroke="#C87A45" stroke-width="1.8" stroke-linecap="round" fill="none"/>
    <circle cx="16" cy="19" r="1.1" fill="#C87A45"/>
  </svg>
  <div>
    <div style="font-size: 14px; font-weight: 700; margin-bottom: 2px;">赛博小熊猫 Loki</div>
    <div style="font-size: 12px; color: #6B6157;">AI 工具测评 · 工作流分享 · 提示词开源</div>
  </div>
</div>
```
