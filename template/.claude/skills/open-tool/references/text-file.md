# テキストファイルを開く

## 共通フロー

1. 開く対象のファイルパスを決める。
2. 対象ファイルが存在することを確認する。
3. OS で `*.txt` をデフォルトで開くよう設定されているアプリケーションを特定する。
4. 対象ファイルの実際の拡張子は使わず、手順 3 で特定した `*.txt` 用のアプリケーションを明示して開く。
5. 対象ファイルをそのアプリケーションに渡して開く。
6. 終了コードと標準エラー出力を確認する。

対象ファイルの拡張子に関連付けられた別アプリケーションがあっても、それは使わない。
`*.txt` の既定アプリケーションを特定できない場合は、その旨を伝えて前提条件を確認する。

## macOS で `*.txt` の既定アプリケーションを特定する

1. LaunchServices から `*.txt` の既定アプリケーションを取得する。次のコマンドでアプリケーションの絶対パスを特定する。

```sh
swift -e 'import Foundation; import CoreServices; import UniformTypeIdentifiers; if let type = UTType(filenameExtension: "txt"), let appCFURL = LSCopyDefaultApplicationURLForContentType(type.identifier as CFString, .all, nil)?.takeRetainedValue() { print((appCFURL as URL).path) } else { fputs("not found\n", stderr); exit(1) }'
```

2. 手順 1 の結果が空または失敗の場合は、`~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist` の `public.plain-text` 関連付けを確認して補助的に調べる。

```sh
plutil -p ~/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist | rg -n 'public\.plain-text|LSHandlerRoleAll' -C 2
```

3. 手順 1 または手順 2 で特定した `*.txt` 用のアプリケーションパスを保持する。
4. 共通フローの手順 4 以降でそのアプリケーションパスを使う。

```sh
open -a "$txt_default_app" "$target_file"
```