# 小红书版式系统 · V2（三段式填充版）

> V2核心改进：三段式垂直分配 + IP视觉主体 + 装饰元素填空 + Horror Vacui
> 每种版式严格按 顶25%→中50%→底25% 分配，禁止下半部空白
> 完整CSS见 `templates/carousel-v2.html`

---

## 通用装饰元素（所有版式可用）

```html
<!-- 噪点纹理 -->
<div class="noise"></div>

<!-- 进度条 -->
<div class="progress-bar"><div class="bar" style="width:10%"></div></div>

<!-- 光晕 -->
<div class="glow"></div>  或  <div class="qt-glow"></div>  或  <div class="ec-glow"></div>

<!-- 背景大字水印（得意黑装饰体） -->
<div class="watermark" style="top:-20px;left:-30px;font-size:120px;">ODYSSEY</div>

<!-- 装饰圆点 -->
<div class="deco-dot" style="top:50px;left:40px;width:8px;height:8px;background:var(--accent);opacity:0.4;"></div>

<!-- 装饰圆环 -->
<div class="deco-ring" style="top:30px;right:30px;width:60px;height:60px;"></div>

<!-- 装饰方块（可旋转） -->
<div class="deco-square" style="bottom:190px;right:30px;width:14px;height:14px;transform:rotate(45deg);"></div>

<!-- 边缘重复文字 -->
<div class="edge-text" style="bottom:6px;left:50%;transform:translateX(-50%);">ODYSSEY × AI · 2025 · LOKI · ODYSSEY × AI</div>

<!-- 四角装饰（金句页用） -->
<div class="qt-corners">
  <div class="qt-corner tl"></div>
  <div class="qt-corner tr"></div>
  <div class="qt-corner bl"></div>
  <div class="qt-corner br"></div>
</div>

<!-- IP圆形大图（视觉主体，占30-40%） -->
<img class="ip-hero" style="width:240px;height:240px;" src="ip-library/loki-thinking.png" alt="Loki">
```

---

## 版式 X01 · 封面 · 居中大字（三段式）

**结构**：eyebrow+title顶 → IP圆形大图中 → sub+meta底

```html
<div class="card cover">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:10%"></div></div>
  <div class="glow"></div>
  <!-- 装饰 -->
  <div class="watermark" style="top:-20px;left:-30px;font-size:120px;">ODYSSEY</div>
  <div class="watermark" style="bottom:-30px;right:-20px;font-size:100px;">AI×ODYSSEY</div>
  <div class="deco-ring" style="top:30px;right:30px;width:60px;height:60px;"></div>
  <div class="deco-dot" style="top:50px;left:40px;width:8px;height:8px;background:var(--accent);opacity:0.4;"></div>
  <div class="edge-text" style="bottom:6px;left:50%;transform:translateX(-50%);">ODYSSEY × AI · 2025 · LOKI</div>

  <!-- 顶部 25% -->
  <div class="cv-top">
    <div class="cv-eyebrow">ODYSSEY × AI</div>
    <h2 class="cv-title">AI到底在<br><span class="hl">缩短</span>还是<span class="hl">拉长</span><br>你的迷茫</h2>
  </div>
  <!-- 中部 50% — IP视觉主体 -->
  <div class="cv-mid">
    <img class="ip-hero cv-ip" src="ip-library/loki-thinking.png" alt="Loki">
  </div>
  <!-- 底部 25% -->
  <div class="cv-bot">
    <div class="cv-bot-deco-top">
      <div class="cv-bot-deco-line"></div>
      <div class="cv-bot-deco-dot"></div>
      <div class="cv-bot-deco-label">两面观察</div>
      <div class="cv-bot-deco-dot"></div>
      <div class="cv-bot-deco-line"></div>
    </div>
    <p class="cv-sub">一个文科生的两面观察</p>
    <div class="cv-meta">
      <div class="cv-meta-item"><span class="cv-meta-num">20-35</span><span class="cv-meta-label">岁</span></div>
      <div class="cv-meta-item"><span class="cv-meta-num">试错</span><span class="cv-meta-label">成本</span></div>
      <div class="cv-meta-item"><span class="cv-meta-num">两面性</span><span class="cv-meta-label">观察</span></div>
    </div>
  </div>
  <div class="brand-mark"><svg><use href="#panda"/></svg><span class="brand-text">赛博小熊猫Loki</span></div>
</div>
```

