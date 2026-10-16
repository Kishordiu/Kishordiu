#!/usr/bin/env python3
"""Render GitHub profile theme banners from the committed packed dot masks.
The dot masks are the source artwork; this script builds editable vector-path dots and SMIL animation.
"""
from pathlib import Path
import json, base64, sys, random
import numpy as np
from PIL import Image, ImageDraw
W, H = 1180, 610
GRID_W, GRID_H = 120, 133
X0, Y0, PW, PH = 74.0, 137.0, 378.0, 420.0
SEED = 6615

DARK = {
    'bg':'#0b1222','panel':'#101a2d','panel2':'#0a1020','line':'#2d3c56',
    'text':'#f3f5fb','muted':'#96a4bc','portrait':'#b39aff','accent':'#22d3ee',
    'green':'#34d399','red':'#fb7185','pill':'#a78bfa','badge_text':'#101020',
    'grid':'#22314a'
}
LIGHT = {
    'bg':'#ffffff','panel':'#ffffff','panel2':'#f4f7fc','line':'#d6dfed',
    'text':'#111a2d','muted':'#64748b','portrait':'#23314a','accent':'#0891b2',
    'green':'#059669','red':'#e11d48','pill':'#7c3aed','badge_text':'#ffffff',
    'grid':'#e9eef7'
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
    """Sample three recognizable tool marks into a shared logo stage in the portrait frame."""
    sz = 100
    mask = Image.new('L', (sz,sz), 0); d = ImageDraw.Draw(mask)
    if name == 'git':
        d.polygon([(50,5),(95,50),(50,95),(5,50)], fill=255)
        d.line([(34,36),(50,50),(68,32)], fill=0, width=8)
        d.line([(50,50),(50,71)], fill=0, width=8)
        for c in [(34,36),(68,32),(50,71)]: d.ellipse((c[0]-5,c[1]-5,c[0]+5,c[1]+5),fill=0)
    elif name == 'vscode':
        d.polygon([(15,36),(42,9),(82,1),(82,99),(42,91),(15,64),(1,58),(1,42)], fill=255)
        d.polygon([(14,50),(42,29),(42,71)], fill=0)
        d.polygon([(47,25),(73,18),(73,82),(47,75),(61,50)], fill=0)
    elif name == 'figma':
        d.rounded_rectangle((24,5,53,37), radius=14, fill=255)
        d.rounded_rectangle((24,33,53,65), radius=14, fill=255)
        d.rounded_rectangle((24,61,53,93), radius=14, fill=255)
        d.ellipse((47,5,78,37), fill=255)
        d.ellipse((47,33,78,65), fill=255)
        d.rectangle((47,5,53,65),fill=0)
        d.rectangle((47,33,53,65),fill=0)
        d.ellipse((47,5,78,37),fill=255); d.ellipse((47,33,78,65),fill=255)
    pix = np.asarray(mask) > 0
    yy, xx = np.where(pix)
    rng = np.random.default_rng(seed)
    if len(xx) == 0: return [(263,347)]*count
    chosen = rng.integers(0, len(xx), count)
    scale = 1.42
    px = 263 + (xx[chosen]-50)*scale
    py = 347 + (yy[chosen]-50)*scale
    px += rng.normal(0,0.45,count); py += rng.normal(0,0.45,count)
    return list(zip(px,py))

def escape(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def make_svg(theme: dict, mode: str, dot_coords: list[tuple[float,float]], output: Path):
    rng = random.Random(SEED + (0 if mode=='dark' else 1))
    groups = dot_groups(dot_coords, rng, 60)
    sx, sy = PW / GRID_W, PH / GRID_H
    view_coords = [(X0 + (x + .5)*sx, Y0 + (y + .5)*sy) for x,y in dot_coords]
    particle_count = min(320, max(220, len(dot_coords)//40))
    chosen = rng.sample(view_coords, particle_count)
    git = logo_targets('git', particle_count, SEED+4)
    vscode = logo_targets('vscode', particle_count, SEED+5)
    figma = logo_targets('figma', particle_count, SEED+6)
    c = theme
    chunks = [f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1180" height="610" viewBox="0 0 1180 610" role="img" aria-labelledby="title desc">
<title id="title">K. Kishor Kumar — animated engineering profile</title><desc id="desc">A dithered portrait shimmers into view, then particles morph through Git, VS Code and Figma before rebuilding the portrait. Theme: {mode}.</desc>
<defs><clipPath id="portraitClip"><rect x="59" y="121" width="408" height="448" rx="18"/></clipPath><linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="{c['accent']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['accent']}" stop-opacity=".22"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></linearGradient></defs>
<rect width="1180" height="610" rx="26" fill="{c['bg']}"/>
<rect x="7.5" y="7.5" width="1165" height="595" rx="24" fill="{c['panel']}" stroke="{c['line']}" stroke-width="1.6"/>
<path d="M8 61H1172" stroke="{c['line']}"/><circle cx="34" cy="34" r="6.5" fill="#ff6159"/><circle cx="54" cy="34" r="6.5" fill="#ffbd2e"/><circle cx="74" cy="34" r="6.5" fill="#28c840"/>
<text x="590" y="40" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" letter-spacing="1.7" text-anchor="middle" fill="{c['muted']}">profile.sh — live</text>
<rect x="44" y="92" width="422" height="480" rx="23" fill="{c['panel']}" stroke="{c['line']}" stroke-width="1.6"/><text x="67" y="116" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" letter-spacing=".5" fill="{c['muted']}">VISUAL.MAP</text>
<rect x="59" y="137" width="393" height="422" rx="17" fill="{c['panel2']}" stroke="{c['line']}" stroke-width=".8"/>
<g clip-path="url(#portraitClip)"><rect x="59" y="121" width="408" height="448" fill="{c['panel2']}"/>
''']
    chunks.append(f'<g id="portrait" transform="translate({X0+PW/GRID_W/2:.3f} {Y0+PH/GRID_H/2:.3f}) scale({PW/GRID_W:.4f} {PH/GRID_H:.4f})" stroke="{c["portrait"]}" stroke-width=".82" stroke-linecap="round" fill="none">')
    chunks.append(f'<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.2113;0.3028;0.9085;1" dur="14.2s" repeatCount="indefinite"/>')
    for bucket in groups:
        d = path_d(bucket, digits=0)
        delay = rng.uniform(0,1.45)
        chunks.append(f'<path d="{d}" opacity="0"><animate attributeName="opacity" values="0;1" dur=".52s" begin="{delay:.2f}s" fill="freeze"/></path>')
    chunks.append('</g>')
    chunks.append(f'<g id="logo-travellers" fill="none" stroke="{c["accent"]}" stroke-width="2.5" stroke-linecap="round" opacity="0">')
    chunks.append(f'<path d="{path_d(chosen)}"><animate attributeName="d" dur="14.2s" repeatCount="indefinite" calcMode="linear" keyTimes="0;0.2113;0.3028;0.4437;0.5352;0.6761;0.7676;0.9085;1" values="{path_d(chosen)};{path_d(chosen)};{path_d(git)};{path_d(git)};{path_d(vscode)};{path_d(vscode)};{path_d(figma)};{path_d(figma)};{path_d(chosen)}"/></path>')
    chunks.append(f'<animate attributeName="opacity" values="0;0;1;1;1;1;1;1;0" keyTimes="0;0.2113;0.3028;0.4437;0.5352;0.6761;0.7676;0.9085;1" dur="14.2s" repeatCount="indefinite"/>')
    chunks.append('</g></g>')
    labels = [('GIT',.3028,.4437),('VS CODE',.5352,.6761),('FIGMA',.7676,.9085)]
    for label,start,end in labels:
        chunks.append(f'<text x="255" y="535" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" letter-spacing="2.4" text-anchor="middle" fill="{c["accent"]}" opacity="0">{label}<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;{start};{end};1" dur="14.2s" repeatCount="indefinite"/></text>')
    chunks.append(f'''<text x="493" y="108" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="13" letter-spacing=".7" fill="{c['muted']}">SYSTEM.INFO</text>
<text x="493" y="177" font-family="Arial,Helvetica,sans-serif" font-size="35" font-weight="750" letter-spacing=".15" fill="{c['text']}">K. KISHOR KUMAR</text>
<text x="493" y="189" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12.5" letter-spacing=".35" fill="{c['muted']}">Engineer · Builder · Innovator</text>
<rect x="493" y="191" width="185" height="32" rx="16" fill="{c['pill']}"/><text x="510" y="212" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="14" fill="{c['badge_text']}">@Kishordiu</text>
<rect x="1064" y="92" width="82" height="28" rx="14" fill="{c['panel2']}" stroke="{c['line']}"/><circle cx="1081" cy="106" r="4.5" fill="{c['red']}"><animate attributeName="opacity" values="1;.32;1" dur="1.5s" repeatCount="indefinite"/></circle><text x="1093" y="110" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="11" letter-spacing="1" fill="{c['red']}">LIVE</text>
''')
    rows = [
        ('Subject','Full-stack + AI systems'),('Role','CSE · Product builder'),('Origin','Chennai, India'),
        ('Education','B.Tech CSE · BIHER'),('Status','Building / Learning / Shipping'),
        ('ToolChain','Git · VS Code · Figma'),('Core.Lang','Python · TypeScript · C/C++'),
        ('Core.Frontend','React · Vite · HTML/CSS'),('Core.Backend','Node.js · Express'),
        ('Core.Database','Supabase · PostgreSQL'),('Core.Infra','Vercel · GitHub Actions')]
    y=257
    for label,val in rows:
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
<rect x="493" y="596" width="612" height="2.5" rx="1.25" fill="url(#sheen)"/>
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
