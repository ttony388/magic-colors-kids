"""Original vector masters for the three-picture art-direction review.

Never overwrites v1 artwork. Core region names are shared by all three levels.
Closed white shapes are colorable; open detail strokes never receive pointer events.
Run: python3 scripts/generate_art_v2.py
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public/illustrations/v2'
LEVELS = ('easy', 'medium', 'detailed')


class Drawing:
    def __init__(self, subject, level):
        self.subject, self.level, self.parts = subject, level, []
        self.regions = set()

    def region(self, name, d):
        assert name not in self.regions, (self.subject, name)
        assert d.strip().upper().endswith('Z'), (name, 'region must close')
        self.regions.add(name)
        self.parts.append(f'<path data-region="{name}" d="{d}"/>')

    def ellipse(self, name, x, y, rx, ry):
        self.region(name, f'M{x-rx} {y} a{rx} {ry} 0 1 0 {rx*2} 0 a{rx} {ry} 0 1 0 {-rx*2} 0 Z')

    def ink(self, d, width=1.6):
        self.parts.append(f'<path d="{d}" fill="none" stroke-width="{width}" pointer-events="none"/>')

    def pupil(self, x, y, rx=2, ry=5):
        self.parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#202024" stroke="none" pointer-events="none"/>')

    @property
    def medium(self):
        return self.level != 'easy'

    @property
    def detailed(self):
        return self.level == 'detailed'

    def svg(self):
        width = {'easy': 3.2, 'medium': 2.6, 'detailed': 2.2}[self.level]
        return '\n'.join([
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="art-title" data-art-version="2" data-complexity="{self.level}">',
            f'<title id="art-title">{escape(self.subject)} — {self.level} coloring illustration</title>',
            '<desc>Original closed-region vector line art. White areas can be colored individually.</desc>',
            f'<g fill="#ffffff" stroke="#202024" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">',
            *self.parts, '</g>', '</svg>', ''
        ])


def kitten(level):
    a = Drawing('Kitten in the garden', level)
    # A tapering tail curls behind the seated haunch; the front legs carry weight.
    a.region('tail', 'M260 307 C304 321 331 305 327 273 C325 250 308 234 315 215 C319 206 328 209 329 217 C325 234 344 249 347 274 C353 317 315 344 267 331 Z')
    a.region('body', 'M167 189 C158 214 151 249 149 276 C145 305 155 326 181 332 L272 332 C294 321 302 303 293 279 C282 251 259 238 246 207 L233 186 Z')
    a.region('haunch', 'M257 267 C280 266 295 284 293 303 C292 321 273 331 247 332 L225 332 C220 320 228 312 241 309 C229 293 236 273 257 267 Z')
    a.region('chest', 'M174 193 C182 209 203 220 226 195 C232 226 232 252 222 278 L182 279 C169 252 165 224 174 193 Z')
    a.region('paw-left', 'M172 223 C165 237 168 276 160 316 C155 326 160 335 176 335 L193 335 C204 335 209 328 204 320 C196 298 201 267 197 244 C193 224 182 216 172 223 Z')
    a.region('paw-right', 'M212 224 C203 243 207 290 202 318 C199 328 203 337 216 337 L235 337 C248 336 251 329 244 320 C236 298 239 269 234 246 C231 228 223 218 212 224 Z')
    a.parts.append('<g transform="translate(32 20) scale(.84)">')
    # Ears grow out of the cranium rather than triangles sitting on a circle.
    a.region('head', 'M136 117 C130 97 128 76 131 54 C149 61 161 76 172 86 C188 81 209 82 225 88 C238 74 250 65 265 60 C268 80 266 102 261 121 C267 138 267 155 259 169 C249 190 230 203 206 209 C183 210 160 200 145 183 C130 167 126 141 136 117 Z')
    a.region('ear-left', 'M140 74 C149 80 156 86 162 95 L145 111 C142 99 140 87 140 74 Z')
    a.region('ear-right', 'M253 79 C244 85 238 92 234 98 L254 115 C256 103 256 91 253 79 Z')
    a.region('muzzle', 'M173 170 C178 159 190 159 200 166 C208 158 220 158 228 166 C240 182 222 195 202 196 C182 197 164 185 173 170 Z')
    a.region('nose', 'M190 166 Q200 161 211 166 Q207 176 201 177 Q194 176 190 166 Z')
    if a.medium:
        a.region('eye-left', 'M149 143 Q160 128 176 141 Q166 154 149 143 Z')
        a.region('eye-right', 'M219 141 Q234 129 246 142 Q232 154 219 141 Z')
        a.pupil(164, 141, 2.5, 5.3)
        a.pupil(232, 141, 2.5, 5.3)
    else:
        a.ink('M150 142 Q162 130 175 142 M220 142 Q233 130 245 142', 2.6)
        a.pupil(163, 141, 3, 4)
        a.pupil(232, 141, 3, 4)
    a.ink('M201 177 L201 183 Q192 190 185 183 M201 183 Q209 190 217 182 M175 174 Q153 166 121 166 M176 182 Q150 181 124 189 M226 173 Q251 164 279 165 M226 181 Q254 180 278 188')
    if a.medium:
        a.region('forehead-mark', 'M184 94 Q193 101 198 113 Q203 101 211 95 L207 119 Q199 129 191 118 Z')
        a.region('cheek-left', 'M137 148 L152 154 L142 160 Z')
        a.region('cheek-right', 'M259 149 L244 154 L254 162 Z')
    if a.detailed:
        a.ink('M147 122 L153 119 M155 116 L160 114 M237 118 L244 121 M143 168 L151 172 M249 173 L255 169')
    a.parts.append('</g>')
    if a.medium:
        a.ink('M175 325 L175 333 M185 324 L186 333 M217 326 L217 335 M229 325 L230 334 M255 322 Q262 322 265 327 M269 319 Q277 319 280 323')
        a.ink('M179 201 L186 211 L193 205 L200 216 L208 205 L216 210 M241 244 Q249 249 253 258')
    if a.detailed:
        a.region('shoulder-stripe', 'M248 229 Q261 240 270 254 Q259 249 253 250 Z')
        a.region('haunch-stripe', 'M281 281 Q290 288 290 299 L275 295 Z')
        a.ink('M166 239 L170 244 M284 305 L279 309 M307 319 L311 322 M326 306 L331 309 M330 279 L336 278 M321 250 L328 246')
        a.region('leaf-left', 'M86 340 Q64 321 66 303 Q88 308 92 330 Z')
        a.region('leaf-right', 'M91 333 Q99 307 119 308 Q118 327 96 340 Z')
        a.ink('M86 350 Q93 332 79 317 M93 338 L108 318 M124 348 Q135 336 149 345 M279 348 Q289 339 302 347 M103 357 Q187 369 270 355')
    return a


def car(level):
    a = Drawing('Family hatchback', level)
    # True side profile: roof, pillars, wheelbase, overhang and arch clearance.
    a.region('car-body', 'M47 233 L64 213 C77 204 89 201 103 199 L134 151 C141 141 151 136 168 135 L234 135 C250 136 261 141 272 154 L309 196 L335 205 C347 209 355 221 355 238 L355 268 Q355 277 342 277 L329 277 C329 248 314 231 291 231 C268 231 253 248 253 277 L147 277 C147 249 132 231 109 231 C86 231 71 249 71 277 L51 277 Q41 277 41 267 L41 249 Q41 239 47 233 Z')
    a.region('window-left', 'M117 194 L143 157 Q149 150 164 150 L185 150 L185 194 Z')
    a.region('window-right', 'M199 150 L232 150 Q248 151 258 162 L285 194 L199 194 Z')
    a.ellipse('wheel-left', 109, 274, 29, 29)
    a.ellipse('wheel-right', 291, 274, 29, 29)
    a.ellipse('hub-left', 109, 274, 17, 17)
    a.ellipse('hub-right', 291, 274, 17, 17)
    a.region('headlight-left', 'M52 222 L77 215 L73 232 L45 239 Z')
    a.region('headlight-right', 'M333 214 Q345 217 350 229 L333 229 Z')
    if a.medium:
        a.region('front-door', 'M109 207 L185 207 L185 264 L158 264 Q155 232 130 224 L109 221 Z')
        a.region('rear-door', 'M198 207 L281 207 L278 222 Q251 232 243 264 L198 264 Z')
        a.region('mirror', 'M114 188 L127 188 Q137 190 135 197 Q131 203 115 201 Z')
        a.region('bumper-front', 'M42 252 L63 252 L63 266 L42 266 Z')
        a.region('bumper-rear', 'M336 252 L355 252 L355 266 L336 266 Z')
        a.ink('M163 215 L177 215 M253 215 L267 215 M94 209 L83 213 M307 204 L320 207 M161 273 L241 273')
        for x in (109, 291):
            a.ellipse(f'axle-{x}', x, 274, 5, 5)
            a.ink(f'M{x} 259 L{x} 267 M{x} 281 L{x} 289 M{x-15} 274 L{x-7} 274 M{x+7} 274 L{x+15} 274')
    if a.detailed:
        a.region('fuel-door', 'M299 211 L312 211 Q315 211 315 214 L315 224 L301 224 Q299 224 299 222 Z')
        a.region('roof-rail', 'M158 126 L230 126 Q234 126 234 130 L234 135 L154 135 L154 131 Q154 126 158 126 Z')
        a.ink('M144 161 L126 187 M153 158 L135 184 M215 158 L204 172 M232 157 L205 185 M56 246 L71 242 M335 238 L348 238 M160 252 L174 252 M210 252 L238 252 M108 309 L293 309')
        for x in (109, 291):
            a.ink(f'M{x-19} 259 L{x-15} 263 M{x+19} 259 L{x+15} 263 M{x-19} 289 L{x-15} 285 M{x+19} 289 L{x+15} 285')
        a.region('road', 'M35 320 Q200 312 365 320 L365 346 Q200 338 35 346 Z')
        a.ink('M51 331 L101 329 M139 328 L189 328 M227 328 L277 329 M315 330 L349 332')
    return a


def mountain(level):
    a = Drawing('Alpine lake and mountain trail', level)
    a.ellipse('sun', 313, 74, 23, 23)
    a.region('cloud', 'M50 91 C36 91 34 76 46 72 C47 59 64 55 72 64 C83 53 99 61 100 73 C116 69 124 85 112 92 Z')
    a.region('mountain-right', 'M154 228 L214 145 L234 152 L269 110 L306 151 L321 148 L366 227 Z')
    a.region('snow-right', 'M242 142 L269 110 L302 147 L289 145 L279 158 L266 142 L255 153 Z')
    a.region('mountain-left', 'M30 240 L70 187 L90 190 L151 99 L185 147 L203 145 L267 240 Z')
    if a.detailed:
        a.region('ridge-left', 'M70 187 L90 190 L113 158 L94 211 L78 218 L62 228 Z')
        a.region('ridge-right', 'M306 151 L321 148 L345 190 L331 180 L319 185 Z')
    a.region('snow-left', 'M117 149 L151 99 L185 147 L168 140 L157 159 L145 141 L133 156 Z')
    a.region('far-shore', 'M30 240 Q71 217 112 230 Q164 214 209 232 Q256 214 301 227 Q333 216 370 233 L370 262 L30 262 Z')
    a.region('lake', 'M30 262 L370 262 L370 307 Q307 288 261 297 Q217 300 176 318 L30 333 Z')
    a.region('meadow', 'M30 282 Q92 268 132 289 Q165 307 211 314 Q259 296 294 301 Q334 304 370 321 L370 365 L30 365 Z')
    a.region('trail', 'M123 365 Q143 340 186 329 Q215 320 211 314 Q231 309 247 307 Q241 326 205 338 Q184 346 174 365 Z')
    a.region('little-tree-trunk', 'M71 281 L82 281 L84 337 L69 337 Z')
    a.region('little-tree', 'M76 197 Q67 219 59 229 L66 228 L50 250 L60 248 L42 275 Q75 289 108 275 L91 249 L101 251 L85 228 L93 230 Z')
    if a.medium:
        a.region('tree-right-trunk', 'M326 278 L337 278 L339 331 L325 331 Z')
        a.region('tree-right', 'M331 209 L315 238 L321 237 L306 259 L315 258 L301 282 Q331 295 359 282 L345 259 L354 261 L340 236 L346 238 Z')
        a.region('rock-one', 'M252 342 L262 326 L284 327 L297 344 L277 351 Z')
        a.region('rock-two', 'M281 353 L291 338 L308 338 L319 354 Z')
        a.ink('M147 166 L140 185 L148 200 M171 169 L188 189 L192 207 M270 166 L285 188 L287 201 M228 186 L215 203 M58 252 Q76 260 95 252 M66 229 Q77 235 85 229 M314 262 Q332 269 348 264 M113 267 L173 267 M213 274 L278 274 M155 285 L218 285')
    if a.detailed:
        a.ink('M151 113 L148 130 M165 171 L161 188 L173 201 M306 195 L320 211 M45 244 L61 239 L76 242 M243 242 L259 238 L276 242 M316 246 L335 241 L353 246 M60 310 L63 303 L68 311 M99 341 L103 332 L107 340 M221 350 L225 342 L229 351 M344 350 L348 340 L352 350 M261 334 L270 337 L284 333 M293 346 L303 345 M204 318 L215 318 M164 351 L177 347')
        # Near-shore reeds with generous closed leaves, not hairline fill targets.
        a.region('reed-left', 'M46 350 Q34 335 38 324 Q50 331 50 346 Z')
        a.region('reed-right', 'M50 346 Q55 331 67 328 Q67 343 53 351 Z')
        a.ink('M49 362 L49 342 M345 310 Q340 296 346 289 M352 313 L354 295 M89 355 Q99 351 112 354')
    return a


if __name__ == '__main__':
    for level in LEVELS:
        (OUT / level).mkdir(parents=True, exist_ok=True)
        for name, factory in [('cat', kitten), ('car', car), ('mountain', mountain)]:
            art = factory(level)
            (OUT / level / f'{name}.svg').write_text(art.svg(), encoding='utf-8')
            print(f'{level:8} {name:8} {len(art.regions):2} regions')
