# worktreeを作成する

git worktree で新しい作業ツリーを作成する。

## 事前確認

最初にブランチを決定する。

- ブランチ名が入力された場合はそのブランチ名を使う
- 何も入力がなければカレントブランチを使う
- ブランチ名が未指定で判断できない場合はユーザーに確認する

## 実行

`scripts/create-worktree.py` を使う（パスはスキルルート基準）。
worktree を作りたい対象リポジトリ上で実行する。

```shell
{スキルルート}/scripts/create-worktree.py --branch feature/example
```

worktree ルートは script が自動で決める。
現在の worktree ルートの親ディレクトリ名が `プロジェクト名-worktrees` ならそれを使う。
そうでなければ現在の worktree ルートの親直下に `プロジェクト名-worktrees` を作って使う。

### オプション

- ブランチは `--branch <branch>` で指定する。local に存在すれば既存 branch を使い、1つの remote にだけ存在すれば tracking branch を作り、どこにもなければ新規 branch を作る
- 新規 branch を作る時の base は `--base <ref>` で指定できる。未指定なら `main`

## 確認

1. script の終了コードを確認する
2. script 出力の `Worktree path`、`Copied`、`Skipped copies`、`mise trust` を確認する
3. 通常実行では最後に `git worktree list` が出るため、追加結果を確認する
4. ユーザーには作成したブランチ名、worktree の絶対パス、コピーした Git 管理外ファイル、`mise trust` の実施有無を伝える
