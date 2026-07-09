#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import parse_qs, quote, urlsplit
from uuid import uuid4

import feishu_to_copy_page as layout


ROOT = layout.ROOT.resolve()
WEB_ROOT = Path(__file__).resolve().parent / "web"
DOCUMENTS: dict[str, dict] = {}


def ensure_within_root(raw_path: str) -> Path:
  if not raw_path:
    raise ValueError("缺少路径")
  resolved = Path(raw_path).expanduser().resolve()
  try:
    resolved.relative_to(ROOT)
  except ValueError as exc:
    raise ValueError("路径必须在工作区里") from exc
  return resolved


def load_article_payload(path: Path) -> dict:
  target = path
  if target.is_dir():
    target = target / "article.json"
  if not target.exists():
    raise FileNotFoundError(f"找不到文件：{target}")
  data = json.loads(target.read_text(encoding="utf-8"))
  if isinstance(data, dict) and "article" in data and "title" in data:
    article = data["article"]
    title = data["title"]
    source_url = data.get("source_url", "")
  elif isinstance(data, dict) and "blocks" in data:
    article = data
    title = article.get("title") or target.parent.name
    source_url = ""
  else:
    raise ValueError("article.json 结构不对")
  return {
    "title": title,
    "source_url": source_url,
    "article": article,
    "output_dir": str(target.parent.resolve()),
    "article_json": str(target.resolve()),
  }


def data_url_to_bytes(data_url: str) -> tuple[str, bytes]:
  header, encoded = data_url.split(",", 1)
  mime = header[5:].split(";")[0] if header.startswith("data:") else "application/octet-stream"
  return mime, base64.b64decode(encoded)


def register_document(title: str, article: dict, *, source_url: str = "", output_dir: str = "", article_json: str = "") -> dict:
  doc_id = uuid4().hex[:12]
  assets: dict[str, str] = {}
  editor_blocks: list[dict] = []

  for block in article.get("blocks", []):
    editor_block = json.loads(json.dumps(block, ensure_ascii=False))
    if editor_block.get("type") == "image":
      src = editor_block.get("src", "")
      if isinstance(src, str) and src.startswith("data:"):
        asset_id = uuid4().hex[:12]
        assets[asset_id] = src
        editor_block["src"] = f"/api/doc-image?doc_id={doc_id}&asset_id={asset_id}"
    editor_blocks.append(editor_block)

  DOCUMENTS[doc_id] = {
    "title": title,
    "source_url": source_url,
    "article": article,
    "assets": assets,
    "editor_article": {
      "title": title,
      "blocks": editor_blocks,
    },
  }

  return {
    "doc_id": doc_id,
    "title": title,
    "source_url": source_url,
    "article": DOCUMENTS[doc_id]["editor_article"],
    "output_dir": output_dir,
    "article_json": article_json,
    "block_count": len(editor_blocks),
  }


def resolve_editor_image_src(src: str) -> str:
  if not isinstance(src, str):
    return src
  parsed = urlsplit(src)
  route = parsed.path or src
  if route != "/api/doc-image":
    return src
  query = parse_qs(parsed.query)
  doc_id = query.get("doc_id", [""])[0]
  asset_id = query.get("asset_id", [""])[0]
  asset = DOCUMENTS.get(doc_id, {}).get("assets", {}).get(asset_id)
  return asset or src


def resolve_editor_article(article: dict) -> dict:
  resolved = {
    "title": article.get("title", ""),
    "blocks": [],
  }
  for block in article.get("blocks", []):
    next_block = json.loads(json.dumps(block, ensure_ascii=False))
    if next_block.get("type") == "image":
      next_block["src"] = resolve_editor_image_src(next_block.get("src", ""))
    resolved["blocks"].append(next_block)
  return resolved


def fetch_remote_image_data_url(src: str) -> str:
  request = Request(
    src,
    headers={
      "User-Agent": "Mozilla/5.0 Codex SvgWechatLayout/1.0",
      "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
      "Referer": "https://www.feishu.cn/",
    },
  )
  with urlopen(request, timeout=15) as response:
    content = response.read()
    mime = response.headers.get_content_type() or mimetypes.guess_type(src)[0] or "image/png"
  return f"data:{mime};base64,{base64.b64encode(content).decode('ascii')}"


def inline_remote_images(article: dict) -> dict:
  cache: dict[str, str] = {}
  resolved = {
    "title": article.get("title", ""),
    "blocks": [],
  }
  for block in article.get("blocks", []):
    next_block = json.loads(json.dumps(block, ensure_ascii=False))
    if next_block.get("type") == "image":
      src = next_block.get("src", "")
      if isinstance(src, str) and src.startswith(("http://", "https://")):
        if src not in cache:
          try:
            cache[src] = fetch_remote_image_data_url(src)
          except Exception:
            cache[src] = src
        next_block["src"] = cache[src]
    resolved["blocks"].append(next_block)
  return resolved


