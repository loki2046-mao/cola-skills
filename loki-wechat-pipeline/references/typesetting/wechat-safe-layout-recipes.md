# 公众号安全模块参考

这个参考文件用于给 `typesetting-wechat-articles` 提供稳定、可复用的排版骨架。

目标不是花样越多越好，而是让公众号后台里"稳定、耐看、深浅色兼容尽量好"的模块能重复使用。

## 平台兼容铁律

以下规则对所有模块通用，修改组件 HTML 时必须遵守：

- **所有文字节点**必须用 `<span leaf="">文字</span>` 包裹——公众号编辑器会重写未包裹的文字节点，导致粘贴后样式整片丢失
- **装饰性空元素**（圆点、渐变分割线、装饰短横、时间线竖线）内部必须放 `<span leaf=""><br></span>` 占位，否则微信会剥掉样式
- **不要把 `font-size`/`border-bottom` 打在 `<strong>` 上**，也不要在同一个 `<p>` 里混多个不同 `font-size`——微信编辑器会自动"纠正"导致样式被重写。正确做法：拆成多个 `<p>`，每个 `<p>` 只有一个字号；高亮样式统一挂在外层 `<span>` 上
- **禁用** `<style>`/`<script>`/`<div>`、`class`/`id` 属性、`position:fixed/absolute/sticky`、`float`、`@media`/`@keyframes`、`display:grid`、CSS 变量、外部字体/CSS
- **可用** 内联 `style`、`display:flex`（有限）、`linear-gradient`、`border-radius`、`box-shadow`、`<section>/<p>/<span>/<strong>/<img>/<h2>/<h3>`
- **强调用左竖条/药丸标签，不用四周虚线框**（`border: dashed`）——虚线框笨重抢戏。唯一例外：`待补素材占位`可用居中虚线框
- **图片用 `max-width:100%` 而非 `width:100%`**——小图不被拉伸变糊
- **不用 `white-space:pre`**——用"每行一个 `<p style="margin:0">`"+全角空格 `　` 缩进

## 基础排版参数

默认正文参数：

- 段落字号：`15px`
- 行高：`1.9` 到 `2`
- 段落下边距：`14px` 到 `18px`
- 一级小节标题字号：`22px`
- 二级小节标题字号：`18px`
- 模块上下留白：`24px` 到 `32px`
- 图片圆角：`10px` 到 `14px`

## 字体方向

如果用户希望更有设计感、杂志感，优先采用下面的字体策略：

- 标题优先使用衬线风格：
  - `"Source Han Serif SC"`
  - `"Noto Serif SC"`
  - `"Songti SC"`
  - `"STSong"`
  - `serif`
- 正文可根据风格选择：
  - 杂志感更强：正文也使用衬线
  - 可读性优先：正文保留无衬线，标题用衬线
- 标题不宜过粗过黑，优先用较大的字号、较松的留白和细节装饰建立高级感

## 配色选择方法

先看内容类型，再选配色。

### 1. 清醒青灰

适合：

- 教程
- 工具测评
- AI 资讯
- 方法论

色值：

- `accent`: `#5F8F82`
- `accent_deep`: `#426E63`
- `accent_soft`: `#EDF4F1`
- `line`: `#CFE0DA`
- `title`: `#2C3A36`
- `caption`: `#72817B`

### 2. 温暖棕橘

适合：

- 故事
- 个人表达
- 观后感
- 品牌感文章

色值：

- `accent`: `#B97A58`
- `accent_deep`: `#966045`
- `accent_soft`: `#F8EFE9`
- `line`: `#E6D2C5`
- `title`: `#3A302B`
- `caption`: `#837168`

### 3. 杂志暖调

适合：

- 个人表达
- 观点文
- 专题长文
- 更想要"高级感"而不是"科技感"的文章

色值：

- `accent`: `#C46E45`
- `accent_deep`: `#9E5534`
- `accent_soft`: `#F3E6DB`
- `line`: `#DECDBF`
- `title`: `#2E241E`
- `caption`: `#7B6A5E`
- `paper`: `#F8F2EC`

