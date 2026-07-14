# License

The Docker Ansible project is released under the MIT license.

The upstream license file is available at:

<https://github.com/willhallonline/docker-ansible/blob/main/LICENSE>

This documentation site is aligned with the same MIT licensing approach unless a
repository-level license file states otherwise.

!!! note "Plain-language summary"
    MIT is a permissive open-source license. It generally allows use, copying,
    modification, distribution, and sublicensing, provided the copyright and
    license notice are included.

## Upstream project

| Project | License |
| --- | --- |
| [`willhallonline/docker-ansible`](https://github.com/willhallonline/docker-ansible) | MIT |
| [`willhallonline/ansible`](https://hub.docker.com/r/willhallonline/ansible) images | Built from the MIT-licensed source repository. |
| Documentation site | Aligned with MIT. |

## What the license covers

The MIT license applies to the source repository content, such as Dockerfiles,
scripts, and project documentation, subject to the actual files and notices in
the upstream repository.

Container images also include software from base operating systems, Python
packages, Ansible, Ansible collections, and other dependencies. Those components
have their own licenses.

!!! warning "Check dependency licenses"
    If you redistribute derived images, review the licenses of the base image,
    operating-system packages, Python packages, Ansible collections, and any
    software you add.

## Derived images

If you build a derived image, keep license notices from the upstream project and
from any added dependencies.

Example:

```Dockerfile
FROM willhallonline/ansible:2.21.0-debian-trixie
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
```

Your `requirements.txt` dependencies may bring additional license obligations.

## Documentation reuse

When reusing examples from this documentation, preserve attribution and license
notices where required by the repository license.

## Not legal advice

This page is a documentation summary for users of the Docker Ansible ecosystem.
It is not legal advice. For legal interpretation, consult the actual license text
and your legal counsel.

## Related links

- [Upstream MIT license](https://github.com/willhallonline/docker-ansible/blob/main/LICENSE)
- [Contributing](contributing.md)
- [Security](../reference/security.md)

## Attribution

When sharing substantial portions of the documentation or derived examples,
include a link back to the relevant upstream repository where practical.

Recommended attribution:

```text
Based on the Docker Ansible documentation and the willhallonline/docker-ansible project.
```

## Questions

For project licensing questions, start with the upstream license text. For
questions about your organisation's obligations, seek legal advice before
redistributing modified images or documentation.
