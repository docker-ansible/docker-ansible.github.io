# Changelog

This page tracks changes **across the Docker Ansible ecosystem** — the core
container images, the GitHub Action, and the testing projects — and points you
at the current source tag or formal release of each.

## Documentation site releases

### v1.1.3 - 2026-11-21

- Updated Docker Ansible Test from `v2.7.5` to `v2.7.6`.
- Corrected the 25-entry test matrix and the `2.22-debian-trixie` latest alias.
- Removed the obsolete 2.22 action-test coverage gap after upstream test coverage
  was restored.

### v1.1.2 - 2026-11-20

- Refreshed the upstream repository snapshot to the latest verified `main`
  commits and formal releases.
- Added scheduled and `repository_dispatch` rebuild triggers for upstream
  documentation changes.
- Added a bounded upstream snapshot synchronizer for the testing page.
- Updated the action and action-test release references after upstream 2.22
  matrix coverage was restored.

### v1.1.0 - 2026-11-16

- Refreshed image patch versions, core release metadata, and current project/test
  snapshots against the upstream repositories.
- Clarified active core support versus legacy tags retained by the action-test
  compatibility matrix.
- Updated runnable examples and linked current successful test workflow runs.

## Current tags and releases at a glance

| Project | Current tag/release | What it is | Release notes |
| --- | --- | --- | --- |
| [Docker Ansible](https://github.com/willhallonline/docker-ansible) | **v6.5.0** | The core container images (`willhallonline/ansible`) | [Release](https://github.com/willhallonline/docker-ansible/releases/tag/v6.5.0) |
| [Docker Ansible GitHub Action](https://github.com/willhallonline/docker-ansible-github-action) | **v1.1.2** | GitHub Action running Ansible via the images | [Releases](https://github.com/willhallonline/docker-ansible-github-action/releases) |
| [Docker Ansible Test](https://github.com/willhallonline/docker-ansible-test) | **v2.7.6** | Systemd image builds and `ansible-playbook --version` smoke tests | [Tags](https://github.com/willhallonline/docker-ansible-test/tags) |
| [Docker Ansible GitHub Action Test](https://github.com/willhallonline/docker-ansible-github-action-test) | **integration-test v1.1.1** | Workflows exercising the GitHub Action | [Release](https://github.com/willhallonline/docker-ansible-github-action-test/releases/tag/v1.1.1) |

!!! tip "Checking for newer releases"
    This table is a snapshot. Each project's **Releases** or **Tags** page on
    GitHub is the source of truth — the links above point at the live data.

## Per-project changelogs

### Docker Ansible

The canonical changelog is maintained in the upstream repository:
[CHANGELOG.md](https://github.com/willhallonline/docker-ansible/blob/main/CHANGELOG.md)

Recent highlights (v6.4.3–v6.5.0):

- added Ansible Core 2.22.0 / Ansible 15.0.0 for Alpine 3.24, Debian Trixie,
  Debian Trixie Slim, and Ubuntu 26.04;
- advanced the `latest` and `alpine` convenience tags to Ansible 2.22 while
  retaining `ubuntu` on Ansible 2.21;
- added Alpine 3.23 and 3.24 support;
- kept the active matrix on Alpine 3.21 through 3.24;
- added `HEALTHCHECK` instructions to active images;
- switched dependency installation from `pip`/`pipx` to `uv`;
- added the non-root `ansible` user and updated the SSH home to
  `/home/ansible/.ssh`;
- removed end-of-life Ansible core 2.16 and 2.17 from active image builds;
- added the Image Matrix Maintainer and Build Failure Triager Copilot agents;
- updated Ansible core to 2.18.20, 2.19.15, 2.20.11, 2.21.6, and 2.22.0;
- builds generally target Linux AMD64 and ARM64, with tag-specific exceptions.

The current default branch and `v6.5.0` release contain these refreshed patch
versions.

The current Ansible core lines shipped in the images are 2.18 through 2.22 —
see [supported tags](../images/tags.md) for the full matrix. The action-test
repository retains 2.16/2.17 tags for compatibility testing and is not the
active core image support matrix.

### Docker Ansible GitHub Action

![GitHub release](https://img.shields.io/github/v/release/willhallonline/docker-ansible-github-action)

**v1.1.2** updates deployment documentation and smoke tests to the current
`2.22-alpine-3.24` image and clarifies exact-version tag pinning. v1.1.1
retries transient Docker image pulls up to three total attempts and refreshes
the documentation link and pinned image reference.
See the
[Docker Ansible GitHub Action](../projects/github-action.md) page and the
[action repository](https://github.com/willhallonline/docker-ansible-github-action/releases)
for current inputs and examples. Pin `@v1.1.2` or a commit SHA for a stable
workflow; the repository also publishes the `v1` major-version tag.

### Docker Ansible Test and Docker Ansible GitHub Action Test

- **Docker Ansible Test** (latest tag **v2.7.6**) — systemd image builds and
  `ansible-playbook --version` smoke tests for the images themselves.
- **Docker Ansible GitHub Action Test** (integration-test **v1.1.1**) —
  a 65-tag compatibility matrix (three aliases plus 62 versioned tags) with
  45 current Ansible 2.18–2.22 tags and aliases plus 20 retained Ansible
  2.16/2.17 tags. Ansible 2.9–2.15 are excluded. See the upstream
  [supported-tags table](https://github.com/willhallonline/docker-ansible#supported-tags-and-respective-dockerfile-links)
  and [test workflow](https://github.com/willhallonline/docker-ansible-github-action-test/blob/main/.github/workflows/test.yml)
  for the active source matrices; the workflow provides localhost/non-root/
  exit-code smoke coverage and is not the active core image matrix.

See [Docker Ansible Test](../projects/testing.md) for how these fit together.

## What changes over time

The Docker Ansible ecosystem changes when Ansible releases, base images, CI
platforms, or dependency policies change.

Typical changes include:

- adding new Ansible versions;
- refreshing Python dependencies;
- adding new base operating-system versions;
- retiring old base images and Ansible streams from the active matrix;
- adjusting CI workflows;
- updating `ansible-lint` and supporting packages;
- documenting compatibility notes.

## Current notable themes

Recent project direction includes these broad changes:

| Area | Summary |
| --- | --- |
| Ansible versions | Current images ship ansible-core 2.18.20 through 2.22.0. |
| Alpine bases | Alpine 3.21 through 3.24 are supported in the active matrix. |
| Ubuntu bases | Ubuntu 26.04 is available alongside Ubuntu 24.04. |
| Debian bases | Debian Trixie variants are available alongside Bookworm variants. |
| Rocky Linux | Rocky Linux 10 is available as a RHEL-family base. |
| Older bases | Older bases and Ansible lines are outside the active matrix over time. |

No dated release entries are reproduced here because the upstream changelog
should remain the canonical history.

## Versioning model

Image tags are generally intended to communicate the Ansible version and the base
operating-system variant. For example, production users should prefer an explicit
Ansible-version and base-OS tag over a floating tag.

```text
willhallonline/ansible:2.22.0-alpine-3.24
willhallonline/ansible:2.22.0-debian-trixie
```

!!! note "Digest pinning"
    Tags can be rebuilt. If you need byte-for-byte repeatability, pin a digest:
    `willhallonline/ansible@sha256:<digest>`.

## Rebuild cadence

The upstream repository includes Renovate configuration for automated dependency
updates. This supports regular rebuilds when relevant dependencies, Ansible
versions, or base images change.

Regular rebuilds are useful because they can pick up:

- base image security fixes;
- Python package updates;
- Ansible patch releases;
- CI workflow updates;
- Docker metadata changes.

## Legacy policy

Ansible core streams 2.9 through 2.17 are outside the active core image matrix
and unmaintained. The action-test project may retain selected 2.16/2.17 tags
for compatibility coverage; verify any legacy reference in the upstream
repository and registry.

## How to evaluate an upgrade

When moving to a newer image tag:

1. read the upstream changelog;
2. check Ansible porting guides for the version jump;
3. run `ansible --version` with the new image;
4. run `ansible-lint` against your project;
5. run `ansible-playbook --syntax-check`;
6. test a representative playbook against non-production targets;
7. pin the chosen tag or digest in CI.

## Example validation commands

```bash
docker run --rm willhallonline/ansible:2.21.6-debian-trixie ansible --version
```

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.6-debian-trixie   ansible-lint
```

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.6-debian-trixie   ansible-playbook --syntax-check -i inventory site.yml
```

## Related documentation

- [Docker Ansible](../projects/docker-ansible.md)
- [Docker Ansible Test](../projects/testing.md)
- [Security](security.md)
- [FAQ](faq.md)
