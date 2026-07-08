#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = ROOT / "已下载的推文"
BUILD_PUBLISH_PACKAGE = ROOT / "tools" / "wechat-direct-publish" / "build_wechat_publish_package.py"


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def slugify_title(title: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", " ", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "未命名文章"


class NoteHtmlParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.blocks: list[dict] = []
        self.current: dict | None = None
        self.buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = dict(attrs)
        if tag in {"h1", "h2", "p"}:
            self.current = {"tag": tag, "attrs": attrs_dict}
            self.buffer = []
        elif tag == "img":
            self.blocks.append({"tag": "img", "attrs": attrs_dict})

    def handle_startendtag(self, tag: str, attrs) -> None:
        if tag == "img":
            self.blocks.append({"tag": "img", "attrs": dict(attrs)})

    def handle_data(self, data: str) -> None:
        if self.current is not None:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current and self.current["tag"] == tag:
            self.current["text"] = "".join(self.buffer).strip()
            self.blocks.append(self.current)
            self.current = None
            self.buffer = []


def parse_note_blocks(content: str) -> list[dict]:
    parser = NoteHtmlParser()
    parser.feed(content)
    blocks = []
    for block in parser.blocks:
        if block["tag"] == "p" and not block.get("text", "").strip():
            continue
        blocks.append(block)
    return blocks


def export_images(note_id: str, blocks: list[dict], image_dir: Path) -> dict[str, str]:
    image_dir.mkdir(parents=True, exist_ok=True)
    image_map: dict[str, str] = {}
    image_index = 0
    for block in blocks:
        if block["tag"] != "img":
            continue
        block_id = block["attrs"]["id"]
        if block_id in image_map:
            continue
        image_index += 1
        response = run_json([
            "wpsnote-cli",
            "read-image",
            "--note_id",
            note_id,
            "--block_id",
            block_id,
            "--json",
        ])
        data = response["data"]
        source_path = Path(data["filePath"])
        ext = source_path.suffix or ".jpg"
        dest_name = f"{image_index:03d}{ext.lower()}"
        dest_path = image_dir / dest_name
        shutil.copy2(source_path, dest_path)
        image_map[block_id] = f"./图片素材/{dest_name}"
    return image_map


EMPHASIS_KEYWORDS = [
    "停不下来",
    "更轻松",
    "默认",
    "7×24 小时",
    "OpenClaw",
    "Vibe coding",
    "Agent",
    "能力边界",
    "工作边界",
    "焦虑边界",
    "时间边界",
    "更自由",
]


def stylize_text(text: str, max_hits: int = 2) -> str:
    escaped = html.escape(text.strip())
    hits = 0
    for keyword in sorted(EMPHASIS_KEYWORDS, key=len, reverse=True):
        if hits >= max_hits:
            break
        escaped_keyword = html.escape(keyword)
        if escaped_keyword in escaped:
            escaped = escaped.replace(escaped_keyword, f"<strong>{escaped_keyword}</strong>", 1)
            hits += 1
    return escaped


def make_paragraph(text: str, classes: str = "") -> str:
    class_attr = f' class="{classes}"' if classes else ""
    return f"<p{class_attr}>{stylize_text(text)}</p>"


def make_highlight(text: str) -> str:
    return (
        '<div class="highlight">'
        f'<p>{stylize_text(text, max_hits=1)}</p>'
        "</div>"
    )


def make_image(image_src: str, image_index: int) -> str:
    frame_class = "poster-frame" if image_index % 3 == 0 else "single-image"
    return (
        f'<figure class="{frame_class}">'
        f'<img src="{html.escape(image_src)}" alt="文章配图" />'
        "</figure>"
    )


def make_sequence_grid(items: list[str], variant: str = "sequence") -> str:
    section_class = "sequence-grid" if variant == "sequence" else "compare-grid"
    card_class = "sequence-card" if variant == "sequence" else "compare-card"
    label_class = "sequence-index" if variant == "sequence" else "compare-index"
    cards = []
    for index, item in enumerate(items, 1):
        cards.append(
            f'<article class="{card_class}">'
            f'<span class="{label_class}">{index:02d}</span>'
            f"<p>{stylize_text(item, max_hits=1)}</p>"
            "</article>"
        )
    return f'<section class="{section_class}">{"".join(cards)}</section>'


def detect_triplet_paragraphs(items: list[dict], start: int) -> tuple[str, list[str], int] | None:
    run: list[str] = []
    index = start
    while index < len(items) and len(run) < 3:
        block = items[index]
        if block["tag"] != "p":
            break
        text = block.get("text", "").strip()
        if not text:
            break
        run.append(text)
        index += 1
    if len(run) < 3:
        return None

    if all(text.startswith("你会") for text in run[:3]):
        return ("sequence", run[:3], 3)
    if run[0].startswith("你不在线") and run[1].startswith("你睡了") and run[2].startswith("你没盯着"):
        return ("compare", run[:3], 3)
    if run[0].startswith("AI 最早带来的是") and run[1].startswith("再往后带来的是") and run[2].startswith("到了 Agent 这一步"):
        return ("compare", run[:3], 3)
    return None


def should_highlight(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if len(stripped) <= 28 and any(token in stripped for token in ["停不下来", "暂停键", "更可怕", "更复杂", "更自由"]):
        return True
    if stripped.startswith("但问题就在于") or stripped.startswith("最可怕的") or stripped.startswith("所以我现在会觉得"):
        return True
    return False


def render_flow(items: list[dict], image_map: dict[str, str], intro: bool = False) -> str:
    parts: list[str] = []
    index = 0
    paragraph_count = 0
    image_count = 0

    while index < len(items):
        block = items[index]
        tag = block["tag"]

        if tag == "p":
            text = block.get("text", "").strip()
            if not text:
                index += 1
                continue

            detected = detect_triplet_paragraphs(items, index)
            if detected:
                variant, triplet_items, consumed = detected
                parts.append(make_sequence_grid(triplet_items, variant=variant))
                paragraph_count += consumed
                index += consumed
                continue

            if should_highlight(text):
                parts.append(make_highlight(text))
            else:
                classes = []
                if paragraph_count == 0:
                    classes.append("lede")
                if intro and paragraph_count == 1:
                    classes.append("soft")
                parts.append(make_paragraph(text, " ".join(classes)))
            paragraph_count += 1
            index += 1
            continue

        if tag == "img":
            image_src = image_map.get(block["attrs"]["id"])
            if image_src:
                image_count += 1
                parts.append(make_image(image_src, image_count))
            index += 1
            continue

        index += 1

    return "\n      ".join(parts)


def build_preview_html(title: str, blocks: list[dict], image_map: dict[str, str]) -> str:
    intro_blocks: list[dict] = []
    sections: list[tuple[str, list[dict]]] = []
    current_section_title: str | None = None
    current_section_blocks: list[dict] = []

    for block in blocks:
        tag = block["tag"]
        if tag == "h1":
            continue
        if tag == "h2":
            if current_section_title is not None:
                sections.append((current_section_title, current_section_blocks))
            current_section_title = block.get("text", "").strip()
            current_section_blocks = []
            continue
        if current_section_title is None:
            intro_blocks.append(block)
        else:
            current_section_blocks.append(block)

    if current_section_title is not None:
        sections.append((current_section_title, current_section_blocks))

    intro_html = render_flow(intro_blocks, image_map, intro=True)
    section_html = []
    for section_title, section_blocks in sections:
        section_html.append(
            '<section class="section">'
            f'<div class="section-heading"><span class="heading-line"></span><h2>{html.escape(section_title)}</h2></div>'
            f"{render_flow(section_blocks, image_map)}"
            "</section>"
        )

    page_body = "\n    ".join(['<section class="intro">' + intro_html + "</section>", *section_html])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #ffffff;
      --paper: #fffdfa;
      --paper-soft: #fff6e8;
      --paper-deep: #f8ebd3;
      --ink: #2e221a;
      --text: #4d4036;
      --muted: #7d6d60;
      --accent: #d88a18;
      --accent-deep: #9e5d0c;
      --accent-soft: #f7e4be;
      --line: #e7d8c0;
      --shadow: rgba(124, 85, 32, 0.09);
      --radius: 24px;
      --img-radius: 18px;
      --page-width: 760px;
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: "Source Han Serif SC", "Noto Serif SC", "Songti SC", "STSong", serif;
      line-height: 1.95;
    }}
    main {{
      width: min(var(--page-width), calc(100vw - 28px));
      margin: 0 auto;
      padding: 38px 0 90px;
    }}
    h1, h2, p, figure, blockquote {{ margin: 0; }}
    strong {{
      color: var(--accent-deep);
      font-weight: 700;
    }}
    .hero-note, .section-heading {{
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    .hero {{
      position: relative;
      padding: 12px 0 34px;
      border-bottom: 1px solid var(--line);
    }}
    .hero::before {{
      content: "";
      position: absolute;
      inset: 0 0 auto auto;
      width: 180px;
      height: 180px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(247, 228, 190, 0.7) 0%, rgba(247, 228, 190, 0) 72%);
      transform: translate(26%, -18%);
      pointer-events: none;
    }}
    .hero-note {{
      display: inline-block;
      padding: 6px 0;
      border-bottom: 1px solid var(--line);
      color: var(--accent-deep);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
    }}
    h1 {{
      position: relative;
      z-index: 1;
      margin-top: 22px;
      color: var(--ink);
      font-size: clamp(36px, 6vw, 58px);
      line-height: 1.18;
      letter-spacing: 0.01em;
    }}
    .accent-line {{
      width: 96px;
      height: 4px;
      margin-top: 22px;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent) 0%, #efb34f 100%);
      box-shadow: 0 10px 24px rgba(216, 138, 24, 0.18);
    }}
    .hero-tail {{
      margin-top: 18px;
      max-width: 600px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.9;
    }}
    .intro, .section {{
      display: grid;
      gap: 16px;
    }}
    .intro {{
      margin-top: 26px;
    }}
    .section {{
      margin-top: 62px;
    }}
    .section-heading {{
      display: grid;
      gap: 12px;
      margin-bottom: 8px;
    }}
    .heading-line {{
      width: 58px;
      height: 1px;
      background: var(--accent);
      opacity: 0.8;
    }}
    h2 {{
      color: var(--ink);
      font-size: clamp(28px, 4.8vw, 38px);
      line-height: 1.35;
    }}
    p {{
      font-size: 18px;
      line-height: 1.95;
    }}
    p.lede {{
      color: var(--ink);
      font-size: 21px;
      line-height: 1.9;
    }}
    p.soft {{
      color: var(--muted);
    }}
    .highlight {{
      margin: 10px 0 2px;
      padding: 18px 20px;
      border-left: 4px solid var(--accent);
      border-radius: 0 18px 18px 0;
      background: linear-gradient(180deg, var(--paper-soft) 0%, #fffaf1 100%);
      box-shadow: 0 14px 28px var(--shadow);
    }}
    .highlight p {{
      color: var(--ink);
      font-size: 18px;
    }}
    .sequence-grid,
    .compare-grid {{
      margin: 12px 0 6px;
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }}
    .sequence-card,
    .compare-card {{
      min-height: 100%;
      padding: 16px 16px 18px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(255,249,239,0.94) 100%);
      box-shadow: 0 14px 26px var(--shadow);
    }}
    .sequence-index,
    .compare-index {{
      display: inline-block;
      margin-bottom: 12px;
      color: var(--accent-deep);
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.12em;
    }}
    .sequence-card p,
    .compare-card p {{
      color: var(--ink);
      font-size: 16px;
      line-height: 1.8;
    }}
    .single-image,
    .poster-frame {{
      margin-top: 8px;
      padding: 4px;
      border: 1px solid var(--line);
      border-radius: 22px;
      background: linear-gradient(180deg, #fffdfa 0%, #fcf4e8 100%);
      box-shadow: 0 14px 30px var(--shadow);
    }}
    .poster-frame {{
      padding: 6px;
      border-radius: 20px;
      background: linear-gradient(180deg, #fff9ef 0%, #f9edd8 100%);
    }}
    .single-image img,
    .poster-frame img {{
      display: block;
      width: 100%;
      height: auto;
      border-radius: var(--img-radius);
    }}
    @media (max-width: 760px) {{
      .sequence-grid,
      .compare-grid {{
        grid-template-columns: 1fr;
      }}
    }}
    @media (max-width: 640px) {{
      main {{
        width: calc(100vw - 24px);
        padding-top: 30px;
      }}
      h1 {{
        font-size: 40px;
      }}
      p {{
        font-size: 16px;
      }}
      p.lede {{
        font-size: 19px;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header class="hero">
      <span class="hero-note">Essay / AI / Work</span>
      <h1>{html.escape(title)}</h1>
      <div class="accent-line"></div>
      <p class="hero-tail">能力越来越强，边界却越来越薄。最麻烦的不是 AI 让人变强，而是它让人越来越难停下来。</p>
    </header>
    {page_body}
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="从 WPS 笔记直接生成公众号排版预览页。")
    parser.add_argument("--note-id", required=True, help="WPS 笔记 ID")
    parser.add_argument("--note-json", help="提前导出的 note.json，避免在子进程里直接调用 wpsnote-cli read")
    parser.add_argument("--image-map-json", help="提前导出的 image_map.json，避免在子进程里直接调用 wpsnote-cli read-image")
    args = parser.parse_args()

    if args.note_json:
        note = json.loads(Path(args.note_json).read_text(encoding="utf-8"))["data"]
    else:
        note = run_json(["wpsnote-cli", "read", "--note_id", args.note_id, "--json"])["data"]
    title = note["title"]
    blocks = parse_note_blocks(note["content"])

    output_dir = OUTPUT_ROOT / f"{slugify_title(title)}_wps_{args.note_id}"
    image_dir = output_dir / "图片素材"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.image_map_json:
        image_map = json.loads(Path(args.image_map_json).read_text(encoding="utf-8"))
    else:
        image_map = export_images(args.note_id, blocks, image_dir)
    preview_html = build_preview_html(title, blocks, image_map)

    preview_path = output_dir / "公众号排版预览.html"
    preview_path.write_text(preview_html, encoding="utf-8")

    meta = {
      "note_id": args.note_id,
      "title": title,
      "output_dir": str(output_dir),
      "preview_html": str(preview_path),
      "images_exported": len(image_map),
    }
    (output_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OUTPUT_DIR={output_dir}")
    print(f"PREVIEW_HTML={preview_path}")
    print(f"IMAGES={len(image_map)}")


if __name__ == "__main__":
    main()
