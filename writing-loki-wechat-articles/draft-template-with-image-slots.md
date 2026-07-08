# Draft Template With Image Slots

Use this template when generating a Loki-style first draft that already reserves illustration positions.

The article itself should read naturally. The image slots should appear only at points where a visual summary or transition helps the reader.

## Output Skeleton

```md
# [文章标题]

[开头 1-3 段]

[图片占位 01]
- 位置作用：
- 这张图要解决什么：
- 图内中文文案：
- 统一画风要求：
- 生成提示词：

[正文段落]

[图片占位 02]
- 位置作用：
- 这张图要解决什么：
- 图内中文文案：
- 统一画风要求：
- 生成提示词：

[正文段落]

[如果还有必要，继续插入图片占位]

[结尾段落]
```

## How To Decide Image Positions

Only add an image slot when at least one of these is true:

1. a long paragraph cluster needs a visual recap
2. a key judgment deserves a summary card
3. a workflow or method can be made clearer through structured graphics
4. an education scene, product result, or model comparison benefits from direct visualization

Usually:

- short observation articles: `1-2` images
- practical tutorials / workflows: `2-4` images
- heavy case studies or education content: `3-5` images

## Image Slot Format

Every slot should follow this exact structure:

### `[图片占位 01]`

- `位置作用`:
  Explain why the image belongs here. Example: 开头判断卡 / 中段方法总结卡 / 结尾复盘卡

- `这张图要解决什么`:
  State the communication goal in one sentence.

- `图内中文文案`:
  List the Chinese words or short phrases that should appear inside the image.
  Keep them concise.

- `统一画风要求`:
  Always include these constraints unless the article explicitly needs a different look:
  - 16:9
  - 4K
  - 图文并茂
  - 中文清晰锐利可读
  - 整体可爱、舒服、有审美
  - 版式清楚，不拥挤
  - 和本文其他图片保持统一画风

- `生成提示词`:
  Write one polished Chinese prompt that can later be sent to `Labnana API` with `Nano Banana Pro`.
  The prompt itself must be entirely in Chinese and must explicitly include `16:9` and `4K`.

## Prompt Pattern

Use this structure for each prompt:

```text
16:9 横版信息插图，4K，使用 Labnana 的 Nano Banana Pro 模型生成，统一温暖可爱画风，图文并茂，中文文字清晰锐利可读，排版舒服，留白合理，整体审美统一。
主题：[这张图的主题]
核心画面：[角色 / 场景 / 物件 / 情绪]
图内文案：[需要展示的中文短句]
版式要求：[标题区 / 内容区 / 对比区 / 流程区 / 卡片区]
风格要求：[可爱、清楚、现代、统一，不要杂乱，不要模糊，不要字糊]
补充要求：[和全文其他插图保持同一套配色、同一套角色设定、同一套字风]
```

## Example

### `[图片占位 01]`

- `位置作用`: 开头判断卡
- `这张图要解决什么`: 用一张图快速交代这次测试的核心结论
- `图内中文文案`: 这次更新到底值不值得看 / 先看结论 / 适合谁 / 不适合谁
- `统一画风要求`: 16:9，图文并茂，中文清晰锐利可读，温暖可爱，版式清楚，和全文统一
- `生成提示词`:
  `16:9 横版信息插图，4K，使用 Labnana 的 Nano Banana Pro 模型生成，统一温暖可爱画风，图文并茂，中文文字清晰锐利可读，排版舒服，留白合理。主题是 AI 工具更新后的结论判断卡。核心画面为一张轻科技感但不冰冷的信息卡片，中间有可爱的角色或拟人化小元素，左右分区展示适合谁和不适合谁。图内中文文案为 这次更新到底值不值得看、先看结论、适合谁、不适合谁。版式要求为上方标题区，中间判断卡区，下方补充说明区。风格统一、可爱、现代、清楚，不要杂乱，不要字糊，和本文其他插图保持同一套配色和字风。`

## Language Constraints Inside The Draft

While filling this template:

- avoid double quotes whenever possible
- do not use `不是……而是……` 类句式
- do not use teaching or lecturing tone
- keep the spoken rhythm natural, like a sharp but friendly friend explaining something
