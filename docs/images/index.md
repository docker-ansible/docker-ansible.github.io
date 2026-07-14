# Docker Ansible images

The `willhallonline/ansible` images provide ready-to-run Docker images for
Ansible automation. They are built from common Linux base images and published
with tags that make the Ansible minor version and operating system explicit.

!!! note "Image repository"
    The public image name is `willhallonline/ansible` on Docker Hub. The source
    repository is [willhallonline/docker-ansible](https://github.com/willhallonline/docker-ansible).

## Registries and source

| Resource | Location |
| --- | --- |
| Docker Hub image | [`willhallonline/ansible`](https://hub.docker.com/r/willhallonline/ansible) |
| GitHub source | [`willhallonline/docker-ansible`](https://github.com/willhallonline/docker-ansible) |
| Dockerfiles | `ansible-core/<os-dir>/Dockerfile` |
| Older releases | `archive/` in the source repository |

Dockerfiles are grouped by base operating system and version. Examples include:

- `ansible-core/alpine-3.22/Dockerfile`
- `ansible-core/debian-bookworm/Dockerfile`
- `ansible-core/debian-bookworm-slim/Dockerfile`
- `ansible-core/debian-trixie/Dockerfile`
- `ansible-core/debian-trixie-slim/Dockerfile`
- `ansible-core/rockylinux-10/Dockerfile`
- `ansible-core/ubuntu-22.04/Dockerfile`
- `ansible-core/ubuntu-24.04/Dockerfile`
- `ansible-core/ubuntu-26.04/Dockerfile`

## Naming convention

Supported moving tags use this pattern:

```text
<ansible-minor>-<os>
```

For example:

```text
2.21-alpine-3.22
2.20-debian-trixie
2.19-rockylinux-10
2.18-ubuntu-24.04
```

The tag tells you two things:

1. the Ansible minor stream, such as `2.21`; and
2. the base operating system, such as `alpine-3.22` or `ubuntu-24.04`.

!!! tip "Prefer explicit tags"
    Use explicit tags such as `2.21-alpine-3.22` in automation. Convenience
    tags are useful for quick tests, but explicit tags make upgrades deliberate.

## Convenience tags

| Tag | Points to |
| --- | --- |
| `latest` | Ansible 2.21 on Alpine 3.22 |
| `alpine` | Ansible 2.21 on Alpine 3.22 |
| `ubuntu` | Ansible 2.21 on Ubuntu 24.04 |

Pulling a convenience tag is simple:

```bash
docker pull willhallonline/ansible:latest
```

For repeatable builds, pin the operating system and Ansible stream instead:

```bash
docker pull willhallonline/ansible:2.21-alpine-3.22
```

## Immutable and pinned tags

In addition to moving minor tags, immutable tags are also published with the
full Ansible patch version and full base operating system version. The pattern
is:

```text
AnsibleVersion-BaseOSversion
```

Browse the full list on
[Docker Hub tags](https://hub.docker.com/r/willhallonline/ansible/tags) when you
need a specific patch release.

!!! note "Moving versus pinned tags"
    Tags such as `2.21-alpine-3.22` track the current image for that Ansible
    minor stream and base. Fully pinned tags are better when exact image
    reproduction matters.

## Image philosophy

The images are intended to be practical Ansible control-node containers. Each
image includes:

- `ansible-core` from PyPI;
- the `ansible` community package from PyPI;
- `ansible-lint` from PyPI; and
- Python plus the tooling needed to run Ansible against remote hosts.

That supporting tooling typically includes SSH client capability, password-based
SSH support where available, Git, certificate handling, and common system
packages expected by Ansible workflows.

## Current Ansible core streams

The supported image matrix currently covers these Ansible core versions:

| Minor | Current core version |
| --- | --- |
| 2.16 | 2.16.14 |
| 2.17 | 2.17.14 |
| 2.18 | 2.18.9 |
| 2.19 | 2.19.2 |
| 2.20 | 2.20.0 |
| 2.21 | 2.21.0 |

See the complete [supported tag matrix](tags.md) for the operating systems that
are available for each stream.

## Base image families

| Family | Page | Package manager | Notes |
| --- | --- | --- | --- |
| Alpine | [Alpine images](alpine.md) | `apk` | Small, musl libc based |
| Debian | [Debian images](debian.md) | `apt` | General-purpose glibc base, normal and slim variants |
| Ubuntu | [Ubuntu images](ubuntu.md) | `apt` | Familiar CI and workstation base |
| Rocky Linux | [Rocky Linux images](rockylinux.md) | `dnf` | Enterprise Linux compatible base |

## Architectures

Current images are published for AMD64 and ARM64. See
[architectures](architectures.md) for platform-specific pull and run examples,
including Apple Silicon, AWS Graviton, and 64-bit Raspberry Pi OS.

## Regular rebuilds

Images are rebuilt regularly, including dependency updates managed through
Renovate. This keeps the supported streams current without changing the public
tagging scheme.

!!! warning "Unsupported streams"
    Older Ansible streams such as 2.9 through 2.15 are no longer maintained in
    the current matrix. See [older releases](older-releases.md) before using
    archived tags.

## Next steps

- Start with [choosing an image](../getting-started/choosing-an-image.md).
- Review the [tag matrix](tags.md).
- Learn how to [run playbooks](../usage/running-playbooks.md).
- Extend an image for project-specific tools in [extending images](../usage/extending-images.md).
- Use the images in [CI workflows](../ci/index.md).
