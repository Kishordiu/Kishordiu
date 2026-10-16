#!/usr/bin/env python3
"""Generate theme-aware static SVG cards from public GitHub profile data.

Uses only the short-lived GITHUB_TOKEN supplied to GitHub Actions.
No personal access token, external stats service, or third-party Python package is required.
"""
from __future__ import annotations

import html
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

API = "https://api.github.com"
OWNER = os.environ.get("GH_OWNER", "Kishordiu")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
OUT.mkdir(parents=True, exist_ok=True)

LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "HTML": "#e34c26", "CSS": "#563d7c", "Java": "#b07219",
    "C++": "#f34b7d", "C": "#555555", "C#": "#178600", "Go": "#00ADD8",
    "Rust": "#dea584", "Kotlin": "#A97BFF", "Dart": "#00B4AB",
    "Jupyter Notebook": "#DA5B0B", "Shell": "#89e051", "Vue": "#41b883",
    "Svelte": "#ff3e00", "PHP": "#4F5D95", "Swift": "#F05138",
    "Ruby": "#701516", "SCSS": "#c6538c", "Markdown": "#083fa1",
}
DARK = {
    "bg": "#0a141c", "panel": "#13222d", "line": "#2d424f",
    "text": "#eef4f7", "muted": "#a2b5c0", "cyan": "#6bc6ce",
    "violet": "#879fc2", "green": "#78b8a3", "pink": "#83a8bc",
    "yellow": "#d0b77e", "blue": "#7aafd0", "orange": "#c69372",
    "bar_bg": "#203541",
}
LIGHT = {
    "bg": "#f3f7f8", "panel": "#ffffff", "line": "#d4e0e5",
    "text": "#1d303b", "muted": "#58717e", "cyan": "#287f8a",
    "violet": "#667fa4", "green": "#317e68", "pink": "#7f9daf",
    "yellow": "#b18b52", "blue": "#397ba9", "orange": "#b97b59",
    "bar_bg": "#e1eaee",
}

def api_get(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Kishordiu-Profile-Stats-Workflow",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=25) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {url}: {body[:300]}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API: {exc}") from exc

def fmt(n: int) -> str:
    return f"{n:,}"

def esc(value: object) -> str:
    return html.escape(str(value), quote=True)

def get_public_repositories():
    repositories = []
    page = 1
    while page <= 10:
        batch = api_get(f"{API}/users/{quote(OWNER)}/repos?type=owner&sort=updated&per_page=100&page={page}")
        if not isinstance(batch, list):
            raise RuntimeError("Unexpected response while reading the public repositories.")
        repositories.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    # Stars/forks are still reported for all owned public repos; languages exclude forks.
    return [repo for repo in repositories if not repo.get("private", False)]

def render_stats(theme_name: str, t: dict, totals: dict, updated: str):
    width, height = 690, 226
    items = [
        ("PUBLIC REPOSITORIES", totals["repos"], t["cyan"]),
        ("STARS EARNED", totals["stars"], t["violet"]),
        ("FORKS RECEIVED", totals["forks"], t["green"]),
        ("FOLLOWERS", totals["followers"], t["pink"]),
    ]
    slots = [(32, 76), (360, 76), (32, 153), (360, 153)]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">GitHub public profile statistics — {esc(OWNER)}</title>',
        f'<desc id="desc">Public repository count, stars, forks and followers. Updated {esc(updated)}.</desc>',
        f'<defs><linearGradient id="cardBg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["panel"]}"/><stop offset="1" stop-color="{t["bg"]}"/></linearGradient><linearGradient id="titleGradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["cyan"]}"/><stop offset=".52" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["pink"]}"/></linearGradient><radialGradient id="cornerGlow"><stop offset="0" stop-color="{t["violet"]}" stop-opacity=".2"/><stop offset="1" stop-color="{t["violet"]}" stop-opacity="0"/></radialGradient></defs>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="url(#cardBg)" stroke="{t["line"]}"/>',
        f'<ellipse cx="630" cy="30" rx="185" ry="100" fill="url(#cornerGlow)"/>',
        f'<text x="28" y="31" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" letter-spacing="1.5" fill="url(#titleGradient)">PUBLIC PROFILE / SYSTEM METRICS</text>',
        f'<circle cx="661" cy="25" r="4" fill="{t["green"]}"/>',
    ]
    for (label, value, accent), (x, y) in zip(items, slots):
        parts.extend([
            f'<rect x="{x}" y="{y}" width="298" height="61" rx="11" fill="{t["panel"]}" stroke="{t["line"]}"/>',
            f'<rect x="{x}" y="{y}" width="3" height="61" rx="1.5" fill="{accent}"/>',
            f'<text x="{x+16}" y="{y+22}" font-family="Arial,Helvetica,sans-serif" font-size="10.5" letter-spacing=".9" fill="{t["muted"]}">{esc(label)}</text>',
            f'<text x="{x+16}" y="{y+47}" font-family="Arial,Helvetica,sans-serif" font-size="22" font-weight="700" fill="{t["text"]}">{fmt(int(value))}</text>',
        ])
    parts.append(f'<text x="28" y="213" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="10" fill="{t["muted"]}">PUBLIC DATA ONLY · UPDATED {esc(updated)}</text>')
    parts.append("</svg>")
    (OUT / f"stats-{theme_name}.svg").write_text("".join(parts), encoding="utf-8")

