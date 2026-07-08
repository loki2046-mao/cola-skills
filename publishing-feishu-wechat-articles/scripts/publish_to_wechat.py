#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import time
import traceback
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from playwright.sync_api import BrowserContext, Page, TimeoutError, sync_playwright


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="把发布包自动灌进微信公众号后台编辑器。")
    parser.add_argument("--manifest", required=True, help="build_wechat_publish_package.py 生成的 manifest.json")
    parser.add_argument("--url", default="https://mp.weixin.qq.com/", help="公众号后台地址")
    parser.add_argument("--save-draft", action="store_true", help="灌稿完成后自动点“保存为草稿”")
    parser.add_argument("--publish", action="store_true", help="灌稿完成后尝试直接点“发布”")
    parser.add_argument("--keep-open", action="store_true", help="脚本跑完后保留浏览器，不自动关闭")
    parser.add_argument("--profile-dir", default="", help="浏览器用户目录，默认在 manifest 目录下创建")
    parser.add_argument("--headless", action="store_true", help="无头模式，主要用于本地验证")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志，方便排查卡点")
    return parser.parse_args()


VERBOSE = False


def log(message: str) -> None:
    if VERBOSE:
        print(f"[wechat-publisher] {message}", flush=True)


def append_debug_log(log_path: Path, message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def visible_editable_candidates(frame) -> list[dict]:
    return frame.evaluate(
        """
        () => {
          const candidates = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]'));
          return candidates.map((el, index) => {
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            const text = (el.textContent || '').trim();
            const placeholder =
              el.getAttribute('placeholder') ||
              el.getAttribute('data-placeholder') ||
              el.getAttribute('aria-label') ||
              '';
            return {
              index,
              tag: el.tagName.toLowerCase(),
              placeholder,
              text,
              width: rect.width,
              height: rect.height,
              area: rect.width * rect.height,
              top: rect.top,
              left: rect.left,
              hidden: style.display === 'none' || style.visibility === 'hidden' || rect.width < 8 || rect.height < 8,
            };
          }).filter((item) => !item.hidden);
        }
        """
    )


def all_editable_candidates(page: Page) -> list[tuple]:
    items: list[tuple] = []
    for frame in [page.main_frame, *page.frames]:
        try:
            candidates = visible_editable_candidates(frame)
        except Exception:
            continue
        for candidate in candidates:
            items.append((frame, candidate))
    return items


def mark_best_target(page: Page, target_name: str, keywords: Iterable[str]) -> tuple | None:
    best: tuple | None = None
    for frame, candidate in all_editable_candidates(page):
        hint = f"{candidate['placeholder']} {candidate['text']}".lower()
        score = sum(1 for keyword in keywords if keyword.lower() in hint)
        if score == 0:
            continue
        if best is None or score > best[0]:
            best = (score, frame, candidate["index"])
    if not best:
        return None
    _, frame, index = best
    log(f"锁定 {target_name} 目标：frame={frame.name or 'main'} index={index}")
    frame.evaluate(
        """
        ({ index, targetName }) => {
          const items = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]'));
          items.forEach((el) => el.removeAttribute(`data-wechat-publisher-${targetName}`));
          const target = items[index];
          if (target) target.setAttribute(`data-wechat-publisher-${targetName}`, '1');
        }
        """,
        {"index": index, "targetName": target_name},
    )
    return frame, f'[data-wechat-publisher-{target_name}="1"]'


def mark_fallback_target(page: Page, target_name: str) -> tuple | None:
    candidates = all_editable_candidates(page)
    if not candidates:
        return None

    chosen: tuple | None = None
    if target_name == "title":
        ranked = sorted(
            candidates,
            key=lambda item: (
                0 if item[1]["tag"] in {"input", "textarea"} else 1,
                item[1]["top"],
                -item[1]["width"],
            ),
        )
        for frame, candidate in ranked:
            if candidate["top"] > 420:
                continue
            if candidate["width"] < 220:
                continue
            if candidate["height"] > 140:
                continue
            chosen = (frame, candidate["index"])
            break
    elif target_name == "body":
        ranked = sorted(
            candidates,
            key=lambda item: (
                0 if item[1]["tag"] == "div" else 1,
                -item[1]["area"],
                item[1]["top"],
            ),
        )
        for frame, candidate in ranked:
            if candidate["area"] < 60000:
                continue
            chosen = (frame, candidate["index"])
            break
    elif target_name == "author":
        ranked = sorted(
            candidates,
            key=lambda item: (
                0 if item[1]["tag"] in {"input", "textarea"} else 1,
                item[1]["top"],
            ),
        )
        title_guess = mark_best_target(page, "title-probe", ["标题", "title", "请输入标题"]) or mark_fallback_target(page, "title")
        title_frame = title_guess[0] if title_guess else None
        title_selector = title_guess[1] if title_guess else None
        title_top = None
        if title_frame and title_selector:
            try:
                title_top = title_frame.evaluate(
                    "(selector) => document.querySelector(selector)?.getBoundingClientRect().top ?? null",
                    title_selector,
                )
            except Exception:
                title_top = None
        for frame, candidate in ranked:
            if candidate["width"] < 180:
                continue
            if title_top is not None and candidate["top"] <= title_top:
                continue
            if candidate["top"] > 520:
                continue
            chosen = (frame, candidate["index"])
            break

    if not chosen:
        return None
    frame, index = chosen
    log(f"回退锁定 {target_name} 目标：frame={frame.name or 'main'} index={index}")
    frame.evaluate(
        """
        ({ index, targetName }) => {
          const items = Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]'));
          items.forEach((el) => el.removeAttribute(`data-wechat-publisher-${targetName}`));
          const target = items[index];
          if (target) target.setAttribute(`data-wechat-publisher-${targetName}`, '1');
        }
        """,
        {"index": index, "targetName": target_name},
    )
    return frame, f'[data-wechat-publisher-{target_name}="1"]'


def locate_editor_targets(page: Page) -> tuple | None:
    title_target = mark_best_target(page, "title", ["标题", "title", "请输入标题"]) or mark_fallback_target(page, "title")
    body_target = mark_best_target(page, "body", ["正文", "从这里开始写正文", "编辑", "内容"]) or mark_fallback_target(page, "body")
    if title_target and body_target:
        log(f"页面已识别为编辑器：url={page.url}")
        return title_target, body_target
    return None


def poke_new_article(page: Page) -> None:
    try:
        new_article = page.get_by_text("新建图文", exact=False)
        if new_article.count() > 0:
            log(f"尝试点击“新建图文”：url={page.url}")
            new_article.first.click(timeout=500)
    except Exception:
        pass


def ensure_editor_ready(context: BrowserContext) -> tuple:
    for _ in range(120):
        pages = [page for page in context.pages if not page.is_closed()]
        for page in reversed(pages):
            located = locate_editor_targets(page)
            if located:
                log("已经找到标题和正文编辑区")
                return page, *located

        for page in reversed(pages):
            poke_new_article(page)

        for page in reversed(pages):
            try:
                page.wait_for_timeout(200)
            except Exception:
                continue
        time.sleep(1.1)

    raise RuntimeError("没有等到公众号图文编辑器。请先登录并打开“新建图文”页面。")


def fill_text_target(frame, selector: str, value: str) -> None:
    log(f"写入文本：selector={selector} value={value[:24]}")
    locator = frame.locator(selector).first
    locator.click()
    frame.evaluate(
        """
        ({ selector, value }) => {
          const target = document.querySelector(selector);
          if (!target) return;
          const isEditable = target.getAttribute('contenteditable') === 'true';
          if (isEditable) {
            target.innerHTML = '';
            target.textContent = value;
          } else {
            target.value = value;
            target.dispatchEvent(new Event('input', { bubbles: true }));
            target.dispatchEvent(new Event('change', { bubbles: true }));
          }
        }
        """,
        {"selector": selector, "value": value},
    )


def focus_editor_end(frame, selector: str) -> None:
    frame.evaluate(
        """
        (selector) => {
          const target = document.querySelector(selector);
          if (!target) return;
          target.focus();
          const selection = window.getSelection();
          const range = document.createRange();
          range.selectNodeContents(target);
          range.collapse(false);
          selection.removeAllRanges();
          selection.addRange(range);
        }
        """,
        selector,
    )


def insert_html(frame, selector: str, snippet: str) -> None:
    log(f"插入 HTML 片段：{snippet[:60]}")
    focus_editor_end(frame, selector)
    frame.evaluate(
        """
        ({ selector, html }) => {
          const target = document.querySelector(selector);
          if (!target) return;
          target.focus();
          const placeCaretAtEnd = () => {
            const selection = window.getSelection();
            const range = document.createRange();
            range.selectNodeContents(target);
            range.collapse(false);
            selection.removeAllRanges();
            selection.addRange(range);
          };
          placeCaretAtEnd();

          const payload = html;
          let inserted = false;

          try {
            inserted = document.execCommand('insertHTML', false, payload);
          } catch (error) {
            inserted = false;
          }

          if (!inserted) {
            try {
              const data = new DataTransfer();
              data.setData('text/html', payload);
              data.setData('text/plain', target.innerText || '');
              const pasteEvent = new ClipboardEvent('paste', {
                clipboardData: data,
                bubbles: true,
                cancelable: true,
              });
              inserted = target.dispatchEvent(pasteEvent);
            } catch (error) {
              inserted = false;
            }
          }

          if (!inserted) {
            const selection = window.getSelection();
            const range = selection.rangeCount ? selection.getRangeAt(0) : document.createRange();
            if (!selection.rangeCount) {
              range.selectNodeContents(target);
              range.collapse(false);
            }
            const fragment = range.createContextualFragment(payload);
            range.deleteContents();
            range.insertNode(fragment);
          }

          placeCaretAtEnd();
          target.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'insertFromPaste', data: null }));
          target.dispatchEvent(new Event('change', { bubbles: true }));
        }
        """,
        {"selector": selector, "html": snippet},
    )


class InlineMarkupParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.segments: list[tuple[str, bool]] = []
        self.bold_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {"strong", "b"}:
            self.bold_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"strong", "b"} and self.bold_depth > 0:
            self.bold_depth -= 1

    def handle_data(self, data: str) -> None:
        if not data:
            return
        self.segments.append((data, self.bold_depth > 0))


class BlockSnippetParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.root_tag: str | None = None
        self.current_item_parts: list[str] = []
        self.items: list[str] = []
        self.inner_parts: list[str] = []
        self.in_li = False

    def handle_starttag(self, tag: str, attrs) -> None:
        lower = tag.lower()
        if self.root_tag is None:
            self.root_tag = lower
            return
        if lower in {"strong", "b"}:
            target = self.current_item_parts if self.in_li else self.inner_parts
            target.append(f"<{lower}>")
        elif lower == "li":
            self.in_li = True
            self.current_item_parts = []

    def handle_endtag(self, tag: str) -> None:
        lower = tag.lower()
        if lower in {"strong", "b"}:
            target = self.current_item_parts if self.in_li else self.inner_parts
            target.append(f"</{lower}>")
        elif lower == "li":
            self.items.append("".join(self.current_item_parts))
            self.current_item_parts = []
            self.in_li = False

    def handle_data(self, data: str) -> None:
        target = self.current_item_parts if self.in_li else self.inner_parts
        target.append(data)


def parse_inline_segments(html_fragment: str) -> list[tuple[str, bool]]:
    parser = InlineMarkupParser()
    parser.feed(html_fragment)
    return [(text, bold) for text, bold in parser.segments if text]


def parse_block_snippet(snippet: str) -> tuple[str, list[tuple[str, bool]], list[list[tuple[str, bool]]]]:
    parser = BlockSnippetParser()
    parser.feed(snippet)
    tag = parser.root_tag or "p"
    inline = parse_inline_segments("".join(parser.inner_parts))
    item_segments = [parse_inline_segments(item) for item in parser.items]
    return tag, inline, item_segments


