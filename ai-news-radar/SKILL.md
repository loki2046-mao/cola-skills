---
name: ai-news-radar
description: AI 日报雷达 Skill。当用户说"雷达掌""AI 日报""今日 AI 新闻"时使用。按 LearnPrompt/ai-news-radar 运行思路执行 AI 日报。
author: kude
---

# AI News Radar Skill - 雷达掌专用（v3)

<!--
仓库位置说明(2026-07-05 核对)
- 完整 ai-news-radar 仓库需要单独获取，联系作者
- 该仓库不包含本 SKILL.md 引用的 bin/ai-news-radar-update、bin/ai-news-radar-top 可执行入口
- 仓库的实际更新入口是 scripts/update_news.py(python scripts/update_news.py --output-dir data --window-hours 24 --rss-opml feeds/follow.opml)
- 仓库的实际数据产物在 data/ 和 runtime-data/ 目录下(latest-24h.json、archive.json、source-status.json、waytoagi-7d.json、title-zh-cache.json)
- 由于目录结构与下方 ../bin/ 和 ../vendor/ai-news-radar/ 引用不匹配,下方路径暂时无法直接使用
- 如需运行,请先到上述完整仓库目录下手动执行 scripts/update_news.py,或为该仓库补建 bin/ 包装脚本
- 如需把仓库 vendor 化到 ~/.cola/vendor/ai-news-radar/,可复制整个仓库(排除 .venv、.git、__pycache__)
-->

## 目标
按 `LearnPrompt/ai-news-radar` 的运行思路执行 AI 日报,而不是只"参考一下名字":
- 固定信源抓取,不依赖临场发挥
- 24h 新鲜度优先,48h 仅补位
- 发送前去重、验链、分类
- 发送成功后立即写账本,防止第二天复读

## 参考项目
- https://github.com/LearnPrompt/ai-news-radar
- 该项目的关键不是"写一段摘要",而是"多源更新 + 去重归一 + 定时发送 + 历史沉淀"

## 本地运行入口(强制)
1. 不要再自己手搓 `web_fetch` 多站拼装日报,先跑本地仓库。
2. 当前工作区的统一入口:
   - 更新数据:`../bin/ai-news-radar-update`
   - 读取精简结果:`../bin/ai-news-radar-top --limit 40 --mode items_ai`
3. 仓库实际位置:`../vendor/ai-news-radar`
4. 默认输出目录:`../vendor/ai-news-radar/runtime-data`
5. 若更新命令失败,原样返回错误,不要假装"已抓取完成"。
6. `ai-news-radar-top` 默认是严格模式:会剔除无明确发布时间、聚合页、HN 评论页、GitHub 仓库首页、Product Hunt 泛产品页。

## 发送目标规则(强制)
1. AI 日报固定用 `message` 工具发送到飞书,且必须显式传 `account=bot2`。
2. `target` 优先级:
   - 今日记忆里已有的主人直发 target
   - 当前飞书消息元数据里的 `sender_id`
   - `user:<sender_id>`
3. 禁止把"缺少 chat_id"当成默认失败理由。若已有 `sender_id` 或已知 `target`,直接发送。
4. 若发送成功,必须把成功使用的 target 记到当天 `memory/YYYY-MM-DD.md`。
5. 只有在没有历史 target、也没有当前 `sender_id` 时,才允许向主人补问。
6. 如果当前是 cron 隔离会话,默认交付物是"纯文本日报"。
7. `ai-daily-report` 是例外:若 `OWNER_PROFILE.md` 已定义 bot2 固定主人 target,则可将该值直接作为 `owner_open_id` 创建飞书文档。
8. 若 cron 场景既没有 `sender_id`,也没有 `OWNER_PROFILE.md` 中已确认的固定 `owner_open_id`,必须直接跳过文档相关动作,禁止进入 `feishu-doc-publish`。

## 发现策略(强制)
1. 默认不要依赖 `web_search`。
2. 若 `web_search` 返回 `missing_brave_api_key`,立刻切换到固定信源抓取,不要反复报错。
3. 固定信源至少覆盖 3 个域名,优先从以下列表抓取:
   - `https://openai.com/news/`
   - `https://www.anthropic.com/news`
   - `https://blog.google/technology/ai/`
   - `https://deepmind.google/discover/blog/`
   - `https://huggingface.co/blog`
   - `https://www.theverge.com/ai-artificial-intelligence`
   - `https://techcrunch.com/category/artificial-intelligence/`
   - `https://www.wired.com/tag/artificial-intelligence/`
   - `https://www.aibase.com/zh/news`
   - `https://www.jiqizhixin.com/`

