# HTML 模板结构说明

> 每次生成的可交互诗笺 HTML 必须遵循此结构。

---

## 一、文件命名

```
~/.cola/outputs/daily-collage-poem/YYYY-MM-DD.html
```

---

## 二、整体结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
  <title>每日拼贴诗 · YYYY.MM.DD</title>
  <!-- 字体 -->
  <link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai&family=Noto+Sans+SC:wght@400;700;900&family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/lxgw-wenkai-webfont@1.7.0/style.css" rel="stylesheet">
  <!-- html2canvas（导出图片用） -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <style>
    /* ... 见下方 CSS 模板 ... */
  </style>
</head>
<body>
  <!-- 画布区 -->
  <div class="canvas-wrap" id="canvas">
    <img class="bg-img" src="data:image/png;base64,{{BASE64_IMAGE}}" alt="">
    <!-- 词条：每个 .tag 用 style="left:Xpx;top:Ypx" 绝对定位 -->
    <div class="tag chip-xxx selected" style="left:40px;top:80px">
      <div class="inner">词条文字</div>
    </div>
    <!-- ... 更多词条 ... -->
    <!-- 日期戳 -->
    <div class="datestamp">YYYY · MM · DD</div>
  </div>

  <!-- 底部工具栏 -->
  <div class="toolbar">
    <button onclick="resetPositions()">重置位置</button>
    <button class="primary" onclick="saveImage()">保存图片</button>
  </div>

  <!-- 编辑面板（点击词条弹出） -->
  <div class="edit-panel" id="editPanel">
    <label>文字内容</label>
    <input type="text" id="editText" placeholder="输入词条文字">
    <label>风格</label>
    <div class="opt-row" id="styleOpts">
      <!-- 动态生成风格按钮 -->
    </div>
    <label>大小</label>
    <div class="opt-row" id="sizeOpts">
      <button class="opt-btn" data-size="12">小</button>
      <button class="opt-btn active" data-size="15">中</button>
      <button class="opt-btn" data-size="20">大</button>
      <button class="opt-btn" data-size="26">特大</button>
    </div>
    <button style="margin-top:12px;width:100%;padding:10px;background:#333;color:#ddd;border:none;border-radius:8px;cursor:pointer" onclick="closeEdit()">完成</button>
  </div>

  <script>
    /* ... 见下方 JS 模板 ... */
  </script>
</body>
</html>
```

---

## 三、CSS 核心模板

```css
*, *::before, *::after {
  margin: 0; padding: 0; box-sizing: border-box;
  -webkit-user-select: none; user-select: none;
}
body {
  background: #1a1a1a;
  display: flex; flex-direction: column; align-items: center;
  min-height: 100vh;
  font-family: 'Noto Sans SC', sans-serif;
}

