"""Reproducibly create ten original closed-region coloring illustrations."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'public' / 'illustrations'
ROOT.mkdir(parents=True, exist_ok=True)

def shape(tag, name, **attrs):
    properties = ' '.join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<{tag} data-region="{name}" {properties}/>'

def circle(name, x, y, r):
    return shape('circle', name, cx=x, cy=y, r=r)

def ellipse(name, x, y, rx, ry):
    return shape('ellipse', name, cx=x, cy=y, rx=rx, ry=ry)

def rect(name, x, y, w, h, rx=0):
    return shape('rect', name, x=x, y=y, width=w, height=h, rx=rx)

def path(name, d):
    return shape('path', name, d=d)

def line(d):
    return f'<path d="{d}" fill="none" stroke="#293344" stroke-width="5" stroke-linecap="round" pointer-events="none"/>'

def eyes(coords):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#293344" pointer-events="none"/>' for x,y in coords)

art = {
'cat': [
  ellipse('body',200,269,88,78), path('tail','M271 270 Q342 247 326 184 Q309 166 302 191 Q311 235 266 241 Z'),
  path('ear-left','M124 157 L132 77 L181 119 Z'), path('ear-right','M220 119 L269 77 L277 157 Z'),
  circle('head',200,168,77), ellipse('muzzle',200,205,33,19), circle('nose',200,190,8),
  ellipse('paw-left',158,328,28,17),ellipse('paw-right',243,328,28,17),eyes([(172,165),(227,165)]),line('M200 196 Q191 213 180 207 M200 196 Q209 213 220 207 M151 195 L119 188 M151 205 L119 209 M249 195 L281 188 M249 205 L281 209')],
'garden': [
  path('hill-left','M22 317 Q109 237 212 317 L212 370 L22 370 Z'),path('hill-right','M188 315 Q297 229 378 310 L378 370 L188 370 Z'),
  circle('sun',322,76,34),rect('stem-one',105,238,13,77,5),rect('stem-two',246,225,13,83,5),
  *[ellipse(f'flower-a-{i}',111+dx,222+dy,16,24) for i,(dx,dy) in enumerate([(0,-26),(25,-5),(15,23),(-15,23),(-25,-5)])],
  circle('center-a',111,222,15),
  *[ellipse(f'flower-b-{i}',252+dx,205+dy,13,20) for i,(dx,dy) in enumerate([(0,-23),(22,-2),(13,20),(-13,20),(-22,-2)])],
  circle('center-b',252,205,12),ellipse('leaf-a',86,273,25,11),ellipse('leaf-b',278,267,25,11),
  ellipse('cloud-a',102,92,48,19),ellipse('cloud-b',137,91,31,22)],
'car': [
  path('car-body','M42 245 Q42 224 66 222 L88 219 L117 155 Q124 143 146 143 L252 143 Q273 143 284 159 L318 217 L342 224 Q358 226 358 248 L358 290 Q358 307 340 307 L61 307 Q42 306 42 286 Z'),
  path('window-left','M131 165 L192 165 L192 216 L104 216 Z'),path('window-right','M208 165 L255 165 L290 216 L208 216 Z'),
  circle('wheel-left',116,304,32),circle('hub-left',116,304,12),circle('wheel-right',287,304,32),circle('hub-right',287,304,12),
  ellipse('headlight-left',56,251,12,15),ellipse('headlight-right',344,251,12,15),line('M150 247 Q200 269 252 247')],
'dragon': [
  path('wing-left','M150 186 Q92 89 60 139 L77 178 L50 193 L106 230 Z'),path('wing-right','M250 186 Q308 89 340 139 L323 178 L350 193 L294 230 Z'),
  ellipse('body',200,263,80,83),path('tail','M271 281 Q342 316 317 360 L279 348 Q302 318 256 307 Z'),
  path('horn-left','M150 130 L136 75 L177 111 Z'),path('horn-right','M223 111 L264 75 L250 130 Z'),
  ellipse('head',200,168,69,61),ellipse('snout',200,201,47,24),ellipse('belly',200,276,42,59),
  ellipse('foot-left',148,329,26,17),ellipse('foot-right',252,329,26,17),eyes([(174,161),(226,161)]),line('M185 205 Q200 216 215 205')],
'dino': [
  path('tail','M264 255 L356 209 Q341 283 277 298 Z'),ellipse('body',197,265,91,74),
  path('neck','M135 250 Q126 186 147 122 L195 125 L214 238 Z'),ellipse('head',183,128,69,52),
  *[path(f'spike-{i}',f'M{x} {y} L{x+16} {y-32} L{x+31} {y+2} Z') for i,(x,y) in enumerate([(228,208),(259,224),(291,228)])],
  ellipse('leg-left',153,321,24,35),ellipse('leg-right',250,321,24,35),circle('spot-a',194,251,12),circle('spot-b',240,271,10),
  eyes([(165,120)]),line('M180 144 Q204 158 226 140')],
'fish': [
  path('tail','M294 200 L364 131 L364 269 Z'),ellipse('body',188,200,116,73),
  path('fin-top','M163 133 L192 85 L230 137 Z'),path('fin-bottom','M163 264 L204 315 L226 264 Z'),
  circle('eye',118,184,15),circle('pupil',116,184,5),
  *[circle(f'bubble-{i}',x,y,r) for i,(x,y,r) in enumerate([(68,105,13),(51,65,7),(327,70,16)])],
  *[path(f'scale-{i}',f'M{x} {y-13} Q{x+30} {y} {x} {y+13} Q{x+7} {y} {x} {y-13} Z') for i,(x,y) in enumerate([(180,176),(217,192),(178,220)])],line('M85 216 Q101 228 118 216')],
'rocket': [
  path('flame-outer','M181 308 L200 369 L219 308 Z'),path('flame-inner','M191 313 L200 346 L209 313 Z'),
  path('fin-left','M164 243 L120 320 L169 305 Z'),path('fin-right','M236 243 L280 320 L231 305 Z'),
  path('body','M167 294 L153 176 Q153 114 200 48 Q247 114 247 176 L233 294 Z'),
  path('nose','M168 123 Q180 78 200 48 Q220 78 232 123 Z'),circle('window',200,177,32),circle('window-inner',200,177,18),
  rect('base',163,293,74,24,7),*[circle(f'star-{i}',x,y,r) for i,(x,y,r) in enumerate([(81,102,8),(313,121,10),(308,286,6),(84,268,5)])]],
'apple': [
  path('apple','M200 146 Q129 100 95 164 Q66 232 111 299 Q144 357 200 332 Q256 357 289 299 Q334 232 305 164 Q271 100 200 146 Z'),
  path('leaf','M201 122 Q211 71 278 77 Q260 122 201 122 Z'),rect('stem',193,76,13,68,5),
  ellipse('cheek-left',151,226,18,11),ellipse('cheek-right',249,226,18,11),eyes([(171,202),(229,202)]),line('M180 238 Q200 257 220 238')],
'castle': [
  rect('wall',90,194,220,143),rect('tower-left',50,146,73,191),rect('tower-right',277,146,73,191),
  path('roof-left','M42 146 L86 64 L131 146 Z'),path('roof-right','M269 146 L313 64 L358 146 Z'),
  rect('tower-center',162,127,76,78),path('roof-center','M154 127 L200 40 L246 127 Z'),
  path('door','M170 337 L170 283 Q170 255 200 255 Q230 255 230 283 L230 337 Z'),
  rect('window-left',73,199,27,47,11),rect('window-right',300,199,27,47,11),rect('window-center',187,154,26,40,11),
  *[rect(f'flag-{i}',x,y,24,16) for i,(x,y) in enumerate([(86,54),(313,54),(200,30)])]],
'snowman': [
  circle('body',200,274,71),circle('head',200,157,56),
  path('hat-brim','M135 114 L265 114 L265 132 L135 132 Z'),rect('hat',163,53,74,65,8),rect('hat-band',163,96,74,14),
  path('nose','M195 161 L249 169 L195 177 Z'),rect('scarf',146,199,109,25,9),path('scarf-end','M236 216 L258 221 L253 269 L232 266 Z'),
  circle('button-a',200,253,7),circle('button-b',200,281,7),circle('button-c',200,309,7),
  circle('snow-left',69,301,23),circle('snow-right',326,324,18),eyes([(177,151),(223,151)]),line('M176 182 Q200 197 223 182 M143 254 L94 213 M258 254 L312 205')]
}

# Each new page uses its own silhouette and named, closed coloring regions.
art.update({
'dog': [ellipse('body',215,265,99,73),ellipse('tail',321,238,33,16),ellipse('ear-left',116,145,31,54),ellipse('ear-right',285,145,31,54),circle('head',200,170,75),ellipse('snout',200,213,43,30),circle('nose',200,204,12),ellipse('paw-left',155,323,28,21),ellipse('paw-right',261,323,28,21),circle('collar-tag',200,248,12),eyes([(170,168),(231,168)]),line('M200 218 Q190 232 178 220 M200 218 Q210 232 222 220')],
'rabbit': [ellipse('body',205,275,87,68),ellipse('tail',292,267,24,24),ellipse('ear-left',164,100,26,72),ellipse('ear-right',233,100,26,72),ellipse('inner-ear-left',164,101,12,51),ellipse('inner-ear-right',233,101,12,51),circle('head',200,187,70),ellipse('foot-left',146,328,35,18),ellipse('foot-right',258,328,35,18),circle('nose',200,200,8),eyes([(172,181),(228,181)]),line('M200 207 L200 222 Q184 239 172 222 M200 222 Q216 239 228 222')],
'turtle': [ellipse('shell',197,230,105,72),ellipse('shell-center',197,220,57,48),ellipse('head',313,241,41,38),ellipse('leg-front',256,300,28,29),ellipse('leg-back',119,300,28,29),path('tail','M95 250 L54 275 L102 278 Z'),circle('shell-spot-left',131,226,15),circle('shell-spot-right',263,226,15),circle('eye',325,229,7),line('M322 254 Q337 265 346 252')],
'butterfly': [ellipse('wing-upper-left',130,165,69,65),ellipse('wing-upper-right',270,165,69,65),ellipse('wing-lower-left',150,264,54,58),ellipse('wing-lower-right',250,264,54,58),ellipse('body',200,217,21,104),circle('head',200,107,25),circle('spot-a',127,161,21),circle('spot-b',273,161,21),circle('spot-c',151,261,17),circle('spot-d',249,261,17),eyes([(192,105),(208,105)]),line('M187 87 Q160 60 160 47 M213 87 Q240 60 240 47')],
'tree': [rect('trunk',177,206,46,128,8),circle('crown-left',145,172,56),circle('crown-right',252,172,56),circle('crown-top',200,119,64),circle('fruit-one',138,165,12),circle('fruit-two',239,150,12),circle('fruit-three',196,109,12),ellipse('grass-left',93,338,54,12),ellipse('grass-right',300,338,54,12),line('M35 354 L365 354')],
'mountain': [path('mountain-left','M30 323 L142 95 L253 323 Z'),path('snow-left','M105 171 L142 95 L180 172 L151 160 L140 178 Z'),path('mountain-right','M178 323 L277 130 L377 323 Z'),path('snow-right','M241 201 L277 130 L315 203 L285 187 L274 207 Z'),circle('sun',332,68,31),ellipse('cloud',95,71,51,19),rect('little-tree-trunk',74,276,13,60),path('little-tree','M41 293 L80 224 L117 293 Z')],
'rainbow': [path('arc-red','M35 308 A165 165 0 0 1 365 308 L339 308 A139 139 0 0 0 61 308 Z'),path('arc-orange','M61 308 A139 139 0 0 1 339 308 L314 308 A114 114 0 0 0 86 308 Z'),path('arc-yellow','M86 308 A114 114 0 0 1 314 308 L289 308 A89 89 0 0 0 111 308 Z'),path('arc-green','M111 308 A89 89 0 0 1 289 308 L264 308 A64 64 0 0 0 136 308 Z'),path('arc-blue','M136 308 A64 64 0 0 1 264 308 L238 308 A38 38 0 0 0 162 308 Z'),ellipse('cloud-left',54,315,45,30),ellipse('cloud-right',346,315,45,30),circle('sun',320,86,30)],
'mushroom': [rect('stem',172,200,56,139,20),path('cap','M72 212 Q84 88 200 88 Q316 88 328 212 Z'),circle('spot-one',139,163,22),circle('spot-two',221,122,19),circle('spot-three',268,178,17),ellipse('grass-left',103,335,47,16),ellipse('grass-right',302,335,47,16),circle('little-mushroom-cap',53,308,21),rect('little-mushroom-stem',48,308,10,34,4)],
'bus': [rect('body',45,147,311,161,29),rect('window-one',73,169,66,63,10),rect('window-two',154,169,66,63,10),rect('window-three',236,169,87,63,10),rect('door',243,235,68,72,8),circle('wheel-left',112,307,31),circle('hub-left',112,307,12),circle('wheel-right',294,307,31),circle('hub-right',294,307,12),ellipse('light-left',56,264,12,16),ellipse('light-right',345,264,12,16)],
'train': [rect('engine',190,145,153,170,20),rect('chimney',260,89,35,65,5),rect('cab-window',212,167,63,58,8),circle('engine-wheel',280,313,32),rect('wagon',50,189,135,110,13),rect('wagon-window',71,210,52,42,5),circle('wagon-wheel-a',87,304,23),circle('wagon-wheel-b',150,304,23),circle('steam-one',269,61,17),circle('steam-two',233,40,12),path('front','M342 247 L369 271 L342 293 Z')],
'plane': [path('fuselage','M40 201 Q53 180 106 179 L273 180 L345 196 Q365 205 345 217 L269 233 L103 225 Q56 225 40 201 Z'),path('wing-top','M170 185 L218 84 L252 88 L234 185 Z'),path('wing-bottom','M172 221 L238 315 L270 312 L238 217 Z'),path('tail-top','M73 182 L62 132 L89 135 L117 182 Z'),path('tail-bottom','M76 223 L68 262 L94 257 L118 221 Z'),circle('window-one',278,206,10),circle('window-two',310,206,10),circle('sun',330,86,24)],
'boat': [path('hull','M49 251 L352 251 L299 324 L102 324 Z'),path('sail-main','M195 241 L195 75 L79 238 Z'),path('sail-small','M209 104 L209 241 L317 241 Z'),rect('mast',196,69,11,187,3),path('flag','M205 72 L264 89 L205 109 Z'),ellipse('wave-a',99,344,57,12),ellipse('wave-b',228,350,65,12),ellipse('wave-c',333,344,43,12),circle('sun',330,65,25)]
})

art.update({
'unicorn': [ellipse('body',210,276,92,60),path('neck','M131 273 L145 145 L207 154 L205 259 Z'),ellipse('head',179,151,74,45),path('horn','M170 112 L191 46 L206 113 Z'),path('mane','M119 146 L103 100 L147 126 L151 177 Z'),path('tail','M284 258 Q355 219 334 306 L299 304 Z'),rect('leg-left',156,309,24,50,8),rect('leg-right',258,309,24,50,8),circle('star',247,264,16),circle('eye',158,147,6),line('M185 169 Q199 180 214 168')],
'wizard': [path('robe','M154 191 L246 191 L304 349 L96 349 Z'),circle('face',200,158,50),path('hat','M116 139 L199 48 L284 139 Z'),rect('hat-band',138,131,124,18,5),ellipse('beard',200,204,42,52),circle('star-hat',200,103,14),rect('wand',284,170,11,143,3),circle('wand-tip',289,162,17),circle('robe-star-a',150,286,12),circle('robe-star-b',246,301,12),eyes([(180,155),(220,155)])],
'fairy': [ellipse('wing-left',131,189,53,78),ellipse('wing-right',269,189,53,78),path('dress','M170 232 L230 232 L273 339 L127 339 Z'),circle('face',200,150,44),ellipse('hair',200,119,51,25),rect('arm-left',129,225,49,17,8),rect('arm-right',224,225,49,17,8),ellipse('shoe-left',165,344,21,10),ellipse('shoe-right',235,344,21,10),circle('wand-star',312,120,21),rect('wand-stick',304,141,8,86,3),eyes([(183,151),(217,151)]),line('M187 172 Q200 184 213 172')],
'robot': [rect('head',115,91,170,121,20),rect('body',107,220,186,112,24),rect('eye-left',143,132,42,37,11),rect('eye-right',215,132,42,37,11),rect('mouth',158,184,84,13,6),rect('arm-left',61,234,43,81,16),rect('arm-right',296,234,43,81,16),rect('leg-left',139,329,43,38,9),rect('leg-right',218,329,43,38,9),rect('antenna',194,60,12,34,4),circle('antenna-tip',200,53,13),circle('button-a',168,271,9),circle('button-b',232,271,9)],
'stegosaurus': [path('tail','M278 258 L367 202 L326 287 Z'),ellipse('body',199,263,101,67),path('head','M92 253 Q54 206 75 184 Q106 167 139 208 L143 273 Z'),*[path(f'plate-{i}',f'M{x} {y} L{x+20} {y-58} L{x+43} {y+3} Z') for i,(x,y) in enumerate([(133,212),(177,192),(222,202),(266,228)])],ellipse('leg-one',145,326,21,31),ellipse('leg-two',257,326,21,31),circle('eye',96,211,7),circle('spot',220,274,13),line('M84 238 Q100 249 113 236')],
'triceratops': [ellipse('body',218,269,109,67),path('frill','M144 159 Q176 79 282 126 L294 211 Q236 250 156 216 Z'),ellipse('face',168,208,78,56),path('horn-left','M104 174 L89 111 L130 168 Z'),path('horn-right','M207 161 L237 102 L232 178 Z'),path('nose-horn','M99 220 L74 195 L106 207 Z'),ellipse('leg-left',156,327,22,32),ellipse('leg-right',285,327,22,32),circle('eye',150,204,7),circle('frill-dot',246,167,18),line('M116 233 Q133 247 150 233')],
'pterodactyl': [path('wing-left','M185 195 Q122 100 39 136 L74 177 L54 215 L145 230 Z'),path('wing-right','M215 195 Q278 100 361 136 L326 177 L346 215 L255 230 Z'),ellipse('body',200,236,43,74),ellipse('head',199,151,43,39),path('beak','M163 163 L67 195 L176 185 Z'),path('crest','M206 121 L259 63 L239 142 Z'),path('foot-left','M176 302 L151 333 L194 322 Z'),path('foot-right','M224 302 L249 333 L206 322 Z'),circle('eye',187,150,7),circle('cloud',320,64,24)],
'brontosaurus': [path('tail','M273 273 L366 213 Q346 301 283 316 Z'),ellipse('body',199,278,98,64),path('neck','M105 269 Q103 179 145 98 L190 116 Q166 212 174 270 Z'),ellipse('head',155,115,67,37),ellipse('foot-left',149,332,29,27),ellipse('foot-right',267,332,29,27),circle('body-spot-a',208,254,17),circle('body-spot-b',252,282,13),circle('eye',132,110,6),line('M157 133 Q177 145 193 129')],
'octopus': [path('tentacle-left','M150 243 Q63 216 55 290 Q41 335 103 324 L103 304 Q73 305 82 283 Q92 263 151 289 Z'),path('tentacle-right','M250 243 Q337 216 345 290 Q359 335 297 324 L297 304 Q327 305 318 283 Q308 263 249 289 Z'),path('tentacle-center','M167 273 Q117 350 165 359 Q199 364 201 329 Q203 364 237 359 Q286 349 234 273 Z'),ellipse('head',200,194,86,91),circle('spot-left',155,144,15),circle('spot-right',253,151,15),circle('sucker-left',101,301,9),circle('sucker-right',299,301,9),eyes([(172,190),(228,190)]),line('M181 225 Q200 243 219 225')],
'crab': [ellipse('body',200,258,91,65),ellipse('eye-stalk-left',166,166,12,56),ellipse('eye-stalk-right',234,166,12,56),circle('eye-left',166,116,15),circle('eye-right',234,116,15),path('claw-left','M100 226 Q38 174 50 145 L81 178 L99 143 Q124 188 114 231 Z'),path('claw-right','M300 226 Q362 174 350 145 L319 178 L301 143 Q276 188 286 231 Z'),*[ellipse(f'leg-{i}',x,y,32,13) for i,(x,y) in enumerate([(92,295),(110,322),(308,295),(290,322)])],eyes([(166,116),(234,116)]),line('M180 270 Q200 287 220 270')],
'whale': [path('body','M51 230 Q53 173 161 174 Q250 161 302 204 L355 170 L351 231 L308 244 Q282 315 168 318 Q72 312 51 230 Z'),path('belly','M65 249 Q166 280 300 237 Q260 305 168 318 Q95 315 65 249 Z'),path('tail-top','M309 199 Q317 130 374 136 Q369 179 333 215 Z'),circle('eye',138,221,8),circle('spout-one',240,125,11),circle('spout-two',259,91,13),circle('spout-three',223,86,9),ellipse('fin',208,265,36,16),line('M82 254 Q109 270 132 253')],
'seahorse': [path('body','M207 105 Q274 90 293 153 Q306 200 259 222 Q296 258 272 303 Q238 354 191 319 Q166 298 197 274 Q216 266 224 287 Q217 305 238 299 Q255 279 221 254 Q167 225 184 175 Q150 152 169 122 Z'),path('snout','M175 132 L105 131 L111 160 L181 165 Z'),path('crown','M190 105 L177 65 L207 89 L228 61 L238 109 Z'),path('fin','M266 190 L330 145 L303 218 Z'),circle('eye',215,139,8),circle('spot-a',236,197,11),circle('spot-b',223,230,9),circle('bubble-one',85,83,13),circle('bubble-two',321,91,19)]
})

art.update({
'astronaut': [ellipse('helmet',200,143,76,82),ellipse('visor',200,149,57,55),rect('suit',137,226,126,105,31),rect('backpack',110,233,35,81,8),rect('arm-left',75,235,66,33,14),rect('arm-right',260,235,66,33,14),ellipse('glove-left',73,252,19,24),ellipse('glove-right',327,252,19,24),rect('boot-left',149,314,42,48,11),rect('boot-right',210,314,42,48,11),circle('badge',200,262,18),circle('star-a',90,98,13),circle('star-b',320,123,11),eyes([(182,148),(218,148)]),line('M187 176 Q200 186 213 176')],
'moon': [circle('moon',200,194,116),circle('crater-one',156,149,30),circle('crater-two',247,222,39),circle('crater-three',143,253,20),circle('crater-four',244,125,17),circle('star-one',75,77,12),circle('star-two',322,79,17),circle('star-three',323,312,10)],
'alien': [ellipse('body',200,273,76,72),ellipse('head',200,150,84,72),ellipse('eye-left',167,158,20,27),ellipse('eye-right',233,158,20,27),ellipse('arm-left',104,271,28,57),ellipse('arm-right',296,271,28,57),ellipse('foot-left',155,336,31,19),ellipse('foot-right',245,336,31,19),circle('antenna-tip-left',147,65,14),circle('antenna-tip-right',253,65,14),line('M169 86 L153 65 M231 86 L247 65 M182 205 Q200 215 218 205')],
'saturn': [path('ring-back','M37 202 Q122 115 298 146 Q371 164 372 204 Q298 160 192 173 Q94 183 37 222 Z'),circle('planet',201,205,91),path('stripe-one','M120 164 Q201 193 283 166 L282 188 Q201 215 121 187 Z'),path('stripe-two','M119 224 Q201 249 284 221 L276 246 Q201 270 126 248 Z'),path('ring-front','M39 225 Q129 279 259 251 Q344 232 367 204 L378 217 Q319 301 189 302 Q75 302 32 242 Z'),circle('star-a',60,80,13),circle('star-b',325,86,15),circle('star-c',340,317,9)],
'banana': [path('peel','M72 182 Q153 334 315 168 Q330 231 287 287 Q160 381 72 221 Z'),path('fruit','M76 170 Q172 315 315 156 Q277 277 158 287 Q104 273 76 170 Z'),path('tip-left','M62 165 L90 171 L87 206 L67 196 Z'),path('tip-right','M308 149 L338 141 L331 176 L310 183 Z'),ellipse('spot-a',170,307,12,7),ellipse('spot-b',214,297,10,6),circle('sun',322,75,26)],
'strawberry': [path('berry','M200 125 Q118 82 96 160 Q75 264 200 349 Q325 264 304 160 Q282 82 200 125 Z'),path('leaf-left','M197 127 Q122 66 84 110 Q128 154 197 143 Z'),path('leaf-right','M203 127 Q278 66 316 110 Q272 154 203 143 Z'),path('leaf-center','M200 133 Q179 64 200 50 Q221 64 200 133 Z'),*[ellipse(f'seed-{i}',x,y,6,10) for i,(x,y) in enumerate([(144,184),(198,179),(254,184),(117,231),(170,232),(229,234),(282,230),(156,279),(202,291),(246,279)])]],
'cupcake': [path('cup','M112 209 L288 209 L260 341 L140 341 Z'),path('frosting','M104 213 Q82 191 105 170 Q99 145 129 134 Q126 111 162 109 Q169 72 200 83 Q231 72 238 109 Q274 111 271 134 Q301 145 295 170 Q318 191 296 213 Z'),circle('cherry',200,76,20),rect('wrapper-stripe-left',164,231,15,98,4),rect('wrapper-stripe-right',221,231,15,98,4),circle('sprinkle-one',151,166,7),circle('sprinkle-two',244,156,7),circle('sprinkle-three',197,134,7),circle('sprinkle-four',265,192,7)],
'pizza': [path('slice','M200 45 L347 322 Q200 365 53 322 Z'),path('crust','M53 322 Q200 350 347 322 L362 341 Q200 389 38 341 Z'),circle('topping-one',186,183,24),circle('topping-two',139,274,23),circle('topping-three',253,278,23),circle('topping-four',217,300,13),ellipse('leaf-one',222,239,23,10),ellipse('leaf-two',157,228,19,9)],
'crown': [path('crown','M48 141 L105 192 L149 100 L200 191 L251 100 L295 192 L352 141 L322 308 L78 308 Z'),rect('band',76,302,248,39,11),circle('jewel-center',200,244,28),circle('jewel-left',120,252,19),circle('jewel-right',280,252,19),circle('gem-top',200,99,13),circle('gem-left',104,141,13),circle('gem-right',296,141,13)],
'knight': [ellipse('helmet',200,144,66,71),rect('visor',145,148,110,35,13),path('plume','M179 78 Q189 42 220 49 Q242 66 214 83 Z'),path('armor','M139 211 L261 211 L280 322 L120 322 Z'),path('shield','M77 227 L132 208 L132 309 L105 339 L77 309 Z'),rect('arm-right',269,220,40,83,15),rect('boot-left',141,316,45,44,10),rect('boot-right',214,316,45,44,10),circle('armor-star',200,267,21),rect('sword',320,158,10,179,4),rect('sword-guard',295,210,60,13,5),eyes([(177,166),(223,166)])],
'tower': [rect('tower',124,121,152,220,6),path('roof','M105 121 L200 40 L295 121 Z'),rect('door',169,269,62,72,26),rect('window-one',176,153,48,58,17),rect('window-two',176,225,48,34,15),rect('flag-pole',197,29,7,29),path('flag','M204 30 L261 46 L204 62 Z'),ellipse('bush-left',79,316,39,27),ellipse('bush-right',321,316,39,27),circle('sun',325,75,24)],
'carriage': [path('coach','M80 189 Q91 102 200 103 Q309 102 320 189 L312 270 L88 270 Z'),path('roof','M80 187 Q105 91 200 84 Q295 91 320 187 Z'),rect('door',171,185,58,84,15),rect('window-left',105,186,51,49,11),rect('window-right',244,186,51,49,11),circle('wheel-left',116,292,42),circle('hub-left',116,292,15),circle('wheel-right',284,292,42),circle('hub-right',284,292,15),circle('lantern',337,199,15),line('M330 238 L365 219')],
'pumpkin': [ellipse('pumpkin-left',149,250,65,89),ellipse('pumpkin-right',251,250,65,89),ellipse('pumpkin-center',200,250,74,96),rect('stem',192,122,16,45,5),path('leaf','M198 139 Q242 91 275 120 Q248 154 198 153 Z'),path('eye-left','M133 232 L163 209 L176 238 Z'),path('eye-right','M224 238 L237 209 L267 232 Z'),path('mouth','M143 275 Q200 316 257 275 L244 294 Q200 328 156 294 Z')],
'sunflower': [rect('stem',192,203,16,149,5),ellipse('leaf-left',162,288,43,17),ellipse('leaf-right',236,310,43,17),*[ellipse(f'petal-{i}',200+dx,165+dy,18,42) for i,(dx,dy) in enumerate([(0,-76),(53,-53),(76,0),(53,53),(0,76),(-53,53),(-76,0),(-53,-53)])],circle('center',200,165,52),circle('seed-a',183,153,7),circle('seed-b',217,153,7),circle('seed-c',200,181,7)],
'umbrella': [path('canopy','M55 219 Q63 88 200 86 Q337 88 345 219 Q311 195 272 219 Q237 194 200 219 Q163 194 128 219 Q89 195 55 219 Z'),rect('handle',194,214,12,109,4),path('hook','M194 317 L206 317 Q206 350 235 341 Q250 337 247 318 L260 318 Q271 355 237 362 Q195 366 194 317 Z'),circle('rain-a',76,271,12),circle('rain-b',115,300,10),circle('rain-c',322,277,12),circle('rain-d',291,318,10),line('M200 91 L200 214')],
'christmas-tree': [path('top','M200 45 L105 181 L295 181 Z'),path('middle','M200 109 L73 248 L327 248 Z'),path('bottom','M200 180 L51 328 L349 328 Z'),rect('trunk',177,326,46,42,5),circle('star',200,46,17),circle('bauble-a',128,218,14),circle('bauble-b',253,196,14),circle('bauble-c',117,295,14),circle('bauble-d',278,289,14),circle('bauble-e',200,259,14)]
})

for name, parts in art.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" role="img" aria-label="{name}">
<rect width="400" height="400" fill="white"/>
<g fill="white" stroke="#293344" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">{''.join(parts)}</g>
</svg>'''
    (ROOT / f'{name}.svg').write_text(svg, encoding='utf-8')
print(f'Generated {len(art)} original illustrations in {ROOT}')
