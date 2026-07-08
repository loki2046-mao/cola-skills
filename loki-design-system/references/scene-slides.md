# 演讲 Slides 场景规范 · scene-slides.md
> 赛博小熊猫 Loki · 场景三：演讲 / 分享 / 课程讲义
> 最后更新：2026-05-27

---

## 场景定位

**触发情境：** 公开演讲、AI 工具分享会、课程讲义、meetup、线上直播分享  
**用户离开后的核心感受：** 「我记住了这几个核心信息」  
**技术形态：** 单文件横向翻页 HTML，1920×1080 固定画布，JS scale 适配；不是 PPT 软件  
**气质参照：** 赛博小熊猫 Loki 本人站台讲话——直接、有立场、不堆砌、每一页只说一件事

---

## 节奏系统（全局约束，所有页型共用）

### 明暗交替规则
- **连续同色上限：不超过 3 页**。第 4 页强制切换底色。
- 深底（`#1A1816`）页：封面 / 章节幕封 / 数据页 / 金句页 / 截图页 / 结尾页
- 浅底（`#F5F0E8` 暖米）页：要点列表页 / 对比页（亦可深底）

### 页型多样性规则（来自归藏结论②）
- **7 页以内至少使用 5 种不同页型**；连续 3 页相同结构 = 节奏死了
- 8 页以上必须有 ≥1 个封面/章节幕封系（深底冲击）+ ≥1 个内容系（浅底可读）+ ≥1 个数据/金句系（深底张力）

### 标准 8 页节奏模板
```
P1  封面页      → 深底，冲击
P2  章节幕封    → 深底，宣告
P3  要点列表    → 浅底，内容
P4  数据大字报  → 深底，张力
P5  要点列表    → 浅底，内容（第二章节）
P6  金句引用    → 深底，呼吸
P7  截图展示    → 深底，证据
P8  结尾页      → 最深底，收束
```

### 字号双约束（来自归藏 + Zara 结论）
大字号一律使用 `min(Xvw, Yrem)` 双约束，防止宽屏溢出：

| 用途 | 推荐值 | 示例 |
|------|--------|------|
| 封面标题 | `min(9vw, 11rem)` | 封面极大标题 |
| 章节幕封标题 | `min(7vw, 8.5rem)` | Act 宣言 |
| 数据大数字 | `min(18vw, 22rem)` | 统计大字报 |
| 金句正文 | `min(4.5vw, 5.5rem)` | blockquote |
| 要点标题（左侧） | `min(4vw, 5rem)` | 要点页左栏 |
| 结尾 CTA | `min(3.5vw, 4.5rem)` | 结尾页大字 |

**字重反比规则（来自归藏结论③）：** 越大越细。数字用 `weight 200`，封面标题用得意黑自身，副标题 `weight 100`。

### 进场动画（来自 Zara 结论③）
- Spring 曲线：`cubic-bezier(0.16, 1, 0.3, 1)`（一切进场动效统一用这条）
- Stagger reveals：`.reveal:nth-child(n)` 延迟 `n × 0.08s`，最多延至 `0.4s`
- 每页进场是「一次精心编排」，幻灯片内无持续循环动效
- 降级保底：`prefers-reduced-motion` 下所有 `data-anim` 元素强制 `opacity:1`
- 页面切换用 `visibility + opacity + pointer-events`，禁用 `display:none`

---

## 装饰命名体系（来自不二结论②）

> 给每个装饰目的化命名，AI 按「我要达到什么视觉意图」选择，不是随机堆叠。

| 命名 | 用途 | 典型出现位置 |
|------|------|------------|
| `keyword-highlight` | 标题中 1-2 个词变琥珀橙，其余保持主文字色 | 所有页型的标题层 |
| `chapter-num` | 章节序号，`JetBrains Mono`，极小极细，左上或左下 | 章节幕封、封面 |
| `stat-unit` | 数字右上角单位/缩写（K / M / %），字号约数字的 1/4 | 数据大字报页 |
| `float-tag` | 无底色细边框 pill，标注来源/场景/时间 | 封面、截图页底部 |
| `quote-line` | 左侧 3px 琥珀橙竖线，金句的唯一装饰 | 金句引用页 |

**使用原则：** 一页最多同时出现 3 种装饰；`keyword-highlight` 在标题中不超过 2 处；霓虹青 `#00D9FF` 是 P0 点睛色，一屏最多一次。

---

## 字体加载（所有页型共用）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<!-- 得意黑 -->
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
```

---

## CSS 变量基础（所有页型共用）

```css
:root {
  /* 底色 */
  --dark:       #1A1816;
  --darker:     #111009;
  --paper:      #FDFAF5;
  --warm:       #F5F0E8;
  --oat:        #EBE4D6;

  /* 品牌色 */
  --amber:      #C87A45;
  --amber-light:#D9A87A;
  --amber-deep: #A05E30;
  --cyan:       #00D9FF;   /* P0 点睛，一屏最多一次 */
  --moss:       #7A8458;

  /* 文字 */
  --text-light: #FDFAF5;   /* 深底主文字 */
  --text-dark:  #1F1D1A;   /* 浅底主文字 */
  --text-sub:   #6B6157;   /* 副标题 */
  --text-muted: #9A9085;   /* 元信息 */
  --text-ghost: #C4BBB0;   /* 极淡说明 */

  /* 字体 */
  --font-title: "Smiley Sans Oblique", "得意黑", sans-serif;
  --font-eng:   "Space Grotesk", sans-serif;
  --font-body:  "Noto Sans SC", sans-serif;
  --font-mono:  "JetBrains Mono", monospace;

  /* 动效 */
  --spring:     cubic-bezier(0.16, 1, 0.3, 1);
}
```

---

## 舞台架构（Stage Model，所有页型共用）

```html
<!-- 幻灯片舞台：JS 统一 scale，不 reflow -->
<div class="deck-viewport">
  <div class="deck-stage" id="stage">
    <!-- 各 .slide 页型放在这里 -->
  </div>
