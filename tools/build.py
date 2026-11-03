#!/usr/bin/env python3
"""Build the BRAQON organization profile: profile/assets/*.svg, the avatar SVG and profile/README.md.

Edit the content below, then run:  python3 tools/build.py
No third-party packages needed.
"""

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

# ── Content ──────────────────────────────────────────────────────────────────

TAGLINE = "open-source payments, POS and developer tools"
SUB = "built in Latin America · secure by default · documented like we mean it"
PROMPT = "git init the-next-thing"

PROJECTS = [
    # (name, description, status)
    ("POS", "Open-source point of sale for small businesses.", "coming soon"),
    ("express-version-api", "Versioned routes and APIs for Express.js.", "available"),
    ("more tools", "SDKs and utilities for payment integrations.", "in the lab"),
]

PRINCIPLES = [
    ("Secure by default", "secret scanning, signed releases, least privilege"),
    ("Documented", "if it isn't in the README, it doesn't exist"),
    ("Open", "permissive licenses, public roadmap, PRs welcome"),
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


# Geometric stroke wordmark, same glyphs as the personal profile (cap height 100, stroke 13).
S = 13
h = S / 2
GLYPHS = {
    # One continuous stroke so every corner is a join (no notch where strokes meet).
    "B": (73, [f"M{h},50H44A21.75,21.75 0 0 1 44,{100-h}H{h}V{h}H40A21.75,21.75 0 0 1 40,50H{h}"]),
    "R": (74, [f"M{h},{100-h}V{h}H40A21.75,21.75 0 0 1 40,50H{h}", f"M36,50L70,{100-h}"]),
    "A": (84, [f"M3,{100-h}L42,{h}L81,{100-h}", "M21,68H63"]),
    "Q": (100, ["circle", "M62,66L93,97"]),
    "O": (100, ["circle"]),
    "N": (78, [f"M{h},{100-h}V{h}L{78-h},{100-h}V{h}"]),
}


def wordmark(color, x, y, scale, animate=True):
    parts, cursor, i = [], 0, 0
    for ch in "BRAQON":
        width, strokes = GLYPHS[ch]
        for stroke in strokes:
            attrs = f'class="g" style="animation-delay:{0.12 * i:.2f}s" pathLength="1"' if animate else ""
            if stroke == "circle":
                parts.append(f'<circle {attrs} cx="{cursor + 50}" cy="50" r="{50 - h}"/>')
            else:
                parts.append(f'<path {attrs} transform="translate({cursor},0)" d="{stroke}"/>')
            i += 1
        cursor += width + 14
    return (f'<g transform="translate({x},{y}) scale({scale})" stroke="{color}" stroke-width="{S}" '
            f'stroke-linejoin="round" fill="none">{"".join(parts)}</g>')


# Drawn by default; the animation only hides strokes while it runs.
DRAW_CSS = (".g{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 1.1s cubic-bezier(.6,0,.2,1) backwards}"
            "@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}")

# ── Assets ───────────────────────────────────────────────────────────────────

def hero(c):
    height, scale = 320, 0.8
    width = 73 + 74 + 84 + 100 + 100 + 78 + 14 * 5
    body = (
        '<defs><pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1" fill="{c["border"]}"/></pattern>'
        f'<radialGradient id="glow" cx="50%" cy="0%" r="70%"><stop offset="0" stop-color="{c["accent"]}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/></radialGradient></defs>'
        + panel(1, 1, W - 2, height - 2, c, rx=18, fill=c["bg"])
        + f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="18" fill="url(#dots)" opacity=".6"/>'
        + f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="18" fill="url(#glow)"/>'
        + wordmark(c["fg"], (W - width * scale) / 2, 52, scale)
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
    """Square avatar for the org: white wordmark on black, like the Play Console logo."""
    size, width = 1000, 73 + 74 + 84 + 100 + 100 + 78 + 14 * 5
    scale = 760 / width
    body = (f'<rect width="{size}" height="{size}" fill="#000"/>'
            + wordmark("#ffffff", (size - width * scale) / 2, (size - 100 * scale) / 2, scale, animate=False))
    return svg(size, body, width=size)

# ── README ───────────────────────────────────────────────────────────────────

def pic(name, alt):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/dark/{name}.svg"/>'
            f'<img src="assets/light/{name}.svg" width="100%" alt="{e(alt)}"/></picture>')


def readme():
    return f"""<!-- Generated by tools/build.py. Edit that file and run `python3 tools/build.py`. -->
<p align="center">
  {pic("hero", "BRAQON · " + TAGLINE)}
</p>

<p align="center">
  <a href="https://braqon.dev"><img src="https://img.shields.io/badge/braqon.dev-0d1117?style=for-the-badge&logo=googlechrome&logoColor=white" alt="braqon.dev"/></a>
  <a href="https://www.npmjs.com/org/braqon"><img src="https://img.shields.io/badge/npm-@braqon-CB3837?style=for-the-badge&logo=npm&logoColor=white" alt="npm @braqon"/></a>
  <a href="https://github.com/braqon"><img src="https://img.shields.io/badge/maintainer-@braqon-181717?style=for-the-badge&logo=github&logoColor=white" alt="maintainer @braqon"/></a>
</p>

{pic("s01", "what we build")}

{pic("projects", "projects")}

{pic("s02", "principles")}

{pic("principles", "principles")}

{pic("s03", "contribute")}

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
            "s02.svg": section(2, "principles", "// how we build", c),
            "s03.svg": section(3, "contribute", "// PRs welcome", c),
            "projects.svg": projects(c),
            "principles.svg": principles(c),
            "footer.svg": footer(c),
        }
        for name, content in files.items():
            (out / name).write_text(content, encoding="utf-8")
    (OUT / "assets" / "avatar.svg").write_text(avatar(), encoding="utf-8")
    (OUT / "README.md").write_text(readme(), encoding="utf-8")
    print("built profile/assets and profile/README.md")


if __name__ == "__main__":
    main()
