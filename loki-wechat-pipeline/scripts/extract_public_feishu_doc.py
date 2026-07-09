#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parent.parent
OUTPUT_ROOT = ROOT / "已下载的推文"


BLOCK_COLLECTOR_JS = """
() => {
  const h1 = document.querySelector('h1');
  const title = (h1?.innerText || document.title || '').trim();
  const h1Rect = h1 ? h1.getBoundingClientRect() : {top: 0, left: 0};
  const scrollRoot = document.querySelector('[data-feishu-scroll-root="1"]');
  const scrollTop = scrollRoot ? scrollRoot.scrollTop : window.scrollY;

  const countMeaningfulDescendants = (root) => {
    const children = Array.from(root.querySelectorAll('*'));
    return children.filter((el) => {
      const rect = el.getBoundingClientRect();
      if (rect.width < 40 || rect.height < 12) return false;
      const text = (el.innerText || '').trim();
      const tag = el.tagName.toUpperCase();
      return tag === 'IMG' || text.length > 0;
    }).length;
  };

  let contentRoot = h1?.parentElement || document.body;
  while (contentRoot && contentRoot !== document.body) {
    const rect = contentRoot.getBoundingClientRect();
    if (rect.width >= 520 && countMeaningfulDescendants(contentRoot) >= 20) {
      break;
    }
    contentRoot = contentRoot.parentElement;
  }
  if (!contentRoot) contentRoot = document.body;

  const isVisibleEnough = (el) => {
    const rect = el.getBoundingClientRect();
    if (rect.width < 40 || rect.height < 12) return false;
    const style = window.getComputedStyle(el);
    if (style.display === 'none' || style.visibility === 'hidden') return false;
    if (rect.left + rect.width < h1Rect.left - 60) return false;
    if (rect.top + rect.height < -400) return false;
    if (rect.top > window.innerHeight + 600) return false;
    return true;
  };

  const hasBlockTextChild = (el) => {
    return Array.from(el.children).some((child) => {
      const childText = (child.innerText || '').trim();
      if (!childText) return false;
      const display = window.getComputedStyle(child).display;
      return !['inline', 'inline-block', 'contents'].includes(display);
    });
  };

  const classifyTextType = (el, text) => {
    const tag = el.tagName.toUpperCase();
    if (tag === 'H1') return 'title';
    if (tag.startsWith('H')) return 'heading';
    if (/^\\d+月\\d+日/.test(text)) return 'meta';
    const style = window.getComputedStyle(el);
    const fontSize = parseFloat(style.fontSize || '0');
    const fontWeight = parseInt(style.fontWeight || '400', 10) || 400;
    const isStandaloneTitleLike =
      text.length <= 28 &&
      fontWeight >= 700 &&
      fontSize >= 20 &&
      !/[。！？：；，,.!?]$/.test(text);
    if (fontSize >= 24 || isStandaloneTitleLike) return 'heading';
    return 'paragraph';
  };

  const blocks = [];
  const imageNodes = Array.from(document.querySelectorAll('img'));
  for (const el of imageNodes) {
    if (!isVisibleEnough(el)) continue;
    const rect = el.getBoundingClientRect();
    const src = el.currentSrc || el.src || '';
    if (!src || rect.width < 120 || rect.height < 80) continue;
    blocks.push({
      type: 'image',
      src,
      alt: el.alt || '',
      width: el.naturalWidth || el.width || Math.round(rect.width),
      height: el.naturalHeight || el.height || Math.round(rect.height),
      top: Math.round(rect.top),
      docTop: Math.round(rect.top + scrollTop),
      left: Math.round(rect.left),
    });
  }

  const descendants = Array.from(contentRoot.querySelectorAll('*'));
  for (const el of descendants) {
    if (!isVisibleEnough(el)) continue;
    const tag = el.tagName.toUpperCase();
    const rect = el.getBoundingClientRect();

    if (tag === 'IMG') continue;

    const text = (el.innerText || '').trim();
    if (!text) continue;
    if (hasBlockTextChild(el)) continue;
    if (el.querySelector('img')) continue;

    const textType = classifyTextType(el, text);
    const style = window.getComputedStyle(el);
    blocks.push({
      type: textType,
      text,
      top: Math.round(rect.top),
      docTop: Math.round(rect.top + scrollTop),
      left: Math.round(rect.left),
      fontSize: parseFloat(style.fontSize || '0') || 0,
      fontWeight: parseInt(style.fontWeight || '400', 10) || 400,
    });
  }

  blocks.sort((a, b) => (a.docTop - b.docTop) || (a.left - b.left));
  return blocks;
}
"""


