# Older releases

Ansible core streams 2.9 through 2.17 are outside the supported current matrix
and are unmaintained. Treat any historical image reference as a compatibility
exception and verify that the exact tag is still available before using it.

!!! warning "Unmaintained streams"
    These streams no longer receive normal updates. Use them at your own risk
    and migrate to a supported Ansible stream as soon as practical.

## Current supported streams

The active image matrix is separate from the historical definitions below:

| Stream | Current patch |
| --- | --- |
| Ansible 2.18 | 2.18.19 |
| Ansible 2.19 | 2.19.14 |
| Ansible 2.20 | 2.20.10 |
| Ansible 2.21 | 2.21.5 |

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
| Ansible 2.16 | Outside active matrix | Final 2.16 release was 2.16.19 |
| Ansible 2.17 | Outside active matrix | Final 2.17 release was 2.17.14 |

## Archived image definitions

The upstream repository keeps historical Dockerfiles under the versioned
`archive/ansible-core/` directory. These are the archive paths that exist in
the `v6.4.10` source tree:

| Historical base | Archive path |
| --- | --- |
| Alpine 3.18 | [`archive/ansible-core/alpine-3.18`](https://github.com/willhallonline/docker-ansible/tree/v6.4.10/archive/ansible-core/alpine-3.18) |
| Alpine 3.19 | [`archive/ansible-core/alpine-3.19`](https://github.com/willhallonline/docker-ansible/tree/v6.4.10/archive/ansible-core/alpine-3.19) |
| Debian Bullseye | [`archive/ansible-core/debian-bullseye`](https://github.com/willhallonline/docker-ansible/tree/v6.4.10/archive/ansible-core/debian-bullseye) |
| Debian Bullseye Slim | [`archive/ansible-core/debian-bullseye-slim`](https://github.com/willhallonline/docker-ansible/tree/v6.4.10/archive/ansible-core/debian-bullseye-slim) |
| Rocky Linux 9 | [`archive/ansible-core/rockylinux-9`](https://github.com/willhallonline/docker-ansible/tree/v6.4.10/archive/ansible-core/rockylinux-9) |
| Ubuntu 20.04 | [`archive/ansible-core/ubuntu-20.04`](https://github.com/willhallonline/docker-ansible/tree/v6.4.10/archive/ansible-core/ubuntu-20.04) |

Alpine 3.20 was removed from the supported builds and does not have an
`archive/ansible-core/alpine-3.20` directory in this source tree. Historical
registry tags may still be visible, but they are not active builds or supported
archive definitions. Verify any exact tag in Docker Hub before using it.

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
| 2.17 or older on Ubuntu 20.04 | `2.21-ubuntu-24.04` or another supported Ubuntu tag |
| 2.17 or older on Debian Bullseye | `2.21-debian-trixie` or `2.19-debian-bookworm` |
| 2.17 or older on Alpine | `2.21-alpine-3.24` |
| 2.17 or older on Rocky Linux 9 | `2.21-rockylinux-10` |

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

The supported matrix covers Ansible 2.18 through 2.21 across current bases. Good
starting points include:

| Need | Supported tag to evaluate |
| --- | --- |
| Small default image | `2.21-alpine-3.24` |
| Ubuntu compatibility | `2.21-ubuntu-24.04` |
| Debian compatibility | `2.21-debian-trixie` |
| Enterprise Linux compatibility | `2.21-rockylinux-10` |
| Older supported Ansible stream | Any available `2.18` to `2.20` matrix tag |

See [supported tags](tags.md) for the full current matrix.

## Related pages

- [Supported tags](tags.md)
- [What's inside](whats-inside.md)
- [Choosing an image](../getting-started/choosing-an-image.md)
- [Docker Ansible project](../projects/docker-ansible.md)
