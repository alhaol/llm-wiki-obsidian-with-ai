# LLM Wiki for Obsidian

Turn an Obsidian vault into a knowledge base that a coding agent maintains for
you. You read and ask questions; the agent ingests sources, writes the articles,
and keeps the index and log current.

Two folders, both visible in Obsidian:

- **`raw/`** — immutable source material. Clipped pages, pasted text, fetched
  articles. The agent reads it and never edits it.
- **`wiki/`** — compiled articles, plus `index.md` and `log.md`. The agent owns
  this entirely.

The agent instructions live in a dot-directory, so none of the machinery shows
up in your notes.

Works with **Claude Code**, **Gemini CLI**, **OpenCode**, and **Hermes** from a single install.

---

## Prerequisites

- **git** and **Python 3.9+** (the skill's lint script is Python; no packages
  needed)
- **Obsidian**
- At least one agent CLI: [Claude Code](https://claude.com/claude-code),
  [Gemini CLI](https://github.com/google-gemini/gemini-cli),
  [OpenCode](https://opencode.ai), or [Hermes](https://github.com/NousResearch/hermes-agent)

---

## Setup

Replace `my-llm-wiki` with whatever you want to call the skill — it becomes the
slash command (`/my-llm-wiki`) in OpenCode and Hermes. Lowercase, hyphens only.

```bash
# 1. Create the vault and make it a git repo
mkdir -p ~/brain && cd ~/brain
git init

# 2. Install the skill into the vault's agent directory
git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .claude/skills/my-llm-wiki
rm -rf .claude/skills/my-llm-wiki/.git   # you own this copy now; edit freely

# 3. Bootstrap the vault
python .claude/skills/my-llm-wiki/scripts/init_vault.py
```

<details>
<summary>Windows PowerShell</summary>

```powershell
New-Item -ItemType Directory -Force ~\brain | Out-Null
Set-Location ~\brain
git init

git clone https://github.com/alhaol/llm-wiki-obsidian-with-ai .claude\skills\my-llm-wiki
Remove-Item -Recurse -Force .claude\skills\my-llm-wiki\.git

python .claude\skills\my-llm-wiki\scripts\init_vault.py
```

</details>

Step 3 is not optional glue — it does four things that are tedious to get right
by hand:

- renames the skill in `SKILL.md` frontmatter to match the directory you chose
  (OpenCode rejects a skill whose `name:` and folder disagree)
- creates `raw/` and `wiki/`
- exposes the skill to Hermes under `.agents/skills/`, using a symlink, a
  Windows junction, or a copy — whichever your system allows
- writes a `.gitignore` that keeps Obsidian's per-machine UI state out of history

Then:

1. In Obsidian, **Open folder as vault** and select `~/brain`.
2. Apply the four settings in
   [`references/obsidian-conventions.md`](references/obsidian-conventions.md) —
   the link format one matters most, because wikilinks silently disable every
   lint check the skill provides.
3. Start your agent **from the vault root**. The skill resolves `raw/` and
   `wiki/` relative to your working directory, so always launch from there.

### Why `git init` is required

Not just for history. Hermes locates project-local skills by walking up to the
nearest ancestor containing `.git`. Without a repo, Hermes will not find the
skill at all. Claude Code and OpenCode do not care, so if you will never use
Hermes you can skip it — pass `--no-git-init` and the bootstrapper will tell you
what you are giving up instead of failing.

### Why `.claude/skills/`, not the vault root

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

---

## Per-agent notes

One clone serves all four, because the tools' search paths overlap.

| Agent | Reads the skill from | Extra step |
|---|---|---|
| Claude Code | `.claude/skills/` | none |
| Gemini CLI | `.gemini/skills/` or `.agents/skills/` | none |
| OpenCode | `.claude/skills/` | none |
| Hermes | `.agents/skills/` (created by the bootstrapper) | `hermes skills trust` |

**Hermes only.** Hermes will not auto-load skills from a repo it does not
trust — they are procedure documents it would be following. Run this once per
vault, from inside it:

```bash
hermes skills trust
```

Until you do, Hermes shows a banner saying project skills were found but not
loaded. `hermes skills untrust` reverses it.

**If the bootstrapper reported `copied` rather than `symlink`/`junction`** for
the Hermes path, the two copies drift. Re-run `init_vault.py` after editing
`SKILL.md` to re-sync.

---

## Daily use

Everything is plain conversation with the agent from the vault root.

**Ingest** — add a source and compile it into the wiki:

```
add https://example.com/post to the wiki
```

The agent saves the source to `raw/<topic>/`, decides whether it is new
material, writes or merges the article in `wiki/<topic>/`, updates related
articles it affects, and appends to `wiki/index.md` and `wiki/log.md`. If the
source adds nothing you do not already have, it says so and stops rather than
padding the wiki.

**Query** — ask what you know. This never writes files:

```
what do I know about terminal emulators?
```

Ask it to archive the answer and it becomes a new page, marked `[Archived]` in
the index.

**Lint** — check the wiki's health:

```
lint the wiki
```

It fixes safe things itself (broken internal links, index drift, dead
cross-references) and reports the rest: contradictions between articles, claims
a newer source superseded, raw files you ingested but never compiled, and any
number or quote in an article it cannot find in the source it cites.

That last check is the point of the whole design. Every load-bearing fact in
`wiki/` has to exist verbatim in a `raw/` file the article links. Because `raw/`
is immutable, a verified article stays verified.

You can run that check yourself:

```bash
python .claude/skills/my-llm-wiki/scripts/check_evidence.py .
```

---

## Layout

After setup, from the vault root:

```
~/brain/
├── .claude/skills/my-llm-wiki/   # the skill (hidden from Obsidian)
│   ├── SKILL.md                  # customize here
│   ├── references/               # templates the agent follows
│   ├── scripts/check_evidence.py
│   └── examples/
├── .agents/skills/my-llm-wiki    # link to the above, for Hermes
├── raw/                          # sources, immutable
│   └── <topic>/YYYY-MM-DD-slug.md
├── wiki/                         # articles, agent-owned
│   ├── index.md
│   ├── log.md
│   └── <topic>/<article>.md
├── assets/                       # Obsidian attachments (see conventions)
└── .gitignore
```

Only `raw/`, `wiki/` and `assets/` are visible in Obsidian.

---

## Customizing

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

## Troubleshooting

**The agent does not know about the wiki.** You are probably not in the vault
root. `cd ~/brain` and restart. For Hermes, confirm you ran `hermes skills
trust`.

**OpenCode rejects the skill.** The `name:` in `SKILL.md` frontmatter must match
its directory name exactly, be 1–64 characters, and match
`^[a-z0-9]+(-[a-z0-9]+)*$`. Re-running `init_vault.py` fixes this.

**Lint reports images as missing index entries.** Obsidian is saving attachments
into `wiki/`. Set Settings → Files & Links → Default location for new attachments
→ `assets`.

**Lint reports every link as broken.** The vault is using wikilinks. Turn
"Use [[Wikilinks]]" off; lint only understands markdown links.

**`init_vault.py` says it is not inside a recognized agent directory.** The clone
must land in `<vault>/.claude/skills/<name>/` (or `.gemini/`, `.agents/`, `.hermes/`,
`.opencode/`). Move it there, or pass `--vault ~/brain`.

---

## Credits

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

MIT, © 2026 Ibrahim AbuAlhaol — see [LICENSE](LICENSE).

The vendored skill files remain under their own MIT license:

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
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR OTHER DEALINGS IN THE SOFTWARE.
```
