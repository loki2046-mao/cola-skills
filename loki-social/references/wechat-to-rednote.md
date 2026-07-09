# WeChat To Rednote Conversion

Use this file whenever the source is a 微信公众号长文, newsletter draft, long Markdown article, or any article intended for a long-scroll reading experience. The goal is not to summarize the article; the goal is to extract a Rednote-native carousel with one shareable argument, visible proof, and a caption that carries the extra nuance.

## Conversion Rule

A WeChat article usually has room for setup, background, process, examples, caveats, and links. A Rednote carousel does not. Convert by separating content into four buckets:

| Bucket | Put In Images | Put In Caption | Put In Pinned Comment | Cut |
|--------|---------------|----------------|------------------------|-----|
| Hook | the strongest pain, contradiction, or personal observation | one short origin story | no | weak abstract intro |
| Proof | screenshots, report excerpts, before/after, numbers, visible artifacts | source caveats, longer explanation | install links, full prompt | repeated proof |
| Action | one prompt, one checklist, one workflow, one CTA | usage details | copyable prompt/template | full tutorial text |
| Trust | author's real role, practical judgment, concrete examples | why this was made | GitHub/path/download | generic authority claims |

## Compression Flow

1. **Find the human angle**
   - Keep sentences where the author says "我看过/我做过/我发现/我觉得".
   - Prefer firsthand observations over general claims.
   - If the article promotes a tool, lead with the user pain or result, not the tool name.

2. **Find the evidence objects**
   - Choose 2-4 visible proof objects: screenshot, before/after, table fragment, output excerpt, report card, workflow result, code window, or file stack.
   - If no real screenshot exists, create a clearly labeled demo/report excerpt. Do not imply it is a real product screenshot.
   - Evidence must appear by page 4 at the latest.

3. **Choose the 7-9 image points**
   - Page 1: hook cover.
   - Page 2: reader pain or why this matters now.
   - Page 3: core insight or tool promise.
   - Page 4: input/prompt or setup.
   - Page 5-7: proof pages, before/after, case, score, or workflow.
   - Page 8: how to use/install/get.
   - Page 9: closing thesis and CTA.
   - If fewer than 7 strong points exist, make 6 pages. Do not pad.

4. **Move long-tail content out of images**
   - Installation commands, long links, long prompt templates, background story, and caveats go to caption or pinned comment.
   - Images should be readable at phone size. A dense page needs either a screenshot/excerpt or a short ledger, not a full paragraph.

5. **Write a deck plan before HTML**
   Use this exact internal plan shape:

```text
Article knife:
Audience:
What images carry:
What caption carries:
What pinned comment carries:
Evidence pages:
Page plan:
P1 / role / key sentence / component / evidence
...
```

## Rednote-Native Page Roles

Use these page roles instead of copying article sections:

- **Pain**: "这类人为什么会停下来".
- **Recognition**: "他会不会觉得这说的是我".
- **Proof**: "我凭什么相信你".
- **Transformation**: "原来怎样，后来怎样".
- **Use**: "我怎么照着做".
- **Save**: "这页为什么值得收藏".
- **CTA**: "下一步去哪里、发什么、评论什么".

## Visual Rules For Article Conversion

- Do not make every page an excerpt card. Long articles need rhythm: large hook, proof crop, comparison, checklist, artifact, closing.
- Do not let a pale beige/yellow article aesthetic dominate. Default to bright, clean, youthful backgrounds unless the source explicitly needs archival/vintage.
- Do not crop screenshots halfway through text. If a screenshot is too dense, show a designed excerpt and label it as an excerpt.
- Do not overuse table pages. Two dense tables maximum in one carousel.
- The carousel must look like one set. Keep the same page chrome, type scale, border language, and accent system.

## Caption Requirements

The caption should carry what images cannot:

1. Why the author made this.
2. The concrete pain.
3. What the tool/method actually does.
4. One copyable prompt or usage path.
5. Tags.

Avoid making the caption a second full article. Keep paragraphs short.

