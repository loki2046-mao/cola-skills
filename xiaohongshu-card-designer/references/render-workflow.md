# Render Workflow

## Folder Shape

For every task, create:

```text
xhs-<slug>/
  index.html
  assets/
  output/
```

Copy `assets/xhs-seed.html` to `index.html`, then replace the sample sections with planned pages.

For reliable screenshot export, keep the render page as a single vertical column. Do not apply `transform: scale(...)`, CSS zoom, or auto-fit grid layouts to `.poster`; Playwright will screenshot the transformed or overlapped layout.

## Render Command

Preferred:

```bash
node ./scripts/render.mjs xhs-<slug>
```

The script screenshots every `.poster` node and writes PNGs into `output/`.

## Playwright Fallbacks

If `import "playwright"` fails:

1. Try running with a Node environment that has Playwright installed.
2. If Playwright browser cache is missing, use system Chrome by passing `CHROME_PATH`:

```bash
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" node ./scripts/render.mjs xhs-<slug>
```

3. In Codex runtime, use the bundled Node executable if available.

```bash
PLAYWRIGHT_MODULE=/path/to/node_modules/playwright/index.js \
CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
node ./scripts/render.mjs xhs-<slug>
```

## QA

After render:

- Inspect cover.
- Inspect the densest text page.
- Inspect at least one evidence/screenshot page.
- Inspect install/CTA page if the carousel promotes a Skill, tool, GitHub repo, or workflow.
- Inspect the whole deck as a set, preferably by opening 3-4 representative PNGs side by side.
- Check that each PNG contains only one page and is not contaminated by adjacent posters.
- Run a size check (`sips -g pixelWidth -g pixelHeight output/*.png` on macOS).

## Hard Failure Conditions

Revise and rerender if any condition appears:

- Background reads as old paper, pale yellow, beige, dusty orange, or muddy vintage when the topic is student/career/AI/tool.
- Any screenshot/report/table is cropped halfway through a sentence or too small to inspect.
- The deck looks like unrelated templates rather than one carousel.
- More than two pages use the same title + paragraph + card structure.
- A page has a large empty region with no counterweight from type, evidence, or image mass.
- The first 4 pages do not show any evidence for a tool/Skill/product claim.
- The cover depends on vague AI-product words instead of a concrete reader pain.

## Deliverable Check

Before final response, confirm:

- `index.html` exists.
- `output/` contains ordered PNGs.
- All PNGs are `1080 x 1440`.
- A publish copy file or final response includes title, caption, tags, and optional pinned comment.
- If screenshots are mocked, the card labels them as demo/mock/report excerpt and does not imply real UI capture.

Deliver a clean folder if multiple drafts exist, e.g. `output-final/`.
