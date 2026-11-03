#!/usr/bin/env python3
"""Build the BRAQON organization profile: profile/assets/*.svg, the avatar SVG and profile/README.md.

Edit the content below, then run:  python3 tools/build.py
No third-party packages needed.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "profile"
ORG = "braqon-dev"
W = 1200

MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", fg="#e6edf3",
                 muted="#8b949e", accent="#00b4d8"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", fg="#1f2328",
                  muted="#59636e", accent="#0077b6"),
}
# The tail of the bq mark and of the Q is always BRAQON Cyan (see braqon-dev/brand).
CYAN = "#00b4d8"
INK = "#0b0f14"

# ── Content ──────────────────────────────────────────────────────────────────

TAGLINE = "payments, POS and developer tools"
SUB = "built in Latin America · open source at the core · secure by default"
PROMPT = "git init the-next-thing"

# Official brand icons (24x24 paths) from Simple Icons 13.0.0, CC0: https://simpleicons.org
ICONS = json.loads((Path(__file__).resolve().parent / "icons.json").read_text())
# Simple outline icons drawn here for things without a brand mark.
ICONS["web"] = "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm6.9 6h-2.9a15.6 15.6 0 0 0-1.4-3.6A8 8 0 0 1 18.9 8zM12 4c.8 1.2 1.5 2.5 1.9 4h-3.8c.4-1.5 1.1-2.8 1.9-4zM4.3 14a8 8 0 0 1 0-4h3.3a16.5 16.5 0 0 0 0 4H4.3zm.8 2h2.9c.3 1.3.8 2.5 1.4 3.6A8 8 0 0 1 5.1 16zM8 8H5.1a8 8 0 0 1 4.3-3.6C8.8 5.5 8.3 6.7 8 8zm4 12c-.8-1.2-1.5-2.5-1.9-4h3.8c-.4 1.5-1.1 2.8-1.9 4zm2.3-6H9.7a14.7 14.7 0 0 1 0-4h4.6a14.7 14.7 0 0 1 0 4zm.3 5.6c.6-1.1 1.1-2.3 1.4-3.6h2.9a8 8 0 0 1-4.3 3.6zM16.4 14a16.5 16.5 0 0 0 0-4h3.3a8 8 0 0 1 0 4h-3.3z"
ICONS["mail"] = "M3 5h18a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zm1 2.4V17h16V7.4l-8 5.3-8-5.3zM5.2 7l6.8 4.5L18.8 7H5.2z"
ICON_COLORS = {"github": None, "linkedin": "#0A66C2", "x": None, "youtube": "#FF0000",
               "instagram": "#E4405F", "npm": "#CB3837", "jsr": "#F7DF1E", "web": None, "mail": None}

LINKS = [
    ("web", "BRAQON.DEV", "https://braqon.dev", "web"),
    ("npm", "@BRAQON", "https://www.npmjs.com/org/braqon", "npm"),
    ("jsr", "@BRAQON", "https://jsr.io/@braqon", "jsr"),
    ("x", "@BRAQONDEV", "https://x.com/braqondev", "x"),
    ("linkedin", "BRAQON", "https://www.linkedin.com/company/braqon/", "linkedin"),
    ("youtube", "@BRAQON", "https://www.youtube.com/@braqon", "youtube"),
    ("instagram", "@BRAQONDEV", "https://www.instagram.com/braqondev/", "instagram"),
    ("mail", "HOLA@BRAQON.DEV", "mailto:hola@braqon.dev", "mail"),
]

ROADMAP = [
    # (stage, title, detail, state)
    ("NOW", "express-version-api 2.x", "versioned Express APIs · npm + JSR", "live"),
    ("NEXT", "BRAQON POS", "open-core point of sale", "soon"),
    ("LATER", "payments toolkit", "SDKs for LATAM payment rails", "idea"),
]

PROJECTS = [
    # (name, description, status)
    ("POS", "Point of sale for small businesses. Open core, Pro later.", "coming soon"),
    ("express-version-api", "Versioned routes and APIs for Express.js.", "available"),
    ("more tools", "SDKs and utilities for payment integrations.", "in the lab"),
]

PRINCIPLES = [
    ("Secure by default", "secret scanning, signed releases, least privilege"),
    ("Documented", "if it isn't in the README, it doesn't exist"),
    ("Clear licensing", "every repo says if it is open, free or paid"),
    ("Made in LATAM", "built for the way this region actually pays"),
]

# ── SVG helpers ──────────────────────────────────────────────────────────────

def e(text):
    return escape(text, {'"': "&quot;"})


def svg(height, body, css="", width=W):
    style = ("<style>.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
             f"{css}@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" fill="none" role="img">{style}{body}</svg>\n')


def text(x, y, s, c, size=16, color=None, font=SANS, weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{e(font)}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color or c["fg"]}" text-anchor="{anchor}"{extra}>{s}</text>')


def panel(x, y, w, h, c, rx=14, fill=None, stroke=None, dashed=False):
    dash = ' stroke-dasharray="6 6"' if dashed else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill or c["panel"]}" '
            f'stroke="{stroke or c["border"]}"{dash}/>')


# Geometric stroke wordmark from the brand kit (cap height 100, stroke 13). The Q tail is the accent.
S = 13
h = S / 2
GLYPHS = {
    # One continuous stroke so every corner is a join (no notch where strokes meet).
    "B": (73, [f"M{h},50H44A21.75,21.75 0 0 1 44,{100-h}H{h}V{h}H40A21.75,21.75 0 0 1 40,50H{h}"]),
    "R": (74, [f"M{h},{100-h}V{h}H40A21.75,21.75 0 0 1 40,50H{h}", f"M36,50L70,{100-h}"]),
    "A": (84, [f"M3,{100-h}L42,{h}L81,{100-h}", "M21,68H63"]),
    "Q": (100, ["circle", "tail:M74,74L98,98"]),
    "O": (100, ["circle"]),
    "N": (78, [f"M{h},{100-h}V{h}L{78-h},{100-h}V{h}"]),
}


def wordmark(color, x, y, scale, animate=True, accent=CYAN):
    parts, cursor, i = [], 0, 0
    for ch in "BRAQON":
        width, strokes = GLYPHS[ch]
        for stroke in strokes:
            attrs = f'class="g" style="animation-delay:{0.12 * i:.2f}s" pathLength="1"' if animate else ""
            if stroke == "circle":
                parts.append(f'<circle {attrs} cx="{cursor + 50}" cy="50" r="{50 - h}"/>')
            elif stroke.startswith("tail:"):
                parts.append(f'<path {attrs} stroke="{accent}" transform="translate({cursor},0)" d="{stroke[5:]}"/>')
            else:
                parts.append(f'<path {attrs} transform="translate({cursor},0)" d="{stroke}"/>')
            i += 1
        cursor += width + 14
    return (f'<g transform="translate({x},{y}) scale({scale})" stroke="{color}" stroke-width="{S}" '
            f'stroke-linecap="round" stroke-linejoin="round" fill="none">{"".join(parts)}</g>')


# The bq mark: the b of Braian and the tail of the Q of Quintian. Box 62x92, stroke 12.
MARK_W, MARK_H = 62, 92


def mark(color, x, y, scale, animate=True, accent=CYAN):
    attrs = (lambda d: f'class="g" style="animation-delay:{d:.2f}s" pathLength="1"') if animate else (lambda d: "")
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({scale:.4f})" fill="none" stroke-width="12" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<path {attrs(0)} stroke="{color}" d="M6 6V58"/>'
            f'<circle {attrs(0.1)} stroke="{color}" cx="28" cy="58" r="22"/>'
            f'<path {attrs(0.3)} stroke="{accent}" d="M43.56 73.56L56 86"/></g>')


WORD_W = 73 + 74 + 84 + 100 + 100 + 78 + 14 * 5


def lockup(color, x, y, scale, animate=True):
    """Mark + wordmark, in wordmark units: the mark is 1.42x the cap height, then a half-cap gap."""
    ms = 142 / MARK_H
    return (mark(color, x, y, ms * scale, animate)
            + wordmark(color, x + (MARK_W * ms + 50) * scale, y + 21 * scale, scale, animate))


LOCKUP_W = MARK_W * 142 / MARK_H + 50 + WORD_W


# Drawn by default; the animation only hides strokes while it runs.
DRAW_CSS = (".g{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1.1s cubic-bezier(.6,0,.2,1) backwards}"
            "@keyframes draw{from{stroke-dashoffset:1;stroke-opacity:0}1%{stroke-opacity:1}to{stroke-dashoffset:0}}")
# stroke-opacity hides the dot a round cap leaves on a zero-length dash before each stroke starts.

# ── Assets ───────────────────────────────────────────────────────────────────


def plano(c, w, h, r, cx, cy):
    """Background: the construction lines of the bq mark (ring, stem, axes, cyan tail), clipped to the panel."""
    s = r / 22
    x, y = cx - 28 * s, cy - 58 * s
    return (f'<defs><clipPath id="pc"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath></defs>'
            f'<g clip-path="url(#pc)"><g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" fill="none" stroke-width="{1.4/s:.3f}">'
            f'<g stroke="{c["border"]}" stroke-opacity=".5"><path d="M-400 58H400M28 -400V400M6 -400V400"/>'
            f'<circle cx="28" cy="58" r="16"/><circle cx="28" cy="58" r="28"/></g>'
            f'<g stroke="{c["border"]}"><path d="M6 6V58"/><circle cx="28" cy="58" r="22"/></g>'
            f'<path d="M43.56 73.56L56 86" stroke="#00b4d8" stroke-opacity=".8"/>'
            f'<circle cx="28" cy="58" r="{3.5/s:.2f}" fill="#00b4d8" stroke="none"/></g></g>')

def hero(c):
    height, scale = 320, 0.8
    body = (
        f'<defs><radialGradient id="glow" cx="50%" cy="0%" r="70%"><stop offset="0" stop-color="{c["accent"]}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient></defs>'
        + panel(1, 1, W - 2, height - 2, c, rx=18, fill=c["bg"])
        + plano(c, W, height, height * 0.42, W * 0.86, height * 0.6)
        + f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="18" fill="url(#glow)"/>'
        + lockup(c["fg"], (W - LOCKUP_W * scale) / 2, 34, scale)
        + text(W / 2, 192, e(TAGLINE), c, size=26, weight=600, anchor="middle")
        + text(W / 2, 224, e(SUB), c, size=15, color=c["muted"], font=MONO, anchor="middle")
        + f'<text x="{W/2}" y="276" font-family="{e(MONO)}" font-size="17" text-anchor="middle">'
          f'<tspan fill="{c["accent"]}">{ORG}@github</tspan><tspan fill="{c["muted"]}">:~$ </tspan>'
          f'<tspan fill="{c["fg"]}">{e(PROMPT)}</tspan><tspan class="blink" fill="{c["accent"]}"> ▋</tspan></text>'
    )
    return svg(height, body, DRAW_CSS)


def section(n, title, comment, c):
    body = (
        f'<defs><linearGradient id="rule" x1="0" x2="1"><stop offset="0" stop-color="{c["accent"]}"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></linearGradient></defs>'
        + text(0, 50, f"{n:02d}", c, size=30, color=c["accent"], font=MONO, weight=700)
        + text(62, 50, e(title), c, size=30, weight=700)
        + text(W, 50, e(comment), c, size=15, color=c["muted"], font=MONO, anchor="end")
        + f'<rect x="0" y="70" width="{W}" height="2" fill="url(#rule)"/>'
    )
    return svg(84, body)


def projects(c):
    gap, cw, ch = 24, (W - 2 * 24 - 2) / 3, 170
    parts = []
    for i, (name, desc, status) in enumerate(PROJECTS):
        x = 1 + i * (cw + gap)
        live = status == "available"
        parts.append(panel(x, 1, cw, ch, c, fill=c["panel"] if live else c["bg"],
                           stroke=c["accent"] if live else c["border"], dashed=not live))
        parts.append(text(x + 24, 46, e(name), c, size=20, color=c["accent"] if live else c["fg"],
                          font=MONO, weight=700))
        words, lines, line = desc.split(), [], ""
        for word in words:
            if len(line) + len(word) > 34:
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        lines.append(line)
        for j, l in enumerate(lines):
            parts.append(text(x + 24, 84 + j * 24, e(l), c, size=16, color=c["muted"]))
        dot = c["accent"] if live else c["muted"]
        parts.append(f'<circle cx="{x + 30}" cy="{ch - 30}" r="5" fill="{dot}"/>')
        parts.append(text(x + 44, ch - 25, e(status), c, size=14, color=dot, font=MONO))
    return svg(ch + 2, "".join(parts))


def principles(c):
    cw, gap = (W - 24 - 2) / 2, 24
    parts = []
    for i, (title, sub) in enumerate(PRINCIPLES):
        x = 1 + (i % 2) * (cw + gap)
        y = 1 + (i // 2) * 96
        parts.append(panel(x, y, cw, 80, c))
        parts.append(text(x + 24, y + 34, e(title), c, size=18, weight=700))
        parts.append(text(x + 24, y + 60, e(sub), c, size=14, color=c["muted"], font=MONO))
    return svg(2 * 96 - 14, "".join(parts))


def footer(c):
    body = (
        f'<text x="{W/2}" y="40" font-family="{e(MONO)}" font-size="17" text-anchor="middle">'
        f'<tspan fill="{c["accent"]}">{ORG}@github</tspan><tspan fill="{c["muted"]}">:~$ </tspan>'
        f'<tspan fill="{c["fg"]}">git push --follow-tags</tspan><tspan class="blink" fill="{c["accent"]}"> ▋</tspan></text>'
        + text(W / 2, 76, "BRAQON™ · hecho en Colombia 🇨🇴", c, size=15, color=c["muted"], font=MONO, anchor="middle")
    )
    return svg(96, body)


def avatar():
    """Square avatar for the org: the white bq mark with its cyan tail on Ink."""
    size = 1000
    scale = size * 0.62 / MARK_H
    x = (size - MARK_W * scale) / 2 + size * 0.012  # optical nudge: the tail weighs on the right
    body = (f'<rect width="{size}" height="{size}" fill="{INK}"/>'
            + mark("#ffffff", x, (size - MARK_H * scale) / 2, scale, animate=False))
    return svg(size, body, width=size)

# ── README ───────────────────────────────────────────────────────────────────

def button(label, c, icon):
    width = round(48 + len(label) * 9.4 + 22)
    color = ICON_COLORS[icon] or c["fg"]
    body = (f'<rect x="1" y="1" width="{width-2}" height="42" rx="21" fill="{c["panel"]}" stroke="{c["border"]}"/>'
            f'<path transform="translate(16,12) scale(0.8333)" fill="{color}" d="{ICONS[icon]}"/>'
            + text(48, 27, e(label), c, size=14, font=MONO, weight=700, extra=' letter-spacing="1.5"'))
    return svg(44, body, width=width)


def roadmap(c):
    cw, gap, height = (W - 2 * 24 - 2) / 3, 24, 150
    parts = []
    for i, (stage, title, detail, state) in enumerate(ROADMAP):
        x = 1 + i * (cw + gap)
        live = state == "live"
        parts.append(panel(x, 1, cw, height - 2, c, fill=c["panel"] if live else c["bg"],
                           stroke=c["accent"] if live else c["border"], dashed=state == "idea"))
        parts.append(text(x + 24, 40, stage, c, size=13, color=c["accent"] if live else c["muted"], font=MONO,
                          weight=700, extra=' letter-spacing="3"'))
        parts.append(text(x + 24, 80, e(title), c, size=20, weight=700))
        parts.append(text(x + 24, 110, e(detail), c, size=14, color=c["muted"], font=MONO))
        if i < len(ROADMAP) - 1:
            ax = x + cw + 4
            parts.append(f'<path d="M{ax},{height/2} h{gap-8}" stroke="{c["border"]}" stroke-width="2"/>'
                         f'<path d="M{ax+gap-14},{height/2-5} l6,5 -6,5" stroke="{c["border"]}" stroke-width="2" fill="none"/>')
    return svg(height, "".join(parts))


def pic(name, alt):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg"/>'
            f'<img src="assets/light/{name}.svg" width="100%" alt="{e(alt)}"/></picture>')


def readme():
    links = "\n  ".join(
        f'<a href="{url}"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/l-{name}.svg"/>'
        f'<img src="assets/light/l-{name}.svg" height="32" alt="{e(label)}"/></picture></a>'
        for name, label, url, _ in LINKS)
    return f"""<!-- Generated by tools/build.py. Edit that file and run `python3 tools/build.py`. -->
