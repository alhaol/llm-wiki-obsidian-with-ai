# Third-party notices

This project is MIT licensed — see [LICENSE](LICENSE).

It redistributes files from the project below, which is separately MIT licensed.
Its copyright notice is reproduced here as that license requires.

## karpathy-llm-wiki

- Source: https://github.com/Astro-Han/karpathy-llm-wiki
- License: MIT

Files vendored from it:

```
SKILL.md
references/raw-template.md
references/article-template.md
references/index-template.md
references/archive-template.md
scripts/check_evidence.py
tests/test_check_evidence.py
examples/
```

Modification: explicit `encoding="utf-8"` was added to file I/O in
`tests/test_check_evidence.py`, which otherwise fails on Windows.

```
MIT License

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
