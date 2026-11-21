#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


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
    environment = os.environ.copy()
    if environment.get("GITHUB_TOKEN") and not environment.get("GH_TOKEN"):
        environment["GH_TOKEN"] = environment["GITHUB_TOKEN"]
    result = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github+json", path],
        check=True,
        capture_output=True,
        text=True,
        env=environment,
    )
    return json.loads(result.stdout)


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


def rendered_page(rows):
    text = PAGE.read_text(encoding="utf-8")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = text.splitlines()

    for index, line in enumerate(lines):
        marker = "The current default-branch snapshot, verified on"
        if marker in line:
            prefix = line.split(marker, 1)[0]
            lines[index] = f"{prefix}{marker} {date}, is:"
            break

    start = next(
        i for i, line in enumerate(lines)
        if line.startswith("| Project | `main` commit |")
    )
    end = start + 1
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    lines[start + 2 : end] = rows
    return "\n".join(lines) + "\n"


def main():
    rows = snapshot()
    before = PAGE.read_text(encoding="utf-8")
    rendered = rendered_page(rows)
    changed = rendered != before
    if "--check" in sys.argv:
        if changed:
            print("Upstream snapshot is stale:", file=sys.stderr)
            print("\n".join(rows), file=sys.stderr)
            raise SystemExit(1)
        print("Upstream snapshot is current")
    elif changed:
        PAGE.write_text(rendered, encoding="utf-8")
        print("Updated upstream snapshot")
    else:
        print("Upstream snapshot is already current")


if __name__ == "__main__":
    main()
