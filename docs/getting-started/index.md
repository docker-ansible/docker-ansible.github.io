# Getting started

This section introduces the Docker Ansible workflow: choose an image, mount your
project, run Ansible commands, and optionally add shell aliases for daily use.

The images are published as `willhallonline/ansible` and bundle `ansible-core`, the
`ansible` community package, and `ansible-lint`. They are designed for local machines
and CI/CD systems where you want a consistent Ansible control environment without
installing Python or Ansible directly on the host.

!!! note "What you need"
    You need Docker and an Ansible project directory. The examples assume commands
    are run from the root of your Ansible repository or playbook directory.

## The basic workflow

A typical run looks like this:

1. Pick an image tag.
2. Mount your current directory into the container.
3. Mount any SSH key needed to reach managed hosts.
4. Run a shell, `ansible`, `ansible-playbook`, or `ansible-lint` inside the container.

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/id_rsa \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

The container gives you the Ansible tools. Your repository, inventory, playbooks,
roles, and configuration still live on your host filesystem.

## Start here

<div class="grid cards" markdown>

-   :material-timer-play-outline: **Quick start**

    ---

    Pull and run the image, mount your project, and execute a playbook directly.

    [Read the quick start](quick-start.md)

-   :material-image-search-outline: **Choosing an image**

    ---

    Understand image tags, base OS choices, convenience tags, and version pinning.

    [Choose an image](choosing-an-image.md)

-   :material-console: **Shell aliases**

    ---

    Add reusable commands for interactive work and one-off Ansible invocations.

    [Configure aliases](shell-aliases.md)

</div>

## Which command should I run?

Use the command that matches what you want to do.

=== "Open a shell"

    ```bash
    docker run --rm -it willhallonline/ansible:latest /bin/sh
    ```

    This is useful when you want to inspect the image or try commands manually.

=== "Run from a project"

    ```bash
    docker run --rm -it \
      -v $(pwd):/ansible \
      -v ~/.ssh/id_rsa:/root/id_rsa \
      willhallonline/ansible:latest \
      /bin/sh
    ```

    This mounts the current directory at `/ansible` and makes an SSH private key
    available inside the container.

=== "Run a playbook"

    ```bash
    docker run --rm -it \
      -v $(pwd):/ansible \
      -v ~/.ssh/id_rsa:/root/id_rsa \
      willhallonline/ansible:latest \
      ansible-playbook playbook.yml
    ```

    This runs `ansible-playbook` directly instead of starting an interactive shell.

## Image naming in one minute

Tags follow this pattern:

```text
<ansible-version>-<os>
```

Examples:

```text
2.21-alpine-3.22
2.19-debian-bookworm
2.20-ubuntu-24.04
2.18-rockylinux-10
2.19-debian-bookworm-slim
2.21-debian-trixie
2.21-debian-trixie-slim
```

Convenience tags are also available:

| Tag | Meaning |
| --- | --- |
| `latest` | Ansible 2.21 on Alpine 3.22 |
| `alpine` | Ansible 2.21 on Alpine 3.22 |
| `ubuntu` | Ansible 2.21 on Ubuntu 24.04 |

!!! warning "Pin tags for automation"
    Convenience tags can move when the default image changes. Use fully qualified
    tags in CI/CD and other repeatable workflows.

## Current Ansible versions

The current Ansible core versions available in containers are:

- 2.21.0
- 2.20.0
- 2.19.2
- 2.18.9
- 2.17.14
- 2.16.14

Older versions from 2.9 through 2.15 exist but are unmaintained. If you rely on an
older version, review [older releases](../images/older-releases.md) and plan an
upgrade path.

## Choosing a base OS

The base image affects package compatibility, size, and how closely the container
matches your target systems.

| Base OS | Good for |
| --- | --- |
| Alpine | Small images and fast pulls |
| Debian slim | A balanced default with glibc in a smaller image |
| Debian | Debian-like environments and broader base utilities |
| Ubuntu | Matching Ubuntu-based automation or CI expectations |
| Rocky Linux | Matching Enterprise Linux-style environments |

For a guided decision, read [choosing an image](choosing-an-image.md).

## Multi-architecture support

Current images are published for **AMD64** and **ARM64**. That means the same tag
can be used on common x86 CI runners, Apple Silicon Docker environments, AWS
Graviton, 64-bit Raspberry Pi OS, and other 64-bit ARM hosts where Docker selects
the appropriate image automatically. 32-bit ARM images are not published for
current tags.

See [architectures](../images/architectures.md) for more detail.

## Recommended path through the docs

If this is your first visit, use this order:

1. [Quick start](quick-start.md)
2. [Choosing an image](choosing-an-image.md)
3. [Shell aliases](shell-aliases.md)
4. [Running playbooks](../usage/running-playbooks.md)
5. [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
6. [ansible-lint](../usage/ansible-lint.md)
7. [CI overview](../ci/index.md)

## Common questions before you begin

### Do I need Ansible installed on the host?

No. The container provides `ansible-core`, the `ansible` community package, and
`ansible-lint`. You only need Docker on the host.

### Where should my playbooks live?

Keep them in your normal project directory. Mount that directory into the container
with `-v $(pwd):/ansible`.

### Should I use `latest`?

`latest` is fine for quick experiments. For CI/CD or team documentation, pin a tag
such as `2.21-alpine-3.22`, `2.21-debian-trixie-slim`, or another exact version that
matches your project needs.

### Where do I go for CI/CD examples?

Start with the [CI overview](../ci/index.md), then choose your platform:
[GitHub Actions](../ci/github-actions.md), [GitLab CI](../ci/gitlab-ci.md),
[Azure Pipelines](../ci/azure-pipelines.md), or another supported CI provider.

