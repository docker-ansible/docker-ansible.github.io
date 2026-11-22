# Docker Ansible GitHub Action

[`willhallonline/docker-ansible-github-action`](https://github.com/willhallonline/docker-ansible-github-action)
provides a composite GitHub Action for running Ansible in Docker.

The action runs Bash on the GitHub Actions runner, invokes `docker run` against
the selected Docker Ansible image, and mounts the checked-out repository. This
lets workflows run `ansible-playbook` without installing Ansible directly on
the GitHub-hosted or self-hosted runner.

!!! note "Short description"
    `v1.1.2` is the current release of this project-maintained composite action.
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

The action repository includes the files expected for a composite GitHub Action:

| Path | Purpose |
| --- | --- |
| `action.yml` | Action metadata and interface. |
| `entrypoint.sh` | Container entry point used by the action. |
| `examples/` | Example workflow usage. |
| `README.md` | Current usage, inputs, and examples. |

## Inputs and output

The `v1.1.2` action exposes the following contract:

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
The action requires a GitHub Actions runner with Docker and `GITHUB_WORKSPACE`
set by the workflow environment. If `ansible-playbook` exits nonzero, the action
writes that value to `exit-code` and then fails the step.
Workflows should grant only `contents: read` when using `actions/checkout`.

For a localhost-only playbook, use a no-SSH inventory and the local connection:

```ini
[local]
localhost ansible_connection=local
```

```yaml
- name: Local CI smoke test
  hosts: local
  gather_facts: false
  tasks:
    - ansible.builtin.debug:
        msg: "Ansible is running in the action container"
```

Invoke it without `private-key`, `known-hosts`, or other SSH inputs:

```yaml
- uses: willhallonline/docker-ansible-github-action@v1.1.2
  with:
    playbook: playbooks/smoke.yml
    inventory: inventory/localhost.ini
    image-tag: 2.22-alpine-3.24
```

The latest published action release is `v1.1.2`; the repository also publishes
the `v1` major-version tag. Use `@v1.1.2` for an exact release, `@v1` for the
moving major-version reference, or a commit SHA when you need immutable
behaviour. The three-attempt transient Docker image-pull retry was introduced
in `v1.1.1` and remains in `v1.1.2`, with a five-second delay between attempts;
the action fails after the final attempt.

`image-tag` accepts any tag published by
[`willhallonline/ansible`](https://hub.docker.com/r/willhallonline/ansible/tags).
The `2.22-alpine-3.24` value above is a current example; the separate
action-test workflow covers a defined compatibility matrix rather than every
published tag.

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
or SSH material, and then invokes the composite action.

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

      - uses: willhallonline/docker-ansible-github-action@v1.1.2
        with:
          playbook: playbooks/site.yml
          inventory: inventory/localhost.ini
          image-tag: 2.22-alpine-3.24
```

The action also supports Galaxy requirements, Vault passwords, SSH keys,
`known_hosts`, extra variables, and additional `ansible-playbook` options as
listed in the contract above.

## Why this composite action?

The composite action keeps the orchestration in the workflow runner while using
the same `willhallonline/ansible` images as local Docker commands. It can select
any published image tag without requiring a separate action image build.

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

The integration-test repository's current release is `v1.1.1`. Its
[workflow](https://github.com/willhallonline/docker-ansible-github-action-test/blob/main/.github/workflows/test.yml)
enumerates 65 image tags—three aliases plus 62 versioned tags—and pins
`willhallonline/docker-ansible-github-action@v1.1.1`. The matrix contains 45
current Ansible 2.18–2.22 tags and aliases plus 20 retained Ansible 2.16/2.17
tags; Ansible 2.9–2.15 are excluded. Compare it with the core project's
[supported-tags table](https://github.com/willhallonline/docker-ansible#supported-tags-and-respective-dockerfile-links)
when choosing an image. Each test remains a localhost smoke test and does not
prove SSH, Vault, Galaxy, extra variables, deployment-host behaviour, failure
handling, or linting. See [Docker Ansible Test](testing.md) for the complete
scope.

!!! note "2.22 action-test coverage"
    The action-test matrix includes four Ansible Core 2.22 tags:
    `2.22-alpine-3.24`, `2.22-debian-trixie`,
    `2.22-debian-trixie-slim`, and `2.22-ubuntu-26.04`.

## Related documentation

- [Docker Ansible](docker-ansible.md)
- [Docker Ansible Test](testing.md)
- [GitHub Actions usage](../ci/github-actions.md)
- [Troubleshooting](../reference/troubleshooting.md)
- [Security](../reference/security.md)
