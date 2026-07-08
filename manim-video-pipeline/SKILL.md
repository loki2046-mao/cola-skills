---
name: manim-video-pipeline
description: >
  Manim 动画视频制作全流程管线——从选题到成片。覆盖口播脚本撰写、TTS 配音、
  ASR 时间戳切分、Manim 动画编码、BGM 生成、ffmpeg 合成。
  Use when 用户说「做视频」「做个 Manim 视频」「科普视频」「动画视频」「配音视频」
  「口播视频」「帮我做一个解说视频」「写 Manim 代码」「视频制作」「manim animation」
  「配音+动画」「视频管线」、或涉及 Manim 场景编写与音画同步的任何需求。
author: kude
---

# Manim 视频制作管线

一条完整的「选题 → 脚本 → 配音 → 时间戳 → 动画 → 合成」视频制作管线。

## 核心约束（不可违反）

1. **音画同步是硬约束** — 每个画面元素的出现时间 = 语音说到对应内容的时间点。画面跟着声音走，不抢不超前。
2. **先切音频再写动画** — 绝不能先做动画再对音频。必须先有 ASR 精确时间戳，再写 Manim 代码。
3. **BGM 不盖人声** — 背景音乐音量压到 -18dB 到 -20dB。

## 六步流程

### Step 1: 写口播脚本

根据选题/文章/素材写 2-4 分钟的口播脚本。

要求：
- 口语化，像在跟朋友聊天，不是念稿
- 每段有一个核心观点，别堆砌信息
- 每段 10-30 秒，标注段落分隔
- 开头 5 秒必须抓住注意力（提问/反常识/冲突）
- 结尾要有记忆点（金句/反转/呼应开头）

输出格式：
```
## Seg1: 标题 (预估时长)
口播文字...

## Seg2: 标题 (预估时长)
口播文字...
```

### Step 2: TTS 配音

用 TTS 生成配音音频。

首次执行时询问用户：
- TTS 方案（推荐 ListenHub，也可以用其他服务）
- API key 和 speaker_id（仅用于本次调用）

详细配置见 → [references/tts-setup.md](./references/tts-setup.md)

如果用户选择 ListenHub 且 Cola 环境支持 listenhub skill，可以直接调用：
```
listenhub create_tts content="脚本全文" tts_type=text
```

输出：一个完整的音频文件（MP3/WAV）。

### Step 3: ASR 切时间戳

用 coli 转写配音音频，获取字级时间戳。

```bash
coli asr <audio_file>
```

coli asr 会输出每个字/词的起止时间。从中提取：
- 每段的起止时间（精确到 0.01s）
- 段内关键词/句的精确时间锚点

输出格式示例：
```python
# 段落时间常量（ASR 时间戳）
S1_START = 0.00;   S1_END = 18.54;  S1_DUR = 18.54
S2_START = 18.54;  S2_END = 28.98;  S2_DUR = 10.44
...

# Seg1 关键锚点:
#   0.00 "你有没有发现一件事"
#   2.34 "你的第一反应不是打开搜索引擎去搜"
#   5.04 "而是在群里问一嘴"
```

### Step 4: Manim 动画

按时间戳逐段写 Manim 场景代码。这是最耗时的步骤。

编码前先读 → [references/manim-style-guide.md](./references/manim-style-guide.md)

#### 4.1 整体结构

```python
from manim import *

BG_COLOR = "#0f0f1a"
# ... 配色常量
# ... 时间常量（从 Step 3 复制）
FONT = "Heiti SC"

class MyVideoScene(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        self.seg1_xxx()
        self.seg2_xxx()
        ...

    def seg1_xxx(self):
        # 构建 mobjects
        # 按 ASR 锚点编排动画
        # 清场
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.3)
```

#### 4.2 音画同步编排

每个段落方法内部的时间编排：

```python
def seg3_topic_name(self):
    """SEG 3 (28.98 - 52.62, dur=23.64s)"""
    # 锚点（从ASR时间戳提取）:
    #   0.0s "第一个关键句"
    #   2.8s "第二个关键词"
    #   6.2s "第三个关键句"

    title = Text("段落主题", ...)

    # 0.0s: 标题入场，锚定语音说到"第一个关键句"的时间
    self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.4)
    # 等待到下一个锚点
    self.wait(2.1)  # → 2.8s "第二个关键词"
    self.play(FadeIn(keyword, shift=UP * 0.1), run_time=0.4)
    ...
    # 段落末尾补齐时间
    remaining = S3_DUR - elapsed - 0.3
    self.wait(max(remaining, 0.1))
    self.clear_all(0.3)
```

#### 4.3 设计原则

- 每段一个视觉主题，不要塞太多信息
- 画面服务于语音，不要为了炫技加无关动画
- 用 RoundedRectangle + Text 组合构建卡片，不用外部图片
- 对比用左右分栏 + 虚线分隔
- 强调用 Flash / there_and_back 脉冲 / 颜色变化
- 段间过渡：直接 FadeOut 全部，不做花哨转场

#### 4.4 渲染预览

