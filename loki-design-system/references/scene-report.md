# 场景文件 · 数据报告 / 工具横评
> 赛博小熊猫 Loki · scene-report.md
> 适用：AI工具横向测评、多工具对比、数据分析输出、研究总结
> 最后更新：2026-05-27

---

## 一、场景全局规则

### 核心情绪目标
**「这个结论我信，这个数据有用。」**

读者是和 Loki 一样认真的人：愿意看完，但不接受水分。每个组件的职责是让数据可信、让观点可辨识、让判断可直接用。

### 底色方案

| 用途 | 底色 | 理由 |
|------|------|------|
| 正文区（绝大多数） | 纸白 `#FDFAF5` | 文字密度高，浅底可读性最优 |
| 页面大背景 | 暖米 `#F5F0E8` | 与纸白区块产生轻微层次，不刺眼 |
| 封面 / 强调数据页 / 结论页 | 暗底 `#1A1816` | 深浅交替打节奏，稀缺使用 |
| 分割线 / 边框 / 表格线 | 燕麦 `var(--oat)` = `#EBE4D6` | **必须用暖色边框，禁用冷灰** |

> **深底不超过全文 30%。** 封面用一次，结论页用一次，中间不加深色块，除非有一整页是「关键数据聚焦」。

### 颜色语义（报告场景专用定义）

| 颜色 | 色值 / 变量 | 语义 | 禁止混用场景 |
|------|-------------|------|-------------|
| 琥珀橙 | `#C87A45` / `var(--amber)` | 优秀评级 / CTA / 标题高亮词 | 不用于 My Take 竖线 |
| 烟青 | `#6B8590` / `var(--smoke)` | 良好评级 / 次要标签 / 客观信息标注 | 不用于推荐/高亮 |
| 苔绿 | `#7A8458` | **My Take 专用色** — 作者主观判断的唯一标记 | 不用于任何客观数据、评分、表格 |
| 暗红 | `#8B4A4A` | 差评级 / 警示 | 不用于中性信息 |
| `var(--text-muted)` | `#9A9085` | 一般评级 / 辅助说明 | — |

> **苔绿和琥珀橙的语义互斥是本场景最重要的规则。**
> 苔绿 = 主观 / 我的判断。琥珀橙 = 优秀 / 值得关注的客观结果。两者颜色接近，混用会让读者误判信息性质。

### 密度原则
- 报告是文字密集场景，但「密」不等于「满」——每个模块之间留足 `48px` 以上间距
- 评分表格和对比矩阵是最密的，行高不低于 `52px`，让眼睛呼吸
- 数字要大：重要数据用 `Space Grotesk weight 200`，字号不小于 `32px`，视觉上自带强调
- 每页只有一个「最重要的结论」，其他都是辅助

### CSS 变量基础（所有组件共用）

```css
:root {
  /* 底色 */
  --dark-bg:     #1A1816;
  --paper:       #FDFAF5;
  --warm-oat:    #F5F0E8;
  --oat:         #EBE4D6;

  /* 品牌色 */
  --amber:       #C87A45;
  --amber-light: #D9A87A;
  --amber-deep:  #A05E30;

  /* 语义色 */
  --smoke:       #6B8590;
  --moss:        #7A8458;   /* My Take 专用 */
  --bad-red:     #8B4A4A;

  /* 文字 */
  --text-main:   #1F1D1A;
  --text-sub:    #6B6157;
  --text-muted:  #9A9085;
  --text-dim:    #C4BBB0;
  --text-on-dark:#FDFAF5;

  /* 边框 */
  --border:      #EBE4D6;   /* 暖色，非冷灰 */
  --border-mid:  #D5CABF;
}
```

### 字体加载

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@200;300;400;500;600&family=Noto+Sans+SC:wght@100;300;400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>@import url("https://fontsapi.zeoseven.com/92/main/result.css");</style>
```

---

## 二、内容类型 → 组件映射

> 报告场景的核心规则：**内容性质决定用哪个组件，不是「换一换排版」。**

| 内容类型 | 用哪个组件 | 为什么 |
|---------|-----------|--------|
| 报告开头 | Cover 报告封面 | 建立基调，说清楚这是什么、谁写的 |
| 3条核心结论 | Summary 执行摘要 | 让没时间看全文的人也能拿走结论 |
| 多工具综合评分 | Scorecard 评分表格 | 并列对比，等级可视化 |
| 多工具×多维度 | Matrix 对比矩阵 | 矩阵结构，快速扫列 |
| 「这里有问题」/「这里做得好」 | Evidence 截图证据区 | 真实感，让结论可验证 |
| 作者主观判断 | MyTake 作者观点框 | **苔绿标记主观，严格区分客观数据** |
| 最终推荐结论 | Conclusion 结论卡 | 深底，有力，带 CTA |

---

## 三、组件详解

---

### 组件 1 · Cover 报告封面

**用途**：报告第一屏，建立「这是一份认真的评测」的第一印象。

**适合内容**：报告标题（评测主题）、副标题（测评维度/范围说明）、日期、作者署名、可选 eyebrow 标签（如 `TOOL REVIEW · 2026`）。

**两种底色方案可选**：
- 深底版（`#1A1816`）：用于重型横评，气场强，显专业
- 浅底版（`#FDFAF5`）：用于轻量测评/单工具深评，温度感更高

