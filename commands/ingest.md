---
description: Fetch a source into raw/ and compile it into the wiki
---

Use the {{skill}} skill and follow its **Ingest** section (Fetch, Triage,
Compile, Cascade Updates, Post-Ingest).

Source: $ARGUMENTS

- A URL, a file path, or pasted text: ingest that source.
- Several sources: fetch each, then compile them one at a time.
- No arguments: compile the backlog instead. Run the skill's evidence check,
  and ingest every raw file it lists as unreferenced, skipping the Fetch step
  for each (it is already in `raw/`).

Every article you write must pass the skill's Compliance Gate: guide tags
only, the naming convention, and `wiki/<topic>/`.

Finish with each source's disposition, the articles you created or updated,
and any tags you mapped or dropped.