def segments_to_plain_text(segments: list[tuple[str, bool]]) -> str:
    return "".join(text for text, _ in segments)


def html_to_plain_text(snippet: str) -> str:
    tag, inline_segments, item_segments = parse_block_snippet(snippet)
    if tag in {"ol", "ul"}:
        lines = []
        for index, item in enumerate(item_segments, 1):
            prefix = f"{index}. " if tag == "ol" else "• "
            lines.append(prefix + segments_to_plain_text(item))
        return "\n".join(lines)
    if tag == "blockquote":
        return "▍ " + segments_to_plain_text(inline_segments)
    return segments_to_plain_text(inline_segments)


def write_html_to_clipboard(page, html: str, plain_text: str) -> None:
    page.evaluate(
        """
        async ({ html, text }) => {
          const item = new ClipboardItem({
            'text/html': new Blob([html], { type: 'text/html' }),
            'text/plain': new Blob([text], { type: 'text/plain' }),
          });
          await navigator.clipboard.write([item]);
        }
        """,
        {"html": html, "text": plain_text},
    )


def copy_html_via_browser_selection(page, html: str) -> bool:
    return bool(
        page.evaluate(
            """
            ({ html }) => {
              const prior = document.getElementById('__wechat-copy-stage');
              if (prior) prior.remove();

              const stage = document.createElement('div');
              stage.id = '__wechat-copy-stage';
              stage.contentEditable = 'true';
              stage.style.position = 'fixed';
              stage.style.left = '-99999px';
              stage.style.top = '0';
              stage.style.width = '720px';
              stage.style.opacity = '0';
              stage.style.pointerEvents = 'none';
              stage.innerHTML = html;
              document.body.appendChild(stage);

              const selection = window.getSelection();
              const range = document.createRange();
              range.selectNodeContents(stage);
              selection.removeAllRanges();
              selection.addRange(range);
              stage.focus();

              let copied = false;
              try {
                copied = document.execCommand('copy');
              } catch (error) {
                copied = false;
              }

              selection.removeAllRanges();
              stage.remove();
              return copied;
            }
            """,
            {"html": html},
        )
    )


