# Drone CI

Drone CI runs each pipeline step in a container, so `willhallonline/ansible` fits naturally as the image for lint, syntax-check, and deploy steps.

!!! tip "Use repository secrets"
    Put SSH private keys and Vault passwords in Drone secrets and inject them with `from_secret` only into steps that need them.

## Prerequisites

- A Drone server connected to your Git repository.
- A `.drone.yml` file.
- Docker runner or another runner that supports container images.
- A pinned image tag such as `willhallonline/ansible:2.21-alpine-3.22`.
- Drone secrets for deployment credentials.

Related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Security reference](../reference/security.md)

## Minimal pipeline

```yaml
kind: pipeline
name: ansible

type: docker

steps:
  - name: lint
    image: willhallonline/ansible:2.21-alpine-3.22
    commands:
      - ansible --version
      - ansible-lint
```

## Full worked pipeline

This pipeline runs lint and syntax check for pushes and pull requests, then deploys from `main`.

```yaml
kind: pipeline
name: ansible

type: docker

steps:
  - name: lint
    image: willhallonline/ansible:2.21-alpine-3.22
    environment:
      ANSIBLE_FORCE_COLOR: "true"
    commands:
      - ansible --version
      - |
        if [ -f requirements.yml ]; then
          ansible-galaxy collection install -r requirements.yml
          ansible-galaxy role install -r requirements.yml || true
        fi
      - ansible-lint

  - name: syntax
    image: willhallonline/ansible:2.21-alpine-3.22
    environment:
      ANSIBLE_FORCE_COLOR: "true"
      ANSIBLE_HOST_KEY_CHECKING: "False"
    commands:
      - |
        if [ -f requirements.yml ]; then
          ansible-galaxy collection install -r requirements.yml
          ansible-galaxy role install -r requirements.yml || true
        fi
      - ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
    depends_on:
      - lint

  - name: deploy-production
    image: willhallonline/ansible:2.21-alpine-3.22
    environment:
      ANSIBLE_FORCE_COLOR: "true"
      ANSIBLE_HOST_KEY_CHECKING: "False"
      ANSIBLE_SSH_PRIVATE_KEY:
        from_secret: ansible_ssh_private_key
      ANSIBLE_VAULT_PASSWORD:
        from_secret: ansible_vault_password
    commands:
      - mkdir -p ~/.ssh
      - chmod 700 ~/.ssh
      - printf '%s\n' "$ANSIBLE_SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
      - chmod 600 ~/.ssh/id_ed25519
      - ssh-keyscan -H example.com >> ~/.ssh/known_hosts
      - chmod 644 ~/.ssh/known_hosts
      - printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
      - chmod 600 .vault-password
      - |
        if [ -f requirements.yml ]; then
          ansible-galaxy collection install -r requirements.yml
          ansible-galaxy role install -r requirements.yml || true
        fi
      - ansible-playbook -i inventories/production/hosts.yml site.yml --vault-password-file .vault-password
    depends_on:
      - syntax
    when:
      branch:
        - main
      event:
        - push
```

## Secrets handling

Create Drone secrets named for their purpose:

```sh
drone secret add --repository owner/repo --name ansible_ssh_private_key --data @id_ed25519
drone secret add --repository owner/repo --name ansible_vault_password --data "replace-with-password"
```

Then inject them into only the deploy step:

```yaml
environment:
  ANSIBLE_SSH_PRIVATE_KEY:
    from_secret: ansible_ssh_private_key
  ANSIBLE_VAULT_PASSWORD:
    from_secret: ansible_vault_password
```

!!! warning "Secret command example"
    The `drone secret add` commands above are examples. Do not paste real secrets into shared terminals or logs.

## Host key checking

=== "Known hosts"

    ```yaml
    commands:
      - mkdir -p ~/.ssh
      - ssh-keyscan -H example.com >> ~/.ssh/known_hosts
      - chmod 644 ~/.ssh/known_hosts
    ```

=== "Disable for ephemeral hosts"

    ```yaml
    environment:
      ANSIBLE_HOST_KEY_CHECKING: "False"
    ```

Known hosts are recommended for production.

## Caching

Drone cache configuration depends on installed plugins and runner type. If your installation provides a cache plugin, cache Ansible paths keyed by `requirements.yml`:

```text
/root/.ansible/collections
/root/.ansible/roles
```

If no cache plugin is available, keep the install step explicit and repeatable.

## Tips

- Use one Drone step per Ansible stage.
- Use `depends_on` to enforce lint before syntax and syntax before deploy.
- Inject secrets only into deployment steps.
- Use `when` filters for branch and event gating.
- Pin exact image tags in every step.
- Keep deployment commands in the repository so the pipeline remains reviewable.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Secret is empty | Confirm the secret name in `from_secret` matches Drone exactly. |
| Deploy runs for pull requests | Add `event: push` in the deploy step `when` filter. |
| SSH key has bad permissions | Write it to `~/.ssh/id_ed25519` and `chmod 600`. |
| Galaxy dependencies missing | Install `requirements.yml` in every isolated step. |
| Host key verification fails | Add `known_hosts` or set `ANSIBLE_HOST_KEY_CHECKING=False` for tests. |
