export type Difficulty = 'easy' | 'medium' | 'advanced';
export type Page = { id: string; category: string; title: { bg: string; en: string }; difficulty: Difficulty; asset: string };
export const categories = [
  { id:'animals', bg:'Животни', en:'Animals', color:'#ffc478' },
  { id:'nature', bg:'Природа', en:'Nature', color:'#92dfa0' },
  { id:'vehicles', bg:'Превозни средства', en:'Vehicles', color:'#91caff' },
  { id:'fantasy', bg:'Герои и фантазия', en:'Fantasy', color:'#dfa4ef' },
  { id:'dinosaurs', bg:'Динозаври', en:'Dinosaurs', color:'#9fe7ce' },
  { id:'ocean', bg:'Морски свят', en:'Ocean', color:'#80dce9' },
  { id:'space', bg:'Космос', en:'Space', color:'#a5adf8' },
  { id:'food', bg:'Храна и плодове', en:'Food', color:'#ffb1ad' },
  { id:'fairytales', bg:'Приказки', en:'Fairy tales', color:'#d6b1f5' },
  { id:'seasons', bg:'Сезони и празници', en:'Seasons', color:'#ffe184' },
  { id:'farm', bg:'Ферма', en:'Farm', color:'#b7df73' },
  { id:'toys', bg:'Играчки', en:'Toys', color:'#ffa9d7' }
] as const;
export const pages: Page[] = [
  ['cat','animals','Коте','Kitten','easy'], ['dog','animals','Кученце','Puppy','easy'],
  ['rabbit','animals','Зайче','Bunny','easy'], ['turtle','animals','Костенурка','Turtle','easy'],
  ['butterfly','animals','Пеперуда','Butterfly','medium'], ['horse','animals','Конче на поляната','Horse in a meadow','advanced'],
  ['garden','nature','Градина','Garden','medium'], ['tree','nature','Дърво','Tree','easy'],
  ['mountain','nature','Планина','Mountain','medium'], ['rainbow','nature','Дъга','Rainbow','easy'],
  ['mushroom','nature','Гъбка','Mushroom','easy'], ['forest','nature','Горска пътека','Forest path','advanced'],
  ['car','vehicles','Весела кола','Happy car','easy'], ['bus','vehicles','Автобус','Bus','easy'],
  ['train','vehicles','Влак','Train','medium'], ['plane','vehicles','Самолет','Airplane','medium'],
  ['boat','vehicles','Лодка','Boat','easy'], ['truck','vehicles','Товарен камион','Cargo truck','advanced'],
  ['dragon','fantasy','Малък дракон','Little dragon','medium'], ['unicorn','fantasy','Еднорог','Unicorn','medium'],
  ['wizard','fantasy','Магьосник','Wizard','medium'], ['fairy','fantasy','Фея','Fairy','medium'],
  ['robot','fantasy','Роботче','Robot','easy'], ['griffin','fantasy','Грифон','Griffin','advanced'],
  ['dino','dinosaurs','Динозавърче','Baby dinosaur','easy'], ['stegosaurus','dinosaurs','Стегозавър','Stegosaurus','medium'],
  ['triceratops','dinosaurs','Трицератопс','Triceratops','medium'], ['pterodactyl','dinosaurs','Птеродактил','Pterodactyl','medium'],
  ['brontosaurus','dinosaurs','Бронтозавър','Brontosaurus','easy'], ['trex','dinosaurs','Тиранозавър','Tyrannosaurus','advanced'],
  ['fish','ocean','Рибка','Fish','easy'], ['octopus','ocean','Октопод','Octopus','medium'],
  ['crab','ocean','Раче','Crab','medium'], ['whale','ocean','Кит','Whale','easy'],
  ['seahorse','ocean','Морско конче','Seahorse','medium'], ['dolphin','ocean','Делфин','Dolphin','advanced'],
  ['rocket','space','Ракета','Rocket','medium'], ['astronaut','space','Космонавт','Astronaut','medium'],
  ['moon','space','Луна','Moon','easy'], ['alien','space','Добро извънземно','Friendly alien','easy'],
  ['saturn','space','Сатурн','Saturn','medium'], ['lander','space','Лунен модул','Lunar lander','advanced'],
  ['apple','food','Ябълка','Apple','easy'], ['banana','food','Банан','Banana','easy'],
  ['strawberry','food','Ягода','Strawberry','medium'], ['cupcake','food','Кексче','Cupcake','medium'],
  ['pizza','food','Пица','Pizza','easy'], ['pineapple','food','Ананас','Pineapple','advanced'],
  ['castle','fairytales','Замък','Castle','advanced'], ['crown','fairytales','Корона','Crown','easy'],
  ['knight','fairytales','Рицар','Knight','medium'], ['tower','fairytales','Кула','Tower','medium'],
  ['carriage','fairytales','Карета','Carriage','medium'], ['cottage','fairytales','Приказна къщичка','Storybook cottage','advanced'],
  ['snowman','seasons','Снежен човек','Snowman','easy'], ['pumpkin','seasons','Тиква','Pumpkin','easy'],
  ['sunflower','seasons','Слънчоглед','Sunflower','medium'], ['umbrella','seasons','Чадър','Umbrella','easy'],
  ['christmas-tree','seasons','Коледна елха','Christmas tree','medium'], ['autumn-park','seasons','Есенен парк','Autumn park','advanced'],
  ['cow','farm','Крава','Cow','medium'], ['sheep','farm','Овца','Sheep','easy'],
  ['pig','farm','Прасенце','Piglet','easy'], ['hen','farm','Кокошка','Hen','medium'],
  ['barn','farm','Плевня','Barn','medium'], ['tractor','farm','Трактор','Tractor','medium'],
  ['teddy','toys','Плюшено мече','Teddy bear','easy'], ['kite','toys','Хвърчило','Kite','easy'],
  ['drum','toys','Барабан','Drum','medium'], ['ball','toys','Шарена топка','Colorful ball','easy'],
  ['blocks','toys','Кубчета','Building blocks','medium'], ['rocking-horse','toys','Люлеещо се конче','Rocking horse','advanced']
].map(([id,category,bg,en,difficulty]) => ({ id,category,title:{bg,en},difficulty:difficulty as Difficulty,asset:`/illustrations/${id}.svg` }));
export const getDailyPage = (date: Date) => pages[Math.floor(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate())/86400000)%pages.length];
export function nextSurprise(seen: string[], random = Math.random): { page: Page; seen: string[] } {
  const valid=new Set(pages.map(p=>p.id));
  const used=[...new Set(seen.filter(id=>valid.has(id)))];
  // At the end of a cycle, keep the last picture out of the next draw.
  const cycle=used.length===pages.length?used.slice(-1):used;
  const remaining=pages.filter(p=>!cycle.includes(p.id));
  const page=remaining[Math.min(remaining.length-1,Math.floor(Math.max(0,random())*remaining.length))];
  return {page,seen:[...cycle,page.id]};
}
