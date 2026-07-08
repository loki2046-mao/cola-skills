# 公众号排版组件库

> **设计来源**：嫁接甲木×摸鱼小李 gzh-design-skill 的完整设计语言（杂志封面/目录/多层强调/布局组件/互动三连），配色用 Loki 12套体系（与 loki-social/loki-deck 共用）。
>
> **配色与组件分离**：本组件库只有一份，配色从 `theme-index.md` 的12套里选，运行时替换变量。所有 `{{xxx}}` 占位符替换为所选配色的实际色值。
>
> **平台兼容铁律**：所有文字节点用 `<span leaf="">` 包裹；装饰性空元素（圆点、渐变线、装饰短横、时间线竖线）内部放 `<span leaf=""><br></span>` 占位；禁 `<style>/<script>/class/id/div/position:fixed/absolute/float/@media/@keyframes/display:grid`；不用 `white-space:pre`；图片用 `max-width:100%`；不要把 `font-size`/`border-bottom` 打在 `<strong>` 上，拆成多个 `<p>`，每个只有一个字号。
>
> **内容保真铁律（最高优先级）**：排版时不修改用户的文字内容和图片内容。原文的每一个字必须原样保留，不增删、不改写、不替换。唯一允许的调整：段落拆分合并、标题层级推断、强调样式添加、标点全角化、章节编号添加、图注添加。原文有明显错误时保持原样，在交付时提醒用户。

---

## 设计变量

| 变量 | 用途 | 来源 |
|------|------|------|
| `{{bg}}` | 底色 | theme-index |
| `{{bg2}}` | 次级背景（卡片/引用块底） | theme-index |
| `{{accent}}` | 主色 | theme-index |
| `{{accent2}}` | 辅色（渐变搭档） | theme-index |
| `{{accent-light}}` | 主色浅装饰（渐变浅端/浅边框） | accent 混白 |
| `{{accent-soft}}` | 主色浅底（标签/提示块底色） | accent 8-10% 透明度 |
| `{{accent-border}}` | 主色浅边框 | accent 15% 透明度 |
| `{{highlight}}` | 黄色高亮（点缀色，跨配色统一用 `#FDE68A`） | 固定 |
| `{{highlight-bg}}` | 黄色警告底色 `#FFFBEB` | 固定 |
| `{{highlight-text}}` | 黄色警告文字 `#92400E` | 固定 |
| `{{red-line}}` | 红色下划线（对比/否定专用 `#FECACA`） | 固定 |
| `{{title}}` | 标题色（深色，高对比） | theme-index text |
| `{{body}}` | 正文色 | theme-index text-sub |
| `{{caption}}` | 注释/标签色 | theme-index text-mute |
| `{{ghost}}` | 极淡文字/删除线旧概念色 | theme-index text-ghost |
| `{{border}}` | 细边框 `#E5E7EB` | 固定（浅底）/ 半透明白（深底） |
| `{{bg-gray}}` | 浅灰背景 `#F3F4F6` | 固定（浅底）/ bg2（深底） |
| `{{bg-gray-light}}` | 极浅灰 `#F9FAFB` | 固定（浅底）/ bg2变体（深底） |

字体栈：`-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif`

---

## 组件 1 全局容器

```html
<section style="max-width:677px;margin:0 auto;padding:0 20px;background:{{bg-gray-light}};font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:{{body}};line-height:1.75;letter-spacing:0.5px;overflow-x:hidden;">
  <!-- 所有组件放在这里 -->
</section>
```

**深底配色**：`background:{{bg}}`，`color:{{body}}` 用浅色文字。
**浅底配色**：`background:{{bg-gray-light}}` 或 `#ffffff`，`color:{{body}}` 用深色文字。

---

## 组件 2 封面 cover-breaking（杂志快讯封面）

> **文案策略**：封面标题和公众号外标题是两层标题，视角错开。外标题卖"为什么点开"，封面卖"里面讲什么"。已知外标题时禁止原样复述核心关键词；未知时从五个视角（数字反差/角色革命/案例串/方法论/情绪钩子）自选一个直出。

**有右侧图片版**：