def build_copy_source_html(blocks: list[dict]) -> str:
    rendered: list[str] = []
    for index, block in enumerate(blocks):
        if block.get("type") != "html":
            continue
        rendered.append(
            f'<section data-copy-block="{index}" '
            'style="margin:0 0 32px;padding:0;background:#fff;">'
            f'{block["html"]}'
            "</section>"
        )
    return (
        "<!doctype html><html><head><meta charset='utf-8' />"
        "<style>"
        "body{margin:0;padding:32px;background:#fff;color:#222;"
        "font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Noto Sans SC',sans-serif;}"
        "main{width:720px;margin:0 auto;}"
        "section{break-inside:avoid;}"
        "</style></head><body><main>"
        + "".join(rendered)
        + "</main></body></html>"
    )


def prepare_copy_source_page(context, manifest: dict):
    if not any(block.get("type") == "html" for block in manifest.get("body", [])):
        return None
    page = context.new_page()
    page.set_content(build_copy_source_html(manifest.get("body", [])), wait_until="domcontentloaded")
    return page


def copy_rendered_block_from_source(source_page, html_block_index: int) -> bool:
    locator = source_page.locator(f'[data-copy-block="{html_block_index}"]').first
    if locator.count() == 0:
        return False
    locator.scroll_into_view_if_needed()
    source_page.evaluate(
        """
        (index) => {
          const target = document.querySelector(`[data-copy-block="${index}"]`);
          if (!target) return false;
          const selection = window.getSelection();
          const range = document.createRange();
          range.selectNodeContents(target);
          selection.removeAllRanges();
          selection.addRange(range);
          return true;
        }
        """,
        html_block_index,
    )
    source_page.keyboard.press("Meta+C")
    source_page.wait_for_timeout(150)
    source_page.evaluate(
        """() => {
          const selection = window.getSelection();
          if (selection) selection.removeAllRanges();
        }"""
    )
    return True


