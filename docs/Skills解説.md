# Skills 解説

このドキュメントは、`skills/` に配置した各 skill が何をするものかを説明するための一覧です。

`SKILL.md` は Codex が実行時に読む手順書です。一方で、このドキュメントは人が repository を見たときに、どの skill をいつ使うべきかを判断しやすくするために使います。

## 一覧

| Skill | 何をする skill か | Directory |
| --- | --- | --- |
| `create-agents-md` | repository 向けの `AGENTS.md` を作成、更新し、Codex や coding agent 用の作業ルールを整理します。 | `skills/create-agents-md/` |
| `feature-dev` | 非自明な機能開発を、調査、設計比較、実装、検証、要約まで一貫して進めます。 | `skills/feature-dev/` |
| `frontend-design-brief` | frontend の見た目や設計方向を実装前に明確化し、既存 UI と一貫した変更にします。 | `skills/frontend-design-brief/` |
| `implementation-researcher` | 実装前に built-in API、既存依存、新規 library、自作実装のリスクを比較して方針を決めます。 | `skills/implementation-researcher/` |
| `why-before-build` | personal project で機能追加前に、本当に作るべきか、最小範囲は何かを検討します。 | `skills/why-before-build/` |

## 整理ルール

Codex にデフォルトで入っている可能性がある skill は、安全のためこの repository から外します。

現時点では、自作 skill には license を置いていない前提で、`LICENSE`, `LICENCE`, `COPYING`, `NOTICE` などの license / notice file が含まれる skill を既存/配布 skill と判断して除外しています。

## Skill 別メモ

### create-agents-md

- **目的**: repository の coding agent 向けルールを `AGENTS.md` として整備します。
- **使う場面**: project conventions、build/test command、編集ルール、禁止事項を Codex に覚えさせたいとき。
- **成果物**: `AGENTS.md` の新規作成または更新。
- **注意点**: repository 固有の事実に基づいて書くため、実装や設定を確認してから使います。

### feature-dev

- **目的**: 機能開発を場当たり的にせず、調査から検証まで段階的に進めます。
- **使う場面**: 新機能、仕様変更、設計比較、非自明な修正を依頼するとき。
- **成果物**: 実装方針、変更、検証結果、残課題の整理。
- **注意点**: 小さな typo 修正や単純作業には重めです。

### frontend-design-brief

- **目的**: frontend のデザイン意図、UI 制約、既存 design system との整合を先に固めます。
- **使う場面**: screenshot、design image、既存 UI をもとに変更したいとき。
- **成果物**: 実装前の design brief、維持すべき見た目のルール。
- **注意点**: 実装そのものではなく、デザイン判断を安定させるための skill です。

### implementation-researcher

- **目的**: 実装前に、標準機能、framework 機能、既存依存、新規 library、自作の選択肢を比較します。
- **使う場面**: architecture、dependency、security、file processing、state management など判断リスクがあるとき。
- **成果物**: 推奨方針、理由、実装計画、open question。
- **注意点**: 調査段階ではコードを書かず、方針決定を優先します。

### why-before-build

- **目的**: personal project で、作る前に必要性と最小 scope を確認します。
- **使う場面**: nice-to-have な機能、拡張、polish を追加しそうなとき。
- **成果物**: 作るべきかの判断、縮小案、non-code 代替案、最小実装範囲。
- **注意点**: user pain が弱い場合は、実装しない判断も含めて提案します。

## 追記テンプレート

新しい skill を追加したら、以下をコピーして追記します。

```markdown
### skill-name

- **目的**: この skill が解決する作業を書きます。
- **使う場面**: Codex にこの skill を使わせたい依頼例を書きます。
- **成果物**: 作成、更新、確認されるものを書きます。
- **注意点**: 前提条件、制限、使わない方がよい場面を書きます。
```
