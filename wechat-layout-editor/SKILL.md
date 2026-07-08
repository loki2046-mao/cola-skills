---
name: wechat-layout-editor
description: >
  飞书文档一键转公众号排版编辑器。接收飞书文档链接，自动抓取内容、生成排版 HTML，
  并打开可视化编辑器进行块级编辑（移动、删除、合并、变色、拆分、类型切换）后复制到微信后台。
  支持6种色系切换：赤铜橙、青石蓝、松绿、玫瑰红、琥珀黄、石墨灰。
  Use when 用户说"排版""公众号排版""微信排版""layout""帮我排版""飞书转公众号"
  "帮我把飞书文档排版""用绿色系排版""换个色系""排版编辑器"，
  或提供飞书文档链接并希望转为公众号可粘贴的排版成品。
author: kude
---

# 公众号排版编辑器

将飞书文档一键转为公众号排版，支持可视化块编辑和多色系切换。

## 本地依赖

此 Skill 依赖本地安装的以下工具，不是纯远程服务：

- **Python 3.10+**
- **lark-cli**（已配置飞书认证，用于读取飞书文档内容和下载图片）
- **排版引擎脚本**：`scripts/feishu_to_copy_page.py`（相对于本 SKILL.md 所在目录）
- **编辑器页面**：`scripts/web/editor.html`（相对于本 SKILL.md 所在目录）

## 色系

6种可选色系，用户可通过名称或颜色描述指定，默认为「赤铜橙」。

| 色系名 | accent | warmBg | warmPill | warmBorder | 适用场景 |
|--------|--------|--------|----------|------------|---------|
| 赤铜橙 | #B8623C | #fff8f1 | #f5e0c5 | #ead8c2 | 默认，温暖人文 |
| 青石蓝 | #4A7B9D | #f0f5f8 | #d4e6f0 | #b8d4e3 | 冷静理性、科技 |
| 松绿 | #3D8B6E | #f0f8f4 | #d0ebde | #b2d8c5 | 自然清新、环保 |
| 玫瑰红 | #B85A6C | #fdf2f4 | #f5d4da | #eac2c8 | 情感温柔、女性 |
| 琥珀黄 | #B8923C | #fdf8f0 | #f5e8c5 | #eadcc2 | 明亮活力、教育 |
| 石墨灰 | #6B7280 | #f5f5f6 | #e0e2e5 | #d1d5db | 简约商务、中性 |

每种色系会影响：标题颜色、强调色、背景底色、药丸标签色、边框色、高亮块底色。

## 执行流程

### 1. 解析用户输入

从用户消息中提取：

- **飞书链接**：包含 `feishu.cn/docx/`、`feishu.cn/wiki/`、`feishu.cn/doc/` 的 URL
- **色系名**（可选）：匹配「赤铜橙/青石蓝/松绿/玫瑰红/琥珀黄/石墨灰」或颜色描述（橙色→赤铜橙，蓝色→青石蓝，绿色→松绿，红色/粉色→玫瑰红，黄色→琥珀黄，灰色→石墨灰）
- 没指定色系时默认「赤铜橙」

### 2. 调用排版引擎

引擎已内置 `--theme` 参数，直接在生成阶段应用色系，无需后处理替换。

```bash
TOOLS_DIR="$(dirname "$0")/scripts/svg-wechat-layout"
# 实际使用时，TOOLS_DIR 指向本 Skill 目录下的 scripts/ 子目录
# 即 ~/.cola/skills/wechat-layout-editor/scripts/

python3 "~/.cola/skills/wechat-layout-editor/scripts/feishu_to_copy_page.py" \
  --url "<飞书链接>" \
  --wechat \
  --theme "<色系名>" \
  --output-dir "<输出目录>"
```

`--theme` 可选值：`赤铜橙`（默认）、`青石蓝`、`松绿`、`玫瑰红`、`琥珀黄`、`石墨灰`。

输出目录规则：`~/.cola/outputs/公众号排版/<文章标题>/`

脚本执行成功后会输出 JSON，包含：
- `title`：文章标题
- `output_dir`：输出目录路径
- `copy`：copy.html 路径
- `block_count`：排版块数

### 3. 复制编辑器到输出目录

```bash
cp "~/.cola/skills/wechat-layout-editor/scripts/web/editor.html" "<输出目录>/editor.html"
```

### 4. 启动本地服务并打开编辑器

检查 8790 端口是否已被占用。如果没有，启动 HTTP 服务：

```bash
cd "<输出目录>"
python3 -m http.server 8790 &
```

然后用浏览器打开编辑器：

```bash
open "http://localhost:8790/editor.html"
```

或者直接打开文件：

```bash
open "<输出目录>/editor.html"
```

### 5. 向用户汇报

告诉用户：
- 文章标题
- 排版块数
- 使用的色系
- 编辑器地址
- 如何复制到微信（点击"复制到微信"按钮，去公众号后台粘贴）

## 色系快速匹配规则

用户说的话 → 色系：

- "用橙色""默认色""赤铜" → 赤铜橙
- "用蓝色""冷色""科技感" → 青石蓝
- "用绿色""清新""自然" → 松绿
- "用红色""粉色""温柔" → 玫瑰红
- "用黄色""明亮""活力" → 琥珀黄
- "用灰色""简约""商务" → 石墨灰
- "换个色系""换个颜色" → 列出6种色系让用户选

## 注意事项

- 排版引擎需要 lark-cli 已登录且有文档读取权限
- 飞书链接必须是当前用户有权限访问的文档
- 图片会自动下载并内联为 base64，copy.html 脱离服务器也能显示
- 编辑器依赖同目录下的 copy.html 加载排版内容
- `--wechat` 参数会做微信兼容净化（section→span, div→span, 去 box-shadow 等）
