# Skills 解説

このドキュメントは、`skills/` に配置した各 skill が何をするものかを説明するための一覧です。

`SKILL.md` は Codex が実行時に読む手順書です。一方で、このドキュメントは人が repository を見たときに、どの skill をいつ使うべきかを判断しやすくするために使います。

## 一覧

| Skill | 何をする skill か | Directory |
| --- | --- | --- |
| `create-agentsmd` | repository の根拠、コマンド、階層別の適用範囲を確認し、`AGENTS.md`を作成・改善・監査します。 | `skills/create-agentsmd/` |
| `feature-dev` | 非自明な機能開発を、調査、設計比較、実装、検証、要約まで一貫して進めます。 | `skills/feature-dev/` |
| `frontend-design-brief` | frontend の見た目や設計方向を実装前に明確化し、既存 UI と一貫した変更にします。 | `skills/frontend-design-brief/` |
| `implementation-researcher` | 実装前に built-in API、既存依存、新規 library、自作実装のリスクを比較して方針を決めます。 | `skills/implementation-researcher/` |
| `why-before-build` | personal project で機能追加前に、本当に作るべきか、最小範囲は何かを検討します。 | `skills/why-before-build/` |
| `video-edit` | 提供素材に合う演出と制作方式を選び、音付きの短いプレビューを確認して動画を制作します。 | `skills/video-edit/` |
| `game-development` | エンジン共通で、企画・体験設計から実装、プレイテスト、配布用ビルドまで必要な工程を進めます。 | `skills/game-development/` |

## 整理ルール

現役Skillは`skills/`に置き、自作Skillと明示的に採用した外部Skillを管理します。Codex標準Skillは重複して含めません。license / noticeの有無だけで採用・除外を決めず、目的と出典を確認します。

外部Skillには採用元、採用コミット、ローカルでの変更点を記録し、配布元のlicense / noticeを保持します。置き換えた旧版は`archive/skills/<skill-name>/`へ保管し、`廃止理由.md`に判断理由、置き換え先、復元方法を残します。旧版の`SKILL.md`は`旧手順.md`へ改名し、アーカイブをSkill探索・インストール対象から外します。

廃止したSkillと保管内容は、各フォルダの記録を参照してください。

- [create-agents-mdの廃止理由](../archive/skills/create-agents-md/廃止理由.md)

## Skill 別メモ

### create-agentsmd

- **目的**: repository の coding agent 向けルールを `AGENTS.md` として整備します。
- **使う場面**: `AGENTS.md`の新規作成、既存指示の改善・監査、monorepoの階層別指示を整備するとき。
- **成果物**: 根拠に基づく`AGENTS.md`の新規作成または更新、検証結果と未確認事項。
- **注意点**: 既存の正確な指示を保持し、コマンドを設定から読んだことと実行したことを区別します。外部のチェッカーは任意で、ローカルの検証を代替しません。
- **採用元**: [sunxiayi/agents-md-starter-kitと採用コミット](../skills/create-agentsmd/採用元.md)。旧`create-agents-md`を置き換えています。

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

### video-edit

- **目的**: 提供素材の強みを活かす演出を提案し、専門用語を知らなくても制作・修正を依頼できるようにします。文字中心か動き中心か、動きの強さ、業務説明か動画映えする言葉かを演出案とまとめて選び、手法の名前と見える効果を説明します。原文は意味と必須情報を守って要約できます。
- **使う場面**: PV、キル集、アプリ紹介MVなどの編集依頼。必要なら起動可能なWebアプリの撮影から扱いますが、ジャンルは限定しません。
- **成果物**: 手法の説明と推奨理由を含む演出案、素材と表現に合う制作方式、動き・文言も確認できる音付きの短いプレビュー、確認後の完成動画、修正用の制作記録・編集JSONまたは制作プロジェクト、主な演出の短い説明。今回の指定先を優先し、指定がなければ任意の個人用JSONの既定先へ案件ごとに保存します。個人パスを公開Skillへ含めない設定方法は[保存先と個人設定](../skills/video-edit/references/編集と確認のポイント.md#保存先と個人設定)を参照してください。
- **注意点**: FFmpeg・ffprobeと、選んだ方式の必要環境を使います。基本編集はPython＋FFmpeg、文字・図形・UIの演出はHTML/CSS（HyperFramesを第一候補）、部品の再利用・量産はReact（Remotionを第一候補）を選び、必要なら組み合わせます。同梱ヘルパーにはPythonが必要で、Web基盤や外部Skillsは一括導入しません。BGMは持ち込みを優先し、不足時やAI選曲を指定した場合は候補から選びます。必要な画像素材は任意のGPT Imageで補えます。任意のGemini TTSにはAPI利用環境が必要です。同梱スクリプトは[実行手順](../skills/video-edit/references/実行手順.md)、Web方式は[Web方式の制作](../skills/video-edit/references/Web方式の制作.md)、方式間の合成と画像生成は[編集と確認のポイント](../skills/video-edit/references/編集と確認のポイント.md)、TTSは[音声生成](../skills/video-edit/references/音声生成.md)を参照してください。

### game-development

- **目的**: プレイヤーの行動と選択を軸に、遊べる試作から依頼された完成範囲まで制作します。
- **使う場面**: 新規ゲームの企画・制作、既存ゲームの機能追加・修正・バランス調整、演出、検証、配布用ビルド。
- **成果物**: 依頼範囲に応じた企画とルール、操作可能なゲームとソース、プレイ確認の結果、検証済みの配布物。構想相談だけの場合は実装しません。
- **構成**: [SKILL.md](../skills/game-development/SKILL.md)が共通方針と参照先を担当し、`references/`内の6資料を必要な工程だけ読みます。`agents/openai.yaml`は表示名と呼び出し文を定義します。実用途のあるヘルパーや配布素材が決まるまで`scripts/`や`assets/`を作りません。
- **拡張**: [制作環境の選択](../skills/game-development/references/制作環境の選択.md#環境別手順を追加する)に従い、必要になった環境の手順を`references/engines/<environment>/`へ追加します。初版は特定エンジンのAPIやテンプレートを含みません。
- **注意点**: 実際のプレイ、自動テスト、ビルド成功、人による評価を区別します。使用環境の能力に応じた未確認事項を伝え、特定のエンジン、ジャンル、FPS、外部Skillを必須にしません。配布用ビルドの作成は公開・ストア申請を含みません。

## 追記テンプレート

新しい skill を追加したら、以下をコピーして追記します。

```markdown
### skill-name

- **目的**: この skill が解決する作業を書きます。
- **使う場面**: Codex にこの skill を使わせたい依頼例を書きます。
- **成果物**: 作成、更新、確認されるものを書きます。
- **注意点**: 前提条件、制限、使わない方がよい場面を書きます。
```
