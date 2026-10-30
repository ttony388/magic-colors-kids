import { useEffect, useMemo, useRef, useState } from 'react';
import { Page } from '../../data/pages';
import { loadDrawing, saveDrawing, type SavedDrawing } from '../../storage/db';
import { colors, renderStroke, tools, type Point, type Stroke, type ToolId } from '../../engine/tools';

type Snapshot = { fills: Record<string,string>; strokes: Stroke[] };
const empty = ():Snapshot => ({fills:{},strokes:[]});
const colorWords = {bg:'Цветове',en:'Colors'};
export default function Editor({page,language,toddler,sound,onBack,onComplete}: {page:Page;language:'bg'|'en';toddler:boolean;sound:boolean;onBack:()=>void;onComplete:()=>void}) {
  const [art,setArt]=useState(''); const [history,setHistory]=useState<Snapshot[]>([empty()]); const [cursor,setCursor]=useState(0);
  const [tool,setTool]=useState<ToolId>('bucket'); const [color,setColor]=useState(colors[3]); const [size,setSize]=useState(16);
  const [opacity,setOpacity]=useState(1); const [zoom,setZoom]=useState(1); const [saved,setSaved]=useState(true);
  const [complete,setComplete]=useState(false); const [recent,setRecent]=useState<string[]>([]);
  const svgRef=useRef<HTMLDivElement>(null); const canvasRef=useRef<HTMLCanvasElement>(null); const active=useRef<Stroke|null>(null);
  const saveQueue=useRef<Promise<unknown>>(Promise.resolve());const saveVersion=useRef(0);
  const current=history[cursor] ?? empty();
  const paintedArt=useMemo(()=>{if(!art)return '';const doc=new DOMParser().parseFromString(art,'image/svg+xml');doc.querySelectorAll<SVGElement>('[data-region]').forEach(node=>node.setAttribute('fill',current.fills[node.dataset.region||'']||'#ffffff'));return doc.documentElement.outerHTML},[art,current.fills]);
  useEffect(()=>{ let cancelled=false; setArt('');setHistory([empty()]);setCursor(0);setComplete(false);setSaved(true);
    if(page.id!=='free')fetch(`${import.meta.env.BASE_URL}${page.asset.replace(/^\//,'')}`).then(r=>r.text()).then(raw=>{if(!cancelled){const doc=new DOMParser().parseFromString(raw,'image/svg+xml');const svg=doc.querySelector('svg');if(svg){svg.querySelectorAll('script,foreignObject').forEach(node=>node.remove());setArt(svg.outerHTML)}}});
    loadDrawing(page.id).then(d=>{if(cancelled||!d)return;let strokes:Stroke[]=[];try{strokes=JSON.parse(d.strokes)}catch{ /* old drawing */ }setHistory([{fills:d.fills,strokes}]);setCursor(0);setComplete(d.completed)}).catch(()=>{});
    return()=>{cancelled=true};
  },[page.id,page.asset]);
  useEffect(()=>{const canvas=canvasRef.current,ctx=canvas?.getContext('2d');if(!canvas||!ctx)return;ctx.clearRect(0,0,400,400);current.strokes.forEach(s=>renderStroke(ctx,s));},[current]);
  useEffect(()=>{if(history.length===1&&cursor===0&&!Object.keys(current.fills).length&&!current.strokes.length&&!complete)return;
    setSaved(false);const version=++saveVersion.current;
    const d:SavedDrawing={id:page.id,fills:current.fills,strokes:JSON.stringify(current.strokes),updatedAt:Date.now(),completed:complete};
    saveQueue.current=saveQueue.current.catch(()=>{}).then(()=>saveDrawing(d)).then(()=>{if(version===saveVersion.current)setSaved(true)}).catch(()=>{if(version===saveVersion.current)setSaved(false)});
  },[current,complete,page.id,history.length,cursor]);
  function commit(next:Snapshot){setSaved(false);setHistory(h=>[...h.slice(0,cursor+1),next].slice(-60));setCursor(c=>Math.min(c+1,59))}
  function chooseColor(value:string){setColor(value);setRecent(r=>[value,...r.filter(c=>c!==value)].slice(0,8))}
  function tapSound(){if(!sound)return;try{const audio=new AudioContext();const oscillator=audio.createOscillator(),gain=audio.createGain();oscillator.type='sine';oscillator.frequency.value=520;gain.gain.setValueAtTime(0.035,audio.currentTime);gain.gain.exponentialRampToValueAtTime(0.001,audio.currentTime+0.12);oscillator.connect(gain).connect(audio.destination);oscillator.start();oscillator.stop(audio.currentTime+0.12);oscillator.onended=()=>audio.close()}catch{/* audio may be unavailable */}}
  function fill(event:React.PointerEvent<HTMLDivElement>){if(tool!=='bucket'&&tool!=='magic')return;const target=(event.target as Element).closest('[data-region]') as SVGElement|null;if(!target)return;
    const region=target.dataset.region!;if(current.fills[region]===color)return;commit({...current,fills:{...current.fills,[region]:color}});tapSound()}
  function point(e:React.PointerEvent<HTMLCanvasElement>):Point{const box=e.currentTarget.getBoundingClientRect();return {x:(e.clientX-box.left)*400/box.width,y:(e.clientY-box.top)*400/box.height}}
  function down(e:React.PointerEvent<HTMLCanvasElement>){e.currentTarget.setPointerCapture(e.pointerId);active.current={tool,color,size,opacity,points:[point(e)]};drawActive()}
  function move(e:React.PointerEvent<HTMLCanvasElement>){if(!active.current)return;active.current.points.push(point(e));drawActive()}
  function drawActive(){const ctx=canvasRef.current?.getContext('2d');if(!ctx||!active.current)return;ctx.clearRect(0,0,400,400);current.strokes.forEach(s=>renderStroke(ctx,s));renderStroke(ctx,active.current)}
  function up(){if(active.current){commit({...current,strokes:[...current.strokes,active.current]});active.current=null}}
  function exportPng(){const out=document.createElement('canvas');out.width=800;out.height=800;const ctx=out.getContext('2d')!;ctx.scale(2,2);ctx.fillStyle='white';ctx.fillRect(0,0,400,400);
    const svg=svgRef.current?.querySelector('svg');if(svg){const image=new Image();const source=new XMLSerializer().serializeToString(svg);image.onload=()=>{ctx.drawImage(image,0,0,400,400);ctx.drawImage(canvasRef.current!,0,0,400,400);download(out)};image.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(source)}else{ctx.drawImage(canvasRef.current!,0,0,400,400);download(out)}}
  function download(canvas:HTMLCanvasElement){const a=document.createElement('a');a.download=`magic-colors-${page.id}.png`;a.href=canvas.toDataURL('image/png');a.click()}
  function finish(){setComplete(true);onComplete()}
  const text=language==='bg';const brush=tool!=='bucket'&&tool!=='magic';
  return <div className={`editor ${toddler?'toddler':''}`}>
    <header className="editor-head"><button className="round-button" aria-label={text?'Назад':'Back'} onClick={onBack}>←</button><div><strong>{page.title[language]}</strong><small>{saved?(text?'Запазено':'Saved'):(text?'Запазване…':'Saving…')}</small></div><button className="round-button" aria-label={text?'Изтегли PNG':'Download PNG'} onClick={exportPng}>⇩</button></header>
    <div className="work-area"><div className="stage-scroll"><div className="stage" style={{width:`${zoom*100}%`,maxWidth:`${zoom*520}px`}} data-testid="drawing-stage">
      {page.id==='free'?<div className="blank-sheet"/>:<div className="svg-art" ref={svgRef} onPointerDown={fill} dangerouslySetInnerHTML={{__html:paintedArt}}/>}
      <canvas width="400" height="400" ref={canvasRef} aria-label={text?'Поле за рисуване':'Drawing canvas'} style={{pointerEvents:brush?'auto':'none'}} onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={up}/>
    </div></div></div>
    <div className="editor-controls"><div className="control-row"><button aria-label="Undo" disabled={cursor===0} onClick={()=>setCursor(cursor-1)}>↶</button><button aria-label="Redo" disabled={cursor>=history.length-1} onClick={()=>setCursor(cursor+1)}>↷</button><button aria-label="Zoom out" onClick={()=>setZoom(z=>Math.max(1,z-0.25))}>−</button><span>{Math.round(zoom*100)}%</span><button aria-label="Zoom in" onClick={()=>setZoom(z=>Math.min(2.5,z+0.25))}>+</button><button onClick={()=>{if(confirm(text?'Да изчистим рисунката?':'Clear the drawing?')){commit(empty());setComplete(false)}}}>{text?'Изчисти':'Reset'}</button></div>
      <div className="tool-strip" role="toolbar" aria-label={text?'Инструменти':'Tools'}>{tools.filter(t=>!toddler||['bucket','crayon','eraser'].includes(t.id)).map(t=><button key={t.id} aria-label={t[language]} aria-pressed={tool===t.id} className={tool===t.id?'selected':''} onClick={()=>setTool(t.id)}><b>{t.symbol}</b><small>{t[language]}</small></button>)}</div>
      {!toddler&&brush&&<div className="sliders"><label>{text?'Размер':'Size'} <input aria-label="Brush size" type="range" min="3" max="50" value={size} onChange={e=>setSize(+e.target.value)}/></label><label>{text?'Плътност':'Opacity'} <input aria-label="Opacity" type="range" min="20" max="100" value={opacity*100} onChange={e=>setOpacity(+e.target.value/100)}/></label></div>}
      <div className="palette-head"><strong>{colorWords[language]}</strong><label className="custom-color" title={text?'Избери цвят':'Pick a color'}><input aria-label="Custom color" type="color" onChange={e=>chooseColor(e.target.value)}/>✚</label></div>
      <div className="palette" aria-label={text?'Палитра':'Palette'}>{(toddler?colors.filter((_,i)=>i%8===3):colors).map((c,i)=><button key={i} aria-label={`${text?'Цвят':'Color'} ${i+1}`} aria-pressed={color===c} style={{background:c}} onClick={()=>chooseColor(c)}/>)}</div>
      {!toddler&&recent.length>0&&<div className="recent">{text?'Последни':'Recent'} {recent.map((c,i)=><button key={i} aria-label={`Recent color ${i+1}`} style={{background:c}} onClick={()=>chooseColor(c)}/>)}</div>}
      <button className="finish-button" onClick={finish}>{complete?(text?'Готово ✓':'Done ✓'):(text?'Завърших!':'Finished!')}</button>
    </div>
  </div>
}
