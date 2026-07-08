# 版式系统 · 12 种完整 HTML 代码块

> 每种版式都是独立的 `<section>` 代码块，可直接粘贴到模板的 `<!-- SLIDES_HERE -->` 位置。
> 所有 class 都在 `templates/deck.html` 的 `<style>` 里有定义。
> 配色通过 CSS 变量自动应用，只需替换 `:root` 中的变量值。

---

## 通用结构

每个 slide 的基本结构：

```html
<section class="slide s-cover" data-layout="cover">
  <div class="noise"></div>
  <!-- 内容 -->
  <span class="slide-page">01 / 10</span>
  <div class="brand-mark on-dark">
    <svg viewBox="0 0 32 32" fill="none"><path d="M6 14C6 9 10 6 16 6C22 6 26 9 26 14L26 19C26 24 22 27 16 27C10 27 6 24 6 19Z" stroke="currentColor" stroke-width="1.8" fill="none"/><circle cx="8" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/><circle cx="24" cy="9" r="2.4" stroke="currentColor" stroke-width="1.8" fill="none"/><circle cx="16" cy="19" r="1.1" fill="currentColor"/></svg>
    <span class="brand-text">赛博小熊猫Loki</span>
  </div>
</section>
```

- `on-dark` → 深底页面用（标识半透明白色）
- `on-light` → 浅底页面用（标识半透明黑色）
- `data-layout` → 标注版式类型，便于检查

---

## 版式 01 · 封面 · 居中大字

**用途**：第 1 页，主题宣告
**要素**：居中标题 + 副标 + 底部meta数据 + 光晕

```html
<section class="slide s-cover" data-layout="cover">
  <div class="noise"></div>
  <div class="sv-glow"></div>
  <div class="sv-eyebrow">AI TOOLS · KEYNOTE</div>
  <h1 class="sv-title">5个AI工具<br>让我<span class="hl">效率</span>翻倍</h1>
  <p class="sv-sub">一个文科生的亲测报告。不水字数，只测真正有用的。</p>
  <div class="sv-meta">
    <div class="sv-meta-item"><span class="sv-meta-num">87</span><span class="sv-meta-label">实测工具</span></div>
    <div class="sv-meta-item"><span class="sv-meta-num">5k</span><span class="sv-meta-label">读者</span></div>
    <div class="sv-meta-item"><span class="sv-meta-num">2yr</span><span class="sv-meta-label">更新</span></div>
  </div>
  <span class="slide-page">01 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

**IP形象插入位**：右侧 `position:absolute;right:80px;bottom:80px;width:400px`
使用：`<div class="ip-wrap ip-circle ip-cover"><img src="ip-library/loki-original-3d.png" alt="Loki"></div>`（与 deck.html 一致）

---

## 版式 02 · 章节过渡 · 大序号

**用途**：每幕开场，制造翻页节奏感
**要素**：巨型序号（120px半透明）+ 章节标题

```html
<section class="slide s-chapter" data-layout="chapter">
  <div class="noise"></div>
  <div class="ch-num">01</div>
  <div class="ch-eyebrow">CHAPTER ONE</div>
  <h1 class="ch-title">为什么<br>文科生更适合用AI</h1>
  <span class="slide-page">02 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 03 · 要点列表 · 编号卡片

**用途**：核心观点，3-5个要点
**要素**：标题 + 竖排编号卡片（每项标题+描述），左侧色条

