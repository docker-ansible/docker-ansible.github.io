# Docker Ansible

![Docker Pulls](https://img.shields.io/docker/pulls/willhallonline/ansible)

Run Ansible from a container, consistently, on laptops and in CI/CD.

The **willhallonline Docker Ansible** images package the tools commonly needed to run
Ansible without installing Python, Ansible, or Ansible linting tools directly on the
host. Pull an image, mount your project, and run the same Ansible toolchain anywhere
Docker is available.

!!! note "Project links"
    - Docker Hub: [willhallonline/ansible](https://hub.docker.com/r/willhallonline/ansible)
    - GitHub: [willhallonline/docker-ansible](https://github.com/willhallonline/docker-ansible)
    - Maintainer: [Will Hall](https://www.willhallonline.co.uk)

!!! important "Current release tags"
    Keep these release tags in mind when choosing a runtime or CI integration:

    | Project | Tag | Current image/default |
    | --- | --- | --- |
    | Docker Ansible | [`v6.4.8`](https://github.com/willhallonline/docker-ansible/tree/v6.4.8) (`f054694`, 2026-09-11) | `2.21-alpine-3.24` (`latest`/`alpine`) |
    | Docker Ansible GitHub Action | [`v1.1.0`](https://github.com/willhallonline/docker-ansible-github-action/tree/v1.1.0) | Uses the non-root `ansible` image user |
    | Docker Ansible Test | [`v2.7.4`](https://github.com/willhallonline/docker-ansible-test/tree/v2.7.4) | Tracks the current image matrix |
    | Docker Ansible GitHub Action Test | [`integration-test v1.1.0`](https://github.com/willhallonline/docker-ansible-github-action-test/releases/tag/v1.1.0) | Tests the GitHub Action |

    See the [ecosystem changelog](reference/changelog.md) for release notes and
    links.

## Quick example

Start an interactive shell in the latest image:

```bash
docker run --rm -it willhallonline/ansible:latest /bin/sh
```

Run a playbook from the current directory:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/home/ansible/.ssh/id_rsa \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

!!! tip "Make it repeatable"
    For day-to-day use, add shell aliases so you can run the container from any
    Ansible project without retyping the full `docker run` command.
    See [shell aliases](getting-started/shell-aliases.md).

## What these images include

Each image bundles:

- `ansible-core`
- `ansible`, the community package
- `ansible-lint`

The goal is not to replace Ansible. The goal is to make Ansible **portable**:

- no host Python environment to manage
- no global Ansible installation to upgrade or repair
- fewer differences between a developer workstation and a CI runner
- predictable image tags for repeatable automation

For more detail about the installed tooling, see [what's inside](images/whats-inside.md).

## Why use Docker for Ansible?

Ansible is usually run from a control node. In many teams, that control node might be:

a developer laptop one day, a GitHub Actions runner the next, and a self-hosted CI
worker later in the week. Containerizing the control environment helps keep those
runs aligned.

### Consistent local development

Developers can run the same Ansible version without installing it directly on macOS,
Linux, or a CI image. A project can document one image tag and one command.

### Cleaner CI/CD pipelines

CI jobs can pull a prebuilt Ansible image instead of installing Python packages during
every pipeline run. This keeps pipeline definitions smaller and reduces setup drift.

### Easier version pinning

Tags follow a predictable pattern:

```text
<ansible-version>-<os>
```

Examples include:

```text
2.21-alpine-3.24
2.19-debian-bookworm
2.20-ubuntu-24.04
2.18-rockylinux-10
2.19-debian-bookworm-slim
2.21-debian-trixie
2.21-debian-trixie-slim
```

Pin exact tags in automation when reproducibility matters.

## Get started

<div class="grid cards" markdown>

-   :material-rocket-launch-outline: **Quick start**

    ---

    Run your first containerized Ansible command and execute a playbook from your
    working directory.

    [Start here](getting-started/quick-start.md)

-   :material-docker: **Choose an image**

    ---

    Pick an Ansible version and base operating system for local use, CI, or
    production-like testing.

    [Choose an image](getting-started/choosing-an-image.md)

-   :material-console-line: **Shell aliases**

    ---

    Add convenient aliases for interactive shells and one-off Ansible commands.

    [Set up aliases](getting-started/shell-aliases.md)

-   :material-package-variant-closed: **Image reference**

    ---

    Browse image families, tags, architectures, and release notes.

    [View images](images/index.md)

-   :material-history: **Changelog**

    ---

    See what changed across the ecosystem projects and find the latest release
    of each.

    [View changelog](reference/changelog.md)

</div>

## Supported Ansible core versions

Current Ansible core versions available in containers are:

| Ansible core | Status |
| --- | --- |
| 2.21.4 | Current container version |
| 2.20.9 | Current container version |
| 2.19.13 | Current container version |
| 2.18.19 | Current container version |
| 2.17.14 | Current container version |
| 2.16.19 | Current container version |

Ansible core streams **2.9 through 2.15** are outside the active image matrix and
are unmaintained. Use a current stream unless you have a specific legacy
compatibility requirement. See [older releases](images/older-releases.md).

!!! warning "Avoid floating tags in CI"
    Convenience tags are useful for exploration, but CI should usually pin an exact
    tag such as `2.21-alpine-3.24` or `2.21-debian-trixie-slim`.

## Convenience tags

The repository also publishes convenience tags for common defaults:

| Tag | Points to |
| --- | --- |
| `latest` | Ansible 2.21 on Alpine 3.24 |
| `alpine` | Ansible 2.21 on Alpine 3.24 |
| `ubuntu` | Ansible 2.21 on Ubuntu 24.04 |

These are handy for local testing and examples. For long-lived automation, prefer a
fully pinned tag.

## Base operating systems

Images are available across several base OS families:

- Alpine 3.21, 3.22, 3.23, and 3.24
- Debian Bookworm and Bookworm-slim
- Debian Trixie and Trixie-slim
- Rocky Linux 10
- Ubuntu 22.04, 24.04, and 26.04

Current tags generally publish **AMD64** and **ARM64** variants, but platform
availability is tag-specific. For example, `2.21-ubuntu-24.04` is AMD64-only.
No ARMv7/32-bit ARM images are published. Check the selected tag's manifest
before relying on ARM64 in CI; see [architectures](images/architectures.md).

Explore the image families:

- [Alpine images](images/alpine.md)
- [Debian images](images/debian.md)
- [Ubuntu images](images/ubuntu.md)
- [Rocky Linux images](images/rockylinux.md)
- [Architectures](images/architectures.md)

## Common next steps

After the quick start, most users move on to one of these topics:

- [Running playbooks](usage/running-playbooks.md)
- [SSH keys and authentication](usage/ssh-keys-and-auth.md)
- [Ansible Vault](usage/ansible-vault.md)
- [ansible-lint](usage/ansible-lint.md)
- [Galaxy roles and collections](usage/galaxy-roles-collections.md)
- [Docker Compose usage](usage/docker-compose.md)
- [Extending images](usage/extending-images.md)

For CI/CD examples, start with the [CI overview](ci/index.md), then choose your
platform:

- [GitHub Actions](ci/github-actions.md)
- [GitLab CI](ci/gitlab-ci.md)
- [Bitbucket Pipelines](ci/bitbucket-pipelines.md)
- [Azure Pipelines](ci/azure-pipelines.md)
- [Jenkins](ci/jenkins.md)
- [CircleCI](ci/circleci.md)
- [Drone](ci/drone.md)
- [Woodpecker](ci/woodpecker.md)

## Documentation map

Use this site as a practical handbook:

1. Read [getting started](getting-started/index.md) to understand the workflow.
2. Choose a tag with [choosing an image](getting-started/choosing-an-image.md).
3. Learn the image families in [images](images/index.md).
4. Apply the images locally with [usage guides](usage/index.md).
5. Bring the same commands to CI with [CI/CD examples](ci/index.md).
6. Check [troubleshooting](reference/troubleshooting.md) and [FAQ](reference/faq.md)
   when something behaves differently from your host environment.
7. Follow the [changelog](reference/changelog.md) to track releases across the
   ecosystem projects.
