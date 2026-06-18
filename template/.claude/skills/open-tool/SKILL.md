---
name: open-tool
description: 外部ツールを開く。Xcode、Claude Code、VS Code、Webページ、テキストファイル、コードDiffなど。何かを開く操作を依頼された際に使用。開く、表示する、ブラウザで開く、エディタで開く、diffを見る場合に使用。
---

1. 何を開く依頼かを判定する。
2. 対応する reference を読む。
3. 利用可能なツールと現在の環境に合わせて最短手順で開く。
4. 開けない場合は、足りない前提条件を簡潔に伝える。

対象別 reference:

- Xcode: [references/xcode.md](references/xcode.md)
- Claude Code: [references/claude-code.md](references/claude-code.md)
- VS Code: [references/vscode.md](references/vscode.md)
- Webページ: [references/web-page.md](references/web-page.md)
- テキストファイル: [references/text-file.md](references/text-file.md)
- コードDiff: [references/code-diff.md](references/code-diff.md)

複数候補があり曖昧な場合は、最小限の確認だけ行う。

## 注意
scripts や references へのパスは、スキルルート (SKILL.md が置かれているディレクトリ) を基準にした相対パスで記載されている。エージェントの作業ディレクトリからの相対パスとして解釈してはならないので注意する。
スクリプトを実行する場合は、まずスキルルートを基準にパスを解決し、その解決済みの絶対パスを実行する。