```html
<section class="slide s-keylist" data-layout="keylist">
  <div class="noise"></div>
  <div class="kl-header">
    <div class="kl-eyebrow">KEY POINTS · 核心观点</div>
    <h2 class="kl-title">文科生的<span class="hl">3个优势</span></h2>
  </div>
  <div class="kl-items">
    <div class="kl-item">
      <span class="kl-item-num">01</span>
      <div class="kl-item-content">
        <h4 class="kl-item-title">提问能力</h4>
        <p class="kl-item-desc">文科训练的就是把模糊感觉变成具体问题的能力</p>
      </div>
    </div>
    <div class="kl-item">
      <span class="kl-item-num">02</span>
      <div class="kl-item-content">
        <h4 class="kl-item-title">表达精准</h4>
        <p class="kl-item-desc">你问得越精准，AI给得越有用</p>
      </div>
    </div>
    <div class="kl-item">
      <span class="kl-item-num">03</span>
      <div class="kl-item-content">
        <h4 class="kl-item-title">优化表达而非参数</h4>
        <p class="kl-item-desc">模型帮你跑参数了，你需要跑的是表达</p>
      </div>
    </div>
  </div>
  <span class="slide-page">03 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 04 · 图文混排 · 上图下文

**用途**：产品展示、工具评测
**要素**：上半图片预留位 + 下半标题+正文+meta

```html
<section class="slide s-imgtext" data-layout="imgtext">
  <div class="noise"></div>
  <div class="it-img">
    <span class="it-imgtag">DEMO</span>
    <!-- 可替换为IP形象：<img src="ip-library/loki-excited-laptop.png" style="width:100%;height:100%;object-fit:cover;"> -->
  </div>
  <div class="it-content">
    <div class="it-eyebrow">TOOL DEMO · 工具演示</div>
    <h2 class="it-title">Claude的<span class="hl">长文写作</span>界面</h2>
    <p class="it-body">实际输出3000字报告。<span class="hl">理解力全场最好</span>，改稿指令精准执行。<span class="mute">适合长文写作场景。</span></p>
    <div class="it-meta">
      <span class="it-source">claude.ai · 2026.05实测</span>
      <span class="it-source">04 / 10</span>
    </div>
  </div>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 05 · 数据大字 · 满版数字

**用途**：抛硬数据，核心指标
**要素**：140px大数字 + 标签 + 解读 + 底部3个辅助数据

```html
<section class="slide s-data" data-layout="data">
  <div class="noise"></div>
  <div class="dt-glow"></div>
  <div class="dt-top">
    <span class="dt-eyebrow">DATA · 实测数据</span>
    <div class="dt-neon"></div>
  </div>
  <div class="dt-main">
    <div class="dt-num">73%</div>
    <h2 class="dt-label">AI工具下载后30天内<br><span class="hl">彻底弃用</span></h2>
    <p class="dt-interp">挑工具的成本，其实在使用之后。</p>
  </div>
  <div class="dt-aux">
    <div class="dt-aux-item"><span class="dt-aux-num">87</span><span class="dt-aux-label">实测工具</span></div>
    <div class="dt-aux-item"><span class="dt-aux-num">5</span><span class="dt-aux-label">活过30天</span></div>
    <div class="dt-aux-item"><span class="dt-aux-num">2yr</span><span class="dt-aux-label">持续更新</span></div>
  </div>
  <span class="slide-page">05 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 06 · 金句 · 居中引用

**用途**：情绪锚点，核心金句
**要素**：大引号 + 居中大字 + 出处 + 光晕

```html
<section class="slide s-quote" data-layout="quote">
  <div class="noise"></div>
  <div class="qt-glow"></div>
  <div class="qt-mark">"</div>
  <div class="qt-text">AI的瓶颈<br>不是<span class="hl">技术</span>，<br>是你的<br><span class="hl">问题意识</span></div>
  <div class="qt-cite">
    <div class="qt-cite-line"></div>
    <span class="qt-cite-text">赛博小熊猫Loki · 2026</span>
  </div>
  <span class="slide-page">06 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 07 · 对比 · 左右分栏

**用途**：A vs B 优劣分析
**要素**：左右等分（before/after）+ 徽章 + 要点列表 + verdict条

