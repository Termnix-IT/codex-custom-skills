# Custom Codex Skills

自作した Codex Skills を管理し、GitHub で公開するための repository です。

## Structure

```text
.
├── skills/
│   └── example-skill/
│       └── SKILL.md
├── docs/
│   ├── Skills解説.md
│   └── 公開手順.md
├── AGENTS.md
└── README.md
```

## Adding A Skill

1. `skills/<skill-name>/` を作成します。
2. その中に `SKILL.md` を追加します。
3. `SKILL.md` の frontmatter に `name` と `description` を書きます。
4. 必要に応じて、同じ skill directory に `scripts/`, `assets/`, `references/` を追加します。
5. `docs/Skills解説.md` に、その skill が何をするものかを追記します。

## Skill Template

```markdown
---
name: your-skill-name
description: Use when ...
---

# Your Skill Name

## When To Use

Use this skill when ...

## Workflow

1. ...
2. ...
3. ...
```

## Install Locally

この repository から skill を使う場合は、対象 skill directory を `$CODEX_HOME/skills` 配下へコピーします。

Windows PowerShell の例:

```powershell
Copy-Item -Recurse .\skills\example-skill $env:USERPROFILE\.codex\skills\
```

## Notes

- 実行用ファイルや scripts は English file names を使います。
- 読み物の docs は Japanese file names を使います。
- 公開前に license を選んで追加してください。

## Documentation

- [Skills 解説](docs/Skills解説.md): 追加した skill の目的、使いどころ、成果物、注意点をまとめます。
- [GitHub 公開手順](docs/公開手順.md): repository 作成から push までの手順です。
