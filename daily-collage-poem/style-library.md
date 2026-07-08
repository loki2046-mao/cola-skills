# 拼贴诗 · 样式库

> 从 `~/.cola/outputs/daily-collage-poem/风格展板.html` 提取整理

---

## 一、词条样式完整定义

以下每条样式的 class 名称、HTML 结构和关键 CSS 均已提炼，可直接在生成 HTML 时复用。

### 贴纸类

#### `chip-white-note` — 白色便签纸
```html
<div class="chip chip-white-note"><div class="inner">文字</div></div>
```
```css
.chip-white-note .inner {
  background: #fff;
  padding: 10px 14px;
  font-family: 'LXGW WenKai', serif;
  font-size: 15px;
  color: #333;
  box-shadow: 2px 3px 8px rgba(0,0,0,0.13), 0 1px 2px rgba(0,0,0,0.08);
  transform: rotate(-2deg);
  line-height: 1.5;
  /* 伪元素：横线纹理 */
}
```
适合：日常碎念、温柔记录

#### `chip-yellow-note` — 黄色便签纸
```css
.chip-yellow-note .inner {
  background: linear-gradient(180deg, #fff9b1 0%, #f7e879 100%);
  padding: 10px 14px;
  font-family: 'LXGW WenKai', serif; font-size: 15px; color: #5a4e00;
  box-shadow: 2px 3px 8px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.1);
  transform: rotate(1.5deg); line-height: 1.5;
}
```
适合：待办、小确幸、待记事项

#### `chip-pink-note` — 粉色便签纸
```css
.chip-pink-note .inner {
  background: linear-gradient(180deg, #ffe4ec 0%, #ffc8d9 100%);
  padding: 10px 14px;
  font-family: 'LXGW WenKai', serif; font-size: 15px; color: #7a2043;
  box-shadow: 2px 3px 8px rgba(0,0,0,0.13);
  transform: rotate(-1deg); line-height: 1.5;
}
```
适合：情绪碎片、感受词

#### `chip-kraft` — 牛皮纸便签
```css
.chip-kraft .inner {
  background: linear-gradient(160deg, #d4b896 0%, #c4a67a 50%, #b89968 100%);
  padding: 10px 14px;
  font-family: 'Noto Serif SC', serif; font-size: 15px; color: #3e2c14;
  box-shadow: 2px 3px 8px rgba(0,0,0,0.18);
  transform: rotate(0.8deg); line-height: 1.5;
  /* 伪元素：布纹 */
}
```
适合：复古感、有重量的词

#### `chip-round-sticker` — 圆角贴纸
```css
.chip-round-sticker .inner {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  padding: 7px 16px;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 700; font-size: 14px;
  color: #fff; border-radius: 20px;
  box-shadow: 0 2px 6px rgba(99,102,241,0.35);
  letter-spacing: 1px;
}
```
适合：标签词、人名、关键词

#### `chip-tape` — 胶带贴纸
```css
.chip-tape .inner {
  background: linear-gradient(180deg, rgba(255,255,220,0.55) 0%, rgba(255,255,200,0.45) 100%);
  padding: 6px 18px;
  font-family: 'Noto Sans SC', sans-serif; font-size: 13px; color: #555;
  backdrop-filter: blur(1px);
  border-top: 1px solid rgba(255,255,255,0.6);
  border-bottom: 1px solid rgba(200,190,150,0.4);
  transform: rotate(-1.5deg);
  /* 伪元素：胶带边缘锯齿纹 */
}
```
适合：透明感的小标注

---

### 剪报 / 杂志类

#### `chip-newspaper` — 旧报纸裁剪
```css
.chip-newspaper .inner {
  background: #f4edd8;
  padding: 8px 12px;
  font-family: 'Noto Serif SC', serif; font-size: 16px; font-weight: 700;
  color: #2a2218; filter: sepia(0.2);
  clip-path: polygon(2% 5%, 97% 0%, 100% 93%, 4% 98%);
  box-shadow: 1px 2px 5px rgba(0,0,0,0.15); line-height: 1.4;
  /* 伪元素：横线纹理 */
}
```
适合：记录性、有分量的事实句

