# Older releases

Ansible core streams 2.9 through 2.15 are outside the supported current matrix
and are unmaintained. Treat any historical image reference as a compatibility
exception and verify that the exact tag is still available before using it.

!!! warning "Unmaintained streams"
    These streams no longer receive normal updates. Use them at your own risk
    and migrate to a supported Ansible stream as soon as practical.

## Inactive Ansible streams

| Stream | Status | Notes |
| --- | --- | --- |
| Ansible 2.9 | Outside active matrix | Legacy pre-ansible-core era |
| Ansible 2.10 | Outside active matrix | Unmaintained |
| Ansible 2.11 | Outside active matrix | Unmaintained |
| Ansible 2.12 | Outside active matrix | Unmaintained |
| Ansible 2.13 | Outside active matrix | Unmaintained |
| Ansible 2.14 | Outside active matrix | Final 2.14 release was 2.14.18 |
| Ansible 2.15 | Outside active matrix | Final 2.15 release was 2.15.13 |

Historical tags and definitions may not be published or maintained. Check the
upstream repository and container registry for the exact reference you need.

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
| 2.15 or older on Alpine | `2.21-alpine-3.24` |
| 2.15 or older on Rocky Linux 9 | `2.21-rockylinux-10` |

Migration is usually easiest when done in stages:

1. Update playbooks and collections while still using the old image.
2. Run `ansible-lint` and fix compatibility warnings.
3. Test against a supported image in CI.
4. Update scheduled jobs and documentation to the new tag.
5. Remove old image references from release workflows.

## Use cases for older streams

Acceptable short-term reasons to use a historical image include:

- reproducing a historical CI result;
- testing an old playbook before migration;
- supporting a temporary maintenance branch;
- investigating a regression introduced during an Ansible upgrade; or
- matching a legacy Python runtime while planning remediation.

They are not a good default for new automation.

!!! tip "Create an exit plan"
    If you must use a historical image, record why it is needed, who owns the
    migration, and which supported tag will replace it.

## Supported alternatives

The supported matrix covers Ansible 2.16 through 2.21 across current bases. Good
starting points include:

| Need | Supported tag to evaluate |
| --- | --- |
| Small default image | `2.21-alpine-3.24` |
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
