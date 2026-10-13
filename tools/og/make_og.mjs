// og-card.html 을 1200×630 으로 캡처해 static/images/og-card.png 로 저장 (폰트는 static/ 에서 라우팅)
// 실행: cd tools/og && npm install && npx playwright install chromium && node make_og.mjs
//       (설치된 Chrome 을 쓰려면 CHROME_PATH=/path/to/chrome node make_og.mjs)
import { chromium } from 'playwright';
import { readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const out = path.join(root, 'static/images/og-card.png');
const types = { '.css': 'text/css', '.woff2': 'font/woff2', '.html': 'text/html' };

const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
await page.route('http://og.local/**', async route => {
  const p = new URL(route.request().url()).pathname;
  const file = p === '/' ? path.join(here, 'og-card.html') : path.join(root, 'static', p);
  try {
    await route.fulfill({ body: await readFile(file), contentType: types[path.extname(file)] || 'application/octet-stream' });
  } catch {
    await route.fulfill({ status: 404 });
  }
});
await page.goto('http://og.local/', { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
const missing = await page.evaluate(() => [...document.fonts].filter(f => f.status === 'error').length);
if (missing) throw new Error(`폰트 로드 실패 ${missing}건`);
const png = await page.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1200, height: 630 } });
await writeFile(out, png);
await browser.close();
console.log(`${path.relative(root, out)} ${(png.length / 1024).toFixed(1)} KB`);
