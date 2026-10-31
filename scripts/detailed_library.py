"""Authored Detailed vector library. Never writes the three reviewed masters.

Each subject has an explicit silhouette/composition. Shared helpers are drawing
primitives (leaves, wheels, windows), not legacy-SVG decoration. Regeneration is
opt-in per subject: python3 scripts/detailed_library.py dog rabbit
"""
from pathlib import Path
import sys, math
from generate_art_v2 import Drawing
OUT=Path(__file__).resolve().parents[1]/'public/illustrations/v2/detailed'
ART={}
def art(name):
 a=Drawing(name.replace('-',' ').title(),'detailed');ART[name]=a;return a
def r(a,n,d):a.region(n,d)
def e(a,n,x,y,rx,ry=None):a.ellipse(n,x,y,rx,rx if ry is None else ry)
def ink(a,d):a.ink(d,1.25)
def group(a,s):a.parts.append(f'<g transform="{s}">')
def end(a):a.parts.append('</g>')
def ground(a):ink(a,'M46 350 Q100 343 143 349 M251 349 Q300 343 355 350 M72 340 l4 -9 l5 10 M307 338 l5 -10 l5 10')
def leaf(a,n,x,y,s=1,rot=0):
 group(a,f'translate({x} {y}) rotate({rot}) scale({s})');r(a,n,'M0 0 C-23 -6 -31 -25 -28 -42 C-6 -38 8 -18 0 0 Z');ink(a,'M0 0 Q-14 -19 -23 -33 M-11 -18 L-23 -20 M-16 -26 L-16 -34');end(a)
def flower(a,n,x,y,s=1):
 group(a,f'translate({x} {y}) scale({s})')
 for i in range(6):
  t=i*60;group(a,f'rotate({t})');r(a,f'{n}-petal-{i}','M-5 -7 C-26 -24 -12 -43 0 -33 C13 -44 27 -25 5 -7 Z');end(a)
 e(a,n+'-center',0,0,10);end(a)
def eye(a,n,x,y,rx=8):
 e(a,n,x,y,rx,rx*.72);a.pupil(x+1,y,2.6,3.5)
def wheel(a,n,x,y,s):
 e(a,n+'-tire',x,y,s);e(a,n+'-rim',x,y,s*.65);e(a,n+'-axle',x,y,s*.19)
 for i in range(8):
  t=i*math.pi/4;ink(a,f'M{x+math.cos(t)*s*.27} {y+math.sin(t)*s*.27} L{x+math.cos(t)*s*.56} {y+math.sin(t)*s*.56}')
def cloud(a,n,x,y,s=1):
 group(a,f'translate({x} {y}) scale({s})');r(a,n,'M0 25 C-17 25 -19 7 -5 4 C-4 -13 18 -19 28 -5 C42 -16 60 -6 60 9 C77 4 88 23 72 28 Z');end(a)
def tree(a,n,x,y,s=1):
 group(a,f'translate({x} {y}) scale({s})');r(a,n+'-trunk','M-8 0 L-6 -80 L-23 -104 L-14 -109 L2 -88 L20 -117 L27 -111 L9 -76 L11 0 Z');r(a,n+'-crown','M-48 -83 C-73 -83 -82 -112 -60 -128 C-65 -155 -42 -170 -20 -161 C-10 -188 26 -185 39 -161 C67 -169 91 -146 76 -123 C99 -95 67 -67 41 -78 C17 -59 -12 -65 -24 -80 C-33 -74 -44 -76 -48 -83 Z');ink(a,'M-40 -131 Q-26 -148 -12 -135 M18 -149 Q33 -160 47 -142 M-22 -100 Q-4 -112 10 -98 M45 -109 Q58 -122 67 -109 M0 -15 L0 -54');end(a)

# Companion animals: weight-bearing limbs, separate facial anatomy and tapered tails.
a=art('dog');r(a,'tail','M274 278 C306 268 332 239 328 216 C345 216 351 246 328 274 L291 302 Z');r(a,'body','M148 183 C124 207 126 254 143 293 L169 326 L277 326 C301 307 287 259 258 229 L239 190 Z');r(a,'hind-leg','M256 260 C291 271 302 308 279 325 L235 329 Q218 323 229 310 L253 302 Q234 282 256 260 Z');r(a,'chest','M158 188 Q196 211 230 190 C239 222 219 259 196 280 C176 263 155 226 158 188 Z');r(a,'front-leg-left','M150 227 Q164 215 177 232 L178 308 Q193 318 182 330 L145 330 Q132 326 143 313 Z');r(a,'front-leg-right','M201 235 Q216 220 226 233 L231 310 Q249 319 238 332 L204 332 Q192 328 201 313 Z');r(a,'head','M142 115 C147 79 193 72 226 88 C250 99 255 135 245 166 C238 194 216 212 191 207 C156 204 137 171 142 115 Z');r(a,'ear-left','M151 101 C124 94 106 117 110 158 C112 189 129 195 139 178 Q150 144 158 116 Z');r(a,'ear-right','M229 101 C257 91 276 119 272 155 C269 180 256 193 247 174 L235 125 Z');r(a,'muzzle','M167 163 C171 150 190 152 198 160 C209 148 229 153 232 169 C239 194 180 205 167 181 Z');r(a,'nose','M185 158 Q199 149 212 159 Q211 172 199 175 Q188 172 185 158 Z');eye(a,'eye-left',170,138);eye(a,'eye-right',225,137);r(a,'collar','M153 199 Q194 223 236 196 L240 209 Q195 236 151 213 Z');e(a,'tag',194,229,9,11);ink(a,'M199 175 L198 183 Q184 192 179 182 M198 183 Q210 192 219 181 M151 319 v8 M162 320 v8 M210 321 v8 M220 321 v8 M158 123 Q168 115 178 123 M215 122 Q227 114 235 123 M258 279 Q270 286 266 295');ground(a)
a=art('rabbit');r(a,'ear-left','M169 145 C145 119 132 51 153 39 C180 35 187 103 185 141 Z');r(a,'ear-right','M204 140 C203 101 227 44 246 54 C266 67 233 121 222 147 Z');r(a,'inner-ear-left','M165 119 Q148 72 157 54 Q172 66 174 120 Z');r(a,'inner-ear-right','M219 122 Q226 80 241 68 Q245 86 227 124 Z');e(a,'tail',280,282,25,23);r(a,'body','M168 202 C138 226 131 273 145 311 Q176 338 257 329 C300 310 290 252 251 225 L227 196 Z');r(a,'haunch','M239 260 C276 251 296 300 266 321 L216 330 Q202 319 222 307 C207 287 219 268 239 260 Z');r(a,'head','M154 152 C165 125 212 123 235 146 C251 162 252 189 236 207 C219 230 179 232 159 211 C141 196 139 174 154 152 Z');r(a,'front-paw','M173 226 Q189 217 196 237 L195 305 Q216 319 201 331 L158 331 Q143 320 161 310 Z');r(a,'muzzle','M173 192 Q184 181 196 190 Q211 180 224 190 C236 210 181 222 173 202 Z');r(a,'nose','M190 187 Q199 182 208 188 L200 197 Z');eye(a,'eye-left',169,173,7);eye(a,'eye-right',225,172,7);ink(a,'M200 197 v8 M181 200 L137 190 M181 207 L139 212 M217 199 L260 190 M217 206 L260 214 M167 320 v8 M179 320 v8 M239 316 l5 7 M252 312 l5 8 M163 245 l4 7 M154 260 l5 5');leaf(a,'clover-left',94,326,.7);leaf(a,'clover-right',97,329,.7,95);ground(a)
# Equine silhouette shared by anatomically related subjects, with distinct equipment.
for name in ['horse','unicorn','rocking-horse']:
 a=art(name)
 r(a,'tail','M105 213 C68 206 60 242 48 270 Q76 273 91 254 L115 229 Z')
 r(a,'far-hind-leg','M128 246 L137 285 L119 324 L102 324 L113 282 L105 250 Z');r(a,'far-front-leg','M239 239 L258 280 L263 324 L247 324 L237 284 L221 255 Z')
 r(a,'body-neck','M91 219 C101 185 154 187 195 194 C219 179 226 146 240 120 L268 115 C287 141 282 167 266 190 L255 223 C241 258 203 267 155 254 C117 264 90 249 91 219 Z')
 r(a,'near-hind-leg','M125 240 Q145 241 151 255 L146 285 L157 322 L139 328 L124 288 L112 262 Z');r(a,'near-front-leg','M218 240 L238 242 L226 282 L224 329 L205 329 L207 280 Z')
 r(a,'mane','M232 148 C219 179 217 194 196 203 L214 212 C236 197 251 158 254 140 Z')
 r(a,'head','M240 124 L242 88 L251 97 L260 78 L266 98 C284 100 290 123 308 139 Q321 156 303 166 L276 158 Q257 155 250 137 Z')
 r(a,'muzzle','M294 133 Q321 149 310 161 Q303 173 282 157 L277 147 Z');eye(a,'eye',273,120,6);ink(a,'M301 148 q5 -5 8 0 M291 159 l11 2 M244 101 l5 13 M132 209 Q160 202 180 211 M111 230 Q121 223 130 228 M225 180 l13 -22 M65 257 Q75 233 91 225 M212 320 h12 M140 318 l14 -4 M249 315 h13 M107 316 h15')
 if name=='unicorn':
  r(a,'horn','M263 101 L289 46 L277 109 Z');ink(a,'M272 84 l9 5 M279 69 l7 4');r(a,'mane-lock','M246 111 C220 107 214 130 224 145 Q237 138 242 146 Q225 122 252 123 Z');flower(a,'flower',70,110,.55);cloud(a,'cloud',289,281,.65)
 elif name=='rocking-horse':
  r(a,'saddle','M152 187 Q176 199 207 192 L203 218 Q174 232 150 212 Z');r(a,'rocker','M58 327 Q192 370 331 326 L336 338 Q195 387 53 339 Z');r(a,'handle','M252 162 L289 162 Q296 162 296 169 Q296 176 289 176 L252 176 Z');ink(a,'M256 137 L277 150 M278 150 L266 181 L233 213')
 else:ground(a);leaf(a,'meadow-leaf',328,324,.7,20)
