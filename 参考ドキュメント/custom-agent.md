# Claude Code カスタムエージェント（Agent File）の書き方

Claude Code CLI のカスタムエージェント定義方法のリファレンス。
`.claude/agents/*.md` に置く Markdown ファイルでエージェントを定義する。

出典: https://code.claude.com/docs/en/subagents.md および CLI reference

## 概要

- 1ファイル＝1エージェント。`.claude/agents/<name>.md`
- ファイルは **YAML front-matter ＋ Markdown body** の2部構成
- **body がそのままエージェントの system prompt** になる
- サブエージェント（委任先）としても、`claude --agent <name>` で **メインセッションのエージェント**としても起動できる

## ファイル配置と優先度

優先度の高い順:

1. managed settings（最高）
2. `--agents` CLI のインライン JSON 定義（セッション限定）
3. `.claude/agents/`（プロジェクト）
4. `~/.claude/agents/`（ユーザー）
5. プラグインの `agents/`（最低）

- サブフォルダで整理可能（例: `.claude/agents/review/security.md`）。識別は `name` フィールドのみで行われ、パスは関係しない。
- ファイルを直接編集した場合は **セッション再起動が必要**。`/agents` コマンドで対話的に作成・編集した場合は即時反映。

## front-matter フィールド一覧

| フィールド | 必須 | 型 | 意味 | デフォルト |
|---|---|---|---|---|
| `name` | **必須** | 文字列 | ユニークな識別子（小文字・ハイフン） | — |
| `description` | **必須** | 文字列 | 目的・委譲のトリガーとなる自然言語説明 | — |
| `tools` | 任意 | カンマ区切り文字列 | 利用可能なツール（allowlist） | 全ツール継承 |
| `disallowedTools` | 任意 | カンマ区切り文字列 | 除外するツール（denylist） | — |
| `model` | 任意 | 文字列 | `opus` / `sonnet` / `haiku` / `fable` / フルID / `inherit` | `inherit` |
| `permissionMode` | 任意 | 文字列 | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` | 親セッション継承 |
| `maxTurns` | 任意 | 整数 | エージェント実行の最大ターン数 | — |
| `skills` | 任意 | YAML 配列 | プリロードするスキル名リスト | 実行時に発見して読み込み |
| `mcpServers` | 任意 | YAML 配列 | MCP サーバー定義・参照 | — |
| `hooks` | 任意 | YAML オブジェクト | ライフサイクルフック定義 | — |
| `memory` | 任意 | 文字列 | `user` / `project` / `local` | — |
| `background` | 任意 | 真偽値 | `true` でバックグラウンド実行 | `false` |
| `effort` | 任意 | 文字列 | `low` / `medium` / `high` / `xhigh` / `max` | セッション継承 |
| `isolation` | 任意 | 文字列 | `worktree` で独立作業ツリー化 | — |
| `color` | 任意 | 文字列 | UI 表示色（`red` / `blue` / `green` / `yellow` / `purple` / `orange` / `pink` / `cyan`） | — |
| `initialPrompt` | 任意 | 文字列 | 起動時に自動投入される初期プロンプト（**メイン起動時のみ有効**） | — |

> ⚠️ プラグイン配下のエージェント（`plugins/agents/`）は `hooks` / `mcpServers` / `permissionMode` をサポートしない。

## body（Markdown 本文）

- front-matter の下の本文が **エージェントの system prompt** になる。
- ここにエージェントの役割・振る舞い・手順を書く。
- `memory` を有効にした場合などは、メモリ管理の指示が system prompt に自動で追加される。

## `tools` の書き方

- **カンマ区切り文字列**（YAML 配列ではない）:
  ```yaml
  tools: Read, Glob, Grep
  ```
- 省略時はすべてのツールを継承。
- MCP ツールは `mcp__<server>` または `mcp__<server>__*` で指定。
- サブエージェント委任の制限は `Agent(worker, researcher)` のように書く（**メインセッションエージェント起動時のみ有効**）。

## `model` の書き方

- 有効な値:
  - エイリアス: `opus` / `sonnet` / `haiku` / `fable`
  - フル model ID: `claude-opus-4-8` / `claude-sonnet-4-6` など
  - `inherit`: 親セッションと同じモデル
- デフォルトは `inherit`。
- 解決順序（上が優先）:
  1. `CLAUDE_CODE_SUBAGENT_MODEL` 環境変数
  2. 呼び出し時の `model` パラメータ
  3. front-matter の `model`
  4. 親セッションのモデル

## CLI 起動オプション

### `--agent` — 定義済みエージェントをメイン起動

```bash
claude --agent <name>
```

`.claude/agents/` および `~/.claude/agents/` から `name:` が一致するエージェントを探してメインセッションとして起動する。

### `--agents` — インライン JSON 定義（セッション限定）

```bash
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'
```

front-matter と同じフィールド名を受け付ける。system prompt は `prompt` フィールドで指定する（body に相当）。

## 最小の完全なサンプル

`.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

起動:

```bash
claude --agent code-reviewer
```
