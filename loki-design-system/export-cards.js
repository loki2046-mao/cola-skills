const { chromium } = require('playwright');
const path = require('path');

const htmlFile = process.argv[2] || 'cards.html';
const prefix = process.argv[3] || 'card';

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  });
  const page = await browser.newPage();
  
  await page.setViewportSize({ width: 1200, height: 2000 });
  
  const htmlPath = path.join(__dirname, htmlFile);
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
  
  await page.waitForTimeout(4000);
  
  // Auto-detect card IDs from the page
  const cardElements = await page.locator('.card[id]').all();
  const outputDir = path.join(__dirname, 'images');
  
  for (let i = 0; i < cardElements.length; i++) {
    const outputPath = path.join(outputDir, `${prefix}-${i + 1}.png`);
    await cardElements[i].screenshot({ path: outputPath, type: 'png' });
    console.log(`Saved ${prefix}-${i + 1}.png`);
  }
  
  await browser.close();
  console.log('Done!');
})();