def slugify_title(title: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]+', " ", title)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "未命名飞书文档"


def derive_output_dir(title: str) -> Path:
    return OUTPUT_ROOT / f"{slugify_title(title)}_feishu"


def canonicalize_image_src(src: str) -> str:
    if not src:
        return src
    parts = urlsplit(src)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k not in {"width", "height", "policy", "format"}]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def extract_feishu_doc(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        ctx = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={"width": 1440, "height": 2200},
        )
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        page.evaluate(
            """() => {
              const nodes = Array.from(document.querySelectorAll('*'));
              const target = nodes
                .map((el) => ({el, delta: el.scrollHeight - el.clientHeight}))
                .filter((item) => item.delta > 800)
                .sort((a, b) => b.delta - a.delta)[0]?.el;
              if (target) target.setAttribute('data-feishu-scroll-root', '1');
            }"""
        )
        stable_rounds = 0
        last_top = -1
        for _ in range(36):
            current_top = page.evaluate(
                """() => {
                  const target = document.querySelector('[data-feishu-scroll-root="1"]');
                  if (!target) return -1;
                  target.scrollTop = target.scrollHeight;
                  return target.scrollTop;
                }"""
            )
            page.wait_for_timeout(1200)
            next_top = page.evaluate(
                """() => {
                  const target = document.querySelector('[data-feishu-scroll-root="1"]');
                  return target ? target.scrollTop : -1;
                }"""
            )
            if next_top == last_top or next_top == current_top:
                stable_rounds += 1
                if stable_rounds >= 2:
                    break
            else:
                stable_rounds = 0
            last_top = next_top
        page.evaluate(
            """() => {
              const target = document.querySelector('[data-feishu-scroll-root="1"]');
              if (target) target.scrollTop = 0;
            }"""
        )
        page.wait_for_timeout(1200)
        data = page.evaluate(
            """() => {
              const h1 = document.querySelector('h1');
              const title = (h1?.innerText || document.title || '').trim();
              const bodyText = document.body.innerText || '';
              const images = Array.from(document.querySelectorAll('img'))
                .map((img, i) => ({
                  index: i,
                  src: img.currentSrc || img.src || '',
                  alt: img.alt || '',
                  width: img.naturalWidth || img.width || 0,
                  height: img.naturalHeight || img.height || 0
                }))
                .filter(item => item.src);
              return {title, bodyText, images};
            }"""
        )

        scroll_info = page.evaluate(
            """() => {
              const target = document.querySelector('[data-feishu-scroll-root="1"]');
              if (!target) return null;
              return {
                scrollHeight: target.scrollHeight,
                clientHeight: target.clientHeight
              };
            }"""
        )
        if scroll_info:
            step = max(int(scroll_info["clientHeight"] * 0.78), 800)
            max_top = max(scroll_info["scrollHeight"] - scroll_info["clientHeight"], 0)
            positions = list(range(0, max_top + 1, step))
            if positions[-1] != max_top:
                positions.append(max_top)

            sampled_lines: list[str] = []
            sampled_blocks: list[dict] = []
            for top in positions:
                page.evaluate(
                    """(top) => {
                      const target = document.querySelector('[data-feishu-scroll-root="1"]');
                      if (target) target.scrollTop = top;
                    }""",
                    top,
                )
                page.wait_for_timeout(500)
                chunk_text = page.evaluate(
                    """() => {
                      const target = document.querySelector('[data-feishu-scroll-root="1"]');
                      return target ? (target.innerText || '') : '';
                    }"""
                )
                chunk_blocks = page.evaluate(BLOCK_COLLECTOR_JS)
                sampled_blocks.extend(chunk_blocks)
                chunk_lines = [raw.strip() for raw in chunk_text.splitlines() if raw.strip()]
                if not chunk_lines:
                    continue
                if not sampled_lines:
                    sampled_lines.extend(chunk_lines)
                    continue

                max_overlap = min(len(sampled_lines), len(chunk_lines))
                overlap = 0
                for size in range(max_overlap, 0, -1):
                    if sampled_lines[-size:] == chunk_lines[:size]:
                        overlap = size
                        break
                sampled_lines.extend(chunk_lines[overlap:])

            if sampled_lines:
                data["bodyText"] = "\n".join(sampled_lines)
            if sampled_blocks:
                data["blocks"] = dedupe_blocks(sampled_blocks)

        toc_hashes = page.evaluate(
            """() => {
              return Array.from(document.querySelectorAll('a[href^="#"]'))
                .map((link) => ({
                  href: link.getAttribute('href') || '',
                  text: (link.innerText || '').trim()
                }))
                .filter((item) => item.href && item.text)
                .filter((item, index, arr) => arr.findIndex((other) => other.href === item.href) === index);
            }"""
        )
        if toc_hashes:
            toc_blocks: list[dict] = []
            for item in toc_hashes:
                href = item.get("href", "")
                if not href:
                    continue
                try:
                    locator = page.locator(f'a[href="{href}"]').first
                    locator.click(timeout=3000)
                    page.wait_for_timeout(900)
                    toc_blocks.extend(page.evaluate(BLOCK_COLLECTOR_JS))
                except Exception:
                    continue
            if toc_blocks:
                toc_image_blocks = [block for block in toc_blocks if block.get("type") == "image"]
                data["blocks"] = dedupe_blocks([*data.get("blocks", []), *toc_image_blocks])
        browser.close()
    return data