如果用户希望"白底主页面，只在局部出现暖色"，优先这样使用：

- 页面主背景保持白色或接近白色
- 暖色只放在：标签、小底板、重点模块、图片衬底、画廊区域
- 暖色优先往 `橙黄色` 方向偏，不要偏粉棕太多

推荐替代值：

- `accent`: `#D68A2E`
- `accent_deep`: `#A86418`
- `accent_soft`: `#F8ECD7`
- `line`: `#E7D7BE`
- `paper`: `#FFFDF9`

### 4. 杂志蓝调

适合：

- 冷静分析
- 深度观察
- 内容型长文

色值：

- `accent`: `#4D6A86`
- `accent_deep`: `#374D63`
- `accent_soft`: `#E9EFF4`
- `line`: `#CED9E2`
- `title`: `#22303B`
- `caption`: `#677786`
- `paper`: `#F5F7F8`

### 5. 安静蓝紫

适合：

- 观点文
- 趋势分析
- 冷静型总结

色值：

- `accent`: `#6678B8`
- `accent_deep`: `#4E5E97`
- `accent_soft`: `#EEF1FA`
- `line`: `#D8DDF0`
- `title`: `#2F3550`
- `caption`: `#727A93`

## 使用原则

- 全文只选一套主色
- 大段正文不依赖 `accent_soft` 底色
- `accent_soft` 只给短模块、小标签、摘要卡使用
- 深色模式风险较高时，优先保留边线和标题色，减少背景色
- 同一篇文章的所有图片，必须共用同一套圆角和包边参数
- 主色只在锚点出现（全文 ≤5 处），大面积白底 + 灰阶，彩色只做点缀

## 图片统一参数

默认图片参数：

- `image_radius`: `12px`
- `image_border`: `1.5px solid {{line}}`
- `image_shell_bg`: `transparent` 或 `{{accent_soft}}`
- `image_padding`: `4px` 到 `6px`

使用原则：

- 教程、测评、资讯类，优先 `透明底 + 细边框`
- 情绪、故事、品牌感文章，可以用 `浅色衬底 + 细边框`
- 一篇文章选定后，全篇不要混用不同相框语言
- 如果不想要明显"框套框"，就把内外两层距离压到 `4px-8px`
- 这时外层更像阴影边或相纸压边，而不是第二个独立边框
- `<img>` 一律用 `max-width:100%;height:auto;display:block;margin:0 auto`——不用 `width:100%`

## 模块 1：开头引子

适合文章开头第一屏，做轻量定调。

```html
<section style="margin: 8px 0 28px;">
  <section style="display: inline-block; padding: 4px 10px; border-radius: 999px; background: {{accent_soft}}; color: {{accent_deep}}; font-size: 12px; line-height: 1.2; letter-spacing: 0.08em;">
    <span leaf="">{{栏目名或一句短标签}}</span>
  </section>
  <h2 style="margin: 14px 0 10px; font-size: 24px; line-height: 1.45; color: {{title}}; font-weight: 700;">
    <span leaf="">{{开头主标题}}</span>
  </h2>
  <section style="width: 44px; height: 3px; border-radius: 999px; background: {{accent}};">
    <span leaf=""><br></span>
  </section>
</section>
```

注意：

- 开头标签要短，不超过 10 个字
- 不要在这个模块里塞太多说明文字

## 模块 2：正文段落

正文模块尽量保持透明底，减少深色模式风险。

```html
<p style="margin: 0 0 16px; font-size: 15px; line-height: 1.95; text-align: left;">
  <span leaf="">{{正文内容}}</span>
</p>
```

需要轻强调时：

```html
<p style="margin: 0 0 16px; font-size: 15px; line-height: 1.95; text-align: left;">
  <span style="color: {{title}}; font-weight: 700;"><span leaf="">{{需要强调的短句}}</span></span><span leaf="">{{其余正文}}</span>
</p>
```

