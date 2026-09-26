# Walkthrough: one `/organize` run

A worked example of emptying the `+/` inbox, from a messy drop to a filed,
tagged, compliant vault. Paths, tags, and output formats are the real ones the
skill and its scripts use; the notes themselves are illustrative.

## Before: what was dropped into `+/`

Eight items, exported from an old notes app, a download folder, and the web
clipper:

```
+/
├── Untitled 3.md                    pricing ideas, embeds the whiteboard photo
├── IMG_2041.jpg                     photo of a whiteboard: three pricing tiers
├── 2026-09-19 thoughts.md           a journal entry from last Friday
├── Attention Is All You Need.pdf    the transformer paper
├── why-weekly-reviews-fail.md       web clip, already has a "> Source:" header
├── second-order thinking.md         a principle, in the human's own words
├── notes copy.md                    exact copy of a note already in Concepts/
└── misc.md                          a short list, no context
```

## 0. Snapshot

```
$ python .claude/skills/my-llm-wiki/scripts/inbox.py list .
warning: 3 uncommitted change(s). Commit before organizing, so the run can be undone with one `git revert`.
```

> **Agent:** You have 3 uncommitted changes. Commit them first as
> "Snapshot before organize", so this whole run can be undone with one revert?
>
> **Human:** yes

## 1. Inventory

```
+/2026-09-19 thoughts.md           note
+/Attention Is All You Need.pdf    asset
+/IMG_2041.jpg                     asset
+/Untitled 3.md                    note
+/misc.md                          note
+/notes copy.md                    note   duplicate of Concepts/mental_models_list_md.md
+/second-order thinking.md         note
+/why-weekly-reviews-fail.md       clip

8 item(s): 5 note, 1 clip, 2 asset; 1 duplicate(s)
```

## 2–3. Classify and plan

The agent reads every note and clip, then shows the plan before moving
anything. It is unsure about one item, so it asks once:

> **Agent:** `misc.md` is a list of five gift ideas with no dates or names. Is it
> for a family project (→ `Areas/Family-Projects/`) or just a scrap
> (→ `Fleeting/`)? My guess: Family-Projects.
>
> **Human:** family, it's for my sister's birthday

| Item | Destination | Tags |
|---|---|---|
| `IMG_2041.jpg` | `assets/pricing_tiers_whiteboard_jpg.jpg` | — |
| `Untitled 3.md` | `Areas/Side-Business/tiered_pricing_ideas_md.md` | afpish/independence, status/start, urgency/high, time/q4-2026, type/decision |
| `2026-09-19 thoughts.md` | `Daily/2026_09_19_weekly_reflection_md.md` | afpish/spirit, status/complete, urgency/low, time/archived, type/daily |
| `second-order thinking.md` | `Concepts/second_order_thinking_md.md` | afpish/professional, status/complete, urgency/low, time/ongoing |
| `misc.md` | `Areas/Family-Projects/birthday_gift_ideas_md.md` | afpish/family, status/start, urgency/medium, time/immediate, people/family |
| `Attention Is All You Need.pdf` | `assets/attention_paper_original_pdf.pdf` + raw extract `raw/machine-learning/2017-06-12-attention-is-all-you-need.md` | raw: none |
| `why-weekly-reviews-fail.md` | `raw/productivity/2026-09-20-why-weekly-reviews-fail.md` | raw: none |
| `notes copy.md` | removed (duplicate of `Concepts/mental_models_list_md.md`) | — |

Every move goes through `scripts/rename.py`, so the embed in
`Untitled 3.md` follows the photo:

```
$ python .claude/skills/my-llm-wiki/scripts/rename.py . +/IMG_2041.jpg assets/pricing_tiers_whiteboard_jpg.jpg
moved: +/IMG_2041.jpg -> assets/pricing_tiers_whiteboard_jpg.jpg
links updated: +/Untitled 3.md
```

`![[IMG_2041.jpg]]` became `![[pricing_tiers_whiteboard_jpg.jpg]]`.

## 4. Compile

The two raw files go through Ingest one at a time:

- `2017-06-12-attention-is-all-you-need.md` → **New**:
  `wiki/machine-learning/transformer_architecture_md.md`
- `2026-09-20-why-weekly-reviews-fail.md` → **Update**: merged into
  `wiki/productivity/weekly_review_practices_md.md`, with a
  **Status: Disputed** block where it contradicts an earlier source

## 5. Compliance gate

The old notes carried tags the guide does not list. `check_guide.py --strip`
cleared them after the agent mapped the ones with a clear meaning:

| Tag found | Became |
|---|---|
| `#work` | `afpish/professional` |
| `#journal` | `type/daily` |
| `#ideas`, `#todo`, `#pricing` | removed |

```
$ python .claude/skills/my-llm-wiki/scripts/check_guide.py . <filed paths...>
9 file(s) checked, 0 guide violation(s)
$ python .claude/skills/my-llm-wiki/scripts/check_names.py . <filed paths...>
9 file(s) checked, 0 naming violation(s)
```

## Close out

The log entry, written before the two ingest entries it caused:

```markdown
## [2026-09-26] organize | 8 items from +/
- assets/pricing_tiers_whiteboard_jpg.jpg <- +/IMG_2041.jpg
- Areas/Side-Business/tiered_pricing_ideas_md.md <- +/Untitled 3.md
- Daily/2026_09_19_weekly_reflection_md.md <- +/2026-09-19 thoughts.md
- Concepts/second_order_thinking_md.md <- +/second-order thinking.md
- Areas/Family-Projects/birthday_gift_ideas_md.md <- +/misc.md
- assets/attention_paper_original_pdf.pdf <- +/Attention Is All You Need.pdf
- raw/machine-learning/2017-06-12-attention-is-all-you-need.md <- +/Attention Is All You Need.pdf
- raw/productivity/2026-09-20-why-weekly-reviews-fail.md <- +/why-weekly-reviews-fail.md
- Duplicate removed: +/notes copy.md (same as Concepts/mental_models_list_md.md)
```

```
$ python .claude/skills/my-llm-wiki/scripts/inbox.py finish .
+/ is empty
```

The agent's closing message ends with:

> **Suggested for HOME.md**
> - `- [Tiered pricing ideas](Areas/Side-Business/tiered_pricing_ideas_md.md) — urgency/high, ties to your Q4 focus`
> - `- [Transformer architecture](wiki/machine-learning/transformer_architecture_md.md) — new; you are watching "LLM internals"`
>
> Commit this run as "Organize +/: 8 items"?

## After

```
Areas/Family-Projects/birthday_gift_ideas_md.md
Areas/Side-Business/tiered_pricing_ideas_md.md
Concepts/second_order_thinking_md.md
Daily/2026_09_19_weekly_reflection_md.md
assets/attention_paper_original_pdf.pdf
assets/pricing_tiers_whiteboard_jpg.jpg
raw/machine-learning/2017-06-12-attention-is-all-you-need.md
raw/productivity/2026-09-20-why-weekly-reviews-fail.md
wiki/machine-learning/transformer_architecture_md.md      (new)
wiki/productivity/weekly_review_practices_md.md           (updated)
+/                                                        (empty)
```
