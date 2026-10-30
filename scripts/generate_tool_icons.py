"""Generate original shaded SVG drawings for the coloring tool tray."""
from pathlib import Path

out = Path(__file__).resolve().parents[1] / 'public' / 'tools'
out.mkdir(parents=True, exist_ok=True)

sticks = {
    'pencil': ('#78d554', '#409e34', '<path d="M29 13 40 3l11 10v47L40 76 29 60Z" fill="url(#body)"/><path d="M29 13h22M29 60h22" stroke="#27344d" stroke-width="3"/><path d="M29 60 40 76 51 60Z" fill="#f5ce9b"/><path d="M35 68 40 76 45 68Z" fill="#303b54"/><path d="M40 14v45" stroke="#fff8" stroke-width="3"/>'),
    'crayon': ('#ffd84e', '#f39645', '<path d="M28 10 Q28 4 34 4h12q6 0 6 6v57q0 7-7 7H35q-7 0-7-7Z" fill="url(#body)"/><path d="M28 17h24M28 57h24M28 63h24" stroke="#d37135" stroke-width="3"/><path d="M32 25h16v24H32z" fill="#ffef9b" stroke="#fff" stroke-width="2"/><path d="M35 26v22" stroke="#fff9" stroke-width="3"/>'),
    'pen': ('#3898f2', '#264ca7', '<path d="M34 5h12l2 11-2 45-6 14-6-14-2-45Z" fill="url(#body)"/><path d="M32 18h16M34 57h12" stroke="#27344d" stroke-width="3"/><path d="M36 61 40 75 44 61Z" fill="#c4cad3"/><path d="M40 69v6" stroke="#303b54" stroke-width="3"/><path d="M36 9v45" stroke="#fff8" stroke-width="3"/><path d="M49 21q10 0 8 16" fill="none" stroke="#bec9dc" stroke-width="4" stroke-linecap="round"/>'),
    'felt': ('#45c9f1', '#1683c9', '<path d="M29 18h22v43q0 8-8 8h-6q-8 0-8-8Z" fill="url(#body)"/><path d="M29 18 33 5h14l4 13Z" fill="#27344d"/><path d="M34 5h12l-3 9h-6Z" fill="#6ecdea"/><path d="M29 51h22M34 62h12" stroke="#2473a5" stroke-width="3"/><path d="M35 23v25" stroke="#fff9" stroke-width="3"/>'),
    'marker': ('#fc66a7', '#bd3e9e', '<path d="M29 18h22v44q0 7-7 7h-8q-7 0-7-7Z" fill="url(#body)"/><path d="M29 18 34 5h12l5 13Z" fill="#383b5b"/><path d="M34 5h12l-2 8h-8Z" fill="#f5a6cf"/><path d="M29 52h22M33 61h14" stroke="#993a86" stroke-width="3"/><path d="M35 22v28" stroke="#fff9" stroke-width="3"/>'),
    'brush': ('#f5a344', '#bc623b', '<path d="M35 26h10l4 38q0 10-9 11-9-1-9-11Z" fill="url(#body)"/><path d="M29 19h22v12H29Z" fill="#ccd9e7" stroke="#8a96ac" stroke-width="2"/><path d="M30 20q-3-12 10-17 13 5 10 17Z" fill="#ff6b58"/><path d="M40 5q-6 7-4 15" fill="none" stroke="#ffe69b" stroke-width="3"/><path d="M38 35v28" stroke="#fff9" stroke-width="3"/>'),
    'watercolor': ('#55dcd5', '#299ab8', '<path d="M33 20h14l3 42q1 11-10 13-11-2-10-13Z" fill="url(#body)"/><path d="M29 20h22v10H29Z" fill="#c6d2df"/><path d="M40 2q13 14 9 22-3 8-9 8t-9-8q-4-8 9-22Z" fill="#70e8f1"/><path d="M40 7q-7 13-6 18" fill="none" stroke="#fff9" stroke-width="3"/><path d="M37 35v30" stroke="#fff9" stroke-width="3"/>'),
    'glitter': ('#f7b44f', '#eb749d', '<path d="M29 23h22v39q0 10-11 12-11-2-11-12Z" fill="url(#body)"/><path d="M29 23h22v10H29Z" fill="#f9db7b"/><path d="M32 15h16l4 9H28Z" fill="#e88ac7"/><path d="M32 6h16v9H32Z" fill="#684cbb"/><path d="m40 41 3 7 8 1-6 5 2 8-7-4-7 4 2-8-6-5 8-1Z" fill="#fff6a6"/>'),
    'spray': ('#b180ed', '#7760d3', '<path d="M26 23h28v44q0 8-8 8H34q-8 0-8-8Z" fill="url(#body)"/><path d="M30 14h20v9H30Z" fill="#d3d5e5"/><path d="M35 7h10v7H35Z" fill="#493d89"/><path d="M25 4h31v7H25Z" fill="#868db0"/><path d="M32 31h16v28H32Z" fill="#e2bffa"/><circle cx="40" cy="45" r="6" fill="#fff"/><circle cx="61" cy="10" r="2" fill="#b483ee"/><circle cx="67" cy="6" r="2" fill="#b483ee"/>'),
}

extra = {
    'bucket': '''<path d="M16 23 44 11 66 34 39 66 11 43Z" fill="#55cfe9" stroke="#31415c" stroke-width="3"/><path d="M16 23 44 11 66 34 37 46Z" fill="#a5f4ff" stroke="#31415c" stroke-width="3"/><path d="M20 26 43 17 59 34 38 41Z" fill="#fff8f1"/><path d="M19 47q17 2 23 20" fill="none" stroke="#31415c" stroke-width="3"/><path d="M60 49q12 12 3 21-9 6-13-2-1-6 10-19Z" fill="#f4bd52"/>''',
    'magic': '''<path d="M15 65 51 27" stroke="#374064" stroke-width="11" stroke-linecap="round"/><path d="M17 62 49 29" stroke="#8059d5" stroke-width="6" stroke-linecap="round"/><path d="m54 5 6 14 14 6-14 6-6 14-6-14-14-6 14-6Z" fill="#ffe276" stroke="#e0a849" stroke-width="2"/><circle cx="21" cy="23" r="4" fill="#6bdfca"/><circle cx="67" cy="55" r="3" fill="#f883b1"/>''',
    'eraser': '''<path d="M14 52 43 16q5-5 10 0l17 18q4 5 0 10L43 72H26Z" fill="#f5a0c4" stroke="#37405c" stroke-width="3"/><path d="M29 34 51 56 43 72H26L14 52Z" fill="#adbbec" stroke="#37405c" stroke-width="3"/><path d="m43 16 18 19" stroke="#fff9" stroke-width="4"/><path d="M9 74h62" stroke="#d7e1ef" stroke-width="3"/>''',
}

for name, (light, dark, art) in sticks.items():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" aria-label="{name}"><defs><linearGradient id="body" x1="0" x2="1" y1="0" y2=".5"><stop stop-color="{light}"/><stop offset="1" stop-color="{dark}"/></linearGradient></defs><g stroke-linejoin="round" stroke-linecap="round" stroke="#303951" stroke-width="2">{art}</g></svg>'''
    (out / f'{name}.svg').write_text(svg, encoding='utf-8')
for name, art in extra.items():
    (out / f'{name}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" aria-label="{name}"><g stroke-linejoin="round" stroke-linecap="round">{art}</g></svg>', encoding='utf-8')
print(f'Generated {len(sticks) + len(extra)} tool illustrations in {out}')