#### `chip-magazine` — 杂志裁剪
```css
.chip-magazine .inner {
  background: linear-gradient(135deg, #ff006e, #fb5607);
  padding: 7px 14px;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 900; font-size: 16px;
  color: #fff;
  clip-path: polygon(3% 0%, 100% 2%, 97% 100%, 0% 96%);
  letter-spacing: 2px; text-transform: uppercase;
}
```
适合：英文词、强调词、爆炸式关键词

#### `chip-typewriter` — 打字机字条
```css
.chip-typewriter .inner {
  background: #f5f0e6;
  padding: 6px 16px;
  font-family: 'Courier New', 'SF Mono', monospace; font-size: 14px; color: #222;
  border-top: 1px solid #ccc; border-bottom: 1px solid #ccc;
  letter-spacing: 2px;
  text-shadow: 0 0 0.5px rgba(0,0,0,0.6);
  /* 伪元素：纵向格线 */
}
```
适合：代码感词条、英文短句、日期

---

### 路牌 / 标志类

#### `chip-highway` — 公路路牌
```css
.chip-highway .inner {
  background: #00694b;
  padding: 8px 18px;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 700; font-size: 15px;
  color: #fff; border-radius: 6px;
  border: 3px solid #c0c0c0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3); letter-spacing: 3px;
}
```
适合：方向感词、目标、地点

#### `chip-metro` — 地铁站牌
```css
.chip-metro .inner {
  background: #003882;
  padding: 6px 20px;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 700; font-size: 15px;
  color: #fff; border-radius: 3px;
  border: 2px solid #fff; outline: 2px solid #003882;
  box-shadow: 0 2px 8px rgba(0,0,0,0.25); letter-spacing: 4px;
}
```
适合：站名感、身份词、起点/终点

#### `chip-warning` — 黄色警告牌（菱形）
```css
.chip-warning .inner {
  background: #ffd000;
  padding: 12px 14px;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 900; font-size: 14px;
  color: #1a1a00; border: 3px solid #1a1a00;
  transform: rotate(45deg);
  width: 72px; height: 72px;
  display: flex; align-items: center; justify-content: center;
  text-align: center; line-height: 1.2;
}
/* 注意：外层 .chip-warning 需要 margin: 10px 16px 20px */
```
适合：警示性词条（最多2-3字）

#### `chip-prohibit` — 红色禁止牌（圆形）
```css
.chip-prohibit .inner {
  background: #d40000;
  width: 68px; height: 68px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 900; font-size: 13px;
  color: #fff; border: 4px solid #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3), inset 0 0 0 2px #d40000;
  text-align: center; line-height: 1.2;
}
```
适合：禁止/否定词（最多2字）

---

### 手写 / 涂鸦类

#### `chip-chalk` — 粉笔效果（需深色背景）
```css
.chip-chalk {
  background: #2d4a3e; /* 黑板绿底 */
  padding: 8px 10px; border-radius: 4px;
}
.chip-chalk .inner {
  font-family: 'LXGW WenKai', serif; font-size: 20px;
  color: rgba(255,255,255,0.85);
  text-shadow: 0 0 2px rgba(255,255,255,0.4), 0 0 4px rgba(255,255,255,0.2),
               1px 1px 0 rgba(255,255,255,0.15), -1px 0 0 rgba(255,255,255,0.1);
  padding: 6px 12px; letter-spacing: 2px; filter: blur(0.3px);
}
```
适合：黑板风格主题、深夜感

#### `chip-marker` — 马克笔
```css
.chip-marker .inner {
  font-family: 'Noto Sans SC', sans-serif; font-weight: 900;
  font-size: 18px; font-style: italic; color: #1a1a1a;
  padding: 4px 14px;
  background: linear-gradient(180deg, rgba(255,230,0,0.6) 50%, rgba(255,230,0,0.9) 50%);
  transform: rotate(-2deg); display: inline-block;
}
```
适合：高亮重点词、画线感

