#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="create-worktree.py",
        description="Create a git worktree for a branch with optional local asset copy.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Notes:\n"
            "  - --branch is required.\n"
            "  - If the branch exists locally, it is attached as-is.\n"
            "  - If the branch exists only on one remote, a local tracking branch is created.\n"
            "  - Otherwise a new branch is created from --base.\n"
            "  - When --base is main and origin/main exists, the script fetches origin and uses origin/main."
        ),
    )
    parser.add_argument("--branch", required=True, help="Branch name to use for the worktree.")
    parser.add_argument("--base", default="main", help="Base ref when creating a new branch. Default: main.")
    return parser


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def run_command(args: list[str], capture_output: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=capture_output)


def git_output(repo_root: Path, *git_args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *git_args],
        check=True,
        text=True,
        capture_output=True,
    )
    return completed.stdout.strip()


def git_success(repo_root: Path, *git_args: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *git_args],
        check=False,
        text=True,
        capture_output=True,
    )
    return completed.returncode == 0


def git_lines(repo_root: Path, *git_args: str) -> list[str]:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), *git_args],
        check=True,
        text=True,
        capture_output=True,
    )
    return [line for line in completed.stdout.splitlines() if line]


def set_branch_upstream(repo_root: Path, branch_name: str, remote_name: str) -> None:
    run_command(["git", "-C", str(repo_root), "config", f"branch.{branch_name}.remote", remote_name])
    run_command(["git", "-C", str(repo_root), "config", f"branch.{branch_name}.merge", f"refs/heads/{branch_name}"])


def parse_worktree_porcelain(output: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue

        key, _, value = line.partition(" ")
        current[key] = value

    if current:
        entries.append(current)

    return entries


def ref_contains_path(repo_root: Path, git_ref: str, relative_path: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(repo_root), "cat-file", "-e", f"{git_ref}:{relative_path}"],
        check=False,
        text=True,
        capture_output=True,
    )
    return completed.returncode == 0


def find_remote_tracking_refs(repo_root: Path, branch_name: str) -> list[str]:
    remote_refs = git_lines(repo_root, "for-each-ref", "--format=%(refname:short)", "refs/remotes")
    suffix = f"/{branch_name}"
    return [ref for ref in remote_refs if ref.endswith(suffix) and not ref.endswith("/HEAD")]


def resolve_worktrees_dir(current_worktree_root: Path, repo_name: str) -> Path:
    expected_name = f"{repo_name}-worktrees"
    parent_dir = current_worktree_root.parent
    if parent_dir.name == expected_name:
        return parent_dir
    return parent_dir / expected_name


def remove_path(path: Path) -> None:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink()