# Grazing farm animals with different body plans and faces.
for name in ['cow','pig','sheep']:
 a=art(name)
 if name=='pig':r(a,'tail','M299 223 C327 227 349 210 347 193 C346 175 322 173 315 190 C309 206 329 216 337 202 L331 198 C326 206 316 198 322 190 C330 180 341 188 338 198 C334 211 319 217 301 215 Z')
 else:r(a,'tail','M287 202 Q327 208 320 253 L310 256 Q316 220 284 214 Z')
 for i,(x,y) in enumerate([(126,269),(246,269)]):r(a,f'far-leg-{i}',f'M{x} {y} h19 l-3 54 h-19 Z')
 if name=='sheep':
  r(a,'body','M112 181 C104 159 127 147 145 157 C155 134 183 140 194 150 C213 133 238 146 241 158 C265 143 283 163 279 179 C308 177 319 199 307 219 C327 242 309 266 287 264 C284 289 252 292 239 277 C219 298 196 285 187 278 C166 297 142 281 142 270 C112 282 94 259 104 243 C82 224 88 193 112 181 Z')
  ink(a,'M139 180 q12 -15 23 0 M187 167 q13 -13 25 1 M240 185 q12 -14 22 1 M157 239 q12 -13 24 1 M215 254 q12 -14 23 0 M273 236 q12 -15 22 0')
 else:r(a,'body','M105 193 C141 163 223 159 276 182 C309 199 318 237 296 263 C265 289 200 282 160 268 L117 252 Z')
 for i,x in enumerate([148,271]):r(a,f'near-leg-{i}',f'M{x} 253 Q{x+12} 260 {x+22} 254 L{x+17} 330 L{x-3} 330 Z');ink(a,f'M{x-2} 318 h20 M{x+7} 320 v9')
 if name=='cow':
  r(a,'horn-left','M95 146 Q76 125 90 112 Q91 130 106 137 Z');r(a,'horn-right','M131 136 Q148 125 145 110 Q163 123 144 146 Z')
  r(a,'patch-one','M167 179 C143 190 160 212 177 212 C194 213 194 235 210 232 C227 218 212 201 220 178 Q193 171 167 179 Z');r(a,'patch-two','M266 201 C243 197 240 216 252 226 C267 230 262 257 287 255 Q304 224 286 207 Z')
 r(a,'ear-left','M89 153 Q59 135 50 151 Q57 175 86 174 Z');r(a,'ear-right','M138 151 Q166 133 173 150 Q165 172 142 173 Z')
 r(a,'head','M84 160 C86 130 131 128 145 154 L142 204 Q135 234 112 235 Q87 234 83 209 Z')
 if name=='pig':
  r(a,'ear-fold-left','M85 153 L72 120 Q100 122 108 140 Z');r(a,'ear-fold-right','M126 139 Q145 117 161 131 L145 161 Z')
 e(a,'muzzle',113,211,27 if name!='sheep' else 16,18);e(a,'nostril-left',103,211,4,6);e(a,'nostril-right',123,211,4,6);eye(a,'eye-left',97,177,6);eye(a,'eye-right',133,177,6);ink(a,'M101 229 Q113 235 125 228 M117 150 l-5 5 l-5 -3');ground(a)
# Hen: fan tail, breast, folded wing and scaly toes.
a=art('hen')
for i,(dx,dy,rot) in enumerate([(0,0,-22),(0,0,0),(0,0,22)]):
 group(a,f'translate(106 244) rotate({rot})');r(a,f'tail-feather-{i}','M0 0 C-20 -30 -74 -56 -64 -92 C-29 -108 8 -42 13 -7 Z');ink(a,'M-48 -82 Q-18 -42 5 -8');end(a)
r(a,'body','M112 215 C141 190 182 202 205 181 L241 172 C266 215 275 263 237 289 C205 311 131 302 108 269 Q91 240 112 215 Z');r(a,'neck','M205 202 C214 178 206 146 224 131 Q249 121 263 141 C273 164 253 191 258 211 L246 218 L237 211 L226 222 L217 211 Z');r(a,'comb','M221 133 C211 117 219 100 229 112 C229 90 246 91 249 111 C263 98 276 115 261 135 Z');r(a,'beak','M261 151 L292 163 L261 173 Z');r(a,'wattle','M251 174 Q271 178 261 198 Q247 206 246 181 Z');r(a,'wing','M132 231 C159 210 201 224 226 246 C209 275 163 292 139 265 Q125 249 132 231 Z');eye(a,'eye',249,148,6);ink(a,'M145 239 Q168 232 206 249 M150 251 Q169 251 191 262 M134 276 Q156 294 182 293');r(a,'leg-left','M167 296 L177 297 L175 326 L192 334 L188 339 L171 332 L154 340 L150 335 L165 326 Z');r(a,'leg-right','M210 296 L219 296 L217 323 L236 330 L232 336 L212 329 L199 339 L194 333 L207 323 Z');ground(a)
# Water creatures, each with a species-specific profile.
a=art('turtle');r(a,'tail','M112 249 Q67 250 54 269 L117 264 Z')
for n,d in [('far-foot','M237 258 Q270 270 267 293 L241 293 L220 263 Z'),('hind-foot','M135 248 Q123 278 103 294 L126 304 Q154 283 164 258 Z'),('front-foot','M230 254 Q223 289 202 307 L229 312 Q253 289 261 260 Z')]:r(a,n,d)
r(a,'neck','M262 226 Q284 204 296 187 C315 171 348 183 349 203 Q346 230 301 232 L279 257 Z');r(a,'shell','M93 246 C101 130 253 114 285 238 Q213 288 93 246 Z');r(a,'shell-rim','M93 246 Q191 279 285 238 L291 251 Q193 295 89 259 Z');r(a,'central-scute','M162 164 L206 160 L229 196 L209 235 L166 235 L143 199 Z');ink(a,'M162 164 L147 151 M206 160 L218 151 M229 196 L271 199 M209 235 L220 269 M166 235 L148 268 M143 199 L106 200 M112 291 l9 5 M214 299 l11 5 M309 218 Q326 224 340 211');eye(a,'eye',326,198,7);ground(a)
a=art('fish');r(a,'tail','M109 210 C78 185 53 165 39 174 Q61 216 42 262 Q71 264 111 232 Z');r(a,'dorsal-fin','M144 180 Q170 116 228 133 L256 179 Z');r(a,'lower-fin','M158 256 L184 294 Q208 286 230 263 Z');r(a,'body','M92 220 C149 152 252 141 311 193 L350 215 Q356 220 346 226 C298 281 176 297 92 220 Z');r(a,'gill','M286 178 Q260 220 289 266 Q330 252 349 224 L350 215 Q328 190 286 178 Z');r(a,'pectoral-fin','M249 223 Q222 212 200 227 Q215 255 242 244 Z');eye(a,'eye',313,210,10);ink(a,'M336 230 l12 -5 M54 189 L91 215 M51 248 L92 228 M170 154 L167 173 M190 145 L188 169 M210 145 L214 167 M185 276 L185 267 M201 278 L206 267')
for x,y in [(146,211),(166,200),(186,191),(155,234),(177,224),(199,211),(180,249),(205,251),(229,192)]:ink(a,f'M{x} {y} q10 8 0 16')
for i,(x,y,s) in enumerate([(315,144,9),(334,108,13),(305,77,7)]):e(a,f'bubble-{i}',x,y,s)
leaf(a,'seaweed-left',76,333,1.1);leaf(a,'seaweed-right',80,335,1,90);ink(a,'M40 349 Q165 330 360 350')
for name in ['whale','dolphin']:
 a=art(name)
 if name=='whale':
  r(a,'body','M58 235 C40 175 92 131 158 143 C211 145 237 199 276 215 Q291 190 319 177 L319 206 Q341 195 364 196 Q351 227 319 235 C290 272 233 291 164 282 C106 288 67 269 58 235 Z');r(a,'belly','M58 235 Q123 267 195 252 Q255 248 296 239 C247 278 207 290 164 282 Q86 289 58 235 Z');r(a,'flipper','M171 229 Q216 233 236 268 C201 276 173 261 158 245 Z');eye(a,'eye',94,207,7);ink(a,'M59 233 Q85 247 119 236 M92 254 Q116 269 145 269 M119 259 Q145 276 171 273 M122 148 Q129 139 138 145');r(a,'spout-left','M129 128 C111 112 96 96 104 86 Q114 77 121 92 L137 123 Z');r(a,'spout-right','M140 126 C142 96 158 84 165 94 Q171 106 149 130 Z')
 else:
  r(a,'dorsal-fin','M181 173 Q175 123 199 99 Q208 141 239 164 Z');r(a,'body','M41 222 L85 205 C106 157 181 149 234 170 Q277 186 315 215 Q326 184 354 174 L350 210 L375 223 Q345 243 317 233 C259 252 181 261 127 241 Q92 241 79 230 L43 231 Z');r(a,'belly','M78 228 Q176 249 282 227 L317 233 Q214 278 127 241 Q92 241 78 228 Z');r(a,'flipper','M178 229 Q198 257 193 290 Q161 281 151 242 Z');eye(a,'eye',112,206,6);ink(a,'M46 227 L86 224 Q107 231 124 221 M204 185 Q242 189 273 211')
 ink(a,'M41 319 Q84 302 122 319 T204 319 T286 319 T365 319 M77 340 Q100 333 125 340 M248 341 Q280 333 310 340');cloud(a,'cloud',71,72,.65)
