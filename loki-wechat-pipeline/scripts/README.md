# 自研 SVG 式公众号排版工具

这套工具是独立新写的，不走仓库里原有的飞书发布链路。

目标是：

- 从公开飞书文档抽正文和图片
- 自动提炼更像人写的节标题
- 自动给重点词句做变色加粗
- 单图统一圆角加细边
- 连续多图折成可左右滑动的图组
- 超长提示词折成固定高度、可上下滑动的代码块
- 生成一个可直接在浏览器里点“复制富文本”的页面

## 用法

```bash
python3 ./tools/svg-wechat-layout/feishu_to_copy_page.py \
  --url "https://www.feishu.cn/docx/你的文档"
```

默认输出到：

`~/.cola/skills/loki-wechat-pipeline/自研公众号排版/<标题>/`

目录里会有：

- `article.json`：结构化排版结果
- `source.html`：纯正文页
- `preview.html`：预览页
- `copy.html`：可直接复制进公众号后台的页面
- `index.html`：`copy.html` 的同内容别名

## 本地编辑器

如果你不想每次都靠自动规则，可以直接起本地排版编辑器：

```bash
python3 ./tools/svg-wechat-layout/editor_server.py --port 8789
```

然后打开：

`http://127.0.0.1:8789/`

编辑器支持：

- 从飞书公开文档直接导入
- 载入已有 `article.json`
- 手工改正文、小标题、引言、提示词块、图片块
- 上下移动、复制、删除内容块
- 右侧实时预览
- 一键保存导出新的 `copy.html`

如果你已经有一篇结果，启动时还能直接预载入：

```bash
python3 ./tools/svg-wechat-layout/editor_server.py \
  --port 8789 \
  --article-json "~/.cola/skills/loki-wechat-pipeline/自研公众号排版/某篇文章/article.json"
```

## 说明

- 这页里的正文模块都尽量使用内联样式，减少复制到公众号后台后的丢样式问题
- 图片默认会转成 `data:` 内嵌，方便本地打开后直接复制
- 如果尾图路径不存在，会自动跳过文末尾图