```html
<section style="margin:0 0 32px;background:#fff;border:1.5px solid {{accent-border}};border-radius:20px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.06);width:100%;">
  <section style="padding:32px 28px 28px;">
    <section style="display:flex;align-items:center;gap:8px;margin-bottom:28px;">
      <span style="width:6px;height:6px;background:{{accent}};border-radius:50%;"><span leaf=""><br></span></span>
      <span style="font-size:11px;font-weight:700;letter-spacing:3px;color:{{accent}};"><span leaf="">{{顶部标签}}</span></span>
      <section style="flex:1;height:1px;overflow:hidden;background:linear-gradient(to right,{{accent-border}},transparent);"><span leaf=""><br></span></section>
      <span style="font-size:10px;color:{{ghost}};font-weight:600;"><span leaf="">{{日期}}</span></span>
    </section>
    <section style="display:flex;align-items:center;gap:20px;">
      <section style="flex:1;min-width:0;">
        <p style="font-size:15px;color:{{ghost}};margin:0 0 6px;text-decoration:line-through;letter-spacing:0.5px;">
          <span leaf="">{{划线旧认知}}</span>
        </p>
        <p style="font-size:24px;font-weight:900;color:{{title}};margin:0;line-height:1.05;letter-spacing:-2px;">
          <span leaf="">{{主标题行1}}</span>
          <span style="color:{{accent}};"><span leaf="">{{高亮词}}</span></span>
        </p>
        <p style="font-size:24px;font-weight:900;color:{{accent}};margin:0 0 16px;line-height:1.05;letter-spacing:-2px;">
          <span leaf="">{{主标题行2}}</span>
        </p>
        <section style="width:48px;height:3px;background:linear-gradient(to right,{{accent}},{{accent2}});border-radius:2px;margin-bottom:12px;">
          <span leaf=""><br></span>
        </section>
        <p style="font-size:13px;color:{{caption}};margin:0;line-height:1.7;letter-spacing:0.5px;">
          <span leaf="">{{副标题关键词}}</span>
        </p>
      </section>
      <section style="flex-shrink:0;width:110px;height:110px;border-radius:16px;overflow:hidden;border:1px solid {{accent-border}};box-shadow:0 4px 12px rgba(0,0,0,0.06);">
        <span leaf=""><img src="{{url}}" style="max-width:100%;height:auto;display:block;"></span>
      </section>
    </section>
  </section>
  <section style="background:linear-gradient(135deg,{{accent}},{{accent2}});padding:12px 28px;display:flex;align-items:center;justify-content:space-between;">
    <p style="font-size:12px;color:rgba(255,255,255,0.9);margin:0;font-weight:600;letter-spacing:0.5px;">
      <span leaf="">{{底部左侧文字}}</span>
    </p>
    <section style="display:flex;gap:4px;">
      <span style="background:rgba(255,255,255,0.2);padding:1px 6px;border-radius:3px;font-size:8px;color:#fff;font-weight:600;"><span leaf="">{{标签1}}</span></span>
      <span style="background:rgba(255,255,255,0.2);padding:1px 6px;border-radius:3px;font-size:8px;color:#fff;font-weight:600;"><span leaf="">{{标签2}}</span></span>
    </section>
  </section>
</section>
```

**无右侧图片版**（标题区满宽）：同上去掉右侧图片 section。

---

## 组件 3 目录 toc-scroll（横向滚动目录）

2 个及以上章节时生成。第一个卡片主色高亮，最后一个固定为"写在最后"（PART ///）。

```html
<section style="margin:0 0 32px;">
  <section style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
    <p style="font-size:10px;color:{{caption}};margin:0;text-transform:uppercase;letter-spacing:2px;font-weight:600;">
      <span leaf="">📦 {{N}} Parts + Conclusion</span>
    </p>
    <p style="font-size:10px;color:{{caption}};margin:0;">
      <span leaf="">👉 滑动</span>
    </p>
  </section>
  <section style="overflow-x:scroll;-webkit-overflow-scrolling:touch;white-space:nowrap;padding-bottom:8px;">
    <!-- 第一个（主色高亮） -->
    <section style="display:inline-block;white-space:normal;vertical-align:top;width:110px;background:linear-gradient(135deg,{{accent}},{{accent2}});border-radius:12px;padding:12px;margin-right:8px;">
      <p style="font-size:9px;font-weight:700;color:rgba(255,255,255,0.7);letter-spacing:1px;margin:0 0 5px;"><span leaf="">PART 01</span></p>
      <p style="font-size:13px;font-weight:800;color:#fff;margin:0 0 3px;"><span leaf="">{{章节名}}</span></p>
      <p style="font-size:10px;color:rgba(255,255,255,0.7);margin:0;"><span leaf="">{{副标题}}</span></p>
    </section>
    <!-- 后续（白底） -->
    <section style="display:inline-block;white-space:normal;vertical-align:top;width:110px;background:#fff;border:1px solid {{border}};border-radius:12px;padding:12px;margin-right:8px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
      <p style="font-size:9px;font-weight:700;color:{{caption}};letter-spacing:1px;margin:0 0 5px;"><span leaf="">PART 02</span></p>
      <p style="font-size:13px;font-weight:800;color:{{title}};margin:0 0 3px;"><span leaf=">{{章节名}}</span></p>
      <p style="font-size:10px;color:{{caption}};margin:0;"><span leaf=">{{副标题}}</span></p>
    </section>
    <!-- 最后一个（写在最后） -->
    <section style="display:inline-block;white-space:normal;vertical-align:top;width:110px;background:#fff;border:1px solid {{border}};border-radius:12px;padding:12px;box-shadow:0 2px 6px rgba(0,0,0,0.04);">
      <p style="font-size:9px;font-weight:700;color:{{caption}};letter-spacing:1px;margin:0 0 5px;"><span leaf="">PART ///</span></p>
      <p style="font-size:13px;font-weight:800;color:{{title}};margin:0 0 3px;"><span leaf="">写在最后</span></p>
      <p style="font-size:10px;color:{{caption}};margin:0;"><span leaf=">{{副标题}}</span></p>
    </section>
  </section>
</section>
```