a=art('seahorse');r(a,'dorsal-fin','M233 171 Q279 182 263 231 L236 242 L222 205 Z');r(a,'body','M166 136 L130 145 L116 134 L123 122 L158 112 C156 76 191 60 219 79 Q250 98 229 135 C214 156 228 172 241 199 C266 247 227 276 208 298 C196 316 211 337 228 323 C242 309 224 300 218 309 L210 301 C231 279 264 307 242 335 C213 371 168 335 179 304 C186 280 209 263 208 244 C203 223 171 217 170 187 Q164 166 180 147 Z');r(a,'crest','M177 83 L172 64 L190 68 L199 49 L209 68 L230 67 L226 84 Q201 69 177 83 Z');r(a,'belly','M185 161 C172 190 196 208 213 227 Q234 255 199 290 Q219 259 201 240 C185 224 170 211 170 187 Q169 171 178 157 Z');eye(a,'eye',198,110,9);ink(a,'M130 131 L155 126 M211 142 Q195 148 192 163 M193 191 l24 -6 M201 207 l23 -8 M215 225 l23 -7 M219 243 l23 -5 M214 260 l19 3 M204 277 l14 6 M241 192 l17 5 M245 207 l16 3 M244 222 l13 0');leaf(a,'kelp-left',87,344,1.7);leaf(a,'kelp-right',312,340,1.4,80);ink(a,'M46 355 Q160 341 353 355')
a=art('octopus')
# Eight individually accessible arms radiate from the mantle.
for i,d in enumerate([
'M161 218 C127 212 105 196 78 213 C49 232 36 208 52 197 C27 200 23 233 51 241 C82 250 111 224 153 239 Z',
'M153 235 C112 235 108 271 75 277 C45 280 44 251 61 249 C34 240 27 281 56 292 C91 308 132 264 163 255 Z',
'M164 249 C137 276 146 302 117 319 C98 330 80 311 88 300 C68 314 83 345 111 338 C153 327 163 294 185 270 Z',
'M187 254 C173 292 194 318 175 339 Q161 355 145 342 C149 365 176 370 192 349 C208 326 200 292 212 264 Z',
'M211 253 C230 281 221 318 244 338 C264 355 286 341 279 325 C291 351 264 369 241 351 C213 331 216 304 196 272 Z',
'M229 244 C262 258 268 296 299 301 C319 307 329 287 320 277 C345 291 331 325 301 321 C260 315 251 280 220 267 Z',
'M238 232 C273 219 294 253 323 249 Q347 246 338 227 C360 234 358 263 330 268 C290 275 264 248 234 253 Z',
'M232 214 C264 188 285 216 311 204 Q326 196 316 182 C339 192 328 221 303 223 C271 224 263 214 244 231 Z']):r(a,f'arm-{i+1}',d)
r(a,'mantle','M144 208 C117 164 132 100 181 88 C226 75 268 113 260 163 Q256 190 239 214 C227 241 161 244 144 208 Z');eye(a,'eye-left',170,189,11);eye(a,'eye-right',223,189,11);ink(a,'M182 214 Q197 225 211 212 M149 144 Q152 120 175 114 M57 230 l14 0 M62 286 l13 -2 M107 330 l11 -5 M179 348 l5 -9 M251 346 l10 2 M302 314 l11 -1 M330 260 l9 -5 M304 216 l9 -4')
for i,(x,y) in enumerate([(86,94),(297,131),(312,74)]):e(a,f'bubble-{i}',x,y,10+i*3)
a=art('crab')
for side in [-1,1]:
 group(a,f'translate(200 0) scale({side} 1)')
 for i,y in enumerate([226,246,265]):r(a,f'leg-{side}-{i}',f'M63 {y} L113 {y+4} L145 {y+43} L135 {y+48} L105 {y+18} L60 {y+12} Z')
 r(a,f'arm-{side}','M62 225 Q112 200 108 162 L123 161 Q133 206 78 246 Z');r(a,f'claw-{side}','M100 174 C70 158 76 120 103 110 L99 140 L120 148 L137 128 L127 103 C158 110 167 145 144 167 Q129 181 100 174 Z');r(a,f'eye-stalk-{side}','M23 199 L28 169 L38 169 L36 202 Z');e(a,f'eye-{side}',33,162,11);a.pupil(33,161,4,5);end(a)
r(a,'shell','M112 245 C107 200 159 186 200 192 C249 184 296 209 289 245 C282 285 120 290 112 245 Z');ink(a,'M135 231 Q151 211 176 214 M224 215 Q250 212 267 231 M185 258 Q200 268 215 257 M151 265 Q170 270 180 268');ground(a)
# Dinosaurs: anatomical distinctions in neck, pelvis, frill, plates and forelimbs.
for name in ['dino','brontosaurus','stegosaurus','triceratops','trex','dragon','griffin']:
 a=art(name)
 r(a,'tail','M265 224 C301 217 329 198 360 177 Q350 223 299 249 L265 251 Z')
 for i,x in enumerate([156,246]):r(a,f'far-leg-{i}',f'M{x} 248 L{x+19} 246 L{x+18} 316 L{x-6} 316 Z')
 if name in ['dragon','griffin']:
  r(a,'far-wing','M186 207 Q208 118 289 100 L270 157 L304 167 L256 188 L240 218 Z')
  ink(a,'M195 207 L269 123 L241 180 M249 160 L282 168')
 r(a,'body','M122 216 C140 184 217 176 260 200 C295 219 293 257 261 277 Q206 298 143 272 C119 257 108 239 122 216 Z')
 if name=='brontosaurus':
  r(a,'neck-head','M144 252 C109 218 105 174 101 129 C71 139 57 116 72 100 C88 84 120 90 130 111 C138 134 126 185 169 216 Z');eye(a,'eye',94,108,6);ink(a,'M74 122 l17 0 M111 135 Q113 185 142 214')
 elif name in ['trex','dino']:
  r(a,'neck-head','M139 239 Q115 203 116 165 C84 171 58 162 56 140 L57 111 Q89 84 132 106 C163 120 153 156 171 187 L194 208 Z');r(a,'jaw','M57 142 L114 143 L123 157 Q87 179 63 159 Z');eye(a,'eye',116,121,8);ink(a,'M66 120 h9 M73 144 l5 8 l7 -8 M92 144 l5 8 l7 -8');r(a,'arm','M159 205 Q134 197 125 217 L114 233 L127 239 L141 225 L162 228 Z')
 elif name=='triceratops':
  r(a,'frill','M160 185 L151 157 L133 165 L113 145 L98 161 L78 155 L68 180 L52 186 L62 210 L54 229 L77 243 L112 237 Z');r(a,'head','M137 200 Q107 175 83 198 L58 229 L41 234 L43 249 Q69 269 103 251 L143 228 Z');r(a,'horn-top','M92 204 L67 161 L110 198 Z');r(a,'horn-front','M60 232 L42 211 L75 228 Z');eye(a,'eye',101,218,7)
 else:
  r(a,'neck-head','M143 242 Q110 236 99 218 C74 225 48 215 50 197 Q56 177 82 185 L112 196 Q128 200 144 199 Z');eye(a,'eye',75,199,6);ink(a,'M53 210 L77 213')
 if name=='stegosaurus':
  for i,(x,y,s) in enumerate([(126,201,18),(154,185,26),(190,181,29),(228,188,27),(262,206,21),(299,217,15)]):r(a,f'plate-{i}',f'M{x-14} {y} L{x-12} {y-s} L{x} {y-s-12} L{x+16} {y-s+2} L{x+14} {y+5} Z')
 if name=='dragon':
  r(a,'near-wing','M178 219 C189 169 222 142 274 133 L249 176 L279 192 Q244 187 225 214 L209 237 Z');ink(a,'M186 222 L254 150 L225 201');r(a,'horn','M87 188 L92 164 L105 196 Z');r(a,'flame','M32 196 C19 183 29 170 39 160 Q34 180 47 181 L47 196 Z')
 if name=='griffin':
  r(a,'eagle-head','M115 211 Q104 177 75 178 Q54 178 51 195 L41 202 L60 211 L65 227 L77 220 L87 232 L96 220 L110 227 Z');eye(a,'eagle-eye',74,196,6);r(a,'beak','M53 198 Q30 193 31 214 L47 210 L56 216 Z');r(a,'feather-wing','M176 221 Q200 144 275 129 L253 167 L264 167 L241 187 L251 189 L224 209 L234 210 L208 232 Z');ink(a,'M188 219 L248 158 M206 204 L230 180')
 for i,x in enumerate([157,248]):
  r(a,f'near-leg-{i}',f'M{x} 255 Q{x+14} 249 {x+27} 261 L{x+16} 293 L{x+21} 329 L{x-11} 329 L{x-11} 319 L{x} 310 Z');ink(a,f'M{x-3} 321 v6 M{x+6} 321 v6')
 ink(a,'M182 262 Q209 273 234 260 M282 232 l11 -4');ground(a)
