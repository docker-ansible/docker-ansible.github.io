# Docker Ansible GitHub Action

[`willhallonline/docker-ansible-github-action`](https://github.com/willhallonline/docker-ansible-github-action)
provides a GitHub Action for running Ansible in Docker.

The action wraps the Docker Ansible image family so workflows can run
`ansible-playbook` without installing Ansible directly on the GitHub-hosted or
self-hosted runner.

!!! note "Short description"
    `v1.1.0` is the current release of this project-maintained composite action.
    It runs `ansible-playbook` in the non-root `ansible` image user and mounts SSH
    material under `/home/ansible/.ssh`.

## Links

| Resource | Link |
| --- | --- |
| Source repository | <https://github.com/willhallonline/docker-ansible-github-action> |
| Core image project | <https://github.com/willhallonline/docker-ansible> |
| Docker Hub image | <https://hub.docker.com/r/willhallonline/ansible> |
| Docker Ansible GitHub Action Test | <https://github.com/willhallonline/docker-ansible-github-action-test> |

## What it contains

The action repository includes the files expected for a Docker-based GitHub
Action:

| Path | Purpose |
| --- | --- |
| `action.yml` | Action metadata and interface. |
| `entrypoint.sh` | Container entry point used by the action. |
| `examples/` | Example workflow usage. |
| `README.md` | Current usage, inputs, and examples. |

## Inputs and output

The `v1.1.0` action exposes the following contract:

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `playbook` | Yes | — | Path to the Ansible playbook, relative to `working-directory`. |
| `inventory` | No | `''` | Inventory file or directory, relative to `working-directory`. |
| `working-directory` | No | `.` | Directory, relative to the workspace root, from which to run `ansible-playbook`. |
| `requirements` | No | `''` | `requirements.yml` path, relative to `working-directory`, installed with `ansible-galaxy install`. |
| `galaxy-options` | No | `''` | Additional arguments appended to `ansible-galaxy install`. |
| `vault-password` | No | `''` | Plaintext Vault password written to a temporary runner file and passed as `--vault-password-file`; use a secret. |
| `vault-password-file` | No | `''` | Existing Vault password file, relative to `working-directory`; ignored when `vault-password` is set. |
| `private-key` | No | `''` | PEM SSH private key written to a temporary runner file with mode `600`; use a secret. |
| `host-key-checking` | No | `'true'` | Whether to enforce SSH host key checking (`true`/`false`). |
| `known-hosts` | No | `''` | Additional `known_hosts` entries to trust before connecting. |
| `extra-vars` | No | `''` | Value passed to `--extra-vars`: `@file.yml`, `key=value`, or JSON. |
| `options` | No | `''` | Additional raw, space-separated arguments appended to `ansible-playbook`. |
| `image-tag` | No | `latest` | Tag of the `willhallonline/ansible` image to use; see the [available tags](https://hub.docker.com/r/willhallonline/ansible/tags). |

The sole output is `exit-code`, the exit code returned by `ansible-playbook`.
The action requires a runner with Docker. Workflows should grant only
`contents: read` when using `actions/checkout`.

The public README uses `@v1` as a major-version example. For safe pinning,
use the current release tag `@v1.1.0`; `@v1` is not documented here as a
separate repository tag.

## When to use the action

Use the action when you want GitHub Actions to run Ansible tasks with a packaged
Docker Ansible environment.

Common examples include:

- checking playbook syntax;
- running a playbook against test infrastructure;
- running localhost automation inside CI; and
- keeping local and CI Ansible versions aligned.

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

      - uses: willhallonline/docker-ansible-github-action@v1.1.0
        with:
          playbook: playbooks/site.yml
          inventory: inventory/localhost.ini
          image-tag: 2.21-alpine-3.24
```

The action also supports Galaxy requirements, Vault passwords, SSH keys,
`known_hosts`, extra variables, and additional `ansible-playbook` options as
listed in the contract above.

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
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook --version
```

This makes it easier to debug workflow failures before pushing another commit.

## Testing

The action is exercised by the
[`willhallonline/docker-ansible-github-action-test`](https://github.com/willhallonline/docker-ansible-github-action-test)
repository. The core image project is also covered by image-level tests.

The integration-test repository's current release is `v1.1.0`. Its CI runs a
61-tag matrix and pins this action release, but each test remains a localhost
smoke test; it does not prove SSH, Vault, Galaxy, extra-vars, or
deployment-host behaviour. See [Docker Ansible Test](testing.md) for the
complete scope.

## Related documentation

- [Docker Ansible](docker-ansible.md)
- [Docker Ansible Test](testing.md)
- [GitHub Actions usage](../ci/github-actions.md)
- [Troubleshooting](../reference/troubleshooting.md)
- [Security](../reference/security.md)
