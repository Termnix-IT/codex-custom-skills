# Web方式の制作

HTML/CSSまたはReact方式を選んだ場合に読む。方式の判断と演出案の確認は`SKILL.md`で行う。既存プロジェクトとユーザーが指定した基盤を優先し、新しい描画エンジンやタイムラインを自作しない。

## 準備と共通の制作方針

- Node.js、パッケージ管理ツール、基盤が必要とするブラウザ・描画環境、FFmpeg・ffprobeの所在を確認する。HyperFramesはNode.js 22以降を前提とし、他の必要条件・利用条件・コマンドは採用版の公式資料と`--help`で確認する。
- 新規プロジェクトは案件の出力先に作り、素材とソースを保持する。既存プロジェクトではその依存関係とlockfileを再利用する。必要な依存だけを案件内に導入し、採用版を固定して記録する。実行時の`npx`による追加ダウンロードも導入に含めて扱う。
- 外部Skillが利用可能なら、選んだ基盤に必要な技術手順だけを参照する。未導入なら、この参照と公式資料で進められる。Skill一式を無条件に導入せず、承認済みの演出・素材・尺を引き継ぐ。追加サービスの認証・有料生成・公開は、その操作が必要で合意済みの場合だけ行う。
- [共通の制作記録](編集と確認のポイント.md#共通の制作記録)に主方式、採用理由、実際のバージョン、プロジェクト、時間軸、音声・字幕の管理先を記録する。Web基盤が持つ制作データを再利用できる場合は、そこへ統合する。
- レイアウト、文字組み、図形はHTML/CSS/SVGなどの既存機能を使う。日本語フォントと改行を実際の描画で確認し、使用素材・フォントを最終描画時に読み込める状態にする。ネットワーク素材は利用条件を確認して保存し、制作中の読み込みに依存し続けない。
- 同じ時刻・フレームで同じ画面になるよう作る。現在時刻、未固定の乱数、描画中の通信、実時間任せのアニメーションに依存しない。音や素材の読み込み完了を確認し、開始・終了・重なりを基盤の時間管理に合わせる。

## HTML/CSSで制作する

HyperFramesを第一候補にする。DOMの配置とCSSの見た目を分け、基盤の時刻指定とseek可能なアニメーションで動きを作る。通常のWebページを録画するだけで、タイムラインを任意時刻へ移動できる制作プロジェクトの代わりにしない。

1. 既存のHyperFramesプロジェクトがあれば再利用する。新規では公式CLIで最小の雛形を生成し、採用版の生成オプションを確認する。`init`がSkillsの更新を伴う版では更新対象と保存先も確認し、選んだ方式に必要な範囲に収める。`--skip-skills`は無効化されている版があるため、導入抑止を保証する引数として使わない。承認範囲を超える変更が必要なら既存環境での代案か導入範囲を相談する。
2. 承認済みの構成に各場面・素材・文字を割り当てる。公式のcomposition契約を確認してからHTMLを書く。クリップの表示・素材の再生は基盤に任せ、アニメーションは対応する時間軸で制御する。
3. プレビューを開いてscrubし、冒頭、代表場面、転換、末尾を確認する。レイアウト、フォント、読み取り時間、音声の位置を確認し、lint・必要な検証を通す。
4. 代表場面を5〜15秒程度の音付き動画として書き出す。範囲指定が採用版にない場合は、同じソース・素材から短いcompositionを作る。全編の低解像度化だけで代用しない。
5. 確認された修正を同じソースへ反映して全編を出力し、`SKILL.md`の完成動画の検証を行う。

以下は操作の形。生成時は選んだCLI版、生成後は案件内の固定済み依存を使う。初回生成の引数は現行の公式CLIと`--help`で確認する。

```powershell
npx hyperframes init "制作/html-video" --non-interactive --example=blank
Set-Location "制作/html-video"
npx hyperframes preview
# プレビューを止めて、検証後に書き出す
npx hyperframes lint
npx hyperframes render --output "renders/preview-v1.mp4"
```

例の最後のコマンドはプロジェクト全体を出力する。短いプレビュー用の時間軸を用意してから実行し、完成版では全編の時間軸と別の出力名を使う。出力名だけで短いプレビューになったと扱わない。

## Reactで制作する

Remotionを第一候補にする。Reactを使う理由は部品の再利用、データからの画面生成、既存資産との整合であり、見た目の派手さではない。

1. 既存のRemotionプロジェクトがあれば再利用する。新規では公式の`create-video`で雛形を作り、依存とlockfileを案件内に保持する。生成先、テンプレート、追加オプションは現行CLIで確認する。
2. 構成をcompositionと再利用する部品に分け、width、height、fps、durationInFramesを設定する。文章・数値・色などの内容はpropsで渡し、演出との関係が分かる形で保持する。
3. `useCurrentFrame`などのフレーム情報から見た目を決め、`interpolate`・`spring`・`Sequence`など公式の機能で動きと登場時刻を作る。実時間のCSSアニメーションやタイマー任せにしない。既存React部品も、任意フレームで描画できるか確認する。
4. Studioでscrubし、文字・配置・出入り・素材・音の位置を確認する。プロジェクトにある型検査・lintを実行し、短いプレビュー用compositionを同じ部品と素材で用意して音付き動画へ出力する。
5. プレビュー確認後に全編を出力する。propsとソースを保持し、内容変更はそこへ反映する。出力は`SKILL.md`の完成動画の検証を行う。

以下は既存プロジェクト内で実行する形。エントリーポイントとcomposition IDは実際の登録値へ置き換える。Windowsではpropsをコマンド内のJSON文字列ではなくファイルで渡す。

```powershell
npx remotion studio
npx remotion render src/index.ts Preview renders/preview-v1.mp4 --props=props.json
npx remotion render src/index.ts Main renders/final-v1.mp4 --props=props.json
```

`Preview`と`Main`は例のIDで、自動的に用意されるものではない。短いプレビューでは映像・字幕・音声を同じ短い時間軸へ合わせる。データ違いの量産は、共通部品を修正してから各propsで確認する。

## 別方式との受け渡し

全編をWeb基盤で作れるならそこで完結させる。FFmpeg側へ場面や透過素材を渡す場合は[方式をまたぐ制作](編集と確認のポイント.md#方式をまたぐ制作)を読み、時間軸・alpha・音声・字幕の管理先をそろえる。基盤内のプレビューと最終合成後の映像は両方確認する。

ブラウザの画面が正常でも、任意時刻へのseekやフレーム書き出しが同じ結果になるとは限らない。短い実レンダリングで文字、透明度、動き、音声を確認してから全編へ進む。確認できない場合は未確認の項目を明示する。

## 一次資料

必要な操作・環境差だけを調べ、マニュアルや外部Skill全体を複製しない。

- [HyperFrames公式](https://github.com/heygen-com/hyperframes): 必要環境、CLI、Skillsと制作方式。
- [HyperFramesのcomposition契約](https://github.com/heygen-com/hyperframes/tree/main/skills/hyperframes-core): HTML、時間指定、素材再生、描画の規則。
- [Remotionのプロジェクト作成](https://www.remotion.dev/docs): 雛形と必要環境。
- [Remotionの基本構造](https://www.remotion.dev/docs/the-fundamentals): フレームとcomposition。
- [Remotionのアニメーション](https://www.remotion.dev/docs/animating-properties): フレームに応じた変化。
- [Remotion Studio](https://www.remotion.dev/docs/cli/studio)、[render](https://www.remotion.dev/docs/cli/render): プレビュー、出力、Windowsのprops指定。
