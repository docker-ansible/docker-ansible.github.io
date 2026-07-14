# CircleCI

CircleCI jobs can use `willhallonline/ansible` as their Docker executor image. Combine separate lint, syntax, and deploy jobs with workflows so production deployment only starts after checks pass.

!!! tip "Use contexts for deployment secrets"
    Store production SSH and Vault secrets in a restricted CircleCI context rather than project-level variables when multiple projects share deployment credentials.

## Prerequisites

- A `.circleci/config.yml` file.
- CircleCI project enabled.
- Playbook and inventory files in the repository.
- A pinned image tag such as `willhallonline/ansible:2.21-alpine-3.22`.
- Contexts or project environment variables for secrets.
- Optional CircleCI SSH key configured for `add_ssh_keys`.

Related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Galaxy roles and collections](../usage/galaxy-roles-collections.md)

## Minimal job

```yaml
version: 2.1

jobs:
  lint:
    docker:
      - image: willhallonline/ansible:2.21-alpine-3.22
    steps:
      - checkout
      - run:
          name: Show Ansible version
          command: ansible --version
      - run:
          name: Run ansible-lint
          command: ansible-lint

workflows:
  ansible:
    jobs:
      - lint
```

## Full workflow

This workflow runs lint, syntax check, and a production deployment from `main`.

```yaml
version: 2.1

commands:
  install_galaxy:
    description: Install Galaxy dependencies when requirements.yml exists
    steps:
      - restore_cache:
          keys:
            - ansible-galaxy-{{ checksum "requirements.yml" }}
            - ansible-galaxy-
      - run:
          name: Install Galaxy dependencies
          command: |
            if [ -f requirements.yml ]; then
              ansible-galaxy collection install -r requirements.yml -p ~/.ansible/collections
              ansible-galaxy role install -r requirements.yml -p ~/.ansible/roles || true
            fi
      - save_cache:
          key: ansible-galaxy-{{ checksum "requirements.yml" }}
          paths:
            - ~/.ansible/collections
            - ~/.ansible/roles

jobs:
  lint:
    docker:
      - image: willhallonline/ansible:2.21-alpine-3.22
    environment:
      ANSIBLE_FORCE_COLOR: "true"
    steps:
      - checkout
      - install_galaxy
      - run:
          name: Run ansible-lint
          command: |
            ansible --version
            ansible-lint

  syntax:
    docker:
      - image: willhallonline/ansible:2.21-alpine-3.22
    environment:
      ANSIBLE_FORCE_COLOR: "true"
      ANSIBLE_HOST_KEY_CHECKING: "False"
    steps:
      - checkout
      - install_galaxy
      - run:
          name: Syntax check
          command: |
            ansible-playbook \
              -i inventories/staging/hosts.yml \
              site.yml \
              --syntax-check

  deploy:
    docker:
      - image: willhallonline/ansible:2.21-alpine-3.22
    environment:
      ANSIBLE_FORCE_COLOR: "true"
      ANSIBLE_HOST_KEY_CHECKING: "False"
    steps:
      - checkout
      - add_ssh_keys:
          fingerprints:
            - "SHA256:replace-with-your-circleci-key-fingerprint"
      - install_galaxy
      - run:
          name: Prepare SSH and Vault
          command: |
            mkdir -p ~/.ssh
            chmod 700 ~/.ssh
            ssh-keyscan -H example.com >> ~/.ssh/known_hosts
            chmod 644 ~/.ssh/known_hosts
            printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
            chmod 600 .vault-password
      - run:
          name: Deploy production
          command: |
            ansible-playbook \
              -i inventories/production/hosts.yml \
              site.yml \
              --vault-password-file .vault-password

workflows:
  ansible:
    jobs:
      - lint
      - syntax:
          requires:
            - lint
      - deploy:
          context:
            - ansible-production
          requires:
            - syntax
          filters:
            branches:
              only: main
```

## Alternative: SSH key from an environment variable

If you cannot use `add_ssh_keys`, store the key in a restricted context variable.

```yaml
- run:
    name: Install SSH key
    command: |
      mkdir -p ~/.ssh
      chmod 700 ~/.ssh
      printf '%s\n' "$ANSIBLE_SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
      chmod 600 ~/.ssh/id_ed25519
```

Prefer `add_ssh_keys` for keys managed by CircleCI.

## Secrets handling

=== "Context variables"

    Create a context such as `ansible-production` with:

    ```text
    ANSIBLE_VAULT_PASSWORD
    ANSIBLE_SSH_PRIVATE_KEY
    ```

    Attach that context only to deployment jobs.

=== "CircleCI SSH keys"

    ```yaml
    - add_ssh_keys:
        fingerprints:
          - "SHA256:replace-with-your-circleci-key-fingerprint"
    ```

CircleCI injects keys into the job's SSH configuration. Still add known hosts for the targets you deploy to.

## Host key checking

Use known hosts for production:

```yaml
- run:
    name: Add known hosts
    command: |
      mkdir -p ~/.ssh
      ssh-keyscan -H example.com >> ~/.ssh/known_hosts
```

For short-lived test hosts, set:

```yaml
environment:
  ANSIBLE_HOST_KEY_CHECKING: "False"
```

## Tips

- Use workflows to express lint → syntax → deploy dependencies.
- Attach production contexts only to production jobs.
- Use branch filters so deploy jobs run only on `main`.
- Cache Galaxy dependencies using `requirements.yml` as the key.
- Keep the image tag pinned in every Docker executor.
- Add `ansible --version` to lint output for runtime visibility.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `add_ssh_keys` does not add the key | The fingerprint must match a key configured in CircleCI. |
| Deploy job cannot read Vault password | Confirm the workflow job has the production context. |
| Cache step fails when no requirements file exists | Add a small `requirements.yml` or remove cache checksum usage. |
| Deploy runs on non-main branch | Check workflow `filters`, not only job commands. |
| SSH host verification fails | Add target hosts to `~/.ssh/known_hosts`. |