**文字基调**：标题直接说测评对象，不绕弯。副标题说评测框架，极简，不超过一句话。

#### ❌ 封面禁忌
- 不加装饰图案或背景纹理（留白是力量）
- 标题不超过 20 字
- 不把评分结果放在封面（那是剧透，不是吸引力）

#### 完整 HTML（深底版）

```html
<!-- 字体加载见全局规则 -->
<section style="
  background: var(--dark-bg, #1A1816);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: clamp(40px, 6vw, 80px);
  position: relative;
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- Eyebrow 标签行 -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 300;
    letter-spacing: 0.22em;
    color: #9A9085;
    text-transform: uppercase;
    margin-bottom: 32px;
  ">TOOL REVIEW · CYBER PANDA LOKI · 2026</div>

  <!-- 主标题（得意黑） -->
  <h1 style="
    font-family: 'Smiley Sans Oblique', 'Noto Sans SC', sans-serif;
    font-size: clamp(40px, 6vw, 88px);
    line-height: 1.1;
    color: #FDFAF5;
    margin: 0 0 20px;
    max-width: 800px;
  ">
    五款 AI 写作工具<br>
    <span style="color: #C87A45;">深度横评</span>
  </h1>

  <!-- 副标题 -->
  <p style="
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 16px;
    font-weight: 100;
    color: #6B6157;
    margin: 0 0 48px;
    max-width: 500px;
    line-height: 1.7;
  ">从日常写作到长文创作，测试真实使用场景下的表现差异</p>

  <!-- 分割线 -->
  <div style="width: 48px; height: 1px; background: #C87A45; margin-bottom: 24px;"></div>

  <!-- 作者 + 日期行 -->
  <div style="
    display: flex;
    align-items: center;
    gap: 24px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #9A9085;
  ">
    <span>Loki · 赛博小熊猫</span>
    <span style="color: #EBE4D6; opacity: 0.3;">|</span>
    <span>2026-05-27</span>
  </div>
</section>
```

#### 完整 HTML（浅底版）

```html
<section style="
  background: var(--paper, #FDFAF5);
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: clamp(40px, 6vw, 80px);
  border-bottom: 1px solid #EBE4D6;
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- 左侧橙竖线装饰（浅底封面特有） -->
  <div style="
    width: 3px;
    height: 60px;
    background: #C87A45;
    margin-bottom: 32px;
  "></div>

  <!-- Eyebrow -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 300;
    letter-spacing: 0.22em;
    color: #9A9085;
    text-transform: uppercase;
    margin-bottom: 20px;
  ">TOOL REVIEW · 2026</div>

  <!-- 主标题 -->
  <h1 style="
    font-family: 'Smiley Sans Oblique', 'Noto Sans SC', sans-serif;
    font-size: clamp(36px, 5vw, 72px);
    line-height: 1.15;
    color: #1F1D1A;
    margin: 0 0 16px;
    max-width: 700px;
  ">
    五款 AI 写作工具<span style="color: #C87A45;">深度横评</span>
  </h1>

  <!-- 副标题 -->
  <p style="
    font-size: 15px;
    font-weight: 100;
    color: #6B6157;
    margin: 0 0 36px;
    max-width: 480px;
    line-height: 1.7;
  ">从日常写作到长文创作，测试真实使用场景下的表现差异</p>

  <!-- 作者 + 日期 -->
  <div style="
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #9A9085;
    display: flex;
    gap: 20px;
  ">
    <span>Loki · 赛博小熊猫</span>
    <span>2026-05-27</span>
  </div>
</section>
```

---

### 组件 2 · Summary 执行摘要

**用途**：报告前段，呈现 3 条核心结论。让没时间读完整报告的人直接拿走判断依据。

**适合内容**：3 条带加粗结论句的摘要条目，每条有 1-2 句展开说明。条目数量不超过 4 条（超过就是没提炼）。

**底色**：纸白 `#FDFAF5`，左侧橙色竖线是每条结论的视觉锚点。

**文字基调**：结论句直接、有立场（不是「各有优缺点」），展开说明提供依据，口吻中立。

#### ❌ Summary 禁忌
- 不写「综合来看，各工具都有自己的优势」这类废话结论
- 每条结论句不超过 30 字
- 不在摘要区放图表或评分——这是文字区

