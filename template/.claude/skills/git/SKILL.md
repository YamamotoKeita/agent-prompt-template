---
name: git
description: Git操作を行う。commit、push、ブランチ作成、worktree作成、mainブランチの取り込みとコンフリクト解消など。
---

`docs/git-rules.md` があれば必ず参照すること。

開発で頻出するGit操作を行う。依頼内容から操作を判定し、操作別参考資料にある場合は手順に沿って操作する。
操作別参考資料にない場合は、一般的なGitの操作方法に従って操作する。

## 操作別参考資料

- [ブランチの変更を取り込む](references/merge-or-rebase.md)
- [worktreeを作る](references/worktree.md)


## 共通ルール

- 指定がない限り amend しない
- 指定がない限り force push しない
- push 先は origin を優先する
