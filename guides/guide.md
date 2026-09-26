# Obsidian AFPISH Vault — Folder & Tag Charter

**Version:** 1.1  
**Last Updated:** 2026-09-25  
**Purpose:** Define folder hierarchy and tag structure for agent-compliant, retrieval-optimized knowledge management.

> **Make this guide yours before you bootstrap.** This file ships with the
> LLM-wiki skill as `guides/guide.md`. The values below — areas, people, places,
> time windows — are the author's own. Edit them to match your life and work,
> *then* run `init_vault.py`: it copies this guide into your vault as
> `Systems/vault-guide.md` and creates every folder listed under
> [Folder Hierarchy](#folder-hierarchy). After that, the vault copy is the one
> that counts — edit it in Obsidian, and re-run the bootstrapper to create any
> folders you add.
>
> Both you and your agent follow this guide: you when capturing and reviewing,
> the agent whenever it writes a note. Keep it short enough that both actually
> read it.

---

## Overview

This vault organizes notes by **folder (source/purpose)** and **tags (relationships/metadata)**.

- **Folders** answer: "Where should this live?" (context, source, processing stage)
- **Tags** answer: "What is this about?" and "What does it relate to?" (relationships, lifecycle, priorities)

Folders and tags are **orthogonal**—a note's folder location is independent of its tags.

---

## Folder Hierarchy

```
/Daily
  └─ Daily captured notes (process weekly into other folders)

/Fleeting
  └─ Quick inbox (temporary, process regularly)

/Areas
  /Areas/Day-Job
  /Areas/Side-Business
  /Areas/Family-Projects
  /Areas/Open-Source
  /Areas/Study
  └─ Active projects/domains; long-lived work

/Concepts
  └─ Reusable reference material (patterns, principles, frameworks)
  └─ Timeless or cross-project ideas

/raw
  └─ External sources, saved verbatim (papers, links, captures)
  └─ Immutable once saved; the LLM-wiki skill files them by topic

/wiki
  └─ Compiled knowledge articles, owned by the agent (see SKILL.md)
  └─ Ready for active use and agent queries

/Systems
  └─ Meta-notes (this charter, MOCs, indices, process documentation)

/Archive
  └─ Completed projects, retired work (not active)
```

The bootstrapper creates every folder in the block above: each line that starts
with `/` is a folder path. Keep that shape when you edit it — one path per
line, descriptions on `└─` lines.

### Adding New Folders

New top-level folders should be rare. If needed:
1. Ask: "Is this a **source** (raw), a **stage** (Daily), an **active area** (Areas), or **meta** (Systems)?"
2. Document in `/Systems/vault-structure.md`
3. Update this guide

New sub-folders under `/Areas` are fine—add one per active project.

---

## Tag Charter

Each note receives tags from multiple facets. **All tag prefixes are lowercase and hyphenated** (e.g., `#afpish/spirit`, not `#Afpish/Spirit`).

### Facet: Life Balance (AFPISH)

Captures which life domain(s) this note serves. Apply 1–3 per note.

| Tag | Meaning |
|-----|---------|
| `#afpish/spirit` | Spiritual integrity, principles, intellectual grounding |
| `#afpish/family` | Family commitments, relationships, parenting |
| `#afpish/professional` | Work, career, consulting |
| `#afpish/independence` | Autonomy, self-directed projects, side ventures |
| `#afpish/social` | Community, networks, relationships beyond family |
| `#afpish/health` | Physical, mental, energy management |

### Facet: Status

Lifecycle state of the note. Apply exactly 1 per note.

| Tag | Meaning |
|-----|---------|
| `#status/start` | Not yet begun (outline, idea stage) |
| `#status/progress` | Active work in progress |
| `#status/complete` | Finished, polished, ready for use |
| `#status/archived` | Superseded or no longer relevant |

**Note:** Status is independent of folder. A `/wiki` article can be `#status/progress` (still thin, awaiting sources) or `#status/complete` (well covered).

### Facet: Urgency

Priority signal relative to time. Apply 1 per note.

| Tag | Meaning |
|-----|---------|
| `#urgency/critical` | Blocks something; must move this week |
| `#urgency/high` | Important for direction; target this month |
| `#urgency/medium` | Worth attention; address this quarter |
| `#urgency/low` | Backlog; no deadline |

### Facet: Time Window

When this note is relevant. Apply 1 per note. Quarters/years are flexible—adjust to your planning horizon.

| Tag | Meaning |
|-----|---------|
| `#time/immediate` | This week or today |
| `#time/q4-2026` | This quarter |
| `#time/2027` | This year |
| `#time/ongoing` | Standing, no endpoint |
| `#time/archived` | No longer on the calendar |

### Facet: Type

What kind of note this is (for agent parsing). Apply as needed.

| Tag | Meaning |
|-----|---------|
| `#type/paper` | Academic or research paper |
| `#type/tool` | Software/tool evaluation or setup |
| `#type/code` | Code snippet, implementation, script |
| `#type/decision` | Decision log, choice made |
| `#type/project-log` | Status update, progress note |
| `#type/moc` | Map of Content (index/outline) |
| `#type/daily` | Daily capture/journal |

### Facet: People

Key stakeholders or collaborators (avoid tagging every person—just key contacts). Add as needed.

| Tag | Meaning |
|-----|---------|
| `#people/jane-doe` | Key collaborator (example; replace with your own) |
| `#people/team-work` | Your work team |
| `#people/partner` | Partner or spouse |
| `#people/family` | Family members (group tag) |

**Extending:** Add `#people/<name>` for new key contacts.

### Facet: Places

Geographic or organizational context. Add as needed.

| Tag | Meaning |
|-----|---------|
| `#places/home-city` | Your home city |
| `#places/abroad` | Travel or international work |
| `#places/office` | Your workplace |
| `#places/home` | Home, personal space |

**Extending:** Add `#places/<location>` for new geographic contexts.

---

## Tag Application Examples

### Example 1: Side Business Plan (in `/Areas/Side-Business`)

```
# Side Business — Q4 2026 Plan

Tags: #afpish/independence #afpish/professional #status/progress #urgency/high #time/q4-2026 #type/decision #people/jane-doe #places/abroad
```

**Why these tags?**
- `#afpish/independence` + `#afpish/professional`: Spans both autonomy and career
- `#status/progress`: Actively being refined
- `#urgency/high`: Affects near-term direction
- `#time/q4-2026`: Needed this quarter
- `#type/decision`: Capturing a strategic choice
- `#people/jane-doe`: Involves a key collaborator
- `#places/abroad`: Geographic context

---

### Example 2: Wiki Article Compiled from a Paper (in `/wiki/machine-learning`)

```
# Transformer Architecture

Tags: #type/paper #afpish/professional #status/progress #urgency/medium #time/q4-2026
```

**Why these tags?**
- `#type/paper`: Compiled from a research paper
- `#afpish/professional`: Professional development
- `#status/progress`: One source so far; more to ingest
- `#urgency/medium`: Worth reading, no immediate deadline
- `#time/q4-2026`: Targeting this quarter for completion

---

### Example 3: Family Project Build Log (in `/Areas/Family-Projects`)

```
# Build Log — Week of Sept 22, 2026

Tags: #afpish/family #afpish/independence #status/progress #time/immediate #type/project-log #urgency/medium
```

**Why these tags?**
- `#afpish/family`: It's family-focused
- `#afpish/independence`: Child autonomy & learning
- `#status/progress`: Ongoing build
- `#time/immediate`: Active work this week
- `#type/project-log`: Status/progress capture
- `#urgency/medium`: Important but not blocking

---

## Guidelines for Humans

### Daily Workflow

1. **Capture** (`/Daily` or `/Fleeting`): Minimal tags, just capture
2. **Weekly Review**: Move to appropriate folder + add full tag set
3. **Status Updates**: Change `#status/` tag as work progresses
4. **Synthesis**: Drop sources into `/raw` (or paste a URL) and ask the agent to ingest them — it compiles `/wiki` for you. Your own polished thinking goes to `/Concepts`

### Tag Discipline

- **Apply all mandatory facets** per note: AFPISH (1–3), Status (1), Urgency (1), Time (1)
- **Add optional facets** (Type, People, Places) when relevant
- **Keep tag values consistent**: Use the values in the charter, not variations
- **Monthly cleanup**: Archive stale `#status/progress` notes or update time windows

### Evolving the System

**To add a value to an existing facet:**
1. Add it to this guide
2. Update `/Systems/vault-structure.md`
3. Use it going forward (no migration needed)

**To add a new facet:**
1. Define its purpose and values
2. Document it in this guide
3. Discuss with yourself (or team) before rolling out
4. Update `/Systems/vault-structure.md`

---

## Guidelines for Agents

### Working with the LLM-Wiki Skill

This guide covers the whole vault; `SKILL.md` covers `raw/` and `wiki/`. Where
they overlap, `SKILL.md` wins on structure (file names, topic directories,
metadata blockquotes, the index and log) and this guide wins on tags.

- **Read this guide before writing any note**, and re-read it when the human
  says it changed.
- **Wiki articles** get the tag facets below as YAML frontmatter above the H1,
  written without `#` (`tags: [afpish/professional, status/progress, ...]`).
  Keep the `> Sources:` / `> Raw:` / `> Updated:` blockquotes exactly as
  `SKILL.md` specifies.
- **`raw/` files are never tagged** — they are immutable source copies.
  `wiki/index.md` and `wiki/log.md` are not tagged either.
- **Notes outside `raw/` and `wiki/`** (Daily, Areas, Concepts, ...) are the
  human's. Create or edit them only when asked, and then follow this guide's
  folders and tags.
- **Only use values listed here.** If a note needs a tag value or folder the
  guide does not have, propose adding it to the guide instead of inventing it.

### Query Patterns (Obsidian Dataview/CLI)

**Find all active work in a life domain:**
```
#afpish/independence AND #status/progress
```

**Find high-urgency items this quarter:**
```
#urgency/critical AND #time/q4-2026
```

**Find all papers being read:**
```
#type/paper AND #status/progress
```

**Find everything related to a person:**
```
#people/jane-doe
```

**Find completed notes by domain:**
```
#afpish/professional AND #status/complete
```

### Tag Parsing Rules

- **Tag format:** Always `#facet/value` (lowercase, hyphenated)
- **Facets are prefixed:** `afpish`, `status`, `urgency`, `time`, `type`, `people`, `places`
- **Multiple tags per facet are rare** except for AFPISH (which can have 1–3)
- **Tag values are canonical:** Check this guide for exact spellings
- **Folders are paths:** `/Daily`, `/Areas/Side-Business`, etc. (use as context)

### Compliance Expectations

When querying this vault, expect (except in `raw/`, `wiki/index.md` and `wiki/log.md`):
- Every note has exactly 1 `#status/*` tag
- Every note has exactly 1 `#urgency/*` tag
- Every note has exactly 1 `#time/*` tag
- Every note has 1–3 `#afpish/*` tags
- Optional tags (`#type/*`, `#people/*`, `#places/*`) are present as relevant
- Folder structure mirrors active areas and processing stages

If a note violates these rules, it needs retagging.

---

## Maintenance

### Monthly

- Review `/Daily` for stragglers; move or archive
- Spot-check `/Areas/` notes for correct status/urgency
- Update `#time/*` tags for next quarter if crossing a boundary

### Quarterly

- Regenerate MOCs in `/Systems` (the agent keeps `wiki/index.md` current on its own)
- Review `/Archive` to see if anything should be revived
- Update this guide with lessons learned or new facets

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-09-25 | Initial charter: AFPISH + Status + Urgency + Time + Type + People + Places |
| 1.1 | 2026-09-25 | Aligned with the LLM-wiki skill: lowercase `raw/` and `wiki/`, customize-before-bootstrap note, agent rules for the skill |

---

## See Also

- `raw/` and `wiki/` rules — the LLM-wiki skill's `SKILL.md` (in the vault's hidden `.claude/skills/` directory)
- `/Systems/vault-structure.md` — Implementation details and folder setup
- `/Systems/tag-examples.md` — Real examples from your vault
- `/Systems/agent-queries.md` — Common agent query patterns
