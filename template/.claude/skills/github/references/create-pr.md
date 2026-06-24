# プルリクエストの作成手順

`.github/pull_request_template.md` がある場合必ず確認し、テンプレートの通りにPRを作成すること。

## 未コミット、未PUSHの変更がある場合
ローカルに未コミット、未PUSHの変更がある場合、人間にコミット、PUSHして良いかまず確認する。

## PR 作成
`gh pr create` でPRを作成した後、`gh api` で本文をテンプレートに沿って更新する。
`gh pr create` の `--body` オプションは正しく反映されない場合があるため、必ず `gh api` で上書きする。

```bash
# PR作成（本文は空でOK）
gh pr create --title "タイトル" --body ""

# .github/pull_request_template.md に従って本文を更新
gh api repos/{OWNER}/{REPOSITORY}/pulls/{PR番号} \
  --method PATCH \
  --field body='...'
```

## PRのタイトル
Issueの内容と変更内容を確認した上で、適切なタイトルを付ける。

## 概要、対応内容
Issueの内容とブランチでの変更内容を見た上で記載する。

## 確認方法
Issue内容と変更内容から分かる範囲で記載する。
確認方法が不明な場合は空欄とする。
