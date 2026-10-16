#!/usr/bin/env python3
"""Render GitHub profile theme banners from the committed packed dot masks.
The dot masks are the source artwork; this script builds editable vector-path dots and SMIL animation.
"""
from pathlib import Path
import json, base64, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W, H = 1180, 610
GRID_W, GRID_H = 120, 133
X0, Y0, PW, PH = 74.0, 137.0, 378.0, 420.0
SEED = 6615

DARK = {
    'bg':'#0a141c','panel':'#13222d','panel2':'#0e1b25','line':'#2d424f',
    'text':'#eef4f7','muted':'#a2b5c0','portrait':'#b4d8e4','accent':'#6bc6ce',
    'green':'#78b8a3','red':'#c8797d','pill':'#4d8198','badge_text':'#ffffff',
    'grid':'#203541','pink':'#83a8bc','yellow':'#d0b77e','blue':'#7aafd0',
    'orange':'#c69372','violet':'#879fc2'
}
LIGHT = {
    'bg':'#f3f7f8','panel':'#ffffff','panel2':'#edf3f5','line':'#d4e0e5',
    'text':'#1d303b','muted':'#58717e','portrait':'#286d83','accent':'#287f8a',
    'green':'#317e68','red':'#b86168','pill':'#4e7594','badge_text':'#ffffff',
    'grid':'#e1eaee','pink':'#7f9daf','yellow':'#b18b52','blue':'#397ba9',
    'orange':'#b97b59','violet':'#667fa4'
}

def path_d(points, digits=1):
    # Every move-only subpath gets a zero-length round-capped line: crisp vector dots, no glyphs.
    return ''.join(f'M{x:.{digits}f},{y:.{digits}f}h0' for x,y in points)

def dot_groups(coords, rng, n_groups=60):
    idx = list(range(len(coords))); rng.shuffle(idx)
    buckets = [[] for _ in range(n_groups)]
    for j,i in enumerate(idx): buckets[j % n_groups].append(coords[i])
    return buckets

def logo_targets(name: str, count: int, seed: int):
    """Sample DIU lettering so the portrait particles reassemble as our wordmark."""
    sz = 120
    mask = Image.new("L", (sz, sz), 0)
    draw = ImageDraw.Draw(mask)
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        word_font = ImageFont.truetype(font_path, 47)
        sub_font = ImageFont.truetype(font_path, 10)
    except OSError:
        word_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    word = "DIU"
    bbox = draw.textbbox((0, 0), word, font=word_font, stroke_width=1)
    word_w = bbox[2] - bbox[0]
    draw.text(((sz - word_w) / 2, 15), word, font=word_font, fill=255,
              stroke_width=1, stroke_fill=255)

    sub = "FOUNDRY"
    sub_box = draw.textbbox((0, 0), sub, font=sub_font)
    sub_w = sub_box[2] - sub_box[0]
    draw.text(((sz - sub_w) / 2, 75), sub, font=sub_font, fill=255)

    pixels = np.asarray(mask) > 0
    yy, xx = np.where(pixels)
    rng = np.random.default_rng(seed)
    if len(xx) == 0:
        return [(263, 347)] * count
    chosen = rng.integers(0, len(xx), count)
    scale = 2.12
    px = 263 + (xx[chosen] - sz / 2) * scale
    py = 347 + (yy[chosen] - sz / 2) * scale
    px += rng.normal(0, 0.34, count)
    py += rng.normal(0, 0.34, count)
    return list(zip(px, py))

