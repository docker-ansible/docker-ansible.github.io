# Architectures

Current `willhallonline/ansible` images are published for multiple CPU
architectures. This lets the same image tags work across laptops, CI runners,
edge devices, and cloud ARM instances.

## Supported architectures

| Architecture | Docker platform | Common environments |
| --- | --- | --- |
| AMD64 | `linux/amd64` | Intel and AMD servers, most x86_64 CI runners |
| ARM64 | `linux/arm64` | Apple Silicon, AWS Graviton, ARM servers |
| ARMv7 | `linux/arm/v7` | Raspberry Pi and other 32-bit ARM systems |

!!! note "Applies to current images"
    AMD64, ARM64, and ARMv7 are available for all current supported images in
    the matrix.

## Pulling images

Docker normally selects the right platform automatically for the host running
the command:

```bash
docker pull willhallonline/ansible:2.21-alpine-3.22
```

You can request a specific platform when needed:

=== "AMD64"

    ```bash
    docker pull --platform linux/amd64 willhallonline/ansible:2.21-alpine-3.22
    ```

=== "ARM64"

    ```bash
    docker pull --platform linux/arm64 willhallonline/ansible:2.21-alpine-3.22
    ```

=== "ARMv7"

    ```bash
    docker pull --platform linux/arm/v7 willhallonline/ansible:2.21-alpine-3.22
    ```

## Running on Apple Silicon

Apple Silicon Macs use ARM64. Docker Desktop can run the ARM64 image natively:

```bash
docker run --rm   --platform linux/arm64   willhallonline/ansible:2.21-alpine-3.22   ansible --version
```

You usually do not need `--platform` on Apple Silicon unless you are testing a
specific architecture. If omitted, Docker selects the matching platform from the
multi-architecture image manifest.

## Running on Raspberry Pi

Use ARM64 on 64-bit Raspberry Pi operating systems and ARMv7 on 32-bit systems:

=== "64-bit Raspberry Pi OS"

    ```bash
    docker run --rm       --platform linux/arm64       willhallonline/ansible:2.21-alpine-3.22       ansible --version
    ```

=== "32-bit Raspberry Pi OS"

    ```bash
    docker run --rm       --platform linux/arm/v7       willhallonline/ansible:2.21-alpine-3.22       ansible --version
    ```

## Running on AWS Graviton

AWS Graviton instances use ARM64. Pulls on those hosts should resolve to the
ARM64 image automatically:

```bash
docker run --rm willhallonline/ansible:2.21-ubuntu-24.04 ansible --version
```

For explicit platform selection:

```bash
docker run --rm   --platform linux/arm64   willhallonline/ansible:2.21-ubuntu-24.04   ansible --version
```

## Choosing a platform in CI

Most CI systems run on AMD64 by default. If you schedule jobs on ARM runners,
keep the same image tag and let Docker select the platform:

```yaml
container:
  image: willhallonline/ansible:2.21-ubuntu-24.04
```

When building or testing custom images, specify the platform explicitly if the
runner architecture differs from the deployment architecture.

## Platform and tag compatibility

Architecture support is independent of the tag naming scheme. A supported tag
such as `2.21-alpine-3.22` identifies the Ansible stream and base operating
system. The image manifest then maps that tag to the available platforms.

| Question | Answer |
| --- | --- |
| Do tags include the CPU architecture? | No. Docker selects the matching image from the manifest. |
| Can the same tag run on AMD64 and ARM64? | Yes, for current supported images. |
| Does Apple Silicon need a special tag? | No. Use the normal tag. |
| Does ARMv7 need a special tag? | No. Use the normal tag with an ARMv7-capable Docker host. |

!!! tip "Keep tags architecture-neutral"
    In most Dockerfiles and CI definitions, use the same `willhallonline/ansible`
    tag everywhere. Select platforms only in build or test commands when you
    need to force a specific architecture.

## Verifying the platform at runtime

You can inspect the container architecture with `uname`:

```bash
docker run --rm willhallonline/ansible:2.21-alpine-3.22 uname -m
```

Common outputs include:

| Output | Meaning |
| --- | --- |
| `x86_64` | AMD64 |
| `aarch64` | ARM64 |
| `armv7l` | ARMv7 |

## Related pages

- [Supported tags](tags.md)
- [Alpine images](alpine.md)
- [Ubuntu images](ubuntu.md)
- [CI usage](../ci/index.md)
- [Quick start](../getting-started/quick-start.md)
