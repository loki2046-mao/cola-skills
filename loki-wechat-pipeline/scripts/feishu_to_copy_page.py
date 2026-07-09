#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import html
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import Page, sync_playwright


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = ROOT / "自研公众号排版"
DEFAULT_FOOTER = ROOT / "签名图.png"

PALETTE = {
    "ink": "#201a16",
    "text": "#4d443b",
    "muted": "#7c7065",
    "accent": "#8d5b2d",
    "accent_soft": "#f8efe4",
    "line": "#eadac8",
    "paper": "#fffdfa",
    "paper_deep": "#fbf5ee",
}

WARM_BORDER = "#ead8c2"
WARM_PANEL = "#fcf4ea"
WARM_PANEL_SOFT = "#fff8ef"
WARM_PILL = "#f1dfcb"
WARM_LINE = "#d6ab81"

EMPHASIS_HINTS = (
    "本质",
    "关键",
    "核心",
    "重点",
    "前提",
    "门槛",
    "麻烦",
    "适合",
    "不适合",
    "值不值得",
    "真正",
    "普通人",
    "新手",
)

EMPHASIS_STOPWORDS = {
    "这个",
    "那个",
    "这里",
    "然后",
    "其实",
    "就是",
    "要求",
    "目标",
    "问题",
    "页面主题",
    "输出要求",
    "视觉要求",
    "技术要求",
}

ROLE_PREFIXES = (
    "你现在是一位",
    "你是一位",
    "你是一名",
    "请帮我",
    "请你",
    "请直接",
    "请围绕",
    "请为我",
)

FIELD_MARKERS = {
    "技术要求：",
    "页面主题：",
    "目标气质：",
    "视觉要求：",
    "输出要求：",
    "代码质量要求：",
    "项目背景：",
    "输出结构：",
    "要求：",
}

RESUME_MARKERS = (
    "（此处有视频）",
    "我觉得颜色有点太AI",
    "这个方案的输出也有",
    "然后再看看大家都很关心的生图",
    "真正让我眼前一亮的",
    "想看全文的后台发",
    "直接看效果",
)

UI_NOISE = (
    "登录/注册",
    "最新修改时间",
    "与我分享",
    "飞书云文档",
    "赛博小熊猫",
)

INTRO_KEYWORD_STOPWORDS = {
    "",
    "今天",
    "这篇",
    "一个",
    "一些",
    "我们",
    "你们",
    "他们",
    "自己",
    "一下",
    "这种",
    "那个",
    "这个",
    "什么",
    "为什么",
    "怎么",
    "然后",
    "如果",
    "但是",
    "因为",
    "以及",
    "已经",
    "还是",
    "就是",
    "不是",
    "真的",
    "内容",
    "主题",
    "标题",
    "文章",
    "导读",
}


MARK_SCROLL_ROOT_JS = r"""
() => {
  const candidates = Array.from(document.querySelectorAll("*"))
    .map((el) => {
      const style = getComputedStyle(el);
      const overflowY = style.overflowY;
      const delta = el.scrollHeight - el.clientHeight;
      const rect = el.getBoundingClientRect();
      const score =
        Math.max(delta, 0) +
        (/(auto|scroll)/.test(overflowY) ? 400 : 0) +
        Math.max(rect.width - 400, 0);
      return { el, score, delta, width: rect.width };
    })
    .filter((item) => item.delta > 600 && item.width > 420)
    .sort((a, b) => b.score - a.score);

  const root = candidates[0]?.el || document.scrollingElement || document.body;
  root.setAttribute("data-codex-scroll-root", "1");
  return {
    scrollHeight: root.scrollHeight,
    clientHeight: root.clientHeight,
  };
}
"""


COLLECT_BLOCKS_JS = r"""
() => {
  const root = document.querySelector('[data-codex-scroll-root="1"]');
  const scrollTop = root ? root.scrollTop : window.scrollY;
  const anchorLeft = (document.querySelector("h1")?.getBoundingClientRect().left || 0) - 80;

  const isVisible = (el) => {
    const rect = el.getBoundingClientRect();
    if (rect.width < 32 || rect.height < 10) return false;
    if (rect.bottom < -220 || rect.top > window.innerHeight + 260) return false;
    if (rect.right < anchorLeft) return false;
    const style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity || "1") === 0) {
      return false;
    }
    return true;
  };

  const meaningfulChildText = (el) => {
    return Array.from(el.children).some((child) => {
      if (!isVisible(child)) return false;
      const text = (child.innerText || "").trim();
      if (!text) return false;
      const display = getComputedStyle(child).display;
      return !["inline", "inline-block", "contents"].includes(display);
    });
  };

  const classify = (el, text) => {
    const tag = el.tagName.toUpperCase();
    const style = getComputedStyle(el);
    const fontSize = parseFloat(style.fontSize || "0");
    const fontWeight = parseInt(style.fontWeight || "400", 10) || 400;
    if (tag === "H1") return "title";
    if (/^\d{1,2}月\d{1,2}日/.test(text)) return "meta";
    if (/^最新修改时间/.test(text)) return "meta";
    if (tag.startsWith("H")) return "heading";
    if (fontSize >= 23) return "heading";
    if (fontWeight >= 650 && text.length <= 26 && !/[。！？；，,.!?]$/.test(text)) return "heading";
    return "text";
  };

  const blocks = [];

  for (const img of document.querySelectorAll("img")) {
    if (!isVisible(img)) continue;
    const rect = img.getBoundingClientRect();
    const src = img.currentSrc || img.src || "";
    if (!src) continue;
    blocks.push({
      type: "image",
      src,
      alt: img.alt || "",
      width: img.naturalWidth || Math.round(rect.width),
      height: img.naturalHeight || Math.round(rect.height),
      top: Math.round(rect.top + scrollTop),
      left: Math.round(rect.left),
    });
  }

  for (const el of document.querySelectorAll("h1,h2,h3,h4,h5,h6,p,li,blockquote,pre,code,div,section,span")) {
    if (!isVisible(el)) continue;
    if (el.tagName.toUpperCase() === "IMG") continue;
    if (el.querySelector("img")) continue;
    if (meaningfulChildText(el)) continue;
    const text = (el.innerText || "").trim();
    if (!text) continue;
    const rect = el.getBoundingClientRect();
    const style = getComputedStyle(el);
    blocks.push({
      type: classify(el, text),
      text,
      top: Math.round(rect.top + scrollTop),
      left: Math.round(rect.left),
      fontSize: parseFloat(style.fontSize || "0") || 0,
      fontWeight: parseInt(style.fontWeight || "400", 10) || 400,
    });
  }

  blocks.sort((a, b) => (a.top - b.top) || (a.left - b.left));
  return {
    title: (document.querySelector("h1")?.innerText || document.title || "").trim(),
    blocks,
  };
}
"""


FETCH_IMAGE_JS = r"""
async ({ sources, timeoutMs }) => {
  const fetchOne = async (src) => {
    if (!src || src.startsWith("data:")) {
      return { src, ok: true, passthrough: true };
    }
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort("timeout"), timeoutMs);
    try {
      const response = await fetch(src, {
        credentials: "include",
        signal: controller.signal,
      });
      if (!response.ok) {
        return { src, ok: false, error: `http:${response.status}` };
      }
      const type = response.headers.get("content-type") || "image/png";
      const buffer = await response.arrayBuffer();
      const bytes = new Uint8Array(buffer);
      let binary = "";
      const step = 0x8000;
      for (let i = 0; i < bytes.length; i += step) {
        binary += String.fromCharCode(...bytes.slice(i, i + step));
      }
      return {
        src,
        ok: true,
        type,
        b64: btoa(binary),
      };
    } catch (error) {
      return { src, ok: false, error: String(error) };
    } finally {
      clearTimeout(timer);
    }
  };

  return Promise.all((sources || []).map(fetchOne));
}
"""


def escape_text(text: str) -> str:
  return html.escape(text)


def clean_text(text: str) -> str:
  return text.replace("\u200b", "").replace("\ufeff", "").replace("\xa0", " ").strip()


def normalize_text(text: str) -> str:
  return re.sub(r"\s+", " ", clean_text(text))


def truncate_text(text: str, limit: int) -> str:
  normalized = normalize_text(text)
  if len(normalized) <= limit:
    return normalized
  return normalized[: max(limit - 1, 1)].rstrip("，。！？、；：,.!?;: ") + "…"


def split_keyword_candidates(text: str) -> list[str]:
  normalized = normalize_text(text)
  if not normalized:
    return []
  return [
    part.strip("·#-— ")
    for part in re.split(r"[|｜/、，,。：:；;“”\"'‘’《》【】（）()\s]+", normalized)
    if part.strip("·#-— ")
  ]


