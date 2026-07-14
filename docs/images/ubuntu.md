# Ubuntu images

Ubuntu images provide a familiar `apt`-based environment for Ansible automation.
They are a good fit for teams already using Ubuntu workstations, GitHub Actions
runners, cloud images, or internal documentation based on Ubuntu packages.

!!! note "Ubuntu convenience tag"
    The `ubuntu` convenience tag currently points to Ansible 2.21 on Ubuntu
    24.04.

## Available Ubuntu tags

| Base image | Supported tags |
| --- | --- |
| Ubuntu 26.04 | `2.21-ubuntu-26.04`, `2.20-ubuntu-26.04` |
| Ubuntu 24.04 | `2.21-ubuntu-24.04`, `2.20-ubuntu-24.04`, `2.19-ubuntu-24.04`, `2.18-ubuntu-24.04`, `2.17-ubuntu-24.04`, `2.16-ubuntu-24.04` |
| Ubuntu 22.04 | `2.17-ubuntu-22.04`, `2.16-ubuntu-22.04` |

See the complete [supported tag matrix](tags.md) for all base images.

## Pull an Ubuntu image

=== "Convenience tag"

    ```bash
    docker pull willhallonline/ansible:ubuntu
    ```

=== "Ubuntu 24.04"

    ```bash
    docker pull willhallonline/ansible:2.21-ubuntu-24.04
    ```

=== "Ubuntu 26.04"

    ```bash
    docker pull willhallonline/ansible:2.21-ubuntu-26.04
    ```

=== "Ubuntu 22.04"

    ```bash
    docker pull willhallonline/ansible:2.17-ubuntu-22.04
    ```

## Run Ansible from an Ubuntu image

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-ubuntu-24.04   ansible-playbook -i inventory site.yml
```

Run `ansible-lint` in the same container:

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-ubuntu-24.04   ansible-lint
```

## Characteristics

| Property | Ubuntu images |
| --- | --- |
| Package manager | `apt` |
| C library | glibc |
| Best fit | CI, cloud workflows, Ubuntu-based teams |
| Convenience tag | `ubuntu` |
| Watch point | Tags differ by Ubuntu release and Ansible stream coverage |

Ubuntu images are often the easiest choice when project documentation, bootstrap
scripts, or CI examples already assume Ubuntu packages. They also provide a
familiar shell environment for local troubleshooting.

## Release guidance

| Ubuntu release | Guidance |
| --- | --- |
| 26.04 | Use for the newest supported Ubuntu base with Ansible 2.20 or 2.21 |
| 24.04 | Broadest Ubuntu coverage across Ansible 2.16 through 2.21 |
| 22.04 | Use only when you specifically need this older supported base |

!!! tip "Use Ubuntu 24.04 for broad compatibility"
    Ubuntu 24.04 has the widest supported Ubuntu tag coverage and is the target
    of the `ubuntu` convenience tag.

## What's included

Each Ubuntu image includes:

- `ansible-core` from PyPI;
- the `ansible` community package from PyPI;
- `ansible-lint` from PyPI;
- Python; and
- the tooling needed to run Ansible against remote hosts.

That supporting tooling is intended for normal Ansible control-node operation,
including remote SSH access, Git-based workflows, and common dependency handling.
See [what's inside](whats-inside.md) for more detail.

## When to choose Ubuntu

Choose Ubuntu when:

- your CI environment already uses Ubuntu images;
- your team is comfortable debugging Ubuntu containers;
- your custom image needs packages from Ubuntu repositories;
- vendor install instructions target Ubuntu; or
- you want the `ubuntu` convenience tag for quick tests.

Consider another family when:

- you need the smallest image, where [Alpine](alpine.md) is usually better;
- you prefer Debian slim variants;
- your organization standardizes on Enterprise Linux; or
- you need an Ansible stream not available for a specific Ubuntu release.

## Extending Ubuntu images

Use standard non-interactive `apt-get` patterns in Dockerfiles:

```dockerfile
FROM willhallonline/ansible:2.21-ubuntu-24.04

RUN apt-get update     && apt-get install -y --no-install-recommends jq     && rm -rf /var/lib/apt/lists/*
```

Add Python packages only when they are project requirements:

```dockerfile
FROM willhallonline/ansible:2.21-ubuntu-24.04

RUN pip install --no-cache-dir molecule
```

See [extending images](../usage/extending-images.md) for more guidance.

## Dockerfiles

The Ubuntu Dockerfiles are in the upstream repository under `ansible-core/`:

- [`ansible-core/ubuntu-22.04/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/ubuntu-22.04/Dockerfile)
- [`ansible-core/ubuntu-24.04/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/ubuntu-24.04/Dockerfile)
- [`ansible-core/ubuntu-26.04/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/ubuntu-26.04/Dockerfile)

## Related pages

- [Supported tags](tags.md)
- [Architectures](architectures.md)
- [Running playbooks](../usage/running-playbooks.md)
- [CI usage](../ci/index.md)