---

## 版式 X02 · 要点列表（三段式）

**结构**：标题色块顶 → 3卡片space-evenly中 → 分隔线+脚注底

```html
<div class="card keylist">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:25%"></div></div>
  <div class="watermark" style="top:60px;right:-40px;font-size:110px;">ODYSSEY</div>
  <div class="deco-ring" style="bottom:50px;left:30px;width:40px;height:40px;"></div>
  <div class="edge-text" style="top:6px;left:50%;transform:translateX(-50%);">FEATURE · 3 · ODYSSEY PERIOD</div>

  <div class="kl-top">
    <div class="kl-eyebrow">什么是奥德赛时期</div>
    <h2 class="kl-title"><span class="hl">3个</span>特征</h2>
  </div>
  <div class="kl-mid">
    <div class="kl-item">
      <span class="kl-item-num">01</span>
      <div class="kl-item-content">
        <h4 class="kl-item-title">标题</h4>
        <p class="kl-item-desc">描述</p>
      </div>
    </div>
    <!-- 重复2-3个 -->
  </div>
  <div class="kl-bot">
    <div class="kl-divider"></div>
    <div class="kl-footnote">脚注 · <span class="hl">关键词</span></div>
    <div class="kl-divider"></div>
  </div>
  <div class="brand-mark">...</div>
</div>
```

---

## 版式 X03 · 金句（三段式）

**结构**：引号顶 → 金句大字中（+背景水印+四角装饰）→ 出处+装饰底

```html
<div class="card quote">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:40%"></div></div>
  <div class="qt-glow"></div>
  <div class="watermark" style="top:50%;left:50%;transform:translate(-50%,-50%) rotate(-8deg);font-size:140px;">ODYSSEY</div>
  <div class="qt-corners">
    <div class="qt-corner tl"></div><div class="qt-corner tr"></div>
    <div class="qt-corner bl"></div><div class="qt-corner br"></div>
  </div>
  <div class="deco-dot" style="..."></div>
  <div class="deco-square" style="...;transform:rotate(45deg);"></div>

  <div class="qt-top"><div class="qt-mark">"</div></div>
  <div class="qt-mid">
    <div class="qt-text">金句内容<br><span class="hl">关键词</span></div>
  </div>
  <div class="qt-bot">
    <div class="qt-cite">
      <div class="qt-cite-line"></div>
      <span class="qt-cite-text">赛博小熊猫Loki</span>
    </div>
  </div>
  <div class="brand-mark">...</div>
</div>
```

---

## 版式 X04 · 杂志导读（三段式）

**结构**：标题色块顶（border-bottom accent）→ 双栏正文+竖线分隔中 → 总结框底

```html
<div class="card magazine">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:55%"></div></div>
  <div class="watermark" style="...">MAGAZINE</div>

  <div class="mg-top">
    <div class="mg-eyebrow">eyebrow</div>
    <h2 class="mg-title">标题<span class="hl">高亮</span></h2>
  </div>
  <div class="mg-mid">
    <div class="mg-col">
      <h3 class="mg-subhead">左栏标题</h3>
      <p class="mg-para">正文 <span class="hl">高亮</span></p>
    </div>
    <div class="mg-divider"></div>
    <div class="mg-col">
      <h3 class="mg-subhead">右栏标题</h3>
      <p class="mg-para">正文 <span class="hl">高亮</span></p>
    </div>
  </div>
  <div class="mg-bot">
    <div class="mg-summary">
      <div class="mg-summary-label">TAKEAWAY</div>
      <p class="mg-summary-text">总结 <span class="hl">高亮</span></p>
    </div>
  </div>
  <div class="brand-mark">...</div>
</div>
```

---

## 版式 X05 · 引用插入（三段式）

**结构**：标题色块顶 → 正文+pullquote中 → 末段+标签底

