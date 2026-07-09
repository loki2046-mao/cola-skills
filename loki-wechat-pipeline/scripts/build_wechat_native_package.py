#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import re
import shlex
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FOOTER = ROOT / "签名图.png"
OUTPUT_ROOT = ROOT / "已下载的推文"

COLORS = {
    "ink": "#241f1a",
    "text": "#4a433c",
    "muted": "#786f66",
    "accent": "#b06a1f",
    "accent_deep": "#8d5317",
    "line": "#eadbc9",
    "soft": "#fbf4ea",
    "soft_warm": "#f7f3ee",
}

EMPHASIS_KEYWORDS = [
    "停不下来",
    "更轻松",
    "默认",
    "OpenClaw",
    "Vibe coding",
    "Agent",
    "能力边界",
    "工作边界",
    "焦虑边界",
    "时间边界",
    "更自由",
]


def run_json(cmd: list[str]) -> dict:
    result = subprocess.run(
        ["/bin/zsh", "-lc", shlex.join(cmd)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def slugify_title(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', " ", title)
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
    blocks: list[dict] = []
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
        image_map[block_id] = str(dest_path.resolve())
    return image_map


def build_image_map_from_dir(blocks: list[dict], image_dir: Path) -> dict[str, str]:
    files = sorted([path for path in image_dir.iterdir() if path.is_file()])
    image_blocks = [block for block in blocks if block["tag"] == "img"]
    if len(files) < len(image_blocks):
        raise SystemExit(f"图片目录里的文件数量不足：需要 {len(image_blocks)} 张，实际 {len(files)} 张")
    image_map: dict[str, str] = {}
    for block, file_path in zip(image_blocks, files):
        image_map[block["attrs"]["id"]] = str(file_path.resolve())
    return image_map


def escape_text(text: str) -> str:
    return html.escape(text.strip())


def stylize_text(text: str, max_hits: int = 2) -> str:
    escaped = escape_text(text)
    hits = 0
    for keyword in sorted(EMPHASIS_KEYWORDS, key=len, reverse=True):
        if hits >= max_hits:
            break
        escaped_keyword = html.escape(keyword)
        if escaped_keyword in escaped:
            escaped = escaped.replace(
                escaped_keyword,
                f'<strong style="color:{COLORS["accent_deep"]};font-weight:700;">{escaped_keyword}</strong>',
                1,
            )
            hits += 1
    return escaped


def p_html(text: str, *, color: str | None = None, size: int = 17, margin: str = "0 0 16px",
           weight: int = 400, line_height: float = 1.92, max_hits: int = 2) -> str:
    use_color = color or COLORS["text"]
    return (
        f'<p style="margin:{margin};color:{use_color};font-size:{size}px;'
        f'line-height:{line_height};font-weight:{weight};">{stylize_text(text, max_hits=max_hits)}</p>'
    )


def meta_tags_html(text: str) -> str:
    tags = [token for token in text.split() if token.startswith("#")]
    pills = []
    for tag in tags:
        pills.append(
            f'<span style="display:inline-block;margin:0 8px 8px 0;padding:6px 10px;'
            f'border:1px solid {COLORS["line"]};border-radius:999px;background:#fff;'
            f'color:{COLORS["accent_deep"]};font-size:12px;line-height:1.2;font-weight:700;">'
            f"{escape_text(tag)}</span>"
        )
    if not pills:
        return ""
    return f'<p style="margin:0 0 18px;">{"".join(pills)}</p>'


def heading_html(text: str) -> list[str]:
    return [
        f'<p style="margin:48px 0 12px;"><span style="display:inline-block;width:46px;border-top:2px solid {COLORS["accent"]};font-size:0;line-height:0;">&nbsp;</span></p>',
        f'<p style="margin:0 0 20px;color:{COLORS["ink"]};font-size:28px;line-height:1.42;font-weight:700;">{escape_text(text)}</p>',
    ]


def quote_html(text: str) -> str:
    return (
        f'<table style="width:100%;margin:14px 0 18px;border-collapse:separate;border-spacing:0;">'
        f'<tbody><tr><td style="padding:14px 16px;border-left:4px solid {COLORS["accent"]};'
        f'border-radius:0 14px 14px 0;background:{COLORS["soft"]};color:{COLORS["ink"]};'
        f'font-size:17px;line-height:1.88;">{stylize_text(text, max_hits=1)}</td></tr></tbody></table>'
    )


def three_col_table_html(items: list[str]) -> str:
    cells = []
    for index, item in enumerate(items, 1):
        padding = "0 6px"
        if index == 1:
            padding = "0 6px 0 0"
        elif index == len(items):
            padding = "0 0 0 6px"
        cells.append(
            f'<td style="width:33.33%;padding:{padding};vertical-align:top;">'
            f'<p style="margin:0 0 8px;color:{COLORS["accent_deep"]};font-size:11px;line-height:1.5;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">{index:02d}</p>'
            f'<p style="margin:0;padding:14px 14px 15px;border:1px solid {COLORS["line"]};border-radius:18px;'
            f'background:#fff;color:{COLORS["ink"]};font-size:16px;line-height:1.82;">{stylize_text(item, max_hits=1)}</p>'
            "</td>"
        )
    return (
        '<table style="width:100%;margin:16px 0 18px;border-collapse:separate;border-spacing:0;table-layout:fixed;">'
        f'<tbody><tr>{"".join(cells)}</tr></tbody></table>'
    )


def should_quote(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if stripped.startswith(("但问题就在于", "最可怕的", "这才是最近让我觉得")):
        return True
    if len(stripped) <= 24 and any(token in stripped for token in ["停不下来", "更复杂", "更可怕", "更自由"]):
        return True
    return False


def detect_triplet_paragraphs(items: list[dict], start: int) -> tuple[list[str], int] | None:
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
        return run[:3], 3
    if run[0].startswith("你不在线") and run[1].startswith("你睡了") and run[2].startswith("你没盯着"):
        return run[:3], 3
    if run[0].startswith("AI 最早带来的是") and run[1].startswith("再往后带来的是") and run[2].startswith("到了 Agent 这一步"):
        return run[:3], 3
    return None


def build_manifest_from_blocks(title: str, blocks: list[dict], image_map: dict[str, str], footer_image: Path) -> dict:
    body: list[dict] = []
    intro_index = 0
    index = 0
    title_inserted = False
    while index < len(blocks):
        block = blocks[index]
        tag = block["tag"]
        text = block.get("text", "").strip()

        if tag == "h1":
            index += 1
            continue

        if not title_inserted:
            body.append({
                "type": "html",
                "html": f'<p style="margin:0 0 10px;color:{COLORS["muted"]};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;">Essay / AI / Work</p>'
            })
            body.append({
                "type": "html",
                "html": f'<p style="margin:0 0 18px;color:{COLORS["ink"]};font-size:34px;line-height:1.22;font-weight:700;">{escape_text(title)}</p>'
            })
            body.append({
                "type": "html",
                "html": f'<p style="margin:0 0 20px;color:{COLORS["muted"]};font-size:15px;line-height:1.86;">能力越来越强，边界却越来越薄。最麻烦的不是 AI 让人变强，而是它让人越来越难停下来。</p>'
            })
            title_inserted = True

        if tag == "p" and text.startswith("#"):
            html_block = meta_tags_html(text)
            if html_block:
                body.append({"type": "html", "html": html_block})
            index += 1
            continue

        if tag == "h2":
            for html_block in heading_html(text):
                body.append({"type": "html", "html": html_block})
            index += 1
            continue

        if tag == "img":
            file_path = image_map.get(block["attrs"]["id"])
            if file_path:
                body.append({"type": "image", "file": file_path, "alt": "文章配图"})
            index += 1
            continue

        if tag == "p":
            triplet = detect_triplet_paragraphs(blocks, index)
            if triplet:
                items, consumed = triplet
                body.append({"type": "html", "html": three_col_table_html(items)})
                index += consumed
                continue

            if should_quote(text):
                body.append({"type": "html", "html": quote_html(text)})
            else:
                intro_index += 1
                if intro_index == 1:
                    body.append({"type": "html", "html": p_html(text, color=COLORS["ink"], size=20, weight=600, margin="0 0 18px", max_hits=1)})
                elif intro_index == 2:
                    body.append({"type": "html", "html": p_html(text, color=COLORS["muted"], size=17, margin="0 0 16px", max_hits=1)})
                else:
                    body.append({"type": "html", "html": p_html(text)})
            index += 1
            continue

        index += 1

    if footer_image.exists():
        body.append({"type": "image", "file": str(footer_image.resolve()), "alt": "关注引导图"})

    return {
        "version": 1,
        "mode": "native-editable",
        "title": title,
        "author": "",
        "body": body,
    }


def build_preview_html(manifest: dict) -> str:
    parts: list[str] = []
    for block in manifest["body"]:
        if block["type"] == "html":
            parts.append(block["html"])
        else:
            src = Path(block["file"]).as_uri()
            parts.append(
                f'<figure style="margin:24px 0;"><img src="{src}" alt="{html.escape(block.get("alt", ""))}" '
                'style="display:block;width:100%;border-radius:18px;" /></figure>'
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
      background: #fff;
      color: {COLORS["ink"]};
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    main {{
      width: min(720px, calc(100vw - 28px));
      margin: 0 auto;
      padding: 24px 0 80px;
    }}
  </style>
</head>
<body>
  <main>
    {"".join(parts)}
  </main>
</body>
</html>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="直接从 WPS 笔记生成微信公众号原生发布包。")
    parser.add_argument("--note-id", default="")
    parser.add_argument("--note-json", default="", help="提前导出的 note.json，跳过 CLI 读取")
    parser.add_argument("--image-dir", default="", help="已导出的图片目录，按原文图片顺序映射")
    parser.add_argument("--output-dir", default="", help="输出目录，默认在文章目录下生成 .wechat-publish-package-wechat-native")
    parser.add_argument("--footer-image", default=str(DEFAULT_FOOTER))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.note_id and not args.note_json:
        raise SystemExit("至少传 --note-id 或 --note-json 其中一个。")

    if args.note_json:
        note = json.loads(Path(args.note_json).read_text(encoding="utf-8"))["data"]
    else:
        note = run_json(["wpsnote-cli", "read", "--note_id", args.note_id, "--json"])["data"]
    title = note["title"]
    blocks = parse_note_blocks(note["content"])

    note_id = args.note_id or "manual"
    article_dir = OUTPUT_ROOT / f"{slugify_title(title)}_wps_{note_id}"
    article_dir.mkdir(parents=True, exist_ok=True)
    image_dir = Path(args.image_dir).resolve() if args.image_dir else article_dir / "图片素材"
    if args.image_dir:
        image_map = build_image_map_from_dir(blocks, image_dir)
    else:
        if not args.note_id:
            raise SystemExit("未提供 --image-dir 时必须传 --note-id，才能自动导出图片。")
        image_map = export_images(args.note_id, blocks, image_dir)
    output_dir = Path(args.output_dir).resolve() if args.output_dir else article_dir / ".wechat-publish-package-wechat-native"
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest_from_blocks(title, blocks, image_map, Path(args.footer_image).resolve())
    manifest_path = output_dir / "manifest.json"
    preview_path = output_dir / "publish-preview.html"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    preview_path.write_text(build_preview_html(manifest), encoding="utf-8")

    print(f"MANIFEST={manifest_path}")
    print(f"PREVIEW={preview_path}")


if __name__ == "__main__":
    main()
