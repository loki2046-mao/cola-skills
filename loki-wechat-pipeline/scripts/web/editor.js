const state = {
  docId: "",
  title: "",
  sourceUrl: "",
  outputDir: "",
  article: { title: "", blocks: [] },
  renderTimer: null,
  lastSaved: null,
  lastRenderPayload: null,
  selectedBlocks: new Set(),
  focusedBlockIndex: null,
  history: [],
};

const MERGE_KIND_LABELS = {
  hero: "导读头图块",
  video: "视频块",
  text: "正文块",
  heading: "小标题",
  subheading: "二级标题",
  quote: "引言块",
  highlight: "金句块",
  prompt: "提示词块",
  meta: "信息行",
  list: "分点块",
  "group-horizontal": "横向三栏",
  "group-vertical": "纵向卡片",
};

const ui = {
  sourceUrl: document.getElementById("source-url"),
  articlePath: document.getElementById("article-path"),
  titleInput: document.getElementById("title-input"),
  outputDir: document.getElementById("output-dir"),
  importBtn: document.getElementById("import-btn"),
  loadBtn: document.getElementById("load-btn"),
  saveBtn: document.getElementById("save-btn"),
  undoBtn: document.getElementById("undo-btn"),
  autoLayoutBtn: document.getElementById("auto-layout-btn"),
  copyPreviewBtn: document.getElementById("copy-preview-btn"),
  mergeKindSelect: document.getElementById("merge-kind-select"),
  mergeSelectedBtn: document.getElementById("merge-selected-btn"),
  clearSelectionBtn: document.getElementById("clear-selection-btn"),
  copyLink: document.getElementById("copy-link"),
  blockList: document.getElementById("block-list"),
  previewFrame: document.getElementById("preview-frame"),
  renderStatus: document.getElementById("render-status"),
  statusPill: document.getElementById("status-pill"),
  stats: document.getElementById("stats"),
  saveMeta: document.getElementById("save-meta"),
  selectionMeta: document.getElementById("selection-meta"),
  emptyTemplate: document.getElementById("empty-blocks-template"),
};

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function selectedIndices() {
  return Array.from(state.selectedBlocks).sort((a, b) => a - b);
}

function mergeKindLabel(kind) {
  return MERGE_KIND_LABELS[kind] || kind;
}

function normalizeListItems(items) {
  if (Array.isArray(items)) {
    return items.map((item) => String(item || "")).filter((item) => item.trim());
  }
  if (typeof items === "string") {
    return items.split(/\n+/).map((item) => item.trim()).filter(Boolean);
  }
  return [];
}

function normalizeKeywords(items) {
  return normalizeListItems(items).slice(0, 6);
}

function extractKeywordDrafts(text = "", limit = 4) {
  const seen = new Set();
  return String(text || "")
    .split(/[|｜/、，,。：:；;\s]+/)
    .map((item) => item.trim())
    .filter((item) => item.length >= 2 && item.length <= 10)
    .filter((item) => {
      if (seen.has(item)) return false;
      seen.add(item);
      return true;
    })
    .slice(0, limit);
}

function normalizeGroupItems(items) {
  if (!Array.isArray(items) || !items.length) {
    return [
      { title: "列标题一", text: "这里写第一块内容。" },
      { title: "列标题二", text: "这里写第二块内容。" },
      { title: "列标题三", text: "这里写第三块内容。" },
    ];
  }
  return items.map((item, index) => ({
    title: String(item?.title || `卡片 ${index + 1}`),
    text: String(item?.text || ""),
  }));
}

function cloneArticle(article) {
  return JSON.parse(JSON.stringify(article || { title: "", blocks: [] }));
}

function snapshotEditorState() {
  return {
    title: state.title,
    sourceUrl: state.sourceUrl,
    outputDir: state.outputDir,
    article: cloneArticle(state.article),
    focusedBlockIndex: state.focusedBlockIndex,
  };
}

function updateUndoButton() {
  ui.undoBtn.disabled = state.history.length === 0;
}

function pushHistory(label = "") {
  state.history.push({
    label,
    snapshot: snapshotEditorState(),
  });
  if (state.history.length > 80) {
    state.history.shift();
  }
  updateUndoButton();
}

function restoreSnapshot(snapshot) {
  state.title = snapshot.title || "";
  state.sourceUrl = snapshot.sourceUrl || "";
  state.outputDir = snapshot.outputDir || "";
  state.article = hydrateArticle(snapshot.title, snapshot.article || { title: snapshot.title, blocks: [] });
  state.selectedBlocks.clear();
  state.focusedBlockIndex = Number.isInteger(snapshot.focusedBlockIndex) ? snapshot.focusedBlockIndex : null;
  state.lastRenderPayload = null;
  refreshAll();
}

function undoLastChange() {
  const entry = state.history.pop();
  if (!entry) {
    setStatus("已经没有可撤销的了。", "error");
    return;
  }
  restoreSnapshot(entry.snapshot);
  updateUndoButton();
  setStatus(entry.label ? `已撤销：${entry.label}` : "已撤销上一步");
}

