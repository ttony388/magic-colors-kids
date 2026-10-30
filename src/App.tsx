import { useEffect, useState } from 'react';
import Editor from './features/coloring/Editor';
import { categories, getDailyPage, nextSurprise, pages, type Page } from './data/pages';
import { deleteDrawing, listDrawings, type SavedDrawing } from './storage/db';

const free:Page={id:'free',category:'free',title:{bg:'Свободно рисуване',en:'Free drawing'},difficulty:'easy',asset:''};
type Screen='home'|'category'|'editor'|'gallery'|'parents';
const asset=(p:Page)=>`${import.meta.env.BASE_URL}${p.asset.slice(1)}`;

export default function App(){
  const [screen,setScreen]=useState<Screen>('home');
  const [category,setCategory]=useState('animals');
  const [page,setPage]=useState<Page>(pages[0]);
  const [editorBack,setEditorBack]=useState<Screen>('category');
  const [language,setLanguage]=useState<'bg'|'en'>(()=>localStorage.getItem('language')==='en'?'en':'bg');
  const [toddler,setToddler]=useState(()=>localStorage.getItem('toddler')!=='false');
  const [sound,setSound]=useState(()=>localStorage.getItem('sound')!=='false');
  const [gate,setGate]=useState(false);
  const [answer,setAnswer]=useState('');
  const [drawings,setDrawings]=useState<SavedDrawing[]>([]);
  const [celebrate,setCelebrate]=useState(false);
  const bg=language==='bg';

  useEffect(()=>{localStorage.setItem('language',language);document.documentElement.lang=language},[language]);
  useEffect(()=>localStorage.setItem('toddler',String(toddler)),[toddler]);
  useEffect(()=>localStorage.setItem('sound',String(sound)),[sound]);

  function open(p:Page,back:Screen='category'){setPage(p);setEditorBack(back);setCelebrate(false);setScreen('editor')}
  function surprise(){
    let seen:string[]=[];
    try{seen=JSON.parse(localStorage.getItem('surpriseSeen')||'[]');if(!Array.isArray(seen))seen=[]}catch{/* a fresh cycle is safe */}
    const choice=nextSurprise(seen);
    localStorage.setItem('surpriseSeen',JSON.stringify(choice.seen));
    open(choice.page,'home');
  }
  function gallery(){listDrawings().then(setDrawings).catch(()=>setDrawings([]));setScreen('gallery')}
  function parentGate(){setAnswer('');setGate(true)}
  function goCategory(id:string){setCategory(id);setScreen('category')}

  return <div className={`app ${toddler?'toddler':''}`}>
    {screen==='editor' ? <Editor key={page.id} page={page} language={language} toddler={toddler} sound={sound}
      onBack={()=>setScreen(editorBack)}
      onComplete={()=>{setCelebrate(true);setTimeout(()=>setCelebrate(false),2800)}}
      onClear={()=>setCelebrate(false)}/> : <>
      <div className="shell">
        <header className="topbar">
          <button className="brand" onClick={()=>setScreen('home')} aria-label={bg?'Начало':'Home'}><img className="brand-mark" src={`${import.meta.env.BASE_URL}logo.svg`} alt=""/><span>{bg?'Вълшебни Цветове':'Magic Colors'}</span></button>
          <button className="parent-link" onClick={parentGate} aria-label={bg?'За родители':'Parents'}>⚙</button>
        </header>

        {screen==='home'&&<main>
          <div className="simple-intro"><h1>{bg?'Какво ще оцветиш?':'What will you color?'}</h1>
            <button className="surprise-button" onClick={surprise}><span aria-hidden="true">✦</span>{bg?'ИЗНЕНАДА':'SURPRISE'}<span aria-hidden="true">✦</span></button>
          </div>
          <div className="section-title"><h2>{bg?'Още картинки':'More pictures'}</h2><span>{pages.length} {bg?'картинки':'pictures'}</span></div>
          <div className="category-grid">{categories.map(c=>{const item=pages.find(p=>p.category===c.id)!;return <button className="category-card" key={c.id} onClick={()=>goCategory(c.id)} style={{background:c.color}}>
            <div className="card-art"><img loading="lazy" src={asset(item)} alt=""/></div><strong>{c[language]}</strong><small>{pages.filter(p=>p.category===c.id).length} {bg?'картинки':'pictures'}</small>
          </button>})}</div>
          <div className="simple-links"><button onClick={()=>open(getDailyPage(new Date()),'home')}>{bg?'Картинка на деня':'Daily picture'} →</button><button onClick={gallery}>{bg?'Моите рисунки':'My drawings'} →</button>{!toddler&&<button onClick={()=>open(free,'home')}>{bg?'Свободно рисуване':'Free drawing'} →</button>}</div>
        </main>}

        {screen==='category'&&<main>
          <button className="back-link" onClick={()=>setScreen('home')}>← {bg?'Назад':'Back'}</button>
          <h1 className="category-heading">{categories.find(c=>c.id===category)?.[language]}</h1>
          <div className="page-grid">{pages.filter(p=>p.category===category).map(p=><button key={p.id} className="page-card" onClick={()=>open(p)}>
            <img src={asset(p)} alt=""/><strong>{p.title[language]}</strong>{!toddler&&<span>{p.difficulty==='easy'?(bg?'Лесно':'Easy'):p.difficulty==='medium'?(bg?'Средно':'Medium'):(bg?'Напреднало':'Advanced')}</span>}
          </button>)}</div>
        </main>}

        {screen==='gallery'&&<main>
          <button className="back-link" onClick={()=>setScreen('home')}>← {bg?'Назад':'Back'}</button><h1>{bg?'Моите рисунки':'My drawings'}</h1>
          {drawings.length===0?<div className="empty-gallery">{bg?'Тук ще се появят твоите рисунки.':'Your drawings will appear here.'}<br/><button className="primary" onClick={()=>setScreen('home')}>{bg?'Избери картинка':'Choose a picture'}</button></div>:
            <div className="page-grid">{[...drawings].sort((a,b)=>b.updatedAt-a.updatedAt).map(d=>{const p=pages.find(p=>p.id===d.id)||free;return <div className="page-card" key={d.id}>
              <button onClick={()=>open(p,'gallery')}>{p.id==='free'?<div className="blank-thumb">✎</div>:<img src={asset(p)} alt=""/>}<strong>{p.title[language]}</strong><span>{d.completed?'✓ ':''}{new Date(d.updatedAt).toLocaleDateString(language)}</span></button>
              {!toddler&&<button className="delete" onClick={()=>{if(confirm(bg?'Да изтрием рисунката?':'Delete this drawing?'))deleteDrawing(d.id).then(gallery)}}>{bg?'Изтрий':'Delete'}</button>}
            </div>})}</div>}
        </main>}

        {screen==='parents'&&<main className="settings">
          <button className="back-link" onClick={()=>setScreen('home')}>← {bg?'Назад':'Back'}</button><h1>{bg?'Настройки за родители':'Parent settings'}</h1>
          <label>{bg?'Език':'Language'}<select value={language} onChange={e=>setLanguage(e.target.value as 'bg'|'en')}><option value="bg">Български</option><option value="en">English</option></select></label>
          <label>{bg?'Лесен режим за малки деца':'Simple mode for toddlers'}<input type="checkbox" checked={toddler} onChange={e=>setToddler(e.target.checked)}/></label>
          <label>{bg?'Звуци':'Sounds'}<input type="checkbox" checked={sound} onChange={e=>setSound(e.target.checked)}/></label>
          <p>{bg?'Рисунките се пазят само на това устройство. Няма акаунт или проследяване.':'Drawings stay on this device. No account or tracking.'}</p>
        </main>}
      </div>
    </>}

    {gate&&<div className="modal-backdrop"><form className="gate" onSubmit={e=>{e.preventDefault();if(answer==='7'){setGate(false);setScreen('parents')}else setAnswer('')}}>
      <h2>{bg?'Зона за родители':'Parents only'}</h2><p>{bg?'Колко е 4 + 3?':'What is 4 + 3?'}</p>
      <input autoFocus inputMode="numeric" value={answer} onChange={e=>setAnswer(e.target.value)} aria-label={bg?'Отговор':'Answer'}/>
      <div><button type="button" onClick={()=>setGate(false)}>{bg?'Отказ':'Cancel'}</button><button className="primary" type="submit">{bg?'Продължи':'Continue'}</button></div>
    </form></div>}
    {celebrate&&<div className="celebration" role="status"><span>✦ ✧ ✦</span><strong>{bg?'Чудесна рисунка!':'Wonderful artwork!'}</strong><span>✦ ✧ ✦</span></div>}
  </div>
}