注意：

- 除非必要，正文段落不要写死 `color`
- 强调只强调短词或短句，不要整段加粗
- 不要把 `font-size` 打在 `<strong>` 上，用 `<span>` 挂样式

## 模块 3：章节标题

这是正文里最常用、也最稳的一种层级模块。

```html
<section style="margin: 30px 0 18px;">
  <section style="display: inline-block; padding: 3px 10px; border-radius: 999px; border: 1px solid {{line}}; color: {{accent_deep}}; font-size: 12px; line-height: 1.2;">
    <span leaf="">{{章节标签}}</span>
  </section>
  <h3 style="margin: 12px 0 0; font-size: 22px; line-height: 1.45; color: {{title}}; font-weight: 700;">
    <span leaf="">{{章节标题}}</span>
  </h3>
</section>
```

注意：

- 章节标签可有可无
- 不要一会儿左对齐一会儿居中，全篇保持一致

## 模块 4：重点提醒

适合短提醒、方法要点、转折句。用左竖条强调，不用四周虚线框。

```html
<section style="margin: 22px 0; padding: 14px 16px; border-left: 4px solid {{accent}}; background: {{accent_soft}}; border-radius: 0 10px 10px 0;">
  <p style="margin: 0; font-size: 14px; line-height: 1.85; color: {{title}};">
    <span leaf="">{{重点提醒内容}}</span>
  </p>
</section>
```

注意：

- 这个模块只放短内容
- 超过 90 字时改回普通正文，不要硬塞进卡片
- 用 `border-left` 左竖条 + 浅底，不要用四周虚线框

深色模式要求更高时，改用这个降级版：

```html
<section style="margin: 22px 0; padding: 0 0 0 14px; border-left: 4px solid {{accent}};">
  <p style="margin: 0; font-size: 14px; line-height: 1.85; color: {{title}};">
    <span leaf="">{{重点提醒内容}}</span>
  </p>
</section>
```

## 模块 5：图片模块

适合单张主图、截图、案例图。

```html
<section style="margin: 24px 0 10px; padding: 4px; border: {{image_border}}; border-radius: {{image_radius}}; background: {{image_shell_bg}}; box-sizing: border-box;">
  <img src="{{image_url}}" alt="{{image_alt}}" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: calc({{image_radius}} - 3px);" />
</section>
```

带图注版本：

```html
<section style="margin: 24px 0 10px; padding: 4px; border: {{image_border}}; border-radius: {{image_radius}}; background: {{image_shell_bg}}; box-sizing: border-box;">
  <img src="{{image_url}}" alt="{{image_alt}}" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: calc({{image_radius}} - 3px);" />
</section>
<p style="margin: 8px 0 18px; font-size: 12px; line-height: 1.7; text-align: center; color: {{caption}};">
  <span leaf="">{{图注}}</span>
</p>
```

注意：

- 图注只在图片承载信息时启用
- 情绪图一般不写图注
- 连续两张图之间至少要有一句承接文字或标题
- 图片用 `max-width:100%` 不用 `width:100%`，小图不被拉伸

## 模块 6：静态画廊感组图

适合双图及以上、但当前任务只能输出纯公众号后台 HTML 的情况。

这个模块不伪装成可交互轮播，而是通过"组标题 + 统一包边 + 组内节奏"做出画廊感。