def text_from_block_for_intro(block: dict) -> str:
  block_type = block.get("type")
  if block_type in {"text", "heading", "subheading", "quote", "highlight", "meta"}:
    return normalize_text(block.get("text", ""))
  if block_type == "prompt":
    label = normalize_text(block.get("label", ""))
    if label:
      return label
    lines = [normalize_text(line) for line in str(block.get("text", "")).splitlines() if normalize_text(line)]
    return lines[0] if lines else ""
  if block_type == "list":
    items = [normalize_text(item) for item in block.get("items", []) if normalize_text(item)]
    return "；".join(items[:3])
  if block_type == "group":
    texts: list[str] = []
    for item in block.get("items", []):
      title = normalize_text(item.get("title", ""))
      body = normalize_text(item.get("text", ""))
      joined = "：".join(part for part in [title, body] if part)
      if joined:
        texts.append(joined)
    return "；".join(texts[:3])
  if block_type == "video":
    return normalize_text(block.get("title", "")) or normalize_text(block.get("summary", ""))
  if block_type == "hero":
    return normalize_text(block.get("summary", "")) or normalize_text(block.get("title", ""))
  return ""


def infer_intro_category(blocks: list[dict]) -> str:
  if any(block.get("type") == "video" for block in blocks):
    return "视频类"
  if any(block.get("type") == "prompt" for block in blocks):
    return "提示词类"
  image_count = sum(1 for block in blocks if block.get("type") == "image")
  if image_count >= 3:
    return "图片类"
  if any(block.get("type") in {"group", "list"} for block in blocks):
    return "结构类"
  return "观点类"


def infer_intro_keywords(title: str, blocks: list[dict]) -> list[str]:
  picked: list[str] = []

  def add(keyword: str) -> None:
    normalized = normalize_text(keyword)
    if not normalized or normalized in picked or normalized in INTRO_KEYWORD_STOPWORDS:
      return
    if len(normalized) < 2 or len(normalized) > 12:
      return
    picked.append(normalized)

  for piece in split_keyword_candidates(title):
    add(piece)

  for block in blocks:
    if block.get("type") in {"heading", "subheading", "highlight"}:
      add(text_from_block_for_intro(block))
    for piece in split_keyword_candidates(text_from_block_for_intro(block)):
      add(piece)
      if len(picked) >= 5:
        return picked[:5]

  return picked[:5] or [infer_intro_category(blocks), "主题拆解", "视觉重点"]


def infer_intro_summary(title: str, blocks: list[dict]) -> str:
  fragments: list[str] = []
  priority_types = {"text", "quote", "highlight", "prompt"}
  for block in blocks:
    if block.get("type") not in priority_types:
      continue
    text = text_from_block_for_intro(block)
    if len(text) < 8:
      continue
    fragments.append(text)
    if len(fragments) >= 2:
      break

  if not fragments:
    for block in blocks:
      text = text_from_block_for_intro(block)
      if not text:
        continue
      fragments.append(text)
      if len(fragments) >= 2:
        break

  summary = " ".join(fragments).strip()
  if not summary:
    summary = f"这篇内容围绕“{normalize_text(title) or '今天这篇文章'}”展开，先看导读再决定从哪一节进入。"
  return truncate_text(summary, 88)


def pick_intro_visual(blocks: list[dict]) -> tuple[str, str]:
  for block in blocks:
    if block.get("type") == "image" and normalize_text(block.get("src", "")):
      return block.get("src", ""), normalize_text(block.get("alt", "")) or "今日主题视觉"
  return "", "今日主题视觉"


def ensure_intro_card(title: str, blocks: list[dict]) -> list[dict]:
  if blocks and blocks[0].get("type") == "hero":
    return blocks
  category = infer_intro_category(blocks)
  keywords = infer_intro_keywords(title, blocks)
  image_src, image_alt = pick_intro_visual(blocks)
  hero_block = {
    "type": "hero",
    "title": normalize_text(title) or "未命名文章",
    "category": category,
    "theme": keywords[0] if keywords else category,
    "summary": infer_intro_summary(title, blocks),
    "keywords": keywords,
    "image_src": image_src,
    "image_alt": image_alt,
  }
  return [hero_block, *blocks]


def canonicalize_src(src: str) -> str:
  parts = urlsplit(src)
  query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if key not in {"width", "height", "policy", "format"}]
  return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def slugify(text: str) -> str:
  cleaned = re.sub(r'[\\/:*?"<>|]+', " ", clean_text(text))
  cleaned = re.sub(r"\s+", " ", cleaned).strip()
  return cleaned or "未命名文章"


def should_drop_text(text: str) -> bool:
  normalized = normalize_text(text)
  if not normalized:
    return True
  if normalized in {"❗", "💡", "•"}:
    return True
  return any(noise in normalized for noise in UI_NOISE)


def is_good_image(block: dict) -> bool:
  width = int(block.get("width", 0) or 0)
  height = int(block.get("height", 0) or 0)
  if width <= 0 or height <= 0:
    return True
  ratio = width / height
  if width < 180 or height < 110:
    return False
  return 0.45 <= ratio <= 3.4


def dedupe_blocks(blocks: list[dict]) -> list[dict]:
  merged: list[dict] = []
  seen_images: set[str] = set()
  recent_texts: list[str] = []
  for block in blocks:
    block_type = block.get("type")
    if block_type == "image":
      src = canonicalize_src(block.get("src", ""))
      if not src or src in seen_images:
        continue
      seen_images.add(src)
      merged.append(
        {
          "type": "image",
          "src": src,
          "alt": clean_text(block.get("alt", "")) or "文章配图",
          "width": int(block.get("width", 0) or 0),
          "height": int(block.get("height", 0) or 0),
          "top": int(block.get("top", 0) or 0),
          "left": int(block.get("left", 0) or 0),
        }
      )
      continue

    text = normalize_text(block.get("text", ""))
    if should_drop_text(text):
      continue
    token = f"{block_type}::{text}"
    if token in recent_texts[-120:]:
      continue
    recent_texts.append(token)
    merged.append(
      {
        "type": "heading" if block_type == "heading" else block_type,
        "text": text,
        "top": int(block.get("top", 0) or 0),
        "left": int(block.get("left", 0) or 0),
      }
    )
  return merged


def mark_scroll_root(page: Page) -> dict[str, int]:
  return page.evaluate(MARK_SCROLL_ROOT_JS)


def build_positions(metrics: dict[str, int]) -> list[int]:
  scroll_height = int(metrics.get("scrollHeight", 0) or 0)
  client_height = int(metrics.get("clientHeight", 0) or 0)
  max_top = max(scroll_height - client_height, 0)
  if max_top <= 0:
    return [0]
  step = max(int(client_height * 0.78), 720)
  positions = list(range(0, max_top + 1, step))
  if positions[-1] != max_top:
    positions.append(max_top)
  return positions


def fetch_image_data_urls(page: Page, blocks: list[dict]) -> dict[str, str]:
  sources: list[str] = []
  seen: set[str] = set()
  for block in blocks:
    if block["type"] != "image":
      continue
    src = block["src"]
    if src in seen:
      continue
    seen.add(src)
    sources.append(src)

  data_urls: dict[str, str] = {}
  if not sources:
    return data_urls

  payloads = page.evaluate(FETCH_IMAGE_JS, {"sources": sources, "timeoutMs": 12000})
  for payload in payloads:
    src = payload.get("src", "")
    if not src:
      continue
    if payload.get("ok") and payload.get("passthrough"):
      data_urls[src] = src
    elif payload.get("ok"):
      data_urls[src] = f"data:{payload['type']};base64,{payload['b64']}"
    else:
      data_urls[src] = src
  return data_urls


