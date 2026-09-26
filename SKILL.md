---
name: karpathy-llm-wiki
author: Ibrahim AbuAlhaol
description: "Use when building or maintaining a personal LLM-powered knowledge base. Triggers: ingesting sources into a wiki, fetching sources into raw/, organizing or emptying the + inbox, filing notes into the vault, querying wiki knowledge, linting wiki quality, '/ingest', '/fetch', '/organize', naming or renaming vault notes, callouts, HOME.md or ME.md, 'add to wiki', 'what do I know about', or any mention of 'LLM wiki' or 'Karpathy wiki'."
---

# Karpathy LLM Wiki

Build and maintain a personal knowledge base using LLMs. You manage two directories: `raw/` (immutable source material) and `wiki/` (compiled knowledge articles). Sources go into raw/, you compile them into wiki articles, and the wiki compounds over time. You also empty the `+/` inbox, where the human drops old files, notes, and assets: you file each item into raw/ (then compile it), into the human's own folders, or into `assets/`.

Core ideas from Karpathy:
- "The LLM writes and maintains the wiki; the human reads and asks questions."
- "The wiki is a persistent, compounding artifact."

## Architecture

Three layers, all under the user's project root:

**raw/** — Immutable source material. You read, never modify. Organized by topic subdirectories (e.g., `raw/machine-learning/`).

**wiki/** — Compiled knowledge articles. You have full ownership. Organized by topic subdirectories, one level only: `wiki/<topic>/<article>_md.md` (file names follow the Naming Convention below). Contains two special files:
- `wiki/index.md` — Global index. One row per article, grouped by topic, with link + summary + Updated date.
- `wiki/log.md` — Append-only operation log.

**+/** — The inbox. The human drops anything here: old notes, clipped pages, papers, images, exports. You own it only while running Organize, which moves every item out and leaves `+/` empty (just its `.gitkeep`). Nothing lives in `+/`.

**assets/** — Non-markdown attachments (images, PDFs, audio, office files), flat, one level. Obsidian saves pasted attachments here too (see `references/obsidian-conventions.md`).

**HOME.md** and **ME.md** — The human's two files at the vault root (see below). **GUIDE.html** — the vault guide rendered as a styled page at the root, for the human. The bootstrapper rebuilds it from `Systems/vault-guide.md` on every run; you never edit it (after the guide changes, suggest re-running `init_vault.py`).

**SKILL.md** (this file) — Schema layer. Defines structure and workflow rules.

Templates live in `references/` relative to this file. Read them when you need the exact format for raw files, articles, archive pages, or the index.

### Vault Guide

`Systems/vault-guide.md`, when it exists, is the vault's folder and tag charter. The human wrote it and follows it too. Read it before any Ingest, Organize, Archive, or Lint, and before writing any note outside raw/ and wiki/. How the two fit together:

- **This file wins on structure** in raw/ and wiki/: file names, topic directories, metadata blockquotes, index, log.
- **The guide wins on tags.** Give every new or updated wiki article (archive pages included) YAML frontmatter above the H1 with the guide's mandatory facets, written without `#` (for example, `tags: [afpish/professional, status/progress, urgency/medium, time/ongoing, type/paper]`). Never tag raw/ files, `wiki/index.md`, or `wiki/log.md`.
- **Use only values the guide lists, and clear the rest.** A tag the guide does not list (any spelling, case, or facet it does not define: `#work`, `#Status/Progress`, `#todo`) does not stay on a note you write or file. Map it to the guide's value when the meaning matches (`#paper` → `type/paper`, `#work` → `afpish/professional`); otherwise drop it. If a dropped value keeps coming up, propose adding it to the guide; do not invent one. The same holds for folders. Folders outside raw/ and wiki/ belong to the human: write there only when asked. Running Organize is that ask for the items in `+/`, and nothing else: it files them into those folders but never edits notes already there.
- **Organize tags the human's notes too.** Every markdown note Organize files outside raw/ gets the same mandatory facets in its frontmatter.
- During Lint, check the whole vault against the guide with `scripts/check_guide.py` (see Lint → Guide compliance).

If the guide is absent, skip all of this. Organize then files only into raw/ and assets/, and asks where everything else goes.

### HOME.md and ME.md

Two files at the vault root that the human writes and maintains. They are how you learn what the human cares about, and how you point their attention at what matters. Templates: `references/home-template.md`, `references/me-template.md`.

- **ME.md** — who the human is, their priorities, and their preferences for how you write, file, tag, and talk to them.
- **HOME.md** — their front page: current focus, key notes, areas, and topics they are watching.

Rules:

- **Read both before every workflow** (Ingest, Organize, Query, Archive, Lint), when they exist. Follow ME.md's preferences wherever this file leaves you a choice (summary style, how much to ask, language); this file and the vault guide still win on structure and tags.
- **Never modify either without the human's explicit yes**, given in chat for that specific change. Propose the exact lines instead. With a yes, append to ME.md or edit HOME.md exactly as proposed, nothing more. Approval does not carry over to the next change.
- **Surface, do not bury.** At the end of an Ingest, Organize, or Lint, add a short **Suggested for HOME.md** list when something deserves the human's attention: a new or heavily updated note that touches their Focus or Watching topics, or a note they will clearly return to. Give each as a ready-to-paste line with a relative link. When the human states a lasting preference in conversation, offer it as **Suggested for ME.md**. Skip both lists when there is nothing worth it; a padded list trains the human to ignore it.
- Never tag, rename, or move them. If either is missing, work without it and do not create it unasked (the bootstrapper creates both).

### Naming Convention

Every file you create, move, or rename outside `raw/` and `+/` is named:

```
{word}_{word}[_{word}[_{word}[_{word}]]]_{identifier}.{extension}
```

- **Words**: two to five, lowercase `a-z` and `0-9`, chosen from the content — what the note is about, not when it was made or where it came from. `transformer_attention_mechanism`, not `notes_about_stuff`.
- **Identifier**: the file's type, which is its extension: `md` for notes, `png`, `jpg`, `pdf`, `svg`, `mp3`, `canvas`, and so on. Excalidraw drawings use `excali` (`login_flow_sketch_excali.excalidraw.md`).
- **Daily notes** start with the date as three words: `2026_09_26_standup_md.md` (date plus one or two content words).
- **Collisions**: never overwrite. Pick more specific words first; add a number word only as a last resort (`attention_heads_2_md.md`).
- **Exempt**: `raw/` (sources keep Fetch's date-slug names), `+/` (transient), dot-directories, and the fixed files `HOME.md`, `ME.md`, `GUIDE.html`, `Systems/vault-guide.md`, `wiki/index.md`, `wiki/log.md`.

Examples: `wiki/machine-learning/transformer_architecture_md.md`, `Concepts/second_order_thinking_md.md`, `Areas/Side-Business/side_business_q4_plan_md.md`, `assets/garden_bed_layout_png.png`.

`scripts/check_names.py <project-root> [paths...]` checks names mechanically; run it on every file you name, and during Lint.

**Rename and move only with `scripts/rename.py`**, never by hand:

```
python3 <skill-dir>/scripts/rename.py <project-root> <old-path> <new-path> [--dry-run]
```

It moves the file and rewrites every link to it across the vault — relative markdown links and images, `[[wikilinks]]`, `![[embeds]]`, aliases and `#heading` anchors kept — plus the moved note's own relative links. It refuses to overwrite, and reports bare-name wikilinks it cannot safely change (another file has the same name); fix those by hand. A hand rename that misses one link breaks the vault silently.

### Callouts

Obsidian callouts (`> [!type] Title`) are how a note draws the eye to what matters, and they make notes easier to recall. Use the types the vault guide's **Callouts** table lists, and only those; without a guide, use `summary`, `important`, `tip`, `warning`, and `question`.

- **Every wiki article and archive page** opens its Overview with a `> [!summary]` callout: the takeaway in one to three sentences.
- **Elsewhere in an article**, add a callout only where a point needs extra attention: a key fact (`important`), a pitfall or a contradiction you want seen (`warning`), an open question (`question`). About three per note, at most; a note where everything is highlighted highlights nothing.
- **Write the title as the point itself** (`> [!important] Attention cost grows with the square of the context`), so the title alone works as a recall cue. Fold long ones with `-`.
- **Grounding still applies.** Numbers, dates, and quotes inside a callout must be located in the linked raw files like any other article text.
- **Placement.** Never put a callout between an article's H1 and its metadata blockquote, and keep a blank line after the metadata; `check_evidence.py` reads the first blockquote under the title as the metadata. Keep **Status: Outdated / Disputed** blocks as the plain blockquotes the article template shows.
- **raw/ never gets callouts**; its text is the source's.
- **The human's notes**: Organize may add one `> [!summary]` directly under the title of a `/Concepts` or `/Areas` note it files, as a new block above the untouched original text. Suggest any other callouts in the report instead of inserting them.

`scripts/check_guide.py` reports callout types the guide does not list, and `--strip` renames Obsidian's built-in aliases (`tldr` → `summary`, `hint` → `tip`, `caution` → `warning`, ...) to the listed type they stand for.

### Compliance Gate

Everything Ingest compiles into wiki/ and everything Organize files out of `+/` follows the system in full: the guide's folders, its tags, and the Naming Convention. It is not "later cleanup"; a workflow is not finished until its files pass the gate.

For the files a workflow wrote or moved (vault-relative paths):

1. **Tags.** Give each note outside raw/ its mandatory facets from the guide, mapping the note's existing tags where the meaning matches. Then clear everything else:
   ```
   python3 <skill-dir>/scripts/check_guide.py <project-root> <paths...> --strip
   ```
   It reads the allowed values, facet counts, folders, and callout types from the guide itself. `--strip` removes unlisted frontmatter tags, un-tags unlisted inline hashtags (the word stays, the `#` goes; a line of nothing but tags is removed), and in raw/ drops frontmatter tags and escapes inline hashtags to `\#`, which Obsidian renders the same but no longer indexes. It never adds tags.
2. **Check.** Run both checkers on the same paths and fix whatever they report — missing facets, a wrong folder, a bad name, an unlisted callout type — then run them again:
   ```
   python3 <skill-dir>/scripts/check_guide.py <project-root> <paths...>
   python3 <skill-dir>/scripts/check_names.py <project-root> <paths...>
   ```
3. **Report** the tags you mapped and dropped, grouped by value, in your final summary.

Both checks must exit 0. If one cannot pass without the human (a folder the guide lacks, say), stop and ask; do not leave the file half-compliant.

The gate never touches HOME.md, ME.md, or notes the workflow did not write.

### Initialization

Triggers only on the first Ingest. Check whether `raw/` and `wiki/` exist. Create only what is missing; never overwrite existing files:

- `raw/` directory (with `.gitkeep`)
- `wiki/` directory (with `.gitkeep`)
- `wiki/index.md` — heading `# Knowledge Base Index`, empty body
- `wiki/log.md` — heading `# Wiki Log`, empty body
- `+/` directory (with `.gitkeep`) and `assets/` directory

Organize also triggers this check. If Query or Lint cannot find the wiki structure, tell the user: "Run an ingest first to initialize the wiki." Do not auto-create.

## The Grounding Invariant

Every load-bearing fact in wiki/ — numbers, dates, direct quotes — exists verbatim in the raw/ files linked by that article's Raw field. Compile *establishes* this invariant (locate before you write); lint *verifies* it (`scripts/check_evidence.py` greps the high-signal literals — suffixed or large numbers, decimals, ISO dates, longer quotes — in the linked raws; the compile-time locate-before-write rule covers the rest). Because raw/ is immutable, a verified article stays verified; the script re-checks the whole wiki in seconds, so there is no incremental state to maintain.

---

## Commands

Four slash commands, installed into the vault by `scripts/init_vault.py` from this skill's `commands/` directory, map onto the workflows below. Every supported agent gets all four: command files for Claude Code (`.claude/commands/`), OpenCode (`.opencode/commands/`), Gemini CLI (`.gemini/commands/`, TOML) and Pi (`.pi/prompts/`), and a small skill per command for Hermes (`.hermes/skills/<command>/`). They are shortcuts; the same requests in plain words run the same workflows.

`commands/` is the single source. After changing it (or this skill), re-run `init_vault.py`: it refreshes every generated file (they carry a `generated by init_vault.py` stamp) in every agent and leaves unstamped files, the human's own, alone. Never hand-edit one agent's copy to change a command.

| Command | Runs | Writes |
|---|---|---|
| `/fetch <source>` | Ingest → Fetch only | raw/, log |
| `/ingest <source>` | Ingest, all steps. No argument: compile the backlog of unreferenced raw files | raw/, wiki/, index, log |
| `/organize [--dry-run] [+/paths]` | Organize | the destinations of `+/` items, index, log |
| `/vault-status` | `scripts/vault_status.py`: inbox, backlog, evidence, names, guide, and git in one summary, each with its next step | nothing |

---

## Ingest

Fetch a source into raw/, then compile it into wiki/ — unless the source adds nothing new. Always fetch; whether to compile depends on the triage below.

### Fetch (raw/)

1. Get the source content using whatever web or file tools your environment provides. If nothing can reach the source, ask the user to paste it directly.

2. Pick a topic directory. Check existing `raw/` subdirectories first; reuse one if the topic is close enough. Create a new subdirectory only for genuinely distinct topics.

3. Save as `raw/<topic>/YYYY-MM-DD-descriptive-slug.md`.
   - Slug from source title, kebab-case, max 60 characters.
   - Published date unknown → omit the date prefix from the file name (e.g., `descriptive-slug.md`). The metadata Published field still appears; set it to `Unknown`.
   - If a file with the same name already exists, append a numeric suffix (e.g., `descriptive-slug-2.md`).
   - Include metadata header: source URL, collected date, published date.
   - Preserve original text. Clean formatting noise. Do not rewrite opinions.
   - Carry no tags: drop any `tags:` frontmatter key, and escape inline hashtags as `\#` so Obsidian does not index the source's hashtags as vault tags (`check_guide.py --strip` does both).

   See `references/raw-template.md` for the exact format.

### Triage

After saving the raw file and before editing wiki/, search wiki/ with the source's key entities and synonyms, then state the disposition:

- **New** — creates one or more new articles.
- **Update** — merges into existing article(s).
- **Disputed** — contradicts existing content; may combine with New or Update (see Compile for conflict annotation).
- **No material** — adds no knowledge beyond what the wiki already holds. Keep the raw file, log it (see Post-Ingest), and stop. Do not force an article out of a thin source.

New, Update, and Disputed may be combined. No material is exclusive.

### Compile (wiki/)

Determine where the new content belongs:

- **Same core thesis as existing article** → Merge into that article. Add the new source to Sources/Raw. Update affected sections.
- **New concept** → Create a new article in the most relevant topic directory. Name the file after the concept, not the raw file, following the Naming Convention (`transformer_architecture_md.md`). Open its Overview with a `[!summary]` callout, and use other callouts where a point needs extra attention (see Callouts).
- **Spans multiple topics** → Place in the most relevant directory. Add See Also cross-references to related articles elsewhere.

These are not mutually exclusive. A single source may warrant merging into one article while also creating a separate article for a distinct concept it introduces. In all cases, check for factual conflicts: if the new source contradicts existing content, mark the contested claims with a **Status: Disputed** block (see `references/article-template.md`). When the conflicting content lives in separate articles, mark both and cross-link them.

**Source fidelity.** Every number, date, and direct quote must be located in the raw file (grep or read) *before* it is written; write the value exactly as found — if the source says 42K, write 42K, not 42,000. Derived values (sums, deltas, counts you computed) must show their components so each component is findable in raw. If you cannot locate a value, do not write its exact form; drop it or state it without precision.

See `references/article-template.md` for article format. Key points:
- Sources field: author, organization, or publication name + date, semicolon-separated.
- Raw field: markdown links to raw/ files, semicolon-separated.
- Relative paths from `wiki/<topic>/` use `../../raw/<topic>/<file>.md` (two levels up to project root).

### Cascade Updates

After the primary article, check for ripple effects. Do not rely on the index alone: search the full wiki for the source's key entities, aliases, and the claims it touches, then update every non-archive article whose content is materially affected. Each updated file gets its Updated date refreshed.

When the new source supersedes or contradicts an existing claim, keep the old claim for the record but mark it with a Status block (see `references/article-template.md`): **Outdated** when something newer replaces it, **Disputed** when sources disagree. Never silently rewrite history.

Archive pages are never cascade-updated (they are point-in-time snapshots).

### Post-Ingest

Run the Compliance Gate on the raw file and every article you created or updated: the articles' tags come from the guide only, their names from the Naming Convention, their folders are `wiki/<topic>/`.

Update `wiki/index.md`: add or update entries for every touched article. When adding a new topic section, include a one-line description. The Updated date reflects when the article's knowledge content last changed, not the file system timestamp. See `references/index-template.md` for format.

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] ingest | <primary article title>
- Disposition: <New; Update; Disputed>
- Raw: <raw file path>
- Updated: <cascade-updated article title>
```

Omit `- Updated:` lines when no cascade updates occur. For No material, log and stop. Use a project-root-relative raw path (for example, `raw/topic/file.md`):

```
## [YYYY-MM-DD] ingest | no material: <project-root-relative raw file path>
- Disposition: No material
```

The exact no-material heading is the machine-readable inventory key; the Disposition line remains required for a complete human-readable log entry.

### Research (multi-source ingest)

Use only when the user explicitly asks to research a topic or gather sources into the wiki. Ordinary knowledge questions go to Query, which never writes files.

1. Split the topic into a few angles. For each, search with a wide net — official names, abbreviations, and synonyms, not just the literal keywords.
2. For any core claim you expect to conclude, deliberately search the opposing side: failures, criticism, failed replications.
3. Save selected sources to raw/ as usual. Searching may run in parallel; compilation must not — compile one source at a time, because index.md, log.md, and cascade updates are shared state.

### Fetch only

When the user asks only to fetch or save a source (`/fetch`), run Fetch and stop: no Triage, no Compile, no index change. Append to `wiki/log.md`:

```
## [YYYY-MM-DD] fetch | <project-root-relative raw file path>
```

The raw file stays unreferenced, so Lint lists it as backlog until an Ingest compiles it. `/ingest` with no argument compiles the whole backlog: every unreferenced raw file, skipping Fetch.

---

## Organize

Empty the `+/` inbox: decide where each item belongs, move it there, tag it, compile whatever is knowledge, and leave `+/` empty. Triggers: `/organize`, "organize the inbox", "file what's in +", "clean up +".

The inbox holds a mix: the human's own old notes, clipped articles, papers, exports from other apps, images. Nothing stays and nothing is lost. Items only move, except exact duplicates (step 1).

### 1. Inventory

Read the vault guide, then run:

```
python3 <skill-dir>/scripts/inbox.py list <project-root>
```

**Commit first.** If the output starts with an uncommitted-changes warning, stop and offer to commit the vault as it is (`git add -A` and `git commit -m "Snapshot before organize"`), so the whole run can be undone with one `git revert`. Commit only with the human's yes; if they decline, go on. If the vault is not a git repo, say that the run cannot be undone with git, and go on only with their yes.

It lists every file under `+/` (dotfiles skipped) with a first-guess kind — `clip` (markdown that already has the raw header), `note` (other markdown), `asset` (everything else) — and flags byte-identical duplicates of files already in the vault. Read every note and clip before classifying it; the kind is a hint, not a verdict. Duplicates are the one thing Organize deletes: remove them from `+/` and list them in the log.

### 2. Classify

Give each item exactly one destination. Decide by what the content *is*, not by how the human happened to write it:

| Destination | What belongs there |
|---|---|
| `raw/<topic>/` | Knowledge from outside the human's head: clipped or copied articles, paper text, docs, transcripts, someone else's post — and the human's notes *about* such material (reading, lecture, or course notes). Compiled into wiki/ in step 4. |
| `Daily/` | A capture tied to one day: journal entry, day log, the day's meeting notes. Needs a date from the note itself (file name, heading, or frontmatter). No date in the note → not Daily. |
| `Fleeting/` | Rough, unfinished thoughts and scraps with no clear home yet. |
| `Areas/<area>/` | Work on an active project or domain the guide lists: plans, decisions, logs, specs. |
| `Concepts/` | The human's own distilled idea: a principle, pattern, framework, or mental model, reusable across projects. |
| `Systems/` | Notes about the vault itself: MOCs, processes, conventions. |
| `Archive/` | Material from a finished or abandoned project. |
| `assets/` | Every non-markdown file. A PDF or document that is a *source* also gets a raw/ extract (step 3). |

Never file straight into wiki/: wiki articles come only from Compile. Use the guide's folder list; if an item needs a folder the guide lacks (a new area, say), propose adding it rather than creating it.

When the right destination is genuinely unclear, do not guess. Collect every unclear item and ask about all of them in one question, with your best suggestion for each. Everything you are sure about can proceed.

### 3. Plan, then file

Show the plan as a table — item, destination path, tags, and for raw items the topic — before moving anything. With `--dry-run`, stop here.

Then file in this order, so links can be rewritten against final paths:

1. **Assets** → `assets/`, renamed to the Naming Convention after what the file shows or contains (`IMG_2041.jpg` → `garden_bed_layout_jpg.jpg`).
2. **Human notes** (Daily, Fleeting, Areas, Concepts, Systems, Archive):
   - File name: renamed to the Naming Convention from the content (`Untitled 3.md` → `pricing_experiment_ideas_md.md`). Keep the human's words when they already describe the note. Daily notes start with their date: `2026_09_20_client_call_md.md`.
   - Body: keep it verbatim. Only fix links (below).
   - Frontmatter: add the guide's mandatory facets as `tags:` (values only from the guide), merged into any frontmatter already there. Existing tags the guide lists stay; the rest are mapped to guide values or cleared by the Compliance Gate, frontmatter and inline alike.
   - Callouts: `/Concepts` and `/Areas` notes may get one `> [!summary]` under the title (see Callouts); nothing else in the body changes. Callouts already in the note keep their text; an alias type is renamed to the listed type by the Compliance Gate.
3. **Raw items** → `raw/<topic>/`, following Fetch's naming and topic rules:
   - Raw files keep Fetch's date-slug names, not the Naming Convention.
   - A clip that already has the raw header: move it as is.
   - Other text: wrap it in the raw template. Source is the origin if the text names one; otherwise `Inbox file: <original file name>` (add `personal notes` when the human wrote them). Published is the source's date, or `Unknown`. Preserve the text.
   - A source document in assets/ (a PDF paper, say): extract its text into a raw file whose Source links to the asset, for example `[paper.pdf](../../assets/paper.pdf)`.
   - Never tag raw files: strip any tags the clip or note carried (Fetch's rule).

**Moves.** File every item with `scripts/rename.py <project-root> +/<item> <destination>` (see Naming Convention). Nearly every item is renamed, and the script rewrites every link to it, between inbox items and from the rest of the vault, plus the item's own relative links. Resolve anything it reports as left unchanged. In raw files, fix only paths, never text.

**Collisions.** Never overwrite. In raw/, append a numeric suffix as Fetch does; elsewhere, follow the Naming Convention's collision rule. Then run `scripts/check_names.py` on the paths you wrote and fix anything it reports.

### 4. Compile

Run Triage, Compile, Cascade Updates, and Post-Ingest for each new raw file, one at a time, exactly as in Ingest. No-material items stay in raw/ and are logged as usual.

### 5. Close out

Append to `wiki/log.md`, before the ingest entries it caused:

```
## [YYYY-MM-DD] organize | <N> items from +/
- <destination path> <- +/<original path>
- Duplicate removed: +/<path> (same as <vault path>)
```

One `<-` line per filed item, raw ones included. Run the Compliance Gate on every filed path (step 4 already gated the wiki articles). Then run:

```
python3 <skill-dir>/scripts/inbox.py finish <project-root>
```

It removes empty subfolders of `+/`, keeps `+/.gitkeep`, and fails if any file remains. Organize is done only when it reports `+/ is empty`. If something is left because you are waiting on the human's answer, say so and list it. When Organize was scoped to specific paths, skip `finish` and report only those items.

End with **Suggested for HOME.md** (see HOME.md and ME.md) when something you filed deserves the human's attention, and offer to commit the run (`git commit -m "Organize +/: <N> items"`); commit only with a yes.

---

## Query

Search the wiki and answer questions. Examples of triggers:
- "What do I know about X?"
- "Summarize everything related to Y"
- "Compare A and B based on my wiki"

### Steps

1. Read `wiki/index.md` to locate candidate articles, then full-text search wiki/ with the topic's key terms *and their synonyms*. Never claim the wiki has no relevant content until both the index and the full-text search come back empty — and say that you searched.
2. Read the articles you found and synthesize an answer.
3. Prefer wiki content over your own training knowledge. Cite sources with markdown links: `[Article Title](wiki/topic/article.md)` (project-root-relative paths for in-conversation citations; within wiki/ files, use paths relative to the current file).
4. Output the answer in the conversation. Do not write files unless asked.

### Archiving

When the user explicitly asks to archive or save the answer to the wiki:

1. Write the answer as a new wiki page. See `references/archive-template.md`. When converting conversation citations to the archive page, rewrite project-root-relative paths (e.g., `wiki/topic/article.md`) to file-relative paths (e.g., `../topic/article.md` or `article.md` for same-directory).
   - Sources: markdown links to the wiki articles cited in the answer.
   - No Raw field (content does not come from raw/).
   - File name reflects the query topic and follows the Naming Convention, e.g., `transformer_architectures_overview_md.md`.
   - Place in the most relevant topic directory.
2. Always create a new page. Never merge into existing articles (archive content is a synthesized answer, not raw material).
3. Run the Compliance Gate on the new page (guide tags, Naming Convention, `wiki/<topic>/`).
4. Update `wiki/index.md`. Prefix the Summary with `[Archived]`.
5. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] query | Archived: <page title>
   ```

---

## Lint

Quality checks on the wiki. Three categories with different authority levels.

### Safe Fixes (auto-fix)

Fix these automatically:

**Index consistency** — compare `wiki/index.md` against actual wiki/ files (excluding index.md and log.md):
- File exists but missing from index → add entry with `(no summary)` placeholder. For Updated, use the article's metadata Updated date if present (for archive pages, the Archived date); otherwise fall back to file's last modified date.
- Index entry points to nonexistent file → mark as `[MISSING]` in the index. Do not delete the entry; let the user decide.
- Index entry's Updated differs from the article's metadata Updated (or Archived, for archive pages) → update the index entry to match the article.

**Internal links** — for every markdown link in wiki/ article files (body text and Sources metadata), excluding Raw field links (validated by Raw references below), excluding See Also section links (handled by the See Also rule below), and excluding index.md/log.md (handled above):
- Target does not exist → search wiki/ for a file with the same name elsewhere.
  - Exactly one match → fix the path.
  - Zero or multiple matches → report to the user.

**Raw references** — every link in a Raw field must point to an existing raw/ file:
- Target does not exist → search raw/ for a file with the same name elsewhere.
  - Exactly one match → fix the path.
  - Zero or multiple matches → report to the user.

**See Also** — within each topic directory:
- Target of a See Also link does not exist → search wiki/ for a file with the same name elsewhere.
  - Exactly one match → fix the path.
  - Zero matches → remove the link (a dead cross-reference is not load-bearing).
  - Multiple matches → report to the user.

### Mechanical Reports (no fixes)

Start with `python3 <skill-dir>/scripts/vault_status.py <project-root>` for the one-screen overview, then run the checks below for details on each area it flags.

Run these mechanically with `python3 <skill-dir>/scripts/check_evidence.py <project-root>` (optionally followed by project-root-relative article paths to limit scope). Default scope is the whole wiki; the script is fast. Report findings; never auto-fix facts.

**Source fidelity** — reported suspects are candidates, not verdicts: derived values and product names may appear. Judge each against the raw context and report only real mismatches.

**Evidence errors** — articles the script cannot verify (missing Raw field, unresolvable Raw links, or Raw links escaping `raw/`). These always need a decision, not a fix from the script.

**Unreferenced raw files** — files logged with a No material disposition are excluded; everything else is a genuine backlog reminder.

**Inbox** — run `scripts/inbox.py list`; if `+/` holds anything, report the item count and suggest Organize.

**Guide compliance** — run `python3 <skill-dir>/scripts/check_guide.py <project-root>` (tags, facet counts, folders). In wiki/, which you own, clear unlisted tags with `--strip` on the affected articles and add missing facets: that is a safe fix. Everywhere else (the human's notes, raw/), report and offer the fix; apply it only with the human's yes.

**File names** — run `python3 <skill-dir>/scripts/check_names.py <project-root>` and report violations. Offer to rename wiki/ articles (you own them): with a yes, rename each with `scripts/rename.py`, which also updates `wiki/index.md` and every link to it. Files in the human's folders get a proposed name only; rename them only with the human's yes, the same way.

### Judgment Reports (no fixes)

These rely on your judgment. Report findings without auto-fixing:

- Factual contradictions across articles
- Outdated claims superseded by newer sources but still presented without a Status block
- Missing conflict annotations where sources disagree
- Obviously missing cross-references between related articles (suggest them; do not add silently)
- Malformed Status blocks (Outdated missing its date, or either block missing its explanation; format reference: `references/article-template.md`)
- Orphan pages with no inbound links from other wiki articles
- Missing cross-topic references
- Concepts frequently mentioned but lacking a dedicated page
- Archive pages whose cited source articles have been substantially updated since archival
- Links in HOME.md that point to missing files (propose the fix; HOME.md is the human's)
- Wiki articles without a `[!summary]` callout, and notes crowded with callouts (more than about three besides the summary)

### Post-Lint

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] lint | <N> issues found, <M> auto-fixed
```

---

## Conventions

- Standard markdown with relative links throughout.
- File names follow the Naming Convention everywhere except raw/, +/, and the fixed files.
- Tags come only from the guide; raw/ carries none. Every Ingest and Organize passes the Compliance Gate.
- Callouts use only the guide's types; every wiki article opens with a `[!summary]`.
- HOME.md and ME.md change only with the human's explicit yes.
- wiki/ supports one level of topic subdirectories only. No deeper nesting.
- Today's date for log entries, Collected dates, and Archived dates. Updated dates reflect when the article's knowledge content last changed. Published dates come from the source (use `Unknown` when unavailable).
- Inside wiki/ files, all markdown links use paths relative to the current file. In conversation output, use project-root-relative paths (e.g., `wiki/topic/article.md`).
- Ingest updates both `wiki/index.md` and `wiki/log.md` (a No material ingest updates only the log). Fetch only updates the log. Organize updates the log, and the index for the raw items it compiles. Archive (from Query) updates both. Lint updates `wiki/log.md` (and `wiki/index.md` only when auto-fixing index entries). Plain queries do not write any files.