```html
<section style="
  background: var(--paper, #FDFAF5);
  padding: clamp(48px, 6vw, 80px);
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- Section Eyebrow -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px;
    font-weight: 300;
    letter-spacing: 0.22em;
    color: #9A9085;
    text-transform: uppercase;
    margin-bottom: 36px;
  ">EXECUTIVE SUMMARY · 核心结论</div>

  <!-- 结论列表 -->
  <div style="display: flex; flex-direction: column; gap: 32px; max-width: 720px;">

    <!-- 结论条目 × 3（复制此块） -->
    <div style="display: flex; gap: 20px; align-items: flex-start;">
      <!-- 左橙竖线（装饰命名：summary-line） -->
      <div class="summary-line" style="
        width: 3px;
        min-height: 100%;
        background: #C87A45;
        flex-shrink: 0;
        margin-top: 4px;
      "></div>

      <div>
        <!-- 加粗结论句 -->
        <p style="
          font-size: 17px;
          font-weight: 500;
          color: #1F1D1A;
          margin: 0 0 8px;
          line-height: 1.5;
        ">Claude 在长文写作中的一致性显著优于其他四款</p>

        <!-- 展开说明（灰色，细） -->
        <p style="
          font-size: 14px;
          font-weight: 300;
          color: #6B6157;
          margin: 0;
          line-height: 1.7;
        ">测试了 10 篇 3000 字以上的长文，Claude 在段落衔接和风格一致性上的得分均为最高，尤其是在跨段落引用和语气连贯上。</p>
      </div>
    </div>

    <div style="display: flex; gap: 20px; align-items: flex-start;">
      <div class="summary-line" style="
        width: 3px; min-height: 100%;
        background: #C87A45; flex-shrink: 0; margin-top: 4px;
      "></div>
      <div>
        <p style="font-size: 17px; font-weight: 500; color: #1F1D1A; margin: 0 0 8px; line-height: 1.5;">
          Notion AI 的价格优势在实际使用中被功能上限抵消
        </p>
        <p style="font-size: 14px; font-weight: 300; color: #6B6157; margin: 0; line-height: 1.7;">
          月均 10 美元的定价看起来合理，但功能深度比不上同价位的 ChatGPT Plus，适合轻量用户，不适合把 AI 写作当主要工作流的人。
        </p>
      </div>
    </div>

    <div style="display: flex; gap: 20px; align-items: flex-start;">
      <div class="summary-line" style="
        width: 3px; min-height: 100%;
        background: #C87A45; flex-shrink: 0; margin-top: 4px;
      "></div>
      <div>
        <p style="font-size: 17px; font-weight: 500; color: #1F1D1A; margin: 0 0 8px; line-height: 1.5;">
          没有一款工具在「指令理解」上达到满分
        </p>
        <p style="font-size: 14px; font-weight: 300; color: #6B6157; margin: 0; line-height: 1.7;">
          所有工具在复杂多步骤指令下都出现了理解偏差，差异在于恢复速度和澄清提问的质量，而不是有没有犯错。
        </p>
      </div>
    </div>

  </div>
</section>
```

---

### 组件 3 · Scorecard 评分表格

**用途**：展示多工具在同一套维度下的综合评分，横向可比，等级可视化。

**适合内容**：3-6 个工具 × 4-6 个评分维度，每格给分（1-10 或百分制）加等级色。

**评级颜色语义**（严格执行，不得混用）：

| 等级 | 颜色 | 色值 |
|------|------|------|
| 优秀 | 琥珀橙 `var(--amber)` | `#C87A45` |
| 良好 | 烟青 `var(--smoke)` | `#6B8590` |
| 一般 | `var(--text-muted)` | `#9A9085` |
| 差 | 暗红 | `#8B4A4A` |

**装饰命名**：评分条 = `score-bar`；等级标签 = `verdict-tag`

**文字基调**：维度名精确，不模糊（不写「整体感受」，写「长文连贯性」）。

#### ❌ Scorecard 禁忌
- 不用冷灰色边框（必须用 `var(--oat)` 暖色边框）
- 不用彩色进度条（只用品牌色体系的四级评级色）
- 不省略「分数来源说明」（底部一行说明评分方法）

