# コードDiffを開く

指定されたDiffを開く。
特に何と何のDiffを見るか指定がない場合は、以下の優先順位で開く。

1. 未コミットの全ての変更
2. 派生元ブランチとの差分

## difit

基本は[difit](https://github.com/yoshiko-pg/difit) で開く。

```shell
npx difit  # View the latest commit diff in WebUI
```

### Basic Usage
difit <target>                    # View single commit diff
difit <target> [compare-with]     # Compare two commits/branches

### Single commit review
difit          # HEAD (latest) commit
difit 6f4a9b7  # Specific commit
difit feature  # Latest commit on feature branch

### Compare two commits
difit @ main         # Compare with main branch (@ is alias for HEAD)
difit feature main   # Compare branches
difit . origin/main  # Compare working directory with remote main

### Special Arguments
difit supports special keywords for common diff scenarios:

difit .        # All uncommitted changes (staging area + unstaged)
difit staged   # Staging area changes
difit working  # Unstaged changes only

### GitHub PR
difit --pr https://github.com/owner/repo/pull/123