def download_images(url: str, image_sources: list[dict], image_dir: Path) -> list[dict]:
    image_dir.mkdir(parents=True, exist_ok=True)
    exported: list[dict] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
        ctx = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={"width": 1440, "height": 2200},
        )
        page = ctx.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        page.evaluate(
            """() => {
              const nodes = Array.from(document.querySelectorAll('*'));
              const target = nodes
                .map((el) => ({el, delta: el.scrollHeight - el.clientHeight}))
                .filter((item) => item.delta > 800)
                .sort((a, b) => b.delta - a.delta)[0]?.el;
              if (target) {
                target.setAttribute('data-feishu-scroll-root', '1');
                target.scrollTop = target.scrollHeight;
              }
            }"""
        )
        page.wait_for_timeout(2000)
        page.evaluate(
            """() => {
              const target = document.querySelector('[data-feishu-scroll-root="1"]');
              if (target) target.scrollTop = 0;
            }"""
        )
        page.wait_for_timeout(1200)
        for idx, image in enumerate(image_sources, start=1):
            payload = None
            try:
                payload = page.evaluate(
                    """async (src) => {
                      const res = await fetch(src, {credentials: 'include'});
                      const buf = await res.arrayBuffer();
                      const bytes = new Uint8Array(buf);
                      let binary = '';
                      const chunkSize = 0x8000;
                      for (let i = 0; i < bytes.length; i += chunkSize) {
                        binary += String.fromCharCode(...bytes.slice(i, i + chunkSize));
                      }
                      return {
                        ok: res.ok,
                        status: res.status,
                        type: res.headers.get('content-type') || '',
                        b64: btoa(binary)
                      };
                    }""",
                    image["src"],
                )
            except Exception:
                payload = None

            ext = ".png"
            content_type = (payload or {}).get("type", "")
            if "jpeg" in content_type or "jpg" in content_type:
                ext = ".jpg"
            elif "webp" in content_type:
                ext = ".webp"
            dest = image_dir / f"{idx:03d}{ext}"

            if payload and payload.get("ok"):
                dest.write_bytes(base64.b64decode(payload["b64"]))
            else:
                top = int(image.get("top", 0) or 0)
                page.evaluate(
                    """(top) => {
                      const target = document.querySelector('[data-feishu-scroll-root="1"]');
                      if (target) {
                        const desired = Math.max(top - target.clientHeight / 2, 0);
                        target.scrollTop = desired;
                      }
                    }""",
                    top,
                )
                page.wait_for_timeout(700)
                canonical_src = canonicalize_image_src(image["src"])
                fallback_payload = page.evaluate(
                    """async ({ targetSrc, expectedWidth, expectedHeight }) => {
                      const canonicalize = (src) => {
                        try {
                          const url = new URL(src, location.href);
                          ['width', 'height', 'policy', 'format'].forEach((key) => url.searchParams.delete(key));
                          return url.toString();
                        } catch (error) {
                          return src || '';
                        }
                      };
                      const imgs = Array.from(document.querySelectorAll('img'));
                      let match = imgs.find((img) => canonicalize(img.currentSrc || img.src || '') === targetSrc);
                      if (!match) {
                        match = imgs
                          .map((img) => {
                            const rect = img.getBoundingClientRect();
                            const dw = Math.abs((img.naturalWidth || rect.width || 0) - expectedWidth);
                            const dh = Math.abs((img.naturalHeight || rect.height || 0) - expectedHeight);
                            return { img, score: dw + dh, area: rect.width * rect.height };
                          })
                          .filter((item) => item.area > 12000)
                          .sort((a, b) => a.score - b.score)[0]?.img || null;
                      }
                      if (!match) return null;
                      try {
                        const canvas = document.createElement('canvas');
                        const width = match.naturalWidth || expectedWidth || match.width || 1;
                        const height = match.naturalHeight || expectedHeight || match.height || 1;
                        canvas.width = width;
                        canvas.height = height;
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(match, 0, 0, width, height);
                        const dataUrl = canvas.toDataURL('image/png');
                        return {
                          kind: 'canvas',
                          type: 'image/png',
                          b64: dataUrl.replace(/^data:image\\/png;base64,/, ''),
                        };
                      } catch (error) {
                        // canvas 导出失败时，退回截图裁剪
                      }
                      const rect = match.getBoundingClientRect();
                      return {
                        kind: 'clip',
                        x: Math.max(Math.floor(rect.left), 0),
                        y: Math.max(Math.floor(rect.top), 0),
                        width: Math.max(Math.ceil(rect.width), 1),
                        height: Math.max(Math.ceil(rect.height), 1),
                      };
                    }""",
                    {
                        "targetSrc": canonical_src,
                        "expectedWidth": int(image.get("width", 0) or 0),
                        "expectedHeight": int(image.get("height", 0) or 0),
                    },
                )
                if not fallback_payload:
                    if dest.exists():
                        exported.append(
                            {
                                "index": idx,
                                "src": image["src"],
                                "src_key": image.get("src_key", canonicalize_image_src(image["src"])),
                                "alt": image["alt"],
                                "width": image["width"],
                                "height": image["height"],
                                "content_type": content_type or "image/png",
                                "file": str(dest.resolve()),
                            }
                        )
                        continue
                    print(f"[WARN] 跳过图片（下载失败且截图兜底也没找到）：src={image['src']}")
                    continue
                if fallback_payload.get("kind") == "canvas":
                    dest.write_bytes(base64.b64decode(fallback_payload["b64"]))
                    content_type = fallback_payload.get("type", "image/png")
                else:
                    viewport = page.viewport_size or {"width": 1440, "height": 2200}
                    x = max(int(fallback_payload["x"]), 0)
                    y = max(int(fallback_payload["y"]), 0)
                    max_width = max(viewport["width"] - x, 0)
                    max_height = max(viewport["height"] - y, 0)
                    width = min(int(fallback_payload["width"]), max_width)
                    height = min(int(fallback_payload["height"]), max_height)
                    if width <= 1 or height <= 1:
                        raise RuntimeError(f"截图兜底命中了图片，但裁剪区域越界：src={image['src']}")
                    page.screenshot(path=str(dest), clip={"x": x, "y": y, "width": width, "height": height})
                    content_type = "image/png"
            exported.append(
                {
                    "index": idx,
                    "src": image["src"],
                    "src_key": canonicalize_image_src(image["src"]),
                    "alt": image["alt"],
                    "width": image["width"],
                    "height": image["height"],
                    "content_type": content_type,
                    "file": str(dest.resolve()),
                }
            )
        browser.close()
    return exported


