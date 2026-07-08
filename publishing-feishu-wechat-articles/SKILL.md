---
name: publishing-feishu-wechat-articles
description: Use this skill when the user provides a public Feishu doc link and wants a WeChat Official Account article that can be pasted or auto-filled into the WeChat backend while keeping text editable and images uploaded natively. Trigger for requests about 飞书文档转公众号, 公众号后台直发, 飞书链接排版, 可编辑公众号排版, or when the user wants a one-link-to-WeChat workflow.
author: kude
---

# 飞书转公众号直发

这个 skill 处理的是一条固定工作流：

`公开飞书文档链接 -> 本地抽取 -> 结构清洗 -> 生成微信公众号发布包 -> 自动灌进公众号后台`

目标不是做一个“网页预览稿”，而是做一个**微信公众号后台真的能吃进去**的版本。

默认优先级：

1. 正文可编辑
2. 图片原生可点开
3. 稳定
4. 美观

## 什么时候用

在下面这些情况，优先用这个 skill：

- 用户直接给出飞书云文档链接
- 用户明确要“公众号后台可用”
- 用户强调“文字还要继续编辑”
- 用户强调“图片要能点开”
- 用户不想先自己整理 Markdown

## 核心原则

1. 不走“自由 HTML 网页 -> 微信富文本”的旧路
2. 直接按“微信兼容子集”生成发布包
3. 先保证结构和可编辑性，再追装饰
4. 图片永远走后台原生上传

## 默认流程

### 1. 抽取飞书原文

运行：

```bash
python3 scripts/extract_public_feishu_doc.py \
  --url "公开飞书文档链接"
```

抽取结果会落到：

- `已下载的推文/<文章标题>_feishu/feishu-extracted.json`
- `已下载的推文/<文章标题>_feishu/正文.txt`
- `已下载的推文/<文章标题>_feishu/图片素材/`

### 2. 生成微信原生发布包

运行：

```bash
python3 scripts/build_wechat_native_from_feishu.py \
  --input "/绝对路径/feishu-extracted.json"
```

这一步会生成：

- `.wechat-publish-package-wechat-native/manifest.json`
- `.wechat-publish-package-wechat-native/publish-preview.html`

### 3. 自动灌进公众号后台

运行：

```bash
python3 scripts/publish_to_wechat.py \
  --manifest "/绝对路径/.wechat-publish-package-wechat-native/manifest.json" \
  --save-draft \
  --keep-open \
  --verbose
```

## 单命令入口

如果不想分三步，直接走：

```bash
python3 scripts/run_feishu_wechat_pipeline.py \
  --url "公开飞书文档链接" \
  --save-draft \
  --keep-open \
  --verbose
```

这条命令默认就是 `wechat-copy-native`，也就是：

- 正文走微信兼容富文本
- 图片走后台原生上传
- 优先满足“可编辑 + 可点开”

如果你明确更想要“尽量接近预览稿”，再传：

```bash
--mode high-fidelity
```

## 当前实现保证

- 会优先保留飞书里的标题层级
- 会按正文流中的图片顺序插图
- 会避免把大面积背景、复杂卡片、整页网页样式硬塞进微信公众号后台
- 会把正文按更安全的“标题 / 引语 / 正文 / 图片”块来发布

## 当前实现不做的事

- 不承诺和浏览器预览稿完全 1:1 一致
- 不强行保留复杂阴影、分栏、整页底纹
- 不把截图里的 OCR 垃圾字当成正文

## 调试优先级

如果结果不好看，不要立刻重写整篇。按下面顺序排查：

1. 飞书抽取是不是把正文和截图 OCR 混在了一起
2. 图片块顺序是不是正确
3. 标题块是不是识别成了正文
4. 发布器是不是把某些块错误地按纯文本或富文本处理了

## 输出验收标准

至少满足下面四点才算过关：

1. 微信后台里正文是可编辑的
2. 图片是后台原生图片，能点开
3. 标题、小节、引语、正文不会糊成一坨
4. 不出现全文大面积脏底和奇怪底纹
