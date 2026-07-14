# What's inside the images

The `willhallonline/ansible` images are built to act as Ansible control-node
containers. They include Ansible, linting support, Python, and the system tooling
needed to run playbooks against remote hosts.

!!! note "Purpose"
    These are not target-host images. They are control-node images: run them
    where you want to execute `ansible`, `ansible-playbook`, and `ansible-lint`.

## Core Python packages

Each supported image includes these Python packages from PyPI:

| Package | Purpose |
| --- | --- |
| `ansible-core` | The core Ansible runtime and command-line tools |
| `ansible` | The community package with bundled collections |
| `ansible-lint` | Linting and policy checks for playbooks, roles, and collections |

The current supported Ansible core streams are:

| Minor | Current core version |
| --- | --- |
| 2.21 | 2.21.0 |
| 2.20 | 2.20.0 |
| 2.19 | 2.19.2 |
| 2.18 | 2.18.9 |
| 2.17 | 2.17.14 |
| 2.16 | 2.16.14 |

See [supported tags](tags.md) for which operating systems are available for each
stream.

## Command-line tools

The images include Python and common dependencies needed to run Ansible against
remote hosts. This generally means the control-node tooling required for:

- SSH-based connections;
- password-based SSH workflows where supported;
- Git-based playbook, role, and collection workflows;
- TLS certificate handling;
- installing or importing Python dependencies used by Ansible; and
- running `ansible-lint` in CI.

Typical tools include OpenSSH client functionality, `sshpass`, Git, Python, and
base operating-system packages required by the selected image family.

!!! tip "Keep project tools explicit"
    If your project needs cloud CLIs, custom Python packages, `jq`, `helm`, or
    other tools, build a small derived image so those dependencies are visible in
    version control.

## Commands available in the container

Common commands include:

```bash
ansible --version
ansible-playbook --version
ansible-galaxy --version
ansible-lint --version
python --version
```

Run them through Docker to inspect a tag:

```bash
docker run --rm willhallonline/ansible:2.21-alpine-3.22 ansible --version
docker run --rm willhallonline/ansible:2.21-alpine-3.22 ansible-lint --version
```

## Base operating system differences

The included Ansible tools are consistent in purpose, but the operating system
family affects package management, libc, package names, and image size.

| Family | Package manager | libc | Notes |
| --- | --- | --- | --- |
| Alpine | `apk` | musl | Smallest family; test native dependencies |
| Debian | `apt` | glibc | Standard and slim variants |
| Ubuntu | `apt` | glibc | Familiar CI and cloud base |
| Rocky Linux | `dnf` | glibc | Enterprise Linux compatible base |

## What is not included

The images are intentionally general. They do not try to include every tool that
any playbook might call locally.

Examples of tools you may need to add yourself include:

- cloud provider CLIs;
- Kubernetes or Helm CLIs;
- project-specific Python libraries;
- secret-management CLIs;
- test frameworks such as Molecule; and
- organization-specific certificates or package repositories.

Add these in a derived image, or install them during a CI job when that is more
appropriate.

## Extending safely

A derived image keeps project dependencies repeatable:

=== "Alpine"

    ```dockerfile
    FROM willhallonline/ansible:2.21-alpine-3.22

    RUN apk add --no-cache jq
    ```

=== "Debian or Ubuntu"

    ```dockerfile
    FROM willhallonline/ansible:2.21-ubuntu-24.04

    RUN apt-get update         && apt-get install -y --no-install-recommends jq         && rm -rf /var/lib/apt/lists/*
    ```

=== "Rocky Linux"

    ```dockerfile
    FROM willhallonline/ansible:2.21-rockylinux-10

    RUN dnf install -y jq         && dnf clean all
    ```

See [extending images](../usage/extending-images.md) for complete guidance.

## Rebuilds and dependency updates

Supported images are rebuilt regularly. Dependency updates are managed through
Renovate, which helps keep base images and packaged dependencies current.

!!! warning "Rebuilds can update dependencies"
    Moving tags can receive dependency updates over time. Use fully pinned tags
    from [Docker Hub](https://hub.docker.com/r/willhallonline/ansible/tags) when
    exact image reproduction is required.

## Security considerations

Use the same container hygiene you apply to any automation image:

- pin tags when reproducibility matters;
- keep secrets outside the image;
- mount SSH keys or tokens only at runtime;
- prefer read-only mounts where practical;
- rebuild derived images regularly; and
- review [security guidance](../reference/security.md) for project practices.

## Related pages

- [Supported tags](tags.md)
- [Architectures](architectures.md)
- [Running playbooks](../usage/running-playbooks.md)
- [Extending images](../usage/extending-images.md)