---

## 组件 4 章节标题 chapter-title

第一个章节 `margin-top:16px`，后续 `margin-top:48px`。末章编号 `///`，PART 改 `LAST`。

```html
<section style="margin-top:48px;margin-bottom:32px;">
  <section style="display:flex;align-items:center;gap:16px;margin-bottom:24px;">
    <section style="text-align:center;flex-shrink:0;">
      <p style="margin:0;font-size:28px;font-weight:900;color:{{accent}};line-height:1;letter-spacing:-2px;">
        <span leaf=">{{01}}</span>
      </p>
      <p style="margin:0;font-size:8px;font-weight:700;color:{{ghost}};letter-spacing:2px;">
        <span leaf="">PART</span>
      </p>
    </section>
    <span style="width:1px;height:36px;background:{{border}};flex-shrink:0;"><span leaf=""><br></span></span>
    <section>
      <p style="margin:0 0 1px;font-size:17px;font-weight:900;color:{{title}};letter-spacing:0.3px;">
        <span leaf=">{{中文标题}}</span>
      </p>
      <p style="margin:0;font-size:11px;font-weight:600;color:{{caption}};letter-spacing:1.5px;">
        <span leaf=">{{ENGLISH · 英文副标题}}</span>
      </p>
    </section>
  </section>
</section>
```

---

## 组件 5 正文段落 paragraph

```html
<p style="margin:0 0 16px;font-size:14px;line-height:1.9;text-align:justify;">
  <span leaf=">{{正文内容}}</span>
</p>
```

段间距较大时用 `margin-bottom:24px`。

---

## 组件 6 行内强调（9 种 + 使用原则）

### 6a. 主色加粗（核心概念、关键结论、品牌名）

```html
<strong style="color:{{accent}};"><span leaf="">文字</span></strong>
```

### 6b. 主色背景标签

```html
<strong style="color:{{accent}};background:{{accent-soft}};padding:0 4px;border-radius:2px;"><span leaf="">文字</span></strong>
```

### 6c. 黄色渐变高亮（一段话中最想让读者注意的短语，每段 ≤1-2 处）

```html
<span style="background:linear-gradient(120deg,{{highlight}} 0%,rgba(255,255,255,0) 100%);padding:0 4px;border-radius:2px;font-weight:600;color:{{title}};"><span leaf="">文字</span></span>
```

### 6d. 黄色底部高亮（下划线效果）

```html
<span style="color:{{title}};font-weight:bold;border-bottom:3px solid {{highlight}};"><span leaf="">文字</span></span>
```

### 6e. 主色下划线（正文关键词默认标记）

```html
<span style="border-bottom:2px solid {{accent-light}};font-weight:600;"><span leaf="">文字</span></span>
```

### 6f. 红色下划线（对比、否定）

```html
<span style="border-bottom:2px solid {{red-line}};"><span leaf="">文字</span></span>
```

### 6g. 代码标签

```html
<span style="background:{{bg-gray}};color:{{title}};padding:2px 6px;border-radius:4px;font-size:13px;font-weight:600;"><span leaf="">code</span></span>
```

### 6h. 获取方式标签（黄色背景）

```html
<span style="background:{{highlight}};color:{{title}};padding:2px 6px;border-radius:4px;font-size:13px;font-weight:700;"><span leaf="">「关键词」</span></span>
```

### 6i. 删除线灰色（旧概念）

```html
<span style="background:{{bg-gray}};color:{{caption}};padding:2px 6px;border-radius:4px;font-size:13px;text-decoration:line-through;font-weight:600;"><span leaf="">旧词</span></span>
```

**使用原则**：
1. 主色加粗用于核心概念、关键结论、品牌名
2. 黄色高亮每段 ≤1-2 处
3. 主色下划线用于次要强调（正文关键词逐段标记）
4. 红色下划线只用于对比/否定
5. 一段文字中不超过 2 种高亮效果

---

## 组件 7 内容标签（STEP / CASE / TOOL）

### 7a. step-label

```html
<section style="margin-bottom:24px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:{{title}};color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;"><span leaf="">STEP 01</span></span>
    <h4 style="font-size:15px;font-weight:800;color:{{title}};margin:0;">
      <span leaf=">{{步骤标题}}</span>
    </h4>
  </section>
  <p style="font-size:14px;margin:0 0 16px;color:{{body}};line-height:1.9;text-align:justify;">
    <span leaf=">{{步骤内容}}</span>
  </p>
</section>
```

### 7b. case-label

```html
<section style="margin-bottom:28px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:{{border}};color:{{caption}};font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;"><span leaf="">CASE 01</span></span>
    <h4 style="font-size:15px;font-weight:800;color:{{title}};margin:0;">
      <span leaf=">{{案例标题}}</span>
    </h4>
  </section>
</section>
```

### 7c. tool-label

