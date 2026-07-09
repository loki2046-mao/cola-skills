# Cola Skills · 赛博小熊猫 Loki 的个人 Skill 集

> 这是 [Loki](https://github.com/loki2046-mao) 与 Claude 合作为 [Cola](https://docs.colaos.ai/) AI Agent 操作系统自写的 10 个 Skill 合集。涵盖 PPT 生成、社交图文、公众号全链路、品牌设计系统、视频制作、海报生成、人生复盘等场景。

## Skills 一览

### 🎨 设计与视觉

| Skill | 说明 |
|-------|------|
| [loki-deck](loki-deck/) | 生成 Loki 个人风格的 HTML PPT（12 配色 × 12 版式 + IP 形象库，单文件输出，键盘翻页） |
| [loki-social](loki-social/) | 小红书/社交图文统一 Skill（4 种模式：simple 快速模板 / brand 品牌风格+IP / compress 公众号转小红书 / advanced 108组件高级定制） |
| [loki-design-system](loki-design-system/) | 品牌设计系统 — 共享基础层（SSOT），被所有视觉 Skill 引用的品牌色板、字体、IP 形象、场景规范 |

### ✍️ 公众号全链路

| Skill | 说明 |
|-------|------|
| [loki-wechat-pipeline](loki-wechat-pipeline/) | 公众号全链路工作台：写作 → 封面 → 排版 → 可视化编辑器 → 飞书发布，分层调用或全链路运行 |

### 🛠️ 工具与多媒体

| Skill | 说明 |
|-------|------|
| [manim-video-pipeline](manim-video-pipeline/) | Manim 数学动画视频管线（脚本 → TTS → ASR → Manim → BGM → ffmpeg） |
| [nb-image-prompt](nb-image-prompt/) | 图像提示词管理库（多模型适配 + Obsidian 同步） |

### 🧠 知识与洞察

| Skill | 说明 |
|-------|------|
| [freeview](freeview/) | 口喷 → 作品凝聚引擎（碎片感受 → 完整解读作品） |
| [ai-career-compass](ai-career-compass/) | AI 职业罗盘（岗位 AI 暴露度 + 求职行动教练） |
| [qichi-life-os](qichi-life-os/) | 栖迟人生系统（全量复盘 + 四维模式识别 + Obsidian 输出） |
| [daily-collage-poem](daily-collage-poem/) | 每日拼贴诗（对话提取词条 + 视觉拼贴诗笺） |

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                    Loki 的 Cola Skills                    │
├──────────────┬──────────────┬──────────────┬──────────────┤
│   内容生产    │   视觉输出    │   个人系统    │   工具/提示词  │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ loki-wechat- │ loki-deck    │ qichi-life-os│ nb-image-    │
│ pipeline     │              │              │ prompt       │
│ (写作+排版+  │ loki-social  │              │              │
│  封面+发布)  │ (小红书统一)  │ daily-       │ ai-career-   │
│              │              │ collage-poem│ compass      │
│ freeview     │ manim-video- │              │              │
│ (口喷→作品)  │ pipeline     │              │              │
├──────────────┴──────────────┴──────────────┴──────────────┤
│              loki-design-system（共享基础层）              │
│         品牌色板 · 字体 · IP 形象 · 场景规范 · 组件库       │
└─────────────────────────────────────────────────────────┘
```

## 使用方式

这些 Skill 是为 [Cola](https://docs.colaos.ai/) 设计的。将 Skill 目录复制到 `~/.cola/skills/` 即可使用：

```bash
git clone https://github.com/loki2046-mao/cola-skills.git ~/.cola/skills/cola-skills
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

## License

MIT — 随意使用，注明来源即可。
