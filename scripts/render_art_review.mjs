import { chromium } from 'playwright';
import { readFile, writeFile, mkdir, readdir } from 'node:fs/promises';
import { resolve } from 'node:path';

const output = resolve('docs/art-review');
await mkdir(output, { recursive: true });
const style = `*{box-sizing:border-box}body{margin:0;background:#eeeae3;color:#292929;font:16px system-ui}main{padding:42px;width:1600px}header{margin:0 0 28px}h1{font-size:34px;margin:8px 0}p{margin:6px 0;color:#666}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.cell{background:white;border:1px solid #ddd8ce;border-radius:12px;padding:14px}.cell svg{width:100%;height:auto;display:block}.label{font-size:16px;font-weight:650}.meta{font-size:12px;color:#777}.eyebrow{letter-spacing:2px;font-size:12px;font-weight:bold;color:#856b49}footer{margin-top:24px;color:#666}`;
const doc = (heading, contents, columns = 4) => `<!doctype html><html lang="en"><meta charset="utf-8"><title>Magic Colors · Artwork review</title><style>${style}.grid{grid-template-columns:repeat(${columns},1fr)}</style><main><header><div class="eyebrow">MAGIC COLORS KIDS / ART DIRECTION REVIEW 01</div><h1>${heading}</h1><p>Original SVG line art · Stable, individually colorable white regions</p></header><div class="grid">${contents}</div><footer>Review samples only. Existing artwork and saved drawings remain available.</footer></main></html>`;
let cells = '';
for (const [subject, title] of [['cat', 'Kitten'], ['car', 'Family hatchback'], ['mountain', 'Alpine landscape']]) {
  for (const level of ['current', 'easy', 'medium', 'detailed']) {
    const path = level === 'current' ? `${subject}.svg` : `v2/${level}/${subject}.svg`;
    const svg = await readFile(resolve('public/illustrations', path), 'utf8');
    cells += `<div class="cell"><div class="label">${title} · ${level[0].toUpperCase() + level.slice(1)}</div><div class="meta">${(svg.match(/data-region=/g) || []).length} color regions</div>${svg}</div>`;
  }
}
await writeFile(`${output}/comparison.html`, doc('Natural shapes. Room to color.', cells));
const files = (await readdir('public/illustrations')).filter(f => f.endsWith('.svg')).sort();
for (let sheet = 0; sheet < 2; sheet++) {
  let thumbnails = '';
  for (const file of files.slice(sheet * 36, (sheet + 1) * 36)) {
    thumbnails += `<div class="cell"><div class="label">${file.slice(0, -4)}</div>${await readFile(`public/illustrations/${file}`, 'utf8')}</div>`;
  }
  await writeFile(`${output}/legacy-${sheet + 1}.html`, doc(`Existing library · ${sheet * 36 + 1}–${(sheet + 1) * 36}`, thumbnails, 6));
}
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 1500 }, deviceScaleFactor: 1 });
for (const name of ['comparison', 'legacy-1', 'legacy-2']) {
  await page.goto(`file://${output}/${name}.html`);
  await page.screenshot({ path: `${output}/${name}.png`, fullPage: true });
}
await browser.close();
console.log('Rendered comparison and two complete legacy catalog sheets.');
