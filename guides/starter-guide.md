# Vault Guide — Starter

**Version:** 1.0  
**Last Updated:** 2026-09-26  
**Purpose:** A minimal folder, naming, and tag charter to grow from.

> **This is the starter guide.** It keeps only what every vault needs: a few
> folders, the naming convention, and four tag facets. Bootstrap with
> `init_vault.py --starter` to use it, then grow it in Obsidian
> (`Systems/vault-guide.md`): add areas as projects start, add tag values when
> you catch yourself wanting one. For a fuller example, see `guide.md` in the
> skill's `guides/` folder.
>
> Both you and your agent follow this guide. The agent reads it before every
> task and uses only the folders and tag values listed here.

---

## Overview

- **Folders** answer: "Where should this live?"
- **Names** answer: "What is this file, at a glance?"
- **Tags** answer: "What state is it in, and what kind of note is it?"

---

## Folder Hierarchy

```
/+
  └─ Inbox: drop anything here; /organize files it and empties it

/Daily
  └─ Notes tied to one day

/Fleeting
  └─ Rough ideas with no home yet

/Areas
  /Areas/Work
  /Areas/Personal
  └─ One folder per active area or project

/Concepts
  └─ Your own principles, patterns, and frameworks

/raw
  └─ Sources saved verbatim (agent-managed, never edited)

/wiki
  └─ Knowledge articles compiled from raw (agent-owned)

/Systems
  └─ This guide and other notes about the vault

/Archive
  └─ Finished or retired work

/assets
  └─ Images, PDFs, and other attachments
```

Each line starting with `/` is a folder; the bootstrapper creates them all.
Add `/Areas/<name>` lines as areas start, then re-run `init_vault.py`.

### Root Files

| File | Who writes it | Purpose |
|------|---------------|---------|
| `HOME.md` | You | Your front page: focus, key notes, what you are watching |
| `ME.md` | You | Who you are and how you want the agent to work |
| `GUIDE.html` | Nobody (generated) | This guide, styled for a browser; rebuilt from this file by `init_vault.py` |

The agent reads `HOME.md` and `ME.md` before every task and never edits them
without your explicit yes.

---

## File Naming

Every file outside `/raw` and `/+` is named from its content, then its type:

```
{word}_{word}[_{word}[_{word}[_{word}]]]_{identifier}.{extension}
```

- **Words**: 2 to 5, lowercase letters and digits, describing what the file is about
- **Identifier**: the extension (`md`, `png`, `pdf`, ...); Excalidraw drawings use `excali`
- **Daily notes** start with the date as three words: `2026_09_26_standup_md.md`

| Kind | Example |
|------|---------|
| Note | `weekly_review_process_md.md` |
| Image | `whiteboard_sketch_png.png` |
| PDF | `lease_agreement_pdf.pdf` |

**Exempt:** `/raw`, `/+`, dot-folders, and `HOME.md`, `ME.md`, `GUIDE.html`,
`Systems/vault-guide.md`, `wiki/index.md`, `wiki/log.md`.

---

## Tag Charter

Tags go in each note's frontmatter, written without `#`:
`tags: [status/active, urgency/medium, time/ongoing, type/reference]`.

### Facet: Status

Where the note is in its life. Apply exactly 1 per note.

| Tag | Meaning |
|-----|---------|
| `#status/draft` | Started, not finished |
| `#status/active` | In use or in progress |
| `#status/done` | Finished and stable |

### Facet: Urgency

How soon it needs attention. Apply 1 per note.

| Tag | Meaning |
|-----|---------|
| `#urgency/high` | This week |
| `#urgency/medium` | This month or quarter |
| `#urgency/low` | Someday |

### Facet: Time Window

When it is relevant. Apply 1 per note.

| Tag | Meaning |
|-----|---------|
| `#time/now` | Current work |
| `#time/ongoing` | No end date |
| `#time/past` | Kept for the record |

### Facet: Type

What kind of note it is. Apply as needed.

| Tag | Meaning |
|-----|---------|
| `#type/reference` | Knowledge to look things up in |
| `#type/project` | Plans, logs, and decisions for a project |
| `#type/idea` | An idea to develop |
| `#type/journal` | A daily or personal entry |

**Growing it:** add a value to a table above, or a new `### Facet:` section
with an "Apply ..." sentence. The agent picks it up on the next task.

---

## Guidelines for Agents

- Read this guide, `HOME.md`, and `ME.md` before every task.
- Use only the folders and tag values listed here. Map a stray tag to the value
  with the same meaning, or remove it. Propose additions to this guide rather
  than inventing values.
- Name every file you create, move, or rename by [File Naming](#file-naming),
  and rename only with `scripts/rename.py`.
- Everything you ingest or organize passes the skill's Compliance Gate before
  the task is done.
- Never edit `HOME.md` or `ME.md` without the human's explicit yes.

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-26 | Starter guide |
