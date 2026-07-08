# FreeView 网页视觉模式与代码参考

本文件提供 webpage 形态生成时的视觉设计参考和可复用代码片段。

## 核心原则

**网页作品打开的第一眼必须有视觉冲击。** 如果打开来是暗色背景上排着几段文字,那是失败的。

## 视觉素材三层架构

### 层 1 - CSS/Canvas/SVG 代码视觉(必须有)

这是氛围底座。用纯代码生成,不依赖外部资源。

#### 1.1 多层渐变背景

不要用单色背景。至少叠加 2-3 层渐变:

```css
.bg {
  background:
    radial-gradient(ellipse at 20% 30%, rgba(180,98,60,0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(60,40,80,0.2) 0%, transparent 50%),
    linear-gradient(180deg, #0d0a08 0%, #1a1410 50%, #0d0a08 100%);
}
```

#### 1.2 渐变流动动效

背景渐变缓慢移动,营造"画面在呼吸"的感觉:

```css
.bg-flow {
  background: linear-gradient(135deg, #1a0f0a, #2a1810, #1a0f0a, #0d0806);
  background-size: 400% 400%;
  animation: bgFlow 15s ease infinite;
}

@keyframes bgFlow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

#### 1.3 Canvas 粒子系统

以下是一个可复用的粒子系统框架。根据作品氛围调整粒子参数:

```javascript
// 雨滴粒子
class RainParticles {
  constructor(canvas) {
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.resize();
    this.init();
    this.animate();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.ctx.canvas.width = window.innerWidth;
    this.ctx.canvas.height = window.innerHeight;
  }

  init() {
    for (let i = 0; i < 80; i++) {
      this.particles.push({
        x: Math.random() * this.ctx.canvas.width,
        y: Math.random() * this.ctx.canvas.height,
        length: Math.random() * 20 + 10,
        speed: Math.random() * 8 + 4,
        opacity: Math.random() * 0.3 + 0.1,
      });
    }
  }

  animate() {
    const w = this.ctx.canvas.width;
    const h = this.ctx.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    this.particles.forEach(p => {
      this.ctx.strokeStyle = `rgba(180,160,140,${p.opacity})`;
      this.ctx.lineWidth = 1;
      this.ctx.beginPath();
      this.ctx.moveTo(p.x, p.y);
      this.ctx.lineTo(p.x - 2, p.y + p.length);
      this.ctx.stroke();

      p.y += p.speed;
      p.x -= 0.5;
      if (p.y > h) { p.y = -p.length; p.x = Math.random() * w; }
    });

    requestAnimationFrame(() => this.animate());
  }
}

// 光点粒子(萤火虫感)
class GlowParticles {
  constructor(canvas, color = 'rgba(200,160,100,') {
    this.ctx = canvas.getContext('2d');
    this.color = color;
    this.particles = [];
    this.resize();
    this.init();
    this.animate();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.ctx.canvas.width = window.innerWidth;
    this.ctx.canvas.height = window.innerHeight;
  }

  init() {
    for (let i = 0; i < 40; i++) {
      this.particles.push({
        x: Math.random() * this.ctx.canvas.width,
        y: Math.random() * this.ctx.canvas.height,
        r: Math.random() * 3 + 1,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5,
        opacity: Math.random() * 0.5 + 0.2,
        pulse: Math.random() * Math.PI * 2,
      });
    }
  }