</div>

<style>
.deck-viewport {
  position: fixed; inset: 0;
  display: flex; align-items: center; justify-content: center;
  background: #111009;
  overflow: hidden;
}
.deck-stage {
  width: 1920px; height: 1080px;
  position: relative;
  transform-origin: center center;
}
.slide {
  position: absolute; inset: 0;
  visibility: hidden; opacity: 0;
  pointer-events: none;
  transition: opacity 0.5s var(--spring);
}
.slide.active {
  visibility: visible; opacity: 1;
  pointer-events: auto;
}
/* 进场统一结构 */
.reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.65s var(--spring), transform 0.65s var(--spring);
}
.slide.active .reveal { opacity: 1; transform: translateY(0); }
.reveal:nth-child(1) { transition-delay: 0.05s; }
.reveal:nth-child(2) { transition-delay: 0.13s; }
.reveal:nth-child(3) { transition-delay: 0.21s; }
.reveal:nth-child(4) { transition-delay: 0.29s; }
.reveal:nth-child(5) { transition-delay: 0.37s; }
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1 !important; transform: none !important; }
}
</style>

<script>
// Scale 适配
function scaleStage() {
  const s = document.getElementById('stage');
  const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
  s.style.transform = `scale(${scale})`;
}
window.addEventListener('resize', scaleStage);
scaleStage();

// 键盘翻页
const slides = document.querySelectorAll('.slide');
let cur = 0;
function go(n) {
  slides[cur].classList.remove('active');
  cur = Math.max(0, Math.min(n, slides.length - 1));
  slides[cur].classList.add('active');
}
go(0);
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') go(cur + 1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')                    go(cur - 1);
});
</script>
```

---

---

## 页型一：封面页 Cover

**用途：** 整个演讲/分享的第一页，奠定气质，让观众在 3 秒内抓住「这场分享是关于什么的」。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 演讲主题（1 句话） | 极大得意黑标题，1-2 个词 `keyword-highlight` |
| 副标题/场合说明 | `Noto Sans SC weight 100`，极细，紧跟标题下方 |
| 演讲者信息 | `JetBrains Mono` 元信息行，底部左对齐 |
| 场合/日期 | `float-tag`，无底色细边框 pill，底部右角 |
| `chapter-num` 期号 | 左上角 `JetBrains Mono`，极小 |

**记忆点：** 标题字号极大但字重极细（得意黑自带斜体张力），副标题极细形成字号/字重双反差。

### 本页文字基调（来自不二结论⑤）
标题要有态度——不是「分享主题」，是「一个立场」。副标题信息量低、字号极小，克制到几乎隐形。演讲者名字是事实不是自我推销。

### 完整 HTML 代码

```html
<section class="slide slide-cover" data-type="cover">
  <!-- 左上期号 -->
  <span class="chapter-num">VOL.01 · 2026</span>

  <!-- 中央内容区 -->
  <div class="cover-body">
    <!-- eyebrow -->
    <p class="eyebrow">CYBER PANDA · AI CREATOR · BEIJING</p>

    <!-- 主标题 -->
    <h1 class="cover-title">
      用 AI 做<span class="keyword-highlight">真正</span>有用的事
    </h1>

    <!-- 副标题 -->
    <p class="cover-sub">纯文科生的 AI 工具箱——2026 年实测整理</p>
  </div>

  <!-- 底部信息行 -->
  <footer class="cover-footer">
    <span class="speaker-info">赛博小熊猫 Loki · hiloki.ai</span>
    <span class="float-tag">AI TOOLS MEETUP · 2026.05</span>
  </footer>
</section>

<style>
.slide-cover {
  background: var(--dark);
  display: flex;
  flex-direction: column;
  padding: 72px 96px;
  box-sizing: border-box;
  overflow: hidden;
}

/* 左上期号 */
.chapter-num {
  font-family: var(--font-mono);
  font-size: 13px;
  letter-spacing: 0.22em;
  color: var(--text-muted);
  text-transform: uppercase;
}

/* 中央内容 */
.cover-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 32px;
}

/* Eyebrow */
.eyebrow {
  font-family: var(--font-eng);
  font-size: 13px;
  font-weight: 300;
  letter-spacing: 0.22em;
  color: var(--text-ghost);
  text-transform: uppercase;
  margin: 0;
}

/* 封面主标题 */
.cover-title {
  font-family: var(--font-title);
  font-size: min(9vw, 11rem);
  line-height: 1.0;
  color: var(--text-light);
  margin: 0;
  letter-spacing: -0.01em;
}
.keyword-highlight { color: var(--amber); }

