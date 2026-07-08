# 小红书 / 社媒卡片场景 · scene-rednote.md
> 赛博小熊猫 Loki · 设计系统场景文件
> 尺寸基准：1080×1440px（3:4）HTML 模拟输出
> 最后更新：2026-05-27

---

## 场景定位

触发场景：AI 工具测评卡、干货合集、金句系列、工具横评、教程步骤、数据洞察。

**核心情绪目标：「收藏/分享给朋友」**——不是「我看了挺好」，是「这个我要留着」。每张卡片只传达一件事，传达到位，不贪多。

### 全局规则（写在卡片外部，适用于所有 8 种类型）

| 规则 | 说明 |
|------|------|
| **字号基准** | 基于 1080×1440px 实际输出。标题 ≥ 48px，正文 ≥ 36px，元信息 ≥ 24px。这是手机阅读的物理底线，不是视觉感觉 |
| **品牌标识位置** | 固定右下角，文字「赛博小熊猫Loki」+ 小熊猫 SVG，颜色浅底用 `#C87A45`，深底用 `#EBE4D6` |
| **进度点（series-dots）** | 系列卡片顶部居中，●=已读，○=未读，间距 8px，颜色 `#C87A45`/`#C4BBB0` |
| **主底色** | 暖米 `#F5F0E8` 为主；深底卡用 `#1A1816` 做对比，一组里最多 2 张深底 |
| **Eyebrow 标签** | 每张卡顶部或左上角，Space Grotesk，全大写，letter-spacing: 0.2em，颜色 `#9A9085` |
| **关键词点橙** | 标题中 1-2 个词 `color: #C87A45`，不是整行变色 |
| **霓虹青 `#00D9FF` 约束** | 一张卡最多出现一次，出就是记忆点，不滥用 |

### 本场景文字基调

- 直接、有立场，不说废话，不做铺垫
- 数字要具体（「省 40 分钟」好过「节省时间」）
- 金句一行，不拆断，不换行破意
- 工具名称首字母大写或保持原名，不乱加引号
- Emoji 极克制：每张卡最多 1 个，用于序号替代或结尾引导，不做装饰堆砌

---

## 全局 CSS 变量与字体加载（所有卡片共用 head 部分）

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>

<style>
:root {
  /* 底色 */
  --warm-rice: #F5F0E8;
  --oat:       #EBE4D6;
  --dark-bg:   #1A1816;
  --paper:     #FDFAF5;

  /* 品牌色 */
  --amber:     #C87A45;
  --amber-lt:  #D9A87A;
  --amber-dk:  #A05E30;
  --neon-cyan: #00D9FF;
  --fire-org:  #FF8C00;

  /* 文字 */
  --text-main: #1F1D1A;
  --text-sub:  #6B6157;
  --text-mute: #9A9085;
  --text-dim:  #C4BBB0;
  --text-lt:   #FDFAF5;

  /* 装饰 */
  --line:      #EBE4D6;
  --line-dark: #2E2A26;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

.card {
  width: 1080px;
  height: 1440px;
  position: relative;
  overflow: hidden;
  font-family: 'Noto Sans SC', sans-serif;
}

/* ── 进度点 ── */
.series-dots {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: center;
}
.series-dots span {
  font-size: 18px;
  line-height: 1;
  color: var(--amber);
}
.series-dots span.inactive {
  color: var(--text-dim);
}

/* ── 品牌标识 ── */
.brand-mark {
  position: absolute;
  bottom: 52px;
  right: 56px;
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-mark svg { opacity: 0.9; }
.brand-mark .brand-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 300;
  letter-spacing: 0.04em;
  color: var(--amber);
}
.brand-mark.on-dark .brand-text { color: var(--oat); }
.brand-mark.on-dark svg { color: var(--oat); }

/* ── Eyebrow ── */
.eyebrow {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 300;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--text-mute);
}
.eyebrow.on-dark { color: #6B6157; }

/* ── 评分条（score-bar）── */
.score-bar-wrap { display: flex; flex-direction: column; gap: 10px; }
.score-bar-row {
  display: flex;
  align-items: center;
  gap: 16px;
}
.score-bar-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 300;
  color: var(--text-sub);
  width: 120px;
  flex-shrink: 0;
}
.score-bar-track {
  flex: 1;
  height: 8px;
  background: var(--oat);
  border-radius: 4px;
  overflow: hidden;
}
.score-bar-fill {
  height: 100%;
  border-radius: 4px;
  background: var(--amber);
  transition: width 0s;
}
.score-bar-val {
  font-family: 'JetBrains Mono', monospace;
  font-size: 24px;
  color: var(--text-sub);
  width: 48px;
  text-align: right;
  flex-shrink: 0;
}

/* ── 步骤序号（step-num）── */
.step-num {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 2px solid var(--amber);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 30px;
  font-weight: 200;
  color: var(--amber);
  flex-shrink: 0;
}