<p align="center">
  {pic("hero", "BRAQON · " + TAGLINE)}
</p>

<p align="center">
  {links}
</p>

<p align="center"><sub>maintained by <a href="https://github.com/braqon">@braqon</a> · hecho en Colombia 🇨🇴</sub></p>

{pic("s01", "what we build")}

{pic("projects", "projects")}

<p align="center">
  <a href="https://www.npmjs.com/package/express-version-api"><img src="https://img.shields.io/npm/v/express-version-api?style=flat-square&logo=npm&label=express-version-api&color=00b4d8" alt="npm version"/></a>
  <a href="https://jsr.io/@braqon/express-version-api"><img src="https://jsr.io/badges/@braqon/express-version-api" alt="JSR"/></a>
  <a href="https://www.npmjs.com/package/express-version-api"><img src="https://img.shields.io/npm/dm/express-version-api?style=flat-square&color=0077b6" alt="npm downloads"/></a>
  <a href="https://github.com/{ORG}/express-version-api/actions"><img src="https://img.shields.io/github/actions/workflow/status/{ORG}/express-version-api/ci.yml?branch=main&style=flat-square&label=CI" alt="CI"/></a>
  <a href="https://github.com/{ORG}/express-version-api"><img src="https://img.shields.io/github/stars/{ORG}/express-version-api?style=flat-square&color=00b4d8" alt="stars"/></a>
