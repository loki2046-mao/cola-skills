# Manim 代码风格指南

从实际成品视频中提炼的编码规范。两个参考项目：78 秒短视频（7 段）和 184 秒长视频（8 段）。

## 目录

1. [项目结构](#项目结构)
2. [全局配色](#全局配色)
3. [时间系统](#时间系统)
4. [分段方法](#分段方法)
5. [常用动画模式](#常用动画模式)
6. [文字处理](#文字处理)
7. [布局组件库](#布局组件库)
8. [时间填充技巧](#时间填充技巧)
9. [段落过渡](#段落过渡)
10. [注意事项](#注意事项)

---

## 项目结构

```python
"""
项目标题 — 版本说明
总音频时长: XXX.XXs
"""
from manim import *
import numpy as np  # 仅在需要三角函数/数组时导入

# 全局配色
# 段落时间常量（来自 ASR）
# 全局字体

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        self.seg1_xxx()
        self.seg2_xxx()
        ...

    def seg1_xxx(self):
        ...
```

## 全局配色

暗色背景 + 高对比文字 + 功能色：

```python
BG_COLOR = "#0f0f1a"        # 深蓝黑背景
PRIMARY = "#7c3aed"          # 紫色（品牌/主色）
SECONDARY = "#00b4d8"        # 蓝色（副色）
ACCENT_YELLOW = "#fbbf24"    # 强调/高亮
ACCENT_RED = "#ef4444"       # 警告/否定
ACCENT_GREEN = "#22c55e"     # 确认/正面
ACCENT_ORANGE = "#f97316"    # 次级警告
TEXT_WHITE = "#f0f0f0"       # 正文
TEXT_GRAY = "#a0a0a0"        # 辅助文字
MUTED_GRAY = "#666666"       # 弱化元素
DARK_PANEL = "#1a1a2e"       # 面板/终端背景
```

配色原则：
- 背景始终暗色，不用纯黑 `#000000`
- 面板/卡片用半透明填充 `fill_opacity=0.1~0.3` + 描边
- 重要信息用 `ACCENT_YELLOW` 或 `weight=BOLD`
- 否定/问题用 `ACCENT_RED`
- 正面/确认用 `ACCENT_GREEN`

## 时间系统

这是整个 skill 最关键的部分。

```python
# 段落时间常量——全部来自 ASR 时间戳
S1_START = 0.00;    S1_END = 18.54;   S1_DUR = 18.54
S2_START = 18.54;   S2_END = 28.98;   S2_DUR = 10.44
...

TOTAL_DUR = 184.14
```

### 时间对齐规则

1. 每个段落方法的总动画时间 = 对应段落音频时长
2. 每个 `self.play()` 的 `run_time` + `self.wait()` 的总和 = 段落时长（减去清场动画）
3. 段内关键元素出现时间 = ASR 给出的对应词汇时间点（相对于段落起始）
4. 在注释中标注 ASR 锚点：

```python
# 语音关键锚点:
#   0.00 "你有没有发现一件事"
#   1.02 "现在买东西之前"
#   2.34 "你的第一反应不是打开搜索引擎去搜"
```

### 时间填充

用 `self.wait()` 填充到下一个锚点，段落末尾计算剩余：

```python
remaining = S1_DUR - elapsed - 0.3  # 0.3 留给清场
self.wait(max(remaining, 0.1))
```

## 分段方法

每个语音段落对应一个 `seg*_xxx(self)` 方法：

```python
def seg3_explosion(self):
    """SEG 3: EXPLOSION  (24.42 - 40.56, dur=16.14s)"""
    # 1. 构建所有 mobject
    # 2. 按时间锚点逐个 play/wait
    # 3. 清场
    self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)
```

长视频可以抽 helper：

```python
def clear_all(self, duration=0.3):
    if self.mobjects:
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=duration)
```

## 常用动画模式

### 入场

```python
FadeIn(obj, shift=UP * 0.2)          # 最常用，轻微位移
FadeIn(obj, scale=0.8)               # 从小变大
FadeIn(obj, shift=LEFT * 0.3)        # 侧向滑入
Write(text_obj)                      # 文字书写效果
GrowArrow(arrow)                     # 箭头生长
Create(shape)                        # 几何图形绘制
```

### 强调

```python
Flash(point, color=ACCENT_RED, line_length=0.4, num_lines=12)  # 爆炸闪光
obj.animate.scale(1.1), rate_func=there_and_back               # 脉冲
obj.animate.set_stroke(width=3), rate_func=there_and_back       # 描边闪烁
```

### 批量入场

```python
LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in items],
            lag_ratio=0.3, run_time=1.5)
```

### 出场

```python
FadeOut(obj)                                           # 单个
self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)  # 全部清场
```

### 动画时长经验值

| 动画类型 | 建议 run_time |
|---------|--------------|
| FadeIn（标题/标签） | 0.4 - 0.8s |
| Write（大标题） | 1.0 - 1.5s |
| LaggedStart（3-6 个元素） | 1.0 - 2.0s |
| 清场 FadeOut | 0.3s |
| Flash 强调 | 0.5s |
| GrowArrow | 0.4 - 0.8s |

## 文字处理

### 字体

```python
FONT = "Heiti SC"  # macOS 中文字体，粗体支持好
```

### 字号层级

| 层级 | 字号范围 | 用途 |
|------|---------|------|
| 超大标题 | 56-72 | 核心概念、段落主题 |
| 标题 | 36-48 | 段落标题 |
| 正文 | 24-32 | 主要信息 |
| 辅助 | 18-22 | 标签、注释 |
| 代码/小字 | 12-16 | 终端模拟、小标签 |

### 粗体强调

```python
Text("关键词", font=FONT, font_size=36, color=ACCENT_YELLOW, weight=BOLD)
```

### 代码文本

```python
Text("$ curl api.example.com", font="Courier New", font_size=18, color="#88cc88")
```

## 布局组件库

### 卡片

```python
card_bg = RoundedRectangle(
    corner_radius=0.15, width=4.5, height=2.2,
    fill_color=COLOR, fill_opacity=0.1,
    stroke_color=COLOR, stroke_width=1.5
)
content = VGroup(title, desc).arrange(DOWN, buff=0.12)
content.move_to(card_bg)
card = VGroup(card_bg, content)
```

### 标签

```python
tag = VGroup(
    RoundedRectangle(corner_radius=0.12, width=2.0, height=0.45,
                     fill_color=COLOR, fill_opacity=0.2,
                     stroke_color=COLOR, stroke_width=1),
    Text("标签文字", font=FONT, font_size=18, color=COLOR)
)
tag[1].move_to(tag[0])
```

### 终端模拟

```python
terminal = RoundedRectangle(
    corner_radius=0.15, width=10, height=4,
    fill_color="#1a1a2e", fill_opacity=0.9,
    stroke_color="#333355", stroke_width=1.5
)
dots = VGroup(*[Dot(radius=0.08, color=c) for c in ["#ff5f56", "#ffbd2e", "#27c93f"]])
dots.arrange(RIGHT, buff=0.12)
dots.next_to(terminal, UP, buff=0).align_to(terminal, LEFT).shift(RIGHT * 0.3 + DOWN * 0.25)
```

### 社交媒体推文

```python
tweet_box = RoundedRectangle(
    corner_radius=0.2, width=8, height=2.5,
    fill_color="#15202b", fill_opacity=0.95,
    stroke_color="#38444d", stroke_width=1
)
```

### 聊天气泡

```python
def _chat_bubble(self, text, align_right, color):
    bg = RoundedRectangle(corner_radius=0.15, width=5.5, height=0.6,
                          fill_color=color, fill_opacity=0.15,
                          stroke_color=color, stroke_width=1)
    t = Text(text, font=FONT, font_size=18, color=TEXT_WHITE)
    t.move_to(bg)
    group = VGroup(bg, t)
    group.shift(RIGHT * 0.3 if align_right else LEFT * 0.3)
    return group
```

### 对比布局（左 vs 右）

```python
left_box = RoundedRectangle(...)  # 左侧颜色
right_box = RoundedRectangle(...)  # 右侧颜色
divider = DashedLine(UP * 3, DOWN * 3, color=MUTED_GRAY, dash_length=0.15)
# 或用等号/大于号
equals = Text("=", font=FONT, font_size=40, color=ACCENT_YELLOW, weight=BOLD)
```

### 同心圆收缩图

```python
outer = Circle(radius=3.0, color=MUTED_GRAY, stroke_width=1.5,
               fill_color=MUTED_GRAY, fill_opacity=0.05)
inner = Circle(radius=1.0, color=ACCENT_YELLOW, stroke_width=2.5,
               fill_color=ACCENT_YELLOW, fill_opacity=0.15)
```

### 饼图/扇形

```python
pie_bg = Circle(radius=1.2, fill_color=KIMI_BLUE, fill_opacity=0.3,
                stroke_color=KIMI_BLUE, stroke_width=2)
pie_sector = Sector(radius=1.2, angle=3*PI/2, start_angle=PI/2,
                    fill_color=COLOR, fill_opacity=0.6,
                    stroke_color=COLOR, stroke_width=2)
```

## 时间填充技巧

```python
# 方法1: 精确计算剩余时间
remaining = S3_DUR - (0.6+0.6+1.0+0.8+0.8+0.5+0.5+1.0+1.5+0.6+1.5+0.8)
self.wait(max(remaining - 0.3, 0.1))

# 方法2: 基于锚点等待
self.wait(2.1)  # until ~8.3s (37.32) "只能等有人走过来告诉你"
```

## 段落过渡

所有段落结尾统一清场，保证干净过渡：

```python
# 全部淡出
self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)

# 或用 helper
self.clear_all(0.3)
```

不同段之间不做花哨转场——直接清场后开始新内容。

## 注意事项

1. **不要用 SVG/图片** — 所有视觉元素用 Manim 基础图形组合，确保可渲染
2. **Emoji 兼容性** — macOS 上 Emoji 可直接用于 Text()，但在 Linux CI 上可能不渲染。如果要跨平台，用图形替代
3. **字体安装** — `Heiti SC` 是 macOS 内置字体。Linux 需要安装或换字体
4. **渲染配置** — 720p 30fps 适合口播视频（`-ql` 低质量预览，`-qm` 中等质量出片）
5. **内存** — 元素多时及时 FadeOut，不要让 mobjects 无限累积
6. **run_time 精度** — Manim 的实际帧时间是离散的（1/fps），极短的 wait 可能被吞掉，最小用 0.1s
