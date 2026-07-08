# TTS 配置指南

配音是管线的第二步。先拿到音频，才能切时间戳，才能写动画。

## 推荐方案：ListenHub

[ListenHub](https://www.listenhub.ai) 提供中文 TTS，音质好、支持多音色。

### API 调用方式

```
POST https://api.marswave.ai/openapi/v1/tts
Header: Authorization: Bearer {YOUR_API_KEY}
Content-Type: application/json

Body:
{
  "input": "要转换的文本",
  "voice": "{SPEAKER_ID}"
}
```

响应返回音频文件（通常是 MP3）。

### 获取 Speaker ID

在 ListenHub 平台试听音色后获取对应的 speaker_id。

也可以通过 Cola 内置的 listenhub skill 操作：
- `listenhub get_speakers` — 列出可用音色
- `listenhub create_tts` — 直接生成 TTS 音频

### 首次使用

运行管线前需要确认：
1. 用户有 ListenHub API key
2. 用户选好了 speaker_id（建议先试听几个再定）
3. 把 API key 和 speaker_id 告诉 AI（仅用于当次调用，不存储）

## 备选方案

任何 TTS 服务都行，只要能输出完整的音频文件（MP3/WAV）：
- Edge TTS（免费、微软声音）
- OpenAI TTS（质量高、英文好）
- 各云厂商 TTS（阿里云、腾讯云等）

关键要求：
- 输出完整音频文件，不是流式片段
- 音质足够好（至少 16kHz 采样率）
- 中文场景选中文优化的音色

## 脚本分段建议

TTS 前先把口播脚本分好段。每段 10-30 秒为佳：
- 太短（<5s）→ 画面来不及展开
- 太长（>40s）→ 单段动画太复杂，调试痛苦

可以一次性送整篇脚本给 TTS，也可以分段生成后拼接。一次性生成的好处是语气连贯、不会有拼接痕迹。
