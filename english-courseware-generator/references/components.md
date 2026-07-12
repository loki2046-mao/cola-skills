# 组件库详细说明

27个教学组件，分8大类。每个组件可独立使用，也可自由组合。组件独立 = 一张课件图可以只放一个组件（配 Header + Footer），也可以放3-6个组件。

## 目录

1. [词汇教学组件](#一词汇教学组件)
2. [对话教学组件](#二对话教学组件)
3. [练习题型组件](三练习题型组件)
4. [语法句型组件](#四语法句型组件)
5. [综合应用组件](#五综合应用组件)
6. [游戏互动组件](#六游戏互动组件)
7. [评估测试组件](#七评估测试组件)
8. [装饰元素组件](#八装饰元素组件)

---

## 一、词汇教学组件

### 1. 词汇卡片 Vocabulary Cards `vocab_cards`

**用途**：展示核心词汇，每张卡片含单词+插图+中文翻译。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 卡片数量 | 2-6 | 4 |
| 是否显示插图 | true/false | true |
| 单词格式 | uppercase / lowercase / capitalize | capitalize |
| 卡片排列 | 2×2 grid / 2×3 grid / 1×4 row | 2×2 grid |

**内容生成规则**：
- 根据学习主题生成对应词汇
- 每个单词配简短中文翻译
- 插图与单词含义直接相关，风格与主题统一
- 单词难度匹配目标年龄

**提示词描述要点**：
```
ZONE 2a — vocabulary card grid:
A 2×2 grid of rounded cards. Each card contains:
- A cute illustration of [word] in the theme style
- The word "[WORD]" in bold, readable font
- Chinese translation "[翻译]" below
Cards have rounded corners, pastel background, consistent spacing.
```

---

### 2. 词汇表 Vocabulary List `vocab_list`

**用途**：适合大量词汇展示，列表或表格形式。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 列表样式 | bullet / number / grid | grid |
| 列数 | 1-4 | 2 |
| 是否含例句 | true/false | false |
| 词汇数量 | 4-12 | 8 |

**内容生成规则**：
- 包含例句时，例句要简短、用该单词造句
- 表格式排列整齐，英文左、中文右

---

### 3. 图文配对 Picture-Word Match `picture_word_match`

**用途**：图片与单词配对练习，检验词汇理解。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 配对数量 | 3-6 | 4 |
| 布局 | horizontal / vertical / grid | grid |

**内容生成规则**：
- 左侧图片，右侧单词（或反过来），用虚线连接
- 图片风格与主题统一
- 可加入干扰项增加难度

---

## 二、对话教学组件

### 4. 漫画对话 Comic Dialogue `comic_dialogue`

**用途**：漫画格式的情景对话，角色互动。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 漫画格数 | 2-4 | 3 |
| 布局 | horizontal / vertical | horizontal |
| 气泡样式 | rounded / oval / cloud | rounded |
| 是否显示角色 | true/false | true |

**内容生成规则**：
- 对话内容围绕学习主题
- 角色使用主题中的角色
- 对话简短，每格1-2句
- 英文对话，可配中文翻译小字

**提示词描述要点**：
```
ZONE 2b — comic dialogue:
A horizontal 3-panel comic strip. Each panel shows:
- Theme characters in a simple scene
- Speech bubble with dialogue text
Panel 1: [Character A] says "[dialogue 1]"
Panel 2: [Character B] says "[dialogue 2]"
Panel 3: [Character A] says "[dialogue 3]"
Speech bubbles are rounded, text is clear and readable.
```

---

### 5. 角色扮演 Role Play `role_play`

**用途**：角色扮演对话框架，给学生练习口语。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 角色数量 | 2-3 | 2 |
| 场景主题 | greeting / shopping / restaurant / school / 自定义 | greeting |
| 是否包含提示词 | true/false | true |

**内容生成规则**：
- 提供角色设定和场景描述
- 给出对话框架，留空让学生填写
- 包含提示词（useful phrases）

---

### 6. 日常用语 Daily Expressions `daily_expressions`

**用途**：日常表达集合，分类展示。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 类别 | greetings / thanks / apology / requests / 自定义 | greetings |
| 格式 | speech_bubbles / list / cards | cards |

---

## 三、练习题型组件

### 7. 填空题 Fill in the Blanks `fill_blanks`

**用途**：填空练习，检验词汇和语法。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 题目数量 | 3-8 | 6 |
| 空格样式 | underline / box / circle | underline |
| 提示类型 | character / image / word_bank / none | word_bank |
| 难度 | easy / medium / hard | easy |

**内容生成规则**：
- 句子内容围绕主题
- 空格处填写目标词汇或语法结构
- 提供 word bank 时，打乱顺序列出
- 难度递增：easy=简单词汇填空，medium=语法填空，hard=完形填空

**提示词描述要点**：
```
ZONE 2c — fill in the blanks exercise:
6 sentences with underlined blanks. Word bank at the top in a rounded box: "[word1] [word2] [word3] [word4] [word5] [word6]"
Sentences:
1. The ___ is very fast.
2. I like ___ and ___.
3. ...
Blank lines are clearly marked with underscores.
```

---

### 8. 选择题 Multiple Choice `multiple_choice`

**用途**：多选一练习。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 题目数量 | 3-6 | 4 |
| 每题选项数 | 3-4 | 3 |
| 选项样式 | abc / 123 / circles | abc |
| 选项是否含图 | true/false | false |

---

### 9. 连线题 Matching `matching`

**用途**：左右连线配对。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 配对数量 | 3-6 | 4 |
| 左侧类型 | word / image | word |
| 右侧类型 | word / image / translation | translation |
| 连线样式 | dotted / solid / curved | dotted |

---

### 10. 判断题 True or False `true_false`

**用途**：判断对错。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 题目数量 | 3-6 | 4 |
| 陈述样式 | simple / complex | simple |
| 图标样式 | check_x / smiley / thumbs | check_x |

---

### 11. 排序题 Ordering `ordering`

**用途**：句子或故事排序。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 排序项数 | 3-5 | 4 |
| 排序类型 | sentence / story / steps | sentence |
| 编号样式 | 123 / abc / 圆圈数字 | 123 |

---

### 12. 单词拼写 Spelling `spelling`

**用途**：拼写练习。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 单词数量 | 3-6 | 4 |
| 提示类型 | scrambled / first_letter / image / none | scrambled |
| 是否显示字母框 | true/false | true |

---

## 四、语法句型组件

### 13. 句型练习 Sentence Patterns `sentence_patterns`

**用途**：句型替换练习。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 句型数量 | 2-4 | 4 |
| 是否显示替换词 | true/false | true |
| 是否颜色标注句型结构 | true/false | true |

**内容生成规则**：
- 基础句型用颜色高亮（如主语蓝色、谓语红色）
- 替换词列表放在句型旁边
- 句型要符合学习目标（如一般现在时、现在进行时）

---

### 14. 造句练习 Sentence Making `sentence_making`

**用途**：用给定词造句。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 提示数 | 2-4 | 4 |
| 提示类型 | word_bank / image / scenario | word_bank |
| 最少单词数 | 3-5 | 3 |

---

### 15. 语法点 Grammar Points `grammar_points`

**用途**：语法知识点讲解。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 语法主题 | tenses / articles / prepositions / plural / 自定义 | tenses |
| 解释风格 | simple / detailed | simple |
| 例句数量 | 2-4 | 3 |

**内容生成规则**：
- 简明讲解语法规则
- 例句要围绕主题
- 用颜色标注语法结构
- 适合目标年龄理解

---

## 五、综合应用组件

### 16. 阅读理解 Reading Comprehension `reading_comprehension`

**用途**：短文阅读+理解题。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 文章长度 | short(50-80词) / medium(80-120词) / long(120-180词) | short |
| 问题数量 | 2-4 | 3 |
| 题型组合 | mc / tf / short_answer | mc, tf |

**内容生成规则**：
- 文章围绕主题角色和场景
- 问题考察文章理解
- 文章中可包含目标词汇

---

### 17. 听力练习 Listening `listening`

**用途**：听力任务（课件图含题目和音频图标提示）。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 音频类型 | dialogue / description / instruction | dialogue |
| 任务类型 | fill_blanks / mc / ordering | fill_blanks |
| 播放次数提示 | 2-3 | 2 |

**注意**：课件图只能展示题目，音频需要教师口头提供或另外录制。图标提示"听2遍"。

---

### 18. 写作练习 Writing `writing`

**用途**：写作任务。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 写作类型 | sentence / paragraph / dialogue / letter | sentence |
| 字数要求 | 句子级 / 50词 / 100词 | 句子级 |
| 提示类型 | topic / words / questions | topic, words |

---

### 19. 口语练习 Speaking `speaking`

**用途**：口语任务。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 口语类型 | dialogue / presentation / description | dialogue |
| 准备时间提示 | 30s / 60s / 90s | 30s |
| 是否显示录音指示 | true/false | true |

---

## 六、游戏互动组件

### 20. 单词 Bingo `word_bingo`

**用途**：Bingo游戏卡片。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 网格大小 | 3×3 / 4×4 | 3×3 |
| 单词来源 | 本课词汇 | 本课词汇 |
| 是否含免费格 | true/false | true |

**内容生成规则**：
- 从本课词汇中随机选取填入网格
- 中心格标 "FREE"
- 每格含单词或小图

---

### 21. 单词搜索 Word Search `word_search`

**用途**：字母网格中找单词。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 网格大小 | 8×8 / 10×10 / 12×12 | 10×10 |
| 单词数量 | 4-8 | 6 |
| 方向 | horizontal / vertical / all | all |

**内容生成规则**：
- 生成字母网格，将目标单词嵌入
- 剩余位置填随机字母
- 旁边列出要找的单词
- 单词可横向、竖向放置（beginner只横向）

---

### 22. 迷宫游戏 Maze `maze_game`

**用途**：答题闯关迷宫。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 迷宫大小 | small / medium / large | medium |
| 任务类型 | answer_questions / collect_words | answer_questions |
| 终点奖励 | character / star / trophy | character |

**内容生成规则**：
- 迷宫路径上有2-3个答题点
- 答对前进，答错后退
- 终点有主题角色或奖励图

---

## 七、评估测试组件

### 23. 小测验 Mini Quiz `mini_quiz`

**用途**：综合小测验。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 题目数量 | 3-6 | 5 |
| 题型组合 | mc / fill / matching / tf | mc, fill |
| 时间限制 | 5min / 10min / 15min | 10min |
| 是否显示分值 | true/false | true |

---

### 24. 自我检测 Self Check `self_check`

**用途**：学生自评清单。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 检测项数 | 3-5 | 5 |
| 评分标准 | stars / smileys / numbers | stars |

**内容生成规则**：
- 检测项如："I can read 8 new words" / "I can use present continuous"
- 3-5星评分，或笑脸评分

---

## 八、装饰元素组件

### 25. 标题区 Header `header`

**用途**：课件标题区，每张课件图必选。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 英文标题 | 自定义 | 课程名 |
| 中文标题 | 自定义 | 课程中文名 |
| 副标题 | 自定义 | 空 |
| 装饰元素 | paw_prints / stars / leaves / 自定义 | 主题相关 |
| 标题样式 | banner / plain / decorative | banner |

**提示词描述要点**：
```
ZONE 1 — header:
Top banner with main title "[TITLE_EN]" in bold playful font,
Chinese subtitle "[标题中文]" below in smaller font.
Decorative [theme-specific] elements (e.g., paw prints, stars) scattered around the banner.
Color: [theme color palette].
```

---

### 26. 角色展示 Characters `character_showcase`

**用途**：展示主题角色。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 角色数量 | 1-6 | 4 |
| 姿势 | standing / action / expression | standing |
| 大小 | small / medium / large | medium |

---

### 27. 页脚 Footer `footer`

**用途**：课件页脚，每张课件图必选。

| 参数 | 可选值 | 默认值 |
|------|--------|--------|
| 英文slogan | 自定义 | "Let's Learn & Have Fun!" |
| 中文slogan | 自定义 | "让我们一起学习，开心玩耍！" |
| 是否显示页码 | true/false | true |

---

## 组件组合建议

### 一张课件图的合理组件数

| 画幅 | 组件数（含Header+Footer） | 实际内容组件 |
|------|--------------------------|-------------|
| 3:4 竖版 | 4-6 | 2-4 |
| 16:9 横版 | 3-5 | 1-3 |
| 1:1 正方 | 3-4 | 1-2 |

### 常见课程类型推荐组合

**词汇课**：Header → Vocab Cards → Picture-Word Match → Fill Blanks → Footer

**对话课**：Header → Comic Dialogue → Role Play → Daily Expressions → Footer

**语法课**：Header → Grammar Points → Sentence Patterns → Fill Blanks → Sentence Making → Footer

**复习课**：Header → Vocab Cards → Multiple Choice → Matching → Word Search → Mini Quiz → Footer

**游戏课**：Header → Word Bingo → Word Search → Maze Game → Footer

**阅读课**：Header → Reading Comprehension → Writing → Self Check → Footer
