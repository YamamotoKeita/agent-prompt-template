# AIエージェント向けプロンプトテンプレート

開発で汎用的に使えるAIエージェント向けプロンプトのテンプレート。
`template` 以下のファイルを各プロジェクトに適用する。

## 構成

```
template/
├── CLAUDE.md                      # 毎セッション読み込まれるエージェントへの基本指示
├── CLAUDE_mdの書き方.md            # CLAUDE.md の書き方ガイド
├── .claude/
│   ├── agent-document-rules.md     # AIエージェント向けのドキュメント指示
│   ├── agents/                     # カスタムエージェントの定義
│   ├── rules/                      # 特定のファイルパスに対する指示
│   └── skills/                     # Agent Skills。エージェント向けの各種操作の手順書
└── docs/                           # プロジェクトの情報。CLAUDE.md にリンクの形で参照させる。
    ├── プロジェクト概要.md            # プロジェクトの概要
    ├── プロジェクト用語集.md          # プロジェクトの用語集
    ├── 外部サービス.md               # 利用する外部サービス
    └── git-rules.md                # Gitブランチ運用・命名・コミットルール
```

## 汎用 Agent Skills

`template/.claude/skills/` 以下には、プロジェクトを問わず汎用的に利用できそうな以下のAgent Skills を配置している。

- create-skill - Agent Skillを作る
- interview - 計画や仕様の詳細を詰める。エッジケースの考慮漏れなどを検出
- git - commit / push / merge / コンフリクト解消などのGit操作
- github - PRの作成など
- open-tool - 各種IDEやエディタ、ブラウザ、Diffなどを立ち上げる

## プロジェクト固有の Agent Skill

汎用スキルの他に、以下のようなプロジェクト固有の基本操作を行う Agent Skills があると望ましい。

- setup - 開発環境を構築する
- build - ビルドする
- run-tests - ユニットテストを実行する
- run-ui-tests - UIテストを実行する
- launch-ui - UIを起動してエージェントがUI操作を行う。
- lint - 静的コードチェック
- documents - ドキュメントの閲覧・検索・作成・更新（エクセル、Kibela、Googleドキュメントなど）
- issues - Issueの閲覧・検索・作成・更新
- read-design - デザインファイルの読み込み（Figma など）

## Progressive Disclosure (段階的開示)

エージェント向けプロンプトの整理には `Progressive Disclosure`(段階的開示) が役立つ。
`Progressive Disclosure` では具体的な詳細を別ファイルに分離して、プロンプトにそのファイルへのリンクを記載することで、情報を段階的に開示する。

例えば、常に読み込まれる `CLAUDE.md` に詳細かつ具体的な情報を記載しても、多くの作業では使われることがなく無駄にコンテキストを汚してしまう。
`CLAUDE.md` には以下のように各種詳細ドキュメントのリンクを書くに留めておけば、さほどコンテキストを使わず、エージェントは必要に応じてドキュメントを見に行くことができる。

```markdown
必要に応じて以下のドキュメントを参照すること。
- docs/プロジェクト概要.md
- docs/プロジェクト用語集.md
- docs/外部サービス.md
- docs/git-rules.md
```

`Progressive Disclosure` は Agent Skills でも使うことができる。
細かな Agent Skills が増えすぎると管理が煩雑かつ、エージェントの混乱を招くため、一つのスキルの粒度を大きめにして関連したいくつかの操作を `Progressive Disclosure` で記載することができる。
例えば、`git-commit`・`git-diff`・`git-merge` スキルをそれぞれ作る代わりに、`git` スキルの中に各操作を `Progressive Disclosure` で記載すれば、Skillの管理が楽になる。

## GitHub Copilot への適用

GitHub Copilot は標準で Claude Code 向けのこれらのファイルを読み込むため、特別な設定はなくてもこれらのファイルを利用できる。
ただし、2026年6月現在 Copilot Review は CLAUDE.md を見てくれないので注意。