a=art('pterodactyl');r(a,'left-wing','M185 191 L68 109 L32 225 Q84 202 103 241 Q139 221 178 253 Z');r(a,'right-wing','M210 190 L330 108 L370 224 Q319 201 296 242 Q257 219 219 255 Z');r(a,'body','M188 156 C163 183 172 222 189 264 L181 299 L195 302 L203 274 L211 301 L225 298 L216 262 C236 219 234 184 214 157 Z');r(a,'head','M186 165 Q171 143 186 127 L203 106 L213 127 Q235 131 230 151 L282 163 L230 173 Q206 187 186 165 Z');eye(a,'eye',210,146,6);ink(a,'M185 192 L68 109 L103 241 M181 213 L46 214 M215 193 L330 108 L296 242 M221 213 L354 213 M231 163 L271 163');cloud(a,'cloud-left',58,302,.7);cloud(a,'cloud-right',277,290,.7)
# Transport: mechanically plausible profiles, hubs, glazing and panel seams.
for name in ['bus','truck','tractor','train']:
 a=art(name)
 if name=='bus':
  r(a,'body','M52 133 Q52 120 67 120 L317 120 Q339 120 344 143 L351 263 Q351 276 337 276 L62 276 Q48 276 48 262 Z');r(a,'belt','M49 208 L347 208 L349 230 L49 230 Z')
  for i,x in enumerate([67,115,163,211]):r(a,f'window-{i}',f'M{x} 138 h37 v58 h-37 Z')
  r(a,'windscreen','M278 138 L319 138 Q328 138 330 152 L335 196 L278 196 Z');r(a,'door','M271 212 L335 212 L338 264 L271 264 Z');ink(a,'M301 213 v50 M284 220 v17 M325 220 v17 M71 245 h33 M178 245 h55');wheel(a,'front',298,278,25);wheel(a,'rear',105,278,25);r(a,'headlight','M337 238 h12 v17 h-12 Z')
 elif name=='truck':
  r(a,'cargo','M43 128 L226 128 L226 258 L43 258 Z');r(a,'cab','M239 161 L301 161 L328 207 L349 215 L349 272 L237 272 Z');r(a,'window','M251 174 L291 174 L312 207 L251 207 Z');r(a,'door','M249 217 L319 217 L319 262 L249 262 Z');r(a,'chassis','M43 259 L350 259 L350 277 L43 277 Z');r(a,'headlight','M332 223 h16 v15 h-16 Z');wheel(a,'rear-a',84,278,26);wheel(a,'rear-b',146,278,26);wheel(a,'front',292,278,26);ink(a,'M61 142 v100 M86 142 v100 M111 142 v100 M136 142 v100 M161 142 v100 M186 142 v100 M211 142 v100 M258 228 h15 M257 188 l10 -10')
 elif name=='tractor':
  r(a,'cab','M106 123 L216 123 L219 244 L100 244 Z');r(a,'roof','M94 111 L222 111 L229 128 L90 128 Z');r(a,'window','M119 138 L201 138 L203 208 L116 208 Z');r(a,'engine','M214 205 L316 205 Q334 207 335 222 L335 273 L203 273 Z');r(a,'exhaust','M282 205 L282 146 L292 146 L296 157 L292 157 L292 205 Z');r(a,'fender','M67 239 Q102 198 154 216 L178 237 L168 245 Q126 222 77 250 Z');wheel(a,'rear',127,280,49);wheel(a,'front',300,288,33);ink(a,'M155 139 v65 M128 213 h24 M228 222 v30 M240 222 v30 M252 222 v30 M264 222 v30 M276 222 v30 M200 271 h24 v12 h-24')
 else:
  r(a,'cab','M63 134 L152 134 L152 259 L63 259 Z');r(a,'roof','M54 122 L162 122 L169 139 L48 139 Z');r(a,'cab-window','M77 150 L137 150 L137 196 L77 196 Z');r(a,'boiler','M151 191 Q214 178 282 191 L282 254 L151 254 Z');r(a,'chimney','M242 190 L240 144 L232 138 L232 126 L268 126 L268 138 L259 144 L260 190 Z');r(a,'front','M282 190 Q306 190 306 222 Q306 255 282 254 Z');r(a,'cowcatcher','M303 245 L343 283 L300 283 Z');r(a,'chassis','M52 250 L306 250 L306 271 L52 271 Z');wheel(a,'rear',94,275,27);wheel(a,'middle',165,275,27);wheel(a,'front-wheel',238,275,27);r(a,'connecting-rod','M93 271 L239 271 Q246 275 239 279 L93 279 Q86 275 93 271 Z');ink(a,'M179 190 v60 M221 190 v60 M78 216 h51 M315 260 v20 M325 270 v10');cloud(a,'steam-one',269,97,.65);cloud(a,'steam-two',319,64,.45)
 ink(a,'M38 318 L365 318 M58 334 L128 334 M157 334 L230 334 M260 334 L343 334')
a=art('plane');r(a,'far-wing','M195 183 L253 67 L279 67 L244 196 Z');r(a,'tail-fin','M93 211 L62 143 L85 143 L126 208 Z');r(a,'fuselage','M40 216 C97 211 169 201 246 185 C281 178 319 184 355 204 Q374 217 354 225 C277 245 140 247 40 231 Z');r(a,'near-wing','M218 212 L155 322 L182 325 L280 220 Z');r(a,'tailplane','M85 224 L43 265 L62 268 L121 230 Z');r(a,'cockpit','M305 190 Q330 194 343 202 L316 205 L300 201 Z');r(a,'engine','M238 254 Q257 246 269 257 L268 280 Q252 293 237 284 Z');e(a,'engine-intake',253,281,13,6)
for i,x in enumerate([147,174,201,228,255,282]):e(a,f'window-{i}',x,213-(x-147)*.07,6,7)
ink(a,'M203 291 L246 235 M254 98 L226 170 M73 159 L97 204 M54 224 L84 222');cloud(a,'cloud-left',41,85,.8);cloud(a,'cloud-right',282,302,.8)
a=art('boat');r(a,'hull','M47 254 L355 254 Q333 302 298 317 L101 317 Q68 301 47 254 Z');r(a,'hull-stripe','M58 271 L346 271 L336 285 L70 285 Z');r(a,'mast','M196 66 L205 66 L205 254 L196 254 Z');r(a,'sail-left','M187 83 L187 233 L62 233 Q133 156 187 83 Z');r(a,'sail-right','M215 98 Q294 163 333 232 L215 232 Z');r(a,'cabin','M133 224 L183 224 L183 253 L122 253 Z');ink(a,'M173 111 L173 220 L89 220 M230 125 Q284 174 309 218 L230 218 M151 235 h19 v10 h-19 Z M218 247 L337 246 M106 297 h184');e(a,'porthole',233,299,8);ink(a,'M35 335 Q74 322 111 335 T187 335 T263 335 T363 335 M75 354 Q113 344 147 354 M250 355 Q281 343 324 355');cloud(a,'cloud',57,81,.75)
a=art('carriage');r(a,'coach','M106 165 Q106 133 144 129 L238 129 Q274 133 274 165 L274 253 Q267 277 239 277 L142 277 Q108 273 106 253 Z');r(a,'roof','M92 139 Q111 112 151 112 L230 112 Q265 111 289 139 Z');r(a,'door','M155 152 L231 152 L231 264 L155 264 Z');r(a,'door-window','M166 163 L220 163 L220 214 L166 214 Z');r(a,'left-window','M118 160 L144 160 L144 216 L118 216 Z');r(a,'right-window','M244 160 L262 160 L262 216 L244 216 Z');r(a,'driver-seat','M279 218 L327 218 L327 232 L292 232 L292 265 L279 265 Z');r(a,'chassis','M86 269 L315 269 L315 281 L86 281 Z');wheel(a,'rear',117,291,39);wheel(a,'front',274,297,33);r(a,'crown-finial','M173 111 L165 88 L183 97 L192 78 L204 97 L220 88 L213 111 Z');ink(a,'M212 226 h9 M174 237 q19 -12 36 0 M178 249 q15 -8 27 0 M309 236 l32 23 M88 146 v41 M292 146 v41');ground(a)
# Landscapes and plants: foliage contours and layered ground, all closed regions.
for name in ['tree','forest','garden','autumn-park']:
 a=art(name);cloud(a,'cloud',64,63,.75);e(a,'sun',308,63,22)
 r(a,'far-meadow','M30 267 Q100 216 200 253 Q290 215 370 254 L370 365 L30 365 Z')
 if name=='tree':tree(a,'oak',205,326,1.38);leaf(a,'ground-leaf',88,338,.7,70);r(a,'acorn','M294 329 Q304 343 314 329 L313 318 L296 318 Z');r(a,'acorn-cap','M292 320 Q303 305 317 320 Z')
 elif name=='forest':
  tree(a,'far-left',93,280,.8);tree(a,'far-right',297,277,.85);r(a,'path','M185 259 L213 260 Q184 290 258 365 L134 365 Q194 299 185 259 Z');tree(a,'near-left',94,335,.93);tree(a,'near-right',300,338,.93);ink(a,'M185 282 l9 -4 M176 334 l12 -3 M224 346 l11 5')
 elif name=='autumn-park':
  tree(a,'left-tree',93,296,1.03);tree(a,'right-tree',312,293,1.02);r(a,'path','M30 320 Q168 279 370 315 L370 347 Q178 316 30 357 Z');r(a,'bench-back','M141 228 L258 228 L258 265 L141 265 Z');r(a,'bench-seat','M137 270 L266 270 L277 283 L126 283 Z')
  for i,x in enumerate([144,249]):r(a,f'bench-leg-{i}',f'M{x} 283 h10 v29 h-10 Z')
  ink(a,'M143 240 h113 M143 253 h113');leaf(a,'fallen-leaf-one',97,346,.5,60);leaf(a,'fallen-leaf-two',293,350,.5,-50)
 else:
  r(a,'garden-bed','M62 263 Q192 236 336 263 L336 316 Q192 336 62 316 Z');r(a,'bed-rim','M55 259 Q192 232 343 259 L343 272 Q192 249 55 272 Z')
  for i,(x,y,s) in enumerate([(105,198,.8),(188,178,1),(277,205,.75)]):
   r(a,f'stem-{i}',f'M{x-3} {y} h6 v85 h-6 Z');leaf(a,f'leaf-{i}',x,y+60,.65,70);flower(a,f'flower-{i}',x,y,s)
  r(a,'watering-can','M273 305 L326 305 L332 346 L271 346 Z');r(a,'spout','M274 324 L245 304 L238 310 L272 339 Z');r(a,'handle','M326 310 C354 302 355 343 331 339 L330 331 C343 334 343 315 327 319 Z')
 ink(a,'M42 348 l5 -8 l5 8 M331 358 l5 -8 l5 8 M161 351 l5 -8 l5 8')