def paste_rich_block(page, frame, selector: str, snippet: str) -> None:
    log(f"粘贴富文本块：{snippet[:60]}")
    focus_editor_end(frame, selector)
    plain_text = html_to_plain_text(snippet)
    copied = copy_html_via_browser_selection(page, snippet)
    if not copied:
        write_html_to_clipboard(page, snippet, plain_text)
    frame.locator(selector).first.click()
    page.keyboard.press("Meta+V")
    page.wait_for_timeout(220)
    page.keyboard.press("Enter")
    page.wait_for_timeout(120)


def paste_rendered_block(page, frame, selector: str, source_page, html_block_index: int, fallback_snippet: str) -> None:
    log(f"粘贴渲染块：index={html_block_index}")
    copied = False
    if source_page is not None:
        try:
            copied = copy_rendered_block_from_source(source_page, html_block_index)
        except Exception:
            copied = False
    if not copied:
        paste_rich_block(page, frame, selector, fallback_snippet)
        return
    focus_editor_end(frame, selector)
    frame.locator(selector).first.click()
    page.keyboard.press("Meta+V")
    page.wait_for_timeout(240)
    page.keyboard.press("Enter")
    page.wait_for_timeout(120)


def insert_plain_text_block(page, frame, selector: str, text: str) -> None:
    clean = text.strip()
    if not clean:
        return
    log(f"插入纯文本块：{clean[:60]}")
    focus_editor_end(frame, selector)
    frame.locator(selector).first.click()
    page.keyboard.insert_text(clean)
    page.wait_for_timeout(80)
    page.keyboard.press("Enter")


def minimal_rich_html(block: dict) -> str:
    text = block.get("text", "").strip()
    if not text:
        return ""
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    if block["type"] == "heading":
        return f'<p><strong>{escaped}</strong></p>'
    if block["type"] == "lead":
        return f'<p><strong>{escaped}</strong></p>'
    if block["type"] == "quote":
        return f'<blockquote>{escaped}</blockquote>'
    if block["type"] == "meta":
        return f'<p>{escaped}</p>'
    return f"<p>{escaped}</p>"
    page.wait_for_timeout(100)


def is_simple_paragraph(snippet: str) -> bool:
    stripped = snippet.strip().lower()
    return stripped.startswith("<p") and stripped.endswith("</p>")


def current_editor_image_count(frame, selector: str) -> int:
    return frame.evaluate(
        """
        (selector) => {
          const root = document.querySelector(selector);
          return root ? root.querySelectorAll('img').length : 0;
        }
        """,
        selector,
    )


def style_last_uploaded_image(frame, selector: str, width_value: str | None) -> None:
    if not width_value:
        return
    frame.evaluate(
        """
        ({ selector, widthValue }) => {
          const root = document.querySelector(selector);
          if (!root) return;
          const imgs = root.querySelectorAll('img');
          const img = imgs[imgs.length - 1];
          if (!img) return;
          img.style.display = 'block';
          img.style.width = widthValue;
          img.style.maxWidth = '100%';
          img.style.margin = '18px auto';
          img.style.height = 'auto';
        }
        """,
        {"selector": selector, "widthValue": width_value},
    )