```html
<section style="margin-bottom:28px;">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="display:inline-block;background:{{title}};color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;"><span leaf="">TOOL 1</span></span>
    <h4 style="font-size:15px;font-weight:800;color:{{title}};margin:0;">
      <span leaf=">{{名称}}</span>
    </h4>
  </section>
</section>
```

---

## 组件 8 代码/Prompt

### 8a. prompt-block

```html
<p style="font-size:13px;color:{{body}};margin:0 0 16px;line-height:1.8;">
  <span style="display:inline-block;background:{{accent}};color:#fff;font-size:11px;font-weight:700;padding:1px 7px;border-radius:3px;margin-right:6px;vertical-align:middle;letter-spacing:0.5px;"><span leaf="">PROMPT</span></span>
  <span style="font-size:12px;color:{{caption}};font-weight:700;"><span leaf=">{{提示词内容}}</span></span>
</p>
```

### 8b. cmd-block

```html
<p style="font-size:13px;color:{{body}};margin:0 0 24px;line-height:1.8;">
  <span style="display:inline-block;background:{{title}};color:#fff;font-size:11px;font-weight:700;padding:1px 7px;border-radius:3px;margin-right:6px;vertical-align:middle;letter-spacing:0.5px;"><span leaf="">CMD</span></span>
  <span style="background:{{bg-gray}};color:{{title}};padding:2px 6px;border-radius:4px;font-size:13px;font-weight:600;"><span leaf=">{{命令内容}}</span></span>
</p>
```

### 8c. 多行代码块

```html
<section style="margin:0 0 20px;border-radius:8px;overflow:hidden;background:#1E293B;">
  <section style="padding:8px 14px;background:#0F172A;">
    <span style="font-size:11px;color:#64748B;font-family:Consolas,Monaco,monospace;letter-spacing:1px;"><span leaf=">{{语言名}}</span></span>
  </section>
  <section style="padding:11px 14px;">
    <p style="margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf=">{{第一行}}</span></p>
    <p style="margin:0;font-family:'SF Mono',Consolas,Monaco,monospace;font-size:13px;line-height:1.6;color:#E2E8F0;"><span leaf="">　　{{缩进行}}</span></p>
  </section>
</section>
```

---

## 组件 9 引用与亮点

### 9a. quote-box（虚线引用框，引用的默认组件）

```html
<section style="background:{{bg-gray-light}};border:1px dashed {{border}};border-radius:8px;padding:12px 16px;margin-bottom:24px;text-align:justify;">
  <p style="font-size:13px;color:{{body}};margin:0;line-height:1.7;">
    <span leaf=">{{引用内容}}</span>
  </p>
</section>
```

### 9b. oneliner-card（一句话亮点卡片）

单行版：

```html
<section style="background:#fff;border:1px dashed {{accent-border}};border-radius:8px;padding:14px 16px;margin-bottom:24px;text-align:center;">
  <p style="margin:0;line-height:1.6;">
    <span style="font-size:15px;color:{{accent}};font-weight:bold;border-bottom:3px solid {{highlight}};padding-bottom:2px;"><span leaf=">{{亮点内容}}</span></span>
  </p>
</section>
```

带前缀引导语版：

```html
<section style="background:#fff;border:1px dashed {{accent-border}};border-radius:8px;padding:14px 16px;margin-bottom:24px;text-align:center;">
  <p style="font-size:12px;color:{{caption}};margin:0 0 6px;line-height:1.5;">
    <span leaf=">{{引导语}}</span>
  </p>
  <p style="margin:0;line-height:1.6;">
    <span style="font-size:15px;color:{{accent}};font-weight:bold;border-bottom:3px solid {{highlight}};padding-bottom:2px;"><span leaf=">{{亮点内容}}</span></span>
  </p>
</section>
```

### 9c. subtitle-highlight（黄色下划线小节标题）

```html
<p style="font-size:15px;font-weight:900;color:{{title}};margin:0 0 16px;">
  <span style="background:linear-gradient(180deg,transparent 65%,{{highlight}} 65%);padding:0 4px;"><span leaf=">{{小节标题}}</span></span>
</p>
```

### 9d. center-divider（居中金句分隔）

```html
<p style="font-size:14px;margin:0 0 20px;text-align:center;color:{{accent}};font-weight:700;letter-spacing:1px;border-top:1px solid {{border}};border-bottom:1px solid {{border}};padding:12px 0;">
  <span leaf=">{{居中金句}}</span>
</p>
```

### 9e. 斜体旁白（括号里的心理活动）

```html
<p style="margin:16px 0;font-size:13px;line-height:1.8;color:{{caption}};font-style:italic;">
  <span leaf=">{{括号里的心理活动}}</span>
</p>
```

### 9f. 短句独立成段（叙事停顿感）

```html
<p style="margin:0 0 20px;font-size:16px;line-height:1.7;color:{{title}};font-weight:600;">
  <span leaf=">{{一个短句}}</span>
</p>
```

---

## 组件 10 提示与信息

### 10a. warn-tip（踩坑提示）