  animate() {
    const w = this.ctx.canvas.width;
    const h = this.ctx.canvas.height;
    this.ctx.clearRect(0, 0, w, h);

    this.particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.pulse += 0.02;

      if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;

      const opacity = p.opacity * (0.5 + 0.5 * Math.sin(p.pulse));
      const r = Math.max(0.5, p.r * (0.8 + 0.2 * Math.sin(p.pulse)));

      const gradient = this.ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r * 4);
      gradient.addColorStop(0, this.color + opacity + ')');
      gradient.addColorStop(1, this.color + '0)');
      this.ctx.fillStyle = gradient;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, r * 4, 0, Math.PI * 2);
      this.ctx.fill();
    });

    requestAnimationFrame(() => this.animate());
  }
}
```

粒子类型根据作品氛围选择:
- 雨 → RainParticles(细长线条,垂直下落)
- 光点/萤火虫 → GlowParticles(发光圆点,缓慢漂浮,呼吸感)
- 雪 → 类似 GlowParticles 但白色,下落速度慢
- 花瓣 → 椭圆形粒子,旋转下落
- 灰尘 → 小白点,缓慢上浮

#### 1.4 SVG 噪点纹理

给整个页面加一层噪点,增加"胶片感":

```css
body::after {
  content: '';
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence baseFrequency='0.9' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: overlay;
}
```

#### 1.5 光晕呼吸

模拟场景中的光源在缓慢呼吸:

```css
.glow {
  position: fixed;
  width: 500px; height: 500px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(180,98,60,0.12) 0%, transparent 60%);
  filter: blur(40px);
  animation: breathe 8s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.15); }
}
```

### 层 2 - 真实剧照/截图(推荐,影视类作品)+ AI 生图(推荐,所有作品)

影视类作品优先获取真实剧照,与 AI 生图混合使用。

#### 2a. 真实剧照/截图(影视类)

获取方式见 SKILL.md「电影剧照获取方案」。剧照比 AI 生图更有「那个 feel」--观众看到真实画面会立刻被拉回电影里。

剧照选择原则:
- 选择与用户感受最匹配的场景(用户说「走廊」就搜 hallway 标签,说「雨」就搜 rain 标签)
- 3-5 张足够,不要贪多
- 剧照 + AI 生图可以混用:剧照负责「真实感」,AI 生图负责「情绪抽象化」

#### 2b. AI 氛围图(所有作品类型)

当生图能力可用时,生成 1-3 张氛围图作为关键视觉。

#### 生图提示词写法

提示词要包含:场景描述 + 情绪氛围 + 视觉风格 + 技术要求

示例(花样年华):
- "1960年代香港昏暗走廊,暖色壁灯,旗袍女子背影渐行渐远,雨打窗户,电影感,王家卫风格,暗调,景深浅,胶片质感,竖版构图"
- "两人在面摊面对面坐着,蒸汽弥漫,暖光,克制距离感,电影截图风格,暗调,侧面构图"
- "吴哥窟石墙,树洞特写,光影斑驳,一个人在低语,远景,纪录片质感,暖色调,构图留白"

示例(赛博朋克游戏):
- "霓虹城市夜景,雨后街道反射,故障感全息广告牌,暗调高对比,赛博朋克风格,宽幅构图"
- "角色站在天台俯瞰城市,风吹衣角,远景城市灯火,孤独感,电影感,冷暖色对比"

#### 图片嵌入方式

生成图片后,保存为本地文件(如 `img/scene-1.jpg`),HTML 中用相对路径引用。在以下位置使用:

1. **全屏背景 section**:
```html
<section class="full-bg" style="background-image: url('img/scene-1.jpg')">
  <div class="overlay"></div>
  <div class="text-on-image">
    <p>文字内容</p>
  </div>
</section>
```
```css
.full-bg { min-height: 100vh; background-size: cover; background-position: center; background-attachment: fixed; }
.overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.4); }
```

2. **全屏视觉打断(无文字)**:
```html
<section class="visual-break">
  <img src="img/scene-2.jpg" alt="">
</section>
```
```css
.visual-break { min-height: 100vh; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.visual-break img { width: 100%; height: 100%; object-fit: cover; }
```

3. **左右分屏**:
```html
<section class="split">
  <div class="split-img"><img src="img/scene-3.jpg" alt=""></div>
  <div class="split-text"><p>文字</p></div>
</section>
```

### 层 3 - 用户提供的图片(可选)

如果用户提供了截图、照片等素材,直接引用。处理方式同层 2。

**混合方案的优先级**:
- 影视类 + 有浏览器工具 → 层1 + 层2a(剧照)+ 层2b(AI生图)+ 层3(如果有)
- 影视类 + 无浏览器工具 → 层1 + 层2b(AI生图)+ 层3(如果有)
- 非影视类 + 有生图能力 → 层1 + 层2b(AI生图)+ 层3(如果有)
- 非影视类 + 无生图能力 → 层1(纯代码视觉)+ 层3(如果有)
- 纯代码视觉的天花板有限,要尽力用 Canvas 做出复杂效果(粒子、光影、渐变叠加),不能只是一个纯色背景

## 布局模式

至少交替使用 3 种以上布局,不要从头到尾一种排版:

### A. 全屏图 + 叠加文字
全屏背景图 + 半透明遮罩 + 文字层

### B. 全屏视觉打断(无文字)
整页只有一张图或 Canvas 动画。这是"呼吸点"。至少要有 1 个。

### C. 左右分屏
一侧视觉一侧文字。可以交替左右。

### D. 碎片拼贴
不规则排列的文字块 + 视觉元素。用 grid 或 absolute 定位。

### E. 文字流 + 动态背景
连续文字,但背景在变化(渐变流动、粒子、光影移动)

### F. 卡片层叠
内容块带阴影和偏移,有层次感

## 滚动动效

### 视差滚动
```javascript
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  document.querySelectorAll('[data-parallax]').forEach(el => {
    const speed = el.dataset.parallax || 0.5;
    el.style.transform = `translateY(${scrolled * speed}px)`;
  });
});
```

### 元素滚入渐入
```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
    }
  });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
