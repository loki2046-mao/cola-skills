#!/usr/bin/env node
import fs from "node:fs/promises";
import { existsSync, statSync } from "node:fs";
import path from "node:path";

async function loadPlaywright() {
  try {
    const mod = await import("playwright");
    return mod.default ?? mod;
  } catch (error) {
    const bundled = process.env.PLAYWRIGHT_MODULE;
    if (bundled) {
      const mod = await import(bundled);
      return mod.default ?? mod;
    }
    throw error;
  }
}

const targetArg = process.argv[2] || ".";
const targetPath = path.resolve(targetArg);
const htmlPath = statSync(targetPath).isDirectory()
  ? path.join(targetPath, "index.html")
  : targetPath;

if (!existsSync(htmlPath)) {
  console.error(`index.html not found: ${htmlPath}`);
  process.exit(2);
}

const taskDir = path.dirname(htmlPath);
const outputDir = path.join(taskDir, "output");
await fs.mkdir(outputDir, { recursive: true });

const { chromium } = await loadPlaywright();
const launchOptions = {
  args: ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"],
};
if (process.env.CHROME_PATH) launchOptions.executablePath = process.env.CHROME_PATH;

const browser = await chromium.launch(launchOptions);
const page = await browser.newPage({
  viewport: { width: 1280, height: 1600 },
  deviceScaleFactor: 1,
});

await page.goto(`file://${htmlPath}`, { waitUntil: "domcontentloaded" });
await page.evaluate(async () => {
  if (document.fonts?.ready) await document.fonts.ready;
  const imgs = [...document.images];
  await Promise.all(imgs.map((img) => {
    if (img.complete) return Promise.resolve();
    return new Promise((resolve) => {
      img.addEventListener("load", resolve, { once: true });
      img.addEventListener("error", resolve, { once: true });
    });
  }));
});
await page.waitForTimeout(300);

const posters = await page.$$eval(".poster", (nodes) =>
  nodes.map((node, index) => ({
    id: node.id || `poster-${String(index + 1).padStart(2, "0")}`,
    name: node.dataset.exportName || `xhs-${String(index + 1).padStart(2, "0")}.png`,
    index,
    hasId: Boolean(node.id),
  }))
);

if (!posters.length) {
  console.error("No .poster nodes found.");
  await browser.close();
  process.exit(1);
}

for (const poster of posters) {
  const locator = poster.hasId
    ? page.locator(`#${poster.id}`)
    : page.locator(".poster").nth(poster.index);
  const outPath = path.join(outputDir, poster.name);
  await locator.screenshot({ path: outPath, type: "png" });
  const box = await locator.boundingBox();
  console.log(`${poster.name} ${Math.round(box.width)}x${Math.round(box.height)} -> ${outPath}`);
}

await browser.close();