def find_image_input(page: Page):
    for frame in [page.main_frame, *page.frames]:
        locator = frame.locator('input[type="file"]').first
        try:
            if locator.count() > 0:
                return frame, locator
        except Exception:
            continue
    return None


def click_image_toolbar(page: Page) -> None:
    labels = ["图片", "上传图片", "插入图片"]
    for label in labels:
        try:
            button = page.get_by_text(label, exact=False)
            if button.count() > 0:
                log(f"点击图片入口：{label}")
                button.first.click(timeout=600)
                page.wait_for_timeout(400)
                return
        except Exception:
            continue


def upload_image(page: Page, body_frame, body_selector: str, file_path: str, width_value: str | None = None) -> None:
    log(f"准备上传图片：{file_path}")
    focus_editor_end(body_frame, body_selector)
    before = current_editor_image_count(body_frame, body_selector)
    input_target = find_image_input(page)
    if not input_target:
        click_image_toolbar(page)
        page.wait_for_timeout(500)
        input_target = find_image_input(page)
    if not input_target:
        raise RuntimeError("没找到公众号后台的图片上传入口。")
    _, locator = input_target
    log("已找到图片 input，开始 set_input_files")
    locator.set_input_files(file_path)
    for _ in range(60):
        page.wait_for_timeout(1000)
        after = current_editor_image_count(body_frame, body_selector)
        if after > before:
            style_last_uploaded_image(body_frame, body_selector, width_value)
            log("图片上传完成")
            return
    raise RuntimeError(f"图片上传超时：{file_path}")


def save_draft(page: Page) -> bool:
    labels = ["保存为草稿", "保存草稿"]
    for label in labels:
        try:
            button = page.get_by_text(label, exact=False)
            if button.count() > 0:
                log(f"点击保存按钮：{label}")
                button.first.click(timeout=1000)
                return True
        except Exception:
            continue
    return False


def click_first_visible(page: Page, labels: list[str], timeout: int = 1200) -> bool:
    for label in labels:
        try:
            locator = page.get_by_text(label, exact=False)
            if locator.count() > 0:
                log(f"点击按钮：{label}")
                locator.first.click(timeout=timeout)
                return True
        except Exception:
            continue
    return False


def publish_article(page: Page) -> bool:
    if not click_first_visible(page, ["发布", "发表"], timeout=1500):
        return False

    page.wait_for_timeout(1000)

    # 公众号后台有时会在弹窗里再确认一次发布。
    click_first_visible(page, ["确认发布", "确认", "确定", "继续发布"], timeout=1200)
    page.wait_for_timeout(1200)
    return True


def resolve_profile_dir(profile_dir: Path) -> Path:
    profile_dir.mkdir(parents=True, exist_ok=True)
    singleton_paths = [
        profile_dir / "SingletonLock",
        profile_dir / "SingletonCookie",
        profile_dir / "SingletonSocket",
    ]
    if not any(path.exists() for path in singleton_paths):
        return profile_dir

    recovery_dir = profile_dir.parent / f"{profile_dir.name}-recovery-{int(time.time())}"
    recovery_dir.mkdir(parents=True, exist_ok=True)
    print("检测到上一次浏览器会话仍占用配置目录，已切换到新的临时浏览器会话，需要重新登录。", flush=True)
    return recovery_dir