```html
<section style="padding:6px 0 4px;margin-bottom:16px;">
  <p style="margin:0 0 6px;font-size:12px;font-weight:700;color:{{caption}};letter-spacing:1px;">
    <span style="color:rgb(255,76,0);"><span leaf="">！踩坑提示 🕳</span></span>
  </p>
  <p style="font-size:13px;color:{{body}};margin:0;line-height:1.7;">
    <span style="color:{{caption}};font-weight:bold;"><span leaf=">{{提示内容}}</span></span>
  </p>
</section>
```

### 10b. accent-tip（主色提示）

```html
<section style="padding:6px 0 4px;margin-bottom:16px;">
  <p style="margin:0 0 6px;font-size:12px;font-weight:700;color:{{caption}};letter-spacing:1px;">
    <span style="color:{{accent}};"><span leaf="">✦ {{提示标题}}</span></span>
  </p>
  <p style="font-size:13px;color:{{body}};margin:0;line-height:1.7;">
    <span leaf=">{{提示内容}}</span>
  </p>
</section>
```

### 10c. yellow-warning（黄色警告框）

```html
<section style="background:{{highlight-bg}};border:1px solid {{highlight}};border-radius:12px;padding:12px 16px;margin-bottom:20px;">
  <p style="font-size:13px;color:{{highlight-text}};margin:0;font-weight:700;">
    <span leaf=">{{警告内容}}</span>
  </p>
</section>
```

### 10d. accent-info（主色信息框）

```html
<section style="background:{{accent-soft}};padding:12px 16px;border-radius:8px;border:1px solid {{accent-border}};margin-bottom:20px;">
  <p style="font-size:13px;color:{{body}};margin:0;line-height:1.7;text-align:justify;">
    <span leaf=">{{信息内容}}</span>
  </p>
</section>
```

---

## 组件 11 布局组件

### 11a. pill-list（胶囊列表）

```html
<section style="margin-bottom:14px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;font-size:13px;font-weight:700;color:{{accent}};background:{{accent-soft}};padding:3px 10px;border-radius:999px;"><span style="display:inline-block;width:6px;height:6px;background:{{accent}};border-radius:50%;margin-right:5px;vertical-align:middle;"><span leaf=""><br></span></span><span leaf=">{{列表项文字}}</span></span>
  </p>
</section>
```

带说明文字版：

```html
<section style="margin-bottom:14px;">
  <p style="margin:0 0 6px;">
    <span style="display:inline-block;font-size:13px;font-weight:700;color:{{accent}};background:{{accent-soft}};padding:3px 10px;border-radius:999px;"><span style="display:inline-block;width:6px;height:6px;background:{{accent}};border-radius:50%;margin-right:5px;vertical-align:middle;"><span leaf=""><br></span></span><span leaf=">{{标题}}</span></span>
  </p>
  <p style="font-size:13px;color:{{body}};margin:0;line-height:1.7;text-align:justify;">
    <span leaf=">{{描述内容}}</span>
  </p>
</section>
```

### 11b. flow-cards（三步横排流程卡片）

```html
<section style="background:{{bg-gray-light}};padding:16px;border-radius:12px;border:1px solid {{border}};margin-bottom:24px;">
  <section style="display:flex;align-items:stretch;justify-content:center;gap:6px;">
    <section style="flex:1;text-align:center;padding:10px 8px;background:linear-gradient(135deg,{{accent}},{{accent2}});border-radius:8px;">
      <p style="font-size:13px;font-weight:800;color:#fff;margin:0 0 3px;"><span leaf=">{{步骤1标题}}</span></p>
      <p style="font-size:10px;color:rgba(255,255,255,0.8);margin:0;line-height:1.5;"><span leaf=">{{步骤1描述}}</span></p>
    </section>
    <section style="display:flex;align-items:center;color:{{ghost}};font-size:14px;padding:0 4px;">
      <span leaf="">→</span>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid {{border}};border-radius:8px;">
      <p style="font-size:13px;font-weight:800;color:{{title}};margin:0 0 3px;"><span leaf=">{{步骤2标题}}</span></p>
      <p style="font-size:10px;color:{{caption}};margin:0;line-height:1.5;"><span leaf=">{{步骤2描述}}</span></p>
    </section>
    <section style="display:flex;align-items:center;color:{{ghost}};font-size:14px;padding:0 4px;">
      <span leaf="">→</span>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid {{accent-border}};border-radius:8px;">
      <p style="font-size:13px;font-weight:800;color:{{accent}};margin:0 0 3px;"><span leaf=">{{步骤3标题}}</span></p>
      <p style="font-size:10px;color:{{caption}};margin:0;line-height:1.5;"><span leaf=">{{步骤3描述}}</span></p>
    </section>
  </section>
  <p style="font-size:12px;color:{{caption}};text-align:center;margin:12px 0 0;letter-spacing:0.5px;">
    <span leaf=">{{底部说明文字}}</span>
  </p>
</section>
```

### 11c. three-col-cards（三列对比卡片）