#### `chip-spray` — 喷漆效果
```css
.chip-spray .inner {
  font-family: 'Noto Sans SC', sans-serif; font-weight: 900;
  font-size: 22px; color: #ff1744;
  text-shadow:
    0 0 4px rgba(255,23,68,0.6), 0 0 8px rgba(255,23,68,0.3),
    2px 2px 6px rgba(255,23,68,0.2), -1px -1px 4px rgba(255,23,68,0.15),
    3px 0 10px rgba(255,23,68,0.1);
  padding: 6px 12px; letter-spacing: 3px;
}
```
适合：爆发感、情绪强烈的词

---

### 特殊类

#### `chip-stamp` — 邮票（需特殊外框）
```css
.chip-stamp {
  padding: 8px;
  background: radial-gradient(circle, transparent 4px, #fff 4px, #fff 5px, transparent 5px) -5px -5px / 10px 10px repeat;
}
.chip-stamp .inner {
  background: #e8f0e4; border: 2px solid #6b8f5e;
  padding: 10px 14px;
  font-family: 'Noto Serif SC', serif; font-size: 13px; color: #3a5a2e;
  text-align: center; line-height: 1.5;
  /* 伪元素::after 显示面值 '¥1.20' */
}
```
适合：纪念性词条、有仪式感的话

#### `chip-subtitle` — 电影字幕条
```css
.chip-subtitle .inner {
  background: rgba(0,0,0,0.72);
  padding: 6px 20px;
  font-family: 'Noto Sans SC', sans-serif; font-weight: 700; font-size: 15px;
  color: #fff; text-align: center;
  letter-spacing: 2px; text-shadow: 0 1px 3px rgba(0,0,0,0.8);
}
```
适合：深夜感、沉静的句子

#### `chip-postcard` — 明信片
```css
.chip-postcard .inner {
  background: #fffef8; padding: 14px 18px;
  font-family: 'LXGW WenKai', serif; font-size: 14px; color: #555;
  border-radius: 8px; border: 1px solid #ddd;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  line-height: 1.6; min-width: 140px;
  /* 伪元素：右上角邮票emoji、底部虚线 */
}
```
适合：温暖的短句、想分享的话

#### `chip-neon` — 霓虹灯（需深色背景）
```css
.chip-neon {
  background: #0a0a1a; padding: 10px 12px; border-radius: 6px;
}
.chip-neon .inner {
  font-family: 'Noto Sans SC', sans-serif; font-weight: 700; font-size: 20px;
  color: #fff;
  text-shadow:
    0 0 5px #ff00de, 0 0 10px #ff00de, 0 0 20px #ff00de,
    0 0 40px #ff00de, 0 0 60px #bc13fe;
  padding: 4px 10px; letter-spacing: 3px;
  animation: neonFlicker 3s ease-in-out infinite;
}
@keyframes neonFlicker {
  0%, 100% { opacity: 1; }
  92% { opacity: 1; } 93% { opacity: 0.7; }
  94% { opacity: 1; } 96% { opacity: 0.85; } 97% { opacity: 1; }
}
```
适合：夜晚主题、兴奋情绪、庆祝

---

## 二、画布背景定义

