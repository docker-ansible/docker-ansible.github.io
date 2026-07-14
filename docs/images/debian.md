# Debian images

Debian images provide a familiar glibc-based base for Ansible automation. They
are useful when you want broad package availability, predictable `apt` behavior,
and a general-purpose Linux userspace.

The project publishes both standard Debian images and slim variants for selected
releases.

## Available Debian tags

| Base image | Supported tags |
| --- | --- |
| Debian Trixie | `2.21-debian-trixie`, `2.20-debian-trixie`, `2.19-debian-trixie`, `2.18-debian-trixie`, `2.17-debian-trixie` |
| Debian Trixie Slim | `2.21-debian-trixie-slim`, `2.20-debian-trixie-slim`, `2.19-debian-trixie-slim`, `2.18-debian-trixie-slim`, `2.17-debian-trixie-slim` |
| Debian Bookworm | `2.19-debian-bookworm`, `2.18-debian-bookworm`, `2.17-debian-bookworm`, `2.16-debian-bookworm` |
| Debian Bookworm Slim | `2.19-debian-bookworm-slim`, `2.18-debian-bookworm-slim`, `2.17-debian-bookworm-slim`, `2.16-debian-bookworm-slim` |

See the complete [supported tag matrix](tags.md) for all operating systems.

!!! note "Trixie and Bookworm coverage"
    Debian Trixie carries the newer supported Ansible streams. Debian Bookworm
    remains available for Ansible 2.16 through 2.19.

## Pull a Debian image

=== "Trixie"

    ```bash
    docker pull willhallonline/ansible:2.21-debian-trixie
    ```

=== "Trixie Slim"

    ```bash
    docker pull willhallonline/ansible:2.21-debian-trixie-slim
    ```

=== "Bookworm"

    ```bash
    docker pull willhallonline/ansible:2.19-debian-bookworm
    ```

=== "Bookworm Slim"

    ```bash
    docker pull willhallonline/ansible:2.19-debian-bookworm-slim
    ```

## Run Ansible from a Debian image

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-debian-trixie   ansible-playbook -i inventory site.yml
```

Run ad hoc commands the same way:

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-debian-trixie   ansible all -i inventory -m ping
```

## Characteristics

| Property | Debian images |
| --- | --- |
| Package manager | `apt` |
| C library | glibc |
| Variants | Standard and slim |
| Best fit | General CI, glibc compatibility, broad package installs |
| Watch point | Larger than Alpine, especially non-slim variants |

Debian is a strong default when you expect to install extra system packages in a
custom image. It also matches many examples and upstream installation guides for
third-party CLIs.

## Standard versus slim

The standard Debian tags use the normal Debian base image for that release. The
slim tags use Debian slim bases and are useful when you want a smaller glibc
image but still prefer `apt` and Debian packaging.

| Choose | When |
| --- | --- |
| Standard | You value compatibility and fewer surprises over image size |
| Slim | You want a smaller Debian image and know which packages your project needs |

!!! tip "Start standard, optimize later"
    If you are debugging dependency issues, begin with the standard Debian tag.
    Move to the slim tag once you know your package set.

## What's included

Each Debian image includes:

- `ansible-core` from PyPI;
- the `ansible` community package from PyPI;
- `ansible-lint` from PyPI;
- Python; and
- the tooling needed to run Ansible against remote hosts.

The supporting tooling is intended for control-node tasks such as SSH-based
connections, Git checkouts, and common Ansible runtime needs. See
[what's inside](whats-inside.md) for more detail.

## When to choose Debian

Choose Debian when:

- you need a glibc-based image;
- your project installs packages with `apt`;
- third-party documentation assumes Debian or Ubuntu;
- you want normal and slim options for the same release; or
- you prefer a conservative general-purpose base.

Choose another family when:

- smallest possible image size is the priority, where [Alpine](alpine.md) may be
  better;
- your organization standardizes on Ubuntu runner images;
- you need Enterprise Linux compatibility, where [Rocky Linux](rockylinux.md)
  may be better; or
- you require an Ansible stream not available for your chosen Debian release.

## Extending Debian images

Use `apt-get` in non-interactive Dockerfile steps:

```dockerfile
FROM willhallonline/ansible:2.21-debian-trixie

RUN apt-get update     && apt-get install -y --no-install-recommends jq     && rm -rf /var/lib/apt/lists/*
```

Use slim tags when the extra package set is known:

```dockerfile
FROM willhallonline/ansible:2.21-debian-trixie-slim

RUN apt-get update     && apt-get install -y --no-install-recommends ca-certificates curl     && rm -rf /var/lib/apt/lists/*
```

See [extending images](../usage/extending-images.md) for more patterns.

## Dockerfiles

The Debian Dockerfiles are in the upstream repository under `ansible-core/`:

- [`ansible-core/debian-bookworm/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/debian-bookworm/Dockerfile)
- [`ansible-core/debian-bookworm-slim/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/debian-bookworm-slim/Dockerfile)
- [`ansible-core/debian-trixie/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/debian-trixie/Dockerfile)
- [`ansible-core/debian-trixie-slim/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/debian-trixie-slim/Dockerfile)

## Related pages

- [Supported tags](tags.md)
- [Architectures](architectures.md)
- [Running playbooks](../usage/running-playbooks.md)
- [Security reference](../reference/security.md)