## 链接硬规则(强制)
1. 最终发出的必须是"具体文章页",不能是频道页、列表页、聚合页。
2. 像 The Verge AI 频道页、Wired 标签页,只能拿来发现候选,不可作为多条新闻共用链接。
3. 每条链接发送前必须验可用性,只接受 `HTTP 200/301/302`。
4. 相对链接必须转成绝对 URL 后再验链。
5. 404、4xx、5xx、登录墙、空白页、伪链接,一律丢弃。

## 新鲜度硬规则(强制)
1. 每条必须带 `发布时间` 与 `原始链接`。
2. 默认只收录最近 24 小时内容(Asia/Shanghai)。
3. 无法确认发布时间的条目,直接丢弃。
4. 若 24 小时内不足 8 条,可放宽到 48 小时,但必须显式标注 `48h补位`。
5. 严禁复用昨日或更早日报原文冒充"今日更新"。

## 去重硬规则(强制)
1. 生成去重键:`normalize(title) + host + yyyy-mm-dd`。
2. 与 `memory/ai-news-radar-sent.jsonl` 最近 7 天记录对比。
3. 标题高度相似或同链接视为重复,重复项直接丢弃。
4. 同一事件多源报道只保留 1 条,正文里可并入其他来源域名。

## 输出格式(强制)

```md
📰 AI 资讯日报 | YYYY-MM-DD

🔥 重点动态
1. 标题 - 一句话说明(发布时间:YYYY-MM-DD HH:mm)
   链接:https://...
   可用性:HTTP 200

🛠️ 工具/产品更新
- 标题 - 一句话说明(发布时间:YYYY-MM-DD HH:mm)
  链接:https://...
  可用性:HTTP 200

🎬 AI 视频相关
- 标题 - 一句话说明(发布时间:YYYY-MM-DD HH:mm)
  链接:https://...
  可用性:HTTP 200

📌 其他值得一看
- 标题 - 一句话说明(发布时间:YYYY-MM-DD HH:mm)
  链接:https://...
  可用性:HTTP 200

📊 资讯来源:列出本次真实使用的域名
⏰ 抓取时间:YYYY-MM-DD HH:mm (Asia/Shanghai)
```

## 执行流程(强制)
1. 读取 `memory/YYYY-MM-DD.md`、昨日记忆、`memory/ai-news-radar-sent.jsonl`。
2. 先解析发送目标,并确认本轮固定使用 `account=bot2`。
3. 如果这轮是 09:00 的 cron 日报任务,默认只读取已有的 `latest-24h.json`、`source-status.json` 和 `memory/ai-news-radar-sent.jsonl`,不要重复抓全量。
4. 只有在数据文件缺失时,才执行 `../bin/ai-news-radar-update`;否则直接进入读取。
5. 执行 `../bin/ai-news-radar-top --limit 40 --mode items_ai`,只基于这份精简结果挑选日报候选。
6. 对候选条目做发布时间校验、24h 过滤、链接可用性校验。
7. 与 `memory/ai-news-radar-sent.jsonl` 做去重,并按"重点 / 工具 / 视频 / 其他"分类。
8. 优先判断这轮是否具备固定 `owner_open_id`:
   - 先读取 `OWNER_PROFILE.md`
   - 校验其中 `delivery_target` 与当前 cron `delivery.to` 一致
   - 若具备,则按 `feishu-doc-publish` 规则创建飞书文档、写入、回读,并只交付本次 `create.url`
   - 若不具备,则降级为一条可直接投递的纯文本日报
9. 发送日报或文档链接。
10. 仅在发送工具返回成功后,将已发送条目写入 `memory/ai-news-radar-sent.jsonl`。
11. 将本轮发送结果、target、messageId、以及本轮使用的 `owner_open_id`(若有)记到当天记忆。

## 产物读取规则
1. 优先使用 `runtime-data/latest-24h.json` 的 `items_ai`。
2. 若 `items_ai` 太少,可回退到 `items`,但必须继续做去重和验链。
3. 不要整份回贴 JSON;只抽取将要发送的条目。
4. `source-status.json` 用于判断本轮哪些源失败,失败信息可写到日报末尾。
5. 严禁直接把 `latest-24h.json` 原始结果整批发送给主人;必须经过 `ai-news-radar-top` 的严格筛选结果。

## 账本格式(强制)
`memory/ai-news-radar-sent.jsonl` 一行一条 JSON,字段至少包含:
- `date`
- `title`
- `url`
- `hash`
- `category`
- `statusCode`

## 失败与降级
- 若有效条目 < 5:只发送"今日新增不足"短报,不复读旧文。
- 若关键源连续失败:在日报末尾标注"源站异常",并切换到同类备选源。
- 若 `web_search` 缺 key:不要卡住,直接走固定源。
- 若发送失败:不要写入去重账本;先记录失败原因,再修复发送目标。