def build_text_lines(body_text: str, title: str) -> list[str]:
    lines = [line.strip() for line in body_text.splitlines()]
    lines = [line for line in lines if line]
    # 飞书 bodyText 常常会把标题和目录也带进来；这里只先保留原始顺序，后续再做排版判断。
    if title and lines and lines[0] != title:
        lines.insert(0, title)
    return lines


def dedupe_blocks(blocks: list[dict]) -> list[dict]:
    def normalize_text(text: str) -> str:
        return re.sub(r"[\u200b\u200c\u200d\u2060\ufeff]+", "", re.sub(r"\s+", " ", text)).strip()

    deduped: list[dict] = []
    seen_text_streak: list[str] = []
    seen_image_keys: set[str] = set()
    for block in blocks:
        if block["type"] == "image":
            src = block.get("src", "")
            if src.startswith("blob:"):
                key = f"blob::{round((block.get('docTop', block.get('top', 0)) or 0) / 120)}::{int(block.get('width', 0))}x{int(block.get('height', 0))}"
            else:
                key = canonicalize_image_src(src)
            if key in seen_image_keys:
                continue
            seen_image_keys.add(key)
            trimmed = dict(block)
            trimmed["src_key"] = key
            deduped.append(trimmed)
            continue

        text = normalize_text(block.get("text", ""))
        if not text:
            continue
        normalized = f"{block['type']}::{text}"
        if deduped and deduped[-1]["type"] != "image" and normalize_text(deduped[-1].get("text", "")) == text:
            continue
        if normalized in seen_text_streak[-80:]:
            continue
        seen_text_streak.append(normalized)
        trimmed = dict(block)
        trimmed["text"] = text
        deduped.append(trimmed)
    return deduped


