# Contributing

Contributions are welcome across the Docker Ansible ecosystem. The main places
to contribute are the core image repository and this documentation site.

!!! note "Be specific"
    When opening issues or pull requests, include the image tag, base OS,
    Ansible version, Docker version, and a minimal reproduction where possible.

## Core project contributions

The core image repository is:

<https://github.com/willhallonline/docker-ansible>

Before contributing, read the upstream contribution guide:

<https://github.com/willhallonline/docker-ansible/blob/main/CONTRIBUTING.md>

Useful contribution areas include:

- bug reports for image build or runtime issues;
- documentation fixes;
- new or updated base image variants;
- Ansible version updates;
- CI and test improvements;
- compatibility notes for collections or Python packages.

## Reporting issues

A good issue usually includes:

| Field | Example |
| --- | --- |
| Image | `willhallonline/ansible:2.21.0-alpine-3.22` |
| Host OS | Ubuntu, macOS, Windows, or CI runner image. |
| Docker version | Output from `docker version`. |
| Command | The exact `docker run` or workflow step. |
| Expected result | What you expected to happen. |
| Actual result | Full error text with secrets removed. |
| Reproduction | Minimal playbook, inventory, or Dockerfile. |

!!! warning "Remove secrets"
    Do not include private keys, tokens, vault passwords, inventory passwords, or
    internal hostnames unless they are safe to disclose.

## Pull requests to the core project

When opening a PR:

1. keep the change focused;
2. explain why the change is needed;
3. update documentation if behaviour changes;
4. add or update tests where appropriate;
5. mention any compatibility impact;
6. follow the upstream `CONTRIBUTING.md` guidance.

## Documentation site contributions

This documentation site lives at:

<https://github.com/docker-ansible/docker-ansible.github.io>

The site uses MkDocs Material.

To work locally:

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open the local MkDocs URL printed by the command.

!!! tip "Keep docs practical"
    Prefer copyable commands, short explanations, and links to the upstream
    repositories for fast-changing details such as exact image tags or GitHub
    Action inputs.

## Documentation style

When editing this site:

- use one `# H1` per page;
- use tables for comparisons;
- use admonitions for notes, tips, and warnings;
- use fenced code blocks with language hints;
- prefer relative links for internal pages;
- avoid duplicating fast-changing release data when an upstream source of truth
  already exists.

## Local documentation checks

For documentation-only changes, a local preview is usually enough:

```bash
mkdocs serve
```

For a production-style build check, run:

```bash
mkdocs build
```

If dependencies are missing, install them from the repository requirements file:

```bash
pip install -r requirements.txt
```

## Security reports

Do not report vulnerabilities in public issues. Use the upstream security policy:

<https://github.com/willhallonline/docker-ansible/blob/main/SECURITY.md>

## Related repositories

| Repository | Purpose |
| --- | --- |
| [`willhallonline/docker-ansible`](https://github.com/willhallonline/docker-ansible) | Core image builds. |
| [`willhallonline/docker-ansible-github-action`](https://github.com/willhallonline/docker-ansible-github-action) | Docker-based GitHub Action. |
| [`willhallonline/docker-ansible-test`](https://github.com/willhallonline/docker-ansible-test) | Image tests. |
| [`willhallonline/docker-ansible-github-action-test`](https://github.com/willhallonline/docker-ansible-github-action-test) | Action tests. |

## License expectations

The Docker Ansible project uses the MIT license. By contributing, expect your
contribution to be distributed under the same project license unless the target
repository states otherwise.

See [License](license.md).
