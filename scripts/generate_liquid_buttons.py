#!/usr/bin/env python3
"""Generate the custom liquid-glass / claymorphism SVG buttons used by the profile README."""
from pathlib import Path
import html
import sys

# id, label, sublabel, width, accent, monogram
BUTTONS = [
    ("linkedin", "LINKEDIN", "LET'S CONNECT", 198, "#0A66C2", "in"),
    ("email", "EMAIL", "SAY HELLO", 170, "#EA4335", "@"),
    ("diu-foundry", "DIU FOUNDRY", "IDEAS → SYSTEMS", 214, "#8B5CF6", "D"),
    ("achievements", "GITHUB ACHIEVEMENTS", "OFFICIAL ACHIEVEMENT SHELF", 238, "#64748B", "★"),
    ("gemini", "GEMINI AMBASSADOR", "2026 · STUDENT COMMUNITY", 252, "#8B5CF6", "G"),
    ("biher", "BIHER · B.TECH CSE", "COMPUTER SCIENCE", 228, "#0891B2", "B"),
    ("status", "BUILD · LEARN · SHIP", "ALWAYS IN MOTION", 238, "#10B981", "+"),
    ("guide", "PROFILE GUIDE", "ASSETS & WORKFLOWS", 202, "#7C3AED", "?"),
    ("python", "PYTHON", "", 128, "#3776AB", "Py"),
    ("typescript", "TYPESCRIPT", "", 153, "#3178C6", "TS"),
    ("react", "REACT", "", 120, "#38BDF8", "R"),
    ("node", "NODE.JS", "", 132, "#339933", "N"),
    ("supabase", "SUPABASE", "", 142, "#3FCF8E", "S"),
    ("postgresql", "POSTGRESQL", "", 152, "#4169E1", "Pg"),
    ("figma", "FIGMA", "", 116, "#F24E1E", "F"),
    ("vercel", "VERCEL", "", 120, "#64748B", "V"),
]

def escape(value: str) -> str:
    return html.escape(value, quote=True)

def render_button(button_id: str, label: str, sublabel: str, width: int, accent: str, monogram: str) -> str:
    height = 60 if sublabel else 47
    radius = 18 if sublabel else 15
    icon_size = 27 if sublabel else 23
    icon_x = 12
    icon_y = (height - icon_size) / 2
    text_x = icon_x + icon_size + 10
    available = width - text_x - 12
    main_size = min(14.5 if sublabel else 13.2, max(9.5, available / max(len(label), 1) * 1.55))
    main_y = height / 2 - (4.5 if sublabel else -4)
    sub_y = height / 2 + 14.5
    safe_id = escape(button_id)
    safe_label = escape(label)
    safe_sub = escape(sublabel)
    safe_mark = escape(monogram)
    label_svg = (
        f'<text x="{text_x}" y="{main_y:.1f}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="{main_size:.1f}" font-weight="750" letter-spacing=".7" fill="#F8FAFC" '
        f'textLength="{available}" lengthAdjust="spacingAndGlyphs">{safe_label}</text>'
    )
    if sublabel:
        label_svg += (
            f'<text x="{text_x}" y="{sub_y:.1f}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" '
            f'font-size="8.5" font-weight="600" letter-spacing=".85" fill="#B9C5E4" '
            f'textLength="{available}" lengthAdjust="spacingAndGlyphs">{safe_sub}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{safe_label} — liquid glass clay button</title>
<desc id="desc">A tactile layered button with a liquid colour wave and soft glass highlights.</desc>
<defs>
  <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#26324F"/>
    <stop offset=".46" stop-color="#121D35"/>
    <stop offset="1" stop-color="#0A1021"/>
  </linearGradient>
  <linearGradient id="liquid" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#22D3EE" stop-opacity="0"/>
    <stop offset=".24" stop-color="{accent}" stop-opacity=".23"/>
    <stop offset=".55" stop-color="#C4B5FD" stop-opacity=".35"/>
    <stop offset=".78" stop-color="#F472B6" stop-opacity=".24"/>
    <stop offset="1" stop-color="#22D3EE" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="orb">
    <stop offset="0" stop-color="{accent}" stop-opacity=".44"/>
    <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  <filter id="clayDepth" x="-25%" y="-35%" width="160%" height="190%">
    <feDropShadow dx="0" dy="4" stdDeviation="3.2" flood-color="#000000" flood-opacity=".48"/>
  </filter>
  <clipPath id="glassClip">
    <rect x="4" y="4" width="{width-8}" height="{height-8}" rx="{radius}"/>
  </clipPath>
</defs>
<rect x="4" y="4" width="{width-8}" height="{height-8}" rx="{radius}" fill="url(#surface)" stroke="{accent}" stroke-opacity=".8" stroke-width="1" filter="url(#clayDepth)"/>
<g clip-path="url(#glassClip)">
  <ellipse cx="{width*.79:.1f}" cy="{height*.35:.1f}" rx="{width*.32:.1f}" ry="{height*.75:.1f}" fill="url(#orb)">
    <animate attributeName="cx" values="{width*.58:.1f};{width*.80:.1f};{width*.62:.1f}" dur="7s" repeatCount="indefinite"/>
  </ellipse>
  <path d="M{-width*.42:.1f} 0 H{-width*.18:.1f} L{width*.22:.1f} {height} H{-width*.02:.1f} Z" fill="url(#liquid)" opacity=".98">
    <animateTransform attributeName="transform" type="translate" values="0 0;{width*1.45:.1f} 0" dur="5.6s" repeatCount="indefinite"/>
  </path>
  <path d="M9 8 H{width-16}" fill="none" stroke="#FFFFFF" stroke-opacity=".22" stroke-width="1.1" stroke-linecap="round"/>
  <circle cx="{width-20}" cy="{height*.27:.1f}" r="1.8" fill="#FFFFFF" opacity=".7">
    <animate attributeName="opacity" values=".25;.95;.25" dur="3.2s" repeatCount="indefinite"/>
  </circle>
  <circle cx="{width-29}" cy="{height*.39:.1f}" r="1" fill="{accent}" opacity=".9"/>
</g>
<rect x="5" y="5" width="{width-10}" height="{height-10}" rx="{radius-1}" fill="none" stroke="#FFFFFF" stroke-opacity=".12" stroke-width=".8"/>
<rect x="{icon_x}" y="{icon_y:.1f}" width="{icon_size}" height="{icon_size}" rx="{9 if sublabel else 7}" fill="{accent}" fill-opacity=".24" stroke="{accent}" stroke-opacity=".78" stroke-width=".8"/>
<text x="{icon_x+icon_size/2:.1f}" y="{icon_y+icon_size/2+4.5:.1f}" font-family="Arial,Helvetica,sans-serif" font-size="{12 if len(monogram)>1 else 14}" font-weight="800" text-anchor="middle" fill="#FFFFFF">{safe_mark}</text>
{label_svg}
</svg>'''

def main() -> None:
    outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist/buttons")
    outdir.mkdir(parents=True, exist_ok=True)
    for item in BUTTONS:
        button_id, label, sublabel, width, accent, monogram = item
        target = outdir / f"{button_id}.svg"
        target.write_text(render_button(*item), encoding="utf-8")
        print(f"{target}: {target.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
