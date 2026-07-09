# Cola Skills · 赛博小熊猫 Loki 的个人 Skill 集

> 这是 [Loki](https://github.com/loki2046-mao) 为 [Cola](https://docs.colaos.ai/) AI Agent 操作系统自写的 19 个 Skill 合集。涵盖 PPT 生成、社交图文、公众号写作、品牌设计系统、微信排版发布、海报生成、人生复盘等场景。

## Skills 一览

### 🎨 设计与视觉

| Skill | 说明 |
|-------|------|
| [loki-deck](loki-deck/) | 生成 Loki 个人风格的 HTML PPT（12 配色 × 12 版式 + IP 形象库，单文件输出，键盘翻页） |
| [loki-social](loki-social/) | 生成小红书/小绿书社交图文（9 配色 × 7 版式 + V2 主题切换 + 像素切割截图） |
| [loki-design-system](loki-design-system/) | Loki 品牌设计系统（色板、字体、IP 形象、组件库） |
| [cover-design-system](cover-design-system/) | 封面设计系统（多主题封面生成） |
| [xhs-card-generator](xhs-card-generator/) | 小红书图文卡片生成器（HTML + 像素切割） |
| [xiaohongshu-card-designer](xiaohongshu-card-designer/) | 小红书卡片设计师（Node.js 渲染引擎） |

### ✍️ 写作与内容

| Skill | 说明 |
|-------|------|
| [loki-writing-style](loki-writing-style/) | 按 Loki 公众号风格写作/润色文章 |
| [writing-loki-wechat-articles](writing-loki-wechat-articles/) | 完整的公众号文章写作 Skill（风格库 + 范例库） |
| [typesetting-wechat-articles](typesetting-wechat-articles/) | 公众号排版 Skill（签名图、配色、组件校验） |
| [publishing-feishu-wechat-articles](publishing-feishu-wechat-articles/) | 飞书文档 → 微信公众号发布管线 |
| [wechat-layout-editor](wechat-layout-editor/) | 微信公众号编辑器（SVG 布局 + Web 编辑器） |
| [cola-case-writer](cola-case-writer/) | 案例写作 Skill |

### 🛠️ 工具与多媒体

| Skill | 说明 |
|-------|------|
| [manim-video-pipeline](manim-video-pipeline/) | Manim 数学动画视频管线 |
| [nb-image-prompt](nb-image-prompt/) | 提示词管理库 |
| [personalized-podcast](../../) | 个性化播客（⚠️ fork 自 zarazhangrui，未包含在本仓库） |

### 🧠 知识与洞察

| Skill | 说明 |
|-------|------|
| [freeview](freeview/) | 口喷 → 作品凝聚引擎（碎片感受 → 完整解读作品） |
| [ai-career-compass](ai-career-compass/) | AI 职业罗盘 |
| [daily-collage-poem](daily-collage-poem/) | 每日拼贴诗 |
| [ie-recall-memory](ie-recall-memory/) | WPS 洞察回忆器 |
| [qichi-life-os](qichi-life-os/) | 栖迟人生系统（全量复盘 + 四维模式识别 + Obsidian 输出） |

## 使用方式

这些 Skill 是为 [Cola](https://docs.colaos.ai/) 设计的。将 Skill 目录复制到 `~/.cola/skills/` 即可使用：

```bash
# 克隆到 Cola 的 skills 目录
git clone https://github.com/loki2046-mao/cola-skills.git ~/.cola/skills/cola-skills

# 或者复制你需要的 Skill
cp -R cola-skills/loki-deck ~/.cola/skills/
```

每个 Skill 的具体用法请阅读其 `SKILL.md` 文件。

## 第三方推荐 Skill

以下 Skill 不是我写的，但我在使用中做了修改和适配，推荐一起使用：

| Skill | 作者 | 原始仓库 | 我的修改 |
|-------|------|---------|---------|
| ai-news-radar | LearnPrompt (卡尔) | [github.com/LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar) | 包装为 Cola Skill 格式，编写运行规则和发送逻辑 |
| codebase-to-course | zarazhangrui | [github.com/zarazhangrui/codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) | inline handler 矛盾修复 |
| follow-builders | zarazhangrui | [github.com/zarazhangrui/follow-builders](https://github.com/zarazhangrui/follow-builders) | — |
| frontend-slides | voltagent/zarazhangrui | [github.com/zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 删重复 plugins/、瘦身 28→14KB、export-pdf display 修复 |
| personalized-podcast | zarazhangrui | [github.com/zarazhangrui/personalized-podcast](https://github.com/zarazhangrui/personalized-podcast) | publish.py 死代码修复、bootstrap.py 配置修复、添加 run_pipeline.py 入口 |
| guizang-ppt-skill | guizang (op7418) | [github.com/op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | 硬编码路径清除、瘦身 35.8→15KB |
| comeonzhj-auto-redbook-skills | comeonzhj | — | 补 requirements.txt、taste.md/palettes.md 合并、V2 配色调整 |
| heran11011-cola-feishu-bridge | heran11011 | — | 补 frontmatter |
| self-mirror | zachbeta | — | 补女性作家镜像 |
| retrospective-base | zachbeta | — | 硬编码路径清除 |
| marswaveai-skills | marswave.ai | — | listenhub 去重、/speech→/tts 修正 |
| voltagent-awesome-design-md | voltagent | — | 补完整 SKILL.md |

## 技术特点

- **单文件输出**：PPT、社交图文、海报等视觉产物均为单 HTML 文件，浏览器直接打开
- **品牌一致性**：所有视觉 Skill 共享 `loki-design-system` 的色板、字体、IP 形象规范
- **主题切换**：loki-social V2 支持 5 套 `.theme-xxx` CSS 主题动态切换
- **像素级截图**：社交图文使用像素级切割算法，确保小红书 3:4 卡片完美呈现
- **自包含**：所有脚本（Python/Node.js）都在 Skill 目录内，无外部依赖路径

## License

MIT — 随意使用，注明来源即可。
