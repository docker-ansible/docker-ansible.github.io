# Architectures

Current `willhallonline/ansible` images generally publish AMD64 and ARM64
variants, but platform availability is specific to each tag. For example,
`2.21-ubuntu-24.04` is currently AMD64-only. No ARMv7/32-bit ARM images are
published.

## Supported architectures

| Architecture | Docker platform | Common environments |
| --- | --- | --- |
| AMD64 | `linux/amd64` | Intel and AMD servers, most x86_64 CI runners |
| ARM64 | `linux/arm64` | Apple Silicon, AWS Graviton, ARM servers, 64-bit Raspberry Pi OS |

!!! note "Current image manifests"
    Most current tags publish AMD64 and ARM64 variants. If you use a Raspberry
    Pi, run a 64-bit OS and verify that the selected tag publishes ARM64.

## Pulling images

Docker normally selects the right platform automatically for the host running
the command:

```bash
docker pull willhallonline/ansible:2.21-alpine-3.24
```

You can request a specific platform when needed:

=== "AMD64"

    ```bash
    docker pull --platform linux/amd64 willhallonline/ansible:2.21-alpine-3.24
    ```

=== "ARM64"

    ```bash
    docker pull --platform linux/arm64 willhallonline/ansible:2.21-alpine-3.24
    ```

## Running on Apple Silicon

Apple Silicon Macs use ARM64. Docker Desktop can run the ARM64 image natively:

```bash
docker run --rm \
  --platform linux/arm64 \
  willhallonline/ansible:2.21-alpine-3.24 \
  ansible --version
```

You usually do not need `--platform` on Apple Silicon when the selected tag
publishes ARM64. If omitted, Docker selects an available platform from the image
manifest.

## Running on Raspberry Pi

Use a 64-bit Raspberry Pi operating system so Docker can pull the ARM64 variant:

```bash
docker run --rm \
  --platform linux/arm64 \
  willhallonline/ansible:2.21-alpine-3.24 \
  ansible --version
```

Current image tags do not publish ARMv7/32-bit ARM variants. On 32-bit Raspberry
Pi OS, switch to a 64-bit OS.

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
such as `2.21-alpine-3.24` identifies the Ansible stream and base operating
system. The image manifest then maps that tag to its available platforms.

| Question | Answer |
| --- | --- |
| Do tags include the CPU architecture? | No. Docker selects the matching image from the manifest. |
| Can the same tag run on AMD64 and ARM64? | Usually, but check the selected tag's manifest; `2.21-ubuntu-24.04` is AMD64-only. |
| Does Apple Silicon need a special tag? | No. Use the normal tag. |
| Can I use current tags on 32-bit Raspberry Pi OS? | No. ARMv7/32-bit ARM images are not published. |

!!! tip "Keep tags architecture-neutral"
    In most Dockerfiles and CI definitions, use the same `willhallonline/ansible`
    tag everywhere. Select platforms only in build or test commands when you
    need to force a specific architecture.

## Verifying the platform at runtime

You can inspect the container architecture with `uname`:

```bash
docker run --rm willhallonline/ansible:2.21-alpine-3.24 uname -m
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