a=art('mushroom');r(a,'stem','M170 194 Q181 252 158 318 Q199 345 240 318 Q216 253 230 194 Z');r(a,'gills','M76 196 Q200 153 326 196 Q217 249 76 196 Z');r(a,'cap','M65 196 C83 129 131 82 196 81 C265 79 315 124 338 196 Q198 226 65 196 Z')
for i,(x,y,rx,ry) in enumerate([(130,149,22,17),(197,116,25,15),(267,152,24,18),(208,183,23,13)]):e(a,f'cap-spot-{i}',x,y,rx,ry)
ink(a,'M110 212 l48 13 M136 216 l29 13 M248 223 l42 -12 M240 231 l24 -7 M190 243 Q200 277 186 307 M222 274 l4 29');leaf(a,'leaf-left',92,335,.9,25);leaf(a,'leaf-right',292,338,.9,100);ground(a)
a=art('rainbow')
for i in range(7):
 ro=166-i*17;ri=ro-17;r(a,f'band-{i}',f'M{200-ro} 270 A{ro} {ro} 0 0 1 {200+ro} 270 L{200+ri} 270 A{ri} {ri} 0 0 0 {200-ri} 270 Z')
cloud(a,'cloud-left',47,266,1);cloud(a,'cloud-right',286,265,1);r(a,'meadow','M30 331 Q101 303 200 327 Q293 307 370 331 L370 366 L30 366 Z');flower(a,'daisy-left',101,326,.4);flower(a,'daisy-right',309,333,.4);ink(a,'M101 330 v25 M309 337 v22')
a=art('butterfly');r(a,'upper-wing-left','M188 196 C131 97 40 55 37 133 C36 188 104 213 181 220 Z');r(a,'upper-wing-right','M212 196 C269 97 360 55 363 133 C364 188 296 213 219 220 Z');r(a,'lower-wing-left','M185 214 C108 194 58 234 80 289 C101 337 158 299 190 242 Z');r(a,'lower-wing-right','M215 214 C292 194 342 234 320 289 C299 337 242 299 210 242 Z')
for side in [-1,1]:
 group(a,f'translate(200 0) scale({side} 1)');r(a,f'upper-panel-{side}','M23 193 C59 137 119 101 139 121 Q151 165 23 208 Z');r(a,f'lower-panel-{side}','M24 233 Q99 215 107 262 Q95 302 24 244 Z');e(a,f'wing-eye-{side}',111,151,14,19);e(a,f'lower-spot-{side}',78,261,12,15);ink(a,'M34 191 L91 138 M40 202 L120 177 M36 239 L82 246');end(a)
r(a,'body','M191 184 Q201 169 209 184 L214 239 Q210 270 201 280 Q190 263 187 238 Z');e(a,'head',200,171,12);ink(a,'M194 163 Q180 144 174 147 M206 163 Q220 143 226 147 M191 209 h20 M190 224 h22 M192 239 h19');flower(a,'flower',200,346,.5)
# Food studies: organic contours and recognizable cut surfaces.
a=art('apple');r(a,'stem','M193 130 Q185 91 203 71 L218 76 Q203 98 207 132 Z');leaf(a,'leaf',207,116,1.4,95);r(a,'fruit','M199 142 C144 99 77 127 75 193 C69 256 111 329 156 331 Q180 326 200 329 Q227 340 251 326 C295 305 332 229 321 181 C307 122 247 108 199 142 Z');ink(a,'M167 146 Q198 162 229 143 M99 202 Q92 258 129 291 M174 312 Q197 302 222 314');r(a,'slice-flesh','M282 270 Q321 263 350 301 Q326 345 279 350 Q305 315 282 270 Z');r(a,'slice-peel','M279 350 Q326 345 350 301 L359 306 Q334 355 277 359 Z');r(a,'seed','M316 307 Q330 311 319 325 Q310 322 316 307 Z')
a=art('banana');r(a,'back-fruit','M92 125 C115 255 218 288 307 187 L329 187 C285 314 138 322 77 181 Z');r(a,'middle-fruit','M77 155 C97 276 225 322 328 214 L342 220 C275 357 104 335 58 197 Z');r(a,'front-fruit','M64 177 C97 286 225 322 320 258 L332 272 C238 378 85 329 49 217 Z');r(a,'stem','M49 217 L46 177 L67 129 L83 121 L98 133 L79 176 L64 218 Z');r(a,'stem-tip','M67 129 L71 108 L91 109 L98 133 Z');ink(a,'M72 205 Q128 309 242 300 M93 175 Q154 278 258 246 M94 141 Q133 231 221 224 M309 192 l16 5 M326 222 l12 6 M319 263 l10 9')
a=art('strawberry');r(a,'fruit','M85 148 C91 100 158 98 199 124 C251 91 315 107 321 153 C333 221 255 308 201 341 C148 312 70 224 85 148 Z');r(a,'calyx','M200 136 L140 104 L153 136 L111 145 L159 161 L166 184 L199 155 L231 181 L239 157 L286 142 L243 131 L258 105 Z');r(a,'stem','M194 132 Q185 93 207 70 L219 76 Q202 102 208 133 Z')
for i,(x,y) in enumerate([(111,177),(150,200),(196,188),(241,202),(287,174),(126,235),(178,242),(223,248),(269,235),(159,284),(202,293),(240,284)]):
 r(a,f'seed-{i}',f'M{x} {y-6} Q{x-8} {y+3} {x} {y+9} Q{x+8} {y+3} {x} {y-6} Z')
a=art('pineapple');r(a,'fruit','M111 204 C110 158 155 140 202 147 C254 139 287 164 289 209 L283 284 C278 328 245 347 197 346 C147 347 114 324 112 283 Z');r(a,'crown-left','M174 161 Q126 123 115 80 Q160 97 191 151 Z');r(a,'crown-right','M209 156 Q247 95 285 85 Q278 126 231 164 Z');r(a,'crown-back','M180 151 Q164 80 180 43 Q202 75 209 149 Z');r(a,'crown-front','M183 164 Q196 96 233 57 Q244 103 215 165 Z')
for row in range(5):
 for col in range(3):
  x=145+col*48+(row%2)*12;y=187+row*30
  r(a,f'diamond-{row}-{col}',f'M{x} {y-12} L{x+17} {y} L{x} {y+12} L{x-17} {y} Z');ink(a,f'M{x-3} {y+2} l3 -5 l3 5')
ink(a,'M139 107 L181 151 M266 105 L223 154 M183 68 L195 142 M228 82 L204 149')
a=art('cupcake');r(a,'wrapper','M97 218 L303 218 L279 333 Q201 352 123 333 Z');r(a,'icing','M91 218 C63 196 88 172 110 174 C94 148 121 126 145 134 C135 105 169 89 191 104 C199 78 230 80 241 107 C274 101 291 127 278 148 C309 150 326 175 307 196 Q333 221 303 236 Q282 249 265 231 Q240 254 215 235 Q187 254 167 234 Q142 250 124 232 Q104 242 91 218 Z');e(a,'cherry',202,79,21);ink(a,'M204 61 Q202 40 223 33 M113 181 Q142 164 166 180 M175 142 Q211 122 246 142 M192 201 Q232 185 264 201 M130 246 L145 324 M158 248 L169 330 M188 249 L191 332 M218 249 L216 332 M246 248 L241 330 M274 246 L264 324');r(a,'icing-drop','M100 219 Q108 229 108 250 Q121 265 129 250 L127 230 Z')
a=art('pizza');r(a,'cheese','M61 121 Q196 70 339 121 L202 339 Z');r(a,'crust','M51 103 Q197 49 349 103 L339 126 Q198 80 61 126 Z')
for i,(x,y,s) in enumerate([(112,154,20),(211,130,21),(277,160,18),(175,214,19),(217,266,16)]):e(a,f'tomato-{i}',x,y,s);ink(a,f'M{x-8} {y-4} q8 -9 16 0 M{x-7} {y+6} q7 7 14 0')
for i,(x,y) in enumerate([(164,150),(247,204),(179,278)]):
 r(a,f'mushroom-{i}',f'M{x-17} {y} Q{x-17} {y-25} {x} {y-25} Q{x+17} {y-25} {x+17} {y} L{x+5} {y} L{x+5} {y+14} L{x-5} {y+14} L{x-5} {y} Z')
