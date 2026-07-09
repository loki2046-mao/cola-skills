# 各平台数据获取方式

## 公众号

**数据源：** 飞书多维表格（165 篇文章已录入）
- 字段：阅读 / 点赞 / 转发 / 在看 / 评论
- 数据文件：wechat_article_metrics.json（由 Loki 自己用脚本抓取）
- 获取方式：飞书 API 读取多维表格
- 备选：Loki 手动提供最新数据

## 小红书

**数据源：** 小红书创作者后台
- 指标：粉丝数 / 图文曝光 / 互动量 / 收藏
- 获取方式：手动输入或截图 OCR
- 注意：小红书 API 不开放，只能手动或半自动

## 网站 (hiloki.ai)

**数据源：** analytics.hiloki.ai/stats
- 获取方式：HTTP GET https://analytics.hiloki.ai/stats
- 返回 JSON：今日 PV/UV、历史总量、来源、国家
- 无需鉴权

## X / 即刻

**数据源：** 平台界面
- 指标：粉丝数 / 发布数
- 获取方式：手动输入

## AI 订阅积分

**数据源：** 飞书「AI 积分追踪」表
- 获取方式：飞书 API 读取
- 备选：Loki 手动提供
- 追踪平台：Cola、OpenClaw、ListenHub、即梦、MonicaPlus、YouMind、阿里云百炼、Lovart、Alice 等

## 实时热点

**数据源：** web_search
- 搜索关键词：AI + 热点话题
- 搜索范围：最近 24-48 小时
- 筛选：与 Loki 的内容定位（AI 工具测评/教程/个人体验）相关的热点