function createBlock(type = "text") {
  if (type === "hero") {
    return {
      type,
      title: state.title || "今天这篇想聊什么",
      category: "观点类",
      theme: "主题导读",
      summary: "这里写这一篇最前面的简短主题说明，让读者一眼知道今天在聊什么。",
      keywords: ["主题", "关键词", "视觉感"],
      image_src: "",
      image_alt: "今日主题视觉",
    };
  }
  if (type === "video") {
    return {
      type,
      title: "今天的视频",
      summary: "",
      note: "",
      link: "",
      cover_src: "",
      cover_alt: "视频封面",
    };
  }
  if (type === "heading") return { type, text: "新小标题" };
  if (type === "subheading") return { type, text: "这一节的小标题" };
  if (type === "quote") return { type, text: "这一句可以做成引言块。" };
  if (type === "highlight") return { type, text: "这一句值得被单独放大，做成文章里的金句。" };
  if (type === "prompt") return { type, label: "这段提示词", text: "把你的长提示词贴在这里。" };
  if (type === "image") return { type, src: "", alt: "文章配图", width: 1200, height: 800 };
  if (type === "meta") return { type, text: "2026年4月3日" };
  if (type === "list") return { type, style: "unordered", items: ["第一点", "第二点", "第三点"] };
  if (type === "group") {
    return {
      type,
      layout: "horizontal",
      items: normalizeGroupItems(),
    };
  }
  return { type: "text", text: "这里写正文。" };
}

function blockToPlainText(block) {
  if (!block) return "";
  if (block.type === "hero") return [block.title, block.summary, ...(block.keywords || [])].filter(Boolean).join("\n");
  if (block.type === "video") return [block.title, block.summary, block.note, block.link].filter(Boolean).join("\n");
  if (["text", "heading", "subheading", "quote", "highlight", "meta"].includes(block.type)) return String(block.text || "");
  if (block.type === "prompt") return String(block.text || "");
  if (block.type === "list") return normalizeListItems(block.items).join("\n");
  if (block.type === "group") {
    return normalizeGroupItems(block.items)
      .map((item) => [item.title, item.text].filter(Boolean).join("："))
      .join("\n");
  }
  return "";
}

function normalizeBlock(block) {
  const type = block?.type || "text";
  if (type === "hero") {
    return {
      type,
      title: block.title || "",
      category: block.category || "观点类",
      theme: block.theme || "",
      summary: block.summary || "",
      keywords: normalizeKeywords(block.keywords),
      image_src: block.image_src || "",
      image_alt: block.image_alt || "今日主题视觉",
    };
  }
  if (type === "video") {
    return {
      type,
      title: block.title || "",
      summary: block.summary || "",
      note: block.note || "",
      link: block.link || "",
      cover_src: block.cover_src || "",
      cover_alt: block.cover_alt || "视频封面",
    };
  }
  if (type === "prompt") {
    return {
      type,
      label: block.label || "这段提示词",
      text: block.text || "",
    };
  }
  if (type === "image") {
    return {
      type,
      src: block.src || "",
      alt: block.alt || "文章配图",
      width: Number(block.width || 0),
      height: Number(block.height || 0),
    };
  }
  if (type === "list") {
    return {
      type,
      style: block.style || "unordered",
      items: normalizeListItems(block.items),
    };
  }
  if (type === "group") {
    return {
      type,
      layout: block.layout || "horizontal",
      items: normalizeGroupItems(block.items),
    };
  }
  return {
    type,
    text: block.text || "",
  };
}

function hydrateArticle(title, article) {
  return {
    title: title || article?.title || "",
    blocks: Array.isArray(article?.blocks) ? article.blocks.map(normalizeBlock) : [],
  };
}

function blockTypeLabel(type) {
  return {
    hero: "导读头图",
    video: "视频块",
    text: "正文",
    heading: "小标题",
    subheading: "二级标题",
    quote: "引言",
    highlight: "金句",
    prompt: "提示词块",
    image: "图片",
    meta: "信息行",
    list: "分点块",
    group: "卡片组",
  }[type] || type;
}

function setStatus(message, tone = "idle") {
  ui.statusPill.textContent = message;
  ui.statusPill.style.background = tone === "error" ? "rgba(180, 35, 24, 0.12)" : "rgba(141, 91, 45, 0.12)";
  ui.statusPill.style.color = tone === "error" ? "#b42318" : "#8d5b2d";
}

function updateStats() {
  const blocks = state.article.blocks;
  const counts = {
    总块数: blocks.length,
    导读: blocks.filter((block) => block.type === "hero").length,
    标题: blocks.filter((block) => block.type === "heading").length,
    二级标题: blocks.filter((block) => block.type === "subheading").length,
    图片: blocks.filter((block) => block.type === "image").length,
    视频: blocks.filter((block) => block.type === "video").length,
    提示词: blocks.filter((block) => block.type === "prompt").length,
    结构块: blocks.filter((block) => ["list", "group"].includes(block.type)).length,
  };
  ui.stats.innerHTML = Object.entries(counts).map(([key, value]) => `<span>${key} ${value}</span>`).join("");
}

function updateSelectionMeta() {
  const count = state.selectedBlocks.size;
  const targetLabel = mergeKindLabel(ui.mergeKindSelect?.value || "text");
  ui.selectionMeta.textContent = count ? `已选 ${count} 个块，准备合成成 ${targetLabel}。` : "还没选中块";
  ui.mergeKindSelect.disabled = count === 0;
  ui.mergeSelectedBtn.disabled = count === 0;
  ui.clearSelectionBtn.disabled = count === 0;
}

