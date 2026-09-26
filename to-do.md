# To-do

Remaining improvements, most useful first. Items 1–7 of the original list
(safe rename, vault status, organize snapshot, generated guide HTML,
quickstart, organize walkthrough, starter guide) are done.

## Planned

### 1. Continuous integration

Add a GitHub Actions workflow that runs `python -m unittest discover -s tests`
on Linux, macOS, and Windows, with Python 3.9 and the latest 3.x.

- Why: the Windows link (junction) and line-ending code paths in
  `init_vault.py`, `build_guide.py`, and the tests break silently otherwise.
- Note: the TOML tests skip on Python < 3.11 (no `tomllib`); CI should prove
  the skip works on 3.9.

### 2. Skill version and changelog

Add `version:` to the `SKILL.md` frontmatter and a `CHANGELOG.md`.
`init_vault.py` prints the version it installed and whether a re-run changed
anything ("skill v1.4, 3 commands updated").

- Why: tells users when pulling an update and re-running the bootstrapper
  will actually change their vault.

### 3. HOME dashboard block

Add an optional Dataview block to `references/home-template.md` that lists
notes tagged `urgency/critical` or `urgency/high`, and notes in
`status/progress` for the current `time/` window.

- Why: makes the tags visibly pay off on the front page.
- Constraint: it must stay optional and clearly marked, since the agent never
  edits `HOME.md`; the human keeps or deletes it. It needs the Dataview
  community plugin.

## Follow-ups noted along the way

- **Blank line after a stripped tags line.** When `check_guide.py --strip`
  removes a line that held only tags, the blank lines around it can leave a
  double blank line. Collapse it.
- **Hermes command names.** Hermes's docs do not say whether a skill's slash
  command comes from its folder name or its `name:` field; the generated
  command skills set both to the same value. Confirm against a live Hermes
  install, and check that `organize`, `ingest`, `fetch`, and `vault-status`
  do not collide with Hermes built-ins.
- **Pi project trust.** Pi loads `.pi/prompts/` only after the project is
  trusted. Confirm the first-run prompt wording and document it precisely in
  `docs/setup.md`.
- **README length.** Still about 760 lines. Consider moving "How Grounding
  Works" and the FAQ to `docs/` as well.