def main() -> None:
    parser = argparse.ArgumentParser(description="提取公开飞书文档的正文和图片")
    parser.add_argument("--url", required=True, help="公开飞书文档链接")
    parser.add_argument("--output-dir", help="输出目录，默认按标题落到 已下载的推文 下")
    args = parser.parse_args()

    data = extract_feishu_doc(args.url)
    title = data["title"] or "未命名飞书文档"
    output_dir = Path(args.output_dir) if args.output_dir else derive_output_dir(title)
    output_dir.mkdir(parents=True, exist_ok=True)
    image_dir = output_dir / "图片素材"

    sampled_image_sources = [
        {
            "src": block["src"],
            "src_key": block.get("src_key", canonicalize_image_src(block["src"])),
            "alt": block.get("alt", ""),
            "width": block.get("width", 0),
            "height": block.get("height", 0),
            "top": block.get("docTop", block.get("top", 0)),
        }
        for block in data.get("blocks", [])
        if block.get("type") == "image" and block.get("src")
    ]
    merged_sources: list[dict] = []
    seen_src_keys: set[str] = set()
    for image in [*sampled_image_sources, *data.get("images", [])]:
        src = image.get("src", "")
        if not src:
            continue
        src_key = image.get("src_key") or canonicalize_image_src(src)
        if src_key in seen_src_keys:
            continue
        seen_src_keys.add(src_key)
        merged_sources.append(
            {
                "src": src,
                "src_key": src_key,
                "alt": image.get("alt", ""),
                "width": image.get("width", 0),
                "height": image.get("height", 0),
                "top": image.get("top", 0),
            }
        )

    exported_images = download_images(args.url, merged_sources, image_dir)
    payload = {
        "source_url": args.url,
        "title": title,
        "text_lines": build_text_lines(data["bodyText"], title),
        "images": exported_images,
        "blocks": dedupe_blocks(data.get("blocks", [])),
    }

    json_path = output_dir / "feishu-extracted.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    text_path = output_dir / "正文.txt"
    text_path.write_text("\n".join(payload["text_lines"]), encoding="utf-8")

    print(json.dumps(
        {
            "title": title,
            "output_dir": str(output_dir.resolve()),
            "json": str(json_path.resolve()),
            "text": str(text_path.resolve()),
            "image_count": len(exported_images),
            "image_dir": str(image_dir.resolve()),
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