/* 副标题 */
.cover-sub {
  font-family: var(--font-body);
  font-size: 22px;
  font-weight: 100;
  color: var(--text-sub);
  margin: 0;
  letter-spacing: 0.04em;
}

/* 底部信息行 */
.cover-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}
.speaker-info {
  font-family: var(--font-mono);
  font-size: 15px;
  color: var(--text-muted);
  letter-spacing: 0.1em;
}

/* float-tag：无底色细边框 pill */
.float-tag {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.18em;
  color: var(--text-ghost);
  border: 1px solid rgba(255,255,255,0.15);
  padding: 6px 16px;
  text-transform: uppercase;
}

/* reveal 入场 */
.slide-cover .eyebrow  { transition-delay: 0.05s; }
.slide-cover .cover-title { transition-delay: 0.15s; }
.slide-cover .cover-sub   { transition-delay: 0.28s; }
.slide-cover .cover-footer { transition-delay: 0.38s; }
</style>
```

### ❌ 禁忌
- 禁止居中对称布局（封面只能左对齐或左偏对齐，居中显得像 PPT 模板）
- 禁止标题把「所有词」都橙色高亮——只允许 1-2 个词，其余保持 `--text-light`
- 禁止堆砌 logo / 头像 / 二维码（封面只有一个视觉主角：标题）
- 禁止副标题字号超过 28px（字号反差是记忆点，副标题极细是对比的前提）
- 禁止 `font-weight: 700` 的加粗标题（得意黑本身有斜体张力，加粗反而笨拙）

---

## 页型二：章节幕封 Chapter

**用途：** 演讲节奏分隔符，插在每个主题切换处，让观众重新聚焦。类似电影幕间字卡。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 章节序号 | `chapter-num`，Space Grotesk 极大，背景装饰级别 |
| 章节名 | 得意黑，`min(7vw, 8.5rem)`，中段主角 |
| 一句引语（可选） | `Noto Sans SC weight 100`，12-16px，极淡 |

**记忆点：** 序号字号极大（4x 正文）但透明度极低（0.07），作为纯视觉装饰——章节名是主角，序号是背景纹理。

### 本页文字基调
章节名是宣言而非目录标题。「第三部分：如何选工具」不如「选工具的真相」。一句话，有立场。

### 完整 HTML 代码

```html
<section class="slide slide-chapter" data-type="chapter">
  <!-- 装饰性大序号（背景层）-->
  <span class="chapter-bg-num" aria-hidden="true">03</span>

  <!-- 中央内容 -->
  <div class="chapter-body">
    <p class="chapter-label reveal">CHAPTER THREE</p>
    <h2 class="chapter-title reveal">选工具的<span class="keyword-highlight">真相</span></h2>
    <p class="chapter-tagline reveal">不是功能最多的，是你真正会用的那个</p>
  </div>
</section>

<style>
.slide-chapter {
  background: var(--dark);
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0 120px;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
}

/* 装饰性大序号（背景层）*/
.chapter-bg-num {
  position: absolute;
  right: -40px;
  top: 50%;
  transform: translateY(-50%);
  font-family: var(--font-eng);
  font-size: min(38vw, 48rem);
  font-weight: 200;
  color: rgba(253, 250, 245, 0.05);
  line-height: 1;
  letter-spacing: -0.05em;
  user-select: none;
  pointer-events: none;
}

/* 中央内容 */
.chapter-body {
  display: flex;
  flex-direction: column;
  gap: 28px;
  max-width: 900px;
}

/* 章节小标签 */
.chapter-label {
  font-family: var(--font-mono);
  font-size: 13px;
  letter-spacing: 0.24em;
  color: var(--amber);
  text-transform: uppercase;
  margin: 0;
}

/* 章节标题 */
.chapter-title {
  font-family: var(--font-title);
  font-size: min(7vw, 8.5rem);
  line-height: 1.0;
  color: var(--text-light);
  margin: 0;
  letter-spacing: -0.01em;
}

