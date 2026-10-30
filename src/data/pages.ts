export type Difficulty = 'easy' | 'medium' | 'advanced';
export type Page = { id: string; category: string; title: { bg: string; en: string }; difficulty: Difficulty; asset: string };
export const categories = [
  { id:'animals', bg:'Животни', en:'Animals', color:'#ffcf95' },
  { id:'nature', bg:'Природа', en:'Nature', color:'#b9e6ac' },
  { id:'vehicles', bg:'Превозни средства', en:'Vehicles', color:'#b5d4ff' },
  { id:'fantasy', bg:'Герои и фантазия', en:'Fantasy', color:'#efc7f5' },
  { id:'dinosaurs', bg:'Динозаври', en:'Dinosaurs', color:'#bce9d3' },
  { id:'ocean', bg:'Морски свят', en:'Ocean', color:'#a9e8ef' },
  { id:'space', bg:'Космос', en:'Space', color:'#c6c8f6' },
  { id:'food', bg:'Храна и плодове', en:'Food', color:'#ffd2d1' },
  { id:'fairytales', bg:'Приказки', en:'Fairy tales', color:'#ead1f7' },
  { id:'seasons', bg:'Сезони и празници', en:'Seasons', color:'#ffe9a7' }
] as const;
export const pages: Page[] = [
  ['cat','animals','Коте','Kitten','easy'], ['dog','animals','Кученце','Puppy','easy'],
  ['rabbit','animals','Зайче','Bunny','easy'], ['turtle','animals','Костенурка','Turtle','easy'],
  ['butterfly','animals','Пеперуда','Butterfly','medium'],
  ['garden','nature','Градина','Garden','medium'], ['tree','nature','Дърво','Tree','easy'],
  ['mountain','nature','Планина','Mountain','medium'], ['rainbow','nature','Дъга','Rainbow','easy'],
  ['mushroom','nature','Гъбка','Mushroom','easy'],
  ['car','vehicles','Весела кола','Happy car','easy'], ['bus','vehicles','Автобус','Bus','easy'],
  ['train','vehicles','Влак','Train','medium'], ['plane','vehicles','Самолет','Airplane','medium'],
  ['boat','vehicles','Лодка','Boat','easy'],
  ['dragon','fantasy','Малък дракон','Little dragon','medium'], ['unicorn','fantasy','Еднорог','Unicorn','medium'],
  ['wizard','fantasy','Магьосник','Wizard','medium'], ['fairy','fantasy','Фея','Fairy','medium'],
  ['robot','fantasy','Роботче','Robot','easy'],
  ['dino','dinosaurs','Динозавърче','Baby dinosaur','easy'], ['stegosaurus','dinosaurs','Стегозавър','Stegosaurus','medium'],
  ['triceratops','dinosaurs','Трицератопс','Triceratops','medium'], ['pterodactyl','dinosaurs','Птеродактил','Pterodactyl','medium'],
  ['brontosaurus','dinosaurs','Бронтозавър','Brontosaurus','easy'],
  ['fish','ocean','Рибка','Fish','easy'], ['octopus','ocean','Октопод','Octopus','medium'],
  ['crab','ocean','Раче','Crab','medium'], ['whale','ocean','Кит','Whale','easy'],
  ['seahorse','ocean','Морско конче','Seahorse','medium'],
  ['rocket','space','Ракета','Rocket','medium'], ['astronaut','space','Космонавт','Astronaut','medium'],
  ['moon','space','Луна','Moon','easy'], ['alien','space','Добро извънземно','Friendly alien','easy'],
  ['saturn','space','Сатурн','Saturn','medium'],
  ['apple','food','Ябълка','Apple','easy'], ['banana','food','Банан','Banana','easy'],
  ['strawberry','food','Ягода','Strawberry','medium'], ['cupcake','food','Кексче','Cupcake','medium'],
  ['pizza','food','Пица','Pizza','easy'],
  ['castle','fairytales','Замък','Castle','advanced'], ['crown','fairytales','Корона','Crown','easy'],
  ['knight','fairytales','Рицар','Knight','medium'], ['tower','fairytales','Кула','Tower','medium'],
  ['carriage','fairytales','Карета','Carriage','medium'],
  ['snowman','seasons','Снежен човек','Snowman','easy'], ['pumpkin','seasons','Тиква','Pumpkin','easy'],
  ['sunflower','seasons','Слънчоглед','Sunflower','medium'], ['umbrella','seasons','Чадър','Umbrella','easy'],
  ['christmas-tree','seasons','Коледна елха','Christmas tree','medium']
].map(([id,category,bg,en,difficulty]) => ({ id,category,title:{bg,en},difficulty:difficulty as Difficulty,asset:`/illustrations/${id}.svg` }));
export const getDailyPage = (date: Date) => pages[Math.floor(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate())/86400000)%pages.length];
