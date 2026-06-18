# Xcode を開く

1. カレントディレクトリで `scripts/open-first-xcodeproj.sh` を実行する。
   - 特定の Swift ファイルをエディターで開きたい場合は第2引数にファイルの絶対パスを渡す（例: `scripts/open-first-xcodeproj.sh . /path/to/Foo.swift`）
2. 終了コードと標準エラー出力を確認する。

プロジェクトファイルが見つからない場合は、その旨を伝えて探索起点を確認する。