```html
<section style="
  background: var(--paper, #FDFAF5);
  padding: clamp(48px, 6vw, 80px);
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- Eyebrow -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px; font-weight: 300;
    letter-spacing: 0.22em; color: #9A9085;
    text-transform: uppercase; margin-bottom: 36px;
  ">SCORECARD · 综合评分</div>

  <!-- 评分卡容器 -->
  <div style="display: flex; flex-direction: column; gap: 0; max-width: 800px; border: 1px solid #EBE4D6; border-radius: 4px; overflow: hidden;">

    <!-- 表头行 -->
    <div style="
      display: grid;
      grid-template-columns: 160px repeat(5, 1fr);
      background: #F5F0E8;
      border-bottom: 1px solid #EBE4D6;
    ">
      <div style="padding: 14px 16px; font-size: 11px; font-weight: 300; color: #9A9085; font-family: 'Space Grotesk', sans-serif; letter-spacing: 0.1em; text-transform: uppercase;">工具</div>
      <!-- 维度标题 × 5（复制修改） -->
      <div style="padding: 14px 12px; font-size: 12px; font-weight: 400; color: #6B6157; border-left: 1px solid #EBE4D6;">长文连贯</div>
      <div style="padding: 14px 12px; font-size: 12px; font-weight: 400; color: #6B6157; border-left: 1px solid #EBE4D6;">指令理解</div>
      <div style="padding: 14px 12px; font-size: 12px; font-weight: 400; color: #6B6157; border-left: 1px solid #EBE4D6;">速度</div>
      <div style="padding: 14px 12px; font-size: 12px; font-weight: 400; color: #6B6157; border-left: 1px solid #EBE4D6;">价格</div>
      <div style="padding: 14px 12px; font-size: 12px; font-weight: 400; color: #6B6157; border-left: 1px solid #EBE4D6;">综合</div>
    </div>

    <!-- 数据行 × N（每个工具一行） -->

    <!-- Claude -->
    <div style="display: grid; grid-template-columns: 160px repeat(5, 1fr); border-bottom: 1px solid #EBE4D6; min-height: 52px;">
      <div style="padding: 14px 16px; font-size: 14px; font-weight: 500; color: #1F1D1A; display: flex; align-items: center;">Claude</div>

      <!-- 评分格：优秀 → var(--amber) -->
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <!-- score-bar -->
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 90%; height: 100%; background: #C87A45; border-radius: 2px;"></div>
        </div>
        <!-- verdict-tag -->
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 400; color: #C87A45;">9.0</span>
      </div>

      <!-- 指令理解：良好 → var(--smoke) -->
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 78%; height: 100%; background: #6B8590; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 400; color: #6B8590;">7.8</span>
      </div>

      <!-- 速度：一般 → var(--text-muted) -->
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 60%; height: 100%; background: #9A9085; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 400; color: #9A9085;">6.0</span>
      </div>

      <!-- 价格：差 → bad-red -->
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 40%; height: 100%; background: #8B4A4A; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 400; color: #8B4A4A;">4.0</span>
      </div>

      <!-- 综合：优秀 -->
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; justify-content: center;">
        <span style="
          font-family: 'Space Grotesk', sans-serif;
          font-size: 18px; font-weight: 200;
          color: #C87A45;
        ">8.2</span>
      </div>
    </div>

    <!-- ChatGPT（第二行示例） -->
    <div style="display: grid; grid-template-columns: 160px repeat(5, 1fr); border-bottom: 1px solid #EBE4D6; min-height: 52px;">
      <div style="padding: 14px 16px; font-size: 14px; font-weight: 500; color: #1F1D1A; display: flex; align-items: center;">ChatGPT Plus</div>
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 72%; height: 100%; background: #6B8590; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; color: #6B8590;">7.2</span>
      </div>
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 85%; height: 100%; background: #C87A45; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; color: #C87A45;">8.5</span>
      </div>
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 88%; height: 100%; background: #C87A45; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; color: #C87A45;">8.8</span>
      </div>
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; flex-direction: column; gap: 6px; justify-content: center;">
        <div style="width: 100%; height: 4px; background: #EBE4D6; border-radius: 2px; overflow: hidden;">
          <div class="score-bar" style="width: 75%; height: 100%; background: #6B8590; border-radius: 2px;"></div>
        </div>
        <span class="verdict-tag" style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; color: #6B8590;">7.5</span>
      </div>
      <div style="padding: 12px; border-left: 1px solid #EBE4D6; display: flex; align-items: center; justify-content: center;">
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 200; color: #C87A45;">8.0</span>
      </div>
    </div>

    <!-- 更多工具行：复制上方行，替换数据 -->

  </div>

  <!-- 评分说明 -->
  <p style="
    font-size: 12px; font-weight: 300; color: #9A9085;
    margin-top: 16px; line-height: 1.6;
  ">评分基于 2026-05 实测，满分 10 分。各维度均为 Loki 亲测 3 次取平均，不含官方宣传数据。</p>
</section>
```

---

### 组件 4 · Matrix 对比矩阵

**用途**：多工具 × 多维度的结构化对比，快速扫列，看「谁在哪个维度领先」。

**适合内容**：功能有无（√/×）、特性等级、数字对比。列数不超过 6，行数不超过 8（超过就拆表）。

**首列固定**：工具名（行标签）首列左对齐，有视觉锚定感。

**底色交替**：奇数行 `#FDFAF5`，偶数行 `#F5F0E8`，用暖色调区分，不用冷灰斑马线。

**文字基调**：表格只放「能判断的信息」，不放「感受」。√/× 是判断，「尚可」不是。

#### ❌ Matrix 禁忌
- 不用冷灰色边框和斑马线（用暖色边框 `var(--oat)` + 暖色交替行）
- 不在表格里放长句子（≥ 10 字就是设计失误，应该换成 Evidence 组件）
- 表头不加背景色块（除非是深底强调版）