def render_languages(theme_name: str, t: dict, languages: dict, updated: str):
    width, height = 640, 286
    top = sorted(languages.items(), key=lambda item: item[1], reverse=True)[:7]
    total = sum(value for _, value in top)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">Top public repository languages — {esc(OWNER)}</title>',
        '<desc id="desc">Language share estimated from the bytes reported by GitHub for owned non-fork public repositories. This measures code volume, not skill.</desc>',
        f'<defs><linearGradient id="cardBg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t["panel"]}"/><stop offset="1" stop-color="{t["bg"]}"/></linearGradient><linearGradient id="titleGradient" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t["cyan"]}"/><stop offset=".52" stop-color="{t["violet"]}"/><stop offset="1" stop-color="{t["pink"]}"/></linearGradient><radialGradient id="cornerGlow"><stop offset="0" stop-color="{t["pink"]}" stop-opacity=".15"/><stop offset="1" stop-color="{t["pink"]}" stop-opacity="0"/></radialGradient></defs>',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="url(#cardBg)" stroke="{t["line"]}"/>',
        f'<ellipse cx="535" cy="27" rx="185" ry="105" fill="url(#cornerGlow)"/>',
        f'<text x="26" y="31" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" letter-spacing="1.5" fill="url(#titleGradient)">LANGUAGE DISTRIBUTION</text>',
    ]
    if not top or total <= 0:
        parts.append(f'<text x="26" y="86" font-family="Arial,Helvetica,sans-serif" font-size="14" fill="{t["text"]}">No public language data yet.</text>')
    else:
        x, y, bar_width, bar_height = 26, 48, 588, 9
        cur_x = x
        for name, amount in top:
            segment = bar_width * amount / total
            color = LANG_COLORS.get(name, t["cyan"])
            parts.append(f'<rect x="{cur_x:.2f}" y="{y}" width="{max(0, segment):.2f}" height="{bar_height}" fill="{color}"/>')
            cur_x += segment
        row_y = 89
        for name, amount in top:
            pct = 100 * amount / total
            color = LANG_COLORS.get(name, t["cyan"])
            parts.extend([
                f'<circle cx="32" cy="{row_y-4}" r="4" fill="{color}"/>',
                f'<text x="46" y="{row_y}" font-family="Arial,Helvetica,sans-serif" font-size="13" fill="{t["text"]}">{esc(name)}</text>',
                f'<text x="610" y="{row_y}" text-anchor="end" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="12" fill="{t["muted"]}">{pct:.1f}%</text>',
                f'<rect x="46" y="{row_y+7}" width="564" height="3" rx="1.5" fill="{t["bar_bg"]}"/>',
                f'<rect x="46" y="{row_y+7}" width="{564*pct/100:.2f}" height="3" rx="1.5" fill="{color}"/>',
            ])
            row_y += 27
    parts.append(f'<text x="26" y="{height-12}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="9.5" fill="{t["muted"]}">PUBLIC NON-FORK REPOSITORIES · UPDATED {esc(updated)}</text>')
    parts.append("</svg>")
    (OUT / f"top-languages-{theme_name}.svg").write_text("".join(parts), encoding="utf-8")

def main():
    profile = api_get(f"{API}/users/{quote(OWNER)}")
    repos = get_public_repositories()
    stars = sum(int(r.get("stargazers_count") or 0) for r in repos)
    forks = sum(int(r.get("forks_count") or 0) for r in repos)
    languages = {}
    for repo in repos:
        if repo.get("fork") or not repo.get("size"):
            continue
        full_name = repo.get("full_name")
        if not full_name:
            continue
        language_data = api_get(f"{API}/repos/{full_name}/languages")
        if isinstance(language_data, dict):
            for language, byte_count in language_data.items():
                languages[language] = languages.get(language, 0) + int(byte_count or 0)
    totals = {
        "repos": len(repos),
        "stars": stars,
        "forks": forks,
        "followers": int(profile.get("followers") or 0),
    }
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    render_stats("dark", DARK, totals, updated)
    render_stats("light", LIGHT, totals, updated)
    render_languages("dark", DARK, languages, updated)
    render_languages("light", LIGHT, languages, updated)
    print(f"Generated 4 SVG cards for @{OWNER}: {totals}; languages={len(languages)}")
    for path in sorted(OUT.glob("*.svg")):
        print(f"{path}: {path.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