/* ── 对比列分隔 ── */
.compare-divider {
  width: 1px;
  background: var(--line);
  flex-shrink: 0;
}
</style>
```

---

## 1. 封面卡 Cover

**用途**：系列第 1 张。建立视觉锚点，让人判断「这一组要不要看下去」。

**适合内容**：
- 「X 个工具测评」「AI 工作流干货」「金句系列 Vol.N」
- 有明确主题词、有系列感、有号召性副标题

**文字基调**：标题要有立场，不是「介绍一下……」，是「这 5 个工具让我效率翻倍」。副标题一句话说清楚内容是什么。

**❌ 禁忌**：
- 副标题超过 2 行
- 全屏塞满元素，没有留白
- 系列序号放中间（只能右下角或顶部居中）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Cover Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
/* [在此插入全局 CSS 变量] */
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --amber-lt:#D9A87A; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0; --text-lt:#FDFAF5;
  --line:#EBE4D6;
}
* { margin:0; padding:0; box-sizing:border-box; }

body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background: var(--warm-rice);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
}

/* 右侧橙竖条 — 封面品牌辨识条 */
.cover-stripe {
  position:absolute; right:0; top:0; bottom:0;
  width:18px;
  background: var(--amber);
}

/* 顶部区域 */
.cover-top {
  padding: 80px 96px 0 96px;
  display:flex; flex-direction:column; gap:24px;
}

.series-dots {
  display:flex; align-items:center; gap:8px;
}
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:var(--text-dim); }

.eyebrow {
  font-family:'Space Grotesk',sans-serif;
  font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase;
  color:var(--text-mute);
}

/* 主标题区 — 靠下留白大 */
.cover-body {
  position:absolute;
  bottom: 220px; left:96px; right:120px;
}

.cover-vol {
  font-family:'JetBrains Mono',monospace;
  font-size:26px; color:var(--amber);
  letter-spacing:0.1em;
  margin-bottom:32px;
}

.cover-title {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:96px; line-height:1.05;
  color:var(--text-main);
  letter-spacing:-0.02em;
  margin-bottom:40px;
}
.cover-title .hl { color:var(--amber); }

.cover-subtitle {
  font-family:'Noto Sans SC',sans-serif;
  font-size:36px; font-weight:300; line-height:1.6;
  color:var(--text-sub);
  border-left:3px solid var(--amber);
  padding-left:24px;
}

/* 底部装饰线 */
.cover-rule {
  position:absolute;
  bottom: 180px; left:96px;
  width:160px; height:1px;
  background:var(--oat);
}

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:var(--amber); }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif;
  font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:var(--amber);
}
</style>
</head>
<body>
<div class="card">
  <div class="cover-stripe"></div>

  <div class="cover-top">
    <div class="series-dots">
      <span>●</span><span class="inactive">○</span>
      <span class="inactive">○</span><span class="inactive">○</span>
    </div>
    <div class="eyebrow">AI TOOLS · REVIEW SERIES</div>
  </div>

  <div class="cover-body">
    <div class="cover-vol">VOL.01</div>
    <h1 class="cover-title">
      5 个 AI 工具<br>
      让我<span class="hl">效率</span>翻倍
    </h1>
    <p class="cover-subtitle">
      一个文科生的亲测报告<br>每个都附上真实使用场景
    </p>
  </div>

  <div class="cover-rule"></div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 2. 列表卡 List

**用途**：「X 个工具 / 方法 / 技巧」。快速给读者 takeaway，是收藏率最高的卡片类型之一。

**适合内容**：
- 条数在 3–8 条之间（超过 8 条要拆成多张）
- 每条一句话，不展开，每条都独立成立
- 条目之间有隐性关联（同类工具 / 同主题技巧）

**文字基调**：每条直接说工具名或方法名，加 3–6 字的价值点，不写解释。读者扫一眼就知道这条是不是要点进去看。

**❌ 禁忌**：
- 每条超过两行（必须一行内）
- 序号和文字靠太近（序号是视觉元素，要有间距）
- 所有条目等重——实际上第一条和最后一条要在视觉上有区分

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>List Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
  --line:#EBE4D6;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background:var(--warm-rice);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
  padding:80px 96px;
}

.card-top {
  display:flex; flex-direction:column; gap:20px;
  margin-bottom:64px;
}

.series-dots { display:flex; gap:8px; }
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:var(--text-dim); }

.eyebrow {
  font-family:'Space Grotesk',sans-serif;
  font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase;
  color:var(--text-mute);
}

.card-title {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:72px; line-height:1.1;
  color:var(--text-main);
  letter-spacing:-0.02em;
}
.card-title .hl { color:var(--amber); }

/* 列表主体 */
.list-body {
  display:flex; flex-direction:column; gap:0;
}

.list-item {
  display:flex; align-items:center;
  gap:40px;
  padding:32px 0;
  border-bottom:1px solid var(--oat);
}
.list-item:last-child { border-bottom:none; }

.list-num {
  font-family:'Space Grotesk',sans-serif;
  font-size:52px; font-weight:200;
  color:var(--text-dim);
  width:72px; flex-shrink:0;
  line-height:1;
  /* 大序号是装饰，不抢内容 */
}
/* 第一条序号高亮，制造层次 */
.list-item:first-child .list-num { color:var(--amber); }

.list-content { flex:1; }
.list-tool {
  font-family:'Space Grotesk',sans-serif;
  font-size:32px; font-weight:500;
  color:var(--text-main);
  letter-spacing:0.01em;
  margin-bottom:6px;
}
.list-desc {
  font-size:30px; font-weight:300;
  color:var(--text-sub); line-height:1.5;
}

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:var(--amber); }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif;
  font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:var(--amber);
}
</style>
</head>
<body>
<div class="card">
  <div class="card-top">
    <div class="series-dots">
      <span class="inactive">○</span><span>●</span>
      <span class="inactive">○</span><span class="inactive">○</span>
    </div>
    <div class="eyebrow">AI TOOLS COLLECTION</div>
    <h2 class="card-title">
      <span class="hl">5 个</span>工具<br>我每天都在用
    </h2>
  </div>

  <div class="list-body">
    <div class="list-item">
      <div class="list-num">01</div>
      <div class="list-content">
        <div class="list-tool">Perplexity</div>
        <div class="list-desc">学术搜索，信息可溯源，替代百度</div>
      </div>
    </div>
    <div class="list-item">
      <div class="list-num">02</div>
      <div class="list-content">
        <div class="list-tool">Claude</div>
        <div class="list-desc">长文写作/改稿，理解力最好</div>
      </div>
    </div>
    <div class="list-item">
      <div class="list-num">03</div>
      <div class="list-content">
        <div class="list-tool">Cursor</div>
        <div class="list-desc">不会代码也能用，做网页工具</div>
      </div>
    </div>
    <div class="list-item">
      <div class="list-num">04</div>
      <div class="list-content">
        <div class="list-tool">Notion AI</div>
        <div class="list-desc">知识库整理，摘要速度极快</div>
      </div>
    </div>
    <div class="list-item">
      <div class="list-num">05</div>
      <div class="list-content">
        <div class="list-tool">ElevenLabs</div>
        <div class="list-desc">语音克隆，做播客省 2 小时</div>
      </div>
    </div>
  </div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 3. 工具测评卡 Review

**用途**：单个工具的深度评价。给读者一个「要不要用它」的清晰结论。

**适合内容**：
- 一张卡只测一个工具
- 包含评分维度（易用性/功能/性价比等）、一句话总结、优缺点列表

**文字基调**：立场鲜明，不说「有优有劣」。「总结」那行必须是一个判断，不是描述。优缺点各 2-3 条，不需要对称，缺点可以比优点少。

**❌ 禁忌**：
- 评分全高（那就不是测评，是广告）
- 优缺点超过 4 条（认知过载，读者不记了）
- 总结用「综上所述……」这类书面语

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Review Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --amber-lt:#D9A87A; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
  --line:#EBE4D6;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background:var(--warm-rice);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
  padding:80px 96px;
}

/* 顶部 */
.card-top { margin-bottom:52px; }
.series-dots { display:flex; gap:8px; margin-bottom:20px; }
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:var(--text-dim); }
.eyebrow {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase; color:var(--text-mute);
}

/* 工具名 + 类别标签 */
.tool-header {
  display:flex; align-items:flex-end; gap:24px;
  margin-top:32px; margin-bottom:12px;
}
.tool-name {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:84px; line-height:1; color:var(--text-main);
  letter-spacing:-0.02em;
}
.tool-tag {
  font-family:'Space Grotesk',sans-serif;
  font-size:24px; font-weight:300;
  color:var(--amber); border:1px solid var(--amber);
  padding:4px 16px; border-radius:4px;
  margin-bottom:16px; letter-spacing:0.05em;
}

/* 一句话总结 */
.tool-verdict {
  font-size:36px; font-weight:300; line-height:1.5;
  color:var(--text-sub);
  padding:28px 32px;
  background:var(--paper);
  border-left:4px solid var(--amber);
  margin-bottom:48px;
}

/* 评分条 */
.score-section { margin-bottom:48px; }
.score-label-title {
  font-family:'Space Grotesk',sans-serif;
  font-size:20px; font-weight:300; letter-spacing:0.15em;
  text-transform:uppercase; color:var(--text-mute);
  margin-bottom:24px;
}
.score-bar-wrap { display:flex; flex-direction:column; gap:18px; }
.score-bar-row { display:flex; align-items:center; gap:20px; }
.score-bar-label {
  font-family:'Space Grotesk',sans-serif; font-size:26px;
  font-weight:300; color:var(--text-sub); width:130px; flex-shrink:0;
}
.score-bar-track {
  flex:1; height:10px; background:var(--oat); border-radius:5px; overflow:hidden;
}
.score-bar-fill {
  height:100%; border-radius:5px; background:var(--amber);
}
.score-bar-val {
  font-family:'JetBrains Mono',monospace; font-size:26px;
  color:var(--text-sub); width:52px; text-align:right; flex-shrink:0;
}

/* 优缺点 */
.pros-cons { display:flex; gap:40px; }
.pros-col, .cons-col { flex:1; }
.pros-cons-title {
  font-family:'Space Grotesk',sans-serif;
  font-size:22px; font-weight:400; letter-spacing:0.12em;
  text-transform:uppercase; margin-bottom:20px;
}
.pros-col .pros-cons-title { color: #7A8458; }
.cons-col .pros-cons-title { color: #9A7070; }

.pc-item {
  display:flex; align-items:flex-start; gap:12px;
  font-size:30px; font-weight:300; line-height:1.5;
  color:var(--text-main); margin-bottom:14px;
}
.pc-item .pc-icon {
  font-family:'Space Grotesk',sans-serif;
  font-size:26px; font-weight:500; margin-top:2px; flex-shrink:0;
}
.pros-col .pc-icon { color:#7A8458; }
.cons-col .pc-icon { color:#9A7070; }

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:var(--amber); }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:var(--amber);
}
</style>
</head>
<body>
<div class="card">
  <div class="card-top">
    <div class="series-dots">
      <span class="inactive">○</span><span class="inactive">○</span>
      <span>●</span><span class="inactive">○</span>
    </div>
    <div class="eyebrow">TOOL REVIEW · AI WRITING</div>
    <div class="tool-header">
      <div class="tool-name">Claude</div>
      <div class="tool-tag">AI 写作</div>
    </div>
  </div>

  <div class="tool-verdict">
    文科生的主力写作工具，理解力全场最好，但价格让人肉疼
  </div>

  <div class="score-section">
    <div class="score-label-title">评分维度</div>
    <div class="score-bar-wrap">
      <div class="score-bar-row">
        <div class="score-bar-label">易用性</div>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:90%"></div></div>
        <div class="score-bar-val">9.0</div>
      </div>
      <div class="score-bar-row">
        <div class="score-bar-label">理解力</div>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:96%"></div></div>
        <div class="score-bar-val">9.6</div>
      </div>
      <div class="score-bar-row">
        <div class="score-bar-label">性价比</div>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:60%"></div></div>
        <div class="score-bar-val">6.0</div>
      </div>
      <div class="score-bar-row">
        <div class="score-bar-label">稳定性</div>
        <div class="score-bar-track"><div class="score-bar-fill" style="width:82%"></div></div>
        <div class="score-bar-val">8.2</div>
      </div>
    </div>
  </div>

  <div class="pros-cons">
    <div class="pros-col">
      <div class="pros-cons-title">✓ 优点</div>
      <div class="pc-item"><span class="pc-icon">✓</span>改稿指令精准执行</div>
      <div class="pc-item"><span class="pc-icon">✓</span>长文不乱不跑题</div>
      <div class="pc-item"><span class="pc-icon">✓</span>引用场景理解准确</div>
    </div>
    <div class="cons-col">
      <div class="pros-cons-title">✗ 缺点</div>
      <div class="pc-item"><span class="pc-icon">✗</span>免费额度极少</div>
      <div class="pc-item"><span class="pc-icon">✗</span>无法联网检索</div>
    </div>
  </div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 4. 金句卡 Quote

**用途**：一句有力量的话，单独成卡。分享率最高，传播性最强。

**适合内容**：
- 原创观点（来自文章、播客、演讲）
- 反常识判断（「AI 工具的瓶颈不是技术，是你的问题意识」）
- 有张力的对立感（「用了，不一定有用。不用，肯定没用。」）

**文字基调**：金句是完整的，不需要补充语境。一句话成立，不加解释，不加注释。署名只写「赛博小熊猫Loki」。

**❌ 禁忌**：
- 金句拆成两句（破坏冲击力）
- 字号不够大（这张卡就是字，字就是画面）
- 加过多装饰（竖线就够了，不要方块、气泡、阴影）
- 用名人金句冒充自己原创

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Quote Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816;
  --amber:#C87A45; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  /* 深底版 — 金句适合深底，反差强，截图传播效果好 */
  background:var(--dark-bg);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
}

/* 大装饰引号 — 背景级装饰，不抢金句 */
.deco-quote {
  position:absolute;
  top:80px; left:72px;
  font-family:'Space Grotesk',sans-serif;
  font-size:320px; line-height:1;
  font-weight:200;
  color:rgba(200,122,69,0.07);
  user-select:none;
  pointer-events:none;
}

/* 顶部小标签 */
.card-top {
  position:absolute;
  top:80px; left:96px; right:96px;
  display:flex; justify-content:space-between; align-items:center;
}
.eyebrow {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase; color:#4A4540;
}
.series-dots { display:flex; gap:8px; }
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:#3A3530; }

/* 金句主体 — 垂直居中偏上 */
.quote-body {
  position:absolute;
  top:50%; left:96px; right:96px;
  transform:translateY(-54%);
}

/* 装饰竖线 */
.quote-vline {
  width:4px; height:80px;
  background:var(--amber);
  margin-bottom:48px;
}

.quote-text {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:76px; line-height:1.18;
  color:#FDFAF5;
  letter-spacing:-0.01em;
}
.quote-text .hl { color:var(--amber); }

.quote-source {
  margin-top:52px;
  display:flex; align-items:center; gap:20px;
}
.quote-source-line {
  width:40px; height:1px; background:var(--amber); opacity:0.6;
}
.quote-source-text {
  font-family:'Space Grotesk',sans-serif;
  font-size:26px; font-weight:300;
  color:#6B6157; letter-spacing:0.08em;
}

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:#EBE4D6; }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:#EBE4D6;
}

/* 底部霓虹线装饰 */
.neon-rule {
  position:absolute; bottom:130px; left:96px;
  width:60px; height:2px; background:var(--neon-cyan);
  box-shadow:0 0 12px rgba(0,217,255,0.4);
}
</style>
</head>
<body>
<div class="card">
  <div class="deco-quote">"</div>

  <div class="card-top">
    <div class="eyebrow">LOKI'S TAKE</div>
    <div class="series-dots">
      <span class="inactive">○</span><span class="inactive">○</span>
      <span class="inactive">○</span><span>●</span>
    </div>
  </div>

  <div class="quote-body">
    <div class="quote-vline"></div>
    <div class="quote-text">
      AI 工具的瓶颈<br>
      不是<span class="hl">技术</span>，<br>
      是你的<span class="hl">问题意识</span>
    </div>
    <div class="quote-source">
      <div class="quote-source-line"></div>
      <div class="quote-source-text">赛博小熊猫Loki · 2026</div>
    </div>
  </div>

  <div class="neon-rule"></div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 5. 步骤卡 Steps

**用途**：「怎么做」类内容。1→2→3 流程，给读者一条清晰的行动路径。

**适合内容**：
- 教程、操作步骤、工作流
- 3–5 步最佳（少于 3 步不需要卡片，多于 5 步要拆）
- 每步必须有可执行动作，不是「了解……」，是「打开……」「输入……」「点击……」

**文字基调**：动词开头，具体到可执行。「第一步」「然后」「接下来」这类过渡词删掉，直接是动作。

**❌ 禁忌**：
- 步骤之间没有连接感（必须有视觉上的流向暗示）
- 每步长度差异极大（排版散）
- 步骤序号小于正文字号（序号是视觉锚点）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Steps Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
  --line:#EBE4D6;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background:var(--warm-rice);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
  padding:80px 96px;
}

.card-top { margin-bottom:60px; }
.series-dots { display:flex; gap:8px; margin-bottom:20px; }
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:var(--text-dim); }
.eyebrow {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase; color:var(--text-mute);
  margin-bottom:24px;
}
.card-title {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:68px; line-height:1.1; color:var(--text-main);
  letter-spacing:-0.02em;
}
.card-title .hl { color:var(--amber); }

/* 步骤主体 */
.steps-body { display:flex; flex-direction:column; gap:0; }

.step-item {
  display:flex; gap:36px;
  padding:36px 0;
}

.step-left {
  display:flex; flex-direction:column;
  align-items:center; flex-shrink:0; width:72px;
}
/* step-num 圆形序号 */
.step-num {
  width:72px; height:72px; border-radius:50%;
  border:2px solid var(--amber);
  display:flex; align-items:center; justify-content:center;
  font-family:'Space Grotesk',sans-serif;
  font-size:28px; font-weight:200; color:var(--amber);
  flex-shrink:0;
}
/* 当前步骤（第一步）填色 */
.step-item:first-child .step-num {
  background:var(--amber); color:#FDFAF5;
}
/* 步骤之间的连接线 */
.step-connector {
  width:1px; flex:1;
  background:var(--oat);
  margin:8px 0;
  min-height:24px;
}
.step-item:last-child .step-connector { display:none; }

.step-content { flex:1; padding-top:14px; }
.step-title {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:44px; line-height:1.2; color:var(--text-main);
  margin-bottom:10px;
}
.step-desc {
  font-size:30px; font-weight:300; line-height:1.6;
  color:var(--text-sub);
}
.step-tag {
  display:inline-block;
  margin-top:14px;
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  color:var(--amber); border:1px solid var(--amber);
  padding:3px 14px; border-radius:3px; letter-spacing:0.05em;
}

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:var(--amber); }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:var(--amber);
}
</style>
</head>
<body>
<div class="card">
  <div class="card-top">
    <div class="series-dots">
      <span class="inactive">○</span><span class="inactive">○</span>
      <span>●</span><span class="inactive">○</span>
    </div>
    <div class="eyebrow">WORKFLOW · HOW TO</div>
    <h2 class="card-title">
      用 AI 写出<span class="hl">有用</span>文章<br>3 步工作流
    </h2>
  </div>

  <div class="steps-body">
    <div class="step-item">
      <div class="step-left">
        <div class="step-num">1</div>
        <div class="step-connector"></div>
      </div>
      <div class="step-content">
        <div class="step-title">拆解读者问题</div>
        <div class="step-desc">问 Claude：「目标读者遇到 X 问题时，会搜索哪 5 个关键词？」</div>
        <div class="step-tag">Perplexity + Claude</div>
      </div>
    </div>
    <div class="step-item">
      <div class="step-left">
        <div class="step-num">2</div>
        <div class="step-connector"></div>
      </div>
      <div class="step-content">
        <div class="step-title">搭结构，不要直接写</div>
        <div class="step-desc">先让 AI 出提纲，你改逻辑，再逐段生成，不要一次性全写</div>
        <div class="step-tag">Claude Sonnet</div>
      </div>
    </div>
    <div class="step-item">
      <div class="step-left">
        <div class="step-num">3</div>
        <div class="step-connector"></div>
      </div>
      <div class="step-content">
        <div class="step-title">加入你的亲测细节</div>
        <div class="step-desc">每篇至少 1 个真实使用场景，AI 写不出这个，这是你的护城河</div>
        <div class="step-tag">只能靠自己</div>
      </div>
    </div>
  </div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 6. 对比卡 Compare

**用途**：两个选项的正面对比。帮读者做决策，不是「都挺好」，是「这个更适合你」。

**适合内容**：
- A 工具 vs B 工具
- 用 AI / 不用 AI
- 老方法 / 新方法
- 两种场景 / 两种人群

**文字基调**：每列 3–5 行，每行一条维度，平行句式。结论行必须有立场，不能「各有优劣」。

**❌ 禁忌**：
- 两列信息量严重不对等（视觉失衡）
- 没有结论行（对比没有指向，读者不知道该怎么选）
- 用颜色给一列加光环（不能靠颜色暗示「谁赢了」，靠内容说话）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Compare Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
  --line:#EBE4D6;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background:var(--warm-rice);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
  padding:80px 96px;
}

.card-top { margin-bottom:56px; }
.series-dots { display:flex; gap:8px; margin-bottom:20px; }
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:var(--text-dim); }
.eyebrow {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase; color:var(--text-mute);
  margin-bottom:24px;
}
.card-title {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:68px; line-height:1.1; color:var(--text-main);
  letter-spacing:-0.02em;
}
.card-title .hl { color:var(--amber); }

/* 对比主体 */
.compare-grid {
  display:grid; grid-template-columns:1fr 1px 1fr;
  gap:0; margin-bottom:48px;
}

.compare-col { padding:0 40px; }
.compare-col:first-child { padding-left:0; }
.compare-col:last-child { padding-right:0; }

/* 中间分隔线 */
.compare-divider {
  background:var(--line); width:1px;
}

.col-header {
  margin-bottom:36px;
  padding-bottom:24px;
  border-bottom:2px solid var(--oat);
}
.col-name {
  font-family:'Space Grotesk',sans-serif;
  font-size:36px; font-weight:500;
  color:var(--text-main); letter-spacing:0.02em;
  margin-bottom:8px;
}
.col-sub {
  font-family:'Space Grotesk',sans-serif;
  font-size:24px; font-weight:300;
  color:var(--text-mute); letter-spacing:0.05em;
}
/* 左列（被比较对象/弱一方）样式 */
.compare-col.col-a .col-name { color:var(--text-sub); }
/* 右列（推荐/强一方）强调 */
.compare-col.col-b .col-name { color:var(--amber); }

.compare-row {
  display:flex; align-items:flex-start; gap:14px;
  padding:18px 0;
  border-bottom:1px solid var(--oat);
  font-size:30px; font-weight:300; line-height:1.5;
  color:var(--text-main);
}
.compare-row:last-child { border-bottom:none; }
.compare-row .row-dot {
  width:8px; height:8px; border-radius:50%;
  background:var(--oat); margin-top:11px; flex-shrink:0;
}
.compare-col.col-b .row-dot { background:var(--amber); }

/* 结论行 */
.compare-verdict {
  background:var(--paper);
  border-left:4px solid var(--amber);
  padding:28px 32px;
  font-size:34px; font-weight:300; line-height:1.5;
  color:var(--text-sub);
}
.compare-verdict strong { color:var(--text-main); font-weight:500; }

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:var(--amber); }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:var(--amber);
}
</style>
</head>
<body>
<div class="card">
  <div class="card-top">
    <div class="series-dots">
      <span class="inactive">○</span><span class="inactive">○</span>
      <span class="inactive">○</span><span>●</span>
    </div>
    <div class="eyebrow">HEAD TO HEAD · AI TOOLS</div>
    <h2 class="card-title">
      ChatGPT vs <span class="hl">Claude</span><br>文科生选哪个？
    </h2>
  </div>

  <div class="compare-grid">
    <div class="compare-col col-a">
      <div class="col-header">
        <div class="col-name">ChatGPT</div>
        <div class="col-sub">OPENAI</div>
      </div>
      <div class="compare-row"><span class="row-dot"></span>插件生态丰富</div>
      <div class="compare-row"><span class="row-dot"></span>免费额度更多</div>
      <div class="compare-row"><span class="row-dot"></span>可联网搜索</div>
      <div class="compare-row"><span class="row-dot"></span>长文理解时跑题</div>
      <div class="compare-row"><span class="row-dot"></span>改稿指令打折执行</div>
    </div>
    <div class="compare-divider"></div>
    <div class="compare-col col-b">
      <div class="col-header">
        <div class="col-name">Claude</div>
        <div class="col-sub">ANTHROPIC</div>
      </div>
      <div class="compare-row"><span class="row-dot"></span>写作理解力最好</div>
      <div class="compare-row"><span class="row-dot"></span>改稿精准执行</div>
      <div class="compare-row"><span class="row-dot"></span>长文不丢失逻辑</div>
      <div class="compare-row"><span class="row-dot"></span>无联网功能</div>
      <div class="compare-row"><span class="row-dot"></span>免费额度少</div>
    </div>
  </div>

  <div class="compare-verdict">
    <strong>文科写作首选 Claude。</strong>
    ChatGPT 留给需要联网和工具调用的场景
  </div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 7. 数据卡 Data

**用途**：一个（最多两个）核心数据，让数字说话。收藏率极高，适合截图传播。

**适合内容**：
- 有冲击力的具体数字（「省了 40 分钟 / 天」「覆盖 5000+ 读者」）
- 数字必须有解读（大数字下方一句话说「这意味着什么」）
- 对比数据（用前 vs 用后）

**文字基调**：数字是主角，其余都是注脚。大数字不加单位说明就要求读者猜——必须明确写清楚量纲。解读用「也就是说……」而不是「数据表明……」。

**❌ 禁忌**：
- 超过 2 个大数字（读者不知道看哪个）
- 数字来源不可信（不要编造）
- 数字没有解读（读完不知道为什么这个数字重要）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Data Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background:var(--dark-bg);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
}

/* 顶部区 */
.card-top {
  position:absolute; top:80px; left:96px; right:96px;
}
.series-dots { display:flex; gap:8px; margin-bottom:20px; }
.series-dots span { font-size:20px; color:var(--amber); }
.series-dots span.inactive { color:#2E2A26; }
.eyebrow {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase; color:#4A4540;
}

/* 主体 — 数字居中 */
.data-body {
  position:absolute;
  top:50%; left:96px; right:96px;
  transform:translateY(-52%);
  text-align:center;
}

/* 大数字 */
.data-number {
  font-family:'Space Grotesk',sans-serif;
  font-size:240px; font-weight:200; line-height:0.9;
  color:var(--amber); letter-spacing:-0.04em;
  margin-bottom:0;
}
.data-unit {
  font-family:'Space Grotesk',sans-serif;
  font-size:60px; font-weight:200;
  color:var(--amber); opacity:0.6;
  letter-spacing:0.05em;
  margin-bottom:48px;
}

/* 分割线 */
.data-rule {
  width:80px; height:1px;
  background:var(--amber); opacity:0.4;
  margin:0 auto 40px;
}

.data-label {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:52px; line-height:1.3;
  color:#FDFAF5; margin-bottom:28px;
}
.data-label .hl { color:var(--amber); }

.data-interpret {
  font-size:32px; font-weight:300; line-height:1.6;
  color:#6B6157;
}

/* 第二数据块（可选） */
.data-secondary {
  margin-top:72px;
  padding-top:48px;
  border-top:1px solid #2E2A26;
  display:flex; justify-content:center; gap:80px;
}
.data-sec-item { text-align:center; }
.data-sec-num {
  font-family:'Space Grotesk',sans-serif;
  font-size:72px; font-weight:200;
  color:var(--oat); line-height:1;
  margin-bottom:12px;
}
.data-sec-label {
  font-family:'Noto Sans SC',sans-serif;
  font-size:26px; font-weight:300;
  color:#4A4540;
}

/* 霓虹点睛 */
.neon-dot {
  position:absolute; top:80px; right:96px;
  width:12px; height:12px; border-radius:50%;
  background:var(--neon-cyan);
  box-shadow:0 0 20px rgba(0,217,255,0.5), 0 0 40px rgba(0,217,255,0.2);
}

/* 品牌标识 */
.brand-mark {
  position:absolute; bottom:52px; right:56px;
  display:flex; align-items:center; gap:10px;
}
.brand-mark svg { color:var(--oat); }
.brand-mark .brand-text {
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.04em; color:var(--oat);
}
</style>
</head>
<body>
<div class="card">
  <div class="neon-dot"></div>

  <div class="card-top">
    <div class="series-dots">
      <span class="inactive">○</span><span>●</span>
      <span class="inactive">○</span><span class="inactive">○</span>
    </div>
    <div class="eyebrow">DATA · MY USAGE STATS</div>
  </div>

  <div class="data-body">
    <div class="data-number">40</div>
    <div class="data-unit">MIN / DAY</div>
    <div class="data-rule"></div>
    <div class="data-label">
      我用 AI 每天<span class="hl">节省</span>的时间
    </div>
    <div class="data-interpret">
      也就是说，一年省出 243 小时——<br>
      相当于 6 周的工作日
    </div>

    <div class="data-secondary">
      <div class="data-sec-item">
        <div class="data-sec-num">5k+</div>
        <div class="data-sec-label">公众号读者</div>
      </div>
      <div class="data-sec-item">
        <div class="data-sec-num">30+</div>
        <div class="data-sec-label">亲测工具</div>
      </div>
      <div class="data-sec-item">
        <div class="data-sec-num">2yr</div>
        <div class="data-sec-label">持续更新</div>
      </div>
    </div>
  </div>

  <div class="brand-mark">
    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</div>
</body>
</html>
```

