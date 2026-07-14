# Rocky Linux images

Rocky Linux images provide an Enterprise Linux compatible base for Ansible
automation. They are useful when your control-node tooling, compliance
expectations, or package choices align with the RHEL-compatible ecosystem.

The supported Rocky Linux base is Rocky Linux 10.

## Available Rocky Linux tags

| Base image | Supported tags |
| --- | --- |
| Rocky Linux 10 | `2.21-rockylinux-10`, `2.20-rockylinux-10`, `2.19-rockylinux-10`, `2.18-rockylinux-10`, `2.17-rockylinux-10`, `2.16-rockylinux-10` |

See the complete [supported tag matrix](tags.md) for all operating systems.

## Pull a Rocky Linux image

=== "Latest supported stream"

    ```bash
    docker pull willhallonline/ansible:2.21-rockylinux-10
    ```

=== "Ansible 2.20"

    ```bash
    docker pull willhallonline/ansible:2.20-rockylinux-10
    ```

=== "Ansible 2.16"

    ```bash
    docker pull willhallonline/ansible:2.16-rockylinux-10
    ```

## Run Ansible from a Rocky Linux image

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-rockylinux-10   ansible-playbook -i inventory site.yml
```

Run an ad hoc connectivity check:

```bash
docker run --rm -it   -v "$PWD:/work"   -w /work   willhallonline/ansible:2.21-rockylinux-10   ansible all -i inventory -m ping
```

## Characteristics

| Property | Rocky Linux images |
| --- | --- |
| Package manager | `dnf` |
| C library | glibc |
| Base | Rocky Linux 10 |
| Best fit | Enterprise Linux compatible workflows |
| Watch point | Larger than Alpine and different package names from Debian/Ubuntu |

Rocky Linux is a good match when you manage Enterprise Linux fleets and want the
container control node to feel close to the managed hosts. It is also useful
when internal security or compliance documentation expects RHEL-compatible
commands and package names.

## What's included

Each Rocky Linux image includes:

- `ansible-core` from PyPI;
- the `ansible` community package from PyPI;
- `ansible-lint` from PyPI;
- Python; and
- the tooling needed to run Ansible against remote hosts.

The supporting tooling is selected for Ansible control-node operation, including
remote connectivity, Git workflows, and common runtime dependencies. See
[what's inside](whats-inside.md) for more detail.

## When to choose Rocky Linux

Choose Rocky Linux when:

- your organization standardizes on Enterprise Linux compatible distributions;
- your playbook development mirrors RHEL-like managed nodes;
- you need `dnf` and RPM packaging in your custom image;
- internal documentation assumes RHEL-compatible commands; or
- you want all current Ansible streams on the same Rocky Linux base.

Consider another family when:

- image size is the most important constraint;
- your project uses Debian or Ubuntu package names in wrapper scripts;
- you want slim Debian variants; or
- you need Alpine's minimal footprint.

!!! tip "Match your managed environment"
    If most of your managed hosts are Enterprise Linux systems, using a Rocky
    Linux control-node image can make local testing and dependency installation
    easier to reason about.

## Extending Rocky Linux images

Use `dnf` for operating system packages:

```dockerfile
FROM willhallonline/ansible:2.21-rockylinux-10

RUN dnf install -y jq     && dnf clean all
```

Install Python tools only when the project needs them:

```dockerfile
FROM willhallonline/ansible:2.21-rockylinux-10

RUN pip install --no-cache-dir molecule
```

See [extending images](../usage/extending-images.md) for additional patterns.

## Dockerfile

The Rocky Linux Dockerfile is in the upstream repository under `ansible-core/`:

- [`ansible-core/rockylinux-10/Dockerfile`](https://github.com/willhallonline/docker-ansible/blob/main/ansible-core/rockylinux-10/Dockerfile)

## Related pages

- [Supported tags](tags.md)
- [Architectures](architectures.md)
- [Running playbooks](../usage/running-playbooks.md)
- [FAQ](../reference/faq.md)
