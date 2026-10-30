export const tools = [
  {id:'bucket',bg:'Кофичка',en:'Fill',symbol:'▰'},
  {id:'magic',bg:'Магия',en:'Magic',symbol:'✦'},
  {id:'pencil',bg:'Молив',en:'Pencil',symbol:'✎'},
  {id:'crayon',bg:'Пастел',en:'Crayon',symbol:'▥'},
  {id:'pen',bg:'Флумастер',en:'Felt pen',symbol:'╱'},
  {id:'marker',bg:'Маркер',en:'Marker',symbol:'▮'},
  {id:'brush',bg:'Четка',en:'Brush',symbol:'⌁'},
  {id:'watercolor',bg:'Акварел',en:'Watercolor',symbol:'◒'},
  {id:'glitter',bg:'Блясък',en:'Glitter',symbol:'✧'},
  {id:'spray',bg:'Спрей',en:'Spray',symbol:'⋮'},
  {id:'eraser',bg:'Гума',en:'Eraser',symbol:'◇'}
] as const;
export type ToolId = typeof tools[number]['id'];
export const colors = Array.from({length:64},(_,i)=>{const hue=Math.floor(i/8)*45; const light=[25,35,45,55,65,75,82,92][i%8];return `hsl(${hue} 90% ${light}%)`});
export type Point = {x:number;y:number};
export type Stroke = {tool:ToolId;color:string;size:number;opacity:number;points:Point[]};
export function renderStroke(ctx:CanvasRenderingContext2D,s:Stroke) {
  const pts=s.points; if(!pts.length)return;
  ctx.save(); ctx.globalAlpha=s.opacity; ctx.lineCap='round';ctx.lineJoin='round';
  if(s.tool==='eraser') ctx.globalCompositeOperation='destination-out';
  if(s.tool==='marker')ctx.globalAlpha*=0.35;
  if(s.tool==='watercolor')ctx.globalAlpha*=0.22;
  ctx.strokeStyle=s.color;ctx.fillStyle=s.color;
  if(s.tool==='spray'||s.tool==='glitter'||s.tool==='crayon'){
    pts.forEach((p,j)=>{for(let i=0;i<(s.tool==='spray'?22:12);i++){
      const angle=(i*2.399+j*0.618);const radius=(Math.sqrt((i*13+j*7)%19)/4.4)*s.size;
      const x=p.x+Math.cos(angle)*radius,y=p.y+Math.sin(angle)*radius;
      ctx.globalAlpha=s.opacity*(s.tool==='glitter'?(i%3?0.35:0.95):s.tool==='crayon'?0.3:0.18);
      ctx.beginPath();ctx.arc(x,y,s.tool==='glitter'?(i%3?0.7:1.8):s.tool==='crayon'?1.1:0.7,0,Math.PI*2);ctx.fill();
    }});
  } else {
    ctx.lineWidth=s.size*(s.tool==='pencil'?0.35:s.tool==='pen'?0.65:s.tool==='marker'?2.2:s.tool==='watercolor'?2.5:1);
    ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);pts.slice(1).forEach(p=>ctx.lineTo(p.x,p.y));
    if(pts.length===1){ctx.lineTo(pts[0].x+0.01,pts[0].y+0.01)}ctx.stroke();
    if(s.tool==='watercolor'){ctx.lineWidth*=0.55;ctx.globalAlpha=s.opacity*0.18;ctx.stroke()}
  }
  ctx.restore();
}
