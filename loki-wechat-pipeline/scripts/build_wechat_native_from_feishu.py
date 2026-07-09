#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FOOTER = ROOT / "签名图.png"
OUTPUT_ROOT = ROOT / "已下载的推文"

COLORS = {
    "ink": "#221d18",
    "text": "#4a4238",
    "muted": "#7b7066",
    "accent": "#9c642c",
    "accent_soft": "#fbf6ef",
    "line": "#ead9c4",
}

EMPHASIS_KEYWORDS = [
    "OpenClaw",
    "Skill",
    "API",
    "token",
    "会员",
    "普通人",
    "新手友好",
]

EMPHASIS_HINTS = (
    "本质",
    "关键",
    "核心",
    "重点",
    "前提",
    "麻烦",
    "问题",
    "门槛",
    "刚需",
    "值不值得",
    "新手友好",
    "普通人",
    "长期订阅",
)

EMPHASIS_STOPWORDS = {
    "这个",
    "那个",
    "这里",
    "然后",
    "其实",
    "就是",
    "真的",
    "当然",
    "还有",
    "如果",
    "因为",
    "所以",
    "要求",
    "页面主题",
    "输出要求",
    "技术要求",
    "目标气质",
    "视觉要求",
}

PROMPT_ROLE_PREFIXES = (
    "你现在是一位",
    "你是一名",
    "你是一位",
    "请帮我",
    "请你",
    "请围绕",
    "请为我",
    "请直接",
)