/* 一行引语 */
.chapter-tagline {
  font-family: var(--font-body);
  font-size: 20px;
  font-weight: 100;
  color: var(--text-sub);
  margin: 0;
  letter-spacing: 0.04em;
}
</style>
```

### ❌ 禁忌
- 禁止章节幕封放内容（它是「呼吸页」，信息量为零）
- 禁止序号装饰色用纯白或琥珀橙（opacity 0.05 的透明白才是对的，有颜色就太抢戏）
- 禁止标题超过 2 行（超了就是内容页，不是幕封）
- 禁止跳过章节幕封直接切内容（7 页以上必须有至少一个章节幕封）

---

## 页型三：要点列表页 Points

**用途：** 一个主题下的核心要点，最多 5 条。浅底，供观众阅读和拍照记录。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 2-5 条并列要点 | 右侧要点列表，每条独立行 |
| 区块主题名 | 左侧极大得意黑标题（竖向占满） |
| 每条要点的补充说明 | 要点正文下方极细小字，`weight 100` |
| 顶部 Eyebrow | `Space Grotesk` 全大写，`letter-spacing: 0.22em` |

**记忆点：** 左侧标题极大（占左 40% 宽度），右侧 5 条要点极细，字号/字重双重反差。浅底让文字绝对可读。

### 本页文字基调
要点要短——每条 8-15 字，是「结论」不是「过程描述」。补充说明可以稍长，但字号极小（这一行是给认真的人的，不是给所有人的）。

### 完整 HTML 代码

```html
<section class="slide slide-points" data-type="points">
  <div class="points-layout">
    <!-- 左侧大标题 -->
    <div class="points-left reveal">
      <p class="eyebrow-warm">CORE POINTS</p>
      <h2 class="points-title">选工具<br>的逻辑</h2>
    </div>

    <!-- 右侧要点列表 -->
    <ol class="points-list">
      <li class="point-item reveal">
        <span class="point-num">01</span>
        <div class="point-content">
          <p class="point-main">先问「我会用多久」</p>
          <p class="point-sub">学习成本超过 2 小时的工具，先做 POC 再决定</p>
        </div>
      </li>
      <li class="point-item reveal">
        <span class="point-num">02</span>
        <div class="point-content">
          <p class="point-main">免费版够用就别付费</p>
          <p class="point-sub">大部分场景 free tier 已经满足，付费是为了效率而非功能</p>
        </div>
      </li>
      <li class="point-item reveal">
        <span class="point-num">03</span>
        <div class="point-content">
          <p class="point-main">看输出质量，不看参数表</p>
          <p class="point-sub">自己动手测一遍，胜过看一百篇对比文章</p>
        </div>
      </li>
      <li class="point-item reveal">
        <span class="point-num">04</span>
        <div class="point-content">
          <p class="point-main">组合比单品更重要</p>
          <p class="point-sub">没有一个工具能做所有事，找到你的工作流组合</p>
        </div>
      </li>
      <li class="point-item reveal">
        <span class="point-num">05</span>
        <div class="point-content">
          <p class="point-main"><span class="keyword-highlight-dark">放弃</span>是一种能力</p>
          <p class="point-sub">工具不适合就换，沉没成本不是理由</p>
        </div>
      </li>
    </ol>
  </div>
</section>

<style>
.slide-points {
  background: var(--warm);
  padding: 72px 96px;
  box-sizing: border-box;
}

/* 双栏布局 */
.points-layout {
  display: grid;
  grid-template-columns: 0.95fr 1.4fr;
  gap: 0 80px;
  height: 100%;
  align-items: center;
}

/* 左栏 */
.points-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}
.eyebrow-warm {
  font-family: var(--font-eng);
  font-size: 12px;
  font-weight: 300;
  letter-spacing: 0.24em;
  color: var(--amber);
  text-transform: uppercase;
  margin: 0;
}
.points-title {
  font-family: var(--font-title);
  font-size: min(4vw, 5rem);
  line-height: 1.08;
  color: var(--text-dark);
  margin: 0;
  letter-spacing: -0.01em;
}

/* 右栏：要点列表 */
.points-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.point-item {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  padding: 22px 0;
  border-bottom: 1px solid var(--oat);
}
.point-item:first-child { border-top: 1px solid var(--oat); }

/* 序号 */
.point-num {
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 400;
  color: var(--amber);
  letter-spacing: 0.08em;
  padding-top: 3px;
  flex-shrink: 0;
  width: 28px;
}

/* 要点内容 */
.point-content { display: flex; flex-direction: column; gap: 6px; }
.point-main {
  font-family: var(--font-body);
  font-size: 22px;
  font-weight: 400;
  color: var(--text-dark);
  margin: 0;
  line-height: 1.35;
}
.point-sub {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 100;
  color: var(--text-sub);
  margin: 0;
  line-height: 1.65;
}

/* 浅底版 keyword-highlight */
.keyword-highlight-dark { color: var(--amber-deep); }
</style>
```

### ❌ 禁忌
- 禁止超过 5 条要点（超了拆成两页，一页只说一件事）
- 禁止要点用长句段落（超过 20 字的「要点」不是要点，是内容，换截图页）
- 禁止浅底上用霓虹青 `#00D9FF`（视觉冲突，霓虹青只在深底）
- 禁止去掉分割线 `border-bottom`（细线是「每条独立」的视觉锚，没了列表变成散点）
- 禁止左侧标题和右侧要点字号接近（字号反差是这个页型存在的理由）

---

## 页型四：数据大字报页 Stat

**用途：** 抛出一个有冲击力的数字/事实，让观众停下来思考。深底，数字是绝对主角。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 单一核心数据 | `Space Grotesk weight 200`，`min(18vw, 22rem)` |
| 数据单位/缩写 | `stat-unit`，数字右上角，字号约 1/4 |
| 数据解读（1 句话） | 数字下方，`Noto Sans SC weight 100`，20-22px |
| 数据来源/背景 | 最底部，`JetBrains Mono`，12px，极淡 |

**记忆点：** 数字本身就是视觉元素。整页就一个数字 + 一句解读，没有任何多余信息。

### 本页文字基调
数字解读用「所以」逻辑，而不是「这说明了什么」——直接给结论。「有 73% 的工具在 30 天后被弃用——挑工具的成本，其实在使用之后。」

### 完整 HTML 代码

