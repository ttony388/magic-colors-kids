import { test, expect, type Page } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const levels = ['easy', 'medium', 'detailed'];
const subjects = ['cat', 'car', 'mountain'];

async function openReview(page: Page, subject = 'Garden kitten', level = 'Easy') {
  await page.addInitScript(() => { localStorage.setItem('language', 'en'); localStorage.setItem('sound', 'false'); });
  await page.goto('/');
  await page.getByRole('button', { name: 'New artwork · Preview' }).click();
  await page.getByRole('button', { name: level, exact: true }).click();
  await page.getByRole('button', { name: subject, exact: true }).click();
  await expect(page.locator('.svg-art [data-region]').first()).toBeVisible();
}

for (const subject of subjects) for (const level of levels) {
  test(`${subject} ${level}: clean geometry, reachable regions and visual baseline`, async ({ page }) => {
    const svg = readFileSync(resolve(`public/illustrations/v2/${level}/${subject}.svg`), 'utf8');
    await page.setViewportSize({ width: 440, height: 440 });
    await page.setContent(`<style>body{margin:0;padding:20px;background:white}svg{display:block;width:400px;height:400px}</style>${svg}`);
    const report = await page.evaluate(() => {
      const regions = [...document.querySelectorAll<SVGPathElement>('[data-region]')];
      return regions.map(node => {
        const id = node.dataset.region!;
        const b = node.getBoundingClientRect();
        let hits = 0;
        // Actual browser hit testing catches fully occluded shapes as well as tiny slivers.
        for (let y = Math.ceil(b.top) + 1; y < b.bottom; y += 2) {
          for (let x = Math.ceil(b.left) + 1; x < b.right; x += 2) {
            if (document.elementFromPoint(x, y) === node) hits++;
          }
        }
        const length = node.getTotalLength();
        const pts = Array.from({ length: 161 }, (_, i) => node.getPointAtLength(length * i / 160));
        const cross = (a: DOMPoint, b: DOMPoint, c: DOMPoint) => (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
        let intersections = 0;
        for (let i = 0; i < 160; i++) for (let j = i + 2; j < 160; j++) {
          if (i === 0 && j === 159) continue;
          if (cross(pts[i], pts[i + 1], pts[j]) * cross(pts[i], pts[i + 1], pts[j + 1]) < -0.001 &&
              cross(pts[j], pts[j + 1], pts[i]) * cross(pts[j], pts[j + 1], pts[i + 1]) < -0.001) intersections++;
        }
        return { id, hits, length, intersections, bounds: { left: b.left, top: b.top, right: b.right, bottom: b.bottom } };
      });
    });
    for (const region of report) {
      expect(region.hits, `${region.id} must be reachable`).toBeGreaterThan(6);
      expect(region.length, `${region.id} must render`).toBeGreaterThan(5);
      expect(region.intersections, `${region.id} must not self-intersect`).toBe(0);
      expect(region.bounds.left).toBeGreaterThan(20);
      expect(region.bounds.top).toBeGreaterThan(20);
      expect(region.bounds.right).toBeLessThan(420);
      expect(region.bounds.bottom).toBeLessThan(420);
    }
    await expect(page.locator('svg')).toHaveScreenshot(`${subject}-${level}.png`, { maxDiffPixelRatio: .001 });
  });
}

test('review bucket, history, save, gallery and old drawing coexist', async ({ page }) => {
  await openReview(page);
  await page.getByRole('button', { name: 'Color 2', exact: true }).click();
  const head = page.locator('[data-region="head"]');
  await head.click({ position: { x: 50, y: 45 } });
  await expect(head).not.toHaveAttribute('fill', '#ffffff');
  const chosen = await head.getAttribute('fill');
  await page.getByRole('button', { name: 'Undo', exact: true }).click();
  await expect(head).toHaveAttribute('fill', '#ffffff');
  await page.getByRole('button', { name: 'Redo', exact: true }).click();
  await expect(head).toHaveAttribute('fill', chosen!);
  await expect(page.getByText('Saved', { exact: true })).toBeVisible();
  await page.reload();
  await page.getByRole('button', { name: /My drawings/ }).click();
  await page.getByRole('button', { name: /Garden kitten · Easy/ }).click();
  await expect(page.locator('[data-region="head"]')).toHaveAttribute('fill', chosen!);
  await page.reload();
  await page.getByRole('button', { name: /Animals/ }).click();
  await page.getByRole('button', { name: 'Kitten', exact: true }).click();
  await expect(page.locator('[data-region="head"]')).toHaveAttribute('fill', '#ffffff');
});

test('brush stays registered during rotation, tray resize and completion animation', async ({ page }) => {
  await openReview(page);
  await page.getByRole('button', { name: 'Ballpoint pen', exact: true }).click();
  await page.getByRole('button', { name: 'Medium', exact: true }).click();
  const art = page.locator('.svg-art');
  const b = (await art.boundingBox())!;
  await page.mouse.click(b.x + b.width * .5, b.y + b.height * .6);
  const canvas = page.getByLabel('Drawing canvas');
  async function alphaAtArtPoint() {
    return canvas.evaluate(el => {
      const c = el as HTMLCanvasElement, cb = c.getBoundingClientRect();
      const a = document.querySelector('.svg-art')!.getBoundingClientRect();
      return c.getContext('2d')!.getImageData(Math.round((a.left - cb.left + a.width * .5) * c.width / cb.width), Math.round((a.top - cb.top + a.height * .6) * c.height / cb.height), 1, 1).data[3];
    });
  }
  await expect.poll(alphaAtArtPoint).toBeGreaterThan(0);
  await page.setViewportSize({ width: 1340, height: 800 });
  await expect.poll(alphaAtArtPoint).toBeGreaterThan(0);
  await page.getByRole('button', { name: 'Hide tools' }).click();
  await expect.poll(alphaAtArtPoint).toBeGreaterThan(0);
  await page.getByRole('button', { name: 'Show tools' }).click();
  await page.getByRole('button', { name: /Bring to life/ }).click();
  await expect(page.locator('.artwork-layer')).toHaveCSS('animation-name', 'picture-awake');
  expect(await canvas.evaluate(el => el.parentElement === document.querySelector('.svg-art')!.parentElement)).toBe(true);
  await expect(page.locator('.artwork-layer')).not.toHaveCSS('transform', 'none');
  await expect(page.getByTestId('drawing-stage')).not.toHaveClass(/alive/, { timeout: 4500 });
  await expect.poll(alphaAtArtPoint).toBeGreaterThan(0);
  await page.getByRole('button', { name: 'Reset', exact: true }).click();
  await expect.poll(alphaAtArtPoint).toBe(0);
});

test('automatic completion retains colored regions and respects reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await openReview(page, 'Family hatchback', 'Medium');
  const ids = await page.locator('[data-region]').evaluateAll(nodes => nodes.map(n => n.getAttribute('data-region')!));
  for (const id of ids.slice(0, Math.ceil(ids.length * .8))) {
    await page.locator(`[data-region="${id}"]`).dispatchEvent('pointerdown', { pointerType: 'touch' });
  }
  await expect(page.getByTestId('drawing-stage')).toHaveClass(/alive/);
  await expect(page.locator('.artwork-layer')).toHaveCSS('animation-name', 'none');
  await expect(page.locator(`[data-region="${ids[0]}"]`)).not.toHaveAttribute('fill', '#ffffff');
});

