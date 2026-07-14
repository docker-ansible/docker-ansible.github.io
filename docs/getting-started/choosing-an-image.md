# Choosing an image

Choosing the right Docker Ansible image means choosing two things:

1. the Ansible core version
2. the base operating system

The `willhallonline/ansible` images use predictable tags so you can make that choice
explicit.

```text
<ansible-version>-<os>
```

For example:

```text
2.21-alpine-3.22
2.19-debian-bookworm
2.20-ubuntu-24.04
2.18-rockylinux-10
2.19-debian-bookworm-slim
2.21-debian-trixie
2.21-debian-trixie-slim
```

!!! tip "Short recommendation"
    For local experiments, `latest` is fine. For CI/CD, pin an exact tag. If you are
    unsure which OS family to start with, Alpine is smallest, while Debian slim is a
    good middle ground when you want glibc.

## Start with the Ansible version

Current Ansible core versions available in containers are:

| Ansible core | Use when |
| --- | --- |
| 2.21.0 | You want the newest current container version documented here |
| 2.20.0 | You need the 2.20 feature line |
| 2.19.2 | You need the 2.19 feature line |
| 2.18.9 | You need the 2.18 feature line |
| 2.17.14 | You need the 2.17 feature line |
| 2.16.14 | You need the 2.16 feature line |

Older versions **2.9 through 2.15** exist, but are unmaintained. Use them only for
legacy automation that cannot yet move forward.

## Match your project requirements

Choose the Ansible version that matches your playbooks, collections, and CI policy.

Ask:

- Which `ansible-core` version do our playbooks require?
- Which versions are supported by the collections we use?
- Do we need to match an existing CI pipeline or release branch?
- Are we testing an upgrade from one Ansible core version to another?

If your project does not require a specific older version, start with a current
version and pin the exact image tag.

!!! warning "Do not rely on moving tags for repeatable runs"
    Tags such as `latest`, `alpine`, and `ubuntu` are convenient defaults. They are
    not the best choice for reproducible CI. Use a full tag like
    `2.21-alpine-3.22` instead.

## Then choose the base OS

The base OS affects image size, package behavior, libc compatibility, and how closely
the Ansible control environment resembles the systems or CI images you already use.

| Base OS | Best fit |
| --- | --- |
| Alpine | Smallest images and fastest pulls |
| Debian slim | Good middle ground with glibc and a smaller footprint |
| Debian | Debian-style environment with a fuller base than slim |
| Ubuntu | Match Ubuntu-based CI or operational expectations |
| Rocky Linux | Match Enterprise Linux-style environments |

## Alpine images

Alpine is a strong default when you care about image size and fast pulls.

Use Alpine when:

- you want the smallest practical image family
- you want quick downloads in CI jobs
- your playbooks and collections do not need Debian, Ubuntu, or Enterprise Linux
  system packages inside the control container
- you are comfortable with Alpine as the control environment

Example:

```bash
docker run --rm -it willhallonline/ansible:2.21-alpine-3.22 ansible --version
```

The convenience tags `latest` and `alpine` currently point to Ansible 2.21 on Alpine
3.22.

See [Alpine images](../images/alpine.md).

## Debian and Debian slim images

Debian is a good general-purpose base. Debian slim is often the best middle ground
when you want glibc without choosing a larger distribution image.

Use Debian slim when:

- you want a smaller image than a full distribution base
- you prefer glibc compatibility
- your automation behaves better in a Debian-like control environment
- you want a practical default for teams that do not want Alpine

Examples:

```bash
docker run --rm -it willhallonline/ansible:2.19-debian-bookworm ansible --version
docker run --rm -it willhallonline/ansible:2.21-debian-trixie-slim ansible --version
```

Available Debian families include Bookworm, Bookworm-slim, Trixie, and Trixie-slim.

See [Debian images](../images/debian.md).

## Ubuntu images

Ubuntu images are useful when your CI jobs, developer documentation, or operational
assumptions already use Ubuntu.

Use Ubuntu when:

- your CI runners or examples are Ubuntu-based
- you want the control container to feel familiar to Ubuntu users
- you need to match Ubuntu package expectations in helper scripts
- you want the `ubuntu` convenience tag for local exploration

Example:

