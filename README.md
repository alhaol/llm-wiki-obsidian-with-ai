# 🧠 LLM Wiki for Obsidian

> **Your AI agent writes the wiki. You read it and ask questions.**

Turn an [Obsidian](https://obsidian.md) vault into a personal knowledge base
that a coding agent maintains for you. Feed it articles, blog posts, and
research — the agent compiles them into structured wiki pages, keeps cross-references
up to date, and makes sure every fact traces back to a source.

```
 You ──► paste a URL ──► Agent fetches, compiles, indexes ──► You read in Obsidian
```

### ✨ Key features

- 📥 **Ingest** — feed the agent a URL or text; it saves the source, writes a
  structured wiki article, and updates the index
- 🔍 **Query** — ask what you know; the agent searches your wiki and answers
  with citations
- 🩺 **Lint** — the agent audits the wiki for broken links, stale claims, and
  facts that don't match their sources
- 🔒 **Grounded** — every number, date, and quote in your wiki must exist
  verbatim in the source file it cites. Verified once, verified forever.

### 🤖 Works with any agent

One install, four supported agents:

| | Agent | Skills directory |
|---|---|---|
| 🟣 | [Claude Code](https://claude.com/claude-code) | `.claude/skills/` |
| 🔵 | [Gemini CLI](https://github.com/google-gemini/gemini-cli) | `.gemini/skills/` |
| 🟢 | [OpenCode](https://opencode.ai) | `.claude/skills/` |
| 🟡 | [Hermes](https://github.com/NousResearch/hermes-agent) | `.agents/skills/` |

---

## 📋 Prerequisites

| Requirement | Why |
|---|---|
| **git** | Hermes needs `.git` to find project skills; also gives you history |
| **Python 3.9+** | The lint script is pure Python — no packages needed |
| **Obsidian** | Your reading interface |
| **An agent CLI** | At least one of the four above |

---

## 🚀 Setup

> Replace `my-llm-wiki` with whatever you want to call the skill — it becomes
> the slash command (`/my-llm-wiki`) in OpenCode and Hermes. Lowercase, hyphens
> only.

### macOS / Linux

Pick the block that matches your agent — the bootstrapper cross-links everything,
so all four agents will find the skill no matter which directory you clone into.

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

### What the bootstrapper does

Step 3 is not optional glue — it handles four things that are tedious to get
right by hand:

| | What | Why |
|---|---|---|
| 🏷️ | Renames the skill in `SKILL.md` frontmatter | OpenCode rejects a skill whose `name:` and folder disagree |
| 📁 | Creates `raw/` and `wiki/` | The two directories your vault needs |
| 🔗 | Cross-links the skill to `.agents/`, `.claude/`, `.gemini/` | So every agent can find it, no matter which directory you cloned into |
| 🚫 | Writes a `.gitignore` | Keeps Obsidian's per-machine UI state out of git |

### After the bootstrapper

1. In Obsidian → **Open folder as vault** → select `~/brain`
2. Apply the settings in
   [`references/obsidian-conventions.md`](references/obsidian-conventions.md) —
   the link format one matters most, because **wikilinks silently disable every
   lint check** the skill provides
3. Start your agent **from the vault root** — the skill resolves `raw/` and
   `wiki/` relative to your working directory

---

## 📖 Daily Use

Everything is plain conversation with the agent. Just talk to it from the vault root.

### 📥 Ingest — add knowledge

Tell the agent to add a source. It fetches, saves, triages, compiles, and indexes:

```
> add https://example.com/post to the wiki
```

**What happens behind the scenes:**

```
1. Fetch    →  saves to raw/ai-coding-tools/2026-03-19-statusline-landscape.md
2. Triage   →  "New article — no existing coverage of this topic"
3. Compile  →  writes wiki/ai-coding-tools/claude-code-statusline-landscape.md
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

Every action gets a timestamped entry: `ingest`, `query`, `lint`.

</details>

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
| 🟢 **Safe fixes** | Broken links, index drift, dead cross-refs | ✅ Yes |
| 🟡 **Mechanical** | Facts that don't match their source files | ❌ Reports only |
| 🔴 **Judgment** | Contradictions, stale claims, missing cross-refs | ❌ Reports only |

You can run the mechanical evidence check yourself, outside the agent:

```bash
python .claude/skills/my-llm-wiki/scripts/check_evidence.py .
```

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
│   ├── 📂 scripts/                  ← check_evidence.py, init_vault.py
│   └── 📂 examples/                 ← real wiki samples (see below)
├── 🔗 .agents/skills/my-llm-wiki    ← link for Hermes
├── 🔗 .gemini/skills/my-llm-wiki    ← link for Gemini CLI
├── 📂 raw/                          ← sources, immutable
│   └── <topic>/YYYY-MM-DD-slug.md
├── 📂 wiki/                         ← articles, agent-owned
│   ├── 📄 index.md
│   ├── 📄 log.md
│   └── <topic>/<article>.md
├── 📂 assets/                       ← Obsidian attachments
└── 📄 .gitignore
```

> 💡 Only `raw/`, `wiki/`, and `assets/` are visible in Obsidian. Everything
> in dot-directories (`.claude/`, `.gemini/`, `.agents/`) is invisible to the
> vault.

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

### After: compiled article ([`claude-code-statusline-landscape.md`](examples/claude-code-statusline-landscape.md))

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

| | Agent | Reads from | Extra step |
|---|---|---|---|
| 🟣 | Claude Code | `.claude/skills/` | none |
| 🔵 | Gemini CLI | `.gemini/skills/` or `.agents/skills/` | none |
| 🟢 | OpenCode | `.claude/skills/` | none |
| 🟡 | Hermes | `.agents/skills/` | `hermes skills trust` (once per vault) |

<details>
<summary>🟡 Hermes-specific setup</summary>

Hermes will not auto-load skills from a repo it does not trust. Run this once
per vault, from inside it:

```bash
hermes skills trust
```

Until you do, Hermes shows a banner saying project skills were found but not
loaded. `hermes skills untrust` reverses it.

**If the bootstrapper reported `copied` rather than `symlink`/`junction`** for
the Hermes path, the two copies drift. Re-run `init_vault.py` after editing
`SKILL.md` to re-sync.

</details>

---

## ⚙️ Customizing

Edit `SKILL.md` in your copy. It is the schema layer — topic conventions, how
aggressive to be about creating new articles, your tag taxonomy, house style for
summaries. Rules live there rather than in a root `CLAUDE.md` so they travel with
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

The skill itself — `SKILL.md`, `references/raw-template.md`,
`references/article-template.md`, `references/index-template.md`,
`references/archive-template.md`, `scripts/check_evidence.py`, `tests/` and
`examples/` — is from
[Astro-Han/karpathy-llm-wiki](https://github.com/Astro-Han/karpathy-llm-wiki)
by Yuhan Lei, MIT licensed. The only change to those files is adding explicit
`encoding="utf-8"` to file I/O in `tests/`, which otherwise fails on Windows.

This repo adds the Obsidian integration: `scripts/init_vault.py`,
`references/obsidian-conventions.md`, and this README.

The underlying idea is Andrej Karpathy's: the LLM writes and maintains the wiki,
the human reads and asks questions, and the wiki is a persistent, compounding
artifact.

---

📄 MIT, © 2026 Ibrahim AbuAlhaol — see [LICENSE](LICENSE).

<details>
<summary>Vendored skill license (Yuhan Lei)</summary>

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