```html
<section style="
  background: var(--warm-oat, #F5F0E8);
  padding: clamp(48px, 6vw, 80px);
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- Eyebrow -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px; font-weight: 300;
    letter-spacing: 0.22em; color: #9A9085;
    text-transform: uppercase; margin-bottom: 36px;
  ">COMPARISON MATRIX · 功能对比</div>

  <!-- 矩阵容器（横向可滚动） -->
  <div style="overflow-x: auto; -webkit-overflow-scrolling: touch;">
    <table style="
      width: 100%; min-width: 600px;
      border-collapse: collapse;
      background: #FDFAF5;
      border: 1px solid #EBE4D6;
      border-radius: 4px;
      overflow: hidden;
    ">
      <!-- 表头 -->
      <thead>
        <tr style="background: #FDFAF5; border-bottom: 2px solid #EBE4D6;">
          <th style="
            width: 140px; padding: 14px 16px;
            text-align: left; font-size: 11px; font-weight: 300;
            color: #9A9085; font-family: 'Space Grotesk', sans-serif;
            letter-spacing: 0.1em; text-transform: uppercase;
            border-right: 1px solid #EBE4D6;
            position: sticky; left: 0; background: #FDFAF5; z-index: 1;
          ">工具</th>
          <!-- 维度列标题 × N（复制修改） -->
          <th style="padding: 14px 16px; text-align: center; font-size: 13px; font-weight: 400; color: #1F1D1A; border-right: 1px solid #EBE4D6;">API 接入</th>
          <th style="padding: 14px 16px; text-align: center; font-size: 13px; font-weight: 400; color: #1F1D1A; border-right: 1px solid #EBE4D6;">中文优化</th>
          <th style="padding: 14px 16px; text-align: center; font-size: 13px; font-weight: 400; color: #1F1D1A; border-right: 1px solid #EBE4D6;">离线可用</th>
          <th style="padding: 14px 16px; text-align: center; font-size: 13px; font-weight: 400; color: #1F1D1A; border-right: 1px solid #EBE4D6;">免费额度</th>
          <th style="padding: 14px 16px; text-align: center; font-size: 13px; font-weight: 400; color: #1F1D1A;">插件生态</th>
        </tr>
      </thead>

      <tbody>
        <!-- 奇数行：#FDFAF5 -->
        <tr style="background: #FDFAF5; border-bottom: 1px solid #EBE4D6;">
          <td style="padding: 14px 16px; font-size: 14px; font-weight: 500; color: #1F1D1A; border-right: 1px solid #EBE4D6; position: sticky; left: 0; background: #FDFAF5;">Claude</td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #C87A45; font-weight: 500; font-size: 16px;">✓</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #6B8590; font-size: 13px;">良好</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #8B4A4A; font-weight: 500; font-size: 16px;">✗</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #6B8590; font-size: 13px;">有限</span>
          </td>
          <td style="padding: 14px 16px; text-align: center;">
            <span style="color: #8B4A4A; font-weight: 500; font-size: 16px;">✗</span>
          </td>
        </tr>

        <!-- 偶数行：#F5F0E8 -->
        <tr style="background: #F5F0E8; border-bottom: 1px solid #EBE4D6;">
          <td style="padding: 14px 16px; font-size: 14px; font-weight: 500; color: #1F1D1A; border-right: 1px solid #EBE4D6; position: sticky; left: 0; background: #F5F0E8;">ChatGPT Plus</td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #C87A45; font-weight: 500; font-size: 16px;">✓</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #C87A45; font-size: 13px; font-weight: 500;">优秀</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #8B4A4A; font-weight: 500; font-size: 16px;">✗</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #6B8590; font-size: 13px;">有限</span>
          </td>
          <td style="padding: 14px 16px; text-align: center;">
            <span style="color: #C87A45; font-weight: 500; font-size: 16px;">✓</span>
          </td>
        </tr>

        <!-- 奇数行 -->
        <tr style="background: #FDFAF5; border-bottom: 1px solid #EBE4D6;">
          <td style="padding: 14px 16px; font-size: 14px; font-weight: 500; color: #1F1D1A; border-right: 1px solid #EBE4D6; position: sticky; left: 0; background: #FDFAF5;">Gemini Advanced</td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #C87A45; font-weight: 500; font-size: 16px;">✓</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #9A9085; font-size: 13px;">一般</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #8B4A4A; font-weight: 500; font-size: 16px;">✗</span>
          </td>
          <td style="padding: 14px 16px; text-align: center; border-right: 1px solid #EBE4D6;">
            <span style="color: #C87A45; font-size: 13px; font-weight: 500;">丰富</span>
          </td>
          <td style="padding: 14px 16px; text-align: center;">
            <span style="color: #C87A45; font-weight: 500; font-size: 16px;">✓</span>
          </td>
        </tr>

        <!-- 更多行：复制上方，替换数据 -->
      </tbody>
    </table>
  </div>

  <!-- 图例 -->
  <div style="
    display: flex; gap: 24px; margin-top: 16px;
    font-size: 12px; font-weight: 300; color: #9A9085;
    font-family: 'Space Grotesk', sans-serif;
  ">
    <span><span style="color: #C87A45;">✓</span> 支持 / 优秀</span>
    <span><span style="color: #6B8590;">良好</span> 部分支持</span>
    <span><span style="color: #9A9085;">一般</span> 基础功能</span>
    <span><span style="color: #8B4A4A;">✗</span> 不支持 / 差</span>
  </div>
</section>
```

---

### 组件 5 · Evidence 截图证据区

**用途**：让评测结论可验证。放截图，加标注，说明「这里有问题」或「这里做得好」。

**适合内容**：工具输出截图 + 说明性标注（箭头、圆圈、批注文字）。一组证据一个「结论锚点」，不要把多个不相关的截图塞一起。

**装饰命名**：标注圆圈/箭头 = `evidence-mark`；截图容器 = `evidence-frame`

**文字基调**：标注文字简短直接，「这里的段落衔接断了」比「此处存在连贯性问题」更好。

#### ❌ Evidence 禁忌
- 不用截图装饰页面（截图是证据，不是插图）
- 标注不超过 3 处（超过说明截图选错了）
- 不放没有标注的原始截图（那是附录，不是证据）