```bash
docker run --rm -it willhallonline/ansible:2.20-ubuntu-24.04 ansible --version
```

The `ubuntu` convenience tag currently points to Ansible 2.21 on Ubuntu 24.04.

See [Ubuntu images](../images/ubuntu.md).

## Rocky Linux images

Rocky Linux images are useful when you want the Ansible control environment to align
with Enterprise Linux-style systems.

Use Rocky Linux when:

- your organization standardizes on Enterprise Linux-like environments
- CI or local testing should resemble a Rocky Linux control node
- playbook helper scripts assume an Enterprise Linux-style userland

Example:

```bash
docker run --rm -it willhallonline/ansible:2.18-rockylinux-10 ansible --version
```

See [Rocky Linux images](../images/rockylinux.md).

## Base OS versions available

The image set includes these base OS versions:

- Alpine 3.19, 3.20, 3.21, and 3.22
- Debian Bookworm and Bookworm-slim
- Debian Trixie and Trixie-slim
- Rocky Linux 10
- Ubuntu 22.04, 24.04, and 26.04

For the complete tag list, see [image tags](../images/tags.md).

## Multi-architecture considerations

Current images are multi-architecture:

- AMD64
- ARM64

In most cases Docker chooses the correct architecture automatically for the host. This
makes it practical to use the same tag on x86 CI runners, Apple Silicon, AWS
Graviton, 64-bit Raspberry Pi OS, and other supported 64-bit platforms. 32-bit ARM
images are not published for current tags; use a 64-bit OS for current images, or
check Docker Hub tags if you rely on older archived images.

For details, see [architectures](../images/architectures.md).

## Decision guide

=== "Smallest local image"

    Use Alpine.

    ```text
    2.21-alpine-3.22
    ```

    This is a good fit for fast local tests and quick CI pulls.

=== "Balanced default"

    Use Debian slim.

    ```text
    2.21-debian-trixie-slim
    ```

    This is a practical middle ground when you want glibc and a smaller footprint.

=== "Ubuntu-like workflows"

    Use Ubuntu.

    ```text
    2.20-ubuntu-24.04
    ```

    Choose this when your examples, scripts, or CI assumptions are Ubuntu-oriented.

=== "Enterprise Linux-style workflows"

    Use Rocky Linux.

    ```text
    2.18-rockylinux-10
    ```

    Choose this when you want the control environment to resemble Enterprise
    Linux-style systems.

## CI/CD guidance

For CI, prefer exact tags:

```yaml
image: willhallonline/ansible:2.21-alpine-3.22
```

Avoid:

```yaml
image: willhallonline/ansible:latest
```

The exact syntax depends on the CI system, but the rule is the same: pin the Ansible
version and OS variant so future runs remain predictable.

CI examples are available for:

- [GitHub Actions](../ci/github-actions.md)
- [GitLab CI](../ci/gitlab-ci.md)
- [Bitbucket Pipelines](../ci/bitbucket-pipelines.md)
- [Azure Pipelines](../ci/azure-pipelines.md)
- [Jenkins](../ci/jenkins.md)
- [CircleCI](../ci/circleci.md)
- [Drone](../ci/drone.md)
- [Woodpecker](../ci/woodpecker.md)

## Local development guidance

For local work, choose the image that makes the developer loop easiest.

- Use `latest` when trying the project for the first time.
- Use `alpine` for quick pulls and small local images.
- Use an exact tag once a project standardizes on a version.
- Use shell aliases so the whole team runs the same image command.

See [shell aliases](shell-aliases.md) for copy-and-paste examples.

## Upgrade strategy

When upgrading Ansible versions:

1. Keep the old pinned tag in CI.
2. Test the new tag locally.
3. Run `ansible-lint` and representative playbooks.
4. Update CI to the new exact tag.
5. Document the chosen version in your project README or automation guide.

For example, test a newer version locally:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:2.21-alpine-3.22 \
  ansible-lint
```

Then run one or more playbooks with the same tag.

## Summary

- Choose the Ansible version your project needs.
- Choose Alpine for smallest and fastest pulls.
- Choose Debian slim for a balanced glibc-based image.
- Choose Ubuntu or Rocky Linux when you want to match production or CI expectations.
- Use convenience tags for exploration.
- Pin exact tags in CI/CD.

