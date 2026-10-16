#!/usr/bin/env python3
"""Generate compact, muted ocean-glass / soft-clay SVG controls for the profile README."""
from pathlib import Path
import html
import sys

# id, label, width, accent, monogram, compact-skill-button
BUTTONS = [
    ("linkedin", "LINKEDIN", 146, "#4E96C8", "in", False),
    ("email", "EMAIL", 120, "#C97871", "@", False),
    ("diu-foundry", "DIU FOUNDRY", 160, "#7C91D6", "D", False),
    ("achievements", "GITHUB ACHIEVEMENTS", 186, "#8995A6", "★", False),
    ("gemini", "GEMINI AMBASSADOR", 188, "#867BC4", "G", False),
    ("biher", "BIHER · B.TECH CSE", 168, "#4CA2AD", "B", False),
    ("status", "BUILD · LEARN · SHIP", 172, "#4E9D88", "+", False),
    ("guide", "PROFILE GUIDE", 148, "#6E89BA", "?", False),
    ("python", "PYTHON", 94, "#578BB8", "Py", True),
    ("typescript", "TYPESCRIPT", 111, "#5E91B5", "TS", True),
    ("react", "REACT", 84, "#5AABB9", "R", True),
    ("node", "NODE.JS", 96, "#5E9C75", "N", True),
    ("supabase", "SUPABASE", 105, "#5AAE90", "S", True),
    ("postgresql", "POSTGRESQL", 115, "#6086C6", "Pg", True),
    ("figma", "FIGMA", 82, "#CE866D", "F", True),
    ("vercel", "VERCEL", 86, "#8C96A4", "V", True),
]

def escape(value: str) -> str:
    return html.escape(value, quote=True)

def render_button(button_id: str, label: str, width: int, accent: str, monogram: str, compact: bool) -> str:
    height = 32 if compact else 42
    radius = 11 if compact else 13
    icon_size = 18 if compact else 22
    icon_x = 8 if compact else 10
    icon_y = (height - icon_size) / 2
    text_x = icon_x + icon_size + (7 if compact else 8)
    available = width - text_x - (8 if compact else 9)
    # Estimate an appropriate font size so long labels stay readable without forced stretching.
    average_units = len(label) * 0.64 + max(0, len(label) - 1) * 0.035
    max_size = 10.0 if compact else 12.2
    font_size = min(max_size, available / max(average_units, 1))
    baseline = height / 2 + (3.3 if compact else 4.0)
    safe_label = escape(label)
    safe_mark = escape(monogram)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{safe_label} — ocean glass clay button</title>
<desc id="desc">Compact tactile button with a soft slate surface, subtle water sheen and a restrained coloured edge.</desc>
<defs>
  <linearGradient id="surface" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#2A394A"/>
    <stop offset=".48" stop-color="#1D2B3D"/>
    <stop offset="1" stop-color="#132032"/>
  </linearGradient>
  <linearGradient id="water" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8BE5E0" stop-opacity="0"/>
    <stop offset=".32" stop-color="#8BE5E0" stop-opacity=".16"/>
    <stop offset=".6" stop-color="#8DBBF1" stop-opacity=".22"/>
    <stop offset="1" stop-color="#8BE5E0" stop-opacity="0"/>
  </linearGradient>
  <radialGradient id="tint">
    <stop offset="0" stop-color="{accent}" stop-opacity=".16"/>
    <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  <filter id="softClay" x="-20%" y="-35%" width="145%" height="185%">
    <feDropShadow dx="0" dy="2" stdDeviation="2.2" flood-color="#020617" flood-opacity=".30"/>
  </filter>
  <clipPath id="surfaceClip">
    <rect x="3" y="3" width="{width-6}" height="{height-6}" rx="{radius}"/>
  </clipPath>
</defs>
<rect x="3" y="3" width="{width-6}" height="{height-6}" rx="{radius}" fill="url(#surface)" stroke="{accent}" stroke-opacity=".56" stroke-width=".9" filter="url(#softClay)"/>
<g clip-path="url(#surfaceClip)">
  <ellipse cx="{width*.75:.1f}" cy="{height*.38:.1f}" rx="{width*.37:.1f}" ry="{height*.95:.1f}" fill="url(#tint)">
    <animate attributeName="cx" values="{width*.62:.1f};{width*.82:.1f};{width*.62:.1f}" dur="9s" repeatCount="indefinite"/>
  </ellipse>
  <path d="M{-width*.3:.1f} 0 H{-width*.14:.1f} L{width*.19:.1f} {height} H{width*.03:.1f} Z" fill="url(#water)" opacity=".62">
    <animateTransform attributeName="transform" type="translate" values="0 0;{width*1.32:.1f} 0" dur="8.5s" repeatCount="indefinite"/>
  </path>
  <path d="M{radius} 5 H{width-radius}" stroke="#F1F5F9" stroke-opacity=".17" stroke-width=".8" stroke-linecap="round"/>
</g>
<rect x="4" y="4" width="{width-8}" height="{height-8}" rx="{radius-1}" fill="none" stroke="#F1F5F9" stroke-opacity=".08" stroke-width=".7"/>
<rect x="{icon_x}" y="{icon_y:.1f}" width="{icon_size}" height="{icon_size}" rx="{6 if compact else 7}" fill="{accent}" fill-opacity=".17" stroke="{accent}" stroke-opacity=".58" stroke-width=".8"/>
<text x="{icon_x+icon_size/2:.1f}" y="{icon_y+icon_size/2+(3.6 if compact else 4):.1f}" font-family="Arial,Helvetica,sans-serif" font-size="{9.8 if compact else 11.5}" font-weight="700" text-anchor="middle" fill="#EAF1F8">{safe_mark}</text>
<text x="{text_x}" y="{baseline:.1f}" font-family="Arial,Helvetica,sans-serif" font-size="{font_size:.2f}" font-weight="700" letter-spacing=".28" fill="#E5EDF6">{safe_label}</text>
</svg>'''

def main() -> None:
    outdir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist/buttons")
    outdir.mkdir(parents=True, exist_ok=True)
    for item in BUTTONS:
        button_id, label, width, accent, monogram, compact = item
        target = outdir / f"{button_id}.svg"
        target.write_text(render_button(*item), encoding="utf-8")
        print(f"{target}: {target.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