| class 名 | 描述 | 颜色/实现方式 |
|---------|------|------------|
| `bg-cement` | 浅灰水泥墙 | `#e8e6e3` + 细格线 repeating-linear-gradient |
| `bg-wood` | 深色木板墙 | `#3e2a1a` + 木纹条纹 gradient 叠加 |
| `bg-paper` | 米白旧报纸底 | `#f0e8d0` + 横线纹理 + `sepia(0.05)` |
| `bg-blackboard` | 黑板绿 | `#1a3329` + 微弱网格 + radial 光晕 |
| `bg-white` | 纯白墙 | `#fff` |
| `bg-warm` | 暖色渐变 | `linear-gradient(160deg, #ffbe76, #ff7979, #eb4d4b)` |
| `bg-cool` | 冷色渐变 | `linear-gradient(160deg, #a29bfe, #6c5ce7, #341f97)` |
| `bg-photo` | 城市光斑 | Unsplash 写真背景（自动替换为 ListenHub 生成图） |
| `bg-window` | 窗边漏光 | Unsplash 写真背景 |
| `bg-rain` | 雨后玻璃 | Unsplash 写真背景 |
| `bg-film` | 胶片暖调 | Unsplash 写真背景 |
| `bg-alley` | 小巷街景 | Unsplash 写真背景 |

> 生成 HTML 时，**写真类背景统一改为 ListenHub 生成的 base64 内嵌图**，不用 Unsplash URL（避免 CORS）。

---

## 三、艺术形式库

| 形式 | 适合情绪 | 背景 class / 背景图提示词方向 | 词条样式组合 |
|------|---------|--------------------------|------------|
| 涂鸦墙 | 兴奋、叛逆、轻松 | `bg-cement` 或自定义图（dry concrete wall, front view, plain light texture, no text, no logos, photorealistic） | `chip-spray` 大字 + `chip-spray` 小字（不同颜色）+ `chip-marker` |
| 杂志剪报 | 文艺、思考、日常 | `bg-paper` 或自定义图（old wooden table surface, warm light, flat lay, no text） | `chip-newspaper` + `chip-magazine` + `chip-typewriter` + `chip-kraft` |
| 路牌指引 | 迷茫、选择、方向感 | 自定义图（empty crossroads, gray sky, no people, photorealistic） | `chip-highway` + `chip-metro` + `chip-warning` + `chip-prohibit` |
| 便签墙 | 忙碌、多任务、计划 | `bg-cement` 或自定义图（cork board texture, warm light, close up, no text） | `chip-white-note` + `chip-yellow-note` + `chip-pink-note` + `chip-round-sticker` |
| 电影字幕 | 沉静、深夜、温柔 | 自定义图（dark cinematic cityscape at night, window glow, moody, no text） | `chip-subtitle` + `chip-typewriter` + `chip-tape`（透明感） |
| 霓虹灯 | 兴奋、夜晚、庆祝 | 自定义图（dark wet alley at night, neon reflections, no text, no people） | `chip-neon` + `chip-metro` + `chip-round-sticker` |
| 明信片 | 温暖、分享、思念 | 自定义图（warm coffee shop window corner, sunlight, blurred background, no text） | `chip-postcard` + `chip-stamp` + `chip-tape` + `chip-kraft` |
| 旧报纸 | 记录、复古、回顾 | `bg-paper` 或自定义图（aged sepia newspaper pages spread on table, no readable text） | `chip-newspaper` + `chip-typewriter` + `chip-stamp` + `chip-magazine` |
| 黑板涂鸦 | 学习、思考、深夜 | `bg-blackboard` 或自定义图（old school chalkboard texture, no text） | `chip-chalk` + `chip-marker` + `chip-typewriter` |
| 街边张贴 | 随意、自由、混搭 | 自定义图（urban wall covered in old layered posters, texture, no readable text） | `chip-round-sticker` + `chip-tape` + `chip-newspaper` + `chip-spray` |

---

## 四、字体引用

```html
<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai&family=Noto+Sans+SC:wght@400;700;900&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">
<!-- 备用 LXGW CDN -->
<link href="https://cdn.jsdelivr.net/npm/lxgw-wenkai-webfont@1.7.0/style.css" rel="stylesheet">
```

字体映射：
- `'LXGW WenKai', serif` — 手写/毛笔感，用于便签、明信片、粉笔
- `'Noto Serif SC', serif` — 衬线中文，用于报纸、牛皮纸、邮票
- `'Noto Sans SC', sans-serif` — 现代无衬线，用于路牌、圆角贴纸、喷漆
- `'Courier New', monospace` — 打字机感
