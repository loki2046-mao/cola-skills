# 产品 UI 规范 · product-ui.md
> 适用于：station.hiloki.ai（内容工作站）/ wechat-layout.hiloki.ai（排版编辑器）/ hiloki.ai（个人网站）/ Loki assistant / 小熊猫写作平台

---

## 核心原则（4条，记住就够）

1. **内容是主角，UI 是工具** — UI 不抢注意力。大面积中性色，品牌橙只用于当前状态/CTA/激活态
2. **暖色系统，不冰冷** — 深色侧栏用 `#1A1816`（暖墨），不用 `#000`；浅色区用 `#FDFAF5`（纸白），不用 `#FFF`
3. **信息密度适中** — 侧栏导航紧凑但不拥挤，行高 40px，字号 13-14px
4. **一致的品牌存在** — Loki 头像只在左上角 Logo 和用户头像位出现；琥珀橙只用于选中态、主按钮、品牌标识

---

## 布局骨架

所有产品页面共用：**深色侧栏（固定）+ 浅色主区域（可滚动）**

```
┌──────────┬────────────────────────────┐
│          │  顶栏（可选）               │
│  深色    ├────────────────────────────┤
│  侧栏    │                            │
│  220px   │   主内容区                 │
│  #1A1816 │   #FDFAF5                  │
│          │   flex: 1                  │
│          │                            │
└──────────┴────────────────────────────┘
```

### 侧栏规范

| 元素 | 样式 |
|------|------|
| 侧栏宽度 | 220px，flex-shrink: 0 |
| 侧栏底色 | `#1A1816` |
| 侧栏文字 | `#EBE4D6` |
| Logo 区 | padding 16px；Logo + 品牌名；底部 1px `#332F2B` 分割线 |
| 导航行高 | 40px；padding 0 16px；font-size 13px |
| 当前选中 | `background: rgba(200,122,69,0.1)`，左侧 2px `#C87A45` 竖线，文字色 `#C87A45` |
| hover 状态 | `background: rgba(255,255,255,0.04)` |
| 非选中文字 | `color: #9A9085` |
| 分组标签 | `mono 10px #6B6157 letter-spacing 0.1em`，padding 12px 16px 6px |

### 主内容区规范

| 元素 | 样式 |
|------|------|
| 背景 | `#FDFAF5` |
| 顶栏高度 | 48px；border-bottom 1px `#EBE4D6`；padding 0 20px |
| 内容 padding | 20-24px |
| 卡片底色 | `#fff`；border 1px `#EBE4D6` |
| 分割线 | `1px #EBE4D6` |

---

## 组件规范

### 按钮

```
主按钮：background #C87A45  color #fff  font-size 13px  padding 8px 16px
次按钮：background #EBE4D6  color #3A342D  font-size 13px  padding 8px 16px
危险：  background transparent  border 1px #B8624A  color #B8624A
```

不加圆角（border-radius: 0 或极小 2px），体现工具感

### 输入框

```
border: 1px solid #EBE4D6
background: #fff
color: #1F1D1A
font-size: 13px  padding: 8px 12px
focus border: #C87A45
placeholder color: #C4BBB0
```

### 标签/Badge

```
字体：JetBrains Mono 10px  letter-spacing 0.06em
样式 A（品牌）：background rgba(200,122,69,0.1)  color #C87A45  border 1px rgba(200,122,69,0.3)
样式 B（中性）：background #EBE4D6  color #3A342D
样式 C（深色）：background #332F2B  color #C4BBB0（用于深色区域）
```

### 弹窗 / Modal

```
overlay: rgba(26,24,22,0.6)
modal 背景: #FDFAF5
border: 1px #DDD2BD
标题: Smiley Sans Oblique 20px
内容 padding: 24px
```

---

## 深色场景补充

当整体使用深色主题时（如内容工作站深色模式）：

| 元素 | 浅色值 | 深色替换 |
|------|--------|---------|
| 页面背景 | `#FDFAF5` | `#1F1D1A` |
| 卡片背景 | `#fff` | `#252220` |
| 边框 | `#EBE4D6` | `#332F2B` |
| 主文字 | `#1F1D1A` | `#EBE4D6` |
| 次文字 | `#6B6157` | `#9A9085` |
| 淡文字 | `#9A9085` | `#6B6157` |

---

## 不能做的事（产品 UI 禁忌）

- 白色背景 `#FFFFFF` 大面积使用
- 蓝紫系科技感 UI
- 卡片大圆角（border-radius > 4px 慎用）
- 品牌橙用于非激活/非 CTA 元素（不要装饰性地随处洒橙色）
- Glassmorphism / 毛玻璃
- 图标太多太花（侧栏导航尽量文字为主）
