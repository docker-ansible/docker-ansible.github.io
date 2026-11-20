#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


REPOSITORIES = (
    ("Docker Ansible", "willhallonline/docker-ansible"),
    ("Docker Ansible Test", "willhallonline/docker-ansible-test"),
    ("Docker Ansible GitHub Action", "willhallonline/docker-ansible-github-action"),
    (
        "Docker Ansible GitHub Action Test",
        "willhallonline/docker-ansible-github-action-test",
    ),
)

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs/projects/testing.md"


def github_json(path):
    request = Request(
        f"https://api.github.com/{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "docker-ansible-docs",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def snapshot():
    rows = []
    for name, repo in REPOSITORIES:
        branch = github_json(f"repos/{repo}/branches/main")
        sha = branch["commit"]["sha"]
        try:
            release = github_json(f"repos/{repo}/releases/latest")
            tag = release["tag_name"]
        except Exception:
            tag = "No release"
        rows.append(
            f"| {name} | [`{sha}`](https://github.com/{repo}/commit/{sha}) | `{tag}` |"
        )
    return rows


def update_page(rows):
    text = PAGE.read_text(encoding="utf-8")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = text.splitlines()

    for index, line in enumerate(lines):
        if line.startswith("is `v1.1.0`. The current default-branch snapshot, verified on"):
            lines[index] = (
                f"is `v1.1.0`. The current default-branch snapshot, "
                f"verified on {date}, is:"
            )
            break

    start = next(
        i
        for i, line in enumerate(lines)
        if line.startswith("| Project | `main` commit |")
    )
    end = start + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    lines[start + 2 : end] = rows
    PAGE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    rows = snapshot()
    before = PAGE.read_text(encoding="utf-8")
    update_page(rows)
    changed = PAGE.read_text(encoding="utf-8") != before
    if "--check" in sys.argv:
        if changed:
            print("Upstream snapshot is stale:", file=sys.stderr)
            print("\n".join(rows), file=sys.stderr)
            raise SystemExit(1)
        print("Upstream snapshot is current")
    elif changed:
        print("Updated upstream snapshot")
    else:
        print("Upstream snapshot is already current")


if __name__ == "__main__":
    main()
