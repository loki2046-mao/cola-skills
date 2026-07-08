#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import re
from pathlib import Path


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff_-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def next_version(vault: Path, prefix: str, theme_slug: str) -> int:
    pattern = re.compile(rf"^{re.escape(prefix)}-v(\d{{3}})-{re.escape(theme_slug)}\.md$")
    max_v = 0
    for p in vault.glob(f"{prefix}-v*-{theme_slug}.md"):
        m = pattern.match(p.name)
        if m:
            max_v = max(max_v, int(m.group(1)))
    return max_v + 1


def read_prompt_text(prompt: str | None, prompt_file: str | None) -> str:
    if prompt_file:
        return Path(prompt_file).read_text(encoding="utf-8").strip()
    if prompt:
        return prompt.strip()
    raise ValueError("Either --prompt or --prompt-file is required")


def main() -> None:
    parser = argparse.ArgumentParser(description="Save generated prompts to Obsidian vault")
    parser.add_argument("--theme", required=True)
    parser.add_argument("--task-type", required=True, choices=["image", "poster", "character", "toy", "ui"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--version", default="auto", help="auto or 3-digit version like 001")
    parser.add_argument("--vault-path", default=os.path.expanduser("~/prompts-vault"))
    parser.add_argument("--prompt", default=None)
    parser.add_argument("--prompt-file", default=None)
    parser.add_argument("--tags", default="提示词,nb-image-prompt")
    args = parser.parse_args()

    vault = Path(args.vault_path)
    vault.mkdir(parents=True, exist_ok=True)

    now = dt.datetime.now()
    date_prefix = now.strftime("%Y%m%d-%H%M")
    theme_slug = slugify(args.theme)

    if args.version == "auto":
        version_num = next_version(vault, date_prefix, theme_slug)
    else:
        version_num = int(args.version)

    version = f"v{version_num:03d}"
    filename = f"{date_prefix}-{version}-{theme_slug}.md"
    target = vault / filename

    prompt_text = read_prompt_text(args.prompt, args.prompt_file)
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]

    frontmatter = "\n".join(
        [
            "---",
            f'theme: "{args.theme}"',
            f'task_type: "{args.task_type}"',
            f'model: "{args.model}"',
            f'version: "{version}"',
            f'created_at: "{now.strftime("%Y-%m-%d %H:%M:%S")}"',
            f"tags: [{', '.join(tags)}]",
            "---",
            "",
        ]
    )

    body = (
        f"# {args.theme}\n\n"
        f"> 生成时间: {now.strftime('%Y-%m-%d %H:%M')}\n"
        f"> 文件: {filename}\n\n"
        "## Prompt\n\n"
        f"{prompt_text}\n"
    )

    target.write_text(frontmatter + body, encoding="utf-8")
    print(str(target))


if __name__ == "__main__":
    main()
