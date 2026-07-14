# Supported tags

This page is the reference matrix for supported `willhallonline/ansible` tags.
Supported moving tags use the pattern:

```text
<ansible-minor>-<os>
```

For example, `2.21-alpine-3.22` means Ansible 2.21 on Alpine Linux 3.22.

!!! tip "Use this table for automation"
    Pick one tag from the matrix and use it consistently in Dockerfiles, CI
    jobs, and scheduled automation. Avoid relying on `latest` unless you are
    intentionally tracking the default image.

## Current Ansible core versions

| Ansible minor | Current ansible-core version |
| --- | --- |
| 2.21 | 2.21.0 |
| 2.20 | 2.20.0 |
| 2.19 | 2.19.2 |
| 2.18 | 2.18.9 |
| 2.17 | 2.17.14 |
| 2.16 | 2.16.14 |

## Convenience tags

| Tag | Current target | Use case |
| --- | --- | --- |
| `latest` | `2.21-alpine-3.22` | Quick tests and default pulls |
| `alpine` | `2.21-alpine-3.22` | Latest supported Alpine image |
| `ubuntu` | `2.21-ubuntu-24.04` | Latest supported Ubuntu image |

!!! warning "Convenience tags move"
    Convenience tags can change target as the project advances. Use matrix tags
    or fully pinned tags when repeatability matters.

## Full supported tag matrix

| Base image | 2.21 | 2.20 | 2.19 | 2.18 | 2.17 | 2.16 |
| --- | --- | --- | --- | --- | --- | --- |
| Alpine 3.19 | — | — | `2.19-alpine-3.19` | `2.18-alpine-3.19` | `2.17-alpine-3.19` | `2.16-alpine-3.19` |
| Alpine 3.20 | `2.21-alpine-3.20` | `2.20-alpine-3.20` | `2.19-alpine-3.20` | `2.18-alpine-3.20` | `2.17-alpine-3.20` | `2.16-alpine-3.20` |
| Alpine 3.21 | `2.21-alpine-3.21` | `2.20-alpine-3.21` | `2.19-alpine-3.21` | `2.18-alpine-3.21` | `2.17-alpine-3.21` | `2.16-alpine-3.21` |
| Alpine 3.22 | `2.21-alpine-3.22` | `2.20-alpine-3.22` | `2.19-alpine-3.22` | `2.18-alpine-3.22` | `2.17-alpine-3.22` | `2.16-alpine-3.22` |
| Debian Bookworm | — | — | `2.19-debian-bookworm` | `2.18-debian-bookworm` | `2.17-debian-bookworm` | `2.16-debian-bookworm` |
| Debian Bookworm Slim | — | — | `2.19-debian-bookworm-slim` | `2.18-debian-bookworm-slim` | `2.17-debian-bookworm-slim` | `2.16-debian-bookworm-slim` |
| Debian Trixie | `2.21-debian-trixie` | `2.20-debian-trixie` | `2.19-debian-trixie` | `2.18-debian-trixie` | `2.17-debian-trixie` | — |
| Debian Trixie Slim | `2.21-debian-trixie-slim` | `2.20-debian-trixie-slim` | `2.19-debian-trixie-slim` | `2.18-debian-trixie-slim` | `2.17-debian-trixie-slim` | — |
| Rocky Linux 10 | `2.21-rockylinux-10` | `2.20-rockylinux-10` | `2.19-rockylinux-10` | `2.18-rockylinux-10` | `2.17-rockylinux-10` | `2.16-rockylinux-10` |
| Ubuntu 22.04 | — | — | — | — | `2.17-ubuntu-22.04` | `2.16-ubuntu-22.04` |
| Ubuntu 24.04 | `2.21-ubuntu-24.04` | `2.20-ubuntu-24.04` | `2.19-ubuntu-24.04` | `2.18-ubuntu-24.04` | `2.17-ubuntu-24.04` | `2.16-ubuntu-24.04` |
| Ubuntu 26.04 | `2.21-ubuntu-26.04` | `2.20-ubuntu-26.04` | — | — | — | — |

## Pull examples

=== "Latest default"

    ```bash
    docker pull willhallonline/ansible:latest
    ```

=== "Explicit Alpine"

    ```bash
    docker pull willhallonline/ansible:2.21-alpine-3.22
    ```

=== "Explicit Ubuntu"

    ```bash
    docker pull willhallonline/ansible:2.21-ubuntu-24.04
    ```

=== "Explicit Debian"

    ```bash
    docker pull willhallonline/ansible:2.21-debian-trixie
    ```

=== "Explicit Rocky Linux"

    ```bash
    docker pull willhallonline/ansible:2.21-rockylinux-10
    ```

## Fully pinned tags

Immutable tags are also published with full patch versions. They follow this
pattern:

```text
AnsibleVersion-BaseOSversion
```

Use fully pinned tags when you need to reproduce an exact image. Browse
[Docker Hub tags](https://hub.docker.com/r/willhallonline/ansible/tags) for the
specific patch-level tag you need.

## Choosing between tags

| Requirement | Recommended tag style |
| --- | --- |
| Quick local test | `latest`, `alpine`, or `ubuntu` |
| CI pipeline with planned upgrades | Matrix tag such as `2.21-ubuntu-24.04` |
| Reproducible release build | Fully pinned patch-level tag |
| Small image footprint | Alpine tag |
| glibc compatibility | Debian, Ubuntu, or Rocky Linux tag |

!!! note "Supported does not mean identical"
    Images in the same Ansible stream include the same Ansible core stream, but
    package availability, shell tools, and C library behavior come from the base
    operating system.

## Related pages

- [Alpine images](alpine.md)
- [Debian images](debian.md)
- [Ubuntu images](ubuntu.md)
- [Rocky Linux images](rockylinux.md)
- [Architectures](architectures.md)
- [Older releases](older-releases.md)