```html
<section style="background:{{bg-gray-light}};padding:16px;border-radius:12px;border:1px solid {{border}};margin-bottom:28px;">
  <section style="display:flex;align-items:stretch;justify-content:center;gap:6px;">
    <section style="flex:1;text-align:center;padding:10px 8px;background:linear-gradient(135deg,{{accent}},{{accent2}});border-radius:8px;">
      <p style="font-size:13px;font-weight:800;color:#fff;margin:0 0 3px;"><span leaf=">{{卡片1标题}}</span></p>
      <p style="font-size:10px;color:rgba(255,255,255,0.8);margin:0;line-height:1.5;"><span leaf=">{{卡片1描述}}</span></p>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid {{border}};border-radius:8px;">
      <p style="font-size:13px;font-weight:800;color:{{title}};margin:0 0 3px;"><span leaf=">{{卡片2标题}}</span></p>
      <p style="font-size:10px;color:{{caption}};margin:0;line-height:1.5;"><span leaf=">{{卡片2描述}}</span></p>
    </section>
    <section style="flex:1;text-align:center;padding:10px 8px;background:#fff;border:1px solid {{border}};border-radius:8px;">
      <p style="font-size:13px;font-weight:800;color:{{title}};margin:0 0 3px;"><span leaf=">{{卡片3标题}}</span></p>
      <p style="font-size:10px;color:{{caption}};margin:0;line-height:1.5;"><span leaf=">{{卡片3描述}}</span></p>
    </section>
  </section>
</section>
```

### 11d. timeline（时间线列表）

```html
<section style="display:flex;margin-bottom:28px;">
  <section style="display:flex;flex-direction:column;align-items:center;margin-right:16px;flex-shrink:0;">
    <section style="width:14px;height:14px;border-radius:50%;border:3px solid {{accent}};background:#fff;margin-top:4px;box-shadow:0 0 0 2px #fff;">
      <span leaf=""><br></span>
    </section>
    <section style="width:2px;background:{{border}};flex:1;margin-top:4px;min-height:48px;">
      <span leaf=""><br></span>
    </section>
  </section>
  <section style="flex:1;padding-bottom:12px;">
    <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;">
      <span style="display:inline-block;background:{{title}};color:#fff;font-size:10px;font-weight:700;padding:2px 8px;border-radius:12px;"><span leaf=">{{CASE 01}}</span></span>
      <h4 style="font-size:15px;font-weight:800;color:{{title}};margin:0;">
        <span leaf=">{{标题}}</span>
      </h4>
    </section>
    <p style="font-size:11px;font-weight:600;color:{{caption}};letter-spacing:1px;margin:0 0 12px;">
      <span leaf=">{{英文副标题}}</span>
    </p>
    <p style="font-size:14px;margin:0 0 16px;color:{{body}};line-height:1.7;text-align:justify;">
      <span leaf=">{{内容}}</span>
    </p>
  </section>
</section>
```

### 11e. tool-card（工具说明卡片）

```html
<section style="background:#fff;border-radius:12px;padding:16px 20px;box-shadow:0 4px 16px {{accent-border}};margin-bottom:24px;">
  <p style="font-size:13px;color:{{body}};margin:0;line-height:1.8;">
    <span leaf=">{{说明内容}}</span>
  </p>
</section>
```

### 11f. table（表格）

```html
<section style="margin-bottom:24px;overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;font-size:13px;">
    <thead>
      <tr>
        <th style="background:{{accent}};color:#fff;font-weight:700;padding:8px 12px;text-align:left;"><span leaf=">{{列标题1}}</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid {{border}};color:{{body}};"><span leaf=">{{内容}}</span></td>
      </tr>
      <tr>
        <td style="padding:8px 12px;border-bottom:1px solid {{border}};color:{{body}};background:{{bg-gray-light}};"><span leaf=">{{内容}}</span></td>
      </tr>
    </tbody>
  </table>
</section>
```

### 11g. ordered-list（编号列表）

```html
<section style="margin-bottom:24px;">
  <section style="display:flex;align-items:flex-start;gap:10px;margin-bottom:12px;">
    <span style="display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:{{accent}};color:#fff;font-size:11px;font-weight:700;border-radius:50%;flex-shrink:0;margin-top:2px;"><span leaf="">1</span></span>
    <p style="font-size:14px;color:{{body}};margin:0;line-height:1.9;flex:1;">
      <span leaf=">{{列表项内容}}</span>
    </p>
  </section>
</section>
```

---

## 组件 12 媒体组件

### 12a. image（图片容器 + 图注）

```html
<section style="margin:0 0 6px;text-align:center;border-radius:12px;overflow:hidden;border:1px solid {{accent-border}};box-shadow:0 4px 16px rgba(0,0,0,0.06);">
  <span leaf=""><img src="{{url}}" style="max-width:100%;height:auto;display:block;margin:0 auto;"></span>
</section>
<p style="font-size:12px;color:{{caption}};text-align:center;margin:0 0 24px;">
  <span leaf=">{{图注}}</span>
</p>
```

### 12b. video-card（视频说明卡）