ink(a,'M80 109 Q194 71 322 109 M125 191 l9 7 M222 177 l9 -8 M203 309 l5 9 M275 137 l8 -2')
# Architectural studies: roofs, structural walls and generous window/door regions.
for name in ['cottage','barn','castle','tower']:
 a=art(name)
 if name in ['cottage','barn']:
  r(a,'side-wall','M247 171 L337 192 L337 321 L247 321 Z');r(a,'front-wall','M70 177 L161 100 L262 177 L262 321 L70 321 Z');r(a,'side-roof','M161 83 L257 103 L356 186 L263 194 Z');r(a,'front-roof','M51 179 L161 83 L281 181 L269 194 L161 107 L63 194 Z')
  if name=='cottage':
   r(a,'chimney','M267 113 L267 65 L292 65 L292 135 Z');r(a,'door','M135 321 L135 248 Q135 219 161 219 Q188 219 188 248 L188 321 Z');r(a,'window-left','M87 213 h34 v42 h-34 Z');r(a,'window-right','M207 213 h34 v42 h-34 Z');r(a,'attic-window','M143 167 Q143 148 161 148 Q180 148 180 167 L180 188 L143 188 Z');ink(a,'M104 214 v40 M88 234 h31 M224 214 v40 M208 234 h31 M161 149 v38 M145 169 h33 M176 273 v9 M281 76 h9 M284 98 h7')
  else:
   r(a,'door-left','M107 224 L164 224 L164 321 L107 321 Z');r(a,'door-right','M164 224 L221 224 L221 321 L164 321 Z');r(a,'loft','M143 158 L182 158 L182 195 L143 195 Z');ink(a,'M111 229 L160 316 M160 229 L111 316 M168 229 L217 316 M217 229 L168 316 M82 198 v110 M96 197 v113 M235 199 v112 M249 201 v110 M146 176 h32')
  r(a,'side-window','M280 219 L316 227 L316 267 L280 260 Z');ink(a,'M298 224 v40 M281 240 l34 7 M187 116 L276 136 M214 139 L301 159 M237 162 L328 181');r(a,'path','M134 322 L187 322 L225 365 L104 365 Z');ground(a)
 else:
  if name=='castle':
   r(a,'central-wall','M103 206 L294 206 L294 333 L103 333 Z');r(a,'keep','M145 153 L247 153 L247 333 L145 333 Z');r(a,'keep-roof','M132 154 L196 75 L260 154 Z');towers=[(72,164,60),(297,164,60)]
  else:towers=[(139,124,121)]
  for i,(x,y,w) in enumerate(towers):
   r(a,f'tower-{i}',f'M{x} {y} h{w} v{333-y} h{-w} Z');r(a,f'roof-{i}',f'M{x-12} {y} L{x+w/2} {y-75} L{x+w+12} {y} Z');r(a,f'window-{i}',f'M{x+w*.3} {y+61} v-22 a{w*.2} {w*.2} 0 0 1 {w*.4} 0 v22 Z');ink(a,f'M{x+8} {y+85} h18 M{x+w-26} {y+104} h18 M{x+9} {y+133} h20 M{x+w-28} {y+157} h18')
  r(a,'gate','M170 333 L170 284 Q170 254 199 254 Q228 254 228 284 L228 333 Z');ink(a,'M183 279 v53 M199 267 v65 M215 279 v53 M171 308 h56');r(a,'flag','M201 73 L201 40 L253 48 L235 58 L253 69 L201 63 Z');ink(a,'M201 40 v35');r(a,'approach','M170 333 L228 333 L258 366 L143 366 Z');ground(a)
# Space: identifiable hardware and astronomical forms without faces on planets.
a=art('rocket');r(a,'left-fin','M157 226 Q117 241 104 307 L152 286 L173 261 Z');r(a,'right-fin','M243 226 Q283 241 296 307 L248 286 L227 261 Z');r(a,'body','M153 263 C141 162 163 92 200 54 C239 92 260 163 247 263 Z');r(a,'nose','M166 109 Q180 74 200 54 Q224 80 235 109 Z');r(a,'engine','M165 263 L235 263 L228 284 L173 284 Z');e(a,'window-rim',200,165,30);e(a,'window',200,165,21);r(a,'flame','M176 285 Q170 311 184 338 L194 322 L202 362 L217 325 L226 341 Q238 314 224 285 Z');ink(a,'M158 236 h87 M172 248 h18 M210 248 h18 M185 148 l13 -3 M190 155 l14 -4');e(a,'planet',66,101,23);e(a,'moon',327,182,16)
a=art('moon');e(a,'moon',202,207,137)
for i,(x,y,rx,ry) in enumerate([(134,141,27,21),(244,115,22,15),(280,227,31,23),(154,260,35,27),(214,310,17,10),(107,214,13,18),(223,198,16,13)]):
 e(a,f'crater-{i}',x,y,rx,ry);ink(a,f'M{x-rx*.65} {y} Q{x} {y-ry*.9} {x+rx*.65} {y}')
