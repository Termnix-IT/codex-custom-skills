# Skills 解説

このドキュメントは、`skills/` に配置した各 skill が何をするものかを説明するための一覧です。

`SKILL.md` は Codex が実行時に読む手順書です。一方で、このドキュメントは人が repository を見たときに、どの skill をいつ使うべきかを判断しやすくするために使います。

## 書き方

skill を追加したら、以下の観点で 1 件ずつ追記します。

- **目的**: その skill が解決する作業。
- **使う場面**: Codex にその skill を使わせたい具体的な依頼。
- **入力**: ユーザーや repository から必要になる情報。
- **成果物**: skill 実行後に作られるもの、更新されるもの、返される説明。
- **注意点**: 使わない方がよい場面、前提条件、手作業が残る部分。

## 一覧

| Skill | 概要 | Directory |
| --- | --- | --- |
| `example-skill` | custom skill の最小構成を示すサンプルです。 | `skills/example-skill/` |

## example-skill

### 目的

新しい custom skill を作るときの最小テンプレートとして使います。

### 使う場面

- `SKILL.md` の基本構造を確認したいとき。
- 新しい skill を作る前に、frontmatter や workflow の書き方を見たいとき。

### 入力

- 作りたい skill の名前。
- その skill を使うべき状況。
- Codex に実行させたい手順。

### 成果物

- `SKILL.md` の構成例。
- skill directory に置ける補助 directory の考え方。

### 注意点

- この skill は実作業を自動化するものではなく、構成例です。
- 公開前に、自分の skill に合わせて `name`, `description`, workflow を置き換えてください。

## 追加用テンプレート

新しい skill を追加したら、以下をコピーしてこの下に追記します。

```markdown
## skill-name

### 目的

この skill が解決する作業を書きます。

### 使う場面

- Codex にこの skill を使わせたい依頼例を書きます。

### 入力

- 必要な情報やファイルを書きます。

### 成果物

- 作成、更新、確認されるものを書きます。

### 注意点

- 前提条件、制限、使わない方がよい場面を書きます。
```