function syncTopFields() {
  ui.sourceUrl.value = state.sourceUrl;
  ui.titleInput.value = state.title;
  ui.outputDir.value = state.outputDir;
  ui.saveMeta.textContent = state.lastSaved
    ? `最近一次已保存到：${state.lastSaved.output_dir}`
    : "保存后会生成 article.json、preview.html、copy.html。";
  if (state.lastSaved?.copy_url) {
    ui.copyLink.href = state.lastSaved.copy_url;
    ui.copyLink.classList.remove("disabled");
  } else {
    ui.copyLink.href = "#";
    ui.copyLink.classList.add("disabled");
  }
}

function typeSelectMarkup(currentType) {
  const types = ["hero", "text", "heading", "subheading", "quote", "highlight", "prompt", "video", "image", "meta", "list", "group"];
  return `
    <select data-field="type">
      ${types.map((type) => `<option value="${type}" ${currentType === type ? "selected" : ""}>${blockTypeLabel(type)}</option>`).join("")}
    </select>
  `;
}

function imageBodyMarkup(block) {
  const hasSrc = Boolean(block.src);
  const isEmbedded = hasSrc && block.src.startsWith("data:");
  return `
    ${hasSrc ? `<img class="image-preview" src="${escapeHtml(block.src)}" alt="${escapeHtml(block.alt || "文章配图")}" />` : ""}
    ${isEmbedded ? '<p class="image-note">当前是内嵌图源，保留原图数据，不在这里展开整段 data URL。</p>' : ""}
    ${!isEmbedded ? `
      <label class="field">
        <span>图片地址</span>
        <textarea data-field="src" placeholder="https://... 或 data:image/...">${escapeHtml(block.src || "")}</textarea>
      </label>
    ` : ""}
    <label class="field">
      <span>图片描述</span>
      <input data-field="alt" type="text" value="${escapeHtml(block.alt || "")}" placeholder="文章配图" />
    </label>
    <div class="row">
      <label class="field grow">
        <span>宽度</span>
        <input data-field="width" type="number" value="${block.width || 0}" />
      </label>
      <label class="field grow">
        <span>高度</span>
        <input data-field="height" type="number" value="${block.height || 0}" />
      </label>
    </div>
  `;
}

function heroBodyMarkup(block) {
  const hasSrc = Boolean(block.image_src);
  return `
    ${hasSrc ? `<img class="image-preview" src="${escapeHtml(block.image_src)}" alt="${escapeHtml(block.image_alt || "今日主题视觉")}" />` : '<div class="soft-preview">右边可以放今日主题对应的 IP 变体图或视觉参考图。</div>'}
    <div class="row">
      <label class="field grow">
        <span>头图标题</span>
        <input data-field="title" type="text" value="${escapeHtml(block.title || "")}" />
      </label>
      <label class="field grow">
        <span>内容类型</span>
        <input data-field="category" type="text" value="${escapeHtml(block.category || "")}" placeholder="视频类 / 图片类 / 提示词类 / 观点类" />
      </label>
    </div>
    <div class="row">
      <label class="field grow">
        <span>主题标签</span>
        <input data-field="theme" type="text" value="${escapeHtml(block.theme || "")}" placeholder="陪伴感 / 关系观察 / 方法拆解" />
      </label>
      <label class="field grow">
        <span>关键词</span>
        <input data-field="keywordsText" type="text" value="${escapeHtml((block.keywords || []).join(" / "))}" placeholder="每个关键词用 / 隔开" />
      </label>
    </div>
    <label class="field">
      <span>简短导读</span>
      <textarea data-field="summary" placeholder="这里写今天这篇的简短主题逻辑。">${escapeHtml(block.summary || "")}</textarea>
    </label>
    <label class="field">
      <span>右侧视觉图地址</span>
      <textarea data-field="image_src" placeholder="https://... 或 data:image/...">${escapeHtml(block.image_src || "")}</textarea>
    </label>
    <label class="field">
      <span>视觉图说明</span>
      <input data-field="image_alt" type="text" value="${escapeHtml(block.image_alt || "")}" placeholder="今日主题视觉" />
    </label>
  `;
}

function videoBodyMarkup(block) {
  const hasSrc = Boolean(block.cover_src);
  return `
    ${hasSrc ? `<img class="image-preview" src="${escapeHtml(block.cover_src)}" alt="${escapeHtml(block.cover_alt || "视频封面")}" />` : '<div class="soft-preview">视频区域预览</div>'}
    <label class="field">
      <span>视频标题</span>
      <input data-field="title" type="text" value="${escapeHtml(block.title || "")}" />
    </label>
    <label class="field">
      <span>视频说明</span>
      <textarea data-field="summary" placeholder="这里写视频要表达的内容。">${escapeHtml(block.summary || "")}</textarea>
    </label>
    <label class="field">
      <span>报编信息</span>
      <input data-field="note" type="text" value="${escapeHtml(block.note || "")}" placeholder="例如：视频号同步 / 已在后台导入" />
    </label>
    <label class="field">
      <span>视频链接或备注</span>
      <input data-field="link" type="text" value="${escapeHtml(block.link || "")}" placeholder="https://... 或写一句补充说明" />
    </label>
    <label class="field">
      <span>封面图地址</span>
      <textarea data-field="cover_src" placeholder="https://... 或 data:image/...">${escapeHtml(block.cover_src || "")}</textarea>
    </label>
    <label class="field">
      <span>封面图说明</span>
      <input data-field="cover_alt" type="text" value="${escapeHtml(block.cover_alt || "")}" placeholder="视频封面" />
    </label>
  `;
}