def copy_item(
    source_root: Path,
    target_path: Path,
    relative_path: str,
    copied_items: list[str],
    skipped_items: list[str],
) -> None:
    source_path = source_root / relative_path
    destination_path = target_path / relative_path

    if not source_path.exists():
        skipped_items.append(f"{relative_path} (source missing)")
        return

    if destination_path.exists():
        remove_path(destination_path)

    run_command(["mkdir", "-p", str(destination_path.parent)])

    if source_path.is_dir():
        shutil.copytree(source_path, destination_path)
    else:
        shutil.copy2(source_path, destination_path)

    copied_items.append(relative_path)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_candidate = Path.cwd()
    if not git_success(repo_candidate, "rev-parse", "--show-toplevel"):
        fail(f"Git repository not found: {repo_candidate}")

    current_worktree_root = Path(git_output(repo_candidate, "rev-parse", "--show-toplevel"))
    source_root = current_worktree_root
    common_git_dir = Path(git_output(repo_candidate, "rev-parse", "--git-common-dir"))
    if not common_git_dir.is_absolute():
        common_git_dir = (current_worktree_root / common_git_dir).resolve()

    repo_root = common_git_dir.parent if common_git_dir.name == ".git" else current_worktree_root
    repo_name = repo_root.name
    worktrees_dir = resolve_worktrees_dir(current_worktree_root, repo_name)
    branch_name = args.branch
    worktree_dir_name = branch_name.replace("/", "-")
    target_path = worktrees_dir / worktree_dir_name

    notes: list[str] = []
    copied_items: list[str] = []
    skipped_items: list[str] = []
    existing_branch_source_ref: str | None = None
    existing_branch_is_local = False
    create_new_branch = False

    if current_worktree_root.parent == worktrees_dir:
        notes.append(f"Using current parent directory as the worktrees root: {worktrees_dir}")

    if git_success(repo_root, "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"):
        existing_branch_is_local = True
        existing_branch_source_ref = branch_name

        worktree_entries = parse_worktree_porcelain(git_output(repo_root, "worktree", "list", "--porcelain"))
        if any(entry.get("branch") == f"refs/heads/{branch_name}" for entry in worktree_entries):
            fail(f"Existing branch is already checked out in another worktree: {branch_name}")
    else:
        remote_tracking_refs = find_remote_tracking_refs(repo_root, branch_name)
        if len(remote_tracking_refs) > 1:
            fail(f"Branch is ambiguous across remotes: {branch_name}")
        if remote_tracking_refs:
            existing_branch_source_ref = remote_tracking_refs[0]
            notes.append(f"Using remote-tracking branch {existing_branch_source_ref} for initial checkout")
        else:
            create_new_branch = True

    if target_path.exists():
        fail(f"Target path already exists: {target_path}")

    worktree_entries = parse_worktree_porcelain(git_output(repo_root, "worktree", "list", "--porcelain"))
    if any(Path(entry.get("worktree", "")) == target_path for entry in worktree_entries):
        fail(f"Worktree already registered for path: {target_path}")

    effective_base = args.base
    if create_new_branch and args.base == "main" and git_success(repo_root, "remote", "get-url", "origin"):
        fetch_result = subprocess.run(
            ["git", "-C", str(repo_root), "fetch", "--prune", "origin"],
            check=False,
            text=True,
            capture_output=True,
        )
        if fetch_result.returncode == 0 and git_success(repo_root, "show-ref", "--verify", "--quiet", "refs/remotes/origin/main"):
            effective_base = "origin/main"
            notes.append("Fetched origin and used origin/main as the base ref")
        elif fetch_result.returncode != 0:
            notes.append("Fetch from origin failed; used local main as the base ref")

    target_ref_for_mise = effective_base if create_new_branch else (branch_name if existing_branch_is_local else existing_branch_source_ref)
    target_has_mise_toml = ref_contains_path(repo_root, target_ref_for_mise, "mise.toml")
    if target_has_mise_toml and shutil.which("mise") is None:
        fail("mise command not found")

    run_command(["mkdir", "-p", str(worktrees_dir)])

    if create_new_branch:
        run_command(
            ["git", "-C", str(repo_root), "worktree", "add", "--no-track", "-b", branch_name, str(target_path), effective_base],
        )
        if git_success(repo_root, "remote", "get-url", "origin"):
            set_branch_upstream(repo_root, branch_name, "origin")
            notes.append(f"Configured upstream as origin/{branch_name}")
    else:
        if existing_branch_is_local:
            run_command(["git", "-C", str(repo_root), "worktree", "add", str(target_path), branch_name])
        else:
            run_command(
                [
                    "git",
                    "-C",
                    str(repo_root),
                    "worktree",
                    "add",
                    "--track",
                    "-b",
                    branch_name,
                    str(target_path),
                    existing_branch_source_ref,
                ],
            )

    run_command(["mkdir", "-p", str(target_path / ".user")])

    for relative_path in ["Carthage", "syukatsu-kaigi-ios/Config/Secrets.xcconfig", "SKApollo"]:
        copy_item(
            source_root=source_root,
            target_path=target_path,
            relative_path=relative_path,
            copied_items=copied_items,
            skipped_items=skipped_items,
        )

    mise_status = "no mise.toml"
    if target_has_mise_toml:
        run_command(["mise", "trust", str(target_path / 'mise.toml')])
        mise_status = "trusted"

    print(f"Branch: {branch_name}")
    print(f"Worktree path: {target_path}")
    print(f"Worktrees root: {worktrees_dir}")
    if create_new_branch:
        print(f"Mode: create new branch from {effective_base}")
    else:
        print("Mode: attach existing branch")

    print("Copied:")
    if copied_items:
        for item in copied_items:
            print(f"  - {item}")
    else:
        print("  - none")

    print("Skipped copies:")
    if skipped_items:
        for item in skipped_items:
            print(f"  - {item}")
    else:
        print("  - none")

    print(f"mise trust: {mise_status}")

    if notes:
        print("Notes:")
        for note in notes:
            print(f"  - {note}")

    print("\nCurrent worktrees:")
    subprocess.run(["git", "-C", str(repo_root), "worktree", "list"], check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())