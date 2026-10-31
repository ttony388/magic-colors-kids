import { chromium } from 'playwright';
import {readFile,writeFile,readdir} from 'node:fs/promises';
const files=(await readdir('public/illustrations/v2/detailed')).filter(f=>f.endsWith('.svg')).sort();
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1200}});
for(let i=0;i<6;i++){
 let cells='';for(const f of files.slice(i*12,i*12+12))cells+=`<article><b>${f.slice(0,-4)}</b>${await readFile('public/illustrations/v2/detailed/'+f,'utf8')}</article>`;
 const html=`<html><style>body{margin:0;background:#eee;font:18px sans-serif}main{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:12px}article{background:white;padding:10px}svg{display:block;width:100%}b{font-size:16px}</style><main>${cells}</main></html>`;
 await writeFile(`docs/art-review/detailed-${i+1}.html`,html);await page.setContent(html);await page.screenshot({path:`docs/art-review/detailed-${i+1}.png`,fullPage:true});
}
await browser.close();
