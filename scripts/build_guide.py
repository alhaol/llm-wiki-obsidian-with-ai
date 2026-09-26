#!/usr/bin/env python3
"""Render the vault guide (markdown) as a styled, standalone HTML page.

Author: Ibrahim AbuAlhaol

Usage:
    python3 build_guide.py [guide.md] [out.html]

Defaults to guides/guide.md -> guides/guide.html in the skill. The bootstrapper
uses the same renderer to build the vault's GUIDE.html from
Systems/vault-guide.md, so the styled page always matches the guide the human
actually edited. Edit the markdown, never the HTML.

Supports the markdown the guide uses: headings, paragraphs, hard line breaks,
nested lists, tables, fenced code, blockquotes, rules, and inline code, bold,
italic, and links. No dependencies.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
CALLOUT_RE = re.compile(r"^\[!([A-Za-z][\w-]*)\]([+-]?)\s*(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")

CSS = """
:root { --bg:#fbfbfa; --fg:#1d1f21; --muted:#5f6368; --accent:#0b62c4; --soft:#e8f0fb;
  --border:#e1e3e6; --code:#f1f2f4; --panel:#ffffff; }
@media (prefers-color-scheme: dark) { :root { --bg:#16181b; --fg:#e4e6e9; --muted:#9aa0a6;
  --accent:#6fb1ff; --soft:#1c2d44; --border:#2c3035; --code:#22262b; --panel:#1c1f23; } }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.layout { display:grid; grid-template-columns: 250px minmax(0, 1fr); gap:40px;
  max-width:1180px; margin:0 auto; padding:32px 24px 80px; }
nav { position:sticky; top:24px; align-self:start; max-height:calc(100vh - 48px); overflow:auto;
  font-size:14px; }
nav p { margin:0 0 8px; font-weight:600; color:var(--muted); text-transform:uppercase;
  letter-spacing:.06em; font-size:12px; }
nav a { display:block; padding:4px 10px; border-left:2px solid var(--border); color:var(--fg);
  text-decoration:none; }
nav a:hover { border-color:var(--accent); color:var(--accent); }
main { min-width:0; }
h1 { font-size:2rem; line-height:1.2; margin:0 0 16px; }
h2 { font-size:1.45rem; margin:48px 0 12px; padding-bottom:6px; border-bottom:1px solid var(--border); }
h3 { font-size:1.15rem; margin:28px 0 8px; }
h4 { font-size:1rem; margin:20px 0 6px; }
a { color:var(--accent); }
code { background:var(--code); padding:.1em .35em; border-radius:4px; font-size:.9em;
  font-family: ui-monospace, "SF Mono", Consolas, monospace; }
pre { background:var(--code); padding:14px 16px; border-radius:8px; overflow-x:auto; line-height:1.45; }
pre code { background:none; padding:0; }
blockquote { margin:16px 0; padding:10px 16px; background:var(--soft); border-left:4px solid var(--accent);
  border-radius:0 8px 8px 0; }
blockquote p { margin:6px 0; }
.callout { --c:#448aff; margin:16px 0; padding:10px 16px; border-left:4px solid var(--c);
  border-radius:0 8px 8px 0; background:color-mix(in srgb, var(--c) 10%, transparent); }
.callout p { margin:6px 0; }
.callout-title { font-weight:600; color:var(--c); margin:2px 0 6px; }
details.callout > summary { cursor:pointer; }
.callout[data-callout="summary"], .callout[data-callout="tldr"] { --c:#00b8d4; }
.callout[data-callout="important"] { --c:#7c4dff; }
.callout[data-callout="tip"] { --c:#00bfa5; }
.callout[data-callout="example"] { --c:#9c6ade; }
.callout[data-callout="warning"] { --c:#f57c00; }
.callout[data-callout="question"] { --c:#e6a700; }
.callout[data-callout="quote"] { --c:#8a8f98; }
.callout[data-callout="todo"] { --c:#2979ff; }
table { border-collapse:collapse; width:100%; margin:12px 0 20px; font-size:15px; display:block; overflow-x:auto; }
th, td { border:1px solid var(--border); padding:7px 10px; text-align:left; vertical-align:top; }
th { background:var(--panel); }
hr { border:0; border-top:1px solid var(--border); margin:36px 0; }
ul, ol { padding-left:24px; }
li { margin:3px 0; }
.stamp { color:var(--muted); font-size:13px; margin-top:48px; }
@media (max-width: 860px) { .layout { grid-template-columns: 1fr; gap:16px; padding:20px 16px 60px; }
  nav { position:static; max-height:none; } }
"""


def slug(text: str, seen: dict[str, int]) -> str:
    """GitHub-style heading anchor, so links like #file-naming keep working."""
    base = re.sub(r"[^\w\- ]", "", text.lower()).strip().replace(" ", "-")
    n = seen.get(base, 0)
    seen[base] = n + 1
    return base if n == 0 else f"{base}-{n}"


def inline(text: str) -> str:
    codes: list[str] = []

    def stash(m: re.Match) -> str:
        codes.append(f"<code>{html.escape(m.group(2).strip())}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"(`+)(.+?)\1", stash, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def starts_block(line: str) -> bool:
    return bool(
        FENCE_RE.match(line) or HEADING_RE.match(line) or HR_RE.match(line)
        or LIST_RE.match(line) or line.lstrip().startswith((">", "|"))
    )


def render_list(lines: list[str]) -> str:
    first = LIST_RE.match(lines[0])
    indent = len(first.group(1))
    tag = "ol" if first.group(2)[0].isdigit() else "ul"
    items: list[list[str]] = []
    for line in lines:
        match = LIST_RE.match(line)
        if match and len(match.group(1)) <= indent:
            items.append([match.group(3)])
        elif items:
            items[-1].append(line)

    parts = []
    for head, *rest in items:
        text, j = [head], 0
        while j < len(rest) and rest[j].strip() and not LIST_RE.match(rest[j]):
            text.append(rest[j].strip())
            j += 1
        nested = [line for line in rest[j:] if line.strip()]
        body = inline(" ".join(text))
        if nested and LIST_RE.match(nested[0]):
            body += render_list(nested)
        parts.append(f"<li>{body}</li>")
    return f"<{tag}>" + "".join(parts) + f"</{tag}>"


def render_table(lines: list[str]) -> str:
    def cells(line: str) -> list[str]:
        line = line.strip()
        line = line[1:] if line.startswith("|") else line
        line = line[:-1] if line.endswith("|") else line
        return [c.strip() for c in line.split("|")]

    head = "".join(f"<th>{inline(c)}</th>" for c in cells(lines[0]))
    rows = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(line)) + "</tr>"
        for line in lines[2:]
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"


def render_callout(match: re.Match, body: list[str], seen, toc) -> str:
    """An Obsidian callout (`> [!type]+ Title`) as a card; +/- make it foldable."""
    kind, fold, title = match.group(1).lower(), match.group(2), match.group(3).strip()
    heading = inline(title) if title else kind.capitalize()
    inner = render_blocks(body, seen, toc)
    if fold:
        opened = " open" if fold == "+" else ""
        return (
            f'<details class="callout" data-callout="{kind}"{opened}>'
            f'<summary class="callout-title">{heading}</summary>{inner}</details>'
        )
    return (
        f'<div class="callout" data-callout="{kind}">'
        f'<p class="callout-title">{heading}</p>{inner}</div>'
    )


def render_blocks(lines: list[str], seen: dict[str, int], toc: list[tuple[str, str]]) -> str:
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if FENCE_RE.match(line):
            j = i + 1
            while j < len(lines) and not FENCE_RE.match(lines[j]):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1 : j])) + "</code></pre>")
            i = j + 1
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level, text = len(heading.group(1)), heading.group(2)
            anchor = slug(text, seen)
            if level == 2:
                toc.append((anchor, text))
            out.append(f'<h{level} id="{anchor}">{inline(text)}</h{level}>')
            i += 1
            continue

        if HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        if line.lstrip().startswith(">"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith(">"):
                j += 1
            inner = [re.sub(r"^\s*>\s?", "", l) for l in lines[i:j]]
            callout = CALLOUT_RE.match(inner[0])
            if callout:
                out.append(render_callout(callout, inner[1:], seen, toc))
            else:
                out.append("<blockquote>" + render_blocks(inner, seen, toc) + "</blockquote>")
            i = j
            continue

        if line.lstrip().startswith("|") and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            out.append(render_table(lines[i:j]))
            i = j
            continue

        if LIST_RE.match(line):
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                if LIST_RE.match(nxt) or (nxt.strip() and nxt[:1].isspace()):
                    j += 1
                elif not nxt.strip() and j + 1 < len(lines) and (
                    LIST_RE.match(lines[j + 1]) or lines[j + 1][:1].isspace()
                ):
                    j += 1
                else:
                    break
            out.append(render_list(lines[i:j]))
            i = j
            continue

        j = i
        para = []
        while j < len(lines) and lines[j].strip() and (j == i or not starts_block(lines[j])):
            para.append(lines[j])
            j += 1
        text = "\n".join(para)
        text = re.sub(r" {2,}\n", "\x01", text).replace("\n", " ")
        text = inline(text).replace("\x01", "<br>")
        out.append(f"<p>{text}</p>")
        i = j
    return "\n".join(out)


def render(markdown: str, stamp: str = "") -> str:
    """The whole page. `stamp` becomes an HTML comment and a footer line."""
    lines = markdown.replace("\r\n", "\n").split("\n")
    title = next(
        (m.group(2) for m in map(HEADING_RE.match, lines) if m and len(m.group(1)) == 1),
        "Vault Guide",
    )
    toc: list[tuple[str, str]] = []
    body = render_blocks(lines, {}, toc)
    nav = "".join(f'<a href="#{a}">{inline(t)}</a>' for a, t in toc)
    comment = f"<!-- {html.escape(stamp)} -->\n" if stamp else ""
    footer = f'<p class="stamp">{html.escape(stamp)}</p>' if stamp else ""
    return (
        f"<!DOCTYPE html>\n{comment}<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{html.escape(re.sub(r'[*`]', '', title))}</title>\n<style>{CSS}</style>\n</head>\n"
        f"<body>\n<div class=\"layout\">\n<nav><p>Contents</p>{nav}</nav>\n"
        f"<main>\n{body}\n{footer}\n</main>\n</div>\n</body>\n</html>\n"
    )


REPO_STAMP = "generated by scripts/build_guide.py from guides/guide.md; edit the markdown, then re-run it"


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    source = Path(argv[1]) if len(argv) > 1 else root / "guides" / "guide.md"
    target = Path(argv[2]) if len(argv) > 2 else source.with_suffix(".html")
    stamp = REPO_STAMP if len(argv) <= 1 else f"generated by build_guide.py from {source.name}"
    target.write_text(render(source.read_text(encoding="utf-8"), stamp), encoding="utf-8")
    print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
