# Obsidian conventions

The skill was written for a plain folder of markdown. Running it inside an
Obsidian vault mostly just works, but four things need a decision. Paste the
parts you want into your copy of `SKILL.md` so the rules travel with the skill.

## 1. Keep markdown links, not wikilinks

Obsidian resolves both `[Title](../topic/article.md)` and `[[Title]]`. Use
markdown links only.

Lint parses link syntax directly — the internal-link, Raw-reference and See Also
checks (SKILL.md "Safe Fixes") all match markdown link targets, and
`scripts/check_evidence.py` resolves `> Raw:` links to locate the source files.
Wikilinks are invisible to all of it, so a vault written in wikilinks silently
loses every grounding and link check the skill provides.

In Obsidian: Settings → Files & Links → **"Use [[Wikilinks]]" off**, and set
**"New link format" to "Relative path to file"**. That makes links Obsidian
creates by hand match what the skill writes.

## 2. Metadata is blockquotes; add frontmatter only for tags

Articles carry metadata as blockquote lines (`> Sources:`, `> Raw:`,
`> Updated:`). Obsidian's Properties panel does not read those — it reads YAML
frontmatter. Do not convert the blockquotes: `check_evidence.py` matches them
with `^>\s*(Sources?|Raw|Collected|Published|Updated|Archived):`, and the lint
rules for Updated dates and the archive-page exemption depend on them.

If you want Obsidian tags and search properties, add YAML frontmatter *above*
the blockquotes. The two coexist; nothing in the skill parses the frontmatter.

```markdown
---
tags: [ai-coding-tools, terminal]
---

# Ghostty

> Sources: Example, 2026-04-16
> Raw: [ghostty](../../raw/ai-coding-tools/2026-04-17-ghostty.md)
> Updated: 2026-04-17
```

Suggested rule to add to SKILL.md, if you want tags maintained:

> Every wiki article carries YAML frontmatter with a `tags:` list. The first tag
> is the article's topic directory. Add tags only from the taxonomy in
> `wiki/index.md`; propose new ones to the user rather than inventing them.

## 3. Attachments must not land in `raw/` or `wiki/`

By default Obsidian saves pasted images next to the note. An image dropped into
a wiki article lands in `wiki/<topic>/` and lint's index-consistency check then
reports it as a file missing from the index; one dropped into `raw/` shows up as
an unreferenced raw file. Both are false positives that recur on every lint.

In Obsidian: Settings → Files & Links → **"Default location for new
attachments" → "In the folder specified below"** → `assets`.

`assets/` sits outside both trees, so neither lint category sees it.

## 4. Web Clipper should write the raw template

The Obsidian Web Clipper defaults to YAML frontmatter, but `raw/` files use the
blockquote header in `references/raw-template.md`. The skill reads raw files as
plain text when verifying quotes and numbers, so a mismatched header does not
break grounding — but it does mean your clipped files and the agent's files look
different, and the agent has to infer the source URL from an unexpected place.

Configure the clipper to match. In Web Clipper settings → Templates:

- **Note location**: `raw/{{date:YYYY}}-unsorted` — clip into a holding folder
  and let the agent file it into the right topic on ingest. Clipping straight
  into a topic directory works too, but then you are doing the triage by hand.
- **Note name**: `{{date:YYYY-MM-DD}}-{{title|slugify}}`
- **Template body**:

```
# {{title}}

> Source: {{url}}
> Collected: {{date:YYYY-MM-DD}}
> Published: {{published|date:"YYYY-MM-DD"|default:"Unknown"}}

{{content}}
```

That produces exactly the shape `references/raw-template.md` specifies, so a
clipped file and an agent-fetched file are indistinguishable.

If you use the holding folder, add this to SKILL.md:

> Before any ingest, check `raw/*-unsorted/` for clipped files. Treat each as an
> already-fetched source: skip the Fetch step, move the file into the correct
> topic directory, then run Triage and Compile normally.

## What does not need changing

- **Dot-directories.** Obsidian ignores any folder whose name starts with `.`,
  so `.claude/`, `.gemini/`, `.agents/` and `.hermes/` never appear in search, the file
  explorer, or the graph. The skill's own `SKILL.md`, `references/`, `examples/`
  and `tests/` stay out of your notes.
- **Tables in `wiki/index.md`.** Obsidian renders GitHub-flavored markdown
  tables natively; the index template needs no adaptation.
- **`wiki/log.md`.** Append-only and machine-parsed, but it is still a normal
  note. Fold it away in the file explorer if it clutters the sidebar.
