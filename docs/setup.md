# Setup by agent and OS

Every block does the same three things: create the vault as a git repo, clone
the skill into one agent directory, and run the bootstrapper. The bootstrapper
then links the skill and installs the commands for **all five agents**, so pick
the block for the agent you use most; the others work too.

> Replace `my-llm-wiki` with whatever you want to call the skill. Lowercase,
> hyphens only. Before step 3, edit the cloned `guides/guide.md` so the vault
> guide is yours (or pass `--starter` for the minimal starter guide); see the
> [README](../README.md#-vault-guide).

## macOS / Linux

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

## Windows PowerShell

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

[← Back to the README](../README.md#-setup)