---

## 8. 结尾卡 End

**用途**：系列最后一张，收尾 + 关注引导。完成「内容循环」，让读者从「看完了」变成「关注了」。

**适合内容**：
- 总结一句话（不是重新概括全部内容，是留一个印象）
- 明确的关注引导（「关注我，每周更新 AI 工具测评」）
- 品牌标识最大化展示

**文字基调**：不说「感谢观看」，说「如果对你有用，关注起来」。CTA 是邀请，不是命令，但要具体说对方能得到什么。

**❌ 禁忌**：
- 结尾卡还在大量输出信息（这是收尾，不是续集预告）
- 关注引导语太软（「欢迎关注哦」= 没有引导）
- 品牌标识和结尾文字争主角地位（这张卡品牌是主角）

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>End Card</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
<style>
:root {
  --warm-rice:#F5F0E8; --oat:#EBE4D6; --dark-bg:#1A1816; --paper:#FDFAF5;
  --amber:#C87A45; --amber-lt:#D9A87A; --neon-cyan:#00D9FF;
  --text-main:#1F1D1A; --text-sub:#6B6157; --text-mute:#9A9085; --text-dim:#C4BBB0;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#E8E4DC; display:flex; align-items:center; justify-content:center; min-height:100vh; }

.card {
  width:1080px; height:1440px;
  background:var(--dark-bg);
  position:relative; overflow:hidden;
  font-family:'Noto Sans SC',sans-serif;
}

/* 大面积橙色装饰块 — 右上角切入 */
.deco-orange-block {
  position:absolute; top:0; right:0;
  width:360px; height:360px;
  background:var(--amber);
  clip-path:polygon(100% 0, 100% 100%, 0 0);
}

/* 进度点 — 结尾全满 */
.series-dots-full {
  position:absolute; top:80px; left:96px;
  display:flex; gap:8px;
}
.series-dots-full span { font-size:20px; color:var(--amber); }

/* 顶部 eyebrow */
.eyebrow-end {
  position:absolute; top:80px; right:96px;
  font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:300;
  letter-spacing:0.22em; text-transform:uppercase; color:#4A4540;
}

/* 品牌大标识 — 居中展示 */
.brand-center {
  position:absolute;
  top:50%; left:50%;
  transform:translate(-50%, -60%);
  text-align:center;
}

.brand-logo-lg {
  margin:0 auto 36px;
  color:var(--amber);
}

.brand-name-lg {
  font-family:'Smiley Sans Oblique','Noto Sans SC',sans-serif;
  font-size:68px; line-height:1.15;
  color:#FDFAF5; letter-spacing:-0.01em;
  margin-bottom:16px;
}
.brand-name-lg .hl { color:var(--amber); }

.brand-tagline {
  font-family:'Space Grotesk',sans-serif;
  font-size:26px; font-weight:300;
  color:#4A4540; letter-spacing:0.12em;
  text-transform:uppercase;
}

/* 分割线 */
.brand-rule {
  width:60px; height:2px;
  background:var(--amber); margin:36px auto;
}

/* 总结一句话 */
.end-summary {
  position:absolute;
  bottom:260px; left:96px; right:96px;
  text-align:center;
  font-size:36px; font-weight:300; line-height:1.6;
  color:#6B6157;
}
.end-summary strong { color:#FDFAF5; font-weight:400; }

/* 关注引导 CTA */
.end-cta {
  position:absolute;
  bottom:140px; left:96px; right:96px;
  display:flex; justify-content:center;
}
.cta-btn {
  display:inline-flex; align-items:center; gap:16px;
  padding:22px 56px;
  border:1.5px solid var(--amber);
  font-family:'Space Grotesk',sans-serif;
  font-size:28px; font-weight:300;
  color:var(--amber); letter-spacing:0.08em;
  cursor:pointer;
}
.cta-btn:hover { background:var(--amber); color:#1A1816; }

/* 霓虹青点睛 — 结尾最后一个记忆点 */
.neon-accent {
  position:absolute; bottom:80px; left:50%;
  transform:translateX(-50%);
  font-family:'JetBrains Mono',monospace;
  font-size:22px; font-weight:400;
  color:var(--neon-cyan); letter-spacing:0.1em;
  text-shadow:0 0 12px rgba(0,217,255,0.5);
}
</style>
</head>
<body>
<div class="card">
  <div class="deco-orange-block"></div>

  <div class="series-dots-full">
    <span>●</span><span>●</span><span>●</span><span>●</span>
  </div>
  <div class="eyebrow-end">THE END</div>

  <div class="brand-center">
    <svg class="brand-logo-lg" width="96" height="96" viewBox="0 0 32 32" fill="none">
      <path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z"
        stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <path d="M10 15Q12 17 13.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <path d="M22 15Q20 17 18.5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" fill="none"/>
      <circle cx="16" cy="19" r="1.1" fill="currentColor"/>
    </svg>

    <div class="brand-name-lg">
      赛博<span class="hl">小熊猫</span>Loki
    </div>
    <div class="brand-tagline">CYBER PANDA · AI CREATOR</div>
    <div class="brand-rule"></div>
  </div>

  <div class="end-summary">
    <strong>纯文科生用 AI，不追热点，只测真正有用的。</strong><br>
    每周更新，不水字数
  </div>

  <div class="end-cta">
    <div class="cta-btn">关注，不错过下一期</div>
  </div>

  <div class="neon-accent">CYBER PANDA LOKI · SINCE 2024</div>
</div>
</body>
</html>
```

---

## 装饰元素命名索引

| 装饰名 | 用途 | 出现场景 |
|--------|------|---------|
| `series-dots` | 顶部进度点 ●●○○ | 所有系列卡片，串联感 |
| `brand-mark` | 右下角品牌标识 | 所有 8 种卡片，固定位置 |
| `score-bar` | 工具评分进度条 | Review 卡 |
| `score-bar-fill` | 评分条填充 | Review 卡，宽度用内联 style 控制 |
| `step-num` | 圆形步骤序号 | Steps 卡 |
| `step-connector` | 步骤间连接线（虚线感） | Steps 卡 |
| `compare-divider` | 对比列中间分隔线 | Compare 卡 |
| `deco-quote` | 大号装饰引号（背景级） | Quote 卡 |
| `quote-vline` | 金句左侧装饰竖线 | Quote 卡 |
| `neon-rule` / `neon-dot` / `neon-accent` | 霓虹青点睛元素 | 深底卡片各 1 处，不重复 |
| `cover-stripe` | 封面右侧品牌橙竖条 | Cover 卡 |
| `deco-orange-block` | 结尾卡右上角橙色切角 | End 卡 |

---

## 全局 ❌ 禁止（本场景）

- ❌ 蓝紫渐变（`#6C63FF`、`#a855f7`）、Glassmorphism、Neon 荧光色
- ❌ 纯黑 `#000000` 或纯白 `#FFFFFF` 大面积背景
- ❌ 科技蓝 + 银灰（AI 工具通用配色，与品牌气质相反）
- ❌ 霓虹青 `#00D9FF` 每张卡超过一处
- ❌ 每条列表超过一行（列表卡规则）
- ❌ 对比卡没有结论行
- ❌ 评分全高（Review 卡的测评诚信规则）
- ❌ 步骤卡没有步骤间视觉连接
- ❌ 金句卡字号小于 60px
- ❌ 品牌标识移离右下角位置
- ❌ 深底卡片超过系列 2 张（深底稀缺性原则）
- ❌ 同一张卡出现超过 3 处品牌橙
- ❌ Emoji 堆砌（全系列每张卡 ≤ 1 个 emoji）

---

*场景文件 · 赛博小熊猫Loki 设计系统 · 最后更新 2026-05-27*
