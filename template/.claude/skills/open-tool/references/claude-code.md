# Claude Code を開く

Claude CodeをTerminalの新規タブで開く。
下記のスクリプトを参考に対象のディレクトリで、`claude` コマンドを実行する。
ディレクトリの指定がない場合はカレントディレクトリで実行する。

```shell
# 参考スクリプト
osascript -e '
tell application "Terminal"
    activate
    tell application "System Events"
        keystroke "t" using command down
    end tell
    delay 0.3
    do script "cd \"~/Developer/example-project\" && claude" in selected tab of front window
end tell
'
```

## パーミッション設定
タブで開くにはOSのパーミッション設定が必要。
必要に応じてユーザーにパーミッション設定を依頼する。