```html
<section style="background:#fff;border-radius:16px;padding:12px;margin-bottom:32px;border:2px solid {{accent}};box-shadow:0 4px 12px {{accent-border}};">
  <section style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
    <span style="width:8px;height:8px;background:{{accent}};border-radius:50%;"><span leaf=""><br></span></span>
    <span style="font-size:11px;color:{{accent}};font-weight:700;letter-spacing:1px;"><span leaf="">VIDEO 01</span></span>
    <span style="flex:1;height:1px;background:linear-gradient(to right,{{accent-border}},transparent);"><span leaf=""><br></span></span>
    <span style="font-size:11px;color:{{caption}};"><span leaf=">{{视频描述}}</span></span>
  </section>
  <section style="border-radius:10px;overflow:hidden;">
    <span leaf=""><!-- 保留原始视频代码不修改 --></span>
  </section>
</section>
```

### 12c. 待补素材占位

```html
<section style="margin:24px 0;padding:30px 20px;border:1.5px dashed {{accent-border}};border-radius:10px;background:{{bg-gray-light}};text-align:center;">
  <p style="margin:0 0 8px;font-size:24px;line-height:1;"><span leaf="">🖼</span></p>
  <p style="margin:0;font-size:13px;color:{{caption}};line-height:1.6;"><span leaf="">此处插入：{{说明}}</span></p>
</section>
```

---

## 组件 13 结尾组件

### 13a. footer-cta（互动三连区）

```html
<section style="background:radial-gradient(circle at center,{{bg-gray-light}} 0%,#fff 100%);border:1px solid {{border}};border-radius:16px;padding:32px 20px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.03);margin:0 0 24px;">
  <p style="font-size:13px;font-weight:bold;color:{{title}};margin-bottom:20px;line-height:1.6;">
    <span leaf="">既然看到这里了，如果觉得有用，随手点个赞、在看、转发三连吧。</span>
  </p>
  <section style="display:flex;justify-content:center;gap:24px;margin-bottom:16px;">
    <section style="text-align:center;color:{{body}};">
      <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#fff;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05);border:1px solid {{bg-gray}};">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3"></path></svg>
      </section>
      <span style="font-size:10px;font-weight:600;"><span leaf="">点赞</span></span>
    </section>
    <section style="text-align:center;color:{{body}};">
      <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:#fff;border-radius:12px;box-shadow:0 2px 4px rgba(0,0,0,0.05);border:1px solid {{bg-gray}};">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"></circle><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path></svg>
      </section>
      <span style="font-size:10px;font-weight:600;"><span leaf="">在看</span></span>
    </section>
    <section style="text-align:center;color:{{accent}};">
      <section style="width:40px;height:40px;display:flex;align-items:center;justify-content:center;margin:0 auto 6px;background:{{accent-soft}};border-radius:12px;box-shadow:0 2px 4px {{accent-border}};border:1px solid {{accent-border}};">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 18v-4a8 8 0 0 1 8-8h8"></path><polyline points="16 2 20 6 16 10"></polyline></svg>
      </section>
      <span style="font-size:10px;font-weight:600;"><span leaf="">转发</span></span>
    </section>
  </section>
  <p style="font-size:10px;color:{{caption}};letter-spacing:1px;margin:0;">
    <span leaf="">THANKS FOR READING</span>
  </p>
</section>
```

### 13b. 签名区（Loki 固定角色感）

放在 footer-cta 之前。

```html
<section style="margin:24px 0 16px;padding:14px 0;border-top:1px solid {{border}};">
  <p style="margin:0 0 6px;font-size:14px;color:{{title}};line-height:1.8;">
    <span leaf=">{{ps 或个人落款}}</span>
  </p>
  <p style="margin:0;font-size:13px;color:{{caption}};line-height:1.7;">
    <span leaf="">我是 Loki，一只喜欢探索 AI 技术、发掘 AI 趣味的小熊猫。下次见，白白～</span>
  </p>
</section>
```

签名区规则：原文末尾若有作者签名段，合并进这里，不重复生成。固定落款保持不变，除非用户明确要求换。

### 13c. 文末关注引导图

```html
<section style="text-align:center;margin-top:16px;">
  <img src="assets/signature.png" alt="关注引导" style="max-width:100%;height:auto;display:block;margin:0 auto;border-radius:10px;" />
</section>
```

---

## 组件 14 分隔线

```html
<section style="margin:36px 0;text-align:center;">
  <span style="color:{{ghost}};font-size:14px;letter-spacing:0.5em;"><span leaf="">· · ·</span></span>
</section>
```

---

## 完整文章模板骨架

