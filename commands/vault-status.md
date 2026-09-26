---
description: One-screen vault health check with the next step for each finding
---

Use the {{skill}} skill. Run its `scripts/vault_status.py` on the vault root
and show the summary as printed.

Extra arguments: $ARGUMENTS

Then, for each line marked `!!`, say in one sentence what it means and which
command fixes it. Change nothing: this is a read-only check. If the human
asks for details on a line, run the script named in that line's hint.
