# Changelog

The canonical changelog for the Docker Ansible image project is maintained in
the upstream repository:

<https://github.com/willhallonline/docker-ansible/blob/main/CHANGELOG.md>

!!! tip "Use the upstream changelog for release decisions"
    This page summarises how to read the ecosystem changes. The upstream
    `CHANGELOG.md` is the source of truth for project-specific release notes.

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
| Ansible versions | Newer Ansible release lines such as 2.20 and 2.21 are available. |
| Ubuntu bases | Ubuntu 26.04 has been added alongside existing Ubuntu variants. |
| Debian bases | Debian Trixie variants have been added alongside Bookworm variants. |
| Rocky Linux | Rocky Linux 10 is available as a RHEL-family base. |
| Older bases | Older bases and Ansible lines are retired into archive areas over time. |

No dated release entries are reproduced here because the upstream changelog
should remain the canonical history.

## Versioning model

Image tags are generally intended to communicate the Ansible version and the base
operating-system variant. For example, production users should prefer an explicit
Ansible-version and base-OS tag over a floating tag.

```text
willhallonline/ansible:2.21.0-alpine-3.22
willhallonline/ansible:2.21.0-debian-trixie
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
docker run --rm willhallonline/ansible:2.21.0-debian-trixie ansible --version
```

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.0-debian-trixie   ansible-lint
```

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.0-debian-trixie   ansible-playbook --syntax-check -i inventory site.yml
```

## Related documentation

- [Docker Ansible](../projects/docker-ansible.md)
- [Testing](../projects/testing.md)
- [Security](security.md)
- [FAQ](faq.md)
