# Older releases

Older `willhallonline/ansible` images remain available for historical use, but
they are not part of the supported current matrix. Treat them as unmaintained and
use them only when you have a specific compatibility requirement.

!!! warning "Unmaintained images"
    Older release images no longer receive normal updates. Use them at your own
    risk and migrate to a supported Ansible stream as soon as practical.

## Archived Ansible streams

The archived image set includes older Ansible streams:

| Stream | Status | Notes |
| --- | --- | --- |
| Ansible 2.9 | Archived | Legacy pre-ansible-core era |
| Ansible 2.10 | Archived | Unmaintained |
| Ansible 2.11 | Archived | Unmaintained |
| Ansible 2.12 | Archived | Unmaintained |
| Ansible 2.13 | Archived | Unmaintained |
| Ansible 2.14 | Archived | Final 2.14 release was 2.14.18 |
| Ansible 2.15 | Archived | Final 2.15 release was 2.15.13 |

Archived releases may appear on older base images such as:

- Rocky Linux 9;
- Debian Bullseye;
- Ubuntu 20.04; and
- older Alpine releases.

The source repository keeps archived definitions in the `archive/` directory.
The upstream project also documents older releases in its
`docs/older-releases.md` page.

## Why older images are risky

Older images can be useful for reproducing historical automation, but they come
with real trade-offs:

- they no longer receive the same regular dependency updates;
- base operating systems may be out of standard support;
- Python compatibility may be constrained;
- Ansible collections may require newer Ansible versions;
- security fixes may not be available; and
- CI environments may remove support for old dependency stacks.

!!! note "Check Ansible and Python compatibility"
    Ansible-core support is tied to Python versions. Review the upstream
    [Ansible release and maintenance](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html)
    reference before pinning an older stream.

## Migration guidance

Prefer migrating to one of the supported streams:

| If you currently use | Consider migrating to |
| --- | --- |
| 2.15 or older on Ubuntu 20.04 | `2.21-ubuntu-24.04` or another supported Ubuntu tag |
| 2.15 or older on Debian Bullseye | `2.21-debian-trixie` or `2.19-debian-bookworm` |
| 2.15 or older on Alpine | `2.21-alpine-3.22` |
| 2.15 or older on Rocky Linux 9 | `2.21-rockylinux-10` |

Migration is usually easiest when done in stages:

1. Update playbooks and collections while still using the old image.
2. Run `ansible-lint` and fix compatibility warnings.
3. Test against a supported image in CI.
4. Update scheduled jobs and documentation to the new tag.
5. Remove old image references from release workflows.

## Finding archived definitions

Archived Dockerfiles live in the upstream source repository:

```text
archive/
```

Start from the current project page on GitHub:

```text
https://github.com/willhallonline/docker-ansible
```

Look for the archived base and Ansible stream you need, then verify the matching
image tag on Docker Hub.

## Use cases for older images

Acceptable short-term reasons to use an archived image include:

- reproducing a historical CI result;
- testing an old playbook before migration;
- supporting a temporary maintenance branch;
- investigating a regression introduced during an Ansible upgrade; or
- matching a legacy Python runtime while planning remediation.

They are not a good default for new automation.

!!! tip "Create an exit plan"
    If you must use an archived image, record why it is needed, who owns the
    migration, and which supported tag will replace it.

## Supported alternatives

The supported matrix covers Ansible 2.16 through 2.21 across current bases. Good
starting points include:

| Need | Supported tag to evaluate |
| --- | --- |
| Small default image | `2.21-alpine-3.22` |
| Ubuntu compatibility | `2.21-ubuntu-24.04` |
| Debian compatibility | `2.21-debian-trixie` |
| Enterprise Linux compatibility | `2.21-rockylinux-10` |
| Older supported Ansible stream | Any available `2.16` to `2.20` matrix tag |

See [supported tags](tags.md) for the full current matrix.

## Related pages

- [Supported tags](tags.md)
- [What's inside](whats-inside.md)
- [Choosing an image](../getting-started/choosing-an-image.md)
- [Docker Ansible project](../projects/docker-ansible.md)
