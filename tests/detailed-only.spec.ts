import {test,expect} from '@playwright/test';
test('only Detailed artwork is offered from the main catalog',async({page})=>{
 await page.goto('/');
 await expect(page.getByRole('button',{name:'Нови рисунки · Преглед'})).toHaveCount(0);
 await expect(page.locator('.category-card')).toHaveCount(12);
 await page.getByRole('button',{name:/Животни/}).click();
 await expect(page.locator('.page-card')).toHaveCount(6);
 const paths=await page.locator('.page-card img').evaluateAll(ns=>ns.map(n=>n.getAttribute('src')));
 expect(paths.every(p=>p?.includes('/v2/detailed/'))).toBe(true);
 await page.getByRole('button',{name:'Коте',exact:true}).click();
 await expect(page.locator('.svg-art svg')).toHaveAttribute('data-complexity','detailed');
 await page.locator('[data-region="head"]').dispatchEvent('pointerdown',{pointerType:'touch'});
 await expect(page.locator('[data-region="head"]')).not.toHaveAttribute('fill','#ffffff');
});