for (const [name, width, height] of [['phone-portrait', 412, 915], ['phone-landscape', 915, 412], ['tablet-portrait', 800, 1340], ['tablet-landscape', 1340, 800]] as const) {
  test(`responsive ${name}: entire landscape is visible without distortion`, async ({ page }) => {
    await page.setViewportSize({ width, height });
    await openReview(page, 'Alpine lake', 'Detailed');
    const box = (await page.locator('.svg-art').boundingBox())!;
    const tray = (await page.locator('.editor-controls').boundingBox())!;
    expect(Math.abs(box.width - box.height)).toBeLessThan(1);
    expect(box.x).toBeGreaterThanOrEqual(0);
    expect(box.x + box.width).toBeLessThanOrEqual(width);
    if(name==='phone-landscape')expect(box.x+box.width).toBeLessThanOrEqual(tray.x);
    else expect(box.y + box.height).toBeLessThanOrEqual(tray.y);
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
    await expect(page).toHaveScreenshot(`${name}.png`, { maxDiffPixelRatio: .01 });
  });
}

test('production bundle opens every review level with networking offline', async ({ page, context }) => {
  const mime: Record<string, string> = { html: 'text/html', js: 'application/javascript', css: 'text/css', svg: 'image/svg+xml' };
  await context.route('**/*', async route => {
    const url = new URL(route.request().url());
    if (url.hostname !== 'offline.test') throw new Error(`External dependency: ${url.href}`);
    const file = url.pathname === '/' ? 'index.html' : url.pathname.slice(1);
    await route.fulfill({ body: readFileSync(resolve('dist', file)), contentType: mime[file.split('.').at(-1)!] || 'application/octet-stream' });
  });
  await context.setOffline(true);
  await page.goto('http://offline.test/');
  await expect(page.getByRole('heading', { name: 'Какво ще оцветиш?' })).toBeVisible();
  for (const level of levels) for (const subject of subjects) {
    const result = await page.evaluate(async path => { const response = await fetch(path); return response.text(); }, `/illustrations/v2/${level}/${subject}.svg`);
    expect(result).toContain('data-art-version="2"');
  }
  await page.getByRole('button', { name: 'Нови рисунки · Преглед' }).click();
  await page.getByRole('button', { name: 'Коте в градината', exact: true }).click();
  await expect(page.locator('[data-region="head"]')).toBeVisible();
  await page.locator('[data-region="head"]').dispatchEvent('pointerdown', { pointerType: 'touch' });
  await expect(page.locator('[data-region="head"]')).not.toHaveAttribute('fill', '#ffffff');
});
