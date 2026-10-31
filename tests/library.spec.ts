import {test,expect} from '@playwright/test';
import {readFileSync} from 'node:fs';
import {categories,pages} from '../src/data/pages';

for(let sheet=0;sheet<6;sheet++)test(`Detailed library contact sheet ${sheet+1}`,async({page})=>{
  await page.setViewportSize({width:1600,height:1300});
  const sorted=[...pages].sort((a,b)=>a.id.localeCompare(b.id));
  const cells=sorted.slice(sheet*12,sheet*12+12).map(p=>`<article><b>${p.id.split('@')[0]}</b>${readFileSync('public'+p.asset,'utf8')}</article>`).join('');
  await page.setContent(`<style>body{margin:0;background:#eee;font:18px sans-serif}main{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:12px}article{background:white;padding:10px}svg{display:block;width:100%}b{font-size:16px}</style><main>${cells}</main>`);
  await expect(page.locator('main')).toHaveScreenshot(`detailed-sheet-${sheet+1}.png`,{maxDiffPixelRatio:.001});
});

test('all 72 Detailed pages open, bucket-fill, undo and redo in the actual game',async({page})=>{
  test.setTimeout(180000);
  await page.addInitScript(()=>{localStorage.setItem('language','en');localStorage.setItem('sound','false')});
  await page.goto('/');
  for(const category of categories){
    await page.getByRole('button',{name:new RegExp(category.en)}).click();
    for(const p of pages.filter(p=>p.category===category.id)){
      await page.getByRole('button',{name:p.title.en,exact:true}).click();
      await expect(page.locator('.svg-art svg')).toHaveAttribute('data-complexity','detailed');
      const target=await page.locator('.svg-art').evaluate(el=>{
        for(const n of el.querySelectorAll<SVGGraphicsElement>('[data-region]')){
          const b=n.getBoundingClientRect();
          for(let y=b.top+2;y<b.bottom;y+=3)for(let x=b.left+2;x<b.right;x+=3)if(document.elementFromPoint(x,y)===n)return {id:n.getAttribute('data-region')!,x,y};
        }
        return null;
      });
      expect(target,`${p.id} has a reachable fill region`).not.toBeNull();
      const region=page.locator(`[data-region="${target!.id}"]`);
      await page.mouse.click(target!.x,target!.y);
      await expect(region).not.toHaveAttribute('fill','#ffffff');
      const fill=await region.getAttribute('fill');
      await page.getByRole('button',{name:'Undo',exact:true}).click();
      await expect(region).toHaveAttribute('fill','#ffffff');
      await page.getByRole('button',{name:'Redo',exact:true}).click();
      await expect(region).toHaveAttribute('fill',fill!);
      await page.getByRole('button',{name:'Back',exact:true}).click();
    }
    await page.getByRole('button',{name:'Back',exact:true}).click();
  }
});

test('legacy saves keep original geometry and cannot leak colors into Detailed pages',async({page})=>{
  await page.goto('/');
  await page.evaluate(()=>new Promise<void>((resolve,reject)=>{
    const req=indexedDB.open('magic-colors',1);
    req.onupgradeneeded=()=>req.result.createObjectStore('drawings',{keyPath:'id'});
    req.onsuccess=()=>{const tx=req.result.transaction('drawings','readwrite');tx.objectStore('drawings').put({id:'cat',fills:{head:'#123456'},strokes:'[]',completed:false,updatedAt:Date.now()});tx.oncomplete=()=>{req.result.close();resolve()};tx.onerror=()=>reject(tx.error)};
  }));
  await page.getByRole('button',{name:/Моите рисунки/}).click();await page.getByRole('button',{name:/Коте/}).click();
  await expect(page.locator('[data-region="head"]')).toHaveAttribute('fill','#123456');
  await expect(page.locator('.svg-art svg')).not.toHaveAttribute('data-art-version','2');
  await page.reload();await page.getByRole('button',{name:/Животни/}).click();await page.getByRole('button',{name:'Коте',exact:true}).click();
  await expect(page.locator('.svg-art svg')).toHaveAttribute('data-art-version','2');
  await expect(page.locator('[data-region="head"]')).toHaveAttribute('fill','#ffffff');
});