ink(a,'M91 170 Q87 149 108 128 M273 284 Q298 269 311 246 M190 85 Q211 79 228 85');cloud(a,'passing-cloud',42,328,.85)
a=art('saturn');e(a,'planet',201,201,94);ink(a,'M126 147 Q195 169 273 145 M112 178 Q198 198 290 174 M121 228 Q199 247 284 222 M143 267 Q198 278 255 258');r(a,'outer-ring','M111 179 C6 183 17 257 175 268 C325 279 398 217 291 192 L292 207 C355 226 307 250 190 245 C78 243 42 216 111 197 Z');r(a,'inner-ring','M111 188 C44 194 52 229 178 254 C300 265 359 226 292 199 L292 207 C335 226 290 246 186 241 C95 233 77 211 111 203 Z');e(a,'moon-left',64,90,18);e(a,'moon-right',332,311,25);ink(a,'M321 301 q9 -8 17 0 M55 85 q7 -7 14 0')
a=art('lander');r(a,'left-leg','M149 249 L105 316 L89 316 L133 241 Z');r(a,'right-leg','M251 249 L295 316 L311 316 L267 241 Z');r(a,'left-foot','M77 315 L117 315 L123 328 L71 328 Z');r(a,'right-foot','M283 315 L323 315 L329 328 L277 328 Z');r(a,'body','M140 133 L259 133 L285 215 L269 258 L131 258 L115 215 Z');r(a,'cabin','M158 150 L241 150 L257 202 L143 202 Z');r(a,'hatch','M170 216 L230 216 L230 258 L170 258 Z');r(a,'engine','M179 258 L222 258 L229 281 L172 281 Z');r(a,'left-panel','M31 164 L109 179 L109 229 L31 214 Z');r(a,'right-panel','M291 179 L369 164 L369 214 L291 229 Z');r(a,'antenna','M195 133 L195 82 L203 82 L203 133 Z');r(a,'dish','M163 66 Q199 55 235 66 Q220 104 199 104 Q178 104 163 66 Z');ink(a,'M44 167 v50 M65 171 v50 M87 175 v50 M32 188 l76 15 M307 176 v50 M328 172 v50 M350 167 v50 M293 203 l75 -15 M200 151 v50 M179 226 h12 M211 226 h12 M181 273 h40 M196 59 v-15');r(a,'moon-surface','M28 342 Q200 308 372 342 L372 370 L28 370 Z');e(a,'crater-left',125,349,25,7);e(a,'crater-right',284,354,32,8)
# Characters: expressive faces, hands, articulated clothing and accessories.
for name in ['astronaut','alien','robot','wizard','fairy','knight','teddy']:
 a=art(name)
 if name=='fairy':
  for side in [-1,1]:
   group(a,f'translate(200 0) scale({side} 1)');r(a,f'upper-wing-{side}','M20 188 C54 122 119 116 122 157 Q121 203 35 213 Z');r(a,f'lower-wing-{side}','M27 213 C103 196 122 245 89 265 Q54 276 22 236 Z');ink(a,'M36 195 Q73 146 103 155 M42 224 Q78 220 91 246');end(a)
 if name=='astronaut':r(a,'backpack','M119 164 Q112 156 112 176 L112 259 L282 259 L282 167 Q282 158 273 164 Z')
 if name=='teddy':
  e(a,'ear-left',137,104,27);e(a,'ear-right',262,104,27);e(a,'inner-ear-left',137,104,16);e(a,'inner-ear-right',262,104,16)
 # Separate bent arms. Hands remain easy to tap.
 r(a,'arm-left','M146 187 C124 185 113 209 101 244 L121 255 L156 219 Z');r(a,'arm-right','M253 189 C278 185 286 212 298 238 L280 253 L247 221 Z');e(a,'hand-left',108,259,15,18);e(a,'hand-right',292,254,15,18)
 for i,x in enumerate([161,216]):
  r(a,f'leg-{i}',f'M{x} 271 L{x+26} 271 L{x+24} 321 L{x-4} 321 Z');r(a,f'foot-{i}',f'M{x-5} 315 Q{x+10} 309 {x+24} 319 L{x+30} 339 Q{x+5} 351 {x-15} 339 Z')
 r(a,'torso','M151 182 Q198 163 249 184 L265 277 Q199 302 138 277 Z')
 if name in ['wizard','fairy']:
  r(a,'skirt','M155 222 L244 222 L278 308 Q201 326 125 308 Z');ink(a,'M170 246 L151 301 M199 245 v64 M227 245 L250 300')
 if name=='robot':
  r(a,'head','M137 81 Q137 74 146 74 L254 74 Q263 74 263 84 L263 161 Q263 170 254 170 L146 170 Q137 170 137 161 Z');e(a,'eye-left',169,117,14);e(a,'eye-right',231,117,14);r(a,'mouth','M171 145 L229 145 L229 156 L171 156 Z');r(a,'panel','M161 205 L239 205 L239 255 L161 255 Z');e(a,'dial',181,229,11);e(a,'button',218,228,7);r(a,'antenna','M195 74 L195 51 L205 51 L205 74 Z');e(a,'antenna-ball',200,42,10);ink(a,'M182 147 v7 M194 147 v7 M206 147 v7 M218 147 v7 M170 272 h60 M149 321 h36 M204 321 h36')
 elif name=='astronaut':
  e(a,'helmet',200,119,62,61);r(a,'visor','M157 90 Q200 72 242 90 Q258 120 242 149 Q200 169 157 149 Q142 120 157 90 Z');r(a,'chest-console','M164 199 L236 199 L236 242 L164 242 Z');e(a,'console-dial',183,218,9);r(a,'flag-patch','M219 183 h25 v15 h-25 Z');ink(a,'M211 210 h15 M211 221 h15 M159 105 Q175 91 190 94 M157 118 l24 -17 M151 256 Q171 267 174 244 M169 285 h15 M218 285 h15 M98 252 l22 7 M280 247 l21 -7 M158 329 h26 M214 329 h27')
 elif name=='knight':
  r(a,'helmet','M147 150 L147 104 Q150 65 200 65 Q250 65 253 104 L253 150 L223 178 L177 178 Z');r(a,'visor','M147 112 L253 112 L253 145 L147 145 Z');ink(a,'M164 120 v16 M181 120 v16 M198 120 v16 M215 120 v16 M232 120 v16 M200 69 v41');r(a,'breastplate','M155 190 L244 190 L253 264 Q199 290 147 264 Z');r(a,'shield','M81 220 L134 201 L186 220 L177 285 Q157 317 134 330 Q100 306 89 283 Z');r(a,'shield-emblem','M128 224 h13 v26 h24 v13 h-24 v37 h-13 v-37 h-24 v-13 h24 Z');r(a,'sword','M288 228 L288 135 L297 112 L306 135 L306 228 Z');r(a,'guard','M274 229 L320 229 L320 241 L274 241 Z');ink(a,'M297 130 v94')
 else:
  if name=='alien':r(a,'head','M141 91 C154 51 246 51 261 91 C283 141 243 178 201 186 C157 177 119 139 141 91 Z')
  else:r(a,'head','M146 119 C142 67 253 65 256 119 C266 154 237 187 200 187 C160 188 137 154 146 119 Z')
  if name=='alien':
   r(a,'eye-left','M150 111 Q178 103 187 135 Q163 147 150 111 Z');r(a,'eye-right','M213 135 Q222 103 250 111 Q237 147 213 135 Z');ink(a,'M187 161 Q200 169 214 160');e(a,'belt',201,262,52,10);r(a,'badge','M188 211 L200 200 L213 211 L207 228 L194 228 Z')
  else:
   eye(a,'eye-left',177,129,7);eye(a,'eye-right',224,129,7);ink(a,'M184 158 Q200 170 216 157 M198 140 l-4 9 h7')
   if name=='wizard':
    r(a,'beard','M156 149 Q167 163 182 159 Q200 175 220 158 Q236 161 246 149 C250 196 225 215 200 237 C176 214 152 195 156 149 Z');r(a,'hat','M133 104 L178 37 Q195 35 211 58 L247 104 Z');r(a,'brim','M114 105 Q199 87 280 105 L276 116 Q199 103 117 116 Z');ink(a,'M178 182 L188 207 M213 185 L207 218');r(a,'staff','M306 328 L306 155 L315 155 L315 328 Z');e(a,'staff-orb',310,140,18)
   elif name=='fairy':
    r(a,'hair','M143 132 C123 90 157 60 195 67 C237 50 275 87 260 135 L246 144 L242 111 Q212 115 191 89 Q175 111 153 115 L153 145 Z');r(a,'bodice','M157 185 Q199 207 243 185 L236 228 L166 228 Z');r(a,'wand','M297 252 L323 191 L329 194 L303 255 Z');r(a,'wand-star','M329 156 L334 171 L350 171 L338 181 L343 197 L329 187 L316 197 L320 181 L308 171 L324 171 Z');flower(a,'hair-flower',247,86,.38)
   else:
    e(a,'muzzle',200,153,25,18);r(a,'nose','M187 145 Q200 139 213 145 Q211 156 200 158 Q189 155 187 145 Z');e(a,'belly',201,244,37,35);r(a,'bow-left','M197 193 L169 178 L168 207 Z');r(a,'bow-right','M203 193 L232 178 L232 207 Z');e(a,'bow-knot',200,194,8);ink(a,'M200 159 v8 M189 268 l4 -3 l4 3 l4 -3 l4 3 M163 328 l5 -3 l5 3 M219 328 l5 -3 l5 3')
 ground(a)
# Seasonal still lifes.
a=art('pumpkin');r(a,'stem','M186 145 Q190 103 216 83 L236 93 Q211 115 210 147 Z');e(a,'left-lobe',139,231,56,90);e(a,'right-lobe',258,231,57,90);e(a,'middle-left',175,235,53,99);e(a,'middle-right',225,235,53,99);e(a,'center',201,236,33,103);leaf(a,'leaf',210,139,1.3,110);ink(a,'M264 140 C298 113 329 141 307 158 C284 169 281 143 294 139 M185 105 l14 8 M191 121 l15 7');ground(a)
a=art('sunflower');r(a,'stem','M194 195 L207 195 L214 349 L198 349 Z');leaf(a,'leaf-left',200,297,1.65,0);leaf(a,'leaf-right',209,325,1.6,100)
for i in range(12):
 group(a,f'translate(200 156) rotate({i*30})');r(a,f'petal-{i}','M-15 -45 C-34 -67 -21 -100 0 -112 C21 -100 34 -67 15 -45 Z');ink(a,'M0 -53 L0 -90');end(a)
e(a,'flower-center',200,156,51)
for y in range(125,192,14):
 for x in range(169,237,14):
  if (x-200)**2+(y-156)**2<1700:ink(a,f'M{x-2} {y} l2 -3 l2 3')