/* 画布：固定 420×560，3:4 比例 */
.canvas-wrap {
  position: relative;
  width: 420px; height: 560px;
  overflow: hidden;
  margin: 16px auto;
  border-radius: 2px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
.bg-img {
  position: absolute; inset: 0;
  width: 100%; height: 100%; object-fit: cover; z-index: 0;
}

/* 词条基础 */
.tag {
  position: absolute; z-index: 10;
  cursor: grab; line-height: 1.3;
}
.tag:active { cursor: grabbing; }
.tag.selected { outline: 2px dashed rgba(255,255,255,0.4); outline-offset: 4px; }
.tag.dragging { z-index: 999; transform: scale(1.04); }

/* 日期戳 */
.datestamp {
  position: absolute; bottom: 10px; right: 12px; z-index: 10;
  font-size: 10px; color: rgba(200,200,200,0.35);
  font-family: 'Noto Sans SC', sans-serif; letter-spacing: 3px;
  pointer-events: none;
}

/* 工具栏 */
.toolbar {
  display: flex; flex-wrap: wrap; gap: 8px;
  justify-content: center; padding: 12px 16px; max-width: 420px;
}
.toolbar button {
  padding: 6px 14px; border: 1px solid #444;
  background: #222; color: #ddd;
  border-radius: 16px; cursor: pointer; font-size: 12px;
}
.toolbar button:hover { background: #333; }
.toolbar button.primary {
  background: #EB823C; border-color: #EB823C; color: #fff; font-weight: 700;
}

/* 编辑面板 */
.edit-panel {
  display: none; position: fixed; bottom: 0; left: 0; right: 0;
  background: #1a1a1a; border-top: 1px solid #333;
  padding: 16px; z-index: 100;
  max-width: 420px; margin: 0 auto;
}
.edit-panel.show { display: block; }
.edit-panel label {
  color: #999; font-size: 11px; display: block;
  margin-bottom: 4px; margin-top: 10px;
}
.edit-panel input[type="text"] {
  width: 100%; padding: 8px;
  background: #222; border: 1px solid #444;
  color: #fff; border-radius: 6px; font-size: 14px;
  -webkit-user-select: text; user-select: text;
}
.opt-row { display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }
.opt-btn {
  padding: 4px 10px;
  background: #333; border: 1px solid #555;
  color: #ddd; border-radius: 12px; cursor: pointer; font-size: 11px;
}
.opt-btn.active { background: #EB823C; border-color: #EB823C; color: #fff; }

/* 此处粘贴 style-library.md 中所有词条样式 CSS */
/* === chip-white-note / chip-yellow-note / ... 全部 === */
```

---

## 四、JS 核心模板

```javascript
(function() {
  const canvas = document.getElementById('canvas');
  const editPanel = document.getElementById('editPanel');
  const editText = document.getElementById('editText');
  let activeTag = null;

  /* ===== 初始布局记录（用于重置）===== */
  const initialPositions = {};
  document.querySelectorAll('.tag').forEach((tag, i) => {
    tag.dataset.id = i;
    initialPositions[i] = { left: tag.style.left, top: tag.style.top };
  });

  /* ===== 拖拽（mouse + touch 双兼容）===== */
  let dragTarget = null, offsetX = 0, offsetY = 0;

  function getPos(e) {
    return e.touches
      ? { x: e.touches[0].clientX, y: e.touches[0].clientY }
      : { x: e.clientX, y: e.clientY };
  }

  function onStart(e) {
    const tag = e.target.closest('.tag');
    if (!tag) return;
    // 如果正在输入，不触发拖拽
    if (e.target.tagName === 'INPUT') return;
    e.preventDefault();
    dragTarget = tag;
    const pos = getPos(e);
    const rect = tag.getBoundingClientRect();
    offsetX = pos.x - rect.left;
    offsetY = pos.y - rect.top;
    tag.classList.add('dragging');
  }

  function onMove(e) {
    if (!dragTarget) return;
    e.preventDefault();
    const pos = getPos(e);
    const cr = canvas.getBoundingClientRect();
    dragTarget.style.left = (pos.x - cr.left - offsetX) + 'px';
    dragTarget.style.top  = (pos.y - cr.top  - offsetY) + 'px';
  }

  function onEnd(e) {
    if (!dragTarget) return;
    dragTarget.classList.remove('dragging');
    dragTarget = null;
  }

  canvas.addEventListener('mousedown', onStart);
  document.addEventListener('mousemove', onMove);
  document.addEventListener('mouseup', onEnd);
  canvas.addEventListener('touchstart', onStart, { passive: false });
  document.addEventListener('touchmove', onMove, { passive: false });
  document.addEventListener('touchend', onEnd);

  /* ===== 点击词条打开编辑面板 ===== */
  const STYLES = [
    'chip-white-note','chip-yellow-note','chip-pink-note','chip-kraft',
    'chip-round-sticker','chip-tape','chip-newspaper','chip-magazine',
    'chip-typewriter','chip-highway','chip-metro','chip-warning','chip-prohibit',
    'chip-chalk','chip-marker','chip-spray','chip-stamp','chip-subtitle',
    'chip-postcard','chip-neon'
  ];
  const STYLE_LABELS = {
    'chip-white-note':'白便签','chip-yellow-note':'黄便签','chip-pink-note':'粉便签',
    'chip-kraft':'牛皮纸','chip-round-sticker':'圆贴纸','chip-tape':'胶带',
    'chip-newspaper':'旧报纸','chip-magazine':'杂志','chip-typewriter':'打字机',
    'chip-highway':'路牌','chip-metro':'地铁','chip-warning':'警告牌',
    'chip-prohibit':'禁止牌','chip-chalk':'粉笔','chip-marker':'马克笔',
    'chip-spray':'喷漆','chip-stamp':'邮票','chip-subtitle':'字幕',
    'chip-postcard':'明信片','chip-neon':'霓虹'
  };

  canvas.addEventListener('click', e => {
    const tag = e.target.closest('.tag');
    if (!tag) { closeEdit(); return; }
    openEdit(tag);
  });

  function openEdit(tag) {
    activeTag = tag;
    document.querySelectorAll('.tag').forEach(t => t.classList.remove('selected'));
    tag.classList.add('selected');

    editText.value = tag.querySelector('.inner').textContent.trim();

    // 渲染风格按钮
    const opts = document.getElementById('styleOpts');
    opts.innerHTML = STYLES.map(s =>
      `<button class="opt-btn ${tag.classList.contains(s) ? 'active' : ''}"
        data-style="${s}" onclick="applyStyle('${s}')">${STYLE_LABELS[s]||s}</button>`
    ).join('');

    editPanel.classList.add('show');
    editText.oninput = () => {
      if (activeTag) activeTag.querySelector('.inner').textContent = editText.value;
    };
  }

  window.applyStyle = function(style) {
    if (!activeTag) return;
    STYLES.forEach(s => activeTag.classList.remove(s));
    activeTag.classList.add(style);
    document.querySelectorAll('#styleOpts .opt-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.style === style);
    });
  };

  window.closeEdit = function() {
    editPanel.classList.remove('show');
    document.querySelectorAll('.tag').forEach(t => t.classList.remove('selected'));
    activeTag = null;
  };

  /* 大小调整 */
  document.querySelectorAll('#sizeOpts .opt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      if (!activeTag) return;
      activeTag.querySelector('.inner').style.fontSize = btn.dataset.size + 'px';
      document.querySelectorAll('#sizeOpts .opt-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  /* ===== 重置位置 ===== */
  window.resetPositions = function() {
    document.querySelectorAll('.tag').forEach(tag => {
      const id = tag.dataset.id;
      if (initialPositions[id]) {
        tag.style.left = initialPositions[id].left;
        tag.style.top  = initialPositions[id].top;
      }
    });
  };

  /* ===== 保存图片（html2canvas）===== */
  window.saveImage = function() {
    closeEdit();
    // 隐藏选中高亮
    document.querySelectorAll('.tag').forEach(t => t.classList.remove('selected'));
    setTimeout(() => {
      html2canvas(canvas, {
        useCORS: true,
        allowTaint: true,
        scale: 2,
        backgroundColor: null
      }).then(cvs => {
        const a = document.createElement('a');
        a.download = '拼贴诗-' + new Date().toISOString().slice(0,10) + '.png';
        a.href = cvs.toDataURL('image/png');
        a.click();
      });
    }, 100);
  };
})();
```

---

## 五、词条初始布局算法

生成 HTML 时，为每个词条分配初始坐标，避免重叠：

1. 画布有效区域：`left: 10px ~ 360px`，`top: 20px ~ 500px`
2. 按词条数量将区域划分为网格（例如 10 词条 → 3列×4行，每格约 117×130px）
3. 每个词条在所在格内随机偏移 ±15px，并随机 rotate(-3deg ~ 3deg)
4. 路牌类（`chip-highway`/`chip-metro`）倾向于竖向排布
5. 圆形/菱形（`chip-warning`/`chip-prohibit`）预留足够 margin

---

## 六、背景图替换规则

生成时，将 ListenHub 返回的图片路径用 Python 读取并转 base64：

```python
import base64, pathlib

def img_to_base64(path: str) -> str:
    data = pathlib.Path(path).read_bytes()
    ext = pathlib.Path(path).suffix.lstrip('.').lower()
    mime = 'jpeg' if ext in ('jpg','jpeg') else 'png'
    return f"data:image/{mime};base64,{base64.b64encode(data).decode()}"
```

然后将 HTML 模板中的 `{{BASE64_IMAGE}}` 替换为该字符串。

---

## 七、注意事项

- **不用 SVG feTurbulence 做纹理** — 会产生格子/条纹伪影
- **背景图提示词不含中文文字** — AI 无法准确生成中文
- **`chip-warning` / `chip-prohibit`** 为特殊形状，词条字数控制在 2-4 字
- **画布高度固定 560px**，词条不能超出，生成时检查 top < 500
- **保存图片时临时隐藏 edit-panel**，避免截入界面元素
- **html2canvas scale: 2** 保证导出图片为 840×1120 高清
