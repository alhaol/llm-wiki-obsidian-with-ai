# 🧠 LLM Wiki for Obsidian

> **Your AI agent writes the wiki. You read it and ask questions.**

Turn an [Obsidian](https://obsidian.md) vault into a personal knowledge base
that a coding agent maintains for you. Feed it articles, blog posts, and
research — the agent compiles them into structured wiki pages, keeps cross-references
up to date, and makes sure every fact traces back to a source.

```
 You ──► paste a URL ──────────► Agent fetches, compiles, indexes ──► You read in Obsidian
 You ──► drop old files in +/ ─► Agent files, tags, compiles, empties +/
```

### ✨ Key features

- 📥 **Ingest** — feed the agent a URL or text; it saves the source, writes a
  structured wiki article, and updates the index
- 🗂️ **Organize** — drop old notes, clipped pages, papers, and images into the
  `+/` inbox; the agent files each one into the right folder, tags it, compiles
  the knowledge into the wiki, and leaves `+/` empty
- ⌨️ **Slash commands** — `/ingest`, `/fetch`, `/organize`, and `/vault-status` in all five
  agents, re-synced from the skill whenever you re-run the bootstrapper
- 🔍 **Query** — ask what you know; the agent searches your wiki and answers
  with citations
- 🩺 **Lint** — the agent audits the wiki for broken links, stale claims, and
  facts that don't match their sources
- 🔒 **Grounded** — every number, date, and quote in your wiki must exist
  verbatim in the source file it cites. Verified once, verified forever.
- 🧭 **Vault guide** — one folder, naming, and tag charter that you and the
  agent both follow, so the vault stays organized as it grows
- 🔤 **Readable names** — every note and file is named from its content plus a
  type identifier (`second_order_thinking_md.md`, `garden_bed_layout_png.png`)
- 🏠 **HOME and ME** — two notes you own: `HOME.md` is your front page,
  `ME.md` tells the agent who you are. It reads both, suggests updates, and
  never edits them without your yes

### 🤖 Works with any agent

One install, five supported agents, all sharing the same skill and commands:

| | Agent | Skills directory |
|---|---|---|
| 🟣 | [Claude Code](https://claude.com/claude-code) | `.claude/skills/` |
| 🔵 | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `.gemini/skills/` |
| 🟢 | [OpenCode](https://opencode.ai) | `.claude/skills/` |
| 🟡 | [Hermes](https://github.com/NousResearch/hermes-agent) | `.agents/skills/` |
| 🟠 | [Pi](https://pi.dev) | `.agents/skills/` |

---

## 📋 Prerequisites

| Requirement | Why |
|---|---|
| **git** | Hermes needs `.git` to find project skills; also gives you history |
| **Python 3.9+** | The lint script is pure Python — no packages needed |
| **Obsidian** | Your reading interface |
| **An agent CLI** | At least one of the five above |

---

## 🚀 Setup

> Replace `my-llm-wiki` with whatever you want to call the skill — it becomes
> the slash command (`/my-llm-wiki`) in OpenCode and Hermes. Lowercase, hyphens
> only.

> 🧭 **Before step 3, make the vault guide yours.** The clone contains
> [`guides/guide.md`](guides/guide.md), the folder and tag charter for your
> vault. Its areas, people, and places are the author's; edit them in the
> cloned copy (for example `.claude/skills/my-llm-wiki/guides/guide.md`) before
> you run the bootstrapper, which copies it into the vault and creates its
> folders. See [Vault Guide](#-vault-guide) below.

### macOS / Linux

Pick the block that matches your agent — the bootstrapper cross-links everything,
so all five agents will find the skill no matter which directory you clone into.

<details open>
<summary>🟣 Claude Code</summary>

```bash
# 1️⃣  Create the vault and make it a git repo
mkdir -p ~/brain && cd ~/brain
git init

# 2️⃣  Install the skill into the vault's agent directory
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .claude/skills/my-llm-wiki
rm -rf .claude/skills/my-llm-wiki/.git   # you own this copy now; edit freely

# 3️⃣  Bootstrap the vault
python .claude/skills/my-llm-wiki/scripts/init_vault.py
```

</details>

<details>
<summary>🔵 Gemini CLI</summary>

```bash
# 1️⃣  Create the vault and make it a git repo
mkdir -p ~/brain && cd ~/brain
git init

# 2️⃣  Install the skill into the vault's agent directory
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .gemini/skills/my-llm-wiki
rm -rf .gemini/skills/my-llm-wiki/.git   # you own this copy now; edit freely

# 3️⃣  Bootstrap the vault
python .gemini/skills/my-llm-wiki/scripts/init_vault.py
```

</details>

<details>
<summary>🟢 OpenCode</summary>

```bash
# 1️⃣  Create the vault and make it a git repo
mkdir -p ~/brain && cd ~/brain
git init

# 2️⃣  Install the skill (OpenCode reads from .claude/skills/)
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .claude/skills/my-llm-wiki
rm -rf .claude/skills/my-llm-wiki/.git   # you own this copy now; edit freely

# 3️⃣  Bootstrap the vault
python .claude/skills/my-llm-wiki/scripts/init_vault.py
```

</details>

<details>
<summary>🟡 Hermes</summary>

```bash
# 1️⃣  Create the vault and make it a git repo
mkdir -p ~/brain && cd ~/brain
git init

# 2️⃣  Install the skill into the vault's agent directory
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .agents/skills/my-llm-wiki
rm -rf .agents/skills/my-llm-wiki/.git   # you own this copy now; edit freely

# 3️⃣  Bootstrap the vault
python .agents/skills/my-llm-wiki/scripts/init_vault.py

# 4️⃣  Trust the skill (Hermes only, once per vault)
hermes skills trust
```

</details>

<details>
<summary>🟠 Pi</summary>

```bash
# 1️⃣  Create the vault and make it a git repo
mkdir -p ~/brain && cd ~/brain
git init

# 2️⃣  Install the skill (Pi reads .agents/skills/)
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .agents/skills/my-llm-wiki
rm -rf .agents/skills/my-llm-wiki/.git   # you own this copy now; edit freely

# 3️⃣  Bootstrap the vault
python .agents/skills/my-llm-wiki/scripts/init_vault.py

# 4️⃣  Start pi and trust the project when it asks (needed for .pi/prompts/)
pi
```

</details>

### Windows PowerShell

<details open>
<summary>🟣 Claude Code</summary>

```powershell
# 1️⃣  Create the vault and make it a git repo
New-Item -ItemType Directory -Force ~\brain | Out-Null
Set-Location ~\brain
git init

# 2️⃣  Install the skill
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .claude\skills\my-llm-wiki
Remove-Item -Recurse -Force .claude\skills\my-llm-wiki\.git

# 3️⃣  Bootstrap the vault
python .claude\skills\my-llm-wiki\scripts\init_vault.py
```

</details>

<details>
<summary>🔵 Gemini CLI</summary>

```powershell
# 1️⃣  Create the vault and make it a git repo
New-Item -ItemType Directory -Force ~\brain | Out-Null
Set-Location ~\brain
git init

# 2️⃣  Install the skill
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .gemini\skills\my-llm-wiki
Remove-Item -Recurse -Force .gemini\skills\my-llm-wiki\.git

# 3️⃣  Bootstrap the vault
python .gemini\skills\my-llm-wiki\scripts\init_vault.py
```

</details>

<details>
<summary>🟢 OpenCode</summary>

```powershell
# 1️⃣  Create the vault and make it a git repo
New-Item -ItemType Directory -Force ~\brain | Out-Null
Set-Location ~\brain
git init

# 2️⃣  Install the skill (OpenCode reads from .claude\skills\)
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .claude\skills\my-llm-wiki
Remove-Item -Recurse -Force .claude\skills\my-llm-wiki\.git

# 3️⃣  Bootstrap the vault
python .claude\skills\my-llm-wiki\scripts\init_vault.py
```

</details>

<details>
<summary>🟡 Hermes</summary>

```powershell
# 1️⃣  Create the vault and make it a git repo
New-Item -ItemType Directory -Force ~\brain | Out-Null
Set-Location ~\brain
git init

# 2️⃣  Install the skill
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .agents\skills\my-llm-wiki
Remove-Item -Recurse -Force .agents\skills\my-llm-wiki\.git

# 3️⃣  Bootstrap the vault
python .agents\skills\my-llm-wiki\scripts\init_vault.py

# 4️⃣  Trust the skill (Hermes only, once per vault)
hermes skills trust
```

</details>

<details>
<summary>🟠 Pi</summary>

```powershell
# 1️⃣  Create the vault and make it a git repo
New-Item -ItemType Directory -Force ~\brain | Out-Null
Set-Location ~\brain
git init

# 2️⃣  Install the skill (Pi reads .agents\skills\)
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .agents\skills\my-llm-wiki
Remove-Item -Recurse -Force .agents\skills\my-llm-wiki\.git

# 3️⃣  Bootstrap the vault
python .agents\skills\my-llm-wiki\scripts\init_vault.py

# 4️⃣  Start pi and trust the project when it asks (needed for .pi\prompts\)
pi
```

</details>

### What the bootstrapper does

Step 3 is not optional glue — it handles seven things that are tedious to get
right by hand:

| | What | Why |
|---|---|---|
| 🏷️ | Renames the skill in `SKILL.md` frontmatter | OpenCode rejects a skill whose `name:` and folder disagree |
| 📁 | Creates `raw/`, `wiki/`, the `+/` inbox, and `assets/` | The directories the skill's workflows need |
| 🧭 | Copies `guides/guide.md` to `Systems/vault-guide.md`, renders it as `GUIDE.html` at the vault root, and creates the folders the guide lists | One charter, visible in Obsidian, that you and the agent both follow — plus a styled page that keeps the conventions in view and is rebuilt from *your* guide on every re-run |
| 🏠 | Seeds `HOME.md` and `ME.md` at the vault root | Empty templates for you to fill in; the agent reads them before every task |
| 🔗 | Cross-links the skill to `.agents/`, `.claude/`, `.gemini/` | So every agent can find it, no matter which directory you cloned into |
| ⌨️ | Installs `/fetch`, `/ingest`, `/organize`, `/vault-status` into `.claude/commands/`, `.opencode/commands/`, `.gemini/commands/`, `.pi/prompts/`, and as small skills in `.hermes/skills/` | The same commands in all five agents. Re-running refreshes them (see [Keeping agents in sync](#-keeping-agents-in-sync)); a command file you wrote yourself is never touched (`--no-commands` skips this step) |
| 🚫 | Writes a `.gitignore` | Keeps Obsidian's per-machine UI state out of git |

### After the bootstrapper

1. In Obsidian → **Open folder as vault** → select `~/brain`
2. Apply the settings in
   [`references/obsidian-conventions.md`](references/obsidian-conventions.md) —
   the link format one matters most, because **wikilinks silently disable every
   lint check** the skill provides
3. Start your agent **from the vault root** — the skill resolves `raw/` and
   `wiki/` relative to your working directory
4. Open `Systems/vault-guide.md` in Obsidian and pin it — it is your map of
   the vault. `GUIDE.html` at the root is the same charter, styled; open it in
   a browser (Obsidian lists it only with **Settings → Files & Links → Detect
   all file extensions** on)
5. Fill in `HOME.md` and `ME.md` — see [HOME and ME](#-home-and-me)

---

## 🧭 Vault Guide

A wiki the agent writes is only half a vault. The other half is your own
notes: daily captures, projects, ideas. The vault guide is a single note that
says where everything goes and how it is tagged, and **both you and the agent
follow it**.

| | Folders — *where does it live?* | Tags — *what is it about?* |
|---|---|---|
| **Defines** | `+` (inbox), `Daily`, `Fleeting`, `Areas/<project>`, `Concepts`, `raw`, `wiki`, `Systems`, `Archive`, `assets` | Facets written `#facet/value`: life balance (`afpish/*`), `status/*`, `urgency/*`, `time/*`, plus optional `type/*`, `people/*`, `places/*` |
| **You** | Capture in `Daily`/`Fleeting`, drop bulk or old material in `+`, file weekly | Tag in the weekly review, update `status/*` as work moves |
| **Agent** | Keeps `raw/` and `wiki/` in order, empties `+` on `/organize`, writes elsewhere only when asked | Tags every wiki article from the guide's values, flags missing tags during lint |

### Customize it, then bootstrap

1. Edit `guides/guide.md` in your cloned copy of the skill. Replace the
   example areas, people, places, and time windows with your own; add or
   remove facets. Keep the **Folder Hierarchy** block's shape (one `/path`
   per line) because the bootstrapper reads it to create folders.
2. Run `init_vault.py`. It copies the guide to `Systems/vault-guide.md` and
   creates every folder in the hierarchy.
3. From then on, **the vault copy is the one that counts.** Edit it in
   Obsidian as your life changes, and re-run `init_vault.py` to create any
   folders you added. It never overwrites the vault copy.

Already have your own charter? Pass `--guide path/to/charter.md`. Don't want
one? Pass `--no-guide`, and the skill behaves exactly as before.
[`guides/guide.html`](guides/guide.html) is the shipped guide rendered for a
browser. It is generated by `scripts/build_guide.py`; edit `guide.md`, never the
HTML. In your vault, `GUIDE.html` is rebuilt from `Systems/vault-guide.md`
each time you run the bootstrapper, so it always shows your version.

### How the agent uses it

`SKILL.md` tells the agent to read `Systems/vault-guide.md` before every
ingest, archive, and lint. The skill keeps its structure rules for `raw/` and
`wiki/`, and the guide decides the tags. Each wiki article gets the guide's
tags as YAML frontmatter above its title, which Obsidian's tag pane, search,
and Dataview all read:

```markdown
---
tags: [afpish/professional, status/progress, urgency/medium, time/ongoing, type/paper]
---

# Transformer Architecture

> Sources: Vaswani et al., 2017-06-12
> Raw: [attention](../../raw/machine-learning/2017-06-12-attention-is-all-you-need.md)
> Updated: 2026-09-25
```

`raw/` files are never tagged, because they are immutable. When the agent needs
a tag value or folder the guide lacks, it asks you to add it to the guide
instead of making one up.

### ✅ The compliance gate

Everything the agent ingests from `raw/` into `wiki/`, and everything it
files out of `+/`, follows the system in full before the task counts as done:

| | Rule | Checked by |
|---|---|---|
| 🏷️ | Only tags the guide lists, with the right count per facet. Stray tags (`#work`, `#Status/Progress`, `#todo`) are mapped to the guide value with the same meaning, or cleared | `scripts/check_guide.py` (`--strip` clears) |
| 📂 | Only folders the guide lists; sources and articles one level under `raw/<topic>/` and `wiki/<topic>/` | `scripts/check_guide.py` |
| 🔤 | Names follow the [naming convention](#-file-naming) | `scripts/check_names.py` |
| 📄 | `raw/` carries no tags: frontmatter tags go, inline hashtags are escaped to `\#` (they look the same but no longer clutter your tag pane) | `scripts/check_guide.py` |

`check_guide.py` reads the allowed tag values, facet counts, and folders from
your `Systems/vault-guide.md`, so the gate always enforces *your* charter. The
agent reports which tags it mapped or dropped; if a dropped value keeps
appearing, add it to the guide and it will be kept from then on. Lint runs the
same checks across the whole vault: it fixes `wiki/` itself and only proposes
fixes for your own notes.

### 🔤 File naming

Every file outside `raw/` and `+/` is named from its content, then its type:

```
{word}_{word}[_{word}[_{word}[_{word}]]]_{identifier}.{extension}
```

Two to five lowercase words that say what the file is about, then an
identifier that says what kind of file it is: the extension itself, except
Excalidraw drawings, which use `excali`.

| Kind | Example |
|---|---|
| Note or wiki article | `transformer_architecture_md.md` |
| Daily note (date = three words) | `2026_09_26_standup_md.md` |
| Image | `garden_bed_layout_png.png` |
| PDF | `attention_paper_original_pdf.pdf` |
| Drawing | `login_flow_sketch_excali.excalidraw.md` |

The agent names everything it writes this way, `/organize` renames what it
files from `+/`, and lint lists files that break the convention via
`scripts/check_names.py`. Every rename goes through `scripts/rename.py`, which
moves the file and rewrites every link to it — markdown links, `[[wikilinks]]`,
and `![[embeds]]` — so nothing breaks. You can use it yourself:

```bash
python .claude/skills/my-llm-wiki/scripts/rename.py . "Fleeting/Untitled 3.md" Concepts/pricing_experiment_ideas_md.md --dry-run
```
 It renames wiki articles when you
agree, and your own notes only when you say yes. `raw/` keeps the dated slug
names sources arrive with; `HOME.md`, `ME.md`, `GUIDE.html`,
`Systems/vault-guide.md`, `wiki/index.md` and `wiki/log.md` are fixed names.

---

## 🏠 HOME and ME

Two notes at the vault root that **you** write and maintain:

| | `HOME.md` | `ME.md` |
|---|---|---|
| **What** | Your front page: focus, key notes, areas, topics you are watching | Who you are, your priorities, how you want the agent to write, file, and talk to you |
| **Agent reads it** | Before every task, to know what deserves your attention | Before every task, to follow your preferences |
| **Agent suggests** | "Suggested for HOME.md": ready-to-paste links to notes worth your attention after an ingest, organize, or lint | "Suggested for ME.md": a preference you stated in conversation, worded for the file |
| **Agent edits it** | Never, unless you say yes to that exact change | Never, unless you say yes to that exact change |

The bootstrapper creates both from
[`references/home-template.md`](references/home-template.md) and
[`references/me-template.md`](references/me-template.md), with empty sections
and hints. Fill them in yourself; the more `ME.md` says, the less the agent
has to ask.

---

## 📖 Daily Use

Everything is plain conversation with the agent. Just talk to it from the vault root.
Four slash commands cover the common cases:

| Command | What it does |
|---|---|
| `/ingest <url, file, or text>` | Fetch the source into `raw/` and compile it into the wiki |
| `/ingest` | Compile the backlog: every raw file not yet in the wiki |
| `/fetch <url, file, or text>` | Only save the source into `raw/`; compile later with `/ingest` |
| `/organize` | File everything in `+/`, tag it, compile the knowledge, empty `+/` |
| `/organize --dry-run` | Show the filing plan without moving anything |
| `/vault-status` | One-screen health check: inbox, backlog, evidence, names, tags, git — each with its next step |

They work the same in Claude Code, Gemini CLI, OpenCode, Hermes, and Pi. The
commands are thin shortcuts into `SKILL.md`, so plain words ("organize the
inbox", "ingest this") work too.

### 📥 Ingest — add knowledge

Tell the agent to add a source. It fetches, saves, triages, compiles, and indexes:

```
> add https://example.com/post to the wiki
```

**What happens behind the scenes:**

```
1. Fetch    →  saves to raw/ai-coding-tools/2026-03-19-statusline-landscape.md
2. Triage   →  "New article — no existing coverage of this topic"
3. Compile  →  writes wiki/ai-coding-tools/claude_code_statusline_landscape_md.md
4. Index    →  adds row to wiki/index.md
5. Log      →  appends entry to wiki/log.md
```

The agent can also **merge** into existing articles, **flag contradictions** with
a `Status: Disputed` block, or **skip** sources that add nothing new — it won't
pad your wiki with thin content.

<details>
<summary>📋 Example: what a log entry looks like</summary>

From a real wiki's [`log.md`](examples/log-sample.md):

```markdown
## [2026-04-12] ingest | Build in Public content framework
- Disposition: New
- Raw: raw/content-strategy/2026-04-12-x-buildinpublic-thread.md
- Core finding: altruistic content earns distribution, self-narrative does not

## [2026-04-15] ingest | AI coding benchmark methodology
- Disposition: Disputed
- Raw: raw/ai-coding-tools/2026-04-15-vendor-benchmark-post.md
- Updated: Vendor benchmark reliability (marked Status: Disputed)

## [2026-04-18] ingest | no material: raw/ai-coding-tools/2026-04-18-weekly-trending-recap.md
- Disposition: No material
```

Every action gets a timestamped entry: `ingest`, `fetch`, `organize`, `query`, `lint`.

</details>

### 🗂️ Organize — empty the inbox

Got years of notes in another app, a folder of PDFs, or a pile of clipped
pages? Drop them all into `+/` at the vault root (it sorts to the top of
Obsidian's file explorer) and run:

```
> /organize
```

**What happens behind the scenes:**

```
0. Snapshot   →  offers to commit the vault first, so one `git revert` undoes the run
1. Inventory  →  scripts/inbox.py lists every item, guesses note / clip / asset,
                 and flags exact duplicates of files already in the vault
2. Classify   →  each item gets one destination, decided by what it is:
                   clipped article, paper, reading notes  →  raw/<topic>/
                   dated journal entry                    →  Daily/
                   half-formed idea                       →  Fleeting/
                   project plan, decision, log            →  Areas/<area>/
                   your own principle or framework        →  Concepts/
                   finished project                       →  Archive/
                   images, PDFs, other files              →  assets/
3. Plan       →  shows you the table; asks once about anything unclear
4. File       →  moves and renames assets, then notes (Untitled 3.md →
                 pricing_experiment_ideas_md.md; tags added, links fixed),
                 then raw items (wrapped in the raw template, names kept)
5. Compile    →  ingests each new raw file into the wiki, one at a time
6. Close out  →  logs every move, suggests HOME.md entries, checks +/ is empty
```

Nothing is rewritten: your notes keep their text, and only gain a
convention-following name and the vault guide's tags in frontmatter. Nothing is lost: items only move, except exact
byte-for-byte duplicates, which are dropped and logged. Nothing goes straight
into `wiki/`; knowledge gets there only by being compiled from `raw/`.

Run `/organize --dry-run` first if you want to see the plan before anything
moves.

### 🔍 Query — ask what you know

Ask questions. The agent searches your wiki and synthesizes an answer with
citations. This **never writes files** unless you ask it to archive:

```
> what do I know about terminal emulators?
```

```
> compare the statusline tools by star count and language
```

Want to save the answer? Ask the agent to archive it:

```
> archive that answer to the wiki
```

It becomes a new page marked `[Archived]` in the index — a point-in-time
snapshot that is never cascade-updated.

### 🩺 Lint — check wiki health

```
> lint the wiki
```

The agent runs three levels of checks:

| Level | What it does | Auto-fix? |
|---|---|---|
| 🟢 **Safe fixes** | Broken links, index drift, dead cross-refs, stray tags in `wiki/` | ✅ Yes |
| 🟡 **Mechanical** | Facts that don't match their source files; tags, folders, and names outside the guide | ❌ Reports only (offers fixes for your notes) |
| 🔴 **Judgment** | Contradictions, stale claims, missing cross-refs | ❌ Reports only |

For a quick look without the agent, run the same summary `/vault-status` shows:

```bash
python .claude/skills/my-llm-wiki/scripts/vault_status.py .
```

```
  !!  inbox     3 item(s) in +/                             -> /organize
  !!  backlog   2 raw file(s) not compiled                  -> /ingest
  ok  evidence  0 fidelity suspect(s), 0 evidence error(s)
  ok  names     0 naming violation(s)
  ok  guide     0 tag/folder violation(s)
  ok  git       0 uncommitted change(s)
```

Each line names the script with the full details (`check_evidence.py`,
`check_names.py`, `check_guide.py`, `inbox.py`).

---

## 🔬 How Grounding Works

This is the point of the whole design. The wiki is **self-verifying**:

```
wiki/ai-coding-tools/statusline.md          raw/ai-coding-tools/2026-03-19-scan.md
┌──────────────────────────────┐            ┌────────────────────────────────────┐
│ ccusage has 11,693 stars     │──────────► │ ccusage | 11,693 | TypeScript     │
│ claude-hud gained 4,804      │──────────► │ claude-hud went from 2,234 to     │
│ stars in 5 days              │            │ 7,038 (Mar 14→19, GitHub Trending)│
└──────────────────────────────┘            └────────────────────────────────────┘
         wiki/ article                              raw/ source (immutable)
```

- Every number, date, and quote in `wiki/` must exist **verbatim** in the
  `raw/` file it cites
- `raw/` is **immutable** — once saved, never edited
- A verified article **stays verified** — no drift, no silent rewrites

---

## 📁 Layout

After setup, from the vault root:

```
~/brain/
├── 📂 .claude/skills/my-llm-wiki/   ← the skill (hidden from Obsidian)
│   ├── 📄 SKILL.md                  ← customize here
│   ├── 📂 references/               ← templates the agent follows
│   ├── 📂 guides/                   ← vault guide template (edit before bootstrap)
│   ├── 📂 scripts/                  ← init_vault.py, vault_status.py, rename.py, inbox.py,
│   │                                   check_evidence.py, check_guide.py, check_names.py,
│   │                                   build_guide.py
│   ├── 📂 commands/                 ← the four command templates
│   └── 📂 examples/                 ← real wiki samples (see below)
├── 🔗 .agents/skills/my-llm-wiki    ← link for Hermes, Pi, OpenCode, Gemini CLI
├── 🔗 .gemini/skills/my-llm-wiki    ← link for Gemini CLI
├── 📂 .claude/commands/ .gemini/commands/ .opencode/commands/
│                                    ← the four commands, per agent
├── 📂 +/                            ← inbox: drop anything, /organize empties it
├── 📂 raw/                          ← sources, immutable
│   └── <topic>/YYYY-MM-DD-slug.md
├── 📂 wiki/                         ← articles, agent-owned
│   ├── 📄 index.md
│   ├── 📄 log.md
│   └── <topic>/<words>_md.md
├── 📂 Systems/
│   └── 📄 vault-guide.md            ← folder, naming & tag charter, yours to edit
├── 📄 HOME.md                       ← your front page, you maintain it
├── 📄 ME.md                         ← you, for the agent, you maintain it
├── 🌐 GUIDE.html                    ← the charter, styled, for your browser
├── 📂 Daily/ Fleeting/ Areas/ ...   ← your notes, per the guide
├── 📂 assets/                       ← attachments, yours and /organize's
└── 📄 .gitignore
```

> 💡 Everything in dot-directories (`.claude/`, `.gemini/`, `.agents/`) is
> invisible to the vault. What you see in Obsidian is `+/`, `raw/`, `wiki/`,
> `assets/`, and the folders from your vault guide.

---

## 🔄 Raw → Compiled: Before & After

The `examples/` directory contains files from a real wiki. Here's what the
transformation looks like:

### Before: raw source ([`2026-03-19-claude-code-statusline-landscape.md`](examples/2026-03-19-claude-code-statusline-landscape.md))

```markdown
# Claude Code Statusline Market Scan

> Source: claude-pace project research
> Collected: 2026-03-19 (GitHub stars verified via gh api)
> Published: Unknown

| Project | Stars | Language | Form | Last Update | Features |
|---------|------:|----------|------|-------------|----------|
| ccusage | 11,693 | TypeScript | CLI + statusline | 03-18 | Usage analysis + burn rate |
| claude-hud | 7,038 | JavaScript | statusline | 03-15 | Most features, pioneer |
...

### ccusage (11,693 stars) - Overall Strongest
...
```

Unstructured research notes with a metadata header. The agent reads this and
**never touches it again**.

### After: compiled article ([`claude_code_statusline_landscape_md.md`](examples/claude_code_statusline_landscape_md.md))

```markdown
# Claude Code Statusline Tool Ecosystem

> Sources: claude-pace project research, 2026-03-19; 2026-03-24
> Raw: [raw/.../2026-03-19-claude-code-statusline-landscape.md](...)
> Updated: 2026-03-24

## Overview
Around Claude Code's opaque quota problem, the community has spawned over a
dozen statusline tools...

## Competitive Landscape (2026-03-19 Data)
| Project | Stars | Language | Positioning |
|---------|------:|----------|-------------|
| ccusage | 11,693 | TypeScript | CLI usage analysis, cost visualization |
...

## User Pain Points
### Opaque Quota (Root Problem)
1. **Sudden limit hit without warning**: $200/month Max users hit limits in
   10-15 minutes...
```

Structured sections, synthesized tables, cross-references, and a `Raw:` link
that traces every fact back to the source.

### The index ([`ai-coding-tools-index.md`](examples/ai-coding-tools-index.md))

```markdown
# Knowledge Base Index

## ai-coding-tools

| Article | Summary | Updated |
|---------|---------|---------|
| [Claude Max Quota Mechanism](...) | Dual quota mechanism... | 2026-04-02 |
| [Claude Code Statusline Tool Ecosystem](...) | Competitive landscape... | 2026-03-24 |
```

One row per article, grouped by topic, with a summary and last-updated date.
The agent keeps this in sync automatically.

---

## 🤖 Per-Agent Notes

The bootstrapper creates cross-links so one clone serves all agents:

| | Agent | Reads from | Commands from | Extra step |
|---|---|---|---|---|
| 🟣 | Claude Code | `.claude/skills/` | `.claude/commands/*.md` | none |
| 🔵 | Gemini CLI | `.gemini/skills/` or `.agents/skills/` | `.gemini/commands/*.toml` | none |
| 🟢 | OpenCode | `.claude/skills/` | `.opencode/commands/*.md` | none |
| 🟡 | Hermes | `.agents/skills/` | `.hermes/skills/<command>/SKILL.md` (each command is a small skill) | `hermes skills trust` (once per vault) |
| 🟠 | Pi | `.agents/skills/` | `.pi/prompts/*.md` | trust the project when Pi asks (project prompts load only after trust) |

<details>
<summary>🟡 Hermes-specific setup</summary>

Hermes will not auto-load skills from a repo it does not trust. Run this once
per vault, from inside it:

```bash
hermes skills trust
```

Until you do, Hermes shows a banner saying project skills were found but not
loaded. `hermes skills untrust` reverses it.

</details>

### 🔄 Keeping agents in sync

One skill, five agents. What each agent sees stays identical because:

- **Skills are links.** `.agents/`, `.claude/` and `.gemini/skills/` point at
  the one install (symlink, or a junction on Windows), so an edit to
  `SKILL.md` reaches every agent at once. Only when the OS allows neither does
  the bootstrapper copy the skill, and it stamps that copy.
- **Commands are generated.** Each command file carries a
  `generated by init_vault.py` stamp line.

After you edit the skill, its `commands/`, or pull an update, **re-run the
bootstrapper**:

```bash
python .claude/skills/my-llm-wiki/scripts/init_vault.py
```

It refreshes every stamped file and copy (including `GUIDE.html`, rebuilt
from your guide), and reports each one as
`created`, `updated`, or `up to date`. A command file without the stamp is
yours: it is reported as `left alone` and never overwritten. To keep your own
edits to a generated command, delete its stamp line.

---

## ⚙️ Customizing

Edit `SKILL.md` in your copy. It is the schema layer — topic conventions, how
aggressive to be about creating new articles, house style for summaries. Your
folder and tag taxonomy lives in the [vault guide](#-vault-guide) instead, where
you can see it in Obsidian. Rules live there rather than in a root `CLAUDE.md` so they travel with
the skill and stay out of the vault.

[`references/obsidian-conventions.md`](references/obsidian-conventions.md) has
ready-to-paste rules for tags, an Obsidian Web Clipper template that emits the
right raw-file format, and the two settings that prevent lint false positives.

**Staying current with upstream.** Deleting `.git` in step 2 means you will not
get fixes automatically. If you want them, fork this repo on GitHub and clone
your fork instead of deleting the history — then `git pull` in the skill
directory, and resolve conflicts against your edits.

---

## ❓ FAQ & Troubleshooting

<details>
<summary>💬 Why <code>git init</code>?</summary>

Not just for history. Hermes locates project-local skills by walking up to the
nearest ancestor containing `.git`. Without a repo, Hermes will not find the
skill at all. Claude Code, Gemini CLI, and OpenCode do not care, so if you will
never use Hermes you can skip it — pass `--no-git-init` and the bootstrapper
will tell you what you are giving up instead of failing.

</details>

<details>
<summary>💬 Why <code>.claude/skills/</code>, not the vault root?</summary>

Obsidian indexes every `.md` file it can see. Drop this repo at the vault root
and its `SKILL.md`, `references/`, `examples/` and `tests/` become notes in your
graph and search results.

Obsidian ignores any folder whose name starts with a dot. `.claude/` keeps the
skill invisible to the vault while the agents still load it.

That is also why this setup puts **no `CLAUDE.md`, `GEMINI.md` or `AGENTS.md` at the vault
root** — those are `.md` files at the top level of your vault, so they would show
up as notes too. Put your customizations in the copied `SKILL.md` instead. If you
do want a root `AGENTS.md`, add it to Obsidian's Settings → Files & Links →
Excluded files.

</details>

<details>
<summary>⚠️ The agent does not know about the wiki</summary>

You are probably not in the vault root. `cd ~/brain` and restart. For Hermes,
confirm you ran `hermes skills trust`.

</details>

<details>
<summary>⚠️ OpenCode rejects the skill</summary>

The `name:` in `SKILL.md` frontmatter must match its directory name exactly, be
1–64 characters, and match `^[a-z0-9]+(-[a-z0-9]+)*$`. Re-running `init_vault.py`
fixes this.

</details>

<details>
<summary>⚠️ Lint reports images as missing index entries</summary>

Obsidian is saving attachments into `wiki/`. Set Settings → Files & Links →
Default location for new attachments → `assets`.

</details>

<details>
<summary>⚠️ Lint reports every link as broken</summary>

The vault is using wikilinks. Turn "Use [[Wikilinks]]" off; lint only
understands markdown links.

</details>

<details>
<summary>⚠️ <code>init_vault.py</code> says it is not inside a recognized agent directory</summary>

The clone must land in `<vault>/.claude/skills/<name>/` (or `.gemini/`,
`.agents/`, `.hermes/`, `.opencode/`). Move it there, or pass `--vault ~/brain`.

</details>

---

## 🙏 Credits

Originally built on
[Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)
(MIT), and since extended into the vault system described above.

The underlying idea is Andrej Karpathy's: the LLM writes and maintains the wiki,
the human reads and asks questions.

---

📄 MIT, © 2026 Ibrahim AbuAlhaol — see [LICENSE](LICENSE).

<details>
<summary>Upstream license (karpathy-llm-wiki)</summary>

Kept as the MIT license requires for the portions derived from the upstream
project.

```
Copyright (c) 2026 Yuhan Lei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>