```bash
# 低质量快速预览
manim -ql scene.py MyVideoScene

# 中等质量出片
manim -qm scene.py MyVideoScene
```

### Step 5: BGM

添加背景音乐。两种方式：

1. **AI 生成** — 用音乐生成工具按风格生成（科技感/轻快/叙事）
2. **素材库** — 从免费素材库下载

关键要求：
- 时长 ≥ 视频时长（循环或选更长的曲子）
- 风格匹配内容调性
- 不要有歌词

### Step 6: ffmpeg 合成

把视频 + 配音 + BGM 合成最终成片：

```bash
ffmpeg -i video.mp4 -i voiceover.mp3 -i bgm.mp3 \
  -filter_complex "
    [1:a]volume=1.0[voice];
    [2:a]volume=0.08[music];
    [voice][music]amix=inputs=2:duration=first[aout]
  " \
  -map 0:v -map "[aout]" \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  output.mp4
```

参数说明：
- `volume=0.08` ≈ -22dB，确保 BGM 不盖人声（根据实际素材微调到 -18dB ~ -20dB）
- `-shortest` 以最短轨道为准截断
- `-c:v copy` 不重新编码视频，速度快

如果配音和 BGM 需要对齐到精确位置：
```bash
# BGM 延迟 0.5s 开始
-filter_complex "[2:a]adelay=500|500,volume=0.08[music];..."
```

## 工作流快捷路径

### 只改脚本重做

脚本改了 → 从 Step 2 重新开始（TTS → ASR → 改动画 → 合成）。

### 只调动画

不改脚本 → 直接改 Manim 代码 → 重新渲染 → 合成。时间戳不变。

### 快速迭代

先用 `-ql`（480p15fps）快速预览动画节奏，确认没问题再用 `-qm` 出片。

## 常见问题

**Q: 时间对不上怎么办？**
回去看 ASR 时间戳，检查哪个 `self.wait()` 算错了。通常是某个 `run_time` 忘了加进累计时间。

**Q: 中文字体渲染有问题？**
macOS 用 `Heiti SC`，Linux 需要安装中文字体（如 Noto Sans CJK）并修改 FONT 变量。

**Q: 视频太长 Manim 渲染很慢？**
3 分钟视频 `-qm` 大约需要 5-15 分钟渲染。可以先只渲染单个段落调试：在 construct 里注释掉其他 seg 方法。

**Q: 配音节奏不对？**
回到 Step 1 调脚本。TTS 的节奏很大程度取决于文本本身——短句快、长句慢、标点影响停顿。

## 通用 Agent 接入

本管线的核心逻辑不依赖 Cola 的 `session_spawn`、`work_create`、`listenhub` skill 等特有 API。**任何能执行 shell 命令 + 生成文本的 Agent 都可以用。**

### 环境依赖

| 工具 | 安装 | 说明 |
|------|------|------|
| Python 3.10+ | — | Manim 运行时 |
| Manim Community ≥ 0.18 | `pip install manim` | 动画引擎 |
| ffmpeg | `brew install ffmpeg` / `apt install ffmpeg` | 音视频合成 |
| ASR 工具 | `pip install coli-cli` 或 `pip install openai-whisper` | 获取字级时间戳。coli 是本管线默认方案，也可用 whisper / faster-whisper / 任何能输出 word-level timestamps 的工具替代 |
| TTS API | 见 [references/tts-setup.md](./references/tts-setup.md) | 推荐 ListenHub；也可用 Edge-TTS、OpenAI TTS、Fish Audio 等任何 TTS 服务 |

### 每步通用命令行操作

```bash
# Step 1: 写脚本 — 纯文本，Agent 直接生成即可，输出到 script.md

# Step 2: TTS — 调用任意 TTS API，示例用 ListenHub
curl -X POST "https://api.listenhub.cn/v1/tts" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text":"脚本全文","speaker_id":"xxx"}' \
  -o voiceover.mp3

# Step 3: ASR — 获取字级时间戳
coli asr --json voiceover.mp3 > timestamps.json
# 替代方案：whisper voiceover.mp3 --word_timestamps True --output_format json

# Step 4: Manim — 渲染动画
manim render -qm -r 1280,720 scene.py MyVideoScene
# 快速预览用 -ql，正式出片用 -qm 或 -qh

# Step 5 & 6: 合成（配音 + BGM + 视频）
ffmpeg -i media/videos/scene/720p30/MyVideoScene.mp4 \
  -i voiceover.mp3 -i bgm.mp3 \
  -filter_complex \
    "[1:a]volume=1.0[voice];[2:a]volume=0.08[music];[voice][music]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest \
  output.mp4
```

### 对接要点

- **脚本和 Manim 代码**都是纯文本生成，任何 LLM Agent 都能做
- **TTS / ASR** 是外部 API/CLI 调用，只要 Agent 能跑 shell 就行
- **时间戳格式**：只需要每个字/词的 `start`、`end`（秒），不限具体 ASR 工具的输出格式——Agent 自行解析即可
- **Manim style guide** 和 **tts-setup** 两个参考文档在 `references/` 目录下，建议一并提供给 Agent 作为上下文
