import { describe, expect, it } from 'vitest';
import { categories, getDailyPage, pages } from './pages';
import { colors } from '../engine/tools';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
describe('the first playable library',()=>{
  it('registers five unique drawings in each category',()=>{
    expect(pages).toHaveLength(50);
    expect(new Set(pages.map(p=>p.id)).size).toBe(50);
    for(const category of categories)expect(pages.filter(p=>p.category===category.id)).toHaveLength(5);
    const hashes = new Set<string>();
    for(const page of pages){
      expect(page.title.bg.length).toBeGreaterThan(2);expect(page.asset).toMatch(/\.svg$/);
      const svg=readFileSync(new URL(`../../public${page.asset}`,import.meta.url),'utf8');
      const regions=[...svg.matchAll(/data-region="([^"]+)"/g)].map(m=>m[1]);
      expect(regions.length).toBeGreaterThanOrEqual(5);
      expect(new Set(regions).size).toBe(regions.length);
      hashes.add(createHash('sha256').update(svg).digest('hex'));
    }
    expect(hashes.size).toBe(50);
  });
  it('offers 64 distinct palette colors and deterministic daily selection',()=>{
    expect(new Set(colors).size).toBe(64);
    expect(getDailyPage(new Date('2026-10-30'))).toEqual(getDailyPage(new Date('2026-10-30')));
  });
});