function listBodyMarkup(block) {
  return `
    <label class="field">
      <span>分点样式</span>
      <select data-field="style">
        <option value="unordered" ${block.style === "unordered" ? "selected" : ""}>圆点</option>
        <option value="ordered" ${block.style === "ordered" ? "selected" : ""}>编号</option>
      </select>
    </label>
    <label class="field">
      <span>每行一个分点</span>
      <textarea data-field="itemsText" placeholder="每行写一个分点。">${escapeHtml((block.items || []).join("\n"))}</textarea>
    </label>
  `;
}

function groupItemMarkup(item, itemIndex) {
  return `
    <div class="item-card">
      <div class="item-head">
        <span>卡片 ${itemIndex + 1}</span>
        <button data-action="remove-item" data-item-index="${itemIndex}" class="item-remove">删掉这项</button>
      </div>
      <label class="field">
        <span>列标题</span>
        <input data-field="groupTitle" data-item-index="${itemIndex}" type="text" value="${escapeHtml(item.title || "")}" />
      </label>
      <label class="field">
        <span>正文</span>
        <textarea data-field="groupText" data-item-index="${itemIndex}" placeholder="这里写这一列的正文。">${escapeHtml(item.text || "")}</textarea>
      </label>
    </div>
  `;
}

function groupBodyMarkup(block) {
  return `
    <div class="row">
      <label class="field grow">
        <span>排列方式</span>
        <select data-field="layout">
          <option value="horizontal" ${block.layout === "horizontal" ? "selected" : ""}>横向三栏</option>
          <option value="vertical" ${block.layout === "vertical" ? "selected" : ""}>纵向堆叠</option>
        </select>
      </label>
      <button data-action="add-item" class="secondary">新增一项</button>
    </div>
    <div>${normalizeGroupItems(block.items).map(groupItemMarkup).join("")}</div>
  `;
}

function blockBodyMarkup(block) {
  if (block.type === "hero") return heroBodyMarkup(block);
  if (block.type === "video") return videoBodyMarkup(block);
  if (block.type === "prompt") {
    return `
      <label class="field">
        <span>卡片标题</span>
        <input data-field="label" type="text" value="${escapeHtml(block.label || "")}" />
      </label>
      <label class="field">
        <span>提示词内容</span>
        <textarea data-field="text" placeholder="把超长提示词贴在这里。">${escapeHtml(block.text || "")}</textarea>
      </label>
    `;
  }
  if (block.type === "image") return imageBodyMarkup(block);
  if (block.type === "list") return listBodyMarkup(block);
  if (block.type === "group") return groupBodyMarkup(block);
  return `
    <label class="field">
      <span>${block.type === "heading" ? "标题内容" : "内容"}</span>
      <textarea data-field="text" placeholder="在这里直接改文本。">${escapeHtml(block.text || "")}</textarea>
    </label>
  `;
}

function blockCardMarkup(block, index) {
  const selected = state.selectedBlocks.has(index);
  const focused = state.focusedBlockIndex === index;
  return `
    <article class="block-card ${selected ? "is-selected" : ""} ${focused ? "is-focused" : ""}" data-index="${index}">
      <div class="block-head">
        <div class="block-head-left">
          <input class="block-check" data-action="toggle-select" type="checkbox" ${selected ? "checked" : ""} />
          <span class="block-index">${index + 1}</span>
          ${typeSelectMarkup(block.type)}
        </div>
        <div class="block-actions">
          <button data-action="up">上移</button>
          <button data-action="down">下移</button>
          <button data-action="duplicate">复制</button>
          <button data-action="remove">删除</button>
        </div>
      </div>
      ${blockBodyMarkup(block)}
    </article>
  `;
}

function renderBlocks() {
  if (!state.article.blocks.length) {
    ui.blockList.innerHTML = "";
    ui.blockList.append(ui.emptyTemplate.content.cloneNode(true));
    updateSelectionMeta();
    return;
  }
  ui.blockList.innerHTML = state.article.blocks.map(blockCardMarkup).join("");
  updateSelectionMeta();
}

async function requestJSON(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok || payload.ok === false) {
    throw new Error(payload.error || "请求失败");
  }
  return payload;
}

function scheduleRender() {
  clearTimeout(state.renderTimer);
  ui.renderStatus.textContent = "正在刷新预览…";
  state.renderTimer = setTimeout(renderPreview, 220);
}

function focusPreviewBlock(index) {
  const frameWindow = ui.previewFrame.contentWindow;
  if (!frameWindow) return;
  try {
    if (typeof frameWindow.focusBlock === "function") {
      frameWindow.focusBlock(index);
    }
    frameWindow.postMessage({ source: "svg-wechat-editor", blockIndex: index }, "*");
  } catch (error) {
    console.debug("focusPreviewBlock failed", error);
  }
}