```html
<div class="card pullquote">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:70%"></div></div>
  <div class="pq-texture"></div>

  <div class="pq-top">
    <div class="pq-eyebrow">eyebrow</div>
    <h2 class="pq-title">标题<span class="hl">高亮</span></h2>
  </div>
  <div class="pq-mid">
    <p class="pq-para">正文段落</p>
    <div class="pq-pullquote">
      <p class="pq-pullquote-text">引用文字</p>
      <span class="pq-pullquote-cite">— 出处</span>
    </div>
    <p class="pq-para">正文段落 <span class="hl">高亮</span></p>
  </div>
  <div class="pq-bot">
    <p class="pq-bot-text">末段 <span class="hl">高亮</span></p>
    <div class="pq-tag">TAG</div>
  </div>
  <div class="brand-mark">...</div>
</div>
```

---

## 版式 X06 · 卡片拼接（三段式）

**结构**：标题色块顶 → 3满版色块横条中下部（bg/bg2/bg交替）

```html
<div class="card cardstack">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:85%"></div></div>

  <div class="cs-top">
    <div class="cs-eyebrow">eyebrow</div>
    <h2 class="cs-title">标题<span class="hl">高亮</span></h2>
  </div>
  <div class="cs-body">
    <div class="cs-block b1">
      <div class="cs-block-header"><span class="cs-block-num">01</span><span class="cs-block-title">标题</span></div>
      <p class="cs-block-text">描述 <span class="hl">高亮</span></p>
      <div class="cs-deco"><div class="cs-deco-dot"></div><div class="cs-deco-dot"></div><div class="cs-deco-dot"></div></div>
    </div>
    <div class="cs-block b2"><!-- 同上 --></div>
    <div class="cs-block b3"><!-- 同上 --></div>
  </div>
  <div class="brand-mark">...</div>
</div>
```

---

## 版式 X07 · 结尾CTA（三段式）

**结构**：eyebrow顶 → CTA+IP圆形大图中 → 联系方式底

```html
<div class="card endcard">
  <div class="noise"></div>
  <div class="progress-bar"><div class="bar" style="width:100%"></div></div>
  <div class="ec-glow"></div>
  <div class="watermark" style="...">END</div>

  <div class="ec-top">
    <div class="ec-eyebrow">END · 关注</div>
  </div>
  <div class="ec-mid">
    <h2 class="ec-cta"><span class="hl">关注我</span><br>每周AI实测</h2>
    <img class="ip-hero ec-ip" src="ip-library/loki-hero-pose.png" alt="Loki">
  </div>
  <div class="ec-bot">
    <p class="ec-sub">副标题</p>
    <div class="ec-contacts">
      <p class="ec-contact">公众号 · <span class="hl">赛博小熊猫Loki</span></p>
      <p class="ec-contact">网站 · <span class="hl">hiloki.ai</span></p>
    </div>
  </div>
  <div class="brand-mark">...</div>
</div>
```

---

## 三段式CSS核心（所有版式共用）

```css
/* 三段式通用 */
.cover,.keylist,.quote,.magazine,.pullquote,.cardstack,.endcard{
  display:flex;flex-direction:column;padding:0;
}
/* 顶部 25% — 色块背景+标题 */
.cv-top,.kl-top,.qt-top,.mg-top,.pq-top,.cs-top,.ec-top{
  width:100%;height:160-180px;display:flex;flex-direction:column;align-items:center;justify-content:center;
  position:relative;z-index:2;background:var(--bg2);
}
/* 中部 50% — 主内容/IP/正文 */
.cv-mid,.kl-mid,.qt-mid,.mg-mid,.pq-mid,.cs-body,.ec-mid{
  flex:1;position:relative;z-index:2;display:flex;flex-direction:column;
  justify-content:center;align-items:center;
}
/* 底部 25% — 辅助信息+装饰 */
.cv-bot,.kl-bot,.qt-bot,.mg-bot,.pq-bot,.ec-bot{
  width:100%;height:150-180px;display:flex;flex-direction:column;align-items:center;justify-content:center;
  position:relative;z-index:2;background:var(--bg2);border-top:1px solid var(--border);
}
```

---

## 版式替换指南（更新）

| 不满意的版式 | 可替换为 |
|-------------|---------|
| 要点列表(X02) | 杂志导读(X04) / 卡片拼接(X06) |
| 金句(X03) | 金句(X07) — 同类不同内容 |
| 杂志导读(X04) | 引用插入(X05) |
| 引用插入(X05) | 杂志导读(X04) / 卡片拼接(X06) |
| 卡片拼接(X06) | 要点列表(X02) |