```html
<section style="margin: 26px 0;">
  <section style="margin: 0 0 12px;">
    <p style="margin: 0; font-size: 13px; line-height: 1.5; color: {{accent_deep}}; letter-spacing: 0.06em;">
      <span leaf="">{{组标签}}</span>
    </p>
    <p style="margin: 6px 0 0; font-size: 18px; line-height: 1.5; color: {{title}}; font-weight: 700;">
      <span leaf="">{{组标题}}</span>
    </p>
  </section>
  <section style="padding: 6px; border: {{image_border}}; border-radius: {{image_radius}}; background: {{image_shell_bg}}; box-sizing: border-box;">
    <img src="{{image_1_url}}" alt="{{image_1_alt}}" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: calc({{image_radius}} - 4px);" />
  </section>
  <p style="margin: 8px 0 14px; font-size: 12px; line-height: 1.7; text-align: center; color: {{caption}};">
    <span leaf="">01 / {{group_total}} {{image_1_caption}}</span>
  </p>
  <section style="padding: 6px; border: {{image_border}}; border-radius: {{image_radius}}; background: {{image_shell_bg}}; box-sizing: border-box;">
    <img src="{{image_2_url}}" alt="{{image_2_alt}}" style="max-width: 100%; height: auto; display: block; margin: 0 auto; border-radius: calc({{image_radius}} - 4px);" />
  </section>
  <p style="margin: 8px 0 0; font-size: 12px; line-height: 1.7; text-align: center; color: {{caption}};">
    <span leaf="">02 / {{group_total}} {{image_2_caption}}</span>
  </p>
</section>
```

扩展规则：

- 三张以上时继续按同样结构追加
- 如果图片非常多，优先拆成多个小画廊组，不要一个组塞到 8 张以上
- 组标题只写一次，图序帮助读者建立"画廊浏览"感觉
- 组图之间要保持相同外框和相同图注格式

## 模块 7：SVG 交互画廊说明

当用户明确要求"真的可以滑"时，按下面原则执行：

- 交互画廊按 `SVG 交互排版` 处理，而不是用纯内联 HTML 假装实现
- 输出时必须明确这是"SVG 交互版画廊"
- 需要同步规划：图片顺序、滑动页数、指示点、首屏封面感、手机端验证
- 如果当前任务没有这类实现条件，再回退到"静态画廊感组图"

## 模块 8：整篇 SVG-first 排版原则

当用户明确接受"整篇都写成 SVG"时，按下面原则执行：

- 不要把文章做成单纯海报拼接，而要保持"文章"而不是"长图海报"的阅读逻辑
- 整篇 SVG 仍然要有明确层级：
  - 开场区
  - 正文分段区
  - 图片区
  - 总结收尾区
- 章节之间必须有明显节奏变化，例如：
  - 间距变化
  - 小标题标签
  - 轻边线分隔
  - 图文穿插
- 整篇 SVG 里，图片包边、角半径、标题标签风格必须保持全篇统一
- 高审美优先来自：
  - 有控制的留白
  - 节制的色彩
  - 统一的几何语言
  - 图文节奏
  - 收放有度的重点模块
- 不要靠大面积复杂背景、夸张阴影、过多贴纸元素制造"设计感"
- 如果用户明确说"不要 AI 味"，优先选 `杂志暖调` 或 `杂志蓝调`，并提高 Serif 标题权重

## 模块 9：长文本缩略卡片

适合：

- 长提示词
- 大段原文摘录
- 成段话术模板
- 多行结构化说明

设计目标：

- 在版面里只占有限高度
- 默认展示前几行，整体看上去像精修过的"内容卡"
- 卡片内部支持 `横向拖拽/滚动` 和 `纵向滚动`
- 不让长文本把整篇图文节奏拖垮

推荐 HTML（长正文摘录，用 `pre-wrap`）：

```html
<section style="margin: 24px 0; padding: 18px; border: 1px solid {{line}}; border-radius: 22px; background: {{paper}};">
  <p style="margin: 0 0 10px; color: {{accent_deep}}; font-size: 12px; font-weight: 600; letter-spacing: 0.08em;">
    <span leaf="">{{标签}}</span>
  </p>
  <section style="max-height: 220px; overflow: auto; padding: 14px 16px; border-radius: 16px; background: #fff; border: 1px solid {{line}}; white-space: pre-wrap; word-break: break-word;">
    <p style="margin: 0; font-size: 14px; line-height: 1.8; color: {{title}};"><span leaf="">{{长文本内容}}</span></p>
  </section>
</section>
```

如果内容里包含超长单行提示词、JSON、代码式结构，**不用 `white-space:pre`**，改用每行一个 `<p>` + 全角空格缩进：

```html
<section style="margin: 24px 0; padding: 18px; border: 1px solid {{line}}; border-radius: 22px; background: {{paper}};">
  <p style="margin: 0 0 10px; color: {{accent_deep}}; font-size: 12px; font-weight: 600; letter-spacing: 0.08em;">
    <span leaf="">{{标签}}</span>
  </p>
  <section style="max-height: 240px; overflow: auto; padding: 14px 16px; border-radius: 16px; background: #fff; border: 1px solid {{line}};">
    <p style="margin: 0; font-size: 13px; line-height: 1.7; color: {{title}}; font-family: 'SF Mono', Consolas, Monaco, monospace;"><span leaf="">{{第一行代码或提示词}}</span></p>
    <p style="margin: 0; font-size: 13px; line-height: 1.7; color: {{title}}; font-family: 'SF Mono', Consolas, Monaco, monospace;"><span leaf="">　　{{缩进的第二行}}</span></p>
    <p style="margin: 0; font-size: 13px; line-height: 1.7; color: {{title}}; font-family: 'SF Mono', Consolas, Monaco, monospace;"><span leaf="">{{第三行}}</span></p>
  </section>
</section>
```

使用原则：

- 长正文摘录优先 `pre-wrap`
- 长提示词、代码、JSON 优先"每行一个 `<p>` + 全角空格缩进"，**不用 `white-space:pre`**
- 卡片高度通常控制在 `180px-260px`
- 卡片标题尽量短，避免头重脚轻
- 如果一篇文章里有多个长文本卡片，样式必须统一

## 模块 10：序列卡片

适合：

- 第一层 / 第二层 / 第三层
- 第一步 / 第二步 / 第三步
- 第一类 / 第二类 / 第三类

推荐做法：

- 数量少时，用竖向堆叠卡片
- 数量固定且信息短时，用横向三栏
- 如果横向会拥挤，就宁可改竖排，不要为了整齐牺牲呼吸感
- **不用 `display:grid`**（公众号不支持），竖排用 `display:flex; flex-direction:column`，横排用 `display:flex`

竖排版本：

```html
<section style="display: flex; flex-direction: column; gap: 12px; margin: 22px 0;">
  <section style="padding: 16px 18px; border: 1px solid {{line}}; border-radius: 18px; background: {{paper}};">
    <p style="margin: 0 0 6px; color: {{accent_deep}}; font-size: 13px; font-weight: 600;"><span leaf="">第一层</span></p>
    <p style="margin: 0; font-size: 15px; line-height: 1.8;"><span leaf="">{{内容}}</span></p>
  </section>
</section>
```

横向版本：

```html
<section style="display: flex; gap: 12px; margin: 22px 0;">
  <section style="flex: 1; padding: 16px 16px 18px; border: 1px solid {{line}}; border-radius: 18px; background: {{paper}};">
    <p style="margin: 0 0 8px; color: {{accent_deep}}; font-size: 13px; font-weight: 600;"><span leaf="">第一步</span></p>
    <p style="margin: 0; font-size: 14px; line-height: 1.75;"><span leaf="">{{内容}}</span></p>
  </section>
  <section style="flex: 1; padding: 16px 16px 18px; border: 1px solid {{line}}; border-radius: 18px; background: {{paper}};">
    <p style="margin: 0 0 8px; color: {{accent_deep}}; font-size: 13px; font-weight: 600;"><span leaf="">第二步</span></p>
    <p style="margin: 0; font-size: 14px; line-height: 1.75;"><span leaf="">{{内容}}</span></p>
  </section>
  <section style="flex: 1; padding: 16px 16px 18px; border: 1px solid {{line}}; border-radius: 18px; background: {{paper}};">
    <p style="margin: 0 0 8px; color: {{accent_deep}}; font-size: 13px; font-weight: 600;"><span leaf="">第三步</span></p>
    <p style="margin: 0; font-size: 14px; line-height: 1.75;"><span leaf="">{{内容}}</span></p>
  </section>
</section>
```