def json_bytes(payload: dict) -> bytes:
  return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def serve_file(handler: BaseHTTPRequestHandler, file_path: Path, content_type: str | None = None) -> None:
  if not file_path.exists() or not file_path.is_file():
    handler.send_error(HTTPStatus.NOT_FOUND, "Not Found")
    return
  mime = content_type or mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
  content = file_path.read_bytes()
  handler.send_response(HTTPStatus.OK)
  handler.send_header("Content-Type", f"{mime}; charset=utf-8" if mime.startswith("text/") else mime)
  handler.send_header("Cache-Control", "no-store")
  handler.send_header("Content-Length", str(len(content)))
  handler.end_headers()
  handler.wfile.write(content)


class EditorHandler(BaseHTTPRequestHandler):
  server_version = "SvgWechatEditor/0.1"

  def log_message(self, fmt: str, *args: object) -> None:
    print(f"[editor] {self.address_string()} - {fmt % args}")

  def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
    body = json_bytes(payload)
    self.send_response(status)
    self.send_header("Content-Type", "application/json; charset=utf-8")
    self.send_header("Cache-Control", "no-store")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def send_text(self, text: str, status: HTTPStatus = HTTPStatus.OK, content_type: str = "text/plain; charset=utf-8") -> None:
    body = text.encode("utf-8")
    self.send_response(status)
    self.send_header("Content-Type", content_type)
    self.send_header("Cache-Control", "no-store")
    self.send_header("Content-Length", str(len(body)))
    self.end_headers()
    self.wfile.write(body)

  def read_json(self) -> dict:
    content_length = int(self.headers.get("Content-Length", "0") or 0)
    raw = self.rfile.read(content_length) if content_length else b"{}"
    return json.loads(raw.decode("utf-8") or "{}")

  def file_url(self, path: Path) -> str:
    return f"/api/file?path={quote(str(path.resolve()), safe='')}"

  def do_GET(self) -> None:
    parsed = urlsplit(self.path)
    route = parsed.path
    query = parse_qs(parsed.query)

    if route in {"/", "/editor", "/editor/"}:
      serve_file(self, WEB_ROOT / "editor.html", "text/html")
      return

    if route == "/favicon.ico":
      self.send_response(HTTPStatus.NO_CONTENT)
      self.end_headers()
      return

    if route.startswith("/assets/"):
      asset_path = WEB_ROOT / route.removeprefix("/assets/")
      serve_file(self, asset_path)
      return

    if route == "/api/health":
      self.send_json({"ok": True})
      return

    if route == "/api/load":
      try:
        doc_id = query.get("doc_id", [""])[0]
        if doc_id:
          document = DOCUMENTS.get(doc_id)
          if not document:
            raise ValueError("找不到这个编辑会话")
          self.send_json(
            {
              "ok": True,
              "doc_id": doc_id,
              "title": document["title"],
              "source_url": document.get("source_url", ""),
              "article": document["editor_article"],
              "output_dir": "",
              "article_json": "",
              "block_count": len(document["editor_article"].get("blocks", [])),
            }
          )
        else:
          raw_path = query.get("path", [""])[0]
          payload = load_article_payload(ensure_within_root(raw_path))
          editor_payload = register_document(
            payload["title"],
            payload["article"],
            source_url=payload.get("source_url", ""),
            output_dir=payload.get("output_dir", ""),
            article_json=payload.get("article_json", ""),
          )
          self.send_json({"ok": True, **editor_payload})
      except Exception as exc:  # noqa: BLE001
        self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)
      return

    if route == "/api/file":
      try:
        raw_path = query.get("path", [""])[0]
        serve_file(self, ensure_within_root(raw_path))
      except Exception as exc:  # noqa: BLE001
        self.send_text(str(exc), HTTPStatus.BAD_REQUEST)
      return

    if route == "/api/doc-image":
      try:
        doc_id = query.get("doc_id", [""])[0]
        asset_id = query.get("asset_id", [""])[0]
        data_url = DOCUMENTS.get(doc_id, {}).get("assets", {}).get(asset_id)
        if not data_url:
          self.send_error(HTTPStatus.NOT_FOUND, "Not Found")
          return
        mime, content = data_url_to_bytes(data_url)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
      except Exception as exc:  # noqa: BLE001
        self.send_text(str(exc), HTTPStatus.BAD_REQUEST)
      return

    self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

  def do_POST(self) -> None:
    parsed = urlsplit(self.path)
    route = parsed.path

    try:
      payload = self.read_json()
    except Exception as exc:  # noqa: BLE001
      self.send_json({"ok": False, "error": f"JSON 解析失败：{exc}"}, HTTPStatus.BAD_REQUEST)
      return

    if route == "/api/import-feishu":
      self.handle_import_feishu(payload)
      return

    if route == "/api/render":
      self.handle_render(payload)
      return

    if route == "/api/auto-layout":
      self.handle_auto_layout(payload)
      return

    if route == "/api/save":
      self.handle_save(payload)
      return

    self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

  def handle_import_feishu(self, payload: dict) -> None:
    started_at = time.time()
    try:
      url = (payload.get("url") or "").strip()
      if not url:
        raise ValueError("请先填飞书文档链接")
      print(f"[editor] import start url={url}")
      footer_image = Path(payload.get("footer_image") or layout.DEFAULT_FOOTER).resolve()
      title, raw_blocks, image_data = layout.extract_from_feishu(url, fetch_images=True)
      article = layout.normalize_article(title, raw_blocks, image_data, layout.footer_data_url(footer_image))
      output_dir = payload.get("output_dir", "").strip()
      resolved_output = ensure_within_root(output_dir) if output_dir else layout.default_output_dir(title)
      editor_payload = register_document(title, article, source_url=url, output_dir=str(resolved_output))
      print(f"[editor] import done title={title} blocks={len(article.get('blocks', []))} elapsed={time.time() - started_at:.2f}s")
      self.send_json({"ok": True, **editor_payload})
    except Exception as exc:  # noqa: BLE001
      print(f"[editor] import failed elapsed={time.time() - started_at:.2f}s error={exc}")
      self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)

  def handle_render(self, payload: dict) -> None:
    try:
      title = (payload.get("title") or "未命名文章").strip() or "未命名文章"
      article = payload.get("article") or {"title": title, "blocks": []}
      article["title"] = title
      if payload.get("resolve_assets"):
        article = resolve_editor_article(article)
        article = inline_remote_images(article)
      interactive_preview = bool(payload.get("interactive_preview", True))
      copy_prompt_hint = bool(payload.get("copy_prompt_hint", False))
      preview_prompt_hint = bool(payload.get("preview_prompt_hint", True))
      bundle = layout.render_output_bundle(
        title,
        article,
        interactive_preview=interactive_preview,
        copy_prompt_hint=copy_prompt_hint,
        preview_prompt_hint=preview_prompt_hint,
      )
      self.send_json({"ok": True, **bundle})
    except Exception as exc:  # noqa: BLE001
      self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)

  def handle_auto_layout(self, payload: dict) -> None:
    try:
      title = (payload.get("title") or "未命名文章").strip() or "未命名文章"
      article = payload.get("article") or {"title": title, "blocks": []}
      article["title"] = title
      next_article = layout.auto_layout_article(article)
      self.send_json({"ok": True, "article": next_article})
    except Exception as exc:  # noqa: BLE001
      self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)

  def handle_save(self, payload: dict) -> None:
    try:
      title = (payload.get("title") or "未命名文章").strip() or "未命名文章"
      article = payload.get("article") or {"title": title, "blocks": []}
      article["title"] = title
      article = resolve_editor_article(article)
      article = inline_remote_images(article)
      source_url = (payload.get("source_url") or "").strip()
      output_dir_raw = (payload.get("output_dir") or "").strip()
      output_dir = ensure_within_root(output_dir_raw) if output_dir_raw else layout.default_output_dir(title)
      save_payload = layout.build_payload(title, article, source_url=source_url)
      layout.write_outputs(output_dir, save_payload)
      article_json_path = output_dir / "article.json"
      preview_path = output_dir / "preview.html"
      copy_path = output_dir / "copy.html"
      self.send_json(
        {
          "ok": True,
          "title": title,
          "output_dir": str(output_dir),
          "article_json": str(article_json_path),
          "preview": str(preview_path),
          "copy": str(copy_path),
          "preview_url": self.file_url(preview_path),
          "copy_url": self.file_url(copy_path),
        }
      )
    except Exception as exc:  # noqa: BLE001
      self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.BAD_REQUEST)


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="自研公众号排版编辑器")
  parser.add_argument("--host", default="127.0.0.1", help="监听地址")
  parser.add_argument("--port", default=8789, type=int, help="监听端口")
  parser.add_argument("--article-json", default="", help="启动后预载入的 article.json 路径")
  return parser.parse_args()


def main() -> None:
  args = parse_args()
  server = ThreadingHTTPServer((args.host, args.port), EditorHandler)
  base_url = f"http://{args.host}:{args.port}/"
  if args.article_json:
    loaded = load_article_payload(ensure_within_root(args.article_json))
    preloaded = register_document(
      loaded["title"],
      loaded["article"],
      source_url=loaded.get("source_url", ""),
      output_dir=loaded.get("output_dir", ""),
      article_json=loaded.get("article_json", ""),
    )
    base_url = f"{base_url}?doc_id={quote(preloaded['doc_id'], safe='')}"
  print(json.dumps({"url": base_url, "host": args.host, "port": args.port}, ensure_ascii=False, indent=2))
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass
  finally:
    server.server_close()


if __name__ == "__main__":
  main()
