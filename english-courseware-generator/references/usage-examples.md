# 使用示例

4个完整使用场景，展示不同主题、不同组件组合的实际用法。

---

## 示例1：疯狂动物城 — 动物词汇课

**用户输入**：
> 帮我做一个疯狂动物城主题的英语课件，教动物词汇，适合6-10岁，初级难度。

**Skill 执行过程**：

### Step 1: 参数确认
| 参数 | 值 |
|------|-----|
| 主题类型 | IP |
| IP名称 | Zootopia（疯狂动物城） |
| 角色 | Judy, Nick, Flash, Clawhauser |
| 学习内容 | Animals（动物词汇） |
| 目标年龄 | 6-10 |
| 难度 | Beginner |
| 画幅比例 | 3:4 |
| 风格 | cute_cartoon |
| 组件 | Header + Vocab Cards + Fill Blanks + Footer |

### Step 2: 生成教学内容

**词汇**：
| 英文 | 中文 | 角色关联 |
|------|------|----------|
| Rabbit | 兔子 | Judy |
| Fox | 狐狸 | Nick |
| Sloth | 树懒 | Flash |
| Cheetah | 猎豹 | Clawhauser |

**填空题**：
Word bank: Rabbit, Fox, Sloth, Cheetah, fast, cute
1. The ___ is very fast.
2. Judy is a ___.
3. The ___ is slow and sleepy.
4. Nick is a ___.
5. A ___ can run very fast.
6. The animals are very ___.

### Step 3: 构建提示词

（见 prompt-templates.md → 案例1）

### Step 4: 出图

调用生图工具，3:4 比例，4K 分辨率。

---

## 示例2：水果王国 — 词汇+游戏课（原创主题）

**用户输入**：
> 做一个水果主题的英语课件，不用现成IP，我自己创一个"水果王国"，角色就用水果拟人，要有词汇和游戏。

**Skill 执行过程**：

### Step 1: 参数确认
| 参数 | 值 |
|------|-----|
| 主题类型 | Original |
| 原创主题 | Fruit Kingdom（水果王国） |
| 角色 | Apple Prince, Banana Princess, Orange Wizard, Grape Fairy |
| 学习内容 | Fruits（水果词汇） |
| 目标年龄 | 6-8 |
| 难度 | Beginner |
| 画幅比例 | 3:4 |
| 风格 | cute_cartoon |
| 组件 | Header + Vocab Cards (6个) + Word Search + Footer |

### Step 2: 生成教学内容

**词汇**：Apple(苹果), Banana(香蕉), Orange(橙子), Grape(葡萄), Strawberry(草莓), Watermelon(西瓜)

**Word Search 字母网格**（10×10，单词横竖嵌入）：
```
A P P L E O R A N G
B X G R A P E K S
A B A N A N A L B
N S T R A W B E R
A G R A P E Z K R
P W A T E R M E L
L O R A N G E M O
E G R A P E B A N
O R A N G E A P P
B A N A N A G R P
```

### Step 3: 构建提示词

（见 prompt-templates.md → 案例2）

### Step 4: 出图

调用生图工具，3:4 比例，4K 分辨率。

---

## 示例3：小猪佩奇 — 语法课（现在进行时）

**用户输入**：
> 用小猪佩奇做一节语法课，教现在进行时，要有语法讲解、对话例子和练习。

**Skill 执行过程**：

### Step 1: 参数确认
| 参数 | 值 |
|------|-----|
| 主题类型 | IP |
| IP名称 | Peppa Pig（小猪佩奇） |
| 角色 | Peppa, George, Mummy Pig, Daddy Pig |
| 学习内容 | Present Continuous Tense（现在进行时） |
| 目标年龄 | 6-10 |
| 难度 | Beginner-Intermediate |
| 画幅比例 | 3:4 |
| 风格 | cute_cartoon |
| 组件 | Header + Grammar Points + Comic Dialogue + Fill Blanks + Footer |

