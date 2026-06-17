# 開発で汎用的に使えるSkill

ユーティリティー系はProgressive Disclosureを積極的に利用して、一つのSkillで様々な操作ができるようにする。

## 汎用ユーティリティー
- ✅ create-skill: Agent Skillを作る
- ✅ git - commit / push / merge / コンフリクト解消などのGit操作
- ❌ github - PRの作成など
- ❌ open-tool - 各種IDEやブラウザなど、エージェントから別Windowを立ち上げる
- ❌ interview - 計画の詳細を詰める。見落としがちなエッジケースの考慮漏れなどを検出
- ❌ search-skill: 既定のマーケットプレイスなどからAgent Skillを検索する

## プロジェクトユーティリティー
以下はプロジェクトに応じて設定する。

- ⚠️ setup: 開発環境を構築する。最初にプロジェクト向けにAgent Skillsをセットアプする。
- ⚠️ build - ビルドする
- ⚠️ run-test - ユニットテストを実行する
- ⚠️ run-ui-test - UIテストを実行する
- ⚠️ analyze-code - 静的にできるコード解析。Lintチェックなどを想定

## ドキュメント系
以下はプロジェクトに応じて設定する。

- ⚠️ documents: 外部ドキュメントの検索・閲覧・作成・更新（Kibela/Notion等、PJごとに接続先を設定）
- ⚠️ issues: Issueの検索・閲覧・作成・更新
- ⚠️ design
- ⚠️ deploy

## 参考

他に以下なども参考に
https://github.com/addyosmani/agent-skills

Excel・Word・PDFなどの読み取りSkill
https://github.com/anthropics/skills