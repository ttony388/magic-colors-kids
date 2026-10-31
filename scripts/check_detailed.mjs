/* global document */
import { chromium } from 'playwright';
import {readFile,writeFile,readdir} from 'node:fs/promises';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:440,height:440}});const report=[];
for(const f of (await readdir('public/illustrations/v2/detailed')).filter(f=>f.endsWith('.svg')).sort()){
 await page.setContent(`<style>body{margin:0;padding:20px}svg{width:400px;height:400px}</style>${await readFile('public/illustrations/v2/detailed/'+f,'utf8')}`);
 const issues=await page.evaluate(()=>[...document.querySelectorAll('[data-region]')].flatMap(n=>{
 const b=n.getBoundingClientRect();let hits=0;for(let y=Math.ceil(b.top)+1;y<b.bottom;y+=3)for(let x=Math.ceil(b.left)+1;x<b.right;x+=3)if(document.elementFromPoint(x,y)===n)hits++;
 const length=n.getTotalLength();const pts=Array.from({length:161},(_,i)=>n.getPointAtLength(length*i/160));const cross=(a,b,c)=>(b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x);let crossings=0;
 for(let i=0;i<160;i++)for(let j=i+2;j<160;j++){if(i===0&&j===159)continue;if(cross(pts[i],pts[i+1],pts[j])*cross(pts[i],pts[i+1],pts[j+1])<-.001&&cross(pts[j],pts[j+1],pts[i])*cross(pts[j],pts[j+1],pts[i+1])<-.001)crossings++;}
 return hits<3||crossings||b.left<=20||b.top<=20||b.right>=420||b.bottom>=420?[{id:n.dataset.region,hits,crossings,bounds:[b.left,b.top,b.right,b.bottom]}]:[];
 }));if(issues.length)report.push({file:f,issues});
}
await writeFile('docs/art-review/geometry-issues.json',JSON.stringify(report,null,2));console.log(JSON.stringify(report));await browser.close();if(report.length)process.exitCode=1;
