# GitHub Actions

GitHub Actions can run `willhallonline/ansible` either as a job container or through the official Docker-based action. Use a job container when you want normal shell steps. Use the action when you prefer a reusable action wrapper.

!!! tip "Recommended image"
    Pin a specific tag, for example `willhallonline/ansible:2.21-alpine-3.22`. Do not use `latest` for deployment workflows.

## Prerequisites

- A workflow in `.github/workflows/`.
- An Ansible playbook such as `site.yml`.
- Inventory files such as `inventories/staging/hosts.yml` and `inventories/production/hosts.yml`.
- Optional `requirements.yml` for Galaxy roles and collections.
- Repository or environment secrets for SSH and Vault data.

Useful related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Ansible lint](../usage/ansible-lint.md)
- [GitHub Action project](../projects/github-action.md)

## Option 1: use the image as a job container

A job container makes every `run` step execute inside the Ansible image.

```yaml
name: ansible-ci

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  lint:
    runs-on: ubuntu-latest
    container:
      image: willhallonline/ansible:2.21-alpine-3.22
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Show Ansible version
        run: ansible --version

      - name: Run ansible-lint
        run: ansible-lint
```

## Option 2: use the official action

There is an official action repository: [willhallonline/docker-ansible-github-action](https://github.com/willhallonline/docker-ansible-github-action). It is described as "A GitHub Action using Ansible in Docker" and runs Ansible commands inside the `docker-ansible` container.

!!! note "Check current inputs"
    The action repository contains the current `action.yml` and `entrypoint.sh`. Use that repository as the source of truth for supported inputs.

A minimal shape is:

```yaml
name: ansible-action

on:
  workflow_dispatch:

jobs:
  ansible:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run docker-ansible action
        uses: willhallonline/docker-ansible-github-action@main
        with:
          args: ansible --version
```

If the action changes its input names, update this example from the repository documentation.

## Full worked workflow

This workflow runs lint and syntax checks for pull requests and deploys only from `main`.

```yaml
name: ansible

on:
  pull_request:
  push:
    branches:
      - main
  workflow_dispatch:

env:
  ANSIBLE_FORCE_COLOR: "true"
  ANSIBLE_HOST_KEY_CHECKING: "False"

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    container:
      image: willhallonline/ansible:2.21-alpine-3.22
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Galaxy dependencies
        run: |
          if [ -f requirements.yml ]; then
            ansible-galaxy collection install -r requirements.yml
            ansible-galaxy role install -r requirements.yml || true
          fi

      - name: Run ansible-lint
        run: ansible-lint

  syntax:
    name: Syntax check
    runs-on: ubuntu-latest
    needs: lint
    container:
      image: willhallonline/ansible:2.21-alpine-3.22
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Galaxy dependencies
        run: |
          if [ -f requirements.yml ]; then
            ansible-galaxy collection install -r requirements.yml
            ansible-galaxy role install -r requirements.yml || true
          fi

      - name: Syntax check staging playbook
        run: |
          ansible-playbook \
            -i inventories/staging/hosts.yml \
            site.yml \
            --syntax-check

  deploy:
    name: Deploy production
    runs-on: ubuntu-latest
    needs: syntax
    if: github.ref == 'refs/heads/main'
    environment: production
    container:
      image: willhallonline/ansible:2.21-alpine-3.22
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install SSH key
        env:
          SSH_PRIVATE_KEY: ${{ secrets.ANSIBLE_SSH_PRIVATE_KEY }}
        run: |
          mkdir -p ~/.ssh
          chmod 700 ~/.ssh
          printf '%s\n' "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519

      - name: Add known hosts
        run: |
          ssh-keyscan -H example.com >> ~/.ssh/known_hosts
          chmod 644 ~/.ssh/known_hosts

      - name: Write Vault password
        env:
          ANSIBLE_VAULT_PASSWORD: ${{ secrets.ANSIBLE_VAULT_PASSWORD }}
        run: |
          printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
          chmod 600 .vault-password

      - name: Install Galaxy dependencies
        run: |
          if [ -f requirements.yml ]; then
            ansible-galaxy collection install -r requirements.yml
            ansible-galaxy role install -r requirements.yml || true
          fi

      - name: Deploy
        run: |
          ansible-playbook \
            -i inventories/production/hosts.yml \
            site.yml \
            --vault-password-file .vault-password
```

## Secrets handling

Store these values as repository, organization, or environment secrets:

| Secret | Purpose |
| --- | --- |
| `ANSIBLE_SSH_PRIVATE_KEY` | Private key used by Ansible to connect to hosts. |
| `ANSIBLE_VAULT_PASSWORD` | Password for encrypted variables. |

Production secrets should be environment secrets protected by required reviewers.

=== "Inline secret"

    ```yaml
    - name: Write Vault password
      env:
        ANSIBLE_VAULT_PASSWORD: ${{ secrets.ANSIBLE_VAULT_PASSWORD }}
      run: |
        printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
        chmod 600 .vault-password
    ```

=== "Known hosts"

    ```yaml
    - name: Add known hosts
      run: |
        mkdir -p ~/.ssh
        ssh-keyscan -H example.com >> ~/.ssh/known_hosts
    ```

## Caching Galaxy dependencies

Cache installed collections if your `requirements.yml` is stable.

```yaml
- name: Cache Ansible collections
  uses: actions/cache@v4
  with:
    path: ~/.ansible/collections
    key: ansible-collections-${{ hashFiles('requirements.yml') }}
```

Place the cache step before `ansible-galaxy collection install`.

## Tips

- Keep lint and syntax checks separate from deployment.
- Use `environment: production` for review gates.
- Print `ansible --version` when debugging image upgrades.
- Prefer pinned action SHAs or release tags for third-party actions.
- Use `ANSIBLE_HOST_KEY_CHECKING=False` only when the risk is acceptable.
- Keep inventory and playbook paths explicit.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `Permission denied (publickey)` | Confirm the private key secret preserves newlines and has `chmod 600`. |
| Vault decryption fails | Ensure the secret has no trailing newline problems and the playbook uses `--vault-password-file`. |
| Collection not found | Install `requirements.yml` before lint and syntax-check stages. |
| Deployment runs on pull requests | Add `if: github.ref == 'refs/heads/main'` and use protected environments. |
| Host key verification fails | Add `known_hosts` or set `ANSIBLE_HOST_KEY_CHECKING=False` for ephemeral hosts. |