```html
<section class="slide slide-stat" data-type="stat">
  <!-- eyebrow -->
  <p class="stat-eyebrow reveal">DATA · 实测数据</p>

  <!-- 核心数字 -->
  <div class="stat-center reveal">
    <div class="stat-nb-wrap">
      <span class="stat-nb">73</span>
      <span class="stat-unit">%</span>
    </div>
    <p class="stat-read">AI 工具在被下载后 30 天内<span class="keyword-highlight">彻底弃用</span></p>
  </div>

  <!-- 数据来源 -->
  <p class="stat-source reveal">Source: Loki 个人工具库实测 · 2024-2026 · N=87</p>
</section>

<style>
.slide-stat {
  background: var(--dark);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 72px 120px;
  box-sizing: border-box;
  gap: 48px;
}

/* eyebrow */
.stat-eyebrow {
  font-family: var(--font-mono);
  font-size: 13px;
  letter-spacing: 0.24em;
  color: var(--amber);
  text-transform: uppercase;
  margin: 0;
}

/* 核心数字区 */
.stat-center {
  display: flex;
  flex-direction: column;
  gap: 36px;
}
.stat-nb-wrap {
  display: flex;
  align-items: flex-start;
  line-height: 0.85;
}

/* 大数字：越大越细 */
.stat-nb {
  font-family: var(--font-eng);
  font-size: min(18vw, 22rem);
  font-weight: 200;
  color: var(--text-light);
  letter-spacing: -0.04em;
  line-height: 0.85;
}

/* 单位：stat-unit */
.stat-unit {
  font-family: var(--font-eng);
  font-size: min(4.5vw, 5.5rem);
  font-weight: 200;
  color: var(--amber);
  letter-spacing: -0.02em;
  margin-top: 0.18em;
  margin-left: 0.1em;
}

/* 解读文字 */
.stat-read {
  font-family: var(--font-body);
  font-size: 26px;
  font-weight: 300;
  color: var(--text-sub);
  margin: 0;
  max-width: 760px;
  line-height: 1.55;
}
.stat-read .keyword-highlight { color: var(--amber); }

/* 来源 */
.stat-source {
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-ghost);
  margin: 0;
  letter-spacing: 0.08em;
  position: absolute;
  bottom: 60px;
  left: 120px;
}
</style>
```

### ❌ 禁忌
- 禁止一页放两个大数字（选最有冲击力的那个，另一个放下一页或删掉）
- 禁止数字加粗（`weight 200` 越细越有张力，加粗反而失去了记忆点）
- 禁止解读文字超过两行（超了就是内容页，不是数据页）
- 禁止没有来源就放数据（哪怕是「个人实测」也要标注）
- 禁止使用科技蓝/紫色渐变给数字增加「科技感」（数字颜色只有 `--text-light` 和 `--amber`）

---

## 页型五：金句引用页 Quote

**用途：** 演讲中的情绪呼吸点，放核心观点或来自他人的有力引述。深底，左橙竖线是唯一装饰。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 核心观点/金句（1 句） | `Space Grotesk` 或 `Noto Sans SC`，`min(4.5vw, 5.5rem)` |
| 署名/出处 | `JetBrains Mono`，14px，极淡，`weight 400` |
| 引号装饰（可选） | 超大透明引号，`opacity: 0.06`，背景装饰层 |

**记忆点：** 左侧 3px 琥珀橙竖线（`quote-line`），来自杂志引用的排版语言。整页极简，只有竖线、大字、署名，大量留白是主角。

### 本页文字基调
金句要是「一个判断」，不是「一个描述」。「AI 工具会让纯文科生失业」不如「纯文科生的核心能力是提问，AI 正在帮我们让提问变得有力」。

### 完整 HTML 代码

```html
<section class="slide slide-quote" data-type="quote">
  <!-- 背景装饰引号 -->
  <span class="quote-bg" aria-hidden="true">"</span>

  <!-- 引用主体 -->
  <div class="quote-body">
    <!-- quote-line：左侧琥珀橙竖线 -->
    <div class="quote-line-wrap reveal">
      <div class="quote-line"></div>
      <div class="quote-text-wrap">
        <blockquote class="quote-text">
          纯文科生的核心能力是<span class="keyword-highlight">提问</span>，<br>
          AI 正在帮我们让提问变得有力。
        </blockquote>
        <cite class="quote-cite">— 赛博小熊猫 Loki · hiloki.ai · 2026</cite>
      </div>
    </div>
  </div>
</section>

<style>
.slide-quote {
  background: var(--dark);
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 72px 120px;
  box-sizing: border-box;
  overflow: hidden;
  position: relative;
}

/* 背景装饰引号 */
.quote-bg {
  position: absolute;
  right: 80px;
  top: -60px;
  font-family: var(--font-eng);
  font-size: min(50vw, 62rem);
  font-weight: 200;
  color: rgba(253, 250, 245, 0.04);
  line-height: 1;
  user-select: none;
  pointer-events: none;
}

/* 引用主体 */
.quote-body {
  max-width: 1300px;
}

/* quote-line 容器 */
.quote-line-wrap {
  display: flex;
  align-items: stretch;
  gap: 40px;
}

/* quote-line：3px 琥珀橙竖线 */
.quote-line {
  width: 3px;
  background: var(--amber);
  flex-shrink: 0;
  min-height: 100%;
}

.quote-text-wrap {
  display: flex;
  flex-direction: column;
  gap: 36px;
}

/* 金句正文 */
.quote-text {
  font-family: var(--font-body);
  font-size: min(4.5vw, 5.5rem);
  font-weight: 300;
  color: var(--text-light);
  margin: 0;
  line-height: 1.3;
  letter-spacing: 0.01em;
}
.quote-text .keyword-highlight { color: var(--amber); }

/* 署名 */
.quote-cite {
  font-family: var(--font-mono);
  font-size: 15px;
  font-weight: 400;
  color: var(--text-ghost);
  letter-spacing: 0.12em;
  font-style: normal;
}
</style>
```