```
```css
.reveal { opacity: 0; transform: translateY(40px); transition: all 1.2s cubic-bezier(0.16, 1, 0.3, 1); }
.reveal.visible { opacity: 1; transform: translateY(0); }
```

### 鼠标驱动视差
```javascript
document.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 2;
  const y = (e.clientY / window.innerHeight - 0.5) * 2;
  document.querySelectorAll('[data-tilt]').forEach(el => {
    const depth = el.dataset.tilt || 10;
    el.style.transform = `translate(${x * depth}px, ${y * depth}px)`;
  });
});
```

## 色彩参考

不用默认蓝紫色系。根据作品和感受选择:

| 情绪 | 色调方向 | 示例色值 |
|------|----------|----------|
| 温暖/怀旧 | 暖琥珀/赤铜/暖灰 | #B8623C #D4A76A #2A1810 |
| 冷峻/疏离 | 冷灰/青/墨黑 | #3A4A50 #6A7A80 #0A0E10 |
| 热烈/冲动 | 朱红/橙/暖黄 | #D4422E #E8804A #1A0808 |
| 沉郁/内省 | 深蓝/墨绿/深灰 | #1A2A30 #2A3A35 #0D1518 |
| 轻盈/明亮 | 奶白/浅米/淡彩 | #F5EDE0 #D4C8B8 #E8DDD0 |
| 不安/混乱 | 高对比/故障感 | #FF003C #00FFC8 #0A0A0A |

## 排版

- 中文正文行高 1.8-2.0
- 正文字号移动端 16-18px,桌面 18-22px
- 段间距 > 行间距
- 长文 max-width: 680px
- 标题不要太大,要有呼吸感,letter-spacing 适当

## 技术约束

- 自包含 HTML+CSS+JS
- 不用外部 CDN/库
- 系统字体栈
- 移动端响应式
- Canvas 粒子 ≤ 100 个
- `prefers-reduced-motion` 兼容
- 如果用了 AI 生图:图片用相对路径引用(同目录下 img/ 子目录),或 base64 嵌入(每张 < 100KB 时)

## 自检清单

生成网页后,对照以下清单检查:

- [ ] 打开第一眼有视觉冲击？（不是“暗色背景上排着文字”）
- [ ] 至少有 1 个全屏视觉打断 section？（无文字，纯视觉）
- [ ] 至少有 3 种以上不同布局？
- [ ] 背景有多层渐变 + 动效？
- [ ] 有 Canvas 粒子系统或持续运行的视觉动效？
- [ ] 滚动有视差/渐入动效？
- [ ] 至少 2 个交互元素？（进入遮罩/音频开关/黑胶点击/留言展示/鼠标视差）
- [ ] 如果有音频：rainGain 和 musicGain 都是全局变量？进入遮罩解决自动播放？
- [ ] 交互元素的 CSS animation 没有被 JS transform 覆盖？
- [ ] 如果是影视类：有真实剧照？（不是只有 AI 生图）
- [ ] 如果有 AI 生图：至少 1 张氛围图作为全屏背景或打断？
- [ ] 移动端可读？
- [ ] 文字内容占整体内容比例 < 60%？（文字是视觉的一部分，不是全部）

如果任何一项不达标,修改后再输出。

## Web Audio API - 音频合成

纯代码合成环境音效和配乐,不需要外部音频文件。解决浏览器自动播放限制。

### 进入遮罩(解决自动播放限制)

浏览器不允许页面加载时自动播放音频,必须在用户交互后才能启动 AudioContext。用进入遮罩解决:

```html
<div id="enterScreen" style="position:fixed;inset:0;background:var(--dark);display:flex;align-items:center;justify-content:center;z-index:10000;">
  <button id="enterBtn">进 入</button>
</div>
```
```javascript
document.getElementById('enterBtn').addEventListener('click', () => {
  initAudio();
  document.getElementById('enterScreen').classList.add('hidden'); // CSS transition opacity 0→1, 1.5s
});
```

### 雨声合成(白噪声 + 低通滤波)

```javascript
function initAudio() {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

  // 雨声 - 白噪声 + 低通滤波
  const bufferSize = audioCtx.sampleRate * 2;
  const noiseBuffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
  const data = noiseBuffer.getChannelData(0);
  for (let i = 0; i < bufferSize; i++) {
    data[i] = Math.random() * 2 - 1;
  }

  const rainSource = audioCtx.createBufferSource();
  rainSource.buffer = noiseBuffer;
  rainSource.loop = true;

  const rainFilter = audioCtx.createBiquadFilter();
  rainFilter.type = 'lowpass';
  rainFilter.frequency.value = 800;
  rainFilter.Q.value = 0.5;

  const rainGain = audioCtx.createGain();
  rainGain.gain.value = 0.12;

  rainSource.connect(rainFilter);
  rainFilter.connect(rainGain);
  rainGain.connect(audioCtx.destination);
  rainSource.start();
}
```

调整 `rainFilter.frequency` 改变雨声质感:
- 800Hz - 中雨打窗户
- 400Hz - 沉闷的远处雨声
- 1200Hz - 清脆的雨滴

### 配乐合成(振荡器 + ADSR 包络)

用振荡器生成简单的旋律循环,致敬作品的配乐风格:

```javascript
// 三拍子华尔兹循环(致敬 Yumeji's Theme 的节奏)
const musicGain = audioCtx.createGain();
musicGain.gain.value = 0.08;
musicGain.connect(audioCtx.destination);

