# Alpine images

Alpine images are the smallest supported `willhallonline/ansible` images. They
use Alpine Linux as the base operating system and `apk` as the package manager.
They are a good default when you want fast pulls, compact CI jobs, and a minimal
Ansible control-node container.

!!! note "Default image"
    The `latest` and `alpine` convenience tags currently point to Ansible 2.21
    on Alpine 3.22.

## Available Alpine tags

| Base image | Supported tags |
| --- | --- |
| Alpine 3.22 | `2.21-alpine-3.22`, `2.20-alpine-3.22`, `2.19-alpine-3.22`, `2.18-alpine-3.22`, `2.17-alpine-3.22`, `2.16-alpine-3.22` |
| Alpine 3.21 | `2.21-alpine-3.21`, `2.20-alpine-3.21`, `2.19-alpine-3.21`, `2.18-alpine-3.21`, `2.17-alpine-3.21`, `2.16-alpine-3.21` |
| Alpine 3.20 | `2.21-alpine-3.20`, `2.20-alpine-3.20`, `2.19-alpine-3.20`, `2.18-alpine-3.20`, `2.17-alpine-3.20`, `2.16-alpine-3.20` |
| Alpine 3.19 | `2.19-alpine-3.19`, `2.18-alpine-3.19`, `2.17-alpine-3.19`, `2.16-alpine-3.19` |

See the complete [supported tag matrix](tags.md) for cross-family comparisons.

## Pull an Alpine image

=== "Default Alpine"

    ```bash
    docker pull willhallonline/ansible:alpine
    ```

=== "Latest Alpine stream"

    ```bash
    docker pull willhallonline/ansible:2.21-alpine-3.22
    ```

=== "Older supported stream"

    ```bash
    docker pull willhallonline/ansible:2.16-alpine-3.22
    ```

## Run Ansible from an Alpine image

Mount your playbook project into the container and run from that working
directory:

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-alpine-3.22   ansible-playbook -i inventory site.yml
```

Check the installed tools:

```bash
docker run --rm willhallonline/ansible:2.21-alpine-3.22 ansible --version
docker run --rm willhallonline/ansible:2.21-alpine-3.22 ansible-lint --version
```

## Characteristics

| Property | Alpine images |
| --- | --- |
| Package manager | `apk` |
| C library | musl libc |
| Typical footprint | Smallest supported family |
| Best fit | Fast CI jobs, compact runners, simple control-node use |
| Watch point | Some native Python wheels or vendor tools may assume glibc |

Alpine is based on musl libc rather than glibc. Most Ansible automation works
well on Alpine, especially when playbooks call Ansible modules on remote hosts.
The difference matters most when you install extra Python packages or vendor CLI
tools inside the container.

!!! tip "Use Alpine first for simple jobs"
    If your automation only needs Ansible, SSH access, Git, and common control
    node tools, Alpine is often the fastest image to pull and run.

!!! warning "Check native dependencies"
    If you extend the image with Python packages that compile native extensions,
    test the result. Some projects publish wheels primarily for glibc-based
    distributions.

## What's included

Each Alpine image includes:

- `ansible-core` from PyPI;
- the `ansible` community package from PyPI;
- `ansible-lint` from PyPI;
- Python; and
- the tooling needed to run Ansible against remote hosts.

That supporting tooling typically covers SSH connectivity, Git operations,
certificate handling, and common runtime dependencies used by Ansible workflows.
See [what's inside](whats-inside.md) for more detail.

## When to choose Alpine

Choose Alpine when:

- pull time and disk footprint matter;
- your CI runner creates fresh containers frequently;
- you do not need a glibc userspace;
- your extra dependencies are available in Alpine packages or pure Python
  wheels; or
- you want the same target as the `latest` convenience tag.

Consider Debian, Ubuntu, or Rocky Linux instead when:

- you need glibc compatibility;
- you install vendor tools that only test against Debian-like or Enterprise
  Linux distributions;
- your playbook repository assumes `apt`, `bash`, or GNU userland behavior in
  local wrapper scripts; or
- you prefer a larger but more familiar base environment.

## Extending Alpine images

Use `apk add` for operating system packages:

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

RUN apk add --no-cache jq yq
```

For Python tools, prefer repeatable installs and consider pinning package
versions:

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

RUN pip install --no-cache-dir molecule
```

See [extending images](../usage/extending-images.md) for project-specific image
patterns.

## Dockerfiles

The Alpine Dockerfiles are in the upstream repository under `ansible-core/`:

- [`ansible-core/alpine-3.19/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/alpine-3.19/Dockerfile)
- [`ansible-core/alpine-3.20/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/alpine-3.20/Dockerfile)
- [`ansible-core/alpine-3.21/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/alpine-3.21/Dockerfile)
- [`ansible-core/alpine-3.22/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/alpine-3.22/Dockerfile)

## Related pages

- [Supported tags](tags.md)
- [Architectures](architectures.md)
- [Running playbooks](../usage/running-playbooks.md)
- [Choosing an image](../getting-started/choosing-an-image.md)