### ❌ 禁忌
- 禁止金句超过 2 行（超了拆成两个金句分两页放，或重新凝练）
- 禁止竖线颜色改成其他颜色（`quote-line` 必须是 `--amber`，这是引用组件的唯一装饰）
- 禁止在金句页放 eyebrow 或 float-tag（这一页需要极度留白，任何多余元素都在分散视线）
- 禁止给整个引用文字加粗（金句靠「字号大 + 字重轻」制造张力）
- 禁止引号装饰用实色（只能 `opacity < 0.07`，它是背景纹理不是前景元素）

---

## 页型六：截图展示页 Screenshot

**用途：** 展示真实产品截图或操作界面，用「证据」建立可信度。深底大图，底部渐变图注。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 工具界面截图 | 全宽图片，`object-fit: contain`，最大高度 80vh |
| 操作流程截图 | 图片居中，可加 `float-tag` 标注关键位置 |
| 图注/说明 | 底部渐变遮罩 + 白色文字，`Noto Sans SC weight 300` |
| 页面来源 | `JetBrains Mono`，图注右下角极小 |

**记忆点：** 真实截图 > 漂亮插图。渐变图注不遮住主体，只在底部 30% 位置。

### 本页文字基调
图注是「这是什么 + 为什么有用」——两句话。「Claude 的长文写作界面 · 实际输出的 3000 字报告」比「Claude 的使用界面展示」信息量强 3 倍。

### 完整 HTML 代码

```html
<section class="slide slide-screenshot" data-type="screenshot">
  <!-- eyebrow（左上，极小，不干扰图片）-->
  <p class="screenshot-eyebrow reveal">TOOL DEMO · 工具演示</p>

  <!-- 图片容器 -->
  <div class="screenshot-frame reveal">
    <img
      src="your-screenshot.png"
      alt="Claude 长文写作界面实测"
      class="screenshot-img"
    />
    <!-- 底部渐变图注 -->
    <div class="screenshot-caption">
      <p class="caption-main">Claude 的长文写作界面 · 实际输出的 3000 字报告</p>
      <span class="caption-source">claude.ai · 2026.05 实测</span>
    </div>
  </div>
</section>

<style>
.slide-screenshot {
  background: var(--dark);
  display: flex;
  flex-direction: column;
  padding: 60px 96px 60px;
  box-sizing: border-box;
  gap: 20px;
}

/* eyebrow */
.screenshot-eyebrow {
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.22em;
  color: var(--amber);
  text-transform: uppercase;
  margin: 0;
  flex-shrink: 0;
}

/* 图片容器 */
.screenshot-frame {
  position: relative;
  flex: 1;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
}

/* 截图 */
.screenshot-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  object-position: top center;
  display: block;
}

/* 底部渐变图注 */
.screenshot-caption {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  padding: 60px 40px 28px;
  background: linear-gradient(
    to top,
    rgba(26, 24, 22, 0.95) 0%,
    rgba(26, 24, 22, 0.6) 60%,
    transparent 100%
  );
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.caption-main {
  font-family: var(--font-body);
  font-size: 18px;
  font-weight: 300;
  color: var(--text-light);
  margin: 0;
  letter-spacing: 0.02em;
}
.caption-source {
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-ghost);
  letter-spacing: 0.12em;
  flex-shrink: 0;
  margin-left: 40px;
}
</style>
```

### ❌ 禁忌
- 禁止用美化插图替代真实截图（真实感是 Loki 品牌的核心，插图 = 失去可信度）
- 禁止截图加圆角或阴影（裸边框 `1px solid rgba()` 已经够，圆角是 SaaS 营销稿的气质）
- 禁止图注文字覆盖截图主体（渐变只覆盖底部 30%，不遮核心内容）
- 禁止在一张截图页放两张图（选一张最有说服力的，另一张单独一页）
- 禁止图注超过 2 句话（超过就是内容，单独建要点页来承载）

---

## 页型七：左右对比页 Compare

**用途：** 展示「之前/之后」、「A 方案/B 方案」、「错误做法/正确做法」，用视觉上的势均力敌强调对比。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| Before / After | 左列弱化（`opacity: 0.45`）、右列满亮度 |
| A / B 对比（无优劣） | 两列同等亮度，分割线居中 |
| 错误 / 正确 | 左列加 `❌` 标注前缀，右列加 `✓` 标注前缀 |

**记忆点：** 中间 1px 竖分割线（`vrule`），左右色彩/亮度的不对等感让眼睛自然聚焦到「正确那侧」。

### 本页文字基调
对比项用并行结构写——左右字数相近，语气对仗。「每天盲目测 10 个工具」 vs 「每周深度跑通 1 个工具」，节奏感来自并行。