</p>

{pic("s02", "roadmap")}

{pic("roadmap", "roadmap: now express-version-api, next BRAQON POS, later payments toolkit")}

{pic("s03", "principles")}

{pic("principles", "principles")}

{pic("s04", "contribute")}

- 🐛 Found a bug? Open an issue in the project's repo using the templates.
- 🔐 Found a vulnerability? **Don't open a public issue.** Read our [security policy](https://github.com/{ORG}/.github/blob/main/SECURITY.md).
- 🤝 Want to help? Start with [CONTRIBUTING](https://github.com/{ORG}/.github/blob/main/CONTRIBUTING.md) and our [code of conduct](https://github.com/{ORG}/.github/blob/main/CODE_OF_CONDUCT.md).
- 🇨🇴 Hablamos español e inglés. Issues and PRs welcome in both.

{pic("footer", "git push")}
"""


def main():
    for theme, c in THEMES.items():
        out = OUT / "assets" / theme
        out.mkdir(parents=True, exist_ok=True)
        files = {
            "hero.svg": hero(c),
            "s01.svg": section(1, "what we build", "// shipping in the open", c),
            "s02.svg": section(2, "roadmap", "// where we're going", c),
            "s03.svg": section(3, "principles", "// how we build", c),
            "s04.svg": section(4, "contribute", "// PRs welcome", c),
            "roadmap.svg": roadmap(c),
            "projects.svg": projects(c),
            "principles.svg": principles(c),
            "footer.svg": footer(c),
        }
        files.update({f"l-{name}.svg": button(label, c, icon) for name, label, _, icon in LINKS})
        for name, content in files.items():
            (out / name).write_text(content, encoding="utf-8")
    (OUT / "assets" / "avatar.svg").write_text(avatar(), encoding="utf-8")
    (OUT / "README.md").write_text(readme(), encoding="utf-8")
    print("built profile/assets and profile/README.md")
    # Members (and owners) see the README of the private braqon-dev/.github-private repo.
    # Same content, with image paths pointing at this public repo so nothing is duplicated.
    member = OUT.parent.parent / "dot-github-private" / "profile"
    if member.is_dir():
        raw = "https://raw.githubusercontent.com/braqon-dev/.github/main/profile/assets/"
        (member / "README.md").write_text(readme().replace('"assets/', f'"{raw}'), encoding="utf-8")
        print(f"built {member / 'README.md'}")


if __name__ == "__main__":
    main()