```html
<section style="
  background: var(--paper, #FDFAF5);
  padding: clamp(48px, 6vw, 80px);
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- Eyebrow -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px; font-weight: 300;
    letter-spacing: 0.22em; color: #9A9085;
    text-transform: uppercase; margin-bottom: 12px;
  ">EVIDENCE · 截图证据</div>

  <!-- 结论锚点标题 -->
  <h3 style="
    font-family: 'Smiley Sans Oblique', 'Noto Sans SC', sans-serif;
    font-size: clamp(20px, 2.5vw, 28px);
    color: #1F1D1A; margin: 0 0 32px; line-height: 1.3;
  ">第 3 次测试中，Claude 在段落 4→5 的衔接出现了<span style="color: #8B4A4A;">角色混淆</span></h3>

  <!-- 证据主体：截图 + 说明 -->
  <div style="
    display: grid;
    grid-template-columns: 1fr 280px;
    gap: 40px;
    align-items: start;
  ">

    <!-- 截图区（带标注） -->
    <div class="evidence-frame" style="
      position: relative;
      border: 1px solid #EBE4D6;
      border-radius: 4px;
      overflow: hidden;
      background: #F5F0E8;
    ">
      <!-- 截图占位（替换为真实截图 img） -->
      <div style="
        width: 100%; aspect-ratio: 16/9;
        background: linear-gradient(135deg, #EBE4D6 0%, #D5CABF 100%);
        display: flex; align-items: center; justify-content: center;
        font-size: 14px; color: #9A9085;
      ">[ 截图：Claude 输出文本，约 400 字 ]</div>

      <!-- evidence-mark：圆圈标注 1 -->
      <div class="evidence-mark" style="
        position: absolute;
        top: 38%; left: 52%;
        width: 28px; height: 28px;
        border: 2px solid #8B4A4A;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
      ">
        <span style="font-size: 11px; font-weight: 600; color: #8B4A4A;">1</span>
      </div>

      <!-- evidence-mark：箭头标注 2 -->
      <div class="evidence-mark" style="
        position: absolute;
        top: 62%; left: 30%;
        display: flex; align-items: center; gap: 4px;
      ">
        <span style="color: #C87A45; font-size: 18px; line-height: 1;">→</span>
        <div style="
          background: #C87A45;
          color: #FDFAF5;
          font-size: 10px; font-weight: 500;
          padding: 2px 8px; border-radius: 2px;
          white-space: nowrap;
        ">角色从A切换到B</div>
      </div>
    </div>

    <!-- 标注说明列表 -->
    <div style="display: flex; flex-direction: column; gap: 20px; padding-top: 8px;">

      <!-- 标注 1 -->
      <div style="display: flex; gap: 12px; align-items: flex-start;">
        <div style="
          width: 22px; height: 22px; min-width: 22px;
          border: 1.5px solid #8B4A4A;
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          margin-top: 2px;
        ">
          <span style="font-size: 10px; font-weight: 600; color: #8B4A4A;">1</span>
        </div>
        <p style="font-size: 13px; font-weight: 300; color: #1F1D1A; margin: 0; line-height: 1.7;">
          段落 4 结尾仍是角色 A 的视角，段落 5 开头无过渡直接变成角色 B 的口吻
        </p>
      </div>

      <!-- 标注 2 -->
      <div style="display: flex; gap: 12px; align-items: flex-start;">
        <div style="
          width: 22px; height: 22px; min-width: 22px;
          background: #C87A45;
          border-radius: 2px;
          display: flex; align-items: center; justify-content: center;
          margin-top: 2px;
        ">
          <span style="font-size: 10px; font-weight: 600; color: #FDFAF5;">2</span>
        </div>
        <p style="font-size: 13px; font-weight: 300; color: #1F1D1A; margin: 0; line-height: 1.7;">
          「她说」→「他说」的切换发生在无明显触发句的位置，前后文没有提示
        </p>
      </div>

      <!-- 结论小卡 -->
      <div style="
        margin-top: 8px;
        border-top: 1px solid #EBE4D6;
        padding-top: 16px;
        font-size: 13px; font-weight: 300; color: #6B6157;
        line-height: 1.7;
      ">
        此问题在连续对话超过 6 轮后概率上升，重新提供角色设定后可恢复。
      </div>
    </div>

  </div>
</section>
```

---

### 组件 6 · MyTake 作者观点框

**用途**：在客观数据之后，标记「这是 Loki 的主观判断」。颜色和结构都必须区别于客观内容区。

**适合内容**：作者对某工具/某结论的个人判断、推荐理由、使用建议、对行业现象的看法。**不放数据，不放评分。**

**核心视觉标记**：左侧苔绿竖线 `#7A8458`（装饰命名：`my-take-line`）+ 「My Take / Loki」署名标头。苔绿是本场景唯一专属于主观判断的颜色，不得在其他组件中使用。

**文字基调**：第一人称，可以有情绪，可以有立场，语气比摘要更口语。「我觉得」「说实话」「坦白讲」是这个区块的正确语气，摆在客观数据之后刚好形成对比。

#### ❌ MyTake 禁忌
- 竖线颜色不能改为琥珀橙（苔绿是主观的专用颜色，混用会让读者误判信息性质）
- 不省略「Loki」署名标头（读者必须清楚这是作者观点，不是评测事实）
- 不在 MyTake 块里放评分数字（数字是客观的语言，不属于这个区块）
- 不把整个总结都写成 MyTake（MyTake 是点睛，不是主体）

