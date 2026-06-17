# mainブランチを取り込む

現在のブランチに main ブランチの変更を取り込み、コンフリクトが発生した場合は解消する。
特に指定がなければ `merge` をし、rebaseの指定がある場合は `rebase` をする。

## 手順

1. 作業中の変更がないことを確認する
    - `git status`
    - uncommitted changes がある場合はユーザーに伝えて終了
2. origin/main を最新化する
    - `git fetch origin main`
3. 現在ブランチのPull Requestがあれば内容を確認する
    - `gh pr view`
    - 現在ブランチの変更意図を把握するために使う。PRがなければスキップ
4. main ブランチを現在のブランチに merge または rebase する
    - merge の場合: `git merge origin/main`
    - rebase の場合: `git rebase origin/main`
5. コンフリクトファイルの一覧を確認する
    - `git diff --name-only --diff-filter=U`
6. コンフリクトが起きた各ファイルについて、mainブランチ側の変更内容を確認する
    - `git diff $(git merge-base HEAD origin/main)..origin/main -- <コンフリクトファイル>`
7. mainブランチの変更と、現在のブランチの変更意図をどちらも考慮し、妥当なコンフリクト解消を行う
    - 統合の判断に迷う場合は、ユーザーに確認する
8. コンフリクトを解消したら処理を継続する
    - merge の場合: `git add <解消したファイル>` の後に `git merge --continue`
    - rebase の場合: `git add <解消したファイル>` の後に `git rebase --continue`
