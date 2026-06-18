# worktreeを作成する

git worktree で新しい作業ツリーを作成する。

## 事前確認

最初にブランチを決定する。

- ブランチ名が入力された場合はそのブランチ名を使う
- 何も入力がなければカレントブランチを使う（`git branch --show-current` で取得し、`--branch` に渡す）
- ブランチ名が未指定で判断できない場合はユーザーに確認する

script の `--branch` は必須なため、どのケースでも最終的にブランチ名を解決して渡す。

## 実行

`scripts/create-worktree.py` を使う（パスはスキルルート基準）。
worktree を作りたい対象リポジトリ上で実行する。

```shell
{スキルルート}/scripts/create-worktree.py --branch feature/example
```

script は Git 管理外ファイルを **gitignore 対象も含めて** worktree にコピーする。
`node_modules` や Carthage 成果物など、コピーしないとビルド・実行できない資産を運ぶための仕様（意図的なフルコピー）。

worktree ルートは script が自動で決める。
現在の worktree ルートの親ディレクトリ名が `プロジェクト名-worktrees` ならそれを使う。
そうでなければ現在の worktree ルートの親直下に `プロジェクト名-worktrees` を作って使う。

### オプション

- ブランチは `--branch <branch>` で指定する。local に存在すれば既存 branch を使い、1つの remote にだけ存在すれば tracking branch を作り、どこにもなければ新規 branch を作る
- 新規 branch を作る時の base は `--base <ref>` で指定できる。未指定なら `main`

## 確認

1. script の終了コードを確認する
2. script 出力を確認する
    - `Branch`、`Mode`（新規作成 or 既存ブランチ）、`Worktree path`、`Worktrees root`
    - `Copied`、`Skipped copies`（コピーした / スキップした Git 管理外ファイル）
    - `Notes`（base に `origin/main` を使った、upstream を設定した等の補足。あれば必ず確認）
3. 通常実行では最後に `git worktree list` が出るため、追加結果を確認する
4. ユーザーには作成したブランチ名、worktree の絶対パス、コピーした Git 管理外ファイル、`Notes` の内容を伝える
