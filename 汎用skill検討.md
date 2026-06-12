# 開発で汎用的に使えるSkillの検討

ユーティリティー系はProgressive Disclosureを積極的に利用して、一つのSkillで様々な操作ができるようにする。

## 共通
- create-skill: Agent Skillを作る

## ユーティリティー
- git: commit / push / merge / コンフリクト解消などのGit操作
- open-tool: 各種IDEやブラウザなど、エージェントから別Windowを立ち上げる
- github: PRの作成など
- search-skill: 既定のマーケットプレイスなどからAgent Skillを検索する
- interview: 計画の詳細を詰める。見落としがちなエッジケースの考慮漏れなどを検出

## プロジェクトユーティリティー
- setup: 最初にプロジェクト向けにAgent Skillsをセットアプする。開発環境を構築する。
- build: ビルドする
- run-test: ユニットテストを実行する
- run-ui-test: UIテストを実行する
- analyze-code: 静的にできるコード解析。Lintチェックなどを想定
- deploy

## ドキュメント系
- documents: 外部ドキュメントの検索・閲覧・作成・更新（Kibela/Notion等、PJごとに接続先を設定）
- issues: Issueの検索・閲覧・作成・更新

## 参考

他に以下なども参考に
https://github.com/addyosmani/agent-skills

Excel・Word・PDFなどの読み取りSkill
https://github.com/anthropics/skills