## 模块 11：引用或一句话总结

适合插入观点金句。用左竖条强调。

```html
<section style="margin: 24px 0; padding: 2px 0 2px 16px; border-left: 2px solid {{accent}};">
  <p style="margin: 0; font-size: 17px; line-height: 1.9; color: {{title}}; font-weight: 600;">
    <span leaf="">{{引用句或总结句}}</span>
  </p>
</section>
```

注意：

- 一篇文章最多使用 2 次
- 不要把普通正文硬抬成"金句"

## 模块 12：总结收尾

适合结尾做轻量收束。

```html
<section style="margin: 34px 0 0; padding-top: 18px; border-top: 1px solid {{line}};">
  <p style="margin: 0 0 12px; font-size: 16px; line-height: 1.9; color: {{title}}; font-weight: 600;">
    <span leaf="">{{结尾主句}}</span>
  </p>
  <p style="margin: 0; font-size: 14px; line-height: 1.9; text-align: left;">
    <span leaf="">{{收尾说明}}</span>
  </p>
</section>
```

注意：

- 收尾更适合"轻一点"，不要又上复杂卡片
- CTA 如果有，也要克制

## 模块 13：视频说明卡

这个模块是给"文中有视频，但最终要去微信后台手动插入"的场景用的。

核心原则：

- 不假装能用自定义 HTML 长久包住微信原生视频播放器
- 真正稳定的是"视频前说明卡 + 后台插入视频位"
- 视觉上保留一张封面图或视频截图，再配一句导语

适用方式：

- 上面是一个有圆角和包边的封面卡
- 下面是一句短说明：`下面这段内容建议结合视频一起看`
- 再下面留给用户在微信后台手动插入原生视频

这样就算视频本体被微信替换成平台自己的播放器卡片，前面的设计模块依然保留。

## 模块 14：文末关注引导图

这是硬性收尾模块，不是可选装饰。

规则：

- 全文最后必须有
- 默认单独展示
- 不和总结段落混进一个框里
- 和正文图片区共用同一套圆角和包边语言
- 前面最多只接一小段收尾文案，不要再塞复杂说明

如果用户有固定的关注引导图：

- 优先把它当作全局通用尾图
- 每篇文章都在最后复用

## 推荐搭配

### 教程/测评型

- 开头引子
- 正文段落
- 章节标题
- 图片模块
- 静态画廊感组图
- 整篇 SVG-first 分段结构
- 重点提醒
- 总结收尾
- 视频说明卡
- 文末关注引导图

### 观点/分析型

- 开头引子
- 正文段落
- 章节标题
- 引用模块
- 图片模块
- 静态画廊感组图
- 整篇 SVG-first 分段结构
- 总结收尾
- 视频说明卡
- 文末关注引导图

### 故事/情绪型

- 开头引子
- 正文段落
- 图片模块
- 静态画廊感组图
- 整篇 SVG-first 分段结构
- 引用模块
- 总结收尾
- 文末关注引导图

## 自检原则

最后快速检查：

- 如果把所有背景色删掉，文章还是否清楚
- 是否出现了三种以上强调方式同时抢戏
- 是否有整段长文被关在彩色盒子里
- 是否有图片连续堆叠导致阅读断气
- 是否单图与组图的外框语言完全一致
- 是否组图看起来像一组内容，而不是若干张散图
- 是否整体像"人工编辑排过"，而不是"组件拼接"
- 是否所有文字节点都已用 `<span leaf="">` 包裹
- 是否所有图片都用了 `max-width:100%` 而非 `width:100%`
- 是否有任何强调用了四周虚线框（应该改用左竖条/药丸标签）
- 是否有代码块用了 `white-space:pre`（应该改用每行一个 `<p>` + 全角空格缩进）
- 是否有 `display:grid`（应该改用 `display:flex`）