```html
<section style="
  background: var(--paper, #FDFAF5);
  padding: clamp(48px, 6vw, 80px);
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- MyTake 容器 -->
  <div style="
    display: flex;
    gap: 20px;
    align-items: flex-start;
    max-width: 680px;
  ">
    <!-- my-take-line：苔绿竖线，My Take 专属，禁止改色 -->
    <div class="my-take-line" style="
      width: 3px;
      min-height: 100%;
      background: #7A8458;
      flex-shrink: 0;
      margin-top: 4px;
      align-self: stretch;
    "></div>

    <div>
      <!-- 署名标头（必须保留，不能省略） -->
      <div style="
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 14px;
      ">
        <span style="
          font-family: 'Space Grotesk', sans-serif;
          font-size: 10px; font-weight: 400;
          letter-spacing: 0.18em;
          color: #7A8458;
          text-transform: uppercase;
          background: rgba(122, 132, 88, 0.1);
          padding: 3px 8px;
          border-radius: 2px;
        ">MY TAKE</span>
        <span style="
          font-size: 12px; font-weight: 300; color: #9A9085;
        ">Loki · 赛博小熊猫</span>
      </div>

      <!-- 主观判断内容 -->
      <p style="
        font-size: 16px; font-weight: 400;
        color: #1F1D1A;
        margin: 0 0 12px;
        line-height: 1.8;
      ">说实话，Claude 的长文表现确实最稳，但我不会推荐所有人都去用它。</p>

      <p style="
        font-size: 15px; font-weight: 300;
        color: #6B6157;
        margin: 0;
        line-height: 1.8;
      ">如果你的核心需求是快速生成初稿、对质量要求不算极高，ChatGPT Plus 的速度和插件生态更实用。Claude 的优势是「精」，但你得有时间和精力驾驭它，每次给足上下文、调整指令。对普通用户来说，这个「精」可能换不来那个投入比。</p>

      <!-- 可选：引用/金句加粗版本 -->
      <!-- <p style="
        font-size: 17px; font-weight: 500; color: #7A8458;
        border-top: 1px solid #EBE4D6; margin-top: 16px; padding-top: 16px;
      ">工具好不好，取决于你有没有时间让它好。</p> -->
    </div>
  </div>
</section>
```

#### MyTake 与 Summary 的视觉区别一览

| 特征 | Summary 执行摘要 | MyTake 作者观点 |
|------|----------------|----------------|
| 左竖线颜色 | 琥珀橙 `#C87A45` | 苔绿 `#7A8458` |
| 信息性质 | 客观结论（可验证） | 主观判断（不可验证） |
| 署名 | 无（客观不归属个人） | 有「Loki」标头 |
| 数字/评分 | 可以有 | 禁止 |
| 语气 | 中立直接 | 第一人称，可带情绪 |

---

### 组件 7 · Conclusion 结论卡

**用途**：报告收尾，给出最终推荐（或不推荐）。带 CTA 按钮，让读者知道下一步该怎么做。

**适合内容**：最终裁决一句话、推荐原因 2-3 句、CTA 按钮（可以是「去试试」「暂不推荐」「看情况」）。

**底色**：暗底 `#1A1816`，深底给结论以终结感和重量感。

**CTA 颜色语义**：
- 推荐 → 琥珀橙底 `#C87A45` + 深色文字
- 不推荐 → 暗红边框 `#8B4A4A` + 暗红文字（不用填充色，降低攻击性）
- 看情况 → 烟青边框 `#6B8590` + 烟青文字

**文字基调**：深底文字必须用 `#FDFAF5`，副文字用 `#9A9085`，不用白色 `#FFFFFF`。结论句要有立场，「推荐长文写作者使用」比「各有优缺点，按需选择」好。

#### ❌ Conclusion 禁忌
- 不用浅底（结论卡只有一个，深底是稀缺感的来源）
- CTA 按钮不超过 2 个（一屏两个 CTA 是极限）
- 不在结论卡里重复评分数字（那是 Scorecard 的事）
- 不写「总的来说各有优劣」（这是废话裁决，不是结论）

