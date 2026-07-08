# 场景一：个人主页 · scene-landing.md
> 适用：个人 Landing Page、个人品牌页、个人介绍页
> 对应模板：`templates/landing-page.html`
> 核心情绪：「这是一个值得关注的人」

---

## 区块清单（按顺序）

| # | 区块 | 底色 | 必选/可选 |
|---|------|------|----------|
| 1 | Hero：标题 + 副文字 + IP 形象 | `--dark2` 深底 | 必选 |
| 2 | Statement：一句核心主张 | `--warm` 浅底 | 必选 |
| 3 | Works：作品/项目展示 | `--dark` 深底 | 必选 |
| 4 | Stats：数字成就 | `--warm` 浅底 | 推荐 |
| 5 | About：关于我 | `--dark2` 深底 | 推荐 |
| 6 | Contact/Footer：二维码 + 链接 | `--dark2` 深底 | 必选 |

**深浅节奏：深→浅→深→浅→深→深（Footer）**

---

## 组件 01 · Hero

```html
<section style="min-height:100vh;display:grid;grid-template-columns:1fr 440px;
  align-items:end;padding:0 64px 96px;background:var(--dark2);position:relative;overflow:hidden;">
  <!-- 背景光晕 -->
  <div style="position:absolute;right:-60px;bottom:-80px;width:560px;height:560px;
    background:radial-gradient(circle,rgba(0,217,255,.1) 0%,transparent 65%);pointer-events:none;"></div>
  <!-- 左侧文字 -->
  <div>
    <div style="font-family:var(--font-l);font-size:11px;font-weight:300;letter-spacing:.22em;
      text-transform:uppercase;color:rgba(0,217,255,.7);margin-bottom:28px;">
      Cyber Panda · AI Creator · Beijing
    </div>
    <h1 style="font-family:var(--font-d);font-size:clamp(54px,7vw,104px);line-height:1.0;
      letter-spacing:-.03em;color:var(--paper);margin-bottom:32px;">
      主标题<br>第二行<br><span style="color:var(--amber);">关键词</span>
    </h1>
    <p style="font-size:14px;font-weight:100;color:var(--text-muted);line-height:1.9;
      max-width:440px;margin-bottom:48px;">副标题文字，简洁说明身份和做的事。</p>
    <a href="#works" style="display:inline-flex;align-items:center;gap:12px;
      font-family:var(--font-l);font-size:12px;font-weight:400;letter-spacing:.14em;
      text-transform:uppercase;color:var(--paper);border:1px solid var(--dark-border);
      padding:12px 24px;text-decoration:none;transition:border-color .2s,color .2s;">
      看我做了什么
    </a>
  </div>
  <!-- 右侧 IP 形象 -->
  <div style="display:flex;align-items:flex-end;justify-content:center;">
    <img src="ip.jpg" style="width:100%;max-width:440px;mix-blend-mode:lighten;
      filter:contrast(1.05) brightness(.95);border-radius:20px;">
  </div>
</section>
```

**规则：**
- 标题中 1-2 个关键词用 `color:var(--amber)` 点橙，其余保持白色
- IP 形象用 `mix-blend-mode:lighten` 融进深底（消除白色背景）
- 右下角加霓虹青 `#00D9FF` 光晕（IP 胸前 LOKI 的呼应）

---

## 组件 02 · Statement

```html
<section style="background:var(--warm);padding:120px 64px;">
  <div style="max-width:960px;border-top:1px solid var(--oat);padding-top:64px;">
    <div style="font-family:var(--font-l);font-size:10px;font-weight:400;letter-spacing:.22em;
      text-transform:uppercase;color:var(--text-muted);margin-bottom:32px;">Belief</div>
    <p style="font-family:var(--font-d);font-size:clamp(28px,3.8vw,52px);
      line-height:1.25;letter-spacing:-.02em;color:var(--dark);">
      一句话核心主张，<span style="color:var(--amber);">关键词</span>点橙，<br>
      可以换行，字要大，留白要大。
    </p>
  </div>
</section>
```

**规则：** 不超过 3 行，不放列表，这里只说一件最重要的事

---

## 组件 03 · Works 杂志行

