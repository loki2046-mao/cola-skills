# 场景二：产品介绍页 · scene-product.md
> 适用：工具介绍页、平台介绍页、产品 Landing Page
> 对应模板：`assets/base.html`（fork 后自建）
> 核心情绪：「我要去试试这个工具」

---

## 与个人主页的核心差异

| 维度 | 个人主页 | 产品介绍页 |
|------|---------|----------|
| 主角 | 人 | 产品/工具本身 |
| Hero 主视觉 | IP 形象 | 产品截图或界面预览 |
| 内容区布局 | 杂志左右交替（图文并列） | 左功能名+右 tag 列表 |
| 转化目标 | 「关注我」 | 「去用这个工具」 |
| 情绪基调 | 个人气质、温度感 | 可信、可用、值得一试 |

---

## 区块清单（按顺序）

| # | 区块 | 底色 | 必选/可选 |
|---|------|------|----------|
| 1 | Hero：产品名 + 一句话命中痛点 + 截图/mockup | `--dark2` | 必选 |
| 2 | Problem：三大痛点 | `--warm` 浅底 | 必选 |
| 3 | Features：功能详解 | `--dark` 深底 | 必选 |
| 4 | Stats：关键数据 | `--warm` 浅底 | 推荐 |
| 5 | For Who：适合谁 | `--dark-panel` | 推荐 |
| 6 | CTA：转化 | `--dark2` 最深 | 必选 |
| 7 | Footer | `--dark2` | 必选 |

**深浅节奏：深→浅→深→浅→深→深→深**

---

## 组件 01 · Hero（产品型）

```html
<section style="min-height:100vh;display:flex;flex-direction:column;justify-content:flex-end;
  padding:0 60px 100px;background:var(--dark2);position:relative;overflow:hidden;">
  <!-- 背景光晕 -->
  <div style="position:absolute;inset:0;
    background:radial-gradient(ellipse 70% 60% at 60% 40%,rgba(200,122,69,.06) 0%,transparent 70%);
    pointer-events:none;"></div>
  <!-- 文字区 -->
  <div style="position:relative;z-index:2;max-width:700px;">
    <div style="font-family:var(--font-l);font-size:11px;font-weight:300;letter-spacing:.22em;
      text-transform:uppercase;color:var(--smoke-light);margin-bottom:24px;">
      产品 · 工具分类 · 状态
    </div>
    <h1 style="font-family:var(--font-d);font-size:clamp(52px,7.5vw,112px);
      line-height:1.0;letter-spacing:-.025em;color:var(--paper);margin-bottom:28px;">
      动词+结果的<br>一句话标题，<br><span style="color:var(--amber);">命中痛点</span>
    </h1>
    <p style="font-size:15px;font-weight:100;color:var(--text-muted);
      line-height:1.85;max-width:520px;margin-bottom:52px;">
      补充说明：解决了什么问题，面向谁，有什么不同。不超过 2 句。
    </p>
    <div style="display:flex;gap:16px;">
      <a href="#" style="font-family:var(--font-l);font-size:13px;font-weight:400;
        letter-spacing:.1em;text-transform:uppercase;color:var(--dark);background:var(--amber);
        padding:13px 28px;text-decoration:none;">立即使用</a>
      <a href="#features" style="font-family:var(--font-l);font-size:13px;font-weight:300;
        letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);
        border:1px solid var(--dark-border);padding:13px 28px;text-decoration:none;">
        看看能做什么
      </a>
    </div>
  </div>
</section>
```

**规则：**
- 标题是「动词+结果」的句式（写完/搞定/看见/不再xxx）
- 不放 IP 形象，IP 形象是个人主页专属
- 可以加产品界面截图（绝对定位在右侧或下方）

---

## 组件 02 · Problem 痛点三格

```html
<section style="background:var(--warm);color:var(--dark);padding:120px 60px;">
  <div style="font-family:var(--font-l);font-size:10px;font-weight:400;letter-spacing:.22em;
    text-transform:uppercase;color:var(--text-muted);margin-bottom:24px;">Why This</div>
  <h2 style="font-family:var(--font-d);font-size:clamp(32px,4vw,54px);
    line-height:1.1;letter-spacing:-.02em;color:var(--dark);margin-bottom:64px;">
    产品解决的<span style="color:var(--amber);">核心问题</span>
  </h2>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);
    border-top:1px solid var(--oat);border-left:1px solid var(--oat);">
    <div style="padding:48px 40px;border-right:1px solid var(--oat);border-bottom:1px solid var(--oat);">
      <div style="font-family:var(--font-l);font-size:clamp(52px,6vw,80px);font-weight:200;
        letter-spacing:-.05em;line-height:1;color:var(--oat);margin-bottom:20px;">01</div>
      <div style="font-family:var(--font-d);font-size:22px;color:var(--dark);margin-bottom:12px;">
        痛点标题
      </div>
      <p style="font-size:13px;font-weight:300;color:var(--text-sub);line-height:1.85;">
        具体描述这个痛点，1-3句，用用户说话的方式，不是功能介绍。
      </p>
    </div>
    <!-- 重复 3 次 -->
  </div>
</section>
```