const notes = [440, 0, 523, 0, 440, 0]; // A, rest, C, rest, A, rest
const noteDuration = 0.5;
let beatIndex = 0;

function playBeat() {
  if (!isPlaying) return;
  const freq = notes[beatIndex % notes.length];
  if (freq > 0) {
    const osc = audioCtx.createOscillator();
    const oscGain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.value = freq;

    const now = audioCtx.currentTime;
    oscGain.gain.setValueAtTime(0, now);
    oscGain.gain.linearRampToValueAtTime(0.15, now + 0.05);  // Attack
    oscGain.gain.exponentialRampToValueAtTime(0.001, now + noteDuration * 0.9); // Release

    osc.connect(oscGain);
    oscGain.connect(musicGain);
    osc.start(now);
    osc.stop(now + noteDuration);
  }
  beatIndex++;
  setTimeout(playBeat, noteDuration * 1000);
}
playBeat();
```

### 音频统一控制

**重要:rainGain 和 musicGain 都要设为全局变量**,不要做成局部变量。否则暂停/播放时无法同时控制雨声和配乐。

```javascript
let audioCtx = null, rainGain = null, musicGain = null, isPlaying = true;

function setAudioState(playing) {
  isPlaying = playing;
  if (!audioCtx) return;
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const t = audioCtx.currentTime;
  if (rainGain) rainGain.gain.setValueAtTime(playing ? 0.12 : 0, t);
  if (musicGain) musicGain.gain.setValueAtTime(playing ? 0.08 : 0, t);
}
```

## 交互组件

### 黑胶唱片(可点击暂停/播放)

```html
<div class="vinyl" id="vinyl"></div>
```
```css
.vinyl {
  width: 200px; height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, #1a1a1a 30%, #2a2a2a 30%, #1a1a1a 31%, #2a2a2a 50%, #1a1a1a 51%);
  animation: spin 8s linear infinite;
  cursor: pointer;
  margin: 0 auto;
}
.vinyl.paused { animation-play-state: paused; }
@keyframes spin { to { transform: rotate(360deg); } }
```
```javascript
// 注意:黑胶不要加 data-tilt,否则鼠标视差的 transform 会覆盖旋转动画
document.getElementById('vinyl').addEventListener('click', () => {
  setAudioState(!isPlaying);
  document.getElementById('vinyl').classList.toggle('paused', !isPlaying);
});
```

### 留言展示(写完即展示)

用户在 textarea 写感受,点击按钮后留言展示在页面上(本地,不上传):

```html
<textarea id="userFeeling" placeholder="......"></textarea>
<button id="submitFeeling">留下</button>
<div class="feelings-wall" id="feelingsWall" style="display:none;">
  <div class="wall-label">- 此刻的感受 -</div>
</div>
```
```javascript
document.getElementById('submitFeeling').addEventListener('click', () => {
  const textarea = document.getElementById('userFeeling');
  const text = textarea.value.trim();
  if (!text) return;

  const wall = document.getElementById('feelingsWall');
  wall.style.display = 'block';

  const item = document.createElement('div');
  item.className = 'feeling-item';
  const now = new Date();
  const timeStr = now.getFullYear() + '.' + String(now.getMonth()+1).padStart(2,'0') + '.' + String(now.getDate()).padStart(2,'0') + ' ' + String(now.getHours()).padStart(2,'0') + ':' + String(now.getMinutes()).padStart(2,'0');
  item.innerHTML = '<div class="feeling-time">' + timeStr + '</div>' + text.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\n/g, '<br>');
  wall.appendChild(item);

  textarea.value = '';
  textarea.placeholder = '再写一点......';
});
```
```css
.feeling-item {
  padding: 1rem 1.2rem;
  margin-bottom: 0.8rem;
  background: rgba(26,20,16,0.5);
  border-left: 2px solid rgba(184,98,60,0.3);
  animation: fadeInUp 0.8s ease forwards;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
```