```html
<section style="
  background: var(--dark-bg, #1A1816);
  padding: clamp(64px, 8vw, 100px) clamp(40px, 6vw, 80px);
  font-family: 'Noto Sans SC', sans-serif;
">
  <!-- Eyebrow -->
  <div style="
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11px; font-weight: 300;
    letter-spacing: 0.22em; color: #6B6157;
    text-transform: uppercase; margin-bottom: 40px;
  ">VERDICT · 最终结论</div>

  <!-- 裁决主体 -->
  <div style="max-width: 640px;">

    <!-- 最终推荐句（大字，点橙） -->
    <h2 style="
      font-family: 'Smiley Sans Oblique', 'Noto Sans SC', sans-serif;
      font-size: clamp(28px, 4vw, 52px);
      line-height: 1.2;
      color: #FDFAF5;
      margin: 0 0 24px;
    ">
      长文写作首选 <span style="color: #C87A45;">Claude</span>，<br>
      快速出稿首选 <span style="color: #C87A45;">ChatGPT Plus</span>
    </h2>

    <!-- 推荐理由 -->
    <p style="
      font-size: 15px; font-weight: 300;
      color: #9A9085;
      margin: 0 0 40px;
      line-height: 1.8;
      max-width: 520px;
    ">如果你是内容创作者，且长文是主要工作，Claude 的连贯性优势在实际使用中能感受到。如果你更需要速度和工具集成，ChatGPT Plus 的生态更成熟。两者价格相近，不存在「性价比」差异，区别在使用习惯。</p>

    <!-- CTA 按钮组 -->
    <div style="display: flex; gap: 16px; flex-wrap: wrap;">

      <!-- 主推荐 CTA：琥珀橙底 -->
      <a href="#" style="
        display: inline-flex; align-items: center;
        padding: 12px 28px;
        background: #C87A45;
        color: #FDFAF5;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px; font-weight: 400;
        letter-spacing: 0.05em;
        text-decoration: none;
        border-radius: 2px;
        transition: background 0.2s;
      ">去试试 Claude →</a>

      <!-- 次选 CTA：烟青边框 -->
      <a href="#" style="
        display: inline-flex; align-items: center;
        padding: 12px 28px;
        background: transparent;
        border: 1px solid #6B8590;
        color: #6B8590;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px; font-weight: 400;
        letter-spacing: 0.05em;
        text-decoration: none;
        border-radius: 2px;
      ">去试试 ChatGPT Plus</a>

    </div>

    <!-- 不推荐场景（可选块：当结论是「暂不推荐」时替换上方按钮组） -->
    <!--
    <div style="
      margin-top: 32px;
      padding: 20px 24px;
      border: 1px solid rgba(139,74,74,0.4);
      border-radius: 4px;
    ">
      <div style="font-family: 'Space Grotesk', sans-serif; font-size: 11px; letter-spacing: 0.15em; color: #8B4A4A; text-transform: uppercase; margin-bottom: 10px;">暂不推荐</div>
      <p style="font-size: 14px; font-weight: 300; color: #9A9085; margin: 0; line-height: 1.7;">
        Notion AI 在此次测试中未达到同价位工具的水准，中文处理和长文连贯性均低于预期。建议等待后续版本再评估。
      </p>
    </div>
    -->

  </div>

  <!-- 底部元信息 -->
  <div style="
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid rgba(235,228,214,0.15);
    display: flex; gap: 24px; flex-wrap: wrap;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px; color: #6B6157;
  ">
    <span>测评日期：2026-05</span>
    <span>·</span>
    <span>作者：Loki · 赛博小熊猫</span>
    <span>·</span>
    <span>仅代表个人实测结果</span>
  </div>
</section>
```

---

## 四、装饰命名索引

> 所有装饰元素必须用这些名称，不用随意 class 名。

| 装饰名 | 用在哪个组件 | 视觉描述 |
|--------|-------------|---------|
| `summary-line` | Summary 执行摘要 | 琥珀橙左竖线，客观结论的视觉锚点 |
| `score-bar` | Scorecard 评分表格 | 进度条，宽度=分值/满分，颜色=等级色 |
| `verdict-tag` | Scorecard 评分表格 | 分值数字标签，颜色跟随等级色 |
| `evidence-mark` | Evidence 截图证据区 | 圆圈或箭头标注，红色=问题/橙色=亮点 |
| `evidence-frame` | Evidence 截图证据区 | 截图外层容器，暖色边框 |
| `my-take-line` | MyTake 作者观点框 | 苔绿左竖线，主观判断的唯一视觉标记，禁止改色 |

---

## 五、颜色语义速查（本场景）

```
优秀  → var(--amber)   #C87A45  ←→  score-bar + verdict-tag
良好  → var(--smoke)   #6B8590  ←→  score-bar + verdict-tag
一般  → var(--text-muted) #9A9085 ←→ score-bar + verdict-tag
差    → #8B4A4A              ←→  score-bar + evidence-mark（问题标注）
主观  → #7A8458 苔绿           ←→  my-take-line（唯一专属，不共享）

琥珀橙和苔绿绝对不可互换：
  琥珀橙 = 优秀 / CTA / 客观高亮
  苔绿   = 作者主观 / My Take 专属
```

---

## 六、本场景禁止清单

> 以下任何一条出现即需返工。

### 颜色
- [ ] 表格边框使用冷灰色（必须用 `var(--oat)` `#EBE4D6` 暖色边框）
- [ ] My Take 左竖线使用琥珀橙（必须是苔绿 `#7A8458`）
- [ ] 评级颜色语义混乱（优秀用了烟青，或苔绿用在了评分上）
- [ ] 出现蓝紫渐变 / glassmorphism / 科技蓝银灰

### 结构
- [ ] My Take 块没有「Loki」署名标头
- [ ] My Take 块里出现评分数字
- [ ] 同一页面苔绿出现在 My Take 以外的组件
- [ ] 封面放了评分结论（那是剧透）
- [ ] 结论卡用了浅底

### 内容
- [ ] Summary 结论句超过 30 字
- [ ] Matrix 表格单元格放了超过 10 字的句子
- [ ] Evidence 截图没有标注就放进去了
- [ ] Evidence 标注超过 3 处
- [ ] 结论卡写「各有优劣，按需选择」

### 字体
- [ ] 数据大字用了加粗（Space Grotesk weight 200 才是正确选择）
- [ ] 正文用了 weight 500+ 加粗（除非是结论句）
- [ ] 眉毛标签（eyebrow）没有 letter-spacing

---

*场景文件：scene-report.md · 赛博小熊猫 Loki 设计系统 · 2026-05-27*
