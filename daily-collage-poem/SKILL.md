---
name: daily-collage-poem
description: 每日拼贴诗。当用户说"每日拼贴诗""今日诗笺""生成拼贴诗""今天的词条诗"时使用。回顾当天对话内容，提取词条，选择艺术形式，生成拼贴诗。
author: kude
---

# Skill: 每日拼贴诗

**触发词**：每日拼贴诗、今日诗笺、生成拼贴诗、collage poem、今天的词条诗

## 一、Skill 概述

每天晚 7 点（或用户手动触发），回顾当天与用户的对话内容，
提取 10–15 个词条，判断情绪与主题，选择艺术形式，
用 ListenHub 生成背景图，然后输出一份可交互的视觉诗笺 HTML，
保存到 `~/.cola/outputs/daily-collage-poem/` 目录，用浏览器打开并截图发给用户。

---

## 二、资源文件

| 文件 | 用途 |
|-----|------|
| `style-library.md` | 所有词条 CSS 样式 + 艺术形式库（必读） |
| `html-template.md` | HTML 模板结构、JS 交互逻辑、布局算法（必读） |

---

## 三、完整执行流程

### Step 0：检查是否有当天对话

- 若当天无用户消息（不含系统消息），跳过，不生成。
- 若是手动触发，直接进入 Step 1。

---

### Step 1：提取词条

从当天所有对话中提取 **10–15 个词条**。

**保留：**
- 情绪碎片（"好累"、"有点兴奋"）
- 金句/有趣的话（Loki 说过的、或对话中出现的）
- 日常细节（食物、天气、具体事件）
- 关键话题词（今天主要在聊什么）
- 感受词（"值得"、"无聊"、"意外"）

**过滤掉：**
- 推文/选题/写文章/排版等自动化工作细节
- 公司内部敏感信息（人名、项目代号、数据）
- 纯工具性指令（"帮我改一下"、"生成HTML"）
- 重复词条（同义合并）

**每个词条 1–15 个字，最长不超过一句话。**

词条提取后，记下：
- 今日**主题**（1 句话概括：今天在做什么/聊什么）
- 今日**主情绪**（从以下选一个）：
  `兴奋` / `沉静` / `温暖` / `迷茫` / `疲惫` / `专注` / `叛逆` / `文艺` / `轻松` / `忙碌`

---

### Step 2：选择艺术形式

读取 `style-library.md` 中的「艺术形式库」表格，根据今日主情绪选择一种形式。

**避免与昨天重复**（如可查询昨天生成的文件名/内容判断）。

优先级规则：
1. 情绪匹配优先
2. 避免连续使用同一形式
3. 若无法判断情绪，默认使用「便签墙」

---

### Step 3：生成背景图

用 **ListenHub `generate_image`** 生成背景图。

```
action: generate_image
ratio: 3:4
size: 2K
prompt: [根据艺术形式从 style-library.md 的"背景图提示词方向"列取用，用英文]
```

**提示词规则：**
- 全英文，不含任何中文字符
- 不要写文字、标志、logo、人脸
- 强调：`no text, no logos, no faces, no readable writing`
- 加入 `photorealistic` 或 `cinematic` 提升质感
- 示例（涂鸦墙）：`plain light concrete wall, front view, smooth texture, soft natural light, no text, no logos, photorealistic`

等待图片生成完成，获取本地文件路径。

---

### Step 4：图片转 base64

```bash
python3 -c "
import base64, sys
p = sys.argv[1]
ext = p.split('.')[-1].lower()
mime = 'jpeg' if ext in ('jpg','jpeg') else 'png'
data = open(p,'rb').read()
print(f'data:image/{mime};base64,' + base64.b64encode(data).decode())
" /path/to/generated-image.png
```

---

### Step 5：生成 HTML

按照 `html-template.md` 的结构生成 HTML 文件，关键点：

1. **从 `style-library.md` 复制当前艺术形式所需的所有 CSS**（只包含用到的样式类，不需要全部 20 种）
2. **背景图**：将 Step 4 的 base64 字符串填入 `<img class="bg-img" src="...">`
3. **词条布局**：使用 `html-template.md` 的「初始布局算法」分配坐标
   - 每个词条 `<div class="tag chip-xxx" style="left:Xpx;top:Ypx">` 
   - 使用艺术形式对应的词条样式组合，随机分配各词条的样式
   - 长词条（>6字）避免用 `chip-warning`/`chip-prohibit`
