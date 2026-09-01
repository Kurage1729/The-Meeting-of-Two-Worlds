# TMTW WikiとGPTを一緒に使う方法

この文書は、TMTWの確定設定を英語Wikiで管理しながら、日本語でGPTと相談するための初心者向け手順書です。

## 1. 三種類のファイル

### 英語Wiki

`countries/`、`history/`、`culture/`などにある通常のMarkdownです。ここだけを確定設定として扱います。

### 日本語Draft

`_drafts/`に置きます。検討中の案なので、確定設定ではありません。

### GPT向け全体資料

`context/all-context.md`です。英語Wikiを更新すると、GitHub Actionsが全ページを自動的に結合します。自分で編集する必要はありません。

## 2. 最初の導入

1. 配布ZIPを解凍する。
2. 解凍したフォルダの**中身**をGitHubリポジトリのルートへアップロードする。
3. コミットメッセージを`Add GPT context workflow`にする。
4. GitHubのリポジトリで**Actions**タブを開く。
5. 左側に**Build GPT Context**が表示されることを確認する。
6. 自動実行されていなければ、**Run workflow**を押す。
7. 緑色のチェックが付いたら、`context/all-context.md`を開く。
8. プレースホルダーではなく、多数のWikiページが一つに結合されていれば成功。

### Actionsが書き込めない場合

エラーに`Permission`、`403`、`not permitted`などが出た場合は、次を確認します。

1. リポジトリの**Settings**を開く。
2. 左側の**Actions** → **General**を開く。
3. 下部の**Workflow permissions**を探す。
4. **Read and write permissions**を選択して保存する。
5. **Actions**へ戻り、失敗した実行を開いて**Re-run all jobs**を押す。

## 3. 新しい設定を相談する

### Draftを作る

1. `_drafts/TEMPLATE.md`を開く。
2. 内容をコピーする。
3. `_drafts`フォルダで**Add file** → **Create new file**を選ぶ。
4. `topic-name.md`のようなファイル名を付ける。
5. テンプレートを貼り、日本語で案を書く。
6. `Add draft about ...`のようなメッセージでコミットする。

### GPTへ相談する

次のように依頼します。

```text
以下を参照してください。

確定設定全体:
https://raw.githubusercontent.com/kurage1729/The-Meeting-of-Two-Worlds/main/context/all-context.md

今回の検討メモ:
https://raw.githubusercontent.com/kurage1729/The-Meeting-of-Two-Worlds/main/_drafts/topic-name.md

確定設定とDraftを区別してください。
Draftの案について、史実との整合性と既存設定との矛盾を確認しながら、日本語で検討してください。
```

リポジトリが非公開の場合、RawリンクだけではGPTが読めないことがあります。その場合はGitHub連携を使うか、該当ファイルを会話へ添付します。

## 4. 結論を英語Wikiへ反映する

議論がまとまったら、GPTへ次のように依頼します。

```text
今回の決定を確定設定にします。

1. 更新が必要な全Wikiページを列挙してください。
2. 各ページについて、変更後の英語Markdownを作ってください。
3. 他ページやtimelineにも変更が必要なら含めてください。
4. Draftにしか存在しない不採用案はWikiへ入れないでください。
```

出力された内容で英語Wikiを更新し、GitHubへコミットします。通常は数十秒から数分後に**Update GPT context**という自動コミットが追加され、`context/all-context.md`も更新されます。

## 5. Draftを閉じる

英語Wikiへの反映後、Draftの冒頭を次のように変更します。

```text
Status: Resolved
```

`Decision`欄には、採用した結論と更新したページを書きます。Draftは削除せず残しておくと、なぜその設定になったかを後から確認できます。

## 6. 普段の流れ

```text
日本語Draftを書く
        ↓
all-context.mdと一緒にGPTへ渡す
        ↓
日本語で考証・検討する
        ↓
GPTに英語Wikiの変更版を作らせる
        ↓
英語Wikiをコミットする
        ↓
all-context.mdが自動更新される
```

## 7. 注意点

- `context/all-context.md`は直接編集しない。
- `_drafts/`の内容は確定設定として扱わない。
- 英語Wikiを更新したら、関連する年表・人物・国ページも忘れず確認する。
- GPTには「矛盾があれば黙って直さず、先に指摘する」と伝える。
- 一度に大きく変更するより、一つの話題ごとにコミットすると履歴を追いやすい。

