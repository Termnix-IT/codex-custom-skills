# codex-custom-skills

自作・採用した Codex Skills と旧版の履歴を管理し、GitHub で公開するための repository です。

## Structure

```text
.
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
├── archive/
│   └── skills/<skill-name>/
│       ├── 旧手順.md
│       └── 廃止理由.md
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
Copy-Item -Recurse .\skills\<skill-name> $env:USERPROFILE\.codex\skills\
```

## Included Skills

この repository に配置済みの skill は [Skills 解説](docs/Skills解説.md) にまとめています。

現役Skillには自作Skillと、採用元・コミット・ライセンスを明記した外部Skillを含みます。

旧版は`archive/skills/`に保管します。置き換え時の記録方法は[Skills 解説の整理ルール](docs/Skills解説.md#整理ルール)、今回の旧版と理由は[create-agents-mdの廃止理由](archive/skills/create-agents-md/廃止理由.md)を参照してください。アーカイブはインストール対象に含めません。

## Notes

- 実行用ファイルや scripts は English file names を使います。
- 読み物の docs は Japanese file names を使います。
- Codex標準Skillは重複して含めず、外部Skillは採用を決めたものだけを含めます。

## License

MIT License. See [LICENSE](LICENSE).

外部Skillには各Skill内のライセンスと著作権表示も適用されます。

## Documentation

- [Skills 解説](docs/Skills解説.md): 追加した skill の目的、使いどころ、成果物、注意点をまとめます。
- [GitHub 公開手順](docs/公開手順.md): repository 作成から push までの手順です。
