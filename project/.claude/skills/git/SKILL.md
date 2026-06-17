---
name: git
description: Git操作を行う。commit、push、ブランチ作成、worktree作成、mainブランチの取り込みとコンフリクト解消、ブランチの変更内容確認、リリース内容の確認に使用。コミットして、pushして、ブランチを切って、mainを取り込んで、コンフリクトを解消して、worktreeを作って、などの依頼で使用。
---
開発で頻出するGit操作を行う。依頼内容から操作を判定し、対応するフローに従う。

## 操作別参考資料

| 依頼の例 | フロー |
|---|---|
| mainを取り込んで、コンフリクトを解消して | [references/merge-main.md](references/merge-main.md) |
| ブランチを作って、ブランチを切って | [references/create-branch.md](references/create-branch.md) |
| worktreeを作って、別ディレクトリで並行作業したい | [references/worktree.md](references/worktree.md) |
| このブランチの変更内容を確認して | 下記「ブランチの変更内容確認」 |
| リリースできる内容を確認して | [references/confirm-release.md](references/confirm-release.md) |

複数操作の依頼（例: コミットしてからworktree作成）は、依頼の順に各フローを実行する。

## 共通ルール

- 指定がない限り amend しない
- 指定がない限り force push しない
- push 先は origin を優先する
- コンフリクト解消で両方の変更意図の統合に迷う場合は、ユーザーに確認する

docs/gitルール.md があればそちらも参照すること。

## ブランチの変更内容確認

変更ファイルの一覧と変更行数を確認する。

```shell
git diff --stat origin/main...HEAD
```

変更行をすべて出力する場合は以下を実行する。

```shell
git diff origin/main...HEAD
```