ground(a)
a=art('umbrella');r(a,'handle','M193 164 L205 164 L205 312 C205 349 153 350 153 315 L165 315 C165 334 193 334 193 312 Z');r(a,'canopy','M38 216 C59 61 337 61 362 216 Q332 194 307 216 Q278 192 251 215 Q226 191 201 215 Q174 192 148 215 Q119 194 93 216 Q65 195 38 216 Z');r(a,'panel-left','M201 98 Q111 117 93 216 Q120 194 148 215 Q156 133 201 98 Z');r(a,'panel-right','M201 98 Q287 117 307 216 Q278 192 251 215 Q246 133 201 98 Z');r(a,'tip','M194 99 L194 83 Q200 73 206 83 L206 99 Z')
for i,(x,y) in enumerate([(70,268),(302,285),(116,72),(300,59)]):r(a,f'drop-{i}',f'M{x} {y-17} Q{x-18} {y+5} {x} {y+12} Q{x+18} {y+5} {x} {y-17} Z')
a=art('snowman');r(a,'arm-left','M136 224 L78 185 L59 190 L56 182 L74 177 L69 156 L78 153 L87 181 L143 213 Z');r(a,'arm-right','M264 223 L316 184 L320 155 L329 155 L326 180 L347 171 L351 178 L322 192 L270 234 Z');e(a,'body',201,277,86,74);e(a,'head',201,172,58,54);r(a,'hat','M155 127 L149 66 L250 66 L244 127 Z');r(a,'hat-band','M153 103 L247 103 L245 122 L155 122 Z');r(a,'brim','M126 123 Q200 111 276 123 L275 139 Q201 128 127 139 Z');r(a,'scarf','M150 205 Q200 228 251 205 L260 224 Q207 249 142 224 Z');r(a,'scarf-tail','M225 233 L248 231 L260 282 L235 286 Z');r(a,'nose','M198 168 L259 182 L201 190 Z');eye(a,'eye-left',180,162,5);eye(a,'eye-right',222,162,5)
for i,y in enumerate([255,280,305]):e(a,f'button-{i}',197,y,7)
ink(a,'M178 197 Q193 207 213 198 M239 274 l2 9 M247 272 l3 10');ground(a)
a=art('christmas-tree');r(a,'trunk','M185 299 L216 299 L216 343 L185 343 Z');r(a,'tree','M201 62 Q179 107 149 138 L171 134 L118 194 L144 188 L88 253 L121 247 L65 316 Q200 351 337 316 L281 247 L313 253 L258 188 L282 194 L230 134 L253 138 Z');r(a,'star','M200 32 L209 51 L230 53 L214 67 L219 88 L200 77 L181 88 L185 67 L170 53 L191 51 Z');ink(a,'M152 141 Q193 165 246 145 M122 197 Q186 230 275 200 M95 258 Q188 292 309 257')
for i,(x,y) in enumerate([(187,124),(213,190),(154,223),(251,244),(136,294),(213,306)]):e(a,f'bauble-{i}',x,y,12);ink(a,f'M{x} {y-12} v-7')
r(a,'present-left','M38 319 L105 319 L105 366 L38 366 Z');r(a,'ribbon-left','M64 319 h13 v47 h-13 Z');r(a,'present-right','M284 323 L363 323 L363 366 L284 366 Z');r(a,'ribbon-right','M316 323 h13 v43 h-13 Z');ink(a,'M38 335 h67 M284 338 h79')
# Toys with construction and volume rather than generic icons.
a=art('ball');e(a,'ball',201,203,127);r(a,'center-panel','M174 161 L224 161 L247 205 L200 237 L155 205 Z');r(a,'top-panel','M160 83 L147 119 L173 142 L224 142 L251 117 L238 82 Q200 71 160 83 Z');r(a,'left-panel','M83 158 L118 163 L137 205 L110 243 L77 239 Q69 199 83 158 Z');r(a,'right-panel','M319 158 L284 163 L265 205 L292 243 L325 239 Q333 199 319 158 Z');r(a,'bottom-panel','M172 324 L153 290 L174 256 L226 256 L249 291 L230 326 Q199 335 172 324 Z');ink(a,'M147 119 L118 163 M251 117 L284 163 M110 243 L153 290 M292 243 L249 291 M174 161 L173 142 M224 161 L224 142 M155 205 L137 205 M247 205 L265 205 M200 237 L200 256')
a=art('kite');r(a,'kite','M197 49 L304 154 L200 291 L88 158 Z');r(a,'panel-left','M197 49 L200 158 L88 158 Z');r(a,'panel-right','M200 158 L304 154 L200 291 Z');ink(a,'M200 291 C273 301 172 344 253 368 M197 49 L200 291 M88 158 L304 154');r(a,'bow-one','M221 310 L209 298 L201 320 L221 317 L238 327 L244 306 Z');r(a,'bow-two','M216 343 L200 332 L195 353 L216 350 L234 359 L239 339 Z');cloud(a,'cloud-left',36,73,.65);cloud(a,'cloud-right',290,259,.7)
a=art('drum');r(a,'body','M79 163 L321 163 L321 286 Q200 329 79 286 Z');e(a,'bottom-rim',200,286,122,31);r(a,'side','M80 172 Q200 215 320 172 L320 276 Q200 319 80 276 Z');e(a,'top-rim',200,163,126,38);e(a,'skin',200,161,112,28)
for i,x in enumerate([93,135,177,219,261]):r(a,f'cord-{i}',f'M{x} 195 L{x+21} 275 L{x+42} 195 L{x+37} 194 L{x+21} 256 L{x+5} 194 Z')
r(a,'stick-left','M111 69 Q101 61 95 70 Q89 80 102 86 L239 144 L243 137 Z');r(a,'stick-right','M289 65 Q300 59 306 70 Q311 81 298 85 L163 143 L159 136 Z');ink(a,'M112 152 Q193 129 285 152 M100 279 Q200 311 300 279')
a=art('blocks')
for i,(x,y,s) in enumerate([(45,240,78),(150,253,78),(253,235,78),(146,132,78)]):
 r(a,f'front-{i}',f'M{x} {y} h{s} v{s} h{-s} Z');r(a,f'top-{i}',f'M{x} {y} l24 -22 h{s} l-24 22 Z');r(a,f'side-{i}',f'M{x+s} {y} l24 -22 v{s} l-24 22 Z')
 if i==0:r(a,'circle-inset',f'M{x+18} {y+39} a21 21 0 1 0 42 0 a21 21 0 1 0 -42 0 Z')
 elif i==1:r(a,'triangle-inset',f'M{x+39} {y+16} L{x+61} {y+60} L{x+17} {y+60} Z')
 elif i==2:r(a,'square-inset',f'M{x+19} {y+19} h40 v40 h-40 Z')
 else:r(a,'diamond-inset',f'M{x+39} {y+12} L{x+64} {y+39} L{x+39} {y+66} L{x+14} {y+39} Z')

a=art('crown');r(a,'crown','M75 144 L127 181 L159 112 L200 171 L245 112 L275 181 L329 144 L300 286 Q200 321 101 286 Z');r(a,'band','M101 264 Q200 294 300 264 L300 296 Q200 330 101 296 Z');r(a,'center-gem','M200 199 L221 224 L200 249 L179 224 Z');e(a,'left-gem',133,228,12,16);e(a,'right-gem',269,228,12,16)
for i,(x,y) in enumerate([(75,134),(159,102),(245,102),(329,134)]):e(a,f'finial-{i}',x,y,10)
ink(a,'M115 288 Q200 313 285 288 M92 162 L115 251 M310 163 L287 251 M167 131 L182 158 M238 132 L221 158')

# Corrections found in the rendered contact-sheet and hit-target review.
def remove(a,*names):
 a.parts=[p for p in a.parts if not any(f'data-region="{n}"' in p for n in names)]
 a.regions.difference_update(names)
def replace(a,name,d):
 for i,p in enumerate(a.parts):
  if f'data-region="{name}"' in p:a.parts[i]=f'<path data-region="{name}" d="{d}"/>';return
 raise KeyError(name)
remove(ART['drum'],'body')
for name in ['wizard','fairy']:
 a=ART[name]
 for i,x in enumerate([161,216]):replace(a,f'leg-{i}',f'M{x} 271 L{x+26} 271 L{x+24} 333 L{x-4} 333 Z')
remove(ART['griffin'],'eye')
remove(ART['knight'],'hand-left')
remove(ART['train'],'rear-axle','middle-axle','front-wheel-axle')
a=ART['cupcake'];e(a,'wrapper-medallion',202,287,21,22);r(a,'medallion-heart','M201 283 C190 270 180 286 201 300 C222 286 212 270 201 283 Z')
# Sheep have a tapered muzzle, unlike a cow or pig's broad nose.
a=ART['sheep'];remove(a,'muzzle','nostril-left','nostril-right');r(a,'muzzle','M97 207 Q113 195 129 207 Q131 224 113 231 Q95 223 97 207 Z');ink(a,'M106 211 l7 5 l7 -5 M113 216 v8')
# Short, rounded piglet proportions, with soft ears and small cloven hooves.
a=ART['pig'];a.parts.insert(0,'<g transform="translate(0 73) scale(1 .78)">');a.parts.append('</g>')
replace(a,'head','M79 166 C84 136 130 135 148 160 C163 181 153 215 137 230 Q113 250 89 229 C73 211 69 187 79 166 Z')
# The young dinosaur has a soft rounded snout and spots; T. rex is a biped
# with a massive skull, strong haunches and the characteristic small forearm.
a=ART['dino'];remove(a,'far-leg-0','near-leg-0');replace(a,'neck-head','M139 239 Q115 203 116 165 C84 171 58 162 56 140 L57 111 C62 81 125 84 139 115 C151 136 153 166 171 187 L194 208 Z');e(a,'back-spot-one',215,209,12,8);e(a,'back-spot-two',246,221,10,7)
a=art('trex');r(a,'tail','M246 220 Q303 222 368 183 Q352 241 269 265 L236 259 Z');r(a,'far-leg','M211 253 Q242 240 251 266 L230 295 L248 323 L204 323 L204 311 L213 290 L197 274 Z');r(a,'body','M126 157 C151 141 176 177 195 187 C235 181 271 210 265 243 C263 271 231 282 198 271 L148 228 Z');r(a,'neck-head','M145 208 C124 183 120 163 115 148 L71 149 Q41 147 41 122 L42 94 Q76 72 119 83 C154 86 164 114 158 145 L174 178 Z');r(a,'jaw','M42 125 L116 126 L124 145 Q79 168 48 145 Z');eye(a,'eye',122,106,8);r(a,'arm','M162 188 Q140 189 136 207 L124 216 L133 225 L149 215 L156 205 L173 207 Z');r(a,'near-leg','M226 226 C251 230 254 255 238 269 L214 292 L226 320 L239 327 L238 338 L183 338 L182 326 L193 291 L193 254 Q200 231 226 226 Z');ink(a,'M51 109 h9 M59 128 l5 8 l6 -8 M78 128 l6 9 l6 -9 M100 128 l6 7 l5 -7 M199 329 v8 M213 329 v8 M228 329 v8 M211 244 Q229 238 238 250 M278 246 Q319 231 340 215');ground(a)
# Decorative gill/leaf lines are intentionally open and non-interactive.

for name in ['fairy','wizard']:remove(ART[name],'leg-0','leg-1')
remove(ART['forest'],'far-left-trunk','far-right-trunk')
replace(ART['pig'],'tail','M299 221 Q324 227 337 209 L330 204 Q320 218 300 213 Z')
# The fine curl is a non-colorable contour, not an open fill region.
ART['pig'].parts.insert(-1,'<path d="M334 207 C350 196 340 179 329 186 C317 194 326 207 334 198" fill="none" stroke-width="2.2" pointer-events="none"/>')

if __name__=='__main__':
 legacy={p.stem for p in OUT.parent.parent.glob('*.svg')}
 expected=legacy-{'cat','car','mountain'}
 assert set(ART)==expected, f'missing={expected-set(ART)}, extra={set(ART)-expected}'
 selected=sys.argv[1:]
 if not selected:raise SystemExit('Specify subject IDs, or --all for the 69 unfinished subjects. Reviewed masters are never generated here.')
 names=sorted(ART) if selected==['--all'] else selected
 for name in names:
  a=ART[name];(OUT/f'{name}.svg').write_text(a.svg());print(f'{name}: {len(a.regions)} regions')
