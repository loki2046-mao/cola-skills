#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
RICH_PASTE = SCRIPTS


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, check=False, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def parse_printed_kv(output_path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not output_path.exists():
        return data
    raw = output_path.read_text(encoding="utf-8").strip()
    if not raw:
        return data
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {str(k): str(v) for k, v in parsed.items()}
    except json.JSONDecodeError:
        pass
    for line in raw.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="从公开飞书文档一键生成微信公众号发布包，并可选直接灌进公众号后台。")
    parser.add_argument("--url", required=True, help="公开飞书文档链接")
    parser.add_argument("--footer-image", default=str(ROOT / "assets" / "signature.png"), help="文末固定关注图，传不存在路径可禁用")
    parser.add_argument(
        "--mode",
        choices=["wechat-copy-native", "wechat-copy-page", "high-fidelity", "native-editable"],
        default="wechat-copy-native",
        help="wechat-copy-native=原生文字+原生图片自动灌入；wechat-copy-page=生成微信复制页；high-fidelity=优先保真和美观；native-editable=旧实验模式",
    )
    parser.add_argument("--publish", action="store_true", help="生成后直接尝试发布")
    parser.add_argument("--save-draft", action="store_true", help="生成后直接尝试保存草稿")
    parser.add_argument("--keep-open", action="store_true", help="灌稿后保留浏览器")
    parser.add_argument("--verbose", action="store_true", help="输出详细日志")
    args = parser.parse_args()

    extract_log = ROOT / "tmp-feishu-extract.log"
    build_log = ROOT / "tmp-feishu-build.log"
    package_log = ROOT / "tmp-feishu-package.log"

    with extract_log.open("w", encoding="utf-8") as handle:
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "extract_public_feishu_doc.py"), "--url", args.url],
            check=False,
            text=True,
            stdout=handle,
        )
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    extracted = parse_printed_kv(extract_log)
    article_dir = Path(extracted["output_dir"])
    json_path = Path(extracted["json"])

    with build_log.open("w", encoding="utf-8") as handle:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "build_wechat_native_from_feishu.py"),
                "--input",
                str(json_path),
                "--footer-image",
                args.footer_image,
            ],
            check=False,
            text=True,
            stdout=handle,
        )
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    built = parse_printed_kv(build_log)
    manifest = Path(built["MANIFEST"])
    preview = Path(built["PREVIEW"])
    copy_source = Path(built.get("COPY_SOURCE", article_dir / "公众号后台复制源.html"))

    if args.mode == "high-fidelity":
        with package_log.open("w", encoding="utf-8") as handle:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "build_wechat_publish_package.py"),
                    "--input",
                    str(preview),
                    "--mode",
                    "high-fidelity",
                    "--footer-image",
                    args.footer_image,
                    "--output-dir",
                    str(article_dir / ".wechat-publish-package-fidelity"),
                ],
                check=False,
                text=True,
                stdout=handle,
            )
        if result.returncode != 0:
            raise SystemExit(result.returncode)
        packaged = parse_printed_kv(package_log)
        manifest = Path(packaged["MANIFEST"])
        preview = Path(packaged["PREVIEW"])

    print(json.dumps(
        {
            "article_dir": str(article_dir),
            "json": str(json_path),
            "manifest": str(manifest),
            "preview": str(preview),
            "copy_source": str(copy_source),
            "mode": args.mode,
        },
        ensure_ascii=False,
        indent=2,
    ))

    if args.mode == "wechat-copy-page":
        copy_output = article_dir / "公众号后台公网图片复制版.html"
        run(
            [
                "node",
                str(RICH_PASTE / "start-wechat-public-share.mjs"),
                "--article-dir",
                str(article_dir),
                "--input",
                str(copy_source),
                "--output",
                str(copy_output),
                "--preserve-inline",
            ]
        )
        return

    if args.publish or args.save_draft:
        cmd = [
            sys.executable,
            str(SCRIPTS / "publish_to_wechat.py"),
            "--manifest",
            str(manifest),
        ]
        if args.publish:
            cmd.append("--publish")
        if args.save_draft:
            cmd.append("--save-draft")
        if args.keep_open:
            cmd.append("--keep-open")
        if args.verbose:
            cmd.append("--verbose")
        run(cmd)


if __name__ == "__main__":
    main()