### Step 2: 生成教学内容

**语法讲解**：
- 结构：am/is/are + verb-ing
- 用法：表示正在发生的动作
- 例句：Peppa is jumping. / George is laughing. / Mummy Pig is cooking.

**漫画对话**：
- Panel 1: Peppa jumping → "I am jumping!"
- Panel 2: George laughing → "I am laughing!"
- Panel 3: Mummy Pig cooking → "I am cooking!"

**填空题**：
Word bank: is, are, jumping, running, playing, eating
1. Peppa ___ jumping.
2. George and Peppa ___ playing.
3. Daddy Pig ___ eating.
4. They ___ running.
5. Suzy Sheep is ___.
6. We are ___.

### Step 3: 构建提示词

（见 prompt-templates.md → 案例3）

### Step 4: 出图

---

## 示例4：原创海洋世界 — 综合复习课

**用户输入**：
> 做一个海洋世界的英语复习课件，原创主题，包含词汇、选择题、连线和自我检测，适合8-12岁中级难度。

**Skill 执行过程**：

### Step 1: 参数确认
| 参数 | 值 |
|------|-----|
| 主题类型 | Original |
| 原创主题 | Ocean World（海洋世界） |
| 角色 | Wave the Dolphin, Coral the Starfish, Bubble the Turtle |
| 学习内容 | Sea Animals & Ocean Words |
| 目标年龄 | 8-12 |
| 难度 | Intermediate |
| 画幅比例 | 3:4 |
| 风格 | flat_design |
| 组件 | Header + Vocab Cards + Multiple Choice + Matching + Self Check + Footer |

### Step 2: 生成教学内容

**词汇**：Dolphin(海豚), Starfish(海星), Turtle(海龟), Shark(鲨鱼), Octopus(章鱼), Whale(鲸鱼)

**选择题**：
1. What animal is smart and friendly?
   A. Shark  B. Dolphin  C. Octopus
2. How many arms does an octopus have?
   A. Six  B. Eight  C. Ten
3. A turtle has a ___ on its back.
   A. shell  B. wing  C. tail
4. The ___ is the largest animal in the ocean.
   A. Shark  B. Whale  C. Dolphin

**连线题**：
左：Dolphin / Starfish / Turtle / Shark
右：海龟 / 海豚 / 鲨鱼 / 海星

**自我检测**：
1. I can read 6 sea animal words. ☆☆☆☆☆
2. I can match words with Chinese. ☆☆☆☆☆
3. I can answer quiz questions. ☆☆☆☆☆
4. I know the ocean animals. ☆☆☆☆☆

### Step 3: 构建提示词

提示词构建要点：
- 5个组件放在3:4竖版画面中较拥挤，建议ZONE 2分为：
  - ZONE 2a（上）：Vocab Cards（2×3 grid）
  - ZONE 2b（中左）：Multiple Choice
  - ZONE 2c（中右）：Matching
  - ZONE 2d（下）：Self Check