```html
<section class="slide s-compare" data-layout="compare">
  <div class="noise"></div>
  <div class="cp-header">
    <div class="cp-eyebrow">HEAD TO HEAD</div>
    <h2 class="cp-title">ChatGPT vs <span class="hl">Claude</span></h2>
  </div>
  <div class="cp-body">
    <div class="cp-col before">
      <span class="cp-badge">OLD</span>
      <h4 class="cp-col-name">ChatGPT</h4>
      <div class="cp-items">
        <div class="cp-item"><span class="cp-check">✗</span>长文跑题</div>
        <div class="cp-item"><span class="cp-check">✗</span>改稿打折</div>
        <div class="cp-item"><span class="cp-check">✓</span>可联网</div>
      </div>
    </div>
    <div class="cp-col after">
      <span class="cp-badge">BEST</span>
      <h4 class="cp-col-name">Claude ✓</h4>
      <div class="cp-items">
        <div class="cp-item"><span class="cp-check">✓</span>理解力最好</div>
        <div class="cp-item"><span class="cp-check">✓</span>改稿精准</div>
        <div class="cp-item"><span class="cp-check">✓</span>长文不丢逻辑</div>
      </div>
    </div>
  </div>
  <div class="cp-verdict">→ 文科写作首选Claude</div>
  <span class="slide-page">07 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 08 · 步骤 · 竖向时间线

**用途**：教程、工作流、操作步骤
**要素**：圆形序号 + 连接线 + 标题 + 描述

```html
<section class="slide s-steps" data-layout="steps">
  <div class="noise"></div>
  <div class="st-header">
    <div class="st-eyebrow">WORKFLOW · 3 STEPS</div>
    <h2 class="st-title">用AI写出<span class="hl">有用</span>文章</h2>
  </div>
  <div class="st-body">
    <div class="st-step">
      <div class="st-step-left"><div class="st-step-num">1</div><div class="st-step-conn"></div></div>
      <div class="st-step-content"><h4 class="st-step-title">拆解读者问题</h4><p class="st-step-desc">问AI：目标读者遇到X问题时，会搜索哪5个关键词？</p></div>
    </div>
    <div class="st-step">
      <div class="st-step-left"><div class="st-step-num">2</div><div class="st-step-conn"></div></div>
      <div class="st-step-content"><h4 class="st-step-title">搭结构，不要直接写</h4><p class="st-step-desc">先出提纲，你改逻辑，再逐段生成</p></div>
    </div>
    <div class="st-step">
      <div class="st-step-left"><div class="st-step-num">3</div></div>
      <div class="st-step-content"><h4 class="st-step-title">加入亲测细节</h4><p class="st-step-desc">至少1个真实场景。AI写不出的部分是你的护城河</p></div>
    </div>
  </div>
  <span class="slide-page">08 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 09 · 网格选择 · 多卡片

**用途**：推荐、合集、多选项展示
**要素**：2×3网格 + 每卡片序号+标题+描述+标签 + featured高亮

```html
<section class="slide s-grid" data-layout="grid">
  <div class="noise"></div>
  <div class="gr-header">
    <div class="gr-eyebrow">PICK YOUR FIGHT</div>
    <h2 class="gr-title">4个场景 4个<span class="hl">最佳工具</span></h2>
  </div>
  <div class="gr-body">
    <div class="gr-card">
      <span class="gr-card-num">01</span>
      <h4 class="gr-card-title">长文写作</h4>
      <p class="gr-card-desc">理解力最好，改稿精准</p>
      <span class="gr-card-tag">Claude</span>
    </div>
    <div class="gr-card featured">
      <span class="gr-card-num">02</span>
      <h4 class="gr-card-title">搜索研究</h4>
      <p class="gr-card-desc">信息可溯源，替代百度</p>
      <span class="gr-card-tag">Perplexity</span>
    </div>
    <!-- 更多卡片... -->
  </div>
  <span class="slide-page">09 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 10 · 结尾 · CTA引导

**用途**：收尾，关注引导
**要素**：居中CTA + 副标 + 联系方式 + 光晕

```html
<section class="slide s-end" data-layout="end">
  <div class="noise"></div>
  <div class="ec-glow"></div>
  <div class="ec-eyebrow">END · 关注引导</div>
  <h1 class="ec-cta"><span class="hl">关注我</span><br>每周AI实测</h1>
  <p class="ec-sub">不水字数，只测真正有用的。<br>一个文科生的AI工具箱。</p>
  <div class="ec-contacts">
    <span class="ec-contact">公众号 · <span class="hl">赛博小熊猫Loki</span></span>
    <span class="ec-contact">网站 · <span class="hl">hiloki.ai</span></span>
  </div>
  <span class="slide-page">10 / 10</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

**IP形象插入位**：中心位置 `position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)`
使用：`<div class="ip-wrap ip-circle ip-end-left"><img src="ip-library/loki-celebrating.png" alt="Loki"></div>`（与 deck.html 一致）

---

## 版式 11 · 杂志导读 · 双栏正文

**用途**：深度内容，大量文字
**要素**：标题 + 双栏正文（各带小标题+多段文字）+ 底部总结框

