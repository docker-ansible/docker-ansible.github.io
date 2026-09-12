# Changelog

This page tracks changes **across the Docker Ansible ecosystem** — the core
container images, the GitHub Action, and the testing projects — and points you
at the latest release of each.

## Latest tags and releases at a glance

| Project | Latest tag/release | What it is | Release notes |
| --- | --- | --- | --- |
| [docker-ansible](https://github.com/willhallonline/docker-ansible) | **v6.4.8** | The core container images (`willhallonline/ansible`) | [Tags](https://github.com/willhallonline/docker-ansible/tags) |
| [docker-ansible-github-action](https://github.com/willhallonline/docker-ansible-github-action) | **v1.1.0** | GitHub Action running Ansible via the images | [Releases](https://github.com/willhallonline/docker-ansible-github-action/releases) |
| [docker-ansible-test](https://github.com/willhallonline/docker-ansible-test) | **v2.7.3** | Test playbooks exercising the images | [Tags](https://github.com/willhallonline/docker-ansible-test/tags) |
| [docker-ansible-github-action-test](https://github.com/willhallonline/docker-ansible-github-action-test) | — (no tagged releases) | Workflows exercising the GitHub Action | [Commits](https://github.com/willhallonline/docker-ansible-github-action-test/commits) |

!!! tip "Checking for newer releases"
    This table is a snapshot. Each project's **Releases** or **Tags** page on
    GitHub is the source of truth — the links above point at the live data.

## Per-project changelogs

### docker-ansible (core images)

![GitHub release](https://img.shields.io/github/v/release/willhallonline/docker-ansible)

The canonical changelog is maintained in the upstream repository:
[CHANGELOG.md](https://github.com/willhallonline/docker-ansible/blob/main/CHANGELOG.md)

Recent highlights (v6.4.3–v6.4.8):

- added Alpine 3.23 and 3.24 support and moved Alpine 3.19 to the archive;
- deprecated Alpine 3.20;
- added `HEALTHCHECK` instructions to active images;
- switched dependency installation from `pip`/`pipx` to `uv`;
- added the non-root `ansible` user and updated the SSH home to
  `/home/ansible/.ssh`;
- updated Ansible core to 2.16.19, 2.18.19, 2.19.13, 2.20.9, and 2.21.4;
- fixed scheduled ARM64 builds by updating QEMU binfmt.

The current Ansible core lines shipped in the images are 2.16 through 2.21 —
see [supported tags](../images/tags.md) for the full matrix.

### docker-ansible-github-action

![GitHub release](https://img.shields.io/github/v/release/willhallonline/docker-ansible-github-action)

**v1.1.0** adds support for the non-root `ansible` user used by current images,
mounts SSH material under `/home/ansible/.ssh`, and updates the smoke-test
example to Alpine 3.24. See the
[GitHub Action](../projects/github-action.md) page and the
[action repository](https://github.com/willhallonline/docker-ansible-github-action/releases)
for current inputs and examples.

### Testing projects

- **docker-ansible-test** (latest tag **v2.7.3**) — playbooks and scenarios
  used to exercise the images themselves.
- **docker-ansible-github-action-test** — workflow runs validating the GitHub
  Action end to end; it tracks the action rather than cutting its own releases.

See [Testing](../projects/testing.md) for how these fit together.

## What changes over time

The Docker Ansible ecosystem changes when Ansible releases, base images, CI
platforms, or dependency policies change.

Typical changes include:

- adding new Ansible versions;
- refreshing Python dependencies;
- adding new base operating-system versions;
- retiring old base images into `archive/`;
- adjusting CI workflows;
- updating `ansible-lint` and supporting packages;
- documenting compatibility notes.

## Current notable themes

Recent project direction includes these broad changes:

| Area | Summary |
| --- | --- |
| Ansible versions | Current images ship ansible-core 2.16.19 through 2.21.4. |
| Alpine bases | Alpine 3.21 through 3.24 are supported; 3.19 is archived and 3.20 is deprecated. |
| Ubuntu bases | Ubuntu 26.04 is available alongside Ubuntu 22.04 and 24.04. |
| Debian bases | Debian Trixie variants are available alongside Bookworm variants. |
| Rocky Linux | Rocky Linux 10 is available as a RHEL-family base. |
| Older bases | Older bases and Ansible lines are retired into archive areas over time. |

No dated release entries are reproduced here because the upstream changelog
should remain the canonical history.

## Versioning model

Image tags are generally intended to communicate the Ansible version and the base
operating-system variant. For example, production users should prefer an explicit
Ansible-version and base-OS tag over a floating tag.

```text
willhallonline/ansible:2.21.4-alpine-3.24
willhallonline/ansible:2.21.4-debian-trixie
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

## Archive policy

The core repository includes an `archive/` directory for older image definitions.
Archived content is useful for legacy users, but should not be interpreted as a
promise of active maintenance.

!!! warning "Legacy images carry risk"
    Old Ansible versions and old Linux base images may no longer receive security
    fixes. Use them only when required, and isolate the workflows that depend on
    them.

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
docker run --rm willhallonline/ansible:2.21.4-debian-trixie ansible --version
```

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.4-debian-trixie   ansible-lint
```

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.4-debian-trixie   ansible-playbook --syntax-check -i inventory site.yml
```

## Related documentation

- [Docker Ansible](../projects/docker-ansible.md)
- [Testing](../projects/testing.md)
- [Security](security.md)
- [FAQ](faq.md)