提示词：
```text
生成一张儿童英语学习课件图，主题：海洋世界海洋动物词汇。

整体风格：扁平设计风格，高对比纯色，干净几何形状，直角，现代简约插画，矢量风格，高对比度。
面向8-12岁儿童的教学练习页。
双语教学：英文为主，中文翻译辅助。
背景：深蓝渐变，带淡淡波浪图案。

排版 — 多文字区域：

ZONE 1 — 顶部标题区（占画面高度12%）：
简洁横幅，主标题 "OCEAN WORLD ENGLISH" 用粗体现代无衬线字显示。
下方用较小字体显示副标题 "海洋世界英语"。
横幅周围有波浪线和气泡图标装饰。
配色：海洋蓝、珊瑚橙、海绿点缀。

ZONE 2a — 词汇卡片区（占内容区上部30%）：
2×3 排列的扁平设计卡片。每张卡片包含：
- 简洁的扁平风海洋动物插画
- 英文单词用粗体字显示
- 下方用较小字体显示中文翻译
卡片内容：
卡片1：扁平海豚插画，"Dolphin"，"海豚"
卡片2：扁平海星插画，"Starfish"，"海星"
卡片3：扁平海龟插画，"Turtle"，"海龟"
卡片4：扁平鲨鱼插画，"Shark"，"鲨鱼"
卡片5：扁平章鱼插画，"Octopus"，"章鱼"
卡片6：扁平鲸鱼插画，"Whale"，"鲸鱼"
卡片为直角，纯色背景，干净边框。

ZONE 2b — 选择题区（占内容区中部左侧35%）：
4道题，每题3个选项：
Q1: What animal is smart and friendly?
   A. Shark   B. Dolphin   C. Octopus
Q2: How many arms does an octopus have?
   A. Six   B. Eight   C. Ten
Q3: A turtle has a ___ on its back.
   A. shell   B. wing   C. tail
Q4: The ___ is the largest animal in the ocean.
   A. Shark   B. Whale   C. Dolphin
选项用圆圈内字母标注。题间距清晰。

ZONE 2c — 连线区（占内容区中部右侧35%）：
左列："Dolphin"、"Starfish"、"Turtle"、"Shark"
右列："海龟"、"海豚"、"鲨鱼"、"海星"
用虚线连接。排版干净。

ZONE 2d — 自我检测区（占内容区下部15%）：
4个自评项目，5星评分：
1. I can read 6 sea animal words. ☆☆☆☆☆
2. I can match words with Chinese. ☆☆☆☆☆
3. I can answer quiz questions. ☆☆☆☆☆
4. I know the ocean animals. ☆☆☆☆☆
星星横排，简洁干净。

ZONE 3 — 底部页脚区（占画面高度8%）：
左侧用小号字体显示标语 "Explore the Ocean!"。
下方用更小字体显示中文标语 "探索海洋！"。
右侧显示页码 "Review 1"。
页脚上方有一条简洁实线分隔线。

色彩：海洋色系 — 深蓝、珊瑚橙、海绿、白色，干净高对比。所有文字清晰可读。
4K分辨率，字体清晰锐利，教学质量。

反向提示词：
无乱码文字，无错别字，无随机字母，无模糊文字，不可读的文字，文字区域不重叠，字体风格不统一，同一文字区域内不混用语言，无PPT模板感，无廉价练习卷感，无低分辨率文字，无水印，无logo，无不适当内容，无暴力元素，无恐怖元素，无扭曲插画，无杂乱排版，无文字溢出，无文字超出指定区域，无商业字体模仿

画幅比例：3:4
```

### Step 4: 出图

---

## 常见问题处理

### Q: 组件太多了画面很拥挤怎么办？
A: 减少组件数量。3:4竖版建议最多4个内容组件（加Header+Footer共6个区域）。或者换16:9横版分2行排列。或者拆成2张课件图。

### Q: 用户只想做一个单独的练习题怎么办？
A: 只选一个组件 + Header + Footer。例如只要填空题，就是 Header + Fill Blanks + Footer，一张干净简洁的练习图。

### Q: 用户提供了自己的词汇表怎么办？
A: 跳过内容生成步骤，直接用用户提供的词汇和翻译构建提示词。

### Q: 文字总是乱码怎么办？
A: 1) 确保4K分辨率 2) 减少单个ZONE的文字量 3) 文字描述更明确（逐字写死） 4) 尝试切换生图模型 5) 把中文和英文分在不同ZONE减少混合

### Q: 用户想要横版课件怎么办？
A: 16:9适合投影/屏幕展示，组件数减少到1-3个。横向排列优先。排版参考 layout-and-style.md 的16:9分区图。

### Q: 用户想做多页课件怎么办？
A: 每页生成一张图。第一页可以是词汇+对话（导入课），第二页是练习题（练习课），第三页是游戏+测验（复习课）。每页独立生成提示词和出图。