```html
<!-- 1. 封面（组件2 cover-breaking，有图/无图二选一） -->
<!-- 2. 目录（组件3 toc-scroll，2+ 章节时生成，紧跟封面之下） -->
<!-- 3. 开头引言（组件9b oneliner-card，文章有开头金句时） -->
<!-- 4. 前言正文（组件5 段落 ×N） -->
<!-- 5. 第一章（组件4 chapter-title，margin-top:16px） -->
<!--    章内：组件5 正文 + 组件6 行内样式 + 组件7 标签 + 组件8 代码 + 组件9 引用亮点 + 组件10 提示 + 组件11 布局 + 组件12 媒体 -->
<!-- 6. 第二章…第N章（组件4，margin-top:48px） -->
<!-- 7. 结语章（组件4 变体：编号 ///，PART 改 LAST） -->
<!-- 8. 签名区（组件13b） -->
<!-- 9. 互动三连（组件13a footer-cta） -->
<!-- 10. 品牌尾图（组件13c，有素材才加） -->
```

骨架顺序铁律：目录 toc-scroll 必须紧跟封面之下，在开头引言和前言正文之前。

---

## 视觉层级（3 层递进）

| 层级 | 样式 | 用途 | 频率 |
|------|------|------|------|
| **锚点层** | 主色加粗 6a / 黄底下划线 6d / oneliner-card 9b | 核心概念、产品名、关键结论 | 全文 ≤5 处 |
| **标记层** | 主色下划线 6e（默认）/ 黄色渐变高亮 6c | 正文关键词强调 | 每段 1-3 处 |
| **容器层** | quote-box 9a / 提示 10x / 胶囊 11a / 卡片 11x | 引用、旁注、提示、结构化信息 | 按需 |

克制原则：黄色高亮每段 ≤1-2 处；一段内不超过 2 种高亮效果；红色下划线只用于对比/否定；渐变主色仅出现在封面底条、目录首卡、流程首卡等结构位。

---

## 松弛感补充原则

在摸鱼小李设计语言基础上增加的松弛感调整：
1. **短句独立成段**（9f）——叙事文节奏停顿，一句独立一段，前后大留白
2. **斜体旁白**（9e）——括号里的内心独白用斜体+caption色，不抢主视觉
3. **justify对齐**——正文用 `text-align:justify`，右边不参差
4. **段间距充足**——正文 `margin-bottom:16px`，段间距大时用 `24px`
5. **图注不用"图1"**——用自然语言描述

---

## 文章类型 → 组件组合配方

| 文章类型 | 核心组件组合 | 点缀组件 |
|---|---|---|
| 教程/操作指南 | step-label 7a + cmd/prompt 8a/8b + 代码块 8c | warn-tip 10a、flow-cards 11b |
| 盘点/工具清单 | tool-label 7c + tool-card 11e + pill-list 11a | table 11f、oneliner-card 9b |
| 观点/深度分析 | paragraph 5 + quote-box 9a + oneliner-card 9b | center-divider 9d、subtitle-highlight 9c |
| 访谈/人物特稿 | paragraph 5 + quote-box 9a + timeline 11d | oneliner-card 9b、center-divider 9d |
| 个人叙事/情感 | paragraph 5 + 短句独立成段 9f + 斜体旁白 9e + oneliner-card 9b | quote-box 9a、center-divider 9d |
| 数据复盘/报告 | three-col-cards 11c + table 11f + ordered-list 11g | accent-info 10d、黄色渐变高亮 6c |
| 案例实战 | case-label 7b / timeline 11d + step-label 7a | prompt-block 8a、yellow-warning 10c |

所有类型共用固定结构：封面 2 + 目录 3 + 章节标题 4 + 签名/三连 13。

---

## Markdown → 组件映射

| Markdown 元素 | 对应组件 |
|---|---|
| `# 标题` | 封面主标题（组件2，视角错开） |
| 文章开头 `> 引言` | 组件9b oneliner-card |
| `## 章节标题` | 组件4 chapter-title |
| `### 子标题` | 组件9c subtitle-highlight |
| 普通段落 | 组件5 paragraph（每段标1-3处6e） |
| `**加粗**` | 组件6a 主色加粗 |
| `==高亮==` | 组件6c 黄色渐变高亮 |
| `<u>下划线</u>` | 组件6e 主色下划线 |
| `~~删除线~~` | 组件6i 删除线灰色 |
| `> 引用` | 组件9a quote-box |
| 核心金句 | 组件9b oneliner-card / 9d center-divider |
| 操作步骤 | 组件7a step-label |
| 案例/场景 | 组件7b case-label / 11d timeline |
| 技能/工具 | 组件7c tool-label + 11e tool-card |
| Prompt | 组件8a prompt-block |
| 单行命令 | 组件8b cmd-block |
| 多行代码 | 组件8c 多行代码块 |
| 行内 `` `code` `` | 组件6g 代码标签 |
| 并列要点 | 组件11a pill-list |
| 流程（3步） | 组件11b flow-cards |
| 三项对比 | 组件11c three-col-cards |
| 时间脉络 | 组件11d timeline |
| 表格 | 组件11f table |
| `1. 2. 3.` | 组件11g ordered-list |
| 注意/警告 | 组件10a warn-tip / 10c yellow-warning |
| 图片 | 组件12a image |
| 视频 | 组件12b video-card |
| `---` | 组件14 分隔线 |
| 文末 | 组件13b签名 + 13a footer-cta + 13c尾图 |