async function renderPreview() {
  try {
    const payload = await requestJSON("/api/render", {
      method: "POST",
      body: JSON.stringify({
        title: state.title || "未命名文章",
        article: state.article,
        interactive_preview: true,
      }),
    });
    state.lastRenderPayload = payload;
    ui.previewFrame.srcdoc = payload.preview_html;
    ui.renderStatus.textContent = "预览已同步。";
  } catch (error) {
    ui.renderStatus.textContent = `预览失败：${error.message}`;
  }
}

function refreshAll() {
  syncTopFields();
  updateStats();
  renderBlocks();
  updateUndoButton();
  scheduleRender();
}

function setDocument(payload) {
  state.docId = payload.doc_id || "";
  state.title = payload.title || payload.article?.title || "";
  state.sourceUrl = payload.source_url || "";
  state.outputDir = payload.output_dir || "";
  state.article = hydrateArticle(state.title, payload.article || { title: state.title, blocks: [] });
  state.lastSaved = null;
  state.lastRenderPayload = null;
  state.selectedBlocks.clear();
  state.focusedBlockIndex = null;
  state.history = [];
  if (payload.article_json) ui.articlePath.value = payload.article_json;
  setStatus("已载入", "idle");
  refreshAll();
}

async function importFeishu() {
  const url = ui.sourceUrl.value.trim();
  if (!url) {
    setStatus("先填飞书链接", "error");
    return;
  }
  const originalLabel = ui.importBtn.textContent;
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), 180000);
  ui.importBtn.disabled = true;
  ui.importBtn.textContent = "导入中…";
  setStatus("导入中…");
  try {
    const payload = await requestJSON("/api/import-feishu", {
      method: "POST",
      body: JSON.stringify({
        url,
        output_dir: ui.outputDir.value.trim(),
      }),
      signal: controller.signal,
    });
    setDocument(payload);
  } catch (error) {
    if (error.name === "AbortError") {
      setStatus("导入超时了，通常是飞书图片抓取卡住了，重试一次看看。", "error");
    } else {
      setStatus(error.message, "error");
    }
  } finally {
    window.clearTimeout(timeoutId);
    ui.importBtn.disabled = false;
    ui.importBtn.textContent = originalLabel;
  }
}