**规则：**
- 序号用超细大字（`font-weight:200`），颜色用 `var(--oat)`（很淡），不抢标题
- 每格描述不超过 3 句，说的是用户痛苦，不是功能
- 用网格线分割，不是卡片阴影

---

## 组件 03 · Feature 行（产品功能专属）

**注意：这是产品介绍专属布局，不是个人主页的图文交替！**

```html
<!-- 功能区容器 -->
<section style="background:var(--dark);border-top:1px solid var(--dark-border);">
  <!-- 区块标题 -->
  <div style="padding:80px 60px 56px;border-bottom:1px solid var(--dark-border);">
    <div style="font-family:var(--font-l);font-size:10px;font-weight:400;letter-spacing:.22em;
      text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">Features</div>
    <h2 style="font-family:var(--font-d);font-size:clamp(24px,3vw,40px);
      letter-spacing:-.02em;color:var(--paper);">
      为xxx<span style="color:var(--amber);">真正设计</span>的功能
    </h2>
  </div>

  <!-- 功能行：左侧名称描述 + 右侧 tag 列表 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;
    border-bottom:1px solid var(--dark-border);min-height:360px;">
    <!-- 左侧 -->
    <div style="padding:56px 60px;display:flex;flex-direction:column;justify-content:center;
      border-right:1px solid var(--dark-border);">
      <div style="font-family:var(--font-m);font-size:11px;letter-spacing:.16em;
        color:var(--dark-border);margin-bottom:32px;">01 / 06</div>
      <h3 style="font-family:var(--font-d);font-size:clamp(24px,3vw,40px);
        line-height:1.1;letter-spacing:-.02em;margin-bottom:16px;">
        功能名称<span style="color:var(--amber);">关键词</span>
      </h3>
      <p style="font-size:13px;font-weight:300;color:var(--text-muted);
        line-height:1.9;max-width:380px;">
        功能描述：做什么，怎么做，有什么不同。2-3句。
      </p>
    </div>
    <!-- 右侧：具体 feature tag -->
    <div style="padding:56px 60px;display:flex;flex-direction:column;justify-content:center;gap:16px;">
      <!-- 已实现的功能 -->
      <div style="display:inline-flex;align-items:center;gap:8px;font-family:var(--font-l);
        font-size:10px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;
        color:var(--text-muted);border:1px solid var(--dark-border);padding:6px 12px;width:fit-content;">
        <span style="width:6px;height:6px;border-radius:50%;background:var(--amber);flex-shrink:0;"></span>
        具体功能点一
      </div>
      <div style="display:inline-flex;align-items:center;gap:8px;font-family:var(--font-l);
        font-size:10px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;
        color:var(--text-muted);border:1px solid var(--dark-border);padding:6px 12px;width:fit-content;">
        <span style="width:6px;height:6px;border-radius:50%;background:var(--amber);flex-shrink:0;"></span>
        具体功能点二
      </div>
      <!-- 开发中的功能（烟青色）-->
      <div style="display:inline-flex;align-items:center;gap:8px;font-family:var(--font-l);
        font-size:10px;font-weight:400;letter-spacing:.14em;text-transform:uppercase;
        color:var(--smoke);border:1px solid rgba(107,133,144,.3);padding:6px 12px;width:fit-content;">
        <span style="width:6px;height:6px;border-radius:50%;background:var(--smoke);flex-shrink:0;"></span>
        开发中的功能（烟青）
      </div>
    </div>
  </div>
  <!-- 功能行可重复，奇数行正常，偶数行加 direction:rtl 翻转 -->
</section>
```

**规则：**
- 左侧：功能名（大字得意黑）+ 描述（细字2-3句）
- 右侧：具体 feature 的 tag 列表，每个 tag 一行，amber 点代表已完成，smoke 点代表开发中
- 奇数行正常，偶数行整行加 `direction:rtl`（子元素加 `direction:ltr`）
- **绝对不要**在这里放真实截图——截图应该放在「功能展示区」（更大的专属组件）

---

## 组件 04 · 大图展示区（产品截图）

