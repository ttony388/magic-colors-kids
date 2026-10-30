import { useEffect, useMemo, useRef, useState } from 'react';
import { Page } from '../../data/pages';
import { loadDrawing, saveDrawing, type SavedDrawing } from '../../storage/db';
import { colors, renderStroke, tools, type Point, type Stroke, type ToolId } from '../../engine/tools';

type Snapshot = { fills: Record<string,string>; strokes: Stroke[] };
type Sparkle = { id: number; x: number; y: number; dx: number; dy: number; color: string; size: number };
const empty = ():Snapshot => ({fills:{},strokes:[]});
const colorWords = {bg:'Цветове',en:'Colors'};
export default function Editor({page,language,toddler,sound,onBack,onComplete}: {page:Page;language:'bg'|'en';toddler:boolean;sound:boolean;onBack:()=>void;onComplete:()=>void}) {
  const [art,setArt]=useState(''); const [history,setHistory]=useState<Snapshot[]>([empty()]); const [cursor,setCursor]=useState(0);
  const [tool,setTool]=useState<ToolId>('bucket'); const [color,setColor]=useState(colors[3]); const [size,setSize]=useState(16);
  const [opacity,setOpacity]=useState(1); const [saved,setSaved]=useState(true);
  const [complete,setComplete]=useState(false); const [recent,setRecent]=useState<string[]>([]);
  const [trayOpen,setTrayOpen]=useState(true);
  const [alive,setAlive]=useState(false);const aliveTimer=useRef<number|null>(null);
  const [sparkles,setSparkles]=useState<Sparkle[]>([]);
  const svgRef=useRef<HTMLDivElement>(null); const canvasRef=useRef<HTMLCanvasElement>(null); const active=useRef<Stroke|null>(null);
  const stageRef=useRef<HTMLDivElement>(null);const particleId=useRef(0);const lastTrail=useRef(0);const particleTimers=useRef(new Set<number>());
  const audioRef=useRef<AudioContext|null>(null);const lastTone=useRef(-1000);
  const saveQueue=useRef<Promise<unknown>>(Promise.resolve());const saveVersion=useRef(0);
  const current=history[cursor] ?? empty();
  const paintedArt=useMemo(()=>{if(!art)return '';const doc=new DOMParser().parseFromString(art,'image/svg+xml');doc.querySelector('svg > rect:not([data-region])')?.remove();doc.querySelectorAll<SVGElement>('[data-region]').forEach(node=>node.setAttribute('fill',current.fills[node.dataset.region||'']||'#ffffff'));return doc.documentElement.outerHTML},[art,current.fills]);
  useEffect(()=>()=>{particleTimers.current.forEach(clearTimeout);if(aliveTimer.current)clearTimeout(aliveTimer.current);if(audioRef.current)void audioRef.current.close()},[]);
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
  function playColorSound(){if(!sound||performance.now()-lastTone.current<240)return;lastTone.current=performance.now();try{
    const audio=audioRef.current??new AudioContext();audioRef.current=audio;if(audio.state==='suspended')void audio.resume();
    const index=Math.max(0,colors.indexOf(color));const notes=[523.25,587.33,659.25,783.99,880];
    const root=notes[index%notes.length];
    // A soft two-note toy chime, with a little bright overtone on each note.
    for(const [offset,pitch,volume] of [[0,root,0.045],[0.09,root*1.5,0.03]] as const){
      const start=audio.currentTime+offset;
      for(const [wave,multiplier,level] of [['sine',1,1],['triangle',2.01,0.14]] as const){
        const oscillator=audio.createOscillator(),gain=audio.createGain();oscillator.type=wave;
        oscillator.frequency.setValueAtTime(pitch*multiplier,start);
        gain.gain.setValueAtTime(0.0001,start);gain.gain.exponentialRampToValueAtTime(volume*level,start+0.012);
        gain.gain.exponentialRampToValueAtTime(0.0001,start+0.32);
        oscillator.connect(gain).connect(audio.destination);oscillator.start(start);oscillator.stop(start+0.33);
      }
    }
  }catch{/* sound is optional when the browser has no audio output */}}
  function emitSparkles(e:React.PointerEvent,burst=false){
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    const now=performance.now();if(!burst&&now-lastTrail.current<55)return;lastTrail.current=now;
    const box=stageRef.current?.getBoundingClientRect();if(!box)return;
    const x=(e.clientX-box.left)/box.width*100,y=(e.clientY-box.top)/box.height*100;
    if(x<0||x>100||y<0||y>100)return;
    const group=Array.from({length:burst?8:3},(_,i)=>({id:++particleId.current,x,y,
      dx:Math.cos(i*2.4+now)*((burst?24:15)+i*3),dy:Math.sin(i*2.4+now)*((burst?24:15)+i*3)-19,
      color,size:burst?30+(i%3)*5:25+(i%2)*6}));
    setSparkles(prev=>[...prev,...group].slice(-45));
    const timer=window.setTimeout(()=>{setSparkles(prev=>prev.filter(p=>!group.some(g=>g.id===p.id)));particleTimers.current.delete(timer)},850);
    particleTimers.current.add(timer);
  }
  function fill(event:React.PointerEvent<HTMLDivElement>){if(tool!=='bucket'&&tool!=='magic')return;const target=(event.target as Element).closest('[data-region]') as SVGElement|null;
    const region=target?.dataset.region||'__background';if(current.fills[region]===color)return;commit({...current,fills:{...current.fills,[region]:color}});playColorSound()}
  function point(e:React.PointerEvent<HTMLCanvasElement>):Point{const box=e.currentTarget.getBoundingClientRect();return {x:(e.clientX-box.left)*400/box.width,y:(e.clientY-box.top)*400/box.height}}
  function down(e:React.PointerEvent<HTMLCanvasElement>){e.currentTarget.setPointerCapture(e.pointerId);active.current={tool,color,size,opacity,points:[point(e)]};drawActive();playColorSound()}
  function move(e:React.PointerEvent<HTMLCanvasElement>){if(!active.current)return;active.current.points.push(point(e));drawActive();playColorSound()}
  function drawActive(){const ctx=canvasRef.current?.getContext('2d');if(!ctx||!active.current)return;ctx.clearRect(0,0,400,400);current.strokes.forEach(s=>renderStroke(ctx,s));renderStroke(ctx,active.current)}
  function up(){if(active.current){commit({...current,strokes:[...current.strokes,active.current]});active.current=null}}
  function exportPng(){const stage=stageRef.current;if(!stage)return;const w=stage.clientWidth,h=stage.clientHeight;
    const out=document.createElement('canvas');out.width=w*2;out.height=h*2;const ctx=out.getContext('2d')!;ctx.scale(2,2);ctx.fillStyle=current.fills.__background||'white';ctx.fillRect(0,0,w,h);
    const drawStrokes=()=>{ctx.drawImage(canvasRef.current!,0,0,w,h);download(out)};
    const svg=svgRef.current?.querySelector('svg');if(svg){const image=new Image();const source=new XMLSerializer().serializeToString(svg);image.onload=()=>{const box=svgRef.current!.getBoundingClientRect(),stageBox=stage.getBoundingClientRect(),side=Math.min(box.width,box.height);ctx.drawImage(image,(box.left-stageBox.left)+(box.width-side)/2,(box.top-stageBox.top)+(box.height-side)/2,side,side);drawStrokes()};image.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(source)}else drawStrokes()}
  function download(canvas:HTMLCanvasElement){const a=document.createElement('a');a.download=`magic-colors-${page.id}.png`;a.href=canvas.toDataURL('image/png');a.click()}
  function finish(){setComplete(true);setAlive(true);if(aliveTimer.current)clearTimeout(aliveTimer.current);
    const group=Array.from({length:22},(_,i)=>({id:++particleId.current,x:50+(Math.random()-.5)*50,y:43+(Math.random()-.5)*40,
      dx:(Math.random()-.5)*100,dy:-25-Math.random()*45,color:colors[(i*7)%colors.length],size:28+(i%3)*6}));
    setSparkles(prev=>[...prev,...group]);
    const timer=window.setTimeout(()=>{setSparkles(prev=>prev.filter(p=>!group.some(g=>g.id===p.id)));particleTimers.current.delete(timer)},850);particleTimers.current.add(timer);
    aliveTimer.current=window.setTimeout(()=>setAlive(false),3000);onComplete()}
  const text=language==='bg';const brush=tool!=='bucket'&&tool!=='magic';
  return <div className={`editor ${toddler?'toddler':''}`}>
    <header className="editor-head"><button className="round-button" aria-label={text?'Назад':'Back'} onClick={onBack}>←</button><div><strong>{page.title[language]}</strong><small>{saved?(text?'Запазено':'Saved'):(text?'Запазване…':'Saving…')}</small></div><button className="round-button" aria-label={text?'Изтегли PNG':'Download PNG'} onClick={exportPng}>⇩</button></header>
    <div className="work-area"><div className={`stage ${alive?'alive':''} ${trayOpen?'':'tray-collapsed'}`} ref={stageRef} style={{backgroundColor:current.fills.__background||'#ffffff'}} data-testid="drawing-stage" onPointerMove={e=>emitSparkles(e)} onPointerDown={e=>emitSparkles(e,true)}>
      {page.id==='free'?<div className="blank-sheet" onPointerDown={fill}/>:<div className="svg-art" ref={svgRef} onPointerDown={fill} dangerouslySetInnerHTML={{__html:paintedArt}}/>}
      <canvas width="400" height="400" ref={canvasRef} aria-label={text?'Поле за рисуване':'Drawing canvas'} style={{pointerEvents:brush?'auto':'none'}} onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={up}/>
      <div className="sparkle-layer" aria-hidden="true">{sparkles.map(p=><span key={p.id} className="sparkle" style={{left:`${p.x}%`,top:`${p.y}%`,color:p.color,fontSize:p.size,'--dx':`${p.dx}px`,'--dy':`${p.dy}px`} as React.CSSProperties}>✦</span>)}</div>
    </div></div>
    <div className={`editor-controls ${trayOpen?'':'collapsed'}`}><button className="tray-toggle" aria-label={trayOpen?(text?'Скрий инструментите':'Hide tools'):(text?'Покажи инструментите':'Show tools')} onClick={()=>setTrayOpen(v=>!v)}>{trayOpen?'⌄':(text?'🎨 Инструменти':'🎨 Tools')}</button>{trayOpen&&<><div className="tool-strip" role="toolbar" aria-label={text?'Инструменти':'Tools'}>{tools.map(t=><button key={t.id} aria-label={t[language]} aria-pressed={tool===t.id} className={tool===t.id?'selected':''} onClick={()=>setTool(t.id)}><img src={`${import.meta.env.BASE_URL}tools/${t.id}.svg`} alt=""/><small>{t[language]}</small></button>)}</div>
      {!toddler&&brush&&<div className="sliders"><label>{text?'Размер':'Size'} <input aria-label="Brush size" type="range" min="3" max="50" value={size} onChange={e=>setSize(+e.target.value)}/></label><label>{text?'Плътност':'Opacity'} <input aria-label="Opacity" type="range" min="20" max="100" value={opacity*100} onChange={e=>setOpacity(+e.target.value/100)}/></label></div>}
      <div className="palette-row"><strong>{colorWords[language]}</strong><div className="palette" aria-label={text?'Палитра':'Palette'}>{(toddler?colors.filter((_,i)=>i%8===3):colors).map((c,i)=><button key={i} aria-label={`${text?'Цвят':'Color'} ${i+1}`} aria-pressed={color===c} style={{background:c}} onClick={()=>chooseColor(c)}/>)}</div><label className="custom-color" title={text?'Избери цвят':'Pick a color'}><input aria-label="Custom color" type="color" onChange={e=>chooseColor(e.target.value)}/>✚</label></div>
      {!toddler&&recent.length>0&&<div className="recent">{text?'Последни':'Recent'} {recent.map((c,i)=><button key={i} aria-label={`Recent color ${i+1}`} style={{background:c}} onClick={()=>chooseColor(c)}/>)}</div>}
      <div className="control-row"><button aria-label="Undo" disabled={cursor===0} onClick={()=>setCursor(cursor-1)}>↶</button><button aria-label="Redo" disabled={cursor>=history.length-1} onClick={()=>setCursor(cursor+1)}>↷</button><button onClick={()=>{if(confirm(text?'Да изчистим рисунката?':'Clear the drawing?')){commit(empty());setComplete(false)}}}>{text?'Изчисти':'Reset'}</button><button className="finish-button" disabled={!Object.keys(current.fills).length&&!current.strokes.length} onClick={finish}>{complete?(text?'Още магия ✦':'Again ✦'):(text?'Съживи! ✨':'Bring to life! ✨')}</button></div></>}
    </div>
  </div>
}
