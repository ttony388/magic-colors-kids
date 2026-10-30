import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { artLevels, reviewPages, reviewSubjects } from './artwork';
import { artFrame, toArtPoint } from '../engine/artFrame';

describe('versioned original artwork', () => {
  it('offers three independent saves per subject with stable core region IDs', () => {
    expect(reviewPages).toHaveLength(9);
    expect(new Set(reviewPages.map(p => p.id)).size).toBe(9);
    for (const subject of reviewSubjects) {
      let previous: string[] = [];
      for (const level of artLevels) {
        const page = reviewPages.find(p => p.id === `${subject.id}@v2:${level}`)!;
        const svg = readFileSync(new URL(`../../public${page.asset}`, import.meta.url), 'utf8');
        const ids = [...svg.matchAll(/data-region="([^"]+)"/g)].map(m => m[1]);
        expect(ids.length).toBeGreaterThanOrEqual(9);
        expect(new Set(ids).size).toBe(ids.length);
        previous.forEach(id => expect(ids).toContain(id));
        expect(svg).not.toMatch(/<(?:image|script|foreignObject)\b/);
        for (const [, path] of svg.matchAll(/data-region="[^"]+" d="([^"]+)"/g)) {
          expect(path.trim()).toMatch(/Z$/);
        }
        previous = ids;
      }
    }
  });

  it('maps ink to the same uniform frame through tablet rotation and tray changes', () => {
    for (const [width, height, tray] of [[412, 857, 350], [800, 1282, 220], [1340, 742, 220], [915, 354, 170], [412, 857, 44]]) {
      const frame = artFrame(width, height, tray);
      expect(frame.left).toBeGreaterThanOrEqual(0);
      expect(frame.top).toBeGreaterThanOrEqual(0);
      expect(frame.top + frame.side).toBeLessThan(height - tray);
      const p = toArtPoint(frame.left + frame.side * .35, frame.top + frame.side * .8, frame);
      expect(p.x).toBeCloseTo(140);
      expect(p.y).toBeCloseTo(320);
    }
  });
});
