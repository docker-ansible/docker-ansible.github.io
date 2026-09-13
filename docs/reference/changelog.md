# Changelog

This page tracks changes **across the Docker Ansible ecosystem** — the core
container images, the GitHub Action, and the testing projects — and points you
at the latest release of each.

## Latest tags and releases at a glance

| Project | Latest tag/release | What it is | Release notes |
| --- | --- | --- | --- |
| [Docker Ansible](https://github.com/willhallonline/docker-ansible) | [`v6.4.8`](https://github.com/willhallonline/docker-ansible/tree/v6.4.8) | The core container images (`willhallonline/ansible`) | [Source tag](https://github.com/willhallonline/docker-ansible/tree/v6.4.8) |
| [Docker Ansible GitHub Action](https://github.com/willhallonline/docker-ansible-github-action) | **v1.1.0** | GitHub Action running Ansible via the images | [Releases](https://github.com/willhallonline/docker-ansible-github-action/releases) |
| [Docker Ansible Test](https://github.com/willhallonline/docker-ansible-test) | **v2.7.4** | Test playbooks exercising the images | [Tags](https://github.com/willhallonline/docker-ansible-test/tags) |
| [Docker Ansible GitHub Action Test](https://github.com/willhallonline/docker-ansible-github-action-test) | **integration-test v1.1.0** | Workflows exercising the GitHub Action | [Release](https://github.com/willhallonline/docker-ansible-github-action-test/releases/tag/v1.1.0) |

!!! tip "Checking for newer releases"
    This table is a snapshot. Each project's **Releases** or **Tags** page on
    GitHub is the source of truth — the links above point at the live data.

## Per-project changelogs

### Docker Ansible

The canonical changelog is maintained in the upstream repository:
[CHANGELOG.md](https://github.com/willhallonline/docker-ansible/blob/main/CHANGELOG.md)

Recent highlights (v6.4.3–v6.4.8):

- added Alpine 3.23 and 3.24 support;
- kept the active matrix on Alpine 3.21 through 3.24;
- added `HEALTHCHECK` instructions to active images;
- switched dependency installation from `pip`/`pipx` to `uv`;
- added the non-root `ansible` user and updated the SSH home to
  `/home/ansible/.ssh`;
- updated Ansible core to 2.16.19, 2.18.19, 2.19.13, 2.20.9, and 2.21.4;
- builds generally target Linux AMD64 and ARM64, with tag-specific exceptions.

The current Ansible core lines shipped in the images are 2.16 through 2.21 —
see [supported tags](../images/tags.md) for the full matrix.

### Docker Ansible GitHub Action

![GitHub release](https://img.shields.io/github/v/release/willhallonline/docker-ansible-github-action)

**v1.1.0** adds support for the non-root `ansible` user used by current images,
mounts SSH material under `/home/ansible/.ssh`, and updates the smoke-test
example to Alpine 3.24. See the
[Docker Ansible GitHub Action](../projects/github-action.md) page and the
[action repository](https://github.com/willhallonline/docker-ansible-github-action/releases)
for current inputs and examples.

### Docker Ansible Test and Docker Ansible GitHub Action Test

- **Docker Ansible Test** (latest tag **v2.7.4**) — playbooks and scenarios
  used to exercise the images themselves.
- **Docker Ansible GitHub Action Test** (integration-test **v1.1.0**) —
  localhost/non-root/exit-code smoke coverage for the GitHub Action.

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
| Ansible versions | Current images ship ansible-core 2.16.19 through 2.21.4. |
| Alpine bases | Alpine 3.21 through 3.24 are supported in the active matrix. |
| Ubuntu bases | Ubuntu 26.04 is available alongside Ubuntu 22.04 and 24.04. |
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

## Legacy policy

Ansible core streams 2.9 through 2.15 are outside the active matrix and
unmaintained. Historical definitions or tags may not be published; verify any
legacy reference in the upstream repository and registry.

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
- [Docker Ansible Test](../projects/testing.md)
- [Security](security.md)
- [FAQ](faq.md)