### 完整 HTML 代码

```html
<section class="slide slide-compare" data-type="compare">
  <!-- 顶部标签行 -->
  <div class="compare-header reveal">
    <span class="compare-tag compare-before">❌ 之前的做法</span>
    <span class="compare-tag compare-after">✓ 现在的做法</span>
  </div>

  <!-- 对比内容区 -->
  <div class="compare-body">
    <!-- 左列：弱化 -->
    <div class="compare-col col-before reveal">
      <h3 class="compare-col-title">盲目追新</h3>
      <ul class="compare-list">
        <li>每天下载 3-5 个新工具</li>
        <li>跟着评测文章决定要不要用</li>
        <li>工具间没有任何联动</li>
        <li>订阅费每月 $200+，实际用 2 个</li>
      </ul>
    </div>

    <!-- 中间分割线：vrule -->
    <div class="vrule" aria-hidden="true"></div>

    <!-- 右列：满亮度 -->
    <div class="compare-col col-after reveal">
      <h3 class="compare-col-title">
        建<span class="keyword-highlight">工作流</span>，不建工具堆
      </h3>
      <ul class="compare-list">
        <li>每周深度跑通 1 个工具</li>
        <li>自己动手测真实使用场景</li>
        <li>工具之间有明确的衔接逻辑</li>
        <li>订阅费 ≤ $60，每个都在用</li>
      </ul>
    </div>
  </div>
</section>

<style>
.slide-compare {
  background: var(--dark);
  display: flex;
  flex-direction: column;
  padding: 72px 96px;
  box-sizing: border-box;
  gap: 56px;
}

/* 顶部标签行 */
.compare-header {
  display: flex;
  gap: 0;
  width: 100%;
}
.compare-tag {
  font-family: var(--font-mono);
  font-size: 13px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  flex: 1;
}
.compare-before { color: var(--text-muted); }
.compare-after  { color: var(--amber); padding-left: calc(50% + 1px); }

/* 对比内容区 */
.compare-body {
  display: grid;
  grid-template-columns: 1fr 1px 1fr;
  gap: 0 72px;
  flex: 1;
  align-items: start;
}

/* vrule：中间 1px 分割线 */
.vrule {
  width: 1px;
  background: rgba(255,255,255,0.12);
  height: 100%;
  align-self: stretch;
}

/* 对比列 */
.compare-col { display: flex; flex-direction: column; gap: 32px; }

/* Before 列弱化 */
.col-before { opacity: 0.42; }

/* 列标题 */
.compare-col-title {
  font-family: var(--font-title);
  font-size: min(3.5vw, 4.2rem);
  line-height: 1.1;
  color: var(--text-light);
  margin: 0;
}
.col-after .compare-col-title .keyword-highlight { color: var(--amber); }

/* 列表 */
.compare-list {
  list-style: none;
  margin: 0; padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0;
}
.compare-list li {
  font-family: var(--font-body);
  font-size: 20px;
  font-weight: 300;
  color: var(--text-light);
  padding: 18px 0;
  border-bottom: 1px solid rgba(255,255,255,0.07);
  line-height: 1.45;
}
.compare-list li:first-child { border-top: 1px solid rgba(255,255,255,0.07); }
</style>
```

### ❌ 禁忌
- 禁止左右列信息量严重不对等（格数差超过 2 条就失去对比感）
- 禁止右列（After/正确侧）字号明显大于左列——用 `opacity` 区分，而非字号（字号相同才有「势均力敌」感）
- 禁止分割线用彩色（`vrule` 只用极淡白色，不用琥珀橙，橙色是内容元素不是结构元素）
- 禁止超过 5 条对比项（超了视觉变成清单对比表，不是 Slides 的节奏）
- 禁止两列都满亮度（Before/After 的核心是视觉不对等，After 亮、Before 暗）

---

## 页型八：结尾页 End

**用途：** 整场演讲的最后一页，让观众知道「可以做什么」——关注、扫码、提问。最深底色，情绪最聚焦。

### 适合什么内容

| 内容类型 | 布局建议 |
|---------|---------|
| 核心 CTA（1 个） | 居中极大得意黑，`keyword-highlight` 高亮动词 |
| 联系方式 | `JetBrains Mono`，居中，3-4 行 |
| 二维码（可选） | 居中，`64×64px` 白底方块或图片 |
| 品牌 Logo SVG | 顶部居中，极小 |

**记忆点：** 全页最深底色（`--darker` `#111009`），信息密度最低，情绪最聚焦。CTA 用动词开头，直接。

### 本页文字基调
CTA 是命令句而非邀请句——「来关注我」不如「扫码关注 · 每周 AI 实测」。结尾不是总结，是行动召唤。联系方式格式一致：`平台 · 账号名`，不加废话描述。

### 完整 HTML 代码