```html
<!-- 一行：左图右文 -->
<div style="display:grid;grid-template-columns:1fr 1fr;border-bottom:1px solid var(--dark-border);min-height:440px;">
  <div style="overflow:hidden;position:relative;background:#111;">
    <div style="position:absolute;top:24px;left:24px;font-family:var(--font-l);
      font-size:10px;font-weight:300;letter-spacing:.14em;color:rgba(253,250,245,.2);">01</div>
    <img src="screenshots/xxx.png" style="width:100%;height:100%;object-fit:cover;
      object-position:top left;filter:saturate(.8) brightness(.85);transition:transform .7s,filter .4s;">
  </div>
  <div style="padding:56px 64px;display:flex;flex-direction:column;justify-content:center;
    border-left:1px solid var(--dark-border);">
    <div style="display:inline-block;font-family:var(--font-l);font-size:10px;font-weight:400;
      letter-spacing:.16em;text-transform:uppercase;color:var(--amber);
      border:1px solid rgba(200,122,69,.35);padding:4px 10px;margin-bottom:28px;width:fit-content;">
      Tool · Open
    </div>
    <h3 style="font-family:var(--font-d);font-size:clamp(22px,2.6vw,36px);
      line-height:1.15;letter-spacing:-.02em;color:var(--paper);margin-bottom:18px;">
      项目名称<br>第二行
    </h3>
    <p style="font-size:13px;font-weight:300;color:var(--text-muted);line-height:1.9;
      max-width:360px;margin-bottom:36px;">一两句描述这个项目是什么，解决什么问题。</p>
    <a href="#" style="font-family:var(--font-l);font-size:11px;font-weight:400;
      letter-spacing:.12em;text-transform:uppercase;color:rgba(58,52,45,.8);text-decoration:none;">
      链接地址 →
    </a>
  </div>
</div>

<!-- 下一行：右图左文（flip） -->
<div style="display:grid;grid-template-columns:1fr 1fr;direction:rtl;border-bottom:1px solid var(--dark-border);min-height:440px;">
  <div style="direction:ltr;overflow:hidden;position:relative;background:#111;">
    <!-- 图片同上 -->
  </div>
  <div style="direction:ltr;padding:56px 64px;display:flex;flex-direction:column;justify-content:center;
    border-right:1px solid var(--dark-border);">
    <!-- 信息同上 -->
  </div>
</div>
```

**规则：**
- 奇数行：左图右文；偶数行：右图左文（`direction:rtl` + 子元素 `direction:ltr`）
- 图片用真实产品截图，`object-fit:cover`，hover 时 `scale(1.03)` + 去滤镜
- 标签颜色：自己做的工具用 amber，开源用 smoke，在做中用 muted

---

## 组件 04 · Stats 数字大字报

```html
<section style="background:var(--warm);border-top:1px solid var(--oat);">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);
    border-left:1px solid var(--oat);border-top:1px solid var(--oat);">
    <!-- 一格 -->
    <div style="padding:72px 56px 64px;border-right:1px solid var(--oat);border-bottom:1px solid var(--oat);">
      <div style="font-family:var(--font-l);font-size:10px;font-weight:400;letter-spacing:.2em;
        text-transform:uppercase;color:var(--text-muted);margin-bottom:24px;">指标名称</div>
      <div style="font-family:var(--font-l);font-size:clamp(64px,7vw,96px);font-weight:200;
        letter-spacing:-.05em;line-height:1;color:var(--dark);margin-bottom:16px;">
        5000<sup style="font-size:.32em;font-weight:400;color:var(--amber);vertical-align:super;">+</sup>
      </div>
      <div style="font-size:13px;font-weight:300;color:var(--text-sub);line-height:1.75;">补充说明</div>
    </div>
    <!-- 重复 3 次 -->
  </div>
</section>
```

**规则：**
- 数字必须 `font-weight:200`（超细），这是品牌辨识度来源
- `sup` 单位用 amber 色
- 网格线用 `var(--oat)` 浅色，不是卡片阴影

---

## 组件 05 · About 左数据右文字

```html
<section style="background:var(--dark2);padding:140px 64px;border-top:1px solid var(--dark-border);">
  <div style="max-width:1100px;display:grid;grid-template-columns:260px 1fr;gap:100px;align-items:start;">
    <!-- 左侧：数据列 -->
    <div>
      <div style="padding:18px 0;border-bottom:1px solid var(--dark-border);border-top:1px solid var(--dark-border);">
        <div style="font-family:var(--font-l);font-size:9px;font-weight:400;letter-spacing:.22em;
          text-transform:uppercase;color:rgba(58,52,45,.8);margin-bottom:5px;">Location</div>
        <div style="font-family:var(--font-d);font-size:17px;color:var(--paper);">北京</div>
      </div>
      <!-- 重复多行 -->
    </div>
    <!-- 右侧：文字 -->
    <div>
      <div style="font-family:var(--font-l);font-size:10px;font-weight:400;letter-spacing:.22em;
        text-transform:uppercase;color:rgba(0,217,255,.6);margin-bottom:28px;">About</div>
      <h2 style="font-family:var(--font-d);font-size:clamp(32px,4vw,56px);
        line-height:1.1;letter-spacing:-.025em;color:var(--paper);margin-bottom:36px;">
        标题<br>第二行<span style="color:var(--amber);">关键词</span>
      </h2>
      <div style="font-size:14px;font-weight:300;color:var(--text-muted);line-height:1.95;max-width:500px;">
        <p>正文段落一。</p>
        <p style="margin-top:16px;">正文段落二。</p>
      </div>
    </div>
  </div>
</section>
```

---

## 禁用（个人主页专属禁忌）

- Hero 放产品截图（Hero 要放 IP 形象或大字）
- Works 区全是文字没有截图
- Statement 区放功能列表
- Stats 数字用 `font-weight:400` 或 `700`（必须 200）
- 连续两个深色区块中间没有浅色区
