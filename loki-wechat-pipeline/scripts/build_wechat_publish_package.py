#!/usr/bin/env python3

from __future__ import annotations

import argparse
import contextlib
import html
import json
import os
import socketserver
import threading
from dataclasses import dataclass
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright

DEFAULT_FOOTER = Path(__file__).resolve().parent.parent / "typesetting-wechat-articles" / "assets" / "signature.png"


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        return


@dataclass
class LocalServer:
    base_dir: Path
    server: socketserver.TCPServer | None = None
    thread: threading.Thread | None = None
    port: int | None = None

    def start(self) -> str:
        handler = lambda *args, **kwargs: QuietHandler(*args, directory=str(self.base_dir), **kwargs)
        self.server = socketserver.TCPServer(("127.0.0.1", 0), handler)
        self.port = int(self.server.server_address[1])
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return f"http://127.0.0.1:{self.port}"

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把公众号排版预览页转成微信公众号后台发布包。")
    parser.add_argument("--input", required=True, help="公众号排版预览.html 的绝对路径")
    parser.add_argument("--output-dir", help="发布包输出目录，默认在输入目录下生成 .wechat-publish-package")
    parser.add_argument("--author", default="", help="作者名，可选")
    parser.add_argument("--footer-image", default=str(DEFAULT_FOOTER), help="固定文末关注图")
    parser.add_argument(
        "--mode",
        choices=["hybrid", "high-fidelity", "native-editable"],
        default="hybrid",
        help="hybrid=正文文字+复杂模块截图；high-fidelity=整篇按版面分段截图；native-editable=尽量保留原生可编辑正文和标题",
    )
    return parser.parse_args()


