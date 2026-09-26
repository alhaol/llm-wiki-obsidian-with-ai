---
description: File everything in the +/ inbox into the vault, tag it, and empty the inbox
---

Use the {{skill}} skill and follow its **Organize** section for the `+/` inbox
at the vault root.

Arguments: $ARGUMENTS

- No arguments: organize every item in `+/`.
- `--dry-run`: build and show the filing plan, then stop without moving anything.
- One or more paths under `+/`: organize only those items. Leave the rest, and
  skip the final emptiness check.

Every filed item must pass the skill's Compliance Gate: guide folders, guide
tags only (stray tags mapped or cleared), and the naming convention.

Finish with the plan you executed, anything you asked about, the tags you
mapped or dropped, and the output of the inbox `finish` check.