```html
<div style="border-bottom:1px solid var(--dark-border);">
  <!-- 截图全宽展示 -->
  <div style="overflow:hidden;position:relative;background:var(--dark-panel);min-height:480px;">
    <img src="screenshots/product-shot.png"
      style="width:100%;height:100%;object-fit:cover;object-position:top;
      filter:brightness(.9) saturate(.9);">
    <!-- 底部文字遮罩 -->
    <div style="position:absolute;bottom:0;left:0;right:0;padding:32px 60px;
      background:linear-gradient(transparent, rgba(20,18,16,.8));">
      <div style="font-family:var(--font-l);font-size:11px;font-weight:300;letter-spacing:.14em;
        text-transform:uppercase;color:var(--smoke-light);margin-bottom:4px;">截图说明</div>
      <div style="font-family:var(--font-d);font-size:22px;color:var(--paper);">功能名称</div>
    </div>
  </div>
</div>
```

---

## 组件 05 · For Who 适合谁

```html
<section style="background:var(--dark-panel);border-top:1px solid var(--dark-border);padding:120px 60px;">
  <div style="max-width:1100px;display:grid;grid-template-columns:1fr 1fr;gap:80px;align-items:start;">
    <!-- 左侧：大标题 -->
    <div>
      <div style="font-family:var(--font-l);font-size:10px;font-weight:400;letter-spacing:.22em;
        text-transform:uppercase;color:var(--text-muted);margin-bottom:24px;">Who Is It For</div>
      <h2 style="font-family:var(--font-d);font-size:clamp(32px,4vw,54px);
        line-height:1.1;letter-spacing:-.02em;color:var(--paper);margin-bottom:16px;">
        为这些人<span style="color:var(--amber);">造的</span>
      </h2>
      <p style="font-size:13px;font-weight:300;color:var(--text-muted);line-height:1.9;max-width:380px;">
        同时说清楚不适合谁——真诚的定位比什么都强。
      </p>
    </div>
    <!-- 右侧：用户卡片 -->
    <div style="display:flex;flex-direction:column;gap:24px;">
      <div style="padding:28px 32px;border:1px solid var(--dark-border);
        display:flex;gap:20px;align-items:flex-start;">
        <div style="font-family:var(--font-m);font-size:11px;font-weight:400;letter-spacing:.12em;
          color:var(--amber);padding-top:2px;flex-shrink:0;min-width:28px;">01</div>
        <div>
          <div style="font-family:var(--font-d);font-size:18px;margin-bottom:6px;">用户类型名称</div>
          <p style="font-size:13px;font-weight:300;color:var(--text-muted);line-height:1.8;">
            描述这类用户的具体需求场景，1-2句。
          </p>
        </div>
      </div>
      <!-- 重复 2-3 次 -->
    </div>
  </div>
</section>
```

---

## 组件 06 · CTA 转化区

```html
<section style="background:var(--dark2);border-top:1px solid var(--dark-border);
  padding:140px 60px;text-align:center;">
  <div style="font-family:var(--font-l);font-size:10px;font-weight:300;letter-spacing:.22em;
    text-transform:uppercase;color:var(--smoke-light);margin-bottom:24px;">开始使用</div>
  <h2 style="font-family:var(--font-d);font-size:clamp(40px,5.5vw,80px);
    line-height:1.05;letter-spacing:-.025em;margin-bottom:20px;">
    动词+结果<br>的<span style="color:var(--amber);">标题</span>
  </h2>
  <p style="font-size:14px;font-weight:100;color:var(--text-muted);line-height:1.85;
    max-width:440px;margin:0 auto 48px;">
    补充说明，免费/邀请制/数据安全等关键信息。
  </p>
  <a href="#" style="display:inline-flex;align-items:center;font-family:var(--font-l);
    font-size:13px;font-weight:400;letter-spacing:.1em;text-transform:uppercase;
    color:var(--dark);background:var(--amber);padding:14px 32px;text-decoration:none;">
    行动按钮文字 →
  </a>
  <div style="font-family:var(--font-l);font-size:11px;font-weight:300;letter-spacing:.1em;
    color:rgba(46,42,38,.8);margin-top:20px;">product-url.hiloki.ai</div>
</section>
```

**规则：**
- CTA 区只有一个按钮，不要分散
- 按钮文字是行动词（开始使用/立即试试/免费开始）
- 下方小字补充一条最能打消疑虑的信息

---

## 禁用（产品介绍页专属禁忌）

- Hero 放 IP 形象（IP 形象是个人主页专属）
- 功能区用「杂志图文交替」（那是个人主页的 Works 布局）
- 功能描述全是文字段落，没有 tag 可扫视
- Stats 数字用 `font-weight:700`（必须 200）
- CTA 放多个按钮或多个链接