def main() -> None:
    args = parse_args()
    global VERBOSE
    VERBOSE = args.verbose
    if args.save_draft and args.publish:
        raise SystemExit("请不要同时传 --save-draft 和 --publish。二选一就行。")

    manifest_path = Path(args.manifest).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    debug_log_path = manifest_path.parent / "publish-run.log"
    requested_profile_dir = Path(args.profile_dir).resolve() if args.profile_dir else manifest_path.parent / ".wechat-browser-profile"
    profile_dir = resolve_profile_dir(requested_profile_dir)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            str(profile_dir),
            headless=args.headless,
            viewport={"width": 1440, "height": 980},
            executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        )
        context.grant_permissions(["clipboard-read", "clipboard-write"], origin="https://mp.weixin.qq.com")
        page = context.pages[0] if context.pages else context.new_page()
        should_close_context = True
        try:
            page.goto(args.url, wait_until="domcontentloaded")
            print("如果还没登录，请先扫码登录并打开“新建图文”页面。脚本会自动等待。", flush=True)
            append_debug_log(debug_log_path, f"启动发布流程：manifest={manifest_path}")

            page, title_target, body_target = ensure_editor_ready(context)
            copy_source_page = prepare_copy_source_page(context, manifest) if manifest.get("mode") == "wechat-copy-native" else None
            title_frame, title_selector = title_target
            body_frame, body_selector = body_target
            fill_text_target(title_frame, title_selector, manifest["title"])

            author = (manifest.get("author") or "").strip()
            if author:
                author_target = mark_best_target(page, "author", ["作者", "author", "请输入作者"]) or mark_fallback_target(page, "author")
                if author_target:
                    author_frame, author_selector = author_target
                    fill_text_target(author_frame, author_selector, author)

            for idx, block in enumerate(manifest["body"], 1):
                log(f"处理第 {idx}/{len(manifest['body'])} 个内容块：{block['type']}")
                append_debug_log(debug_log_path, f"处理内容块 {idx}/{len(manifest['body'])}: {block['type']}")
                if manifest.get("mode") == "wechat-copy-native" and block["type"] == "html":
                    paste_rendered_block(page, body_frame, body_selector, copy_source_page, idx - 1, block["html"])
                elif block["type"] in {"heading", "lead", "quote", "meta"}:
                    paste_rich_block(page, body_frame, body_selector, minimal_rich_html(block))
                elif block["type"] == "text":
                    insert_plain_text_block(page, body_frame, body_selector, block["text"])
                elif block["type"] == "html":
                    if manifest.get("mode") == "native-editable":
                        insert_plain_text_block(page, body_frame, body_selector, html_to_plain_text(block["html"]))
                    elif is_simple_paragraph(block["html"]) or block["html"].strip().lower().startswith(("<h2", "<blockquote", "<ol", "<ul")):
                        paste_rich_block(page, body_frame, body_selector, block["html"])
                    else:
                        insert_html(body_frame, body_selector, block["html"])
                elif block["type"] == "image":
                    upload_image(page, body_frame, body_selector, block["file"], block.get("display_width"))
                page.wait_for_timeout(220)

            if args.publish:
                if publish_article(page):
                    print("已尝试直接发布。发布前如果后台弹出额外校验，请你手动补一下。", flush=True)
                else:
                    print("没有找到“发布”按钮，请手动确认。", flush=True)
            elif args.save_draft:
                if save_draft(page):
                    print("已尝试保存为草稿。", flush=True)
                else:
                    print("没有找到“保存为草稿”按钮，请手动确认。", flush=True)
            else:
                print("内容已灌入编辑器，未自动保存。", flush=True)

            print("脚本已完成。你现在可以预览、补视频，再手动发布。", flush=True)
            if not args.headless and (args.keep_open or (not args.save_draft and not args.publish)):
                try:
                    page.wait_for_timeout(15 * 60 * 1000)
                except TimeoutError:
                    pass
        except Exception as exc:
            error_text = traceback.format_exc()
            append_debug_log(debug_log_path, f"发布异常：{exc}\n{error_text}")
            print(f"灌稿过程中出错：{exc}", flush=True)
            if not args.headless:
                should_close_context = False
                print(f"我已经把错误日志写到：{debug_log_path}", flush=True)
                print("浏览器会保留，不会自动关闭。你可以直接看后台现场，确认后手动关浏览器就行。", flush=True)
            raise
        finally:
            if should_close_context:
                context.close()


if __name__ == "__main__":
    main()
