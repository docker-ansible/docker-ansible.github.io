# Docker Ansible

[`willhallonline/docker-ansible`](https://github.com/willhallonline/docker-ansible)
is the core repository for the `willhallonline/ansible` Docker image family.

It provides Ansible inside Docker containers for Alpine, Ubuntu, Rocky Linux,
and Debian. The images include `ansible-core`, `ansible`, and `ansible-lint` so
that local development and CI jobs can use the same packaged toolchain.

!!! note "Short description"
    Ansible inside Docker containers: Alpine, Ubuntu, Rocky Linux & Debian with
    Ansible 2.21, 2.20, 2.19, 2.18 & more; older versions are still available
    where maintained or archived.

## Links

| Resource | Link |
| --- | --- |
| Source repository | <https://github.com/willhallonline/docker-ansible> |
| Docker Hub | <https://hub.docker.com/r/willhallonline/ansible> |
| Maintainer | [Will Hall](https://www.willhallonline.co.uk) |
| Changelog | <https://github.com/willhallonline/docker-ansible/blob/main/CHANGELOG.md> |
| Contributing | <https://github.com/willhallonline/docker-ansible/blob/main/CONTRIBUTING.md> |
| Security policy | <https://github.com/willhallonline/docker-ansible/blob/main/SECURITY.md> |
| License | <https://github.com/willhallonline/docker-ansible/blob/main/LICENSE> |

## What is included

Each current image is intended to provide a ready-to-run Ansible environment:

- `ansible-core`
- `ansible`
- `ansible-lint`
- Python and operating-system packages required by the chosen image variant
- A predictable Docker entry point for running Ansible commands

```bash
docker run --rm willhallonline/ansible:latest ansible --version
docker run --rm willhallonline/ansible:latest ansible-lint --version
```

## Supported Ansible versions

Current versions published by the project include:

| Ansible version | Notes |
| --- | --- |
| `2.21.0` | Current newer Ansible release line. |
| `2.20.0` | Current stable Ansible release line. |
| `2.19.2` | Supported recent release line. |
| `2.18.9` | Supported release line. |
| `2.17.14` | Supported older release line. |
| `2.16.14` | Supported older release line. |

!!! warning "Older does not mean maintained"
    Older Ansible versions, including the 2.9-2.15 range, may be available in
    archived image definitions or historical tags. Treat them as legacy and pin
    them explicitly if you must use them.

## Repository layout

The repository is organised around image definitions and support files.

| Path | Purpose |
| --- | --- |
| `ansible-core/<os>/Dockerfile` | Dockerfiles for current image variants. |
| `ansible-core/alpine-3.19` - `ansible-core/alpine-3.22` | Alpine-based image variants. |
| `ansible-core/debian-bookworm` | Debian Bookworm image variant. |
| `ansible-core/debian-bookworm-slim` | Slim Debian Bookworm variant. |
| `ansible-core/debian-trixie` | Debian Trixie image variant. |
| `ansible-core/debian-trixie-slim` | Slim Debian Trixie variant. |
| `ansible-core/rockylinux-10` | Rocky Linux 10 image variant. |
| `ansible-core/ubuntu-22.04` | Ubuntu 22.04 image variant. |
| `ansible-core/ubuntu-24.04` | Ubuntu 24.04 image variant. |
| `ansible-core/ubuntu-26.04` | Ubuntu 26.04 image variant. |
| `archive/` | Older image definitions and legacy versions. |
| `docs/older-releases.md` | Notes for older releases. |
| `docs/using-mitogen.md` | Notes for using Mitogen. |
| `testing-utils/` | Helpers used by testing workflows. |
| `.github/` | GitHub workflows and automation. |
| `.gitlab-ci.yml` | GitLab CI configuration. |
| `renovate.json` | Renovate dependency update configuration. |
| `CHANGELOG.md` | Upstream change history. |
| `CONTRIBUTING.md` | Contribution guidance. |
| `SECURITY.md` | Security reporting guidance. |
| `LICENSE` | MIT license. |

## Base operating systems

The project publishes image variants for multiple Linux distributions so you can
choose the runtime that best matches your playbooks and dependencies.

| Family | Example variants | When to consider it |
| --- | --- | --- |
| Alpine | `alpine-3.19` through `alpine-3.22` | Small images and fast pulls. |
| Debian | `debian-bookworm`, `debian-trixie` | Broad Python package compatibility. |
| Debian slim | `debian-bookworm-slim`, `debian-trixie-slim` | Debian compatibility with a smaller footprint. |
| Ubuntu | `ubuntu-22.04`, `ubuntu-24.04`, `ubuntu-26.04` | Familiar apt-based CI and enterprise workflows. |
| Rocky Linux | `rockylinux-10` | RHEL-family compatibility testing. |

!!! tip "Alpine versus glibc distributions"
    Alpine uses musl libc. Some Python packages with native extensions may need
    build dependencies or may be easier to install on Debian or Ubuntu variants.

## Basic usage

Mount your project into the container and run commands from the mounted path.
Many examples use `/ansible` as the working directory.

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook site.yml
```

For localhost-only playbooks, use a local connection:

```yaml
- hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - debug:
        msg: "Hello from Docker Ansible"
```

Then run:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook -i localhost, playbook.yml
```

## Automation and rebuilds

The upstream repository includes Renovate configuration for automated dependency
updates. Images are rebuilt regularly as the project tracks Ansible, Python, and
base-image updates.

!!! note "Repeatability"
    Regular rebuilds are useful for security and dependency freshness. Production
    jobs should still pin tags, and high-assurance environments should pin image
    digests.

## Related documentation

- [GitHub Action](github-action.md)
- [Testing](testing.md)
- [FAQ](../reference/faq.md)
- [Troubleshooting](../reference/troubleshooting.md)
- [Security](../reference/security.md)