def build_extract_script(mode: str) -> str:
    return r"""
({ mode }) => {
  const main = document.querySelector('main');
  if (!main) {
    throw new Error('页面里没有找到 <main>');
  }

  const COLORS = {
    ink: '#2e221a',
    text: '#4d4036',
    muted: '#7d6d60',
    accent: '#a66012',
    accentDeep: '#8f5510',
    soft: '#fff7ea',
    line: '#e7d8c0'
  };

  let renderCounter = 0;
  const blocks = [];

  const isNativeEditable = mode === 'native-editable';

  const escapeText = (value) => {
    const div = document.createElement('div');
    div.textContent = value || '';
    return div.innerHTML;
  };

  const sanitizeStyledInline = (rawHtml) =>
    (rawHtml || '')
      .replace(/\s*\n\s*/g, ' ')
      .replace(/<strong>/gi, `<strong style="color:${COLORS.accent};font-weight:700;">`)
      .trim();

  const sanitizeNativeInline = (rawHtml) =>
    (rawHtml || '')
      .replace(/\s*\n\s*/g, ' ')
      .replace(/<strong[^>]*>/gi, `<strong style="color:${COLORS.accentDeep};font-weight:700;">`)
      .replace(/<b[^>]*>/gi, `<strong style="color:${COLORS.accentDeep};font-weight:700;">`)
      .replace(/<\/b>/gi, '</strong>')
      .replace(/<span[^>]*>/gi, '')
      .replace(/<\/span>/gi, '')
      .trim();

  const sanitizeInline = (rawHtml) =>
    isNativeEditable ? sanitizeNativeInline(rawHtml) : sanitizeStyledInline(rawHtml);

  const pushHtml = (html) => {
    if (html && html.trim()) {
      blocks.push({ type: 'html', html: html.trim() });
    }
  };

  const nativeParagraphHtml = (innerHtml, options = {}) => {
    const {
      color = COLORS.text,
      fontSize = 17,
      lineHeight = 1.92,
      margin = '0 0 16px',
      fontWeight = 400,
      letterSpacing = '0',
    } = options;
    return `<p style="margin:${margin};color:${color};font-size:${fontSize}px;line-height:${lineHeight};font-weight:${fontWeight};letter-spacing:${letterSpacing};">${sanitizeInline(innerHtml)}</p>`;
  };

  const nativeHeadingBlockHtml = (kickerText, titleText) => {
    const kicker = (kickerText || '').trim();
    const title = (titleText || '').trim();
    const kickerHtml = kicker
      ? `<p style="margin:46px 0 12px;color:${COLORS.accentDeep};font-size:12px;line-height:1.5;font-weight:700;letter-spacing:1.4px;text-transform:uppercase;">${escapeText(kicker)}</p>`
      : `<p style="margin:46px 0 14px;color:${COLORS.accent};font-size:13px;line-height:1;">——</p>`;
    const titleHtml = `<p style="margin:0 0 18px;color:${COLORS.ink};font-size:30px;line-height:1.38;font-weight:700;">${escapeText(title)}</p>`;
    return kickerHtml + titleHtml;
  };

  const nativeQuoteBlockHtml = (innerHtml) =>
    `<table style="width:100%;margin:14px 0 18px;border-collapse:separate;border-spacing:0;">` +
    `<tbody><tr><td style="padding:14px 16px;border-left:4px solid ${COLORS.accent};border-radius:0 16px 16px 0;background:${COLORS.soft};color:${COLORS.ink};font-size:17px;line-height:1.88;">${sanitizeInline(innerHtml)}</td></tr></tbody>` +
    `</table>`;

  const nativeStackedCardsHtml = (items, kind = 'sequence') => {
    const cards = items
      .map((item, index) => {
        const label = kind === 'sequence' ? `0${index + 1}`.slice(-2) : `要点 ${index + 1}`;
        return (
          `<tr>` +
          `<td style="width:33.33%;padding:${index === 0 ? '0 6px 0 0' : index === items.length - 1 ? '0 0 0 6px' : '0 6px'};vertical-align:top;">` +
          `<p style="margin:0 0 8px;color:${COLORS.accentDeep};font-size:11px;line-height:1.5;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">${escapeText(label)}</p>` +
          `<p style="margin:0;padding:14px 14px 15px;border:1px solid ${COLORS.line};border-radius:18px;background:#fffdf8;color:${COLORS.ink};font-size:16px;line-height:1.82;">${sanitizeInline(item)}</p>` +
          `</td>` +
          `</tr>`
        );
      })
      .join('');
    if (items.length === 3) {
      const cols = items
        .map((item, index) => {
          const label = kind === 'sequence' ? `0${index + 1}`.slice(-2) : `要点 ${index + 1}`;
          return (
            `<td style="width:33.33%;padding:${index === 0 ? '0 6px 0 0' : index === items.length - 1 ? '0 0 0 6px' : '0 6px'};vertical-align:top;">` +
            `<p style="margin:0 0 8px;color:${COLORS.accentDeep};font-size:11px;line-height:1.5;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">${escapeText(label)}</p>` +
            `<p style="margin:0;padding:14px 14px 15px;border:1px solid ${COLORS.line};border-radius:18px;background:#fffdf8;color:${COLORS.ink};font-size:16px;line-height:1.82;">${sanitizeInline(item)}</p>` +
            `</td>`
          );
        })
        .join('');
      return `<table style="width:100%;margin:16px 0 18px;border-collapse:separate;border-spacing:0;table-layout:fixed;"><tbody><tr>${cols}</tr></tbody></table>`;
    }
    return items
      .map((item, index) => {
        const label = kind === 'sequence' ? `0${index + 1}`.slice(-2) : `要点 ${index + 1}`;
        return (
          `<p style="margin:${index === 0 ? '16px' : '0'} 0 6px;color:${COLORS.accentDeep};font-size:11px;line-height:1.5;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">${escapeText(label)}</p>` +
          `<p style="margin:0 0 ${index === items.length - 1 ? '18px' : '14px'};padding:14px 16px;border:1px solid ${COLORS.line};border-radius:18px;background:#fffdf8;color:${COLORS.ink};font-size:16px;line-height:1.82;">${sanitizeInline(item)}</p>`
        );
      })
      .join('');
  };

  const nextRenderId = (mode) => {
    renderCounter += 1;
    return `${mode}-${String(renderCounter).padStart(3, '0')}`;
  };

  const pushRenderBlock = (element, mode, alt = '') => {
    const renderId = nextRenderId(mode);
    element.setAttribute('data-wechat-render-id', renderId);
    blocks.push({
      type: 'image',
      renderMode: mode,
      renderId,
      alt: (alt || '').trim(),
    });
  };

  const paragraphHtml = (innerHtml, extra = '') =>
    isNativeEditable
      ? `<p>${sanitizeInline(innerHtml)}</p>`
      : `<p style="margin:0 0 12px;color:${COLORS.text};font-size:17px;line-height:1.92;${extra}">${sanitizeInline(innerHtml)}</p>`;

  const ledeHtml = (innerHtml) =>
    isNativeEditable
      ? nativeParagraphHtml(innerHtml, {
          color: COLORS.ink,
          fontSize: 20,
          lineHeight: 1.9,
          fontWeight: 600,
          margin: '0 0 18px',
        })
      : `<p style="margin:0 0 14px;color:${COLORS.ink};font-size:20px;line-height:1.88;">${sanitizeInline(innerHtml)}</p>`;

  const smallMetaHtml = (innerHtml) =>
    isNativeEditable
      ? `<p>${sanitizeInline(innerHtml)}</p>`
      : `<p style="margin:0 0 14px;color:${COLORS.muted};font-size:14px;line-height:1.85;">${sanitizeInline(innerHtml)}</p>`;

  const pushNativeHeading = (kickerText, titleText) => {
    const kicker = (kickerText || '').trim();
    const title = (titleText || '').trim();
    if (kicker) {
      pushHtml(nativeHeadingBlockHtml(kicker, title));
      return;
    }
    if (title) pushHtml(nativeHeadingBlockHtml('', title));
  };

  const pushNativeQuote = (html) => {
    pushHtml(nativeQuoteBlockHtml(html));
  };

  const pushNativeListFromArticles = (element) => {
    const items = Array.from(element.querySelectorAll('article p')).map((item) => item.innerHTML);
    if (items.length) pushHtml(nativeStackedCardsHtml(items));
  };

  const parseChildren = (container) => {
    const children = Array.from(container.children);

    children.forEach((child, index) => {
      if (child.matches('span.section-tag')) {
        const next = children[index + 1];
        if (next && next.matches('h2')) {
          if (isNativeEditable) {
            pushNativeHeading(child.textContent, next.textContent);
          } else {
            pushRenderBlock(next, 'heading', next.textContent);
          }
        }
        return;
      }

      if (child.matches('div.section-heading')) {
        const heading = child.querySelector('h2');
        if (heading) {
          if (isNativeEditable) {
            pushNativeHeading('', heading.textContent);
          } else {
            pushRenderBlock(child, 'heading', heading.textContent);
          }
        }
        return;
      }

      if (child.matches('h2')) {
        const prev = children[index - 1];
        if (prev && prev.matches('span.section-tag')) {
          return;
        }
        if (isNativeEditable) {
          pushNativeHeading('', child.textContent);
        } else {
          pushRenderBlock(child, 'heading', child.textContent);
        }
        return;
      }

      if (child.matches('p.subtitle')) {
        pushHtml(
          isNativeEditable
            ? nativeParagraphHtml(child.innerHTML, {
                color: COLORS.muted,
                fontSize: 16,
                lineHeight: 1.86,
                margin: '8px 0 16px',
              })
            : `<p style="margin:0 0 14px;color:${COLORS.muted};font-size:17px;line-height:1.82;">${sanitizeInline(child.innerHTML)}</p>`
        );
        return;
      }

      if (child.matches('p.lede')) {
        pushHtml(ledeHtml(child.innerHTML));
        return;
      }

      if (child.matches('p.soft')) {
        pushHtml(
          isNativeEditable
            ? nativeParagraphHtml(child.innerHTML, { color: COLORS.muted })
            : paragraphHtml(child.innerHTML, `color:${COLORS.muted};`)
        );
        return;
      }

      if (child.matches('p.meta')) {
        pushHtml(
          isNativeEditable
          ? `<p style="margin:0 0 14px;"><span style="display:inline-block;padding:7px 10px;border:1px solid ${COLORS.line};border-radius:999px;background:#fffaf1;color:${COLORS.accentDeep};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">${escapeText(child.textContent)}</span></p>`
          : `<p style="margin:0 0 12px;color:${COLORS.accent};font-size:12px;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">${escapeText(child.textContent)}</p>`
        );
        return;
      }

      if (child.matches('div.section-copy, section.intro')) {
        Array.from(child.querySelectorAll(':scope > p')).forEach((paragraph) => {
          if (isNativeEditable) {
            const isLede = paragraph.classList.contains('lede');
            const isSoft = paragraph.classList.contains('soft');
            pushHtml(
              nativeParagraphHtml(paragraph.innerHTML, {
                color: isSoft ? COLORS.muted : isLede ? COLORS.ink : COLORS.text,
                fontSize: isLede ? 20 : 17,
                lineHeight: isLede ? 1.9 : 1.92,
                fontWeight: isLede ? 600 : 400,
                margin: isLede ? '0 0 18px' : '0 0 16px',
              })
            );
          } else {
            pushHtml(paragraphHtml(paragraph.innerHTML));
          }
        });
        Array.from(child.querySelectorAll(':scope > figure.single-image, :scope > figure.poster-frame')).forEach((figure) => {
          const alt = figure.querySelector('img')?.getAttribute('alt') || '';
          pushRenderBlock(figure, 'figure', alt);
        });
        return;
      }

      if (child.matches('p')) {
        pushHtml(isNativeEditable ? nativeParagraphHtml(child.innerHTML) : paragraphHtml(child.innerHTML));
        return;
      }

      if (child.matches('div.highlight')) {
        if (isNativeEditable) {
          const para = child.querySelector('p');
          if (para) pushNativeQuote(para.innerHTML);
        } else {
          pushRenderBlock(child, 'highlight', child.textContent);
        }
        return;
      }

      if (child.matches('div.list-summary')) {
        if (isNativeEditable) {
          const items = Array.from(child.querySelectorAll('li')).map((li) => li.innerHTML);
          if (items.length) pushHtml(nativeStackedCardsHtml(items, 'summary'));
        } else {
          pushRenderBlock(child, 'list-summary', child.textContent);
        }
        return;
      }

      if (child.matches('div.closing-note')) {
        if (isNativeEditable) {
          const para = child.querySelector('p');
          if (para) pushNativeQuote(para.innerHTML);
        } else {
          pushRenderBlock(child, 'closing-note', child.textContent);
        }
        return;
      }

      if (child.matches('section.compare-grid')) {
        if (isNativeEditable) {
          pushNativeListFromArticles(child);
        } else {
          pushRenderBlock(child, 'compare', '对比卡片');
        }
        return;
      }

      if (child.matches('section.sequence-grid')) {
        if (isNativeEditable) {
          pushNativeListFromArticles(child);
        } else {
          pushRenderBlock(child, 'sequence', '步骤卡片');
        }
        return;
      }

      if (child.matches('section.gallery-wrap')) {
        pushRenderBlock(child, 'gallery', child.querySelector('.gallery-title')?.textContent || '图片画廊');
        return;
      }

      if (child.matches('figure.single-image, figure.poster-frame')) {
        const alt = child.querySelector('img')?.getAttribute('alt') || '';
        pushRenderBlock(child, 'figure', alt);
        return;
      }
    });
  };

  const hero = main.querySelector(':scope > header.hero');
  const title = hero?.querySelector('h1')?.textContent?.trim() || document.title.trim();

  if (mode === 'high-fidelity') {
    if (hero) {
      pushRenderBlock(hero, 'hero', title);
    }
    Array.from(main.children).forEach((section) => {
      if (section.matches('header.hero')) return;
      if (section.matches('section.intro, section.section')) {
        const sectionTitle = section.querySelector('h2')?.textContent?.trim() || section.className || 'section';
        pushRenderBlock(section, 'section', sectionTitle);
      }
    });
    return { title, blocks };
  }

  if (hero) {
    const heroNote = hero.querySelector('.hero-note');
    if (heroNote) {
      pushHtml(
        isNativeEditable
          ? `<p style="margin:0 0 12px;"><span style="display:inline-block;padding:0 0 6px;border-bottom:1px solid ${COLORS.line};color:${COLORS.accentDeep};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">${escapeText(heroNote.textContent)}</span></p>`
          : `<p style="margin:0 0 12px;"><span style="display:inline-block;padding:0 0 6px;border-bottom:1px solid ${COLORS.line};color:${COLORS.accentDeep};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;">${escapeText(heroNote.textContent)}</span></p>`
      );
    }
    const heroTail = hero.querySelector('.hero-tail, p.subtitle');
    if (heroTail) {
      pushHtml(
        isNativeEditable
          ? nativeParagraphHtml(heroTail.innerHTML, {
              color: COLORS.muted,
              fontSize: 16,
              lineHeight: 1.9,
              margin: '0 0 18px',
            })
          : `<div style="margin:6px 0 18px;"><p style="margin:0;color:${COLORS.muted};font-size:16px;line-height:1.9;">${sanitizeInline(heroTail.innerHTML)}</p></div>`
      );
    }
    const meta = hero.querySelector('p.meta');
    if (meta) {
      pushHtml(isNativeEditable ? `<p style="margin:0 0 14px;"><span style="display:inline-block;padding:7px 10px;border:1px solid ${COLORS.line};border-radius:999px;background:#fffaf1;color:${COLORS.accentDeep};font-size:12px;line-height:1.4;font-weight:700;letter-spacing:1.1px;text-transform:uppercase;">${escapeText(meta.textContent)}</span></p>` : smallMetaHtml(meta.innerHTML));
    }
    const cover = hero.querySelector('figure.single-image');
    if (cover) {
      const alt = cover.querySelector('img')?.getAttribute('alt') || '';
      pushRenderBlock(cover, 'figure', alt);
    }
  }

  Array.from(main.children).forEach((section) => {
    if (section.matches('header.hero')) return;
    if (section.matches('section.intro, section.section')) {
      parseChildren(section);
    }
  });

  return { title, blocks };
}
"""