async function loadArticleFile() {
  const rawPath = ui.articlePath.value.trim();
  if (!rawPath) {
    setStatus("先填 article.json 路径", "error");
    return;
  }
  setStatus("载入中…");
  try {
    const payload = await requestJSON(`/api/load?path=${encodeURIComponent(rawPath)}`);
    setDocument(payload);
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function saveDocument() {
  setStatus("保存中…");
  try {
    const payload = await requestJSON("/api/save", {
      method: "POST",
      body: JSON.stringify({
        title: state.title || "未命名文章",
        source_url: state.sourceUrl,
        output_dir: ui.outputDir.value.trim(),
        article: state.article,
      }),
    });
    state.outputDir = payload.output_dir;
    state.lastSaved = payload;
    setStatus("已保存");
    syncTopFields();
  } catch (error) {
    setStatus(error.message, "error");
  }
}

async function autoLayoutDraft() {
  ui.autoLayoutBtn.disabled = true;
  const originalLabel = ui.autoLayoutBtn.textContent;
  ui.autoLayoutBtn.textContent = "整理中…";
  setStatus("正在帮你做第一版智能排版…");
  try {
    const payload = await requestJSON("/api/auto-layout", {
      method: "POST",
      body: JSON.stringify({
        title: state.title || "未命名文章",
        article: state.article,
      }),
    });
    pushHistory("智能初稿");
    state.article = hydrateArticle(state.title, payload.article);
    state.selectedBlocks.clear();
    state.focusedBlockIndex = null;
    refreshAll();
    setStatus("已经生成一版智能初稿了，不满意随时撤销。");
  } catch (error) {
    setStatus(`智能初稿失败：${error.message}`, "error");
  } finally {
    ui.autoLayoutBtn.disabled = false;
    ui.autoLayoutBtn.textContent = originalLabel;
  }
}

function copyViaSelection(html) {
  const container = document.createElement("div");
  container.contentEditable = "true";
  container.style.position = "fixed";
  container.style.left = "-99999px";
  container.style.top = "0";
  container.style.opacity = "0";
  container.innerHTML = html;
  document.body.appendChild(container);

  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(container);
  selection.removeAllRanges();
  selection.addRange(range);
  const ok = document.execCommand("copy");
  selection.removeAllRanges();
  document.body.removeChild(container);
  if (!ok) throw new Error("浏览器没有完成复制");
}

async function copyCurrentPreview() {
  const originalLabel = ui.copyPreviewBtn.textContent;
  ui.copyPreviewBtn.disabled = true;
  ui.copyPreviewBtn.textContent = "复制中…";
  setStatus("正在复制当前预览…");
  try {
    const payload = await requestJSON("/api/render", {
      method: "POST",
      body: JSON.stringify({
        title: state.title || "未命名文章",
        article: state.article,
        resolve_assets: true,
        interactive_preview: false,
        copy_prompt_hint: false,
      }),
    });
    copyViaSelection(payload.article_markup);
    setStatus("当前预览已经复制好了，直接去公众号后台粘贴。");
  } catch (error) {
    setStatus(`复制失败：${error.message}`, "error");
  } finally {
    ui.copyPreviewBtn.disabled = false;
    ui.copyPreviewBtn.textContent = originalLabel;
  }
}

function addBlock(type) {
  pushHistory("新增内容块");
  state.article.blocks.push(createBlock(type));
  state.selectedBlocks.clear();
  refreshAll();
  focusEditorBlock(state.article.blocks.length - 1, { scroll: true, syncPreview: true });
}

function buildConvertedBlock(nextType, sourceBlock) {
  const plainText = blockToPlainText(sourceBlock).trim() || "这里补一段内容。";
  if (nextType === "hero") {
    return {
      type: "hero",
      title: state.title || (["heading", "subheading"].includes(sourceBlock?.type) ? plainText : "今天这篇想聊什么"),
      category: "观点类",
      theme: extractKeywordDrafts(plainText, 1)[0] || "主题导读",
      summary: plainText,
      keywords: extractKeywordDrafts(plainText, 4),
      image_src: "",
      image_alt: "今日主题视觉",
    };
  }
  if (nextType === "video") {
    return {
      type: "video",
      title: ["heading", "subheading"].includes(sourceBlock?.type) ? plainText : "今天的视频",
      summary: ["heading", "subheading"].includes(sourceBlock?.type) ? "这里补一段视频说明。" : plainText,
      note: "",
      link: "",
      cover_src: "",
      cover_alt: "视频封面",
    };
  }
  if (nextType === "prompt") {
    return {
      type: "prompt",
      label: ["heading", "subheading"].includes(sourceBlock?.type) ? plainText : "这段提示词",
      text: plainText,
    };
  }
  if (nextType === "subheading") {
    return {
      type: "subheading",
      text: plainText,
    };
  }
  if (nextType === "highlight") {
    return {
      type: "highlight",
      text: plainText,
    };
  }
  if (nextType === "list") {
    return {
      type: "list",
      style: "unordered",
      items: plainText.split(/\n+/).map((item) => item.trim()).filter(Boolean),
    };
  }
  if (nextType === "group") {
    return {
      type: "group",
      layout: "horizontal",
      items: [
        { title: ["heading", "subheading"].includes(sourceBlock?.type) ? plainText : "列标题一", text: ["heading", "subheading"].includes(sourceBlock?.type) ? "" : plainText },
        { title: "列标题二", text: "这里写第二块内容。" },
        { title: "列标题三", text: "这里写第三块内容。" },
      ],
    };
  }
  const next = createBlock(nextType);
  if ("text" in next) next.text = plainText;
  return next;
}

function mergedBlockText(blocks, separator = "\n\n") {
  return blocks
    .map((block) => blockToPlainText(block).trim())
    .filter(Boolean)
    .join(separator)
    .trim();
}

function mergedInlineText(blocks) {
  return mergedBlockText(blocks, "\n")
    .replace(/\s*\n+\s*/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function updateBlock(index, field, value, { rerender = false, itemIndex = null } = {}) {
  const block = state.article.blocks[index];
  if (!block) return;

  if (field === "type") {
    pushHistory("修改块类型");
    state.article.blocks[index] = buildConvertedBlock(value, block);
    refreshAll();
    focusEditorBlock(index, { scroll: false, syncPreview: true });
    return;
  }

  if (field === "width" || field === "height") {
    block[field] = Number(value || 0);
  } else if (field === "keywordsText") {
    block.keywords = normalizeKeywords(String(value || "").split(/[\\/｜|]+/).map((item) => item.trim()));
  } else if (field === "itemsText") {
    block.items = value.split(/\n+/).map((item) => item.trim()).filter(Boolean);
  } else if (field === "style" || field === "layout") {
    block[field] = value;
  } else if (field === "groupTitle" || field === "groupText") {
    const item = block.items?.[itemIndex];
    if (!item) return;
    item[field === "groupTitle" ? "title" : "text"] = value;
  } else {
    block[field] = value;
  }

  if (rerender || field === "type" || field === "layout" || field === "style" || field === "itemsText" || field === "keywordsText") {
    refreshAll();
    focusEditorBlock(index, { scroll: false, syncPreview: true });
    return;
  }
  scheduleRender();
}

function clearSelection({ rerender = true } = {}) {
  state.selectedBlocks.clear();
  if (rerender) {
    renderBlocks();
  } else {
    updateSelectionMeta();
  }
}

function moveBlock(index, delta) {
  const target = index + delta;
  if (target < 0 || target >= state.article.blocks.length) return;
  pushHistory("移动内容块");
  const [block] = state.article.blocks.splice(index, 1);
  state.article.blocks.splice(target, 0, block);
  clearSelection({ rerender: false });
  refreshAll();
  focusEditorBlock(target, { scroll: true, syncPreview: true });
}

function duplicateBlock(index) {
  const block = state.article.blocks[index];
  if (!block) return;
  pushHistory("复制内容块");
  state.article.blocks.splice(index + 1, 0, JSON.parse(JSON.stringify(block)));
  clearSelection({ rerender: false });
  refreshAll();
  focusEditorBlock(index + 1, { scroll: true, syncPreview: true });
}

function removeBlock(index) {
  pushHistory("删除内容块");
  state.article.blocks.splice(index, 1);
  clearSelection({ rerender: false });
  if (state.focusedBlockIndex === index) state.focusedBlockIndex = null;
  refreshAll();
}

function addGroupItem(index) {
  const block = state.article.blocks[index];
  if (!block || block.type !== "group") return;
  pushHistory("新增卡片项");
  block.items.push({ title: `卡片 ${block.items.length + 1}`, text: "" });
  refreshAll();
  focusEditorBlock(index, { scroll: false, syncPreview: true });
}

function removeGroupItem(index, itemIndex) {
  const block = state.article.blocks[index];
  if (!block || block.type !== "group") return;
  if (block.items.length <= 1) {
    setStatus("至少保留一项卡片。", "error");
    return;
  }
  pushHistory("删除卡片项");
  block.items.splice(itemIndex, 1);
  refreshAll();
  focusEditorBlock(index, { scroll: false, syncPreview: true });
}

function extractItemsFromBlocks(blocks) {
  const items = [];
  for (const block of blocks) {
    if (!block) continue;
    if (block.type === "group") {
      items.push(...normalizeGroupItems(block.items));
      continue;
    }
    if (block.type === "list") {
      items.push(...normalizeListItems(block.items).map((text, index) => ({ title: `分点 ${index + 1}`, text })));
      continue;
    }
    if (block.type === "heading" || block.type === "subheading") {
      items.push({ title: block.text || "", text: "" });
      continue;
    }
    const text = blockToPlainText(block).trim();
    if (!text) continue;
    if (items.length && !items[items.length - 1].text) {
      items[items.length - 1].text = text;
    } else {
      items.push({ title: "", text });
    }
  }
  return items.filter((item) => item.title || item.text);
}

function mergeSelected(kind) {
  const indices = selectedIndices();
  if (!indices.length) {
    setStatus("先选几个块再合并。", "error");
    return;
  }

  const blocks = indices.map((index) => state.article.blocks[index]);
  let mergedBlock = null;

  if (kind === "text") {
    mergedBlock = buildConvertedBlock("text", { type: "text", text: mergedBlockText(blocks, "\n\n") });
  }

  if (kind === "prompt") {
    const mergedText = mergedBlockText(blocks, "\n");
    const firstLine = mergedText.split(/\n+/).find(Boolean) || "这段提示词";
    mergedBlock = {
      type: "prompt",
      label: firstLine.length <= 18 ? firstLine : "这段提示词",
      text: mergedText,
    };
  }

  if (kind === "hero") {
    const mergedText = mergedBlockText(blocks, "\n\n");
    mergedBlock = {
      type: "hero",
      title: state.title || "今天这篇想聊什么",
      category: "观点类",
      theme: extractKeywordDrafts(mergedText, 1)[0] || "主题导读",
      summary: mergedText,
      keywords: extractKeywordDrafts(mergedText, 5),
      image_src: "",
      image_alt: "今日主题视觉",
    };
  }

  if (kind === "video") {
    const mergedText = mergedBlockText(blocks, "\n\n");
    mergedBlock = {
      type: "video",
      title: extractKeywordDrafts(mergedInlineText(blocks), 1)[0] || "今天的视频",
      summary: mergedText,
      note: "",
      link: "",
      cover_src: "",
      cover_alt: "视频封面",
    };
  }

  if (kind === "list") {
    mergedBlock = {
      type: "list",
      style: "unordered",
      items: blocks
        .flatMap((block) => {
          if (block.type === "list") return normalizeListItems(block.items);
          return blockToPlainText(block).split(/\n+/).map((item) => item.trim()).filter(Boolean);
        }),
    };
  }

  if (["heading", "subheading", "quote", "highlight", "meta"].includes(kind)) {
    const mergedText = ["heading", "subheading", "meta"].includes(kind)
      ? mergedInlineText(blocks)
      : mergedBlockText(blocks, "\n\n");
    mergedBlock = buildConvertedBlock(kind, { type: "text", text: mergedText });
  }

  if (kind === "group-horizontal" || kind === "group-vertical") {
    mergedBlock = {
      type: "group",
      layout: kind === "group-horizontal" ? "horizontal" : "vertical",
      items: extractItemsFromBlocks(blocks),
    };
  }

  if (!mergedBlock) return;

  pushHistory("合并选中块");
  const firstIndex = indices[0];
  const nextBlocks = state.article.blocks.filter((_, index) => !state.selectedBlocks.has(index));
  nextBlocks.splice(firstIndex, 0, normalizeBlock(mergedBlock));
  state.article.blocks = nextBlocks;
  state.selectedBlocks.clear();
  refreshAll();
  focusEditorBlock(firstIndex, { scroll: true, syncPreview: true });
  setStatus(`已经帮你打包成 ${mergeKindLabel(kind)} 了。`);
}

function toggleSelectBlock(index, checked) {
  if (checked) {
    state.selectedBlocks.add(index);
  } else {
    state.selectedBlocks.delete(index);
  }
  renderBlocks();
}

function focusEditorBlock(index, { scroll = true, syncPreview = false } = {}) {
  state.focusedBlockIndex = index;
  renderBlocks();
  const card = ui.blockList.querySelector(`.block-card[data-index="${index}"]`);
  if (card && scroll) {
    card.scrollIntoView({ block: "center", behavior: "smooth" });
  }
  if (syncPreview) {
    focusPreviewBlock(index);
  }
}

function bindEvents() {
  ui.importBtn.addEventListener("click", importFeishu);
  ui.loadBtn.addEventListener("click", loadArticleFile);
  ui.saveBtn.addEventListener("click", saveDocument);
  ui.undoBtn.addEventListener("click", undoLastChange);
  ui.autoLayoutBtn.addEventListener("click", autoLayoutDraft);
  ui.copyPreviewBtn.addEventListener("click", copyCurrentPreview);
  ui.mergeSelectedBtn.addEventListener("click", () => mergeSelected(ui.mergeKindSelect.value));
  ui.clearSelectionBtn.addEventListener("click", () => clearSelection());
  ui.mergeKindSelect.addEventListener("change", updateSelectionMeta);

  ui.titleInput.addEventListener("input", (event) => {
    state.title = event.target.value;
    state.article.title = state.title;
    scheduleRender();
  });

  ui.sourceUrl.addEventListener("input", (event) => {
    state.sourceUrl = event.target.value;
  });

  ui.outputDir.addEventListener("input", (event) => {
    state.outputDir = event.target.value;
  });

  document.querySelector(".block-toolbar").addEventListener("click", (event) => {
    const button = event.target.closest("[data-add]");
    if (!button) return;
    addBlock(button.dataset.add);
  });

  ui.blockList.addEventListener("input", (event) => {
    const field = event.target.dataset.field;
    const card = event.target.closest(".block-card");
    if (!field || !card) return;
    updateBlock(Number(card.dataset.index), field, event.target.value, {
      rerender: ["src", "image_src", "cover_src", "itemsText", "keywordsText"].includes(field),
      itemIndex: event.target.dataset.itemIndex ? Number(event.target.dataset.itemIndex) : null,
    });
  });

  ui.blockList.addEventListener("change", (event) => {
    const card = event.target.closest(".block-card");
    if (!card) return;
    if (event.target.matches(".block-check")) {
      toggleSelectBlock(Number(card.dataset.index), event.target.checked);
      return;
    }
    const field = event.target.dataset.field;
    if (!field) return;
    updateBlock(Number(card.dataset.index), field, event.target.value, {
      rerender: field === "type" || field === "src" || field === "layout" || field === "style",
      itemIndex: event.target.dataset.itemIndex ? Number(event.target.dataset.itemIndex) : null,
    });
  });

  ui.blockList.addEventListener("click", (event) => {
    const card = event.target.closest(".block-card");
    if (!card) return;
    const index = Number(card.dataset.index);

    const action = event.target.dataset.action;
    if (action === "up") return moveBlock(index, -1);
    if (action === "down") return moveBlock(index, 1);
    if (action === "duplicate") return duplicateBlock(index);
    if (action === "remove") return removeBlock(index);
    if (action === "add-item") return addGroupItem(index);
    if (action === "remove-item") return removeGroupItem(index, Number(event.target.dataset.itemIndex));
    if (action === "toggle-select") return;

    if (!event.target.closest("input,textarea,select,button")) {
      focusEditorBlock(index, { scroll: true, syncPreview: true });
    }
  });

  ui.blockList.addEventListener("contextmenu", (event) => {
    const card = event.target.closest(".block-card");
    if (!card || event.target.closest("input,textarea,select,button")) return;
    event.preventDefault();
    const index = Number(card.dataset.index);
    const nextChecked = !state.selectedBlocks.has(index);
    toggleSelectBlock(index, nextChecked);
    focusEditorBlock(index, { scroll: true, syncPreview: true });
    setStatus(nextChecked ? "这个块已经加入选择了。" : "这个块已经从选择里拿出来了。");
  });

  ui.previewFrame.addEventListener("load", () => {
    if (state.focusedBlockIndex !== null) {
      focusPreviewBlock(state.focusedBlockIndex);
    }
  });

  window.addEventListener("message", (event) => {
    if (event.data?.source !== "svg-wechat-preview") return;
    if (typeof event.data.blockIndex !== "number") return;
    focusEditorBlock(event.data.blockIndex, { scroll: true, syncPreview: false });
  });

  window.addEventListener("keydown", (event) => {
    const target = event.target;
    const isTypingTarget = target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement || target instanceof HTMLSelectElement;
    if (isTypingTarget) return;
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "z") {
      event.preventDefault();
      undoLastChange();
    }
  });
}

async function boot() {
  bindEvents();
  const query = new URLSearchParams(window.location.search);
  const docId = query.get("doc_id");
  if (docId) {
    try {
      const payload = await requestJSON(`/api/load?doc_id=${encodeURIComponent(docId)}`);
      setDocument(payload);
      return;
    } catch (error) {
      setStatus(error.message, "error");
    }
  }
  const articleJson = query.get("article_json");
  if (articleJson) {
    ui.articlePath.value = articleJson;
    await loadArticleFile();
    return;
  }
  state.title = "未命名文章";
  state.article = hydrateArticle(state.title, { title: state.title, blocks: [createBlock("heading"), createBlock("text")] });
  refreshAll();
}

boot();