PROMPT_FIELD_MARKERS = {
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

PROMPT_RESUME_MARKERS = (
    "（此处有视频）",
    "我觉得颜色有点太AI",
    "这个方案的输出也有7000字",
    "然后再看看大家都很关心的生图",
    "真正让我眼前一亮的",
    "想看全文的后台发",
    "直接看效果",
)

INLINE_HEADING_STOPWORDS = {
    "但前提是",
    "这也是我今天想要写这篇的原因",
    "当然，你要是问我",
    "然后问题就来了",
    "这次升级的目标不是",
}


def escape_text(text: str) -> str:
    return html.escape(text)


def clean_line(text: str) -> str:
    return text.replace("\u200b", "").replace("\ufeff", "").strip()


def normalize_fragment(text: str) -> str:
    return re.sub(r"\s+", " ", clean_line(text)).strip("，。！？；：、（）()[]【】 ")


def push_unique_candidate(candidates: list[tuple[int, str]], fragment: str, score: int) -> None:
    cleaned = normalize_fragment(fragment)
    if not cleaned or len(cleaned) < 2 or len(cleaned) > 24:
        return
    if cleaned in EMPHASIS_STOPWORDS:
        return
    if any(cleaned in existing or existing in cleaned for _, existing in candidates):
        return
    candidates.append((score, cleaned))


def pick_emphasis_phrases(text: str, max_hits: int = 2) -> list[str]:
    candidates: list[tuple[int, str]] = []

    for fragment in re.findall(r"[“\"《【](.{2,24}?)[”\"》】]", text):
        push_unique_candidate(candidates, fragment, 5)

    for fragment in re.findall(r"\b[A-Za-z][A-Za-z0-9.+#/_-]*(?:\s+[A-Za-z0-9.+#/_-]+){0,3}", text):
        if any(char.isupper() for char in fragment) or any(char.isdigit() for char in fragment) or len(fragment) <= 5:
            push_unique_candidate(candidates, fragment, 4)

    for clause in re.split(r"[，。！？；：]", text):
        normalized = normalize_fragment(clause)
        if not 4 <= len(normalized) <= 18:
            continue
        score = 0
        if any(hint in normalized for hint in EMPHASIS_HINTS):
            score += 3
        if normalized.startswith(("不是", "就是", "真正", "关键", "核心", "重点", "最好", "一定", "别", "不要", "先")):
            score += 2
        if any(char.isalpha() for char in normalized) or any(char.isdigit() for char in normalized):
            score += 2
        if normalized.endswith(("刚需", "麻烦", "门槛", "问题", "入口", "答案", "差别", "选择", "风险", "建议")):
            score += 2
        if score >= 3:
            push_unique_candidate(candidates, normalized, score)

    for keyword in sorted(EMPHASIS_KEYWORDS, key=len, reverse=True):
        if keyword in text:
            push_unique_candidate(candidates, keyword, 3)

    ranked = sorted(candidates, key=lambda item: (-item[0], -len(item[1])))
    return [fragment for _, fragment in ranked[: max_hits * 2]]


def stylize_text(text: str, max_hits: int = 2) -> str:
    escaped = escape_text(text)
    hits = 0
    for keyword in pick_emphasis_phrases(text, max_hits=max_hits):
        if hits >= max_hits:
            break
        needle = html.escape(keyword)
        if needle in escaped:
            escaped = escaped.replace(
                needle,
                f'<strong style="color:{COLORS["accent"]};font-weight:700;">{needle}</strong>',
                1,
            )
            hits += 1
    return escaped


def p_html(text: str, *, size: int = 17, color: str | None = None, margin: str = "0 0 16px", weight: int = 400) -> str:
    use_color = color or COLORS["text"]
    return (
        f'<p style="margin:{margin};color:{use_color};font-size:{size}px;'
        f'line-height:1.92;font-weight:{weight};">{stylize_text(text)}</p>'
    )


def heading_html(text: str) -> list[str]:
    return [
        f'<p style="margin:0 0 20px;color:{COLORS["ink"]};font-size:30px;line-height:1.35;font-weight:700;">{escape_text(text)}</p>',
    ]


def quote_html(text: str) -> str:
    return (
        f'<p style="margin:18px 0 22px;padding-left:14px;border-left:3px solid {COLORS["line"]};'
        f'color:{COLORS["ink"]};font-size:18px;line-height:1.9;font-weight:600;">{stylize_text(text, max_hits=1)}</p>'
    )


def wechat_meta_html(text: str) -> str:
    return (
        f'<p style="margin:0 0 18px;color:{COLORS["muted"]};font-size:12px;line-height:1.6;'
        f'letter-spacing:0.8px;">{escape_text(text)}</p>'
    )


def wechat_heading_html(text: str) -> str:
    return (
        f'<p style="margin:34px 0 10px;">'
        f'<span style="display:inline-block;width:28px;height:2px;background:{COLORS["accent"]};"></span>'
        f'</p>'
        f'<p style="margin:0 0 18px;color:{COLORS["ink"]};font-size:25px;line-height:1.38;'
        f'font-weight:700;">{escape_text(text)}</p>'
    )


def wechat_emphasis_html(text: str) -> str:
    return (
        f'<p style="margin:0 0 17px;color:{COLORS["ink"]};font-size:16px;line-height:1.92;'
        f'font-weight:400;"><strong style="color:{COLORS["ink"]};font-weight:700;">{escape_text(text)}</strong></p>'
    )


def wechat_paragraph_html(text: str, *, lead: bool = False, muted: bool = False) -> str:
    color = COLORS["muted"] if muted else COLORS["ink"] if lead else COLORS["text"]
    size = 18 if lead else 16
    weight = 600 if lead else 400
    margin = "0 0 18px" if lead else "0 0 17px"
    return (
        f'<p style="margin:{margin};color:{color};font-size:{size}px;line-height:1.92;'
        f'font-weight:{weight};">{stylize_text(text)}</p>'
    )


def wechat_quote_html(text: str) -> str:
    return (
        f'<table style="width:100%;margin:16px 0 20px;border-collapse:collapse;">'
        f'<tbody><tr><td style="padding:0 0 0 14px;border-left:3px solid {COLORS["accent"]};'
        f'color:{COLORS["ink"]};font-size:17px;line-height:1.9;font-weight:600;">'
        f'{stylize_text(text, max_hits=1)}</td></tr></tbody></table>'
    )


def wrap_wechat_section_html(inner_html: str) -> str:
    return (
        f'<table style="width:100%;border-collapse:collapse;margin:0 0 18px;">'
        f'<tbody><tr><td style="padding:0;background:#ffffff;">{inner_html}</td></tr></tbody></table>'
    )


def relative_web_path(from_dir: Path, target: Path) -> str:
    return Path(os.path.relpath(str(Path(target).resolve()), str(Path(from_dir).resolve()))).as_posix()


def title_case_safe(text: str) -> str:
    cleaned = clean_line(text).replace("\u200b", "").replace("\u200c", "").replace("\u200d", "").replace("\u2060", "")
    return cleaned.replace("\xa0", " ").strip()

def slugify_title(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', " ", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "未命名文章"


def normalize_lines(lines: list[str]) -> list[str]:
    return [line for line in (clean_line(x) for x in lines) if line]


def remove_repeated_sequence(lines: list[str], sequence: list[str]) -> list[str]:
    if not sequence:
        return lines
    out: list[str] = []
    i = 0
    n = len(sequence)
    while i < len(lines):
        if lines[i:i + n] == sequence:
            i += n
            continue
        out.append(lines[i])
        i += 1
    return out


def compress_repeated_blocks(lines: list[str], min_match: int = 4, max_match: int = 28) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        best = 0
        max_size = min(max_match, len(lines) - i, len(out))
        for size in range(max_size, min_match - 1, -1):
            block = lines[i:i + size]
            found = False
            for start in range(0, len(out) - size + 1):
                if out[start:start + size] == block:
                    found = True
                    break
            if found:
                best = size
                break
        if best:
            i += best
            continue
        out.append(lines[i])
        i += 1
    return out


def normalize_block_text(text: str) -> str:
    return re.sub(r"\s+", " ", title_case_safe(text))


def prompt_line_score(text: str) -> int:
    normalized = normalize_block_text(text)
    if not normalized:
        return -10
    score = 0
    if any(normalized.startswith(prefix) for prefix in PROMPT_ROLE_PREFIXES):
        score += 6
    if normalized in PROMPT_FIELD_MARKERS or normalized.endswith("："):
        score += 4
    if re.fullmatch(r"\d+\s*[、.．]?\s*\S+", normalized):
        score += 3
    if any(token in normalized for token in ("HTML", "CSS", "JavaScript", "index.html", "输出", "生成", "设计", "项目", "课程", "页面", "视觉", "用户画像", "商业模式")):
        score += 2
    if len(normalized) <= 18:
        score += 1
    if any(marker in normalized for marker in PROMPT_RESUME_MARKERS):
        score -= 8
    if normalized.endswith(("。", "！", "？", "~")) and len(normalized) > 22 and not normalized.endswith("："):
        score -= 1
    return score


def has_prompt_context(blocks: list[dict], start_index: int) -> bool:
    score_total = 0
    strong_hits = 0
    field_hits = 0
    for block in blocks[start_index:start_index + 10]:
        if block["type"] == "image":
            continue
        text = normalize_block_text(block.get("text", ""))
        if not text:
            continue
        score = prompt_line_score(text)
        score_total += max(score, 0)
        if score >= 4:
            strong_hits += 1
        if text in PROMPT_FIELD_MARKERS or text.endswith("："):
            field_hits += 1
    return score_total >= 12 and (strong_hits >= 2 or field_hits >= 2)


def looks_like_resume_narration(text: str) -> bool:
    normalized = normalize_block_text(text)
    if any(marker in normalized for marker in PROMPT_RESUME_MARKERS):
        return True
    return (
        len(normalized) > 24
        and any(token in normalized for token in ("我觉得", "这次", "真正", "然后", "后台发", "直接看效果", "大家都很关心"))
        and prompt_line_score(normalized) <= 0
    )


def derive_prompt_label(lines: list[str]) -> str:
    joined = " ".join(lines[:12])
    if any(token in joined for token in ("官网", "落地页", "首页", "网页应用")):
        return "这段官网提示词，我单拎出来看"
    if any(token in joined for token in ("课程", "训练营", "项目方案", "用户画像", "商业模式")):
        return "这段课程方案提示词"
    if any(token in joined for token in ("修仙", "剑宗", "首席弟子", "正道大会", "玄清宗", "小说")):
        return "这段剧情提示词"
    if any(token in joined for token in ("生图", "海报", "插画", "视觉")):
        return "这段生图提示词"
    if any(token in joined for token in ("HTML", "CSS", "JavaScript", "代码", "index.html")):
        return "这段网页提示词"
    return "这段提示词，我单拎出来了"


def wechat_prompt_card_html(label: str, text: str) -> str:
    line_count = len([line for line in text.splitlines() if line.strip()])
    is_long = line_count >= 10 or len(text) >= 360
    scroll_style = "max-height:288px;overflow-y:auto;-webkit-overflow-scrolling:touch;" if is_long else ""
    hint = "长提示词已折成固定高度，可上下滑动查看。" if is_long else "这段提示词我保留成了可以直接复制的代码块。"
    return (
        '<table style="width:100%;border-collapse:collapse;margin:20px 0 24px;">'
        '<tbody><tr><td style="padding:0;">'
        f'<div style="padding:18px 18px 16px;border:1px solid {COLORS["line"]};border-radius:24px;'
        'background:linear-gradient(180deg,#fdf9f3 0%,#fffdf9 100%);">'
        f'<p style="margin:0 0 6px;color:{COLORS["accent"]};font-size:12px;line-height:1.4;'
        'font-weight:700;letter-spacing:1.2px;">PROMPT</p>'
        f'<p style="margin:0 0 12px;color:{COLORS["ink"]};font-size:18px;line-height:1.6;'
        f'font-weight:600;">{escape_text(label)}</p>'
        f'<div style="padding:14px 15px;border-radius:18px;border:1px solid #ede2d5;background:#fffdfa;'
        f'box-shadow:inset 0 1px 0 rgba(255,255,255,0.72);{scroll_style}">'
        "<pre style=\"margin:0;white-space:pre-wrap;font-family:'SFMono-Regular','JetBrains Mono','Menlo','PingFang SC',monospace;"
        f'font-size:13px;line-height:1.75;color:#3b322b;">{escape_text(text)}</pre>'
        "</div>"
        f'<p style="margin:10px 0 0;color:{COLORS["muted"]};font-size:12px;line-height:1.6;">{escape_text(hint)}</p>'
        "</div></td></tr></tbody></table>"
    )


def collect_prompt_block(blocks: list[dict], start_index: int) -> tuple[dict | None, int, list[dict]]:
    if start_index >= len(blocks):
        return None, start_index, []
    first = blocks[start_index]
    if first["type"] != "text":
        return None, start_index, []
    first_text = normalize_block_text(first.get("text", ""))
    if prompt_line_score(first_text) < 4 or not has_prompt_context(blocks, start_index):
        return None, start_index, []

    lines: list[str] = []
    images: list[dict] = []
    promptish_lines = 0
    index = start_index

    while index < len(blocks):
        block = blocks[index]
        if block["type"] == "heading" and lines:
            break
        if block["type"] == "image":
            if lines and has_prompt_context(blocks, index + 1):
                images.append(block)
                index += 1
                continue
            if lines:
                break
            return None, start_index, []

        text = normalize_block_text(block.get("text", ""))
        if not text:
            index += 1
            continue
        if looks_like_resume_narration(text):
            break

        score = prompt_line_score(text)
        if lines and score <= 0 and len(text) > 24 and not text.endswith("："):
            break

        lines.append(text)
        if score >= 3:
            promptish_lines += 1
        index += 1

    if len(lines) < 4 or promptish_lines < 2:
        return None, start_index, []

    return {"type": "prompt", "label": derive_prompt_label(lines), "text": "\n".join(lines)}, index, images


def is_real_section_heading(blocks: list[dict], index: int, text: str) -> bool:
    normalized = normalize_block_text(text)
    if len(normalized) > 24:
        return False
    if any(mark in normalized for mark in ['“', '”', '"', '《', '》']):
        return False
    if normalized.endswith(("老师", "佬")):
        return False
    prev_text = ""
    next_text = ""
    prev_type = None
    next_type = None
    if index > 0:
        prev = blocks[index - 1]
        prev_type = prev["type"]
        prev_text = normalize_block_text(prev.get("text", ""))
    if index + 1 < len(blocks):
        nxt = blocks[index + 1]
        next_type = nxt["type"]
        next_text = normalize_block_text(nxt.get("text", ""))

    if next_text.startswith(("，", "。", "；", "：", "）", "、")):
        return False
    if prev_type == "heading" or next_type == "heading":
        return False
    if prev_type == "text" and prev_text and not re.search(r"[。！？!?：:]$", prev_text):
        return False
    if prev_type == "text" and prev_text.endswith(("的", "了", "是", "就", "还", "把", "被", "与", "和", "及", "先")):
        return False
    if next_type == "text" and next_text.startswith(("，", "也", "而", "但", "所以", "因为")):
        return False
    return True


def looks_like_inline_heading(blocks: list[dict], index: int, text: str) -> bool:
    normalized = normalize_block_text(text)
    if not 6 <= len(normalized) <= 22:
        return False
    if normalized.endswith(("。", "！", "？", "；", "：", "~")):
        return False
    if normalized in INLINE_HEADING_STOPWORDS:
        return False
    if normalized in PROMPT_FIELD_MARKERS or any(normalized.startswith(prefix) for prefix in PROMPT_ROLE_PREFIXES):
        return False

    prev = blocks[index - 1] if index > 0 else None
    nxt = blocks[index + 1] if index + 1 < len(blocks) else None
    prev_text = normalize_block_text(prev.get("text", "")) if prev else ""
    next_text = normalize_block_text(nxt.get("text", "")) if nxt else ""

    if prev and prev["type"] == "text" and prev_text and not re.search(r"[。！？!?：:]$", prev_text):
        return False
    if nxt and nxt["type"] == "text" and next_text.startswith(("，", "也", "而", "但", "所以", "因为")):
        return False
    if nxt and nxt["type"] == "text" and len(next_text) < 8:
        return False
    if not any(token in normalized for token in ("问题", "麻烦", "门槛", "原因", "重点", "关键", "建议", "选择", "不足", "体验", "平台", "模型", "朋友", "普通人", "新手")) and len(normalized) < 10:
        return False
    return True


def should_render_quote(text: str) -> bool:
    return len(text) <= 28 and any(token in text for token in ["普通人", "太多了", "很麻烦", "新手友好", "你到底该用哪个"])


def canonicalize_image_src(src: str) -> str:
    if not src:
        return src
    parts = urlsplit(src)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k not in {"width", "height", "policy", "format"}]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def should_keep_image(image_info: dict) -> bool:
    width = int(image_info.get("width", 0) or 0)
    height = int(image_info.get("height", 0) or 0)
    if width <= 0 or height <= 0:
        return True
    ratio = width / height
    if width < 220 or height < 120:
        return False
    if ratio > 3.2 or ratio < 0.45:
        return False
    return True


def derive_image_display_width(width: int, height: int) -> str:
    if width > 0 and height > 0:
        ratio = width / height
        if ratio >= 1.4:
            return "92%"
        if ratio <= 0.82:
            return "62%"
        if ratio <= 1.05:
            return "70%"
    return "78%"


def dedupe_sequence_blocks(blocks: list[dict], window: int = 80) -> list[dict]:
    out: list[dict] = []
    recent: list[str] = []
    for block in blocks:
        if block["type"] == "image":
            src = block.get("src") or block.get("file")
            if src and any((item.get("src") or item.get("file")) == src for item in out if item["type"] == "image"):
                continue
            out.append(block)
            continue

        text = normalize_block_text(block.get("text", ""))
        if not text:
            continue
        token = f"{block['type']}::{text}"
        if token in recent[-window:]:
            continue
        recent.append(token)
        item = dict(block)
        item["text"] = text
        out.append(item)
    return out


def split_feishu_payload(payload: dict) -> tuple[str, list[str], list[str], str]:
    lines = normalize_lines(payload["text_lines"])
    title = clean_line(payload["title"]) or lines[0]
    title_positions = [i for i, line in enumerate(lines) if line == title]

    def has_nearby_date(index: int) -> bool:
        for offset in range(1, 4):
            if index + offset < len(lines) and re.search(r"\d+月\d+日", lines[index + offset]):
                return True
        return False

    content_title_index = next(
        (idx for idx in title_positions[1:] if has_nearby_date(idx)),
        title_positions[1] if len(title_positions) > 1 else (title_positions[0] if title_positions else 0),
    )
    date_text = ""
    date_idx = None
    for offset in range(1, 4):
        idx = content_title_index + offset
        if idx < len(lines) and re.search(r"\d+月\d+日", lines[idx]):
            date_idx = idx
            date_text = lines[idx]
            break
    toc_lines = [line for line in lines[:content_title_index] if line != title and not re.search(r"\d+月\d+日", line)]
    body_start = (date_idx + 1) if date_idx is not None else (content_title_index + 1)
    body_lines = lines[body_start:]
    repeated_preamble = [title, *toc_lines]
    body_lines = remove_repeated_sequence(body_lines, repeated_preamble)
    body_lines = [line for line in body_lines if line not in {title, date_text, "❗"}]
    body_lines = compress_repeated_blocks(body_lines)
    noise_lines = {
        "💡",
        "你是一名产品经理和教育行业顾问。",
        "请帮我设计一个AI课程项目方案。",
        "项目背景：",
        "输出结构：",
        "1 项目目标",
        "2 用户画像",
        "3 课程模块设计",
        "4 学习成果形式",
        "5 商业模式",
        "6 潜在风险",
        "要求：",
        "结构清晰",
        "逻辑完整",
        "适合真实项目",
    }
    body_lines = [line for line in body_lines if line not in noise_lines]
    cutoff_markers = [
        "（此处有视频）",
        "输出要求：",
        "直接输出完整 HTML 代码",
        "视觉要求：",
        "有未来感，但不要廉价赛博朋克",
        "页面主题：",
        "目标气质：",
        "你现在是一位世界级前端设计工程师",
        "技术要求：",
        "代码质量要求：",
        "页面滚动时要有细腻动效",
        "燕无晦",
        "太虚剑宗",
        "霜眠居",
        "我已经不在便利店工作了。",
        "你现在是一位非常成熟的中文玄幻修仙小说作者",
        "你是一名产品经理和教育行业顾问。",
        "请帮我设计一个AI课程项目方案。",
        "NanoBanana Pro",
    ]
    for idx, line in enumerate(body_lines):
        if any(marker in line for marker in cutoff_markers):
            body_lines = body_lines[:idx]
            break
    return title, toc_lines, body_lines, date_text


def build_ordered_blocks(payload: dict) -> tuple[str, str, list[dict]]:
    title = title_case_safe(payload.get("title", ""))
    _, toc_lines, _, _ = split_feishu_payload(payload)
    toc_heading_set = {normalize_block_text(line) for line in toc_lines}
    image_map = {}
    for item in payload.get("images", []):
        image_map[item.get("src")] = item
        image_map[item.get("src_key")] = item
        image_map[canonicalize_image_src(item.get("src", ""))] = item
    raw_blocks = dedupe_sequence_blocks(payload.get("blocks", []))
    if not raw_blocks:
        return title, "", []

    body_start = 0
    for idx, block in enumerate(raw_blocks):
        if block["type"] == "title" and normalize_block_text(block.get("text", "")) == normalize_block_text(title):
            body_start = idx
            break

    trimmed = raw_blocks[body_start:]
    date_text = ""
    if trimmed and normalize_block_text(trimmed[0].get("text", "")) == normalize_block_text(title):
        trimmed = trimmed[1:]
    if trimmed and trimmed[0]["type"] == "meta":
        date_text = trimmed[0]["text"]
        trimmed = trimmed[1:]

    out: list[dict] = []
    seen_heading_texts: set[str] = set()
    media_heading_keywords = ["Claude", "GPT", "NanoBanana", "opus", "策划案", "case"]
    media_keep_markers = [
        "（此处有视频）",
        "我觉得",
        "改了一版",
        "我简单",
        "想看全文",
        "后台发",
        "直接看效果",
        "然后再看看",
        "我为什么",
        "我最关心",
        "这次我",
        "我主要",
        "我对",
    ]
    current_media_section = False
    content_started = False
    kept_intro_image = False

    for block in trimmed:
        if block["type"] == "image":
            image_info = image_map.get(block.get("src", "")) or image_map.get(canonicalize_image_src(block.get("src", "")))
            if image_info and should_keep_image(image_info):
                if not content_started:
                    if kept_intro_image:
                        continue
                    kept_intro_image = True
                out.append(
                    {
                        "type": "image",
                        "file": image_info["file"],
                        "alt": image_info.get("alt", "文章配图"),
                        "width": int(image_info.get("width", 0) or 0),
                        "height": int(image_info.get("height", 0) or 0),
                    }
                )
            continue

        text = normalize_block_text(block.get("text", ""))
        if not text or text == date_text:
            continue
        if text == title:
            continue
        if re.fullmatch(r"[❗💡•]+", text):
            continue

        if block["type"] == "heading":
            if current_media_section and text not in toc_heading_set:
                continue
            if text in seen_heading_texts:
                continue
            seen_heading_texts.add(text)
            current_media_section = any(keyword.lower() in text.lower() for keyword in media_heading_keywords)
            out.append({"type": "heading", "text": text})
            content_started = True
            continue

        if current_media_section:
            keep_media_text = (
                any(marker in text for marker in media_keep_markers)
                or prompt_line_score(text) >= 2
                or (len(text) <= 28 and not text.endswith(("。", "！", "？", "~")) and not looks_like_resume_narration(text))
                or (len(text) <= 24 and any(keyword.lower() in text.lower() for keyword in ["Claude", "GPT", "NanoBanana"]))
            )
            if not keep_media_text:
                continue

        out.append({"type": "text", "text": text})
        content_started = True

    return title, date_text, out


def build_manifest(payload: dict, footer_image: Path) -> dict:
    title, date_text, ordered_blocks = build_ordered_blocks(payload)
    body: list[dict] = []

    if date_text:
        body.append({"type": "html", "html": wechat_meta_html(date_text)})

    lead_budget = 2
    index = 0
    while index < len(ordered_blocks):
        block = ordered_blocks[index]
        if block["type"] == "heading":
            if is_real_section_heading(ordered_blocks, index, block["text"]):
                body.append({"type": "html", "html": wechat_heading_html(block["text"])})
                lead_budget = 0
            else:
                body.append({"type": "html", "html": wechat_emphasis_html(block["text"])})
            index += 1
            continue
        if block["type"] == "image":
            body.append(block)
            index += 1
            continue

        prompt_block, next_index, prompt_images = collect_prompt_block(ordered_blocks, index)
        if prompt_block:
            body.append({"type": "html", "html": wechat_prompt_card_html(prompt_block["label"], prompt_block["text"])})
            body.extend(prompt_images)
            lead_budget = 0
            index = next_index
            continue

        text = block["text"]
        if looks_like_inline_heading(ordered_blocks, index, text):
            body.append({"type": "html", "html": wechat_heading_html(text)})
            lead_budget = 0
            index += 1
            continue
        if should_render_quote(text):
            body.append({"type": "html", "html": wechat_quote_html(text)})
            index += 1
            continue
        if lead_budget > 0:
            body.append({"type": "html", "html": wechat_paragraph_html(text, lead=True)})
            lead_budget -= 1
            index += 1
            continue
        body.append({"type": "html", "html": wechat_paragraph_html(text)})
        index += 1

    compact_body: list[dict] = []

    for block in body:
        if block["type"] == "html":
            compact_body.append(block)
            continue
        if block["type"] == "image":
            image_block = dict(block)
            file_path = Path(block["file"])
            image_block["display_width"] = "78%"
            width = int(block.get("width", 0) or 0)
            height = int(block.get("height", 0) or 0)
            if width <= 0 or height <= 0:
                for item in payload.get("images", []):
                    if Path(item.get("file", "")) == file_path:
                        width = int(item.get("width", 0) or 0)
                        height = int(item.get("height", 0) or 0)
                        break
            image_block["display_width"] = derive_image_display_width(width, height)
            compact_body.append(image_block)
            continue
        compact_body.append(block)

    return {
        "version": 1,
        "mode": "wechat-copy-native",
        "title": title,
        "author": "",
        "body": compact_body,
    }


def build_preview_html(manifest: dict) -> str:
    hero_note = "Essay / AI / Tools"
    hero_title = escape_text(manifest["title"])
    hero_meta = ""
    hero_cover = ""
    intro_parts: list[str] = []
    section_html: list[str] = []
    current_section: list[str] = []
    current_heading = ""

    def flush_section() -> None:
        nonlocal current_section, current_heading
        if not current_section:
            return
        heading_html = ""
        if current_heading:
            heading_html = (
                '<div class="section-heading">'
                f'<span class="section-tag">Section</span><h2>{escape_text(current_heading)}</h2>'
                "</div>"
            )
        section_html.append(f'<section class="section">{heading_html}{"".join(current_section)}</section>')
        current_section = []
        current_heading = ""

    image_counter = 0
    for block in manifest["body"]:
        if block["type"] == "meta":
            hero_meta = f'<p class="meta">{escape_text(block["text"])}</p>'
            continue
        if block["type"] == "image":
            image_counter += 1
            src = Path(block["file"]).as_uri()
            figure = (
                '<figure class="single-image">'
                f'<img src="{src}" alt="{html.escape(block.get("alt", ""))}" />'
                "</figure>"
            )
            if image_counter == 1 and not hero_cover:
                hero_cover = figure
            else:
                if current_heading:
                    current_section.append(figure)
                else:
                    intro_parts.append(figure)
            continue
        if block["type"] == "heading":
            flush_section()
            current_heading = block["text"]
            continue
        if block["type"] == "lead":
            target = current_section if current_heading else intro_parts
            target.append(f'<p class="lede">{escape_text(block["text"])}</p>')
            continue
        if block["type"] == "quote":
            target = current_section if current_heading else intro_parts
            target.append(f'<div class="highlight"><p>{escape_text(block["text"])}</p></div>')
            continue
        if block["type"] == "text":
            target = current_section if current_heading else intro_parts
            target.append(f'<p>{escape_text(block["text"])}</p>')
            continue
        if block.get("html"):
            target = current_section if current_heading else intro_parts
            target.append(block["html"])

    flush_section()

    body = (
        f'<header class="hero"><p class="hero-note">{hero_note}</p><h1>{hero_title}</h1>{hero_meta}{hero_cover}</header>'
        f'<section class="intro">{"".join(intro_parts)}</section>'
        + "".join(section_html)
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(manifest["title"])}</title>
  <style>
    body {{
      margin: 0;
      background: #fbf8f3;
      color: {COLORS["ink"]};
      font-family: "Iowan Old Style", "Songti SC", "Noto Serif SC", "Source Han Serif SC", serif;
    }}
    main {{
      width: min(760px, calc(100vw - 28px));
      margin: 0 auto;
      padding: 30px 0 96px;
    }}
    .hero, .intro, .section {{
      background: #fffdfa;
      border: 1px solid #efe1cf;
      border-radius: 28px;
      box-shadow: 0 10px 28px rgba(63, 37, 17, 0.06);
    }}
    .hero {{
      padding: 30px 30px 24px;
      margin-bottom: 18px;
    }}
    .intro, .section {{
      padding: 26px 30px;
      margin-bottom: 18px;
    }}
    .hero-note, .section-tag {{
      margin: 0 0 12px;
      color: {COLORS["accent"]};
      font-family: "SF Pro Display", "PingFang SC", sans-serif;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 1.4px;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 0 0 14px;
      color: {COLORS["ink"]};
      font-size: 40px;
      line-height: 1.18;
      font-weight: 700;
    }}
    h2 {{
      margin: 0 0 18px;
      color: {COLORS["ink"]};
      font-size: 30px;
      line-height: 1.28;
      font-weight: 700;
    }}
    .meta {{
      margin: 0 0 18px;
      color: {COLORS["muted"]};
      font-family: "SF Pro Display", "PingFang SC", sans-serif;
      font-size: 13px;
      line-height: 1.7;
    }}
    p {{
      margin: 0 0 16px;
      color: {COLORS["text"]};
      font-size: 19px;
      line-height: 1.9;
      font-weight: 400;
    }}
    p.lede {{
      color: {COLORS["ink"]};
      font-size: 22px;
      line-height: 1.84;
      font-weight: 600;
    }}
    .section-heading {{
      margin-bottom: 18px;
      padding-bottom: 16px;
      border-bottom: 1px solid #efe1cf;
    }}
    .highlight {{
      margin: 18px 0 22px;
      padding: 18px 18px 18px 20px;
      border-left: 4px solid {COLORS["accent"]};
      background: #fff6eb;
      border-radius: 0 20px 20px 0;
    }}
    .highlight p {{
      margin: 0;
      color: {COLORS["ink"]};
      font-size: 18px;
      font-weight: 600;
      line-height: 1.86;
    }}
    .single-image {{
      margin: 22px 0;
    }}
    .single-image img {{
      display: block;
      width: 100%;
      border-radius: 22px;
      border: 1px solid #eadac5;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>"""


def build_copy_source_html(manifest: dict, base_dir: Path) -> str:
    def image_frame_html(item: dict, *, width: str = "100%", inline: bool = False, margin_right: str = "0") -> str:
        src = relative_web_path(base_dir, Path(item["file"]))
        return (
            f'<span style="display:{"inline-block" if inline else "block"};vertical-align:top;width:{width};'
            f'max-width:100%;margin-right:{margin_right};white-space:normal;">'
            '<span style="display:block;padding:6px;border-radius:24px;border:1px solid #f1e5d8;'
            'background:#fffaf6;">'
            f'<img src="{escape_text(src)}" alt="{escape_text(item.get("alt", ""))}" '
            'style="display:block;width:100%;max-width:100%;height:auto;'
            'border-radius:18px;border:1px solid #eadac5;" />'
            "</span></span>"
        )

    def single_image_html(item: dict) -> str:
        width = item.get("display_width", "78%")
        return (
            '<table style="width:100%;border-collapse:collapse;margin:18px 0 22px;">'
            '<tbody><tr><td style="padding:0;text-align:center;">'
            f'{image_frame_html(item, width=width)}'
            '</td></tr></tbody></table>'
        )

    def gallery_card_width(item: dict) -> str:
        width = int(item.get("width", 0) or 0)
        height = int(item.get("height", 0) or 0)
        if width > 0 and height > 0:
            ratio = width / height
            if ratio >= 1.35:
                return "82%"
            if ratio <= 0.82:
                return "58%"
        return "68%"

    def scroll_gallery_html(items: list[dict]) -> str:
        cards: list[str] = []
        for idx, item in enumerate(items):
            cards.append(
                image_frame_html(
                    item,
                    width=gallery_card_width(item),
                    inline=True,
                    margin_right="12px" if idx < len(items) - 1 else "2px",
                )
            )
        return (
            '<table style="width:100%;border-collapse:collapse;margin:10px 0 24px;">'
            '<tbody><tr><td style="padding:0;">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;margin:0 4px 8px;">'
            f'<span style="color:{COLORS["accent"]};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.2px;">图组</span>'
            f'<span style="color:{COLORS["muted"]};font-size:12px;line-height:1.4;">多图可左右滑动</span>'
            "</div>"
            '<div style="overflow-x:auto;white-space:nowrap;padding:4px 2px 10px;-webkit-overflow-scrolling:touch;">'
            f'{"".join(cards)}'
            "</div></td></tr></tbody></table>"
        )

    parts: list[str] = []
    i = 0
    body = manifest["body"]
    while i < len(body):
        block = body[i]
        if block["type"] == "html":
            parts.append(block["html"])
            i += 1
            continue

        if block["type"] == "image":
            run: list[dict] = []
            while i < len(body) and body[i]["type"] == "image":
                run.append(body[i])
                i += 1

            if len(run) == 1:
                parts.append(single_image_html(run[0]))
            else:
                parts.append(scroll_gallery_html(run))
            continue

        i += 1

    content = "".join(parts)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape_text(manifest["title"])}</title>
</head>
<body style="margin:0;background:#ffffff;">
  <main style="max-width:720px;margin:0 auto;padding:24px 18px 48px;background:#ffffff;">
    {content}
  </main>
</body>
</html>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="从公开飞书提取结果生成微信公众号发布包")
    parser.add_argument("--input", required=True, help="extract_public_feishu_doc.py 生成的 feishu-extracted.json")
    parser.add_argument("--output-dir", default="", help="输出目录")
    parser.add_argument("--footer-image", default=str(DEFAULT_FOOTER))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    title = clean_line(payload["title"]) or "未命名文章"
    article_dir = Path(args.input).resolve().parent
    output_dir = Path(args.output_dir).resolve() if args.output_dir else article_dir / ".wechat-publish-package-wechat-native"
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(payload, Path(args.footer_image).resolve())
    manifest_path = output_dir / "manifest.json"
    preview_path = output_dir / "publish-preview.html"
    copy_source_path = article_dir / "公众号后台复制源.html"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    preview_path.write_text(build_preview_html(manifest), encoding="utf-8")
    copy_source_path.write_text(build_copy_source_html(manifest, article_dir), encoding="utf-8")

    print(f"TITLE={title}")
    print(f"MANIFEST={manifest_path}")
    print(f"PREVIEW={preview_path}")
    print(f"COPY_SOURCE={copy_source_path}")


if __name__ == "__main__":
    main()