```html
<section class="slide slide-end" data-type="end">
  <!-- 品牌 logo -->
  <div class="end-logo reveal">
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" style="color:#EBE4D6">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="end-brand-name">赛博小熊猫 Loki</span>
  </div>

  <!-- CTA 大字 -->
  <div class="end-cta reveal">
    <h2 class="end-cta-text">
      <span class="keyword-highlight">扫码关注</span>
      <br>每周 AI 实测不水字数
    </h2>
  </div>

  <!-- 联系方式 -->
  <div class="end-contacts reveal">
    <p class="end-contact-item">公众号 · 赛博小熊猫Loki</p>
    <p class="end-contact-item">网站 · hiloki.ai</p>
    <p class="end-contact-item">即刻 · 赛博小熊猫Loki</p>
  </div>

  <!-- 二维码占位（替换为实际 img 或 SVG）-->
  <div class="end-qr reveal">
    <div class="qr-placeholder">QR</div>
  </div>
</section>

<style>
.slide-end {
  background: var(--darker);  /* 最深底 #111009 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 72px 96px;
  box-sizing: border-box;
  gap: 48px;
  text-align: center;
}

/* 品牌 logo 行 */
.end-logo {
  display: flex;
  align-items: center;
  gap: 14px;
}
.end-brand-name {
  font-family: var(--font-mono);
  font-size: 14px;
  letter-spacing: 0.16em;
  color: var(--text-muted);
}

/* CTA 大字 */
.end-cta-text {
  font-family: var(--font-title);
  font-size: min(6.5vw, 8rem);
  line-height: 1.08;
  color: var(--text-light);
  margin: 0;
  letter-spacing: -0.01em;
}
.end-cta-text .keyword-highlight { color: var(--amber); }

/* 联系方式 */
.end-contacts {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.end-contact-item {
  font-family: var(--font-mono);
  font-size: 16px;
  color: var(--text-sub);
  letter-spacing: 0.14em;
  margin: 0;
}

/* 二维码 */
.end-qr {
  margin-top: 8px;
}
.qr-placeholder {
  width: 96px; height: 96px;
  background: rgba(253,250,245,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--text-ghost);
  letter-spacing: 0.1em;
}
/* 替换为实际二维码：<img src="qr.png" width="96" height="96"> */
</style>
```

### ❌ 禁忌
- 禁止结尾页放多个 CTA（「关注 + 扫码 + 加群 + 打赏」= 稀释行动力，只选一个最重要的）
- 禁止结尾页做成「感谢聆听」的总结页（总结是要点列表页的工作，结尾只做行动召唤）
- 禁止品牌 logo 比 CTA 字号大（logo 是身份标记，CTA 是主角）
- 禁止联系方式用不同字体混排（一律 `JetBrains Mono`，格式一致）
- 禁止结尾页底色用 `--dark`（必须用最深的 `--darker #111009`，色彩上的闭环感）

---

## 内容类型 → 页型映射（快速选择）

> 对应不二结论①：内容形状决定容器，不是反过来。

| 内容形状 | 对应页型 | 底色 |
|---------|---------|------|
| 演讲开场 | 封面页 Cover | 深底 |
| 主题切换 / 章节分割 | 章节幕封 Chapter | 深底 |
| 2-5 个并列结论 | 要点列表页 Points | 浅底（暖米）|
| 单一有冲击力的数据 | 数据大字报页 Stat | 深底 |
| 核心观点 / 值得记住的一句话 | 金句引用页 Quote | 深底 |
| 工具截图 / 操作界面 / 产品展示 | 截图展示页 Screenshot | 深底 |
| Before/After / A vs B / 错误 vs 正确 | 左右对比页 Compare | 深底 |
| 关注 / 扫码 / 提问 / 演讲收尾 | 结尾页 End | 最深底 |

**原则：** 一件事 → 一个页型。内容匹配不上任何页型 = 这件事要么删掉，要么拆成两页。

---

## Checklist（生成前自检）

### 节奏层
- [ ] 连续同色底页不超过 3 页
- [ ] 7 页以内使用了至少 5 种不同页型
- [ ] 有封面页作为第一页
- [ ] 有结尾页作为最后一页

### 字体层
- [ ] 得意黑只用于标题（封面、章节幕封、结尾 CTA）
- [ ] `Space Grotesk weight 200` 只用于数字大字报
- [ ] `JetBrains Mono` 只用于元信息、期号、来源、联系方式
- [ ] 大字号都用了 `min(Xvw, Yrem)` 双约束
- [ ] 字号/字重反比：越大越细，没有大标题 + 加粗的组合

### 颜色层
- [ ] 琥珀橙 `#C87A45` 每页出现不超过 3 处
- [ ] 霓虹青 `#00D9FF` 全场最多出现 2 次，且只在深底页
- [ ] 没有出现渐变色、紫色、纯黑 `#000000`、纯白 `#FFFFFF`

### 装饰层
- [ ] `keyword-highlight` 每个标题中不超过 2 个词
- [ ] `quote-line` 只出现在金句引用页
- [ ] `chapter-num` 装饰性大背景数字 `opacity < 0.07`
- [ ] `stat-unit` 字号约数字的 1/4，不放大

### 内容层
- [ ] 每页只说一件事（内容超出 → 拆页，不是缩小字号）
- [ ] 要点列表页每页不超过 5 条
- [ ] 截图展示页放的是真实截图，不是插图
- [ ] 结尾页只有 1 个 CTA

---

*最后更新：2026-05-27*  
*适用于赛博小熊猫 Loki 演讲 / 分享 / 课程讲义场景*  
*舞台架构参考 Zara frontend-slides · 节奏约束来自归藏 guizang-ppt-skill · 装饰命名逻辑来自不二 esther-design-system*
