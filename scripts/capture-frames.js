// Captures frames from illusion-engine.html using headless Chromium.
// Output: ./frames/frame0000.png … frame0129.png  (130 frames @ ~20fps)
const { chromium } = require('playwright');
const path = require('path');
const fs   = require('fs');

const WARMUP_MS  = 3500;   // let particles populate
const FRAMES     = 130;
const FRAME_MS   = 50;     // ~20 fps
const FRAME_DIR  = path.resolve(__dirname, '../frames');
const HTML_PATH  = path.resolve(__dirname, '../illusion-engine.html');
const CHROME     = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  fs.mkdirSync(FRAME_DIR, { recursive: true });

  const browser = await chromium.launch({
    executablePath: CHROME,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu'],
  });

  const page = await browser.newPage();
  await page.setViewportSize({ width: 800, height: 450 });
  await page.goto(`file://${HTML_PATH}`);

  process.stdout.write(`Warming up (${WARMUP_MS}ms)…`);
  await page.waitForTimeout(WARMUP_MS);
  console.log(' done.');

  for (let i = 0; i < FRAMES; i++) {
    const file = path.join(FRAME_DIR, `frame${String(i).padStart(4, '0')}.png`);
    await page.screenshot({ path: file, type: 'png' });
    await page.waitForTimeout(FRAME_MS);
    if (i % 20 === 0) process.stdout.write(`  frame ${i}/${FRAMES}\n`);
  }

  await browser.close();
  console.log(`Captured ${FRAMES} frames → ${FRAME_DIR}`);
})().catch(e => { console.error(e); process.exit(1); });
