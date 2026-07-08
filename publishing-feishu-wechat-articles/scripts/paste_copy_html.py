"""
把 copy.html 完整内容（含样式/图片）通过浏览器选中+复制，粘贴进微信公众号编辑器。
用法：
  python3 paste_copy_html.py \
    --copy-html /path/to/copy.html \
    --url "https://mp.weixin.qq.com/..." \
    --title "文章标题" \
    --save-draft
"""
import argparse, json, time
from pathlib import Path
from urllib.request import pathname2url
from playwright.sync_api import sync_playwright

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--copy-html", required=True, help="copy.html 绝对路径")
    p.add_argument("--url", default="https://mp.weixin.qq.com/", help="微信后台编辑器 URL")
    p.add_argument("--title", default="", help="文章标题（可选）")
    p.add_argument("--save-draft", action="store_true")
    p.add_argument("--keep-open", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    copy_html = Path(args.copy_html).resolve()
    profile_dir = copy_html.parent / ".wechat-browser-profile"
    profile_dir.mkdir(parents=True, exist_ok=True)

    file_url = "file://" + pathname2url(str(copy_html))

    with sync_playwright() as pw:
        ctx = pw.chromium.launch_persistent_context(
            str(profile_dir),
            headless=False,
            executable_path=CHROME,
            viewport={"width": 1440, "height": 980},
        )
        ctx.grant_permissions(["clipboard-read", "clipboard-write"],
                              origin="https://mp.weixin.qq.com")

        # 页面1：copy.html（用来选中复制）
        src_page = ctx.new_page()
        src_page.goto(file_url, wait_until="networkidle")
        src_page.wait_for_timeout(1500)

        # 全选 #wx-article 内的内容
        src_page.evaluate("""
            () => {
                const article = document.querySelector('#wx-article') || document.querySelector('main');
                if (!article) { console.error('找不到正文区域'); return; }
                const sel = window.getSelection();
                const range = document.createRange();
                range.selectNodeContents(article);
                sel.removeAllRanges();
                sel.addRange(range);
            }
        """)
        src_page.keyboard.press("Meta+C")
        src_page.wait_for_timeout(500)
        print("[paste] 已复制 copy.html 正文到剪贴板")

        # 页面2：微信后台编辑器
        wx_page = ctx.new_page()
        wx_page.goto(args.url, wait_until="domcontentloaded")
        wx_page.wait_for_timeout(3000)

        # 等编辑器加载
        body_sel = None
        for frame in wx_page.frames:
            loc = frame.locator('[data-wechat-publisher-body="1"], #ueditor_0, .ql-editor, [contenteditable="true"]').first
            if loc.count() > 0:
                body_sel = loc
                print(f"[paste] 找到正文编辑区，frame={frame.name}")
                break

        if not body_sel:
            print("[paste] 未找到正文编辑区，请确认已打开新建图文页面")
            if not args.keep_open:
                ctx.close()
            return

        # 写标题
        if args.title:
            for frame in wx_page.frames:
                title_loc = frame.locator('[data-wechat-publisher-title="1"]').first
                if title_loc.count() > 0:
                    title_loc.click()
                    title_loc.fill(args.title)
                    print(f"[paste] 写入标题：{args.title[:30]}")
                    break

        # 点击正文区，粘贴
        body_sel.click()
        wx_page.keyboard.press("Meta+A")
        wx_page.wait_for_timeout(200)
        wx_page.keyboard.press("Meta+V")
        wx_page.wait_for_timeout(2000)
        print("[paste] 已粘贴正文内容")

        # 保存草稿
        if args.save_draft:
            for frame in wx_page.frames:
                save_btn = frame.get_by_text("保存为草稿", exact=False).first
                if save_btn.count() > 0:
                    save_btn.click()
                    wx_page.wait_for_timeout(1500)
                    print("[paste] 已保存草稿")
                    break

        print("[paste] 完成。")
        if args.keep_open:
            print("[paste] 浏览器保留中，手动关闭即可。")
            input("按 Enter 关闭浏览器...")
        ctx.close()


if __name__ == "__main__":
    main()
