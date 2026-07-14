# Bitbucket Pipelines

Bitbucket Pipelines can run Ansible steps directly in `willhallonline/ansible`. You can set the image globally for the whole pipeline or per step when only some jobs need Ansible.

!!! tip "Pin the image"
    Use an exact tag such as `willhallonline/ansible:2.21-alpine-3.22`. Avoid `latest` in deployment pipelines.

## Prerequisites

- Bitbucket Pipelines enabled for the repository.
- A `bitbucket-pipelines.yml` file at the repository root.
- Playbooks and inventories committed to the repository.
- Repository or workspace variables for Vault and other secrets.
- Bitbucket SSH key settings or secured variables for SSH private keys.

Related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Ansible lint](../usage/ansible-lint.md)

## Minimal pipeline

Set the image at the top level when all steps are Ansible steps.

```yaml
image: willhallonline/ansible:2.21-alpine-3.22

pipelines:
  default:
    - step:
        name: Lint
        script:
          - ansible --version
          - ansible-lint
```

Or set it per step:

```yaml
pipelines:
  default:
    - step:
        name: Lint
        image: willhallonline/ansible:2.21-alpine-3.22
        script:
          - ansible-lint
```

## Full worked pipeline

This pipeline runs lint and syntax checks for all branches and deploys production only from `main`.

```yaml
image: willhallonline/ansible:2.21-alpine-3.22

options:
  max-time: 30

definitions:
  caches:
    ansible-collections: .ansible/collections
    ansible-roles: .ansible/roles
  steps:
    - step: &lint
        name: Lint
        caches:
          - ansible-collections
          - ansible-roles
        script:
          - ansible --version
          - |
            if [ -f requirements.yml ]; then
              ansible-galaxy collection install -r requirements.yml -p .ansible/collections
              ansible-galaxy role install -r requirements.yml -p .ansible/roles || true
            fi
          - ansible-lint

    - step: &syntax
        name: Syntax check
        caches:
          - ansible-collections
          - ansible-roles
        script:
          - |
            if [ -f requirements.yml ]; then
              ansible-galaxy collection install -r requirements.yml -p .ansible/collections
              ansible-galaxy role install -r requirements.yml -p .ansible/roles || true
            fi
          - ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check

    - step: &deploy-production
        name: Deploy production
        deployment: production
        caches:
          - ansible-collections
          - ansible-roles
        script:
          - export ANSIBLE_FORCE_COLOR=true
          - export ANSIBLE_HOST_KEY_CHECKING=False
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
              ansible-galaxy collection install -r requirements.yml -p .ansible/collections
              ansible-galaxy role install -r requirements.yml -p .ansible/roles || true
            fi
          - ansible-playbook -i inventories/production/hosts.yml site.yml --vault-password-file .vault-password

pipelines:
  default:
    - step: *lint
    - step: *syntax

  branches:
    main:
      - step: *lint
      - step: *syntax
      - step: *deploy-production
```

## Repository variables

Create secured repository or workspace variables for values that should not appear in logs.

| Variable | Secured | Purpose |
| --- | --- | --- |
| `ANSIBLE_SSH_PRIVATE_KEY` | Yes | SSH private key used by Ansible. |
| `ANSIBLE_VAULT_PASSWORD` | Yes | Password for Ansible Vault. |

!!! warning "Do not echo secrets"
    Use `printf` to write secrets to files. Avoid `echo` when debugging because secret masking can be imperfect around multiline values.

## SSH key options

Bitbucket has built-in SSH key management for Pipelines. You can either use that feature or inject a private key from a secured variable.

=== "Bitbucket SSH key settings"

    Configure the key under repository settings and add host fingerprints there when possible. Your pipeline can then rely on the configured key.

=== "Secured variable"

    ```yaml
    script:
      - mkdir -p ~/.ssh
      - chmod 700 ~/.ssh
      - printf '%s\n' "$ANSIBLE_SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
      - chmod 600 ~/.ssh/id_ed25519
    ```

## Deployments environments

Use Bitbucket deployment environments for production history and permissions.

```yaml
- step:
    name: Deploy production
    deployment: production
    script:
      - ansible-playbook -i inventories/production/hosts.yml site.yml --vault-password-file .vault-password
```

Set environment-specific variables in Bitbucket if staging and production use different credentials.

## Host key checking

For strict host checking, add known hosts:

```yaml
script:
  - mkdir -p ~/.ssh
  - ssh-keyscan -H example.com >> ~/.ssh/known_hosts
```

For ephemeral test hosts, you can disable checking:

```yaml
script:
  - export ANSIBLE_HOST_KEY_CHECKING=False
```

## Tips

- Use top-level `image:` for simple Ansible-only repositories.
- Use per-step `image:` when the pipeline also builds applications in other containers.
- Use branch pipelines for production deployments.
- Use deployment environments to separate staging and production variables.
- Cache `.ansible/collections` when `requirements.yml` is stable.
- Keep `ansible --version` in the lint step for auditability.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Multiline SSH key fails | Confirm the variable preserves line breaks, including the BEGIN and END lines. |
| Deployment uses wrong environment | Check the `deployment:` name and branch pipeline. |
| Vault password rejected | Confirm the secured variable value is the raw password, not a file path. |
| Host key error | Add known hosts in repository settings or write `~/.ssh/known_hosts`. |
| Pipeline unexpectedly upgraded Ansible | Replace floating tags with an exact image tag. |
