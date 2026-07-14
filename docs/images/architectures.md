# Architectures

Current `willhallonline/ansible` images are published as multi-architecture
images for AMD64 and ARM64. This lets the same image tags work across laptops,
CI runners, Apple Silicon Macs, AWS Graviton instances, 64-bit Raspberry Pi OS,
and other 64-bit ARM hosts.

## Supported architectures

| Architecture | Docker platform | Common environments |
| --- | --- | --- |
| AMD64 | `linux/amd64` | Intel and AMD servers, most x86_64 CI runners |
| ARM64 | `linux/arm64` | Apple Silicon, AWS Graviton, ARM servers, 64-bit Raspberry Pi OS |

!!! note "Current image manifests"
    Current tags publish AMD64 and ARM64 variants. 32-bit ARM images are not
    published for current tags. If you use a Raspberry Pi, run a 64-bit OS so
    Docker can pull the ARM64 image. Some older archived tags may have included
    32-bit ARM variants; check Docker Hub tags before relying on archived images.

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

## Running on Apple Silicon

Apple Silicon Macs use ARM64. Docker Desktop can run the ARM64 image natively:

```bash
docker run --rm \
  --platform linux/arm64 \
  willhallonline/ansible:2.21-alpine-3.22 \
  ansible --version
```

You usually do not need `--platform` on Apple Silicon unless you are testing a
specific architecture. If omitted, Docker selects the matching platform from the
multi-architecture image manifest.

## Running on Raspberry Pi

Use a 64-bit Raspberry Pi operating system so Docker can pull the ARM64 variant:

```bash
docker run --rm \
  --platform linux/arm64 \
  willhallonline/ansible:2.21-alpine-3.22 \
  ansible --version
```

Current image tags do not publish 32-bit ARM variants. On 32-bit Raspberry Pi OS,
switch to a 64-bit OS for current images. If you must use an older archived tag,
check the Docker Hub tag details first to confirm which platforms it published.

## Running on AWS Graviton

AWS Graviton instances use ARM64. Pulls on those hosts should resolve to the
ARM64 image automatically:

```bash
docker run --rm willhallonline/ansible:2.21-ubuntu-24.04 ansible --version
```

For explicit platform selection:

```bash
docker run --rm \
  --platform linux/arm64 \
  willhallonline/ansible:2.21-ubuntu-24.04 \
  ansible --version
```

## Choosing a platform in CI

Most CI systems run on AMD64 by default. If you schedule jobs on ARM64 runners,
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
| Can I use current tags on 32-bit Raspberry Pi OS? | No. Use a 64-bit OS, or check Docker Hub for older archived tags that match your platform. |

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

## Related pages

- [Supported tags](tags.md)
- [Alpine images](alpine.md)
- [Ubuntu images](ubuntu.md)
- [CI usage](../ci/index.md)
- [Quick start](../getting-started/quick-start.md)