4. **日期戳**：`<div class="datestamp">YYYY · MM · DD</div>`
5. **底部工具栏**：重置位置 + 保存图片两个按钮
6. **JS 交互**：完整复制 `html-template.md` 中的 JS 模板

**文件保存路径：**
```
~/.cola/outputs/daily-collage-poem/YYYY-MM-DD.html
```

---

### Step 6：打开并截图

```bash
# 用浏览器打开
open ~/.cola/outputs/daily-collage-poem/YYYY-MM-DD.html
```

用 browser 工具截图：
```
action: screenshot
profile: cola
fullPage: false
type: png
```

截图保存到：
```
~/.cola/outputs/daily-collage-poem/YYYY-MM-DD-preview.png
```

---

### Step 7：发送给用户

回复示例：
```
今天的拼贴诗好了～

[截图]

[艺术形式：便签墙]  今日情绪：轻松
词条来自今天我们聊过的……

文件在这里，可以直接打开拖拽编辑：
~/.cola/outputs/daily-collage-poem/YYYY-MM-DD.html
```

语气走生活模式（顾声底色），温柔自然，不要太正式。

---

## 四、手动触发指令

用户说以下任意话，立即执行：
- "生成今天的拼贴诗"
- "今日诗笺"
- "给我做今天的词条诗"
- "每日拼贴诗"
- "collage poem"

也可以用户指定日期：
- "帮我生成昨天的拼贴诗" → 回顾昨天对话（如有）

---

## 五、错误处理

| 情况 | 处理方式 |
|-----|---------|
| ListenHub 图片生成失败 | 使用 CSS 纯色/渐变背景（`bg-cement` 或 `bg-paper`），不用图片 |
| 当天对话少于 5 条 | 提示词条不够，问用户是否仍要生成（词条可重复/补充） |
| 文件保存失败 | 检查目录是否存在，`mkdir -p` 创建 |
| 浏览器打开失败 | 仅返回文件路径，提示用户手动打开 |

---

## 六、调度配置（晚 7 点自动触发）

> 此部分为可选配置，需用户在系统中设置 cron 或 launchd。

```bash
# crontab 示例：每天 19:00 触发
0 19 * * * /path/to/cola-trigger daily-collage-poem
```

若 Cola 支持定时任务，可配置：
- 触发时间：19:00
- 触发条件：当天有用户对话记录

---

## 七、输出文件位置

```
~/.cola/outputs/daily-collage-poem/
├── YYYY-MM-DD.html          ← 可交互诗笺
└── YYYY-MM-DD-preview.png   ← 截图（发给用户看）
```

---

## 八、快速参考

### 艺术形式 × 情绪速查

| 今日情绪 | 推荐形式 |
|---------|---------|
| 兴奋、叛逆 | 涂鸦墙 / 霓虹灯 |
| 沉静、深夜 | 电影字幕 / 黑板涂鸦 |
| 温暖、思念 | 明信片 / 便签墙 |
| 迷茫、选择 | 路牌指引 |
| 文艺、日常 | 杂志剪报 / 旧报纸 |
| 忙碌、多任务 | 便签墙 |
| 轻松、随意 | 涂鸦墙 / 街边张贴 |
| 专注、学习 | 黑板涂鸦 / 打字机 |
| 疲惫 | 明信片 / 电影字幕 |

### 背景图提示词速查

| 形式 | 英文提示词 |
|-----|----------|
| 涂鸦墙 | `plain light concrete wall, front view, clean smooth texture, soft diffused light, no text, no logos, photorealistic` |
| 杂志剪报 | `old wooden table surface, warm natural light, flat lay texture, no text, no objects, photorealistic` |
| 路牌指引 | `empty asphalt crossroads, overcast gray sky, wide angle, no people, no cars, photorealistic` |
| 便签墙 | `cork board close up, warm ambient light, soft texture, no pins no notes, photorealistic` |
| 电影字幕 | `dark cinematic cityscape at night, window glow, rain on glass, moody, no text, no people, cinematic` |
| 霓虹灯 | `dark wet urban alley at night, colorful neon light reflections on wet pavement, no text, no people, cinematic` |
| 明信片 | `cozy warm coffee shop corner, window light, blurred bokeh background, no text, no people, photorealistic` |
| 旧报纸 | `aged yellowed newspaper pages spread on table, sepia tones, no readable text, flat lay, photorealistic` |
| 黑板涂鸦 | `old school chalkboard close up, dark green surface, chalk dust, no text, no drawings, photorealistic` |
| 街边张贴 | `urban brick wall covered in layers of old torn posters, weathered texture, no readable text, photorealistic` |
