# GitLab CI

GitLab CI can run Ansible directly inside the `willhallonline/ansible` image by setting `image:` at the job level. This keeps runners lightweight and makes Ansible upgrades explicit in `.gitlab-ci.yml`.

!!! note "Upstream example"
    The upstream `docker-ansible` repository itself has a `.gitlab-ci.yml`, so GitLab users can follow the same container-first approach.

## Prerequisites

- A GitLab project with CI/CD enabled.
- A `.gitlab-ci.yml` file.
- Inventory and playbook files in the repository.
- A pinned image tag such as `willhallonline/ansible:2.21-alpine-3.22`.
- CI/CD variables for SSH and Vault secrets.

Related pages:

- [Image tags](../images/tags.md)
- [Galaxy roles and collections](../usage/galaxy-roles-collections.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)

## Minimal job

```yaml
lint:
  image: willhallonline/ansible:2.21-alpine-3.22
  stage: test
  script:
    - ansible --version
    - ansible-lint
```

## Recommended variables

Create these in **Settings → CI/CD → Variables**:

| Variable | Type | Options | Purpose |
| --- | --- | --- | --- |
| `ANSIBLE_SSH_PRIVATE_KEY` | File | Protected, masked if possible | SSH key for managed hosts. |
| `ANSIBLE_VAULT_PASSWORD` | Variable | Protected, masked | Vault password. |

GitLab file variables expose a path to a temporary file. Copy that file into `~/.ssh` and set permissions before deployment.

## Full worked pipeline

```yaml
stages:
  - lint
  - syntax
  - deploy

variables:
  ANSIBLE_FORCE_COLOR: "true"
  ANSIBLE_HOST_KEY_CHECKING: "False"
  ANSIBLE_COLLECTIONS_PATH: "$CI_PROJECT_DIR/.ansible/collections"

cache:
  key:
    files:
      - requirements.yml
  paths:
    - .ansible/collections/
    - .ansible/roles/

.install_galaxy: &install_galaxy
  - |
    if [ -f requirements.yml ]; then
      ansible-galaxy collection install -r requirements.yml -p .ansible/collections
      ansible-galaxy role install -r requirements.yml -p .ansible/roles || true
    fi

.prepare_ssh: &prepare_ssh
  - mkdir -p ~/.ssh
  - chmod 700 ~/.ssh
  - cp "$ANSIBLE_SSH_PRIVATE_KEY" ~/.ssh/id_ed25519
  - chmod 600 ~/.ssh/id_ed25519
  - ssh-keyscan -H example.com >> ~/.ssh/known_hosts
  - chmod 644 ~/.ssh/known_hosts

.prepare_vault: &prepare_vault
  - printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
  - chmod 600 .vault-password

lint:
  image: willhallonline/ansible:2.21-alpine-3.22
  stage: lint
  script:
    - ansible --version
    - *install_galaxy
    - ansible-lint
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'

syntax:
  image: willhallonline/ansible:2.21-alpine-3.22
  stage: syntax
  needs:
    - lint
  script:
    - *install_galaxy
    - ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH'

deploy_production:
  image: willhallonline/ansible:2.21-alpine-3.22
  stage: deploy
  needs:
    - syntax
  environment:
    name: production
  before_script:
    - *prepare_ssh
    - *prepare_vault
  script:
    - *install_galaxy
    - ansible-playbook -i inventories/production/hosts.yml site.yml --vault-password-file .vault-password
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
    - when: never
```

## Alternative: job-level deployment image

You can set the image per job to keep non-Ansible jobs separate.

```yaml
deploy_staging:
  image: willhallonline/ansible:2.21-alpine-3.22
  stage: deploy
  script:
    - ansible-playbook -i inventories/staging/hosts.yml site.yml
```

## Secrets handling

=== "SSH file variable"

    ```yaml
    before_script:
      - mkdir -p ~/.ssh
      - chmod 700 ~/.ssh
      - cp "$ANSIBLE_SSH_PRIVATE_KEY" ~/.ssh/id_ed25519
      - chmod 600 ~/.ssh/id_ed25519
    ```

=== "Vault masked variable"

    ```yaml
    before_script:
      - printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
      - chmod 600 .vault-password
    script:
      - ansible-playbook -i inventories/production/hosts.yml site.yml --vault-password-file .vault-password
    ```

Protect variables that can deploy to production, and restrict production jobs to protected branches.

## Caching Galaxy collections

Use a project-local collections path so GitLab can cache it:

```yaml
variables:
  ANSIBLE_COLLECTIONS_PATH: "$CI_PROJECT_DIR/.ansible/collections"

cache:
  key:
    files:
      - requirements.yml
  paths:
    - .ansible/collections/
```

Install with:

```sh
ansible-galaxy collection install -r requirements.yml -p .ansible/collections
```

## Main-only deploys

Use `rules` to make production deploys main-only:

```yaml
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
    when: manual
  - when: never
```

For stricter control, protect the `main` branch and mark production variables as protected.

## Tips

- Keep `lint`, `syntax`, and `deploy` as separate stages.
- Use file variables for private keys where possible.
- Use masked variables for Vault passwords.
- Pin exact image tags in every Ansible job.
- Use `environment:` for GitLab environment history.
- Keep deployment jobs manual unless your release process requires automatic deploys.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `cp: cannot stat` for SSH key | Confirm `ANSIBLE_SSH_PRIVATE_KEY` is a file variable, not a normal variable. |
| `bad permissions` from SSH | Ensure `chmod 600 ~/.ssh/id_ed25519` ran in `before_script`. |
| Collections reinstall every job | Confirm cache path and `ANSIBLE_COLLECTIONS_PATH` match. |
| Deploy secret unavailable | Protected variables are only available on protected branches/tags. |
| Job does not run on merge requests | Check `rules` and `CI_PIPELINE_SOURCE`. |