def apply_export_layout(page, render_id: str, render_mode: str) -> None:
    if render_mode != "gallery":
        return
    page.evaluate(
        """
        ({ renderId }) => {
          const target = document.querySelector(`[data-wechat-render-id="${renderId}"]`);
          if (!target) return;
          const gallery = target.querySelector('.gallery');
          if (!gallery) return;
          const portrait = gallery.classList.contains('gallery--portrait');
          target.style.width = '760px';
          target.style.boxSizing = 'border-box';
          gallery.style.overflow = 'visible';
          gallery.style.display = 'grid';
          gallery.style.gridTemplateColumns = portrait ? 'repeat(3, minmax(0, 1fr))' : '1fr';
          gallery.style.gap = '16px';
          gallery.style.paddingBottom = '0';
          Array.from(gallery.children).forEach((card) => {
            card.style.flex = 'none';
            card.style.width = '100%';
            card.style.minWidth = '0';
          });
        }
        """,
        {"renderId": render_id},
    )


def screenshot_render_blocks(page, manifest: dict, output_dir: Path) -> None:
    assets_dir = output_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    image_index = 0

    for block in manifest["body"]:
        if block["type"] != "image" or not block.get("renderId"):
            continue

        image_index += 1
        render_mode = block["renderMode"]
        render_id = block["renderId"]
        apply_export_layout(page, render_id, render_mode)
        locator = page.locator(f'[data-wechat-render-id="{render_id}"]')
        locator.scroll_into_view_if_needed()
        page.wait_for_timeout(120)
        filename = f"{image_index:03d}-{render_mode}.png"
        out_path = assets_dir / filename
        locator.screenshot(path=str(out_path))
        block["file"] = str(out_path.resolve())


