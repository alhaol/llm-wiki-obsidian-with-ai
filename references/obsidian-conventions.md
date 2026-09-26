# Obsidian conventions

> [!tip] The short version is in the vault guide
> The guide's **Obsidian Configuration** section (`Systems/vault-guide.md` in
> your vault) is the checklist to apply after bootstrapping and re-check after
> Obsidian updates. This file explains why each setting matters.

The skill was written for a plain folder of markdown. Running it inside an
Obsidian vault mostly just works, but five things need a decision. Paste the
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

Set **"Default location for new notes"** the same way, to `+`: notes you
create land in the inbox, and `/organize` names, tags, and files them. It is the
same folder Organize files attachments into, so pasted and organized files end
up together.

## 4. Web Clipper should write the raw template

The Obsidian Web Clipper defaults to YAML frontmatter, but `raw/` files use the
blockquote header in `references/raw-template.md`. The skill reads raw files as
plain text when verifying quotes and numbers, so a mismatched header does not
break grounding — but it does mean your clipped files and the agent's files look
different, and the agent has to infer the source URL from an unexpected place.

Configure the clipper to match. In Web Clipper settings → Templates:

- **Note location**: `+` — clip into the inbox and let `/organize` file it into
  the right raw/ topic and compile it. Clipping straight into a topic directory
  works too, but then you are doing the triage by hand.
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

Organize recognizes a clip by that header (`scripts/inbox.py` lists it as
`clip`) and moves it into raw/ as is, with no re-wrapping.

## 5. New notes should start with a convention name

Obsidian names new notes `Untitled`, and pasted images `Pasted image
20260926...png`. Neither follows the naming convention (SKILL.md, "Naming
Convention"), so lint will list them until they are renamed.

Rename a note as soon as you know what it is about
(`second_order_thinking_md.md`), or leave it and drop it into `+/` —
`/organize` names it for you. For pasted images, the "Paste image rename" or
similar community plugins can prompt for a name on paste. If you use the
Excalidraw plugin, set its drawing file name to something you will replace,
and keep the `.excalidraw.md` extension; the identifier is `excali`
(`login_flow_sketch_excali.excalidraw.md`).

## What does not need changing

- **Dot-directories.** Obsidian ignores any folder whose name starts with `.`,
  so `.claude/`, `.gemini/`, `.agents/` and `.hermes/` never appear in search, the file
  explorer, or the graph. The skill's own `SKILL.md`, `references/`, `examples/`
  and `tests/` stay out of your notes.
- **Tables in `wiki/index.md`.** Obsidian renders GitHub-flavored markdown
  tables natively; the index template needs no adaptation.
- **`wiki/log.md`.** Append-only and machine-parsed, but it is still a normal
  note. Fold it away in the file explorer if it clutters the sidebar.