def escape(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def make_svg(theme: dict, mode: str, dot_coords: list[tuple[float,float]], output: Path):
    rng = random.Random(SEED + (0 if mode=='dark' else 1))
    groups = dot_groups(dot_coords, rng, 60)
    sx, sy = PW / GRID_W, PH / GRID_H
    view_coords = [(X0 + (x + .5)*sx, Y0 + (y + .5)*sy) for x,y in dot_coords]
    particle_count = min(320, max(220, len(dot_coords)//40))
    chosen = rng.sample(view_coords, particle_count)
    diu = logo_targets('diu', particle_count, SEED+4)
    c = theme
    chunks = [f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-labelledby="title desc">
<title id="title">K. Kishor Kumar — animated engineering profile</title><desc id="desc">A dithered portrait dissolves into colourful living particles, reforms as the DIU Foundry wordmark, then reconstructs the portrait. Theme: {mode}.</desc>
<defs>
<clipPath id="portraitClip"><rect x="59" y="121" width="408" height="448" rx="18"/></clipPath>
<clipPath id="frameClip"><rect x="7.5" y="7.5" width="1165" height="595" rx="24"/></clipPath>
<linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['panel']}"/><stop offset=".5" stop-color="{c['panel2']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
<linearGradient id="portraitGradient" gradientUnits="userSpaceOnUse" x1="60" y1="140" x2="455" y2="565"><stop offset="0" stop-color="{c['violet']}"/><stop offset=".26" stop-color="{c['blue']}"/><stop offset=".5" stop-color="{c['accent']}"/><stop offset=".73" stop-color="{c['pink']}"/><stop offset="1" stop-color="{c['yellow']}"/></linearGradient>
<linearGradient id="travellerGradient" gradientUnits="userSpaceOnUse" x1="490" y1="120" x2="800" y2="420"><stop offset="0" stop-color="{c['accent']}"/><stop offset=".42" stop-color="{c['violet']}"/><stop offset=".72" stop-color="{c['pink']}"/><stop offset="1" stop-color="{c['yellow']}"/></linearGradient>
<linearGradient id="titleGradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['text']}"/><stop offset=".48" stop-color="{c['accent']}"/><stop offset="1" stop-color="{c['pink']}"/></linearGradient>
<linearGradient id="pillGradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['violet']}"/><stop offset=".58" stop-color="{c['blue']}"/><stop offset="1" stop-color="{c['pink']}"/></linearGradient>
<filter id="clayShadow" x="-35%" y="-50%" width="170%" height="210%"><feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity=".38"/></filter>
<clipPath id="pillClip"><rect x="493" y="191" width="185" height="32" rx="16"/></clipPath>
<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="{c['accent']}" stop-opacity="0"/><stop offset=".35" stop-color="{c['accent']}" stop-opacity=".25"/><stop offset=".7" stop-color="{c['pink']}" stop-opacity=".3"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></linearGradient>
<radialGradient id="glowOne"><stop offset="0" stop-color="{c['violet']}" stop-opacity=".25"/><stop offset="1" stop-color="{c['violet']}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowTwo"><stop offset="0" stop-color="{c['accent']}" stop-opacity=".20"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowThree"><stop offset="0" stop-color="{c['pink']}" stop-opacity=".17"/><stop offset="1" stop-color="{c['pink']}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="1180" height="610" rx="26" fill="{c['bg']}"/>
<rect x="7.5" y="7.5" width="1165" height="595" rx="24" fill="url(#surface)" stroke="{c['line']}" stroke-width="1.6"/>
<g clip-path="url(#frameClip)" opacity=".95"><ellipse cx="185" cy="215" rx="330" ry="300" fill="url(#glowOne)"/><ellipse cx="980" cy="460" rx="365" ry="280" fill="url(#glowTwo)"/><ellipse cx="840" cy="90" rx="240" ry="155" fill="url(#glowThree)"/></g>
<path d="M8 61H1172" stroke="{c['line']}"/><circle cx="34" cy="34" r="6.5" fill="#ff6159"/><circle cx="54" cy="34" r="6.5" fill="#ffbd2e"/><circle cx="74" cy="34" r="6.5" fill="#28c840"/>
<text x="590" y="40" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" letter-spacing="1.7" text-anchor="middle" fill="{c['muted']}">profile.sh — live</text>
<rect x="44" y="92" width="422" height="480" rx="23" fill="url(#surface)" stroke="url(#portraitGradient)" stroke-opacity=".75" stroke-width="1.6"/><rect x="44.8" y="128" width="2.8" height="402" rx="1.4" fill="url(#portraitGradient)"/><text x="67" y="116" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" letter-spacing=".5" fill="{c['muted']}">VISUAL.MAP</text>
<rect x="59" y="137" width="393" height="422" rx="17" fill="{c['panel2']}" stroke="{c['line']}" stroke-width=".8"/>
<g clip-path="url(#portraitClip)"><rect x="59" y="121" width="408" height="448" fill="{c['panel2']}"/>
''']
    chunks.append(f'<g id="portrait" transform="translate({X0+PW/GRID_W/2:.3f} {Y0+PH/GRID_H/2:.3f}) scale({PW/GRID_W:.4f} {PH/GRID_H:.4f})" stroke="url(#portraitGradient)" stroke-width=".82" stroke-linecap="round" fill="none">')
    chunks.append(f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.2113;0.3028;0.9085;1" dur="14.2s" repeatCount="indefinite"/>')
    for bucket in groups:
        d = path_d(bucket, digits=0)
        delay = rng.uniform(0,1.45)
        chunks.append(f'<path d="{d}" opacity="0"><animate attributeName="opacity" values="0;1" dur=".52s" begin="{delay:.2f}s" fill="freeze"/></path>')
    chunks.append('</g>')
    chunks.append(f'<g id="logo-travellers" fill="none" stroke="url(#travellerGradient)" stroke-width="2.8" stroke-linecap="round" opacity="0">')
    chunks.append(f'<path d="{path_d(chosen)}"><animate attributeName="d" dur="14.2s" repeatCount="indefinite" calcMode="linear" keyTimes="0;0.21;0.32;0.84;1" values="{path_d(chosen)};{path_d(chosen)};{path_d(diu)};{path_d(diu)};{path_d(chosen)}"/></path>')
    chunks.append(f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.21;0.32;0.84;1" dur="14.2s" repeatCount="indefinite"/>')
    chunks.append('</g></g>')
    labels = [('DIU // FOUNDRY',.32,.84)]
    for label,start,end in labels:
        chunks.append(f'<text x="255" y="535" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" letter-spacing="2.4" text-anchor="middle" fill="{c["accent"]}" opacity="0">{label}<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;{start};{end};1" dur="14.2s" repeatCount="indefinite"/></text>')
    chunks.append(f'''<text x="493" y="108" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" letter-spacing=".7" fill="{c['muted']}">SYSTEM.INFO</text>
<text x="493" y="177" font-family="Arial,Helvetica,sans-serif" font-size="35" font-weight="750" letter-spacing=".15" fill="url(#titleGradient)">K. KISHOR KUMAR</text>
<text x="493" y="189" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12.5" letter-spacing=".35" fill="{c['muted']}">Engineer · Builder · Innovator</text>
<rect x="493" y="191" width="185" height="32" rx="16" fill="url(#pillGradient)" stroke="#ffffff" stroke-opacity=".62" stroke-width="1" filter="url(#clayShadow)"/><g clip-path="url(#pillClip)"><rect x="494" y="192" width="183" height="10" rx="5" fill="#ffffff" opacity=".18"/><path d="M-20 191 L15 191 L-4 223 L-39 223 Z" fill="#ffffff" opacity=".28"><animateTransform attributeName="transform" type="translate" values="-160 0;230 0" dur="4.8s" repeatCount="indefinite"/></path></g><text x="510" y="212" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" font-weight="700" fill="{c['badge_text']}">@Kishordiu</text>
<rect x="1064" y="92" width="82" height="28" rx="14" fill="{c['panel2']}" stroke="{c['line']}"/><circle cx="1081" cy="106" r="4.5" fill="{c['red']}"><animate attributeName="opacity" values="1;.32;1" dur="1.5s" repeatCount="indefinite"/></circle><text x="1093" y="110" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11" letter-spacing="1" fill="{c['red']}">LIVE</text>
''')
    rows = [
        ('Subject','Full-stack + AI systems'),('Role','CSE · Product builder'),('Origin','Chennai, India'),
        ('Education','B.Tech CSE · BIHER'),('Status','Building / Learning / Shipping'),
        ('ToolChain','Git · VS Code · Figma'),('Core.Lang','Python · TypeScript · C/C++'),
        ('Core.Frontend','React · Vite · HTML/CSS'),('Core.Backend','Node.js · Express'),
        ('Core.Database','Supabase · PostgreSQL'),('Core.Infra','Vercel · GitHub Actions')]
    y=257
    for row_index,(label,val) in enumerate(rows):
        row_colors = [c["accent"], c["violet"], c["pink"], c["green"], c["yellow"]]
        chunks.append(f'<circle cx="474" cy="{y-4}" r="2.8" fill="{row_colors[row_index % len(row_colors)]}"/>')
        chunks.append(f'<text x="493" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13.2" fill="{c["muted"]}">{label}</text>')
        chunks.append(f'<path d="M{493+len(label)*7.1:.1f} {y-4} H{705-len(label)*1.2:.1f}" stroke="{c["line"]}" stroke-width=".75" stroke-dasharray="1.5 5" opacity=".65"/>')
        chunks.append(f'<text x="751" y="{y}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13.2" fill="{c["text"]}">{escape(val)}</text>')
        y += 25
    chunks.append(f'''<path d="M493 532H1105" stroke="{c['line']}" stroke-width=".9"/>
<a xlink:href="https://www.linkedin.com/in/k-kishor-kumar-3b2910303/" target="_blank"><text x="493" y="558" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" fill="{c['accent']}">LinkedIn</text></a>
<a xlink:href="https://github.com/Kishordiu" target="_blank"><text x="582" y="558" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" fill="{c['accent']}">GitHub</text></a>
<a xlink:href="mailto:kishorvishwa2525@gmail.com"><text x="657" y="558" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" fill="{c['accent']}">Email</text></a>
<a xlink:href="https://diufoundry.online/" target="_blank"><text x="724" y="558" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" fill="{c['accent']}">DIU Foundry</text></a>
<text x="493" y="586" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" letter-spacing=".7" fill="{c['muted']}">RESEARCH  -&gt;  BUILD  -&gt;  TEST  -&gt;  SHIP</text>
<rect x="493" y="596" width="612" height="2.5" rx="1.25" fill="url(#sheen)"/><circle cx="1100" cy="558" r="3.5" fill="{c['green']}"/><circle cx="1112" cy="558" r="3.5" fill="{c['accent']}"/><circle cx="1124" cy="558" r="3.5" fill="{c['pink']}"/>
</svg>''')
    output.write_text(''.join(chunks), encoding='utf-8')

def main():
    here = Path(__file__).resolve().parent
    data_path = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "portrait_masks.json"
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")
    outdir.mkdir(parents=True, exist_ok=True)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    width, height = int(data["width"]), int(data["height"])
    if (width, height) != (GRID_W, GRID_H) or data.get("format") != "row-major-bitpack-v1":
        raise ValueError("Unexpected portrait mask schema or dimensions")
    def unpack(key):
        raw = base64.b64decode(data[key], validate=True)
        bits = np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="big")[:width*height]
        return bits.reshape((height, width)).astype(bool)
    coords_by_mode = {}
    for mode, key in [("dark", "dark_mask_b64"), ("light", "light_mask_b64")]:
        rows, cols = np.where(unpack(key))
        coords_by_mode[mode] = list(zip(cols.astype(float), rows.astype(float)))
    make_svg(DARK, "dark", coords_by_mode["dark"], outdir / "dark.svg")
    make_svg(LIGHT, "light", coords_by_mode["light"], outdir / "light.svg")
    for f in (outdir / "dark.svg", outdir / "light.svg"):
        print(f"{f}: {f.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