def extract_from_feishu(url: str, *, fetch_images: bool = True) -> tuple[str, list[dict], dict[str, str]]:
  with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 2200})
    page.goto(url, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(3500)
    metrics = mark_scroll_root(page)
    collected: list[dict] = []
    title = ""

    for top in build_positions(metrics):
      page.evaluate(
        """(top) => {
          const root = document.querySelector('[data-codex-scroll-root="1"]');
          if (root) root.scrollTop = top;
        }""",
        top,
      )
      page.wait_for_timeout(450)
      snapshot = page.evaluate(COLLECT_BLOCKS_JS)
      title = clean_text(snapshot.get("title", "")) or title
      collected.extend(snapshot.get("blocks", []))

    page.evaluate(
      """() => {
        const root = document.querySelector('[data-codex-scroll-root="1"]');
        if (root) root.scrollTop = 0;
      }"""
    )
    page.wait_for_timeout(500)
    blocks = dedupe_blocks(collected)
    image_data = fetch_image_data_urls(page, blocks) if fetch_images else {}
    browser.close()
  return title or "未命名文章", blocks, image_data


def emphasis_candidates(text: str) -> list[str]:
  candidates: list[tuple[int, str]] = []

  def push(fragment: str, score: int) -> None:
    normalized = normalize_text(fragment).strip("，。！？；：、（）()[]【】 ")
    if not normalized or len(normalized) < 2 or len(normalized) > 24:
      return
    if normalized in EMPHASIS_STOPWORDS:
      return
    if any(normalized in existing or existing in normalized for _, existing in candidates):
      return
    candidates.append((score, normalized))

  for fragment in re.findall(r"[“\"《【](.{2,24}?)[”\"》】]", text):
    push(fragment, 5)

  for fragment in re.findall(r"\b[A-Za-z][A-Za-z0-9.+#/_-]*(?:\s+[A-Za-z0-9.+#/_-]+){0,3}", text):
    if any(char.isupper() for char in fragment) or any(char.isdigit() for char in fragment):
      push(fragment, 4)

  for clause in re.split(r"[，。！？；：]", text):
    normalized = normalize_text(clause)
    if not 4 <= len(normalized) <= 18:
      continue
    score = 0
    if any(hint in normalized for hint in EMPHASIS_HINTS):
      score += 3
    if normalized.startswith(("不是", "真正", "关键", "核心", "最好", "一定", "别", "不要", "先")):
      score += 2
    if any(char.isalpha() for char in normalized) or any(char.isdigit() for char in normalized):
      score += 2
    if score >= 3:
      push(normalized, score)

  ranked = sorted(candidates, key=lambda item: (-item[0], -len(item[1])))
  return [fragment for _, fragment in ranked[:4]]


def stylize_text(text: str, *, max_hits: int = 2) -> str:
  rendered = escape_text(text)
  hits = 0
  for fragment in emphasis_candidates(text):
    if hits >= max_hits:
      break
    escaped = html.escape(fragment)
    if escaped in rendered:
      rendered = rendered.replace(
        escaped,
        f'<strong style="color:{PALETTE["accent"]};font-weight:700;">{escaped}</strong>',
        1,
      )
      hits += 1
  return rendered


def prompt_score(text: str) -> int:
  normalized = normalize_text(text)
  if not normalized:
    return -10
  score = 0
  if any(normalized.startswith(prefix) for prefix in ROLE_PREFIXES):
    score += 6
  if normalized in FIELD_MARKERS or normalized.endswith("："):
    score += 4
  if re.fullmatch(r"\d+\s*[、.．]?\s*\S+", normalized):
    score += 3
  if any(token in normalized for token in ("HTML", "CSS", "JavaScript", "输出", "网页", "页面", "课程", "项目", "视觉", "代码")):
    score += 2
  if len(normalized) <= 18:
    score += 1
  if any(marker in normalized for marker in RESUME_MARKERS):
    score -= 8
  return score


def looks_like_resume_sentence(text: str) -> bool:
  normalized = normalize_text(text)
  return any(marker in normalized for marker in RESUME_MARKERS)


def has_prompt_context(blocks: list[dict], start: int) -> bool:
  total = 0
  hits = 0
  for block in blocks[start:start + 12]:
    if block["type"] == "image":
      continue
    score = prompt_score(block.get("text", ""))
    total += max(score, 0)
    if score >= 4:
      hits += 1
  return total >= 12 and hits >= 2


def prompt_label(lines: list[str]) -> str:
  joined = " ".join(lines[:10])
  if any(token in joined for token in ("官网", "落地页", "首页", "网页")):
    return "这段网页提示词"
  if any(token in joined for token in ("课程", "训练营", "项目方案", "商业模式")):
    return "这段方案提示词"
  if any(token in joined for token in ("小说", "修仙", "剑宗", "玄清宗")):
    return "这段剧情提示词"
  if any(token in joined for token in ("生图", "插画", "海报", "视觉")):
    return "这段生图提示词"
  return "这段提示词，我单拎出来了"


def collect_prompt_block(blocks: list[dict], start: int) -> tuple[dict | None, int]:
  if start >= len(blocks):
    return None, start
  first = blocks[start]
  if first["type"] != "text":
    return None, start
  _, has_list_marker = strip_list_marker(first.get("text", ""))
  if has_list_marker:
    return None, start
  if prompt_score(first.get("text", "")) < 4 or not has_prompt_context(blocks, start):
    return None, start

  lines: list[str] = []
  index = start
  promptish = 0
  while index < len(blocks):
    block = blocks[index]
    if block["type"] == "heading" and lines:
      break
    if block["type"] == "image":
      break
    text = normalize_text(block.get("text", ""))
    if not text:
      index += 1
      continue
    if looks_like_resume_sentence(text):
      break
    score = prompt_score(text)
    if lines and score <= 0 and len(text) > 24 and not text.endswith("："):
      break
    lines.append(text)
    if score >= 3:
      promptish += 1
    index += 1

  if len(lines) < 4 or promptish < 2:
    return None, start

  return {
    "type": "prompt",
    "label": prompt_label(lines),
    "text": "\n".join(lines),
  }, index


def is_inline_heading(blocks: list[dict], index: int, text: str) -> bool:
  normalized = normalize_text(text)
  if not 6 <= len(normalized) <= 22:
    return False
  if normalized.endswith(("。", "！", "？", "；", "：", "~")):
    return False
  if normalized in FIELD_MARKERS or any(normalized.startswith(prefix) for prefix in ROLE_PREFIXES):
    return False

  previous = normalize_text(blocks[index - 1].get("text", "")) if index > 0 else ""
  following = normalize_text(blocks[index + 1].get("text", "")) if index + 1 < len(blocks) else ""
  if previous and not re.search(r"[。！？!?：:]$", previous):
    return False
  if following.startswith(("，", "也", "而", "但", "所以", "因为")):
    return False
  return any(token in normalized for token in ("问题", "麻烦", "门槛", "原因", "重点", "关键", "建议", "体验", "平台", "模型", "朋友", "新手", "普通人"))


def quote_like(text: str) -> bool:
  normalized = normalize_text(text)
  if len(normalized) > 28:
    return False
  return any(token in normalized for token in ("普通人", "很麻烦", "新手友好", "你到底该用哪个", "值不值得"))


LIST_MARKER_RE = re.compile(r"^(?:[-•·●▪◦]\s*|(?:[（(]?\d{1,2}[)）]?|[①-⑳]|[一二三四五六七八九十]+)[、.．)]\s*)")


def strip_list_marker(text: str) -> tuple[str, bool]:
  normalized = normalize_text(text)
  stripped = LIST_MARKER_RE.sub("", normalized).strip()
  return (stripped or normalized), stripped != normalized


def looks_like_meta_line(text: str) -> bool:
  normalized = normalize_text(text)
  return (
    normalized.endswith("修改")
    or normalized.startswith("最新修改时间")
    or bool(re.fullmatch(r"(昨天|今天|前天)修改", normalized))
    or bool(re.fullmatch(r"\d{1,2}月\d{1,2}日(?:修改)?", normalized))
  )


def looks_like_date_line(text: str) -> bool:
  normalized = normalize_text(text)
  return bool(re.fullmatch(r"\d{4}年\d{1,2}月\d{1,2}日", normalized))


def is_heading_candidate(text: str) -> bool:
  normalized = normalize_text(text)
  if not 2 <= len(normalized) <= 18:
    return False
  if looks_like_meta_line(normalized) or looks_like_date_line(normalized):
    return False
  if normalized.startswith(("——", "-", "—")):
    return False
  if re.search(r"[。！？；，,.!?：:、（）()…]$", normalized):
    return False
  if any(char.isdigit() for char in normalized):
    return False
  return True


def has_heading_cue(text: str) -> bool:
  normalized = normalize_text(text)
  return (
    normalized in {"现在", "后来", "最后"}
    or normalized.startswith(("关于", "那个", "你让我", "刚", "后来", "直到"))
    or normalized.endswith(("的时候", "那天", "之后"))
  )


def should_keep_separate_text(text: str) -> bool:
  normalized = normalize_text(text)
  if not normalized:
    return False
  _, has_marker = strip_list_marker(normalized)
  if has_marker:
    return True
  if looks_like_meta_line(normalized) or looks_like_date_line(normalized):
    return True
  if normalized.startswith(("——", "-", "—")):
    return True
  return is_heading_candidate(normalized) and (has_heading_cue(normalized) or len(normalized) <= 8)


def build_group_item(text: str, index: int) -> dict:
  normalized = normalize_text(text)
  if "：" in normalized:
    title, body = normalized.split("：", 1)
    if 1 <= len(title.strip()) <= 12 and len(body.strip()) >= 4:
      return {"title": title.strip(), "text": body.strip()}
  return {"title": "", "text": normalized}


def collect_structured_series(blocks: list[dict], start: int) -> tuple[dict | None, int]:
  if start >= len(blocks) or blocks[start]["type"] != "text":
    return None, start

  previous_type = blocks[start - 1]["type"] if start > 0 else ""
  items: list[str] = []
  explicit = False
  index = start

  while index < len(blocks):
    block = blocks[index]
    if block["type"] != "text":
      break
    text = normalize_text(block.get("text", ""))
    if not text or looks_like_meta_line(text) or looks_like_date_line(text):
      break
    stripped, has_marker = strip_list_marker(text)
    if prompt_score(text) >= 4 and not has_marker:
      break
    candidate = stripped if has_marker else text
    if len(candidate) > 42:
      break
    if explicit and not has_marker:
      break
    if not explicit and items and not has_marker and len(candidate) > 28:
      break
    explicit = explicit or has_marker
    items.append(candidate)
    index += 1
    if len(items) >= 4:
      break

  if len(items) < 2:
    return None, start

  max_len = max(len(item) for item in items)
  avg_len = sum(len(item) for item in items) / len(items)
  if explicit:
    if len(items) == 3 and max_len <= 28:
      return {
        "type": "group",
        "layout": "horizontal",
        "items": [build_group_item(item, idx) for idx, item in enumerate(items)],
      }, index
    return {
      "type": "list",
      "style": "ordered",
      "items": items,
    }, index

  if previous_type in {"heading", "subheading", "highlight"} and len(items) in {2, 3} and avg_len <= 22 and max_len <= 30:
    return {
      "type": "group",
      "layout": "horizontal" if len(items) == 3 else "vertical",
      "items": [build_group_item(item, idx) for idx, item in enumerate(items)],
    }, index

  return None, start


def is_highlight_candidate(blocks: list[dict], index: int, text: str) -> bool:
  normalized = normalize_text(text)
  if not 10 <= len(normalized) <= 36:
    return False
  if looks_like_meta_line(normalized) or looks_like_date_line(normalized):
    return False
  if prompt_score(normalized) >= 4:
    return False
  if is_heading_candidate(normalized):
    return False
  if not normalized.endswith(("。", "！", "？", "……")):
    return False
  if normalized.count("，") >= 3:
    return False

  previous = normalize_text(blocks[index - 1].get("text", "")) if index > 0 else ""
  following = normalize_text(blocks[index + 1].get("text", "")) if index + 1 < len(blocks) else ""
  has_context = len(previous) >= 20 or len(following) >= 20 or (index > 0 and blocks[index - 1]["type"] in {"heading", "subheading"})
  if not has_context:
    return False
  cue = (
    normalized.startswith(("不是因为", "因为", "所以", "而是", "但", "后来", "其实", "只是"))
    or "被看见" in normalized
    or "我想" in normalized
    or "我记得" in normalized
    or "很重要" in normalized
    or len(normalized) <= 18
  )
  return cue


def display_width(width: int, height: int) -> str:
  if width > 0 and height > 0:
    ratio = width / height
    if ratio >= 1.4:
      return "92%"
    if ratio <= 0.82:
      return "62%"
    if ratio <= 1.05:
      return "70%"
  return "78%"


def text_contains_recent_fragment(recent_texts: list[str], candidate: str) -> bool:
  stripped = candidate.lstrip("。，“”\"")
  for item in recent_texts[-3:]:
    if len(item) >= len(stripped) + 6 and stripped and stripped in item:
      return True
  return False


def should_merge_text(previous: str, current: str) -> bool:
  if not previous or not current:
    return False
  if should_keep_separate_text(previous) or should_keep_separate_text(current):
    return False
  if current.startswith(("。", "，", "、", "；", "：", "）", "”", "\"")):
    return True
  if previous.endswith(("，", "、", "：", "；", "（", "“", "\"", "……", "...")):
    return True
  if not re.search(r"[。！？!?：；]$", previous) and not looks_like_meta_line(current):
    return True
  if len(current) <= 8 and not re.search(r"[。！？!?]$", current):
    return True
  return False


def merge_text(previous: str, current: str) -> str:
  if current.startswith(("。", "，", "、", "；", "：", "）", "”", "\"")):
    return f"{previous.rstrip()}{current.lstrip()}"
  return f"{previous.rstrip()}{current.lstrip()}"


def refine_text_blocks(blocks: list[dict]) -> list[dict]:
  refined: list[dict] = []
  recent_texts: list[str] = []
  for block in blocks:
    if block["type"] != "text":
      refined.append(block)
      continue

    text = normalize_text(block.get("text", ""))
    if not text:
      continue
    if text_contains_recent_fragment(recent_texts, text):
      continue

    if refined and refined[-1]["type"] == "text":
      previous_text = refined[-1]["text"]
      if text in previous_text and len(text) < len(previous_text):
        continue
      if previous_text in text and len(previous_text) < len(text) and len(previous_text) <= 14:
        refined[-1]["text"] = text
        recent_texts.append(text)
        continue
      if should_merge_text(previous_text, text):
        refined[-1]["text"] = merge_text(previous_text, text)
        recent_texts.append(refined[-1]["text"])
        continue

    refined.append({"type": "text", "text": text})
    recent_texts.append(text)

  return refined


def promote_heading_blocks(blocks: list[dict]) -> list[dict]:
  promoted: list[dict] = []
  for index, block in enumerate(blocks):
    if block["type"] != "text":
      promoted.append(block)
      continue

    text = normalize_text(block.get("text", ""))
    previous = normalize_text(blocks[index - 1].get("text", "")) if index > 0 else ""
    following = normalize_text(blocks[index + 1].get("text", "")) if index + 1 < len(blocks) else ""

    is_heading = False
    if is_heading_candidate(text):
      previous_closed = bool(previous) and bool(re.search(r"[。！？!?：:…]$", previous))
      following_long_enough = len(following) >= 8 and not looks_like_meta_line(following)
      if has_heading_cue(text):
        is_heading = True
      elif previous_closed and following_long_enough:
        is_heading = True
      elif len(text) <= 8 and following_long_enough:
        is_heading = True
      elif previous_closed and len(text) <= 12:
        is_heading = True

    promoted.append({"type": "heading" if is_heading else "text", "text": text})
  return promoted


def auto_layout_blocks(blocks: list[dict]) -> list[dict]:
  laid_out: list[dict] = []
  index = 0
  while index < len(blocks):
    block = blocks[index]
    if block["type"] != "text":
      laid_out.append(block)
      index += 1
      continue

    prompt_block, prompt_end = collect_prompt_block(blocks, index)
    if prompt_block:
      laid_out.append(prompt_block)
      index = prompt_end
      continue

    series_block, series_end = collect_structured_series(blocks, index)
    if series_block:
      laid_out.append(series_block)
      index = series_end
      continue

    text = normalize_text(block.get("text", ""))
    if is_highlight_candidate(blocks, index, text):
      laid_out.append({"type": "highlight", "text": text})
      index += 1
      continue

    laid_out.append(block)
    index += 1

  return laid_out


def auto_layout_article(article: dict) -> dict:
  blocks = article.get("blocks", [])
  laid_out = auto_layout_blocks(promote_heading_blocks(refine_text_blocks(blocks)))
  return {
    "title": article.get("title", ""),
    "blocks": ensure_intro_card(article.get("title", ""), laid_out),
  }


def normalize_article(title: str, raw_blocks: list[dict], image_data: dict[str, str], footer_data_url: str | None) -> dict:
  start = 0
  normalized_title = normalize_text(title)
  for idx, block in enumerate(raw_blocks):
    if block["type"] == "title" and normalize_text(block.get("text", "")) == normalized_title:
      start = idx
      break

  blocks = raw_blocks[start:]
  article_blocks: list[dict] = []
  if blocks and normalize_text(blocks[0].get("text", "")) == normalized_title:
    blocks = blocks[1:]
  if blocks and blocks[0]["type"] == "meta":
    article_blocks.append({"type": "meta", "text": blocks[0]["text"]})
    blocks = blocks[1:]

  seen_headings: set[str] = set()
  for block in blocks:
    if block["type"] == "image":
      if not is_good_image(block):
        continue
      article_blocks.append(
        {
          "type": "image",
          "src": image_data.get(block["src"], block["src"]),
          "alt": block.get("alt", "文章配图"),
          "width": int(block.get("width", 0) or 0),
          "height": int(block.get("height", 0) or 0),
        }
      )
      continue

    text = normalize_text(block.get("text", ""))
    if should_drop_text(text) or text == normalized_title:
      continue
    if not article_blocks and looks_like_meta_line(text):
      article_blocks.append({"type": "meta", "text": text})
      continue
    if block["type"] == "heading":
      if text in seen_headings:
        continue
      seen_headings.add(text)
      article_blocks.append({"type": "heading", "text": text})
      continue
    article_blocks.append({"type": "text", "text": text})

  article_blocks = refine_text_blocks(article_blocks)
  article_blocks = promote_heading_blocks(article_blocks)
  article_blocks = auto_layout_blocks(article_blocks)
  article_blocks = ensure_intro_card(title, article_blocks)

  if footer_data_url:
    article_blocks.append({"type": "image", "src": footer_data_url, "alt": "关注引导图", "width": 1280, "height": 640})

  return {
    "title": title,
    "blocks": article_blocks,
  }


def render_meta(text: str) -> str:
  return (
    f'<p style="margin:0 0 18px;color:{PALETTE["muted"]};font-size:12px;line-height:1.6;letter-spacing:0.8px;">'
    f"{escape_text(text)}</p>"
  )


def render_keyword_pills(keywords: list[str]) -> str:
  visible = [normalize_text(keyword) for keyword in keywords if normalize_text(keyword)]
  if not visible:
    return ""
  return "".join(
    f'<span style="display:inline-block;margin:0 8px 8px 0;padding:6px 12px;border-radius:999px;'
    f'background-color:#fff9ef;border:1px solid {WARM_BORDER};color:{PALETTE["accent"]};font-size:12px;'
    f'line-height:1.2;font-weight:700;">#{escape_text(keyword)}</span>'
    for keyword in visible[:5]
  )


def render_intro_visual(block: dict) -> str:
  image_src = normalize_text(block.get("image_src", ""))
  image_alt = normalize_text(block.get("image_alt", "")) or "今日主题视觉"
  if image_src:
    return (
      f'<span style="display:block;padding:8px;border-radius:26px;background-color:#edd5b6;">'
      f'<span style="display:block;padding:8px;border-radius:22px;background-color:#fff5e8;">'
      f'<img src="{escape_text(image_src)}" alt="{escape_text(image_alt)}" '
      'style="display:block;width:100%;max-width:100%;height:auto;border-radius:16px;" />'
      '</span></span>'
    )
  return (
    f'<span style="display:block;padding:8px;border-radius:26px;background-color:#edd5b6;">'
    f'<span style="display:block;min-height:198px;padding:18px 16px;border-radius:22px;background-color:#fff5e8;">'
    f'<span style="display:block;width:76px;height:76px;margin:0 0 12px auto;border-radius:24px;background-color:#ecd0b1;"></span>'
    f'<span style="display:block;width:48px;height:4px;margin:0 0 14px;border-radius:999px;background-color:{WARM_LINE};"></span>'
    f'<span style="display:block;height:54px;border-radius:18px;background-color:#f1dcc3;"></span>'
    '</span></span>'
  )


def render_hero_card(block: dict) -> str:
  title = normalize_text(block.get("title", ""))
  category = normalize_text(block.get("category", ""))
  summary = normalize_text(block.get("summary", ""))
  theme = normalize_text(block.get("theme", ""))
  keywords_markup = render_keyword_pills(block.get("keywords", []))
  title_markup = (
    f'<p style="margin:0 0 12px;font-family:\'Songti SC\',\'STSong\',\'SimSun\',serif;color:{PALETTE["ink"]};'
    f'font-size:30px;line-height:1.36;font-weight:700;">{escape_text(title)}</p>'
    if title
    else ""
  )
  category_markup = (
    f'<span style="display:inline-block;margin:0 0 8px;padding:6px 12px;border-radius:999px;background-color:#fff3e4;'
    f'color:{PALETTE["accent"]};font-size:11px;line-height:1.2;font-weight:700;">{escape_text(category)}</span>'
    if category
    else ""
  )
  theme_markup = (
    f'<p style="margin:0 0 10px;color:{PALETTE["muted"]};font-size:12px;line-height:1.6;letter-spacing:1.2px;'
    f'text-transform:uppercase;">Theme · {escape_text(theme)}</p>'
    if theme
    else ""
  )
  summary_markup = (
    f'<p style="margin:0 0 14px;color:{PALETTE["text"]};font-size:15px;line-height:1.86;">{stylize_text(summary, max_hits=1)}</p>'
    if summary
    else ""
  )
  return (
    f'<span style="display:block;margin:0 0 32px;padding:10px;border-radius:32px;background-color:#ecd4b5;">'
    f'<span style="display:block;padding:18px 18px 16px;border-radius:28px;background-color:#fff4e8;">'
    '<span style="display:block;font-size:0;white-space:nowrap;">'
    '<span style="display:inline-block;vertical-align:top;width:63%;padding-right:14px;white-space:normal;">'
    f'<p style="margin:0 0 12px;">'
    f'<span style="display:inline-block;margin:0 8px 8px 0;padding:6px 12px;border-radius:999px;background-color:{WARM_PILL};'
    f'color:{PALETTE["accent"]};font-size:11px;line-height:1.2;font-weight:700;letter-spacing:1.5px;">今日导读</span>'
    f'{category_markup}</p>'
    f'{theme_markup}'
    f'{title_markup}'
    f'{summary_markup}'
    f'<div>{keywords_markup}</div>'
    '</span>'
    f'<span style="display:inline-block;vertical-align:top;width:37%;white-space:normal;">{render_intro_visual(block)}</span>'
    '</span>'
    '</span>'
    '</span>'
  )


def render_video_cover(block: dict) -> str:
  cover_src = normalize_text(block.get("cover_src", ""))
  cover_alt = normalize_text(block.get("cover_alt", "")) or "视频封面"
  if cover_src:
    return (
      f'<span style="display:block;padding:8px;border-radius:26px;background-color:#edd5b6;">'
      f'<span style="display:block;padding:8px;border-radius:22px;background-color:#fff5e8;">'
      f'<img src="{escape_text(cover_src)}" alt="{escape_text(cover_alt)}" '
      'style="display:block;width:100%;max-width:100%;height:auto;border-radius:16px;" />'
      '</span></span>'
    )
  return (
    f'<span style="display:block;padding:8px;border-radius:26px;background-color:#edd5b6;">'
    f'<span style="display:block;min-height:184px;padding:18px 16px;border-radius:22px;background-color:#fff5e8;">'
    f'<span style="display:block;width:100%;height:100%;min-height:148px;border-radius:18px;background-color:#f1dcc3;">'
    f'<span style="display:block;width:56px;height:56px;margin:44px auto 0;border-radius:999px;background-color:#fff0df;"></span>'
    '</span>'
    '</span></span>'
  )


def render_video_card(block: dict) -> str:
  title = normalize_text(block.get("title", ""))
  summary = normalize_text(block.get("summary", ""))
  note = normalize_text(block.get("note", ""))
  link = normalize_text(block.get("link", ""))
  title_markup = (
    f'<p style="margin:0 0 10px;color:{PALETTE["ink"]};font-family:\'Songti SC\',\'STSong\',\'SimSun\',serif;'
    f'font-size:24px;line-height:1.45;font-weight:700;">{escape_text(title)}</p>'
    if title
    else ""
  )
  summary_markup = (
    f'<p style="margin:0 0 12px;color:{PALETTE["text"]};font-size:15px;line-height:1.84;">{stylize_text(summary, max_hits=1)}</p>'
    if summary
    else ""
  )
  note_markup = (
    f'<div style="padding:10px 12px;border-radius:16px;background-color:#fff5e9;'
    f'color:{PALETTE["accent"]};font-size:13px;line-height:1.75;font-weight:600;">{escape_text(note)}</div>'
    if note
    else ""
  )
  link_markup = (
    f'<p style="margin:10px 0 0;color:{PALETTE["muted"]};font-size:12px;line-height:1.7;">视频链接：{escape_text(link)}</p>'
    if link
    else ""
  )
  return (
    f'<span style="display:block;margin:20px 0 28px;padding:10px;border-radius:32px;background-color:#ecd4b7;">'
    f'<span style="display:block;padding:16px 16px 14px;border-radius:28px;background-color:#fff4e8;">'
    f'<p style="margin:0 0 12px;"><span style="display:inline-block;margin:0 8px 8px 0;padding:6px 12px;border-radius:999px;'
    f'background-color:{WARM_PILL};color:{PALETTE["accent"]};font-size:11px;line-height:1.2;font-weight:700;letter-spacing:1.6px;">VIDEO</span>'
    f'<span style="display:inline-block;margin:0 0 8px;padding:6px 12px;border-radius:999px;background-color:#fff4e7;'
    f'color:{PALETTE["accent"]};font-size:11px;line-height:1.2;font-weight:700;">报编信息</span></p>'
    '<span style="display:block;font-size:0;white-space:nowrap;">'
    f'<span style="display:inline-block;vertical-align:top;width:42%;padding-right:14px;white-space:normal;">{render_video_cover(block)}</span>'
    '<span style="display:inline-block;vertical-align:top;width:58%;white-space:normal;">'
    f'{title_markup}'
    f'{summary_markup}'
    f'{note_markup}'
    f'{link_markup}'
    '</span>'
    '</span>'
    '</span>'
    '</span>'
  )


def render_heading(text: str, chapter_number: int) -> str:
  label = f"{chapter_number:02d}"
  return (
    f'<div style="margin:46px 0 28px;">'
    f'<p style="margin:0 0 12px;"><span style="display:inline-block;padding:6px 14px;border-radius:999px;'
    f'background-color:{WARM_PILL};color:{PALETTE["accent"]};font-size:11px;line-height:1.2;font-weight:700;'
    f'letter-spacing:1.8px;text-transform:uppercase;">Chapter {label}</span></p>'
    f'<div style="padding-left:14px;border-left:3px solid {WARM_LINE};">'
    f'<p style="margin:0;font-family:\'Songti SC\',\'STSong\',\'SimSun\',serif;'
    f'color:{PALETTE["ink"]};font-size:29px;line-height:1.42;font-weight:700;letter-spacing:0.1px;">{escape_text(text)}</p>'
    f'<div style="width:92px;height:2px;margin-top:12px;background-color:{WARM_LINE};border-radius:999px;"></div>'
    '</div>'
    "</div>"
  )


def render_subheading(text: str, section_number: int) -> str:
  label = f"{section_number:02d}"
  return (
    f'<div style="margin:30px 0 20px;">'
    f'<p style="margin:0 0 10px;"><span style="display:inline-block;padding:4px 10px;'
    f'border-radius:999px;background-color:{WARM_PILL};color:{PALETTE["accent"]};font-size:11px;line-height:1.2;'
    f'font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">Section {label}</span></p>'
    f'<div style="padding-left:12px;border-left:2px solid {WARM_BORDER};">'
    f'<p style="margin:0;font-family:\'Songti SC\',\'STSong\',\'SimSun\',serif;'
    f'color:{PALETTE["ink"]};font-size:22px;line-height:1.5;font-weight:700;letter-spacing:0.2px;">'
    f'{escape_text(text)}</p>'
    '</div>'
    '</div>'
  )


def render_paragraph(text: str, *, lead: bool = False) -> str:
  size = 18 if lead else 16
  color = PALETTE["ink"] if lead else PALETTE["text"]
  weight = 600 if lead else 400
  margin = "0 0 18px" if lead else "0 0 17px"
  return (
    f'<p style="margin:{margin};color:{color};font-size:{size}px;line-height:1.92;font-weight:{weight};">'
    f"{stylize_text(text)}</p>"
  )


def render_quote(text: str) -> str:
  return (
    f'<div style="margin:18px 0 22px;padding:14px 16px 14px 16px;border-left:3px solid {PALETTE["accent"]};'
    f'background-color:{WARM_PANEL_SOFT};border-radius:0 18px 18px 0;'
    f'color:{PALETTE["ink"]};font-size:17px;line-height:1.9;font-weight:600;">{stylize_text(text, max_hits=1)}</div>'
  )


def render_highlight(text: str) -> str:
  return (
    f'<div style="margin:12px 0 16px;">'
    f'<span style="display:inline-block;max-width:100%;padding:2px 3px 4px;background-color:#f2dfc9;'
    f'border-radius:16px;">'
    f'<span style="display:inline-block;max-width:100%;padding:6px 10px;background-color:#fbefe0;'
    f'border:1px solid {WARM_BORDER};border-radius:14px;">'
    f'<span style="display:block;width:26px;height:3px;margin:0 0 8px;border-radius:999px;background-color:{WARM_LINE};"></span>'
    f'<span style="display:block;color:{PALETTE["ink"]};font-family:\'Songti SC\',\'STSong\',\'SimSun\',serif;'
    f'font-size:17px;line-height:1.72;font-weight:600;">{stylize_text(text, max_hits=2)}</span>'
    '</span>'
    '</span>'
    '</div>'
  )


def prompt_lines_markup(prompt_text: str) -> str:
  lines = [line for line in prompt_text.splitlines() if line.strip()]
  if not lines:
    lines = [prompt_text]
  rendered: list[str] = []
  for line in lines:
    rendered.append(
      f'<p style="margin:0 0 8px;color:#372f28;font-size:13px;line-height:1.75;'
      f'font-family:\'SFMono-Regular\',\'JetBrains Mono\',\'Menlo\',\'PingFang SC\',monospace;'
      f'white-space:pre-wrap;word-break:break-word;">{escape_text(line)}</p>'
    )
  return "".join(rendered)


def render_prompt_card(label: str, prompt_text: str, *, show_hint: bool = True) -> str:
  line_count = len([line for line in prompt_text.splitlines() if line.strip()])
  scroll_style = "max-height:240px;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;padding-right:6px;"
  hint = "这段提示词已经锁成固定高度，可以直接上下滑动看完整内容。"
  if line_count <= 4 and len(prompt_text) <= 120:
    scroll_style = "max-height:240px;overflow-y:auto;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;"
  hint_markup = (
    f'<p style="margin:10px 0 0;color:{PALETTE["muted"]};font-size:12px;line-height:1.6;">{escape_text(hint)}</p>'
    if show_hint
    else ""
  )
  return (
    f'<div style="margin:20px 0 24px;padding:18px 18px 16px;border-radius:24px;'
    f'background-color:{WARM_PANEL};border:1px solid {WARM_BORDER};">'
    f'<span style="display:inline-block;margin:0 0 8px;padding:5px 12px;border-radius:999px;'
    f'background-color:{WARM_PILL};color:{PALETTE["accent"]};font-size:11px;line-height:1.2;font-weight:700;letter-spacing:1.6px;">PROMPT</span>'
    f'<p style="margin:0 0 12px;color:{PALETTE["ink"]};font-size:18px;line-height:1.6;font-weight:600;">{escape_text(label)}</p>'
    f'<div style="padding:14px 15px;border-radius:18px;background-color:#fffdf9;border:1px solid {WARM_BORDER};{scroll_style}">'
    f'{prompt_lines_markup(prompt_text)}'
    "</div>"
    f"{hint_markup}"
    "</div>"
  )


def image_frame(src: str, alt: str, *, width: str, inline: bool = False, margin_right: str = "0") -> str:
  return (
    f'<span style="display:{"inline-block" if inline else "block"};vertical-align:top;width:{width};max-width:100%;'
    f'margin-right:{margin_right};white-space:normal;">'
    f'<span style="display:block;padding:4px;border-radius:24px;background-color:#fff7ee;border:1px solid {WARM_BORDER};">'
    f'<img src="{escape_text(src)}" alt="{escape_text(alt)}" '
    'style="display:block;width:100%;max-width:100%;height:auto;border-radius:20px;" />'
    "</span></span>"
  )


def render_single_image(block: dict) -> str:
  width = display_width(int(block.get("width", 0) or 0), int(block.get("height", 0) or 0))
  return (
    '<div style="margin:18px 0 22px;text-align:center;">'
    f'{image_frame(block["src"], block.get("alt", "文章配图"), width=width)}'
    '</div>'
  )


def render_gallery(blocks: list[dict]) -> str:
  cards: list[str] = []
  for index, block in enumerate(blocks):
    width = "82%" if int(block.get("width", 0) or 0) > int(block.get("height", 0) or 0) else "58%"
    cards.append(
      image_frame(
        block["src"],
        block.get("alt", "文章配图"),
        width=width,
        inline=True,
        margin_right="12px" if index < len(blocks) - 1 else "2px",
      )
    )
  return (
    '<div style="margin:10px 0 24px;">'
    f'<div style="display:flex;justify-content:space-between;align-items:center;margin:0 4px 8px;">'
    f'<span style="color:{PALETTE["accent"]};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.2px;">图组</span>'
    f'<span style="color:{PALETTE["muted"]};font-size:12px;line-height:1.4;">多图可左右滑动</span>'
    '</div>'
    '<div style="overflow-x:auto;white-space:nowrap;padding:4px 2px 10px;-webkit-overflow-scrolling:touch;">'
    f'{"".join(cards)}'
    '</div></div>'
  )


def render_list_block(items: list[str], *, style: str = "unordered") -> str:
  chips: list[str] = []
  for index, item in enumerate(items):
    if not normalize_text(item):
      continue
    bullet = str(index + 1) if style == "ordered" else "•"
    chips.append(
      '<div style="display:flex;align-items:flex-start;gap:12px;margin:0 0 12px;">'
      f'<span style="display:inline-flex;flex:0 0 auto;align-items:center;justify-content:center;min-width:24px;height:24px;'
      f'border-radius:999px;background:rgba(141,91,45,0.12);color:{PALETTE["accent"]};font-size:12px;font-weight:700;">{escape_text(bullet)}</span>'
      f'<p style="margin:0;color:{PALETTE["text"]};font-size:15px;line-height:1.85;">{stylize_text(item, max_hits=1)}</p>'
      '</div>'
    )
  if not chips:
    return ""
  return (
    f'<div style="margin:18px 0 24px;padding:16px 16px 6px;border-radius:22px;'
    f'background-color:{WARM_PANEL};border:1px solid {WARM_BORDER};">'
    f'{"".join(chips)}'
    '</div>'
  )


def render_group_card(title: str, text: str) -> str:
  title_markup = ""
  if normalize_text(title):
    title_markup = (
      f'<p style="margin:0 0 8px;color:{PALETTE["ink"]};font-size:15px;line-height:1.6;'
      f'font-weight:700;">{escape_text(title)}</p>'
    )
  body_markup = (
    f'<p style="margin:0;color:{PALETTE["text"]};font-size:14px;line-height:1.82;">'
    f'{stylize_text(text, max_hits=1)}</p>'
  )
  return (
    f'<div style="height:100%;padding:16px 14px;border-radius:18px;background-color:{WARM_PANEL_SOFT};'
    f'border:1px solid {WARM_BORDER};">'
    f'<div style="width:28px;height:4px;margin:0 0 10px;border-radius:999px;background-color:{WARM_LINE};"></div>'
    f'{title_markup}{body_markup}'
    '</div>'
  )


def render_group_block(items: list[dict], *, layout: str = "horizontal") -> str:
  normalized_items = [
    {
      "title": normalize_text(item.get("title", "")),
      "text": normalize_text(item.get("text", "")),
    }
    for item in items
    if normalize_text(item.get("title", "")) or normalize_text(item.get("text", ""))
  ]
  if not normalized_items:
    return ""

  if layout == "vertical":
    cards = "".join(
      f'<div style="margin:0 0 10px;">{render_group_card(item["title"], item["text"])}</div>'
      for item in normalized_items
    )
    return f'<div style="margin:18px 0 24px;">{cards}</div>'

  rows: list[str] = []
  for offset in range(0, len(normalized_items), 3):
    chunk = normalized_items[offset:offset + 3]
    cells: list[str] = []
    for index, item in enumerate(chunk):
      width = "31.8%" if len(chunk) == 3 else "48.6%"
      margin_right = "10px" if index < len(chunk) - 1 else "0"
      cells.append(
        f'<span style="display:inline-block;vertical-align:top;width:{width};margin-right:{margin_right};">'
        f'{render_group_card(item["title"], item["text"])}'
        '</span>'
      )
    rows.append(f'<div style="margin:0 0 10px;white-space:nowrap;font-size:0;">{"".join(cells)}</div>')
  return f'<div style="margin:18px 0 24px;">{"".join(rows)}</div>'


def wrap_preview_block(markup: str, start_index: int, end_index: int, *, interactive: bool = False) -> str:
  if not interactive:
    return markup
  return (
    f'<section class="wx-preview-block" data-block-index="{start_index}" data-block-end="{end_index}">'
    f'{markup}'
    '</section>'
  )


def compose_article(article: dict, *, interactive: bool = False, show_prompt_hint: bool = True) -> str:
  blocks = article["blocks"]
  parts: list[str] = []
  lead_budget = 2
  index = 0
  chapter_count = 0
  section_count = 0
  while index < len(blocks):
    block = blocks[index]
    block_type = block["type"]

    if block_type == "hero":
      parts.append(wrap_preview_block(render_hero_card(block), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    if block_type == "meta":
      parts.append(wrap_preview_block(render_meta(block["text"]), index, index, interactive=interactive))
      index += 1
      continue

    if block_type == "video":
      parts.append(wrap_preview_block(render_video_card(block), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    if block_type == "image":
      start_index = index
      run: list[dict] = []
      while index < len(blocks) and blocks[index]["type"] == "image":
        run.append(blocks[index])
        index += 1
      markup = render_single_image(run[0]) if len(run) == 1 else render_gallery(run)
      parts.append(wrap_preview_block(markup, start_index, index - 1, interactive=interactive))
      continue

    if block_type == "prompt":
      markup = render_prompt_card(block.get("label", "这段提示词"), block.get("text", ""), show_hint=show_prompt_hint)
      parts.append(wrap_preview_block(markup, index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    if block_type == "quote":
      parts.append(wrap_preview_block(render_quote(block.get("text", "")), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    if block_type == "highlight":
      parts.append(wrap_preview_block(render_highlight(block.get("text", "")), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    if block_type == "list":
      markup = render_list_block(block.get("items", []), style=block.get("style", "unordered"))
      if markup:
        parts.append(wrap_preview_block(markup, index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    if block_type == "group":
      markup = render_group_block(block.get("items", []), layout=block.get("layout", "horizontal"))
      if markup:
        parts.append(wrap_preview_block(markup, index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue

    prompt_block, next_index = collect_prompt_block(blocks, index)
    if prompt_block:
      parts.append(
        wrap_preview_block(
          render_prompt_card(prompt_block["label"], prompt_block["text"], show_hint=show_prompt_hint),
          index,
          next_index - 1,
          interactive=interactive,
        )
      )
      lead_budget = 0
      index = next_index
      continue

    text = block["text"]
    if block_type == "heading":
      chapter_count += 1
      section_count = 0
      parts.append(wrap_preview_block(render_heading(text, chapter_count), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue
    if block_type == "subheading":
      section_count += 1
      parts.append(wrap_preview_block(render_subheading(text, section_count), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue
    if is_inline_heading(blocks, index, text):
      chapter_count += 1
      section_count = 0
      parts.append(wrap_preview_block(render_heading(text, chapter_count), index, index, interactive=interactive))
      lead_budget = 0
      index += 1
      continue
    if quote_like(text):
      parts.append(wrap_preview_block(render_quote(text), index, index, interactive=interactive))
      index += 1
      continue

    parts.append(wrap_preview_block(render_paragraph(text, lead=lead_budget > 0), index, index, interactive=interactive))
    if lead_budget > 0:
      lead_budget -= 1
    index += 1
  article_inner = "".join(parts)
  return (
    '<section style="padding:26px 18px 34px;background-color:#fff8f1;'
    'border-radius:28px;">'
    f'{article_inner}'
    '</section>'
  )


def build_source_html(title: str, article_markup: str) -> str:
  return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape_text(title)}</title>
</head>
<body style="margin:0;background:#faf5ee;">
  <main style="max-width:460px;margin:0 auto;padding:28px 20px 56px;background:#ffffff;">
    {article_markup}
  </main>
</body>
</html>"""


def build_copy_page(title: str, article_markup: str) -> str:
  script = """
const article = document.getElementById("wx-article");
const status = document.getElementById("status");

function setStatus(message, isError = false) {
  status.textContent = message;
  status.style.color = isError ? "#b42318" : "#8d5b2d";
}

async function copyHtml() {
  const html = article.innerHTML;
  const plain = article.innerText;
  if (navigator.clipboard && window.ClipboardItem) {
    const item = new ClipboardItem({
      "text/html": new Blob([html], { type: "text/html" }),
      "text/plain": new Blob([plain], { type: "text/plain" }),
    });
    await navigator.clipboard.write([item]);
    return;
  }

  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(article);
  selection.removeAllRanges();
  selection.addRange(range);
  const ok = document.execCommand("copy");
  selection.removeAllRanges();
  if (!ok) throw new Error("copy failed");
}

document.getElementById("copy-rich").addEventListener("click", async () => {
  try {
    await copyHtml();
    setStatus("已复制富文本，直接切到公众号后台正文区域粘贴就行。");
  } catch (error) {
    console.error(error);
    setStatus("复制失败了，先点“选中正文”手动复制也能顶上。", true);
  }
});

document.getElementById("select-content").addEventListener("click", () => {
  const selection = window.getSelection();
  const range = document.createRange();
  range.selectNodeContents(article);
  selection.removeAllRanges();
  selection.addRange(range);
  setStatus("正文已经帮你选中了，直接复制即可。");
});
"""
  return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape_text(title)} · 自研公众号复制页</title>
  <style>
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top, rgba(255, 244, 228, 0.72), rgba(255, 244, 228, 0) 42%),
        linear-gradient(180deg, #fbf6ef 0%, #f3ebe1 100%);
      color: {PALETTE["ink"]};
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    .app {{
      width: min(1180px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 28px 0 56px;
    }}
    .toolbar {{
      position: sticky;
      top: 16px;
      z-index: 10;
      display: grid;
      gap: 12px;
      width: min(760px, 100%);
      margin: 0 auto 24px;
      padding: 0;
      background: transparent;
      backdrop-filter: blur(10px);
    }}
    h1 {{
      margin: 0;
      font-size: 28px;
      line-height: 1.5;
      font-family: "Iowan Old Style", "Songti SC", "Noto Serif SC", serif;
      font-weight: 700;
      letter-spacing: 0.4px;
    }}
    p {{
      margin: 0;
    }}
    .toolbar p {{
      color: {PALETTE["muted"]};
      font-size: 15px;
      line-height: 1.8;
    }}
    .actions {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    button {{
      appearance: none;
      border: 0;
      border-radius: 999px;
      padding: 11px 16px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      background: {PALETTE["accent"]};
      color: #fff;
    }}
    button.secondary {{
      background: rgba(255, 255, 255, 0.86);
      color: {PALETTE["accent"]};
      border: 0;
    }}
    .status {{
      min-height: 22px;
      color: {PALETTE["accent"]};
      font-size: 13px;
      line-height: 1.6;
    }}
    .preview {{
      padding: 0;
    }}
    .note {{
      width: min(460px, 100%);
      margin: 0 auto 14px;
      color: {PALETTE["muted"]};
      font-size: 13px;
      line-height: 1.7;
    }}
    #wx-article {{
      width: min(460px, 100%);
      margin: 0 auto;
      padding: 30px 20px 56px;
      background: #fff;
    }}
  </style>
</head>
<body>
  <div class="app">
    <section class="toolbar">
      <h1>自研公众号富文本复制页</h1>
      <p>这页是我自己写的新工具产的，不走仓库里原来的发布链路。点“复制富文本”后，回公众号后台正文区直接粘贴。</p>
      <div class="actions">
        <button id="copy-rich">复制富文本</button>
        <button id="select-content" class="secondary">选中正文</button>
      </div>
      <div id="status" class="status">准备好了。建议直接在浏览器里点复制，再去公众号后台粘贴。</div>
    </section>

    <section class="preview">
      <p class="note">下面这块就是将要复制进公众号后台的正文内容。</p>
      <main id="wx-article">
        {article_markup}
      </main>
    </section>
  </div>
  <script>{script}</script>
</body>
</html>"""


def build_preview_page(title: str, article_markup: str, *, interactive: bool = False) -> str:
  extra_style = ""
  extra_script = ""
  if interactive:
    extra_style = """
    .wx-preview-block {
      position: relative;
      transition: box-shadow 120ms ease, background 120ms ease, transform 120ms ease;
      cursor: pointer;
    }
    .wx-preview-block[data-block-active="1"] {
      background: rgba(248, 239, 228, 0.88);
      box-shadow: 0 0 0 3px rgba(141, 91, 45, 0.18);
      border-radius: 20px;
      transform: translateY(-1px);
    }
    """
    extra_script = """
  <script>
    (() => {
      const blocks = () => Array.from(document.querySelectorAll(".wx-preview-block"));
      let activeIndex = null;

      const setActive = (index, shouldScroll) => {
        activeIndex = index;
        for (const block of blocks()) {
          block.removeAttribute("data-block-active");
        }
        const current = document.querySelector(`.wx-preview-block[data-block-index="${index}"]`);
        if (!current) return;
        current.setAttribute("data-block-active", "1");
        if (shouldScroll) {
          current.scrollIntoView({ block: "center", behavior: "smooth" });
        }
      };

      window.focusBlock = (index) => {
        setActive(Number(index), true);
      };

      document.addEventListener("click", (event) => {
        const target = event.target.closest(".wx-preview-block");
        if (!target) return;
        const index = Number(target.getAttribute("data-block-index"));
        setActive(index, false);
        window.parent.postMessage({ source: "svg-wechat-preview", blockIndex: index }, "*");
      });

      window.addEventListener("message", (event) => {
        if (event.data?.source !== "svg-wechat-editor") return;
        if (typeof event.data.blockIndex !== "number") return;
        setActive(event.data.blockIndex, true);
      });

      if (activeIndex === null) {
        const first = document.querySelector(".wx-preview-block");
        if (first) {
          first.setAttribute("data-block-active", "1");
          activeIndex = Number(first.getAttribute("data-block-index"));
        }
      }
    })();
  </script>"""
  return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape_text(title)} · 自研预览</title>
  <style>
    body {{
      margin: 0;
      background:
        radial-gradient(circle at top, rgba(255, 245, 231, 0.78), rgba(255, 245, 231, 0) 38%),
        linear-gradient(180deg, #fbf6ef 0%, #f3ebe1 100%);
      font-family: "Iowan Old Style", "Songti SC", "Noto Serif SC", serif;
    }}
    main {{
      width: min(520px, calc(100vw - 28px));
      margin: 0 auto;
      padding: 30px 0 96px;
    }}
    .card {{
      padding: 32px 20px 60px;
      background: #fff;
    }}
    {extra_style}
  </style>
</head>
<body>
  <main>
    <section class="card">{article_markup}</section>
  </main>
  {extra_script}
</body>
</html>"""


def footer_data_url(path: Path) -> str | None:
  if not path.exists():
    return None
  mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
  return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def default_output_dir(title: str) -> Path:
  return OUTPUT_ROOT / slugify(title)


def build_payload(title: str, article: dict, *, source_url: str = "") -> dict:
  return {
    "title": title,
    "source_url": source_url,
    "article": article,
    "block_count": len(article.get("blocks", [])),
  }


def render_output_bundle(
  title: str,
  article: dict,
  *,
  interactive_preview: bool = False,
  copy_prompt_hint: bool = False,
  preview_prompt_hint: bool = True,
) -> dict[str, str]:
  article_markup = compose_article(article, show_prompt_hint=copy_prompt_hint)
  source_html = build_source_html(title, article_markup)
  copy_html = build_copy_page(title, article_markup)
  preview_markup = compose_article(article, interactive=interactive_preview, show_prompt_hint=preview_prompt_hint)
  preview_html = build_preview_page(title, preview_markup, interactive=interactive_preview)
  return {
    "article_markup": article_markup,
    "source_html": source_html,
    "copy_html": copy_html,
    "preview_html": preview_html,
  }


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="自研飞书 -> 公众号复制页生成器")
  parser.add_argument("--url", required=True, help="飞书公开文档链接")
  parser.add_argument("--output-dir", default="", help="输出目录，不传则按标题生成")
  parser.add_argument("--footer-image", default=str(DEFAULT_FOOTER), help="文末尾图，不存在则跳过")
  return parser.parse_args()


def write_outputs(output_dir: Path, payload: dict) -> None:
  output_dir.mkdir(parents=True, exist_ok=True)
  bundle = render_output_bundle(payload["title"], payload["article"])

  (output_dir / "article.json").write_text(json.dumps(payload["article"], ensure_ascii=False, indent=2), encoding="utf-8")
  (output_dir / "source.html").write_text(bundle["source_html"], encoding="utf-8")
  (output_dir / "preview.html").write_text(bundle["preview_html"], encoding="utf-8")
  (output_dir / "copy.html").write_text(bundle["copy_html"], encoding="utf-8")
  (output_dir / "index.html").write_text(bundle["copy_html"], encoding="utf-8")


def main() -> None:
  args = parse_args()
  title, raw_blocks, image_data = extract_from_feishu(args.url)
  output_dir = Path(args.output_dir).resolve() if args.output_dir else default_output_dir(title)
  article = normalize_article(title, raw_blocks, image_data, footer_data_url(Path(args.footer_image).resolve()))
  payload = build_payload(title, article, source_url=args.url)
  write_outputs(output_dir, payload)

  print(json.dumps(
    {
      "title": title,
      "output_dir": str(output_dir),
      "article_json": str(output_dir / "article.json"),
      "preview": str(output_dir / "preview.html"),
      "copy": str(output_dir / "copy.html"),
      "block_count": len(article["blocks"]),
    },
    ensure_ascii=False,
    indent=2,
  ))


if __name__ == "__main__":
  main()
