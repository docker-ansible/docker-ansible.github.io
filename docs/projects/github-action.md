# Docker Ansible GitHub Action

[`willhallonline/docker-ansible-github-action`](https://github.com/willhallonline/docker-ansible-github-action)
provides a GitHub Action for running Ansible in Docker.

The action wraps the Docker Ansible image family so workflows can run Ansible
commands without installing Ansible directly on the GitHub-hosted or self-hosted
runner.

!!! note "Short description"
    A GitHub Action using Ansible in Docker.

## Links

| Resource | Link |
| --- | --- |
| Source repository | <https://github.com/willhallonline/docker-ansible-github-action> |
| Core image project | <https://github.com/willhallonline/docker-ansible> |
| Docker Hub image | <https://hub.docker.com/r/willhallonline/ansible> |
| Action test repository | <https://github.com/willhallonline/docker-ansible-github-action-test> |

## What it contains

The action repository includes the files expected for a Docker-based GitHub
Action:

| Path | Purpose |
| --- | --- |
| `action.yml` | Action metadata and interface. |
| `entrypoint.sh` | Container entry point used by the action. |
| `examples/` | Example workflow usage. |
| `README.md` | Current usage, inputs, and examples. |

!!! tip "Use the action README for current inputs"
    GitHub Action inputs can change over time. This documentation explains the
    purpose and architecture; use the action repository README as the source of
    truth for exact workflow syntax and current input names.

## When to use the action

Use the action when you want GitHub Actions to run Ansible tasks with a packaged
Docker Ansible environment.

Common examples include:

- linting Ansible content with `ansible-lint`
- checking playbook syntax
- running a playbook against test infrastructure
- running localhost automation inside CI
- keeping local and CI Ansible versions aligned

## Typical workflow shape

A workflow normally checks out your repository, configures any required secrets
or SSH material, and then invokes the Docker-based action.

```yaml
name: ansible

on:
  pull_request:
  push:
    branches: [main]

jobs:
  run-ansible:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # See the action README for current input names and examples.
      - uses: willhallonline/docker-ansible-github-action@main
        with:
          args: ansible --version
```

The exact `with:` values above are illustrative. Always check the upstream
README before copying workflow syntax into production.

## Why a Docker-based action?

A Docker-based action gives the action author control over the runtime image.
That makes it easier to align CI with the same `willhallonline/ansible` images
used by local Docker commands.

| Benefit | Detail |
| --- | --- |
| Consistent runtime | CI uses the packaged Ansible environment. |
| Fewer runner mutations | No need to install Ansible packages directly on the runner. |
| Easier version selection | Workflows can align with the image tags used elsewhere. |
| Portable examples | Users can reproduce many CI commands locally with `docker run`. |

## Secrets and SSH material

Ansible workflows often need credentials. In GitHub Actions, keep secrets in
GitHub Actions secrets or another approved secret manager.

!!! warning "Do not bake secrets into images"
    Do not place private keys, vault passwords, tokens, or inventory credentials
    into derived Docker images. Pass them at runtime using CI secret mechanisms
    and restrict file permissions.

If your playbook uses SSH, a workflow usually needs to:

1. write the private key from a secret to a file;
2. set permissions such as `chmod 600`;
3. configure `known_hosts` or host key policy;
4. mount or expose the file only to the step that needs it.

## Local equivalent

Most action behaviour should be reproducible with the core Docker image. For
example:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible --version
```

This makes it easier to debug workflow failures before pushing another commit.

## Testing

The action is exercised by the
[`willhallonline/docker-ansible-github-action-test`](https://github.com/willhallonline/docker-ansible-github-action-test)
repository. The core image project is also covered by image-level tests.

See [Testing](testing.md) for smoke-test commands you can run yourself.

## Related documentation

- [Docker Ansible](docker-ansible.md)
- [Testing](testing.md)
- [GitHub Actions usage](../ci/github-actions.md)
- [Troubleshooting](../reference/troubleshooting.md)
- [Security](../reference/security.md)
