# Woodpecker CI

Woodpecker CI is similar to Drone: each step runs in a container image. Use `willhallonline/ansible` for the steps that lint, syntax-check, and deploy playbooks.

!!! tip "Keep deploy filters strict"
    Use `when:` filters for branch and event conditions so production deployment runs only from trusted refs.

## Prerequisites

- A Woodpecker CI instance connected to your repository.
- A `.woodpecker.yml` file.
- A runner that supports container steps.
- A pinned image tag such as `willhallonline/ansible:2.21-alpine-3.22`.
- Woodpecker secrets for SSH and Vault data.

Related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Galaxy roles and collections](../usage/galaxy-roles-collections.md)

## Minimal pipeline

```yaml
steps:
  lint:
    image: willhallonline/ansible:2.21-alpine-3.22
    commands:
      - ansible --version
      - ansible-lint
```

## Full worked pipeline

This pipeline separates lint, syntax check, and production deployment.

```yaml
steps:
  lint:
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
    when:
      event:
        - push
        - pull_request

  syntax:
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
    when:
      event:
        - push
        - pull_request

  deploy-production:
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

Create Woodpecker secrets for deployment jobs:

```sh
woodpecker-cli secret add \
  --repository owner/repo \
  --name ansible_ssh_private_key \
  --value-file id_ed25519

woodpecker-cli secret add \
  --repository owner/repo \
  --name ansible_vault_password \
  --value "replace-with-password"
```

Inject them with `from_secret`:

```yaml
environment:
  ANSIBLE_SSH_PRIVATE_KEY:
    from_secret: ansible_ssh_private_key
  ANSIBLE_VAULT_PASSWORD:
    from_secret: ansible_vault_password
```

!!! warning "Protect production secrets"
    Scope secrets so they are available only to repositories and events that should deploy. Do not expose production secrets to untrusted pull requests.

## Host key checking

=== "Provision known_hosts"

    ```yaml
    commands:
      - mkdir -p ~/.ssh
      - ssh-keyscan -H example.com >> ~/.ssh/known_hosts
      - chmod 644 ~/.ssh/known_hosts
    ```

=== "Disable host key checking"

    ```yaml
    environment:
      ANSIBLE_HOST_KEY_CHECKING: "False"
    ```

Use the first approach for production where possible.

## Branch and event filters

Use `when` on deploy steps:

```yaml
when:
  branch:
    - main
  event:
    - push
```

This prevents deployment from pull requests or feature branches.

## Caching

Woodpecker cache support depends on your runner and plugins. If available, cache:

```text
/root/.ansible/collections
/root/.ansible/roles
```

Without caching, install Galaxy dependencies in each step because steps are isolated containers.

## Tips

- Use one step per lifecycle stage.
- Use `depends_on` for ordering.
- Keep deployment secrets out of lint and syntax steps.
- Pin exact image tags in every step.
- Use `when` filters for production gates.
- Prefer known hosts for production SSH.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Secret not available | Confirm the secret name and repository scope. |
| Deploy runs on pull requests | Add an `event: push` filter to deploy. |
| SSH connection fails | Verify key formatting and `chmod 600`. |
| Vault cannot decrypt | Confirm the secret value is the Vault password and is written to `.vault-password`. |
| Collections missing | Install `requirements.yml` in every step or configure a cache. |