```html
<section class="slide s-magazine" data-layout="magazine">
  <div class="noise"></div>
  <div class="mz-header">
    <div class="mz-eyebrow">DEEP DIVE · 深度</div>
    <h2 class="mz-title">为什么<span class="hl">文科生</span>更该用AI</h2>
  </div>
  <div class="mz-body">
    <div class="mz-col">
      <h4 class="mz-col-title">提问能力的训练</h4>
      <p class="mz-text">文科教育最核心的训练不是写文章，而是提问。你需要从一段模糊的感受中，提取出一个精确的问题。这恰恰是使用AI最需要的能力。<span class="hl">AI不在乎你的答案，它在等你的问题。</span></p>
      <p class="mz-text">很多人觉得AI不好用，不是因为AI不行，是因为他们问得太模糊。"帮我写篇文章"和"帮我写一篇给30岁职场人看的、关于AI工具选择的2000字文章，语气要像朋友聊天"——后者的产出质量是前者的10倍。</p>
    </div>
    <div class="mz-col">
      <h4 class="mz-col-title">表达的精准度</h4>
      <p class="mz-text">文科生对语言的敏感度是天然优势。你知道一个词的细微差别，你知道什么语气让人舒服，你知道怎样的节奏让人读下去。<span class="hl">这些"软技能"在AI时代变成了"硬实力"。</span></p>
      <p class="mz-text">理科生可能在参数调优上更强，但文科生在表达优化上更强。而当前的AI，最缺的不是算力，是表达。</p>
    </div>
  </div>
  <div class="mz-summary">
    <span class="mz-summary-label">TAKEAWAY</span>
    <p class="mz-summary-text">文科生的竞争力 = 提问能力 × 表达精准 × 审美判断</p>
  </div>
  <span class="slide-page">11 / 12</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 版式 12 · 引用插入 · 长文+Pull Quote

**用途**：叙事，长文+引用打断节奏
**要素**：长段落 + 中间引用框（border-left色条）+ 衬线italic引用文

```html
<section class="slide s-pullquote" data-layout="pullquote">
  <div class="noise"></div>
  <div class="pq-header">
    <div class="pq-eyebrow">NARRATIVE · 叙事</div>
    <h2 class="pq-title">关于<span class="hl">写作</span>这件事</h2>
  </div>
  <div class="pq-body">
    <p class="pq-text">写作从来不是把想好的东西写下来。写作是边写边想的过程。你以为你在记录思考，其实你在<span class="hl">通过写字来思考</span>。不开个头，你永远不知道自己想说什么。</p>
    <div class="pq-quote-box">
      <p class="pq-quote-text">"你不需要准备好了再写。你需要开始写了，才会准备好。"</p>
      <span class="pq-quote-cite">— 一个写了5年公众号的文科生</span>
    </div>
    <p class="pq-text">这个道理我用了三年才真正理解。每次坐在电脑前等灵感，等到的都是焦虑。反而是随手开始写的那一刻，文字自己找到了方向。<span class="hl">先写，再想。</span>这就是全部的秘密。</p>
  </div>
  <span class="slide-page">12 / 12</span>
  <div class="brand-mark on-dark"><!-- SVG --></div>
</section>
```

---

## 主题节奏规划

**强制规则**：
- 每页 section 必须有明确的版式类型（`data-layout`）
- 连续 3 页以上同类型版式 = 视觉疲劳，不允许
- 8 页以上必须有 ≥1 个封面 + ≥1 个章节过渡 + ≥1 个结尾
- 整个 deck 不能只有精简版式，大文字量内容必须用 11/12 版式
- 每 3-4 页插入 1 个节奏页（章节过渡/金句/数据大字）

**生成后自检**：
```bash
grep 'data-layout=' index.html
```
列出所有版式类型，人工确认节奏合理。

---

## 版式替换指南

不满意某个版式时，换同类型的另一个：

| 不满意的版式 | 可替换为 | 理由 |
|-------------|---------|------|
| 要点列表(03) | 杂志导读(11) / 网格选择(09) | 同样承载多要点，排版不同 |
| 图文混排(04) | 引用插入(12) | 同样有图文，叙事感更强 |
| 数据大字(05) | 要点列表(03) | 数据可以拆成要点 |
| 金句(06) | 章节过渡(02) | 同样是节奏页 |
| 步骤(08) | 要点列表(03) | 同样是序列信息 |
| 网格选择(09) | 要点列表(03) | 同样是多选项 |
| 杂志导读(11) | 引用插入(12) | 同样是大文字量 |