def append_fixed_footer(manifest: dict, footer_image: Path) -> None:
    if not footer_image.exists():
        return
    manifest["body"].append(
        {
            "type": "image",
            "renderMode": "raw",
            "renderId": None,
            "alt": "关注引导图",
            "file": str(footer_image.resolve()),
        }
    )


def build_preview_html(manifest: dict) -> str:
    parts: list[str] = []
    for block in manifest["body"]:
        if block["type"] == "html":
            parts.append(block["html"])
        elif block["type"] == "image" and block.get("file"):
            src = Path(block["file"]).as_uri()
            alt = html.escape(block.get("alt", ""))
            parts.append(
                '<figure style="margin:24px 0;">'
                f'<img src="{src}" alt="{alt}" style="display:block;width:100%;border-radius:18px;" />'
                "</figure>"
            )

    body = "\n".join(parts)
    title = html.escape(manifest["title"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      background: #f7f3ec;
      color: #2e221a;
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    main {{
      width: min(760px, calc(100vw - 28px));
      margin: 0 auto;
      padding: 28px 0 80px;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""


def build_copy_source_html(manifest: dict) -> str:
    parts: list[str] = []
    copy_index = 0
    for block in manifest["body"]:
        if block["type"] != "html":
            continue
        copy_index += 1
        block["copyIndex"] = copy_index
        parts.append(
            '<div '
            f'data-copy-block-index="{copy_index}" '
            'style="display:block;">'
            f'{block["html"]}'
            "</div>"
        )

    body = "\n".join(parts)
    title = html.escape(manifest["title"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} Copy Source</title>
  <style>
    body {{
      margin: 0;
      background: #ffffff;
      color: #2e221a;
      font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    }}
    main {{
      width: min(760px, calc(100vw - 28px));
      margin: 0 auto;
      padding: 28px 0 80px;
    }}
    [data-copy-block-index] {{
      display: block;
    }}
  </style>
</head>
<body>
  <main>
    {body}
  </main>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"输入文件不存在：{input_path}")

    article_dir = input_path.parent
    output_dir = Path(args.output_dir).resolve() if args.output_dir else article_dir / ".wechat-publish-package"
    output_dir.mkdir(parents=True, exist_ok=True)
    footer_image = Path(args.footer_image).resolve()

    server = LocalServer(article_dir)
    base_url = server.start()

    try:
        encoded_name = quote(input_path.name)
        preview_url = f"{base_url}/{encoded_name}"
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True,
                executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            )
            page = browser.new_page(viewport={"width": 1280, "height": 2200}, device_scale_factor=2)
            page.goto(preview_url, wait_until="networkidle")
            extracted = page.evaluate(build_extract_script(args.mode), {"mode": args.mode})
            manifest = {
                "version": 1,
                "mode": args.mode,
                "title": extracted["title"],
                "author": args.author,
                "source_preview": str(input_path),
                "body": extracted["blocks"],
            }
            screenshot_render_blocks(page, manifest, output_dir)
            append_fixed_footer(manifest, footer_image)
            browser.close()
    finally:
        server.stop()

    manifest_path = output_dir / "manifest.json"
    preview_path = output_dir / "publish-preview.html"
    copy_source_path = output_dir / "copy-source.html"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    preview_path.write_text(build_preview_html(manifest), encoding="utf-8")
    copy_source_path.write_text(build_copy_source_html(manifest), encoding="utf-8")

    print(f"MANIFEST={manifest_path}")
    print(f"PREVIEW={preview_path}")
    print(f"COPY_SOURCE={copy_source_path}")


if __name__ == "__main__":
    main()
