# Content Router

先判断内容，再设计图文。不要先选模板。

## Content Types

### T00 公众号长文 / Newsletter 转小红书
- Signals: 公众号、定稿、长文、Newsletter、推文、Markdown 文章、把这篇转成小红书
- Primary workflow: read `references/wechat-to-rednote.md` before choosing style
- Primary style: 根据内容再路由；不要默认旧纸、公众号排版或文章摘录风
- Secondary styles: 观点海报风、证据截图风、案例复盘风、工作流拆解风
- Required evidence: 2-4 个能证明文章观点的对象，如截图、报告截面、前后对比、案例表、输出结果
- Avoid: 把公众号章节切成 9 张摘要、把长链接/安装命令放进主图、只有封面好看后面全是文字

### T01 求职/简历/职业判断
- Signals: 简历、实习、校招、HR、业务负责人、岗位、JD、作品集、AI 替代
- Primary style: 招聘评审桌风
- Secondary styles: 红笔批注风、工具实测截图风、数据诊断风
- Required evidence: 简历片段、改写前后、风险判断、真实输出截图
- Avoid: 温柔鸡汤、纯清单、过度工具广告

### T02 AI 工具/Skill/工作流演示
- Signals: Skill、工具、安装、工作流、自动生成、Prompt、Agent、截图
- Primary style: 工具实测截图风
- Secondary styles: 产品发布风、工作流拆解风、案例复盘风
- Required evidence: 真实输出、输入/输出、截图窗口、步骤结果
- Avoid: 只讲功能列表，不展示结果

### T03 真实案例/项目复盘
- Signals: 我做了、过程、结果、踩坑、复盘、前后变化、项目
- Primary style: 案例复盘风
- Secondary styles: 数据诊断风、工具实测截图风、观点海报风
- Required evidence: 项目前后、截图、结果、关键决策
- Avoid: 把故事压成空洞方法论

### T04 教程/SOP/行动计划
- Signals: 怎么做、步骤、7 天、清单、流程、安装教程、操作方法
- Primary style: 工作流拆解风
- Secondary styles: 明媚手账风、工具实测截图风
- Required evidence: 步骤产物、检查清单、最终结果
- Avoid: 一页塞完整教程；安装命令挤满卡片

### T05 观点/反常识/行业判断
- Signals: 我发现、说实话、别再、不是、真正、为什么
- Primary style: 观点海报风
- Secondary styles: 数据诊断风、案例复盘风
- Required evidence: 例子、对比、真实观察
- Avoid: 纯金句，没有证明

### T06 产品发布/新功能介绍
- Signals: 发布、上线、我做了、工具、Skill、地址、安装、开源
- Primary style: 产品发布风
- Secondary styles: 工具实测截图风、工作流拆解风
- Required evidence: 产品界面、输出结果、适用场景
- Avoid: 发布会口吻、功能堆叠

### T07 读书/心理/生活经验
- Signals: 读书、情绪、成长、生活方式、关系、观察
- Primary style: 明媚手账风
- Secondary styles: 观点海报风、案例复盘风
- Required evidence: 生活片段、摘录、个人判断
- Avoid: 职场硬工具风

### T08 技术/开发/Agent/代码
- Signals: 代码、架构、Agent、MCP、部署、API、工程、debug
- Primary style: 深色工作台风
- Secondary styles: 工具实测截图风、数据诊断风
- Required evidence: 代码片段、日志、架构图、工具输出
- Avoid: 可爱手账风、过度柔和色彩

## Routing Rules

0. 如果内容是公众号长文或长 Markdown，先使用 `references/wechat-to-rednote.md` 做压缩，再按 T01-T08 选择内容类型。
1. 如果内容有真实工具输出，至少 2 页使用证据截图或证据式窗口。
2. 如果内容是求职/简历，必须出现招聘方视角和改写前后。
3. 如果内容是 Skill/工具，封面通常不先讲工具名，先讲用户痛点或结果。
4. 如果文章很长，最多保留 7-9 个传播点，其他放正文。
5. 如果内容缺少证据，先提示需要截图/样例；用户没有给，就使用清楚标注的 mock evidence，不假装是真截图。
6. 如果用户明确说之前版本土、旧、死板、AI 味重，优先选择明亮清透、证据白底、时尚编辑感或招聘评审桌风；不要选择旧纸、淡黄、复古、低饱和橙棕。

## Page Plan Pattern

```text
P1 hook cover
P2 audience pain / why now
P3 key insight
P4 evidence / screenshot
P5 transformation / before-after
P6 workflow / how it works
P7 case / proof
P8 action / template / steps
P9 closing + CTA
```

This pattern is flexible. Replace pages with stronger evidence when available.
