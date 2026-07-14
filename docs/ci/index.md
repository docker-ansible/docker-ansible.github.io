# CI/CD with docker-ansible

The `willhallonline/ansible` images package Ansible for repeatable automation in CI/CD systems. They are useful when you want the same Ansible runtime on laptops, pull requests, scheduled jobs, and production deployment pipelines.

Use this section to pick a CI system and copy a working pipeline shape. Each page shows a minimal example and a fuller lint → syntax check → deploy workflow.

!!! tip "Start with a pinned tag"
    Prefer an exact image tag such as `willhallonline/ansible:2.21-alpine-3.22` in CI. Avoid `latest` for pipelines because an automatic image update can change Ansible, Python, or operating-system packages without a pull request.

## Why run Ansible in a container in CI?

A containerised Ansible runtime gives you a stable toolchain:

- the same `ansible-playbook` binary in every job;
- predictable versions of `ansible-core`, the `ansible` package, and `ansible-lint`;
- no need to install Ansible on each CI worker;
- smaller pipeline setup scripts;
- easier upgrades by changing one image tag;
- repeatable behaviour across hosted and self-hosted runners.

The image name is:

```text
willhallonline/ansible
```

Common tags include exact version/platform tags such as:

```text
willhallonline/ansible:2.21-alpine-3.22
```

Convenience tags such as `latest`, `alpine`, and `ubuntu` are available, but they are best kept for local experiments or non-production jobs.

## General pipeline pattern

Most CI systems can use the same three-stage shape:

1. **Lint**: run `ansible-lint` against playbooks, roles, and collections.
2. **Syntax check**: run `ansible-playbook --syntax-check` with the same inventory and variables structure used by deployment.
3. **Deploy**: run `ansible-playbook` only for protected branches, tags, environments, or manually approved jobs.

A typical command sequence is:

```sh
ansible --version
ansible-galaxy collection install -r requirements.yml
ansible-lint
ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
ansible-playbook -i inventories/production/hosts.yml site.yml
```

If your repository uses roles instead of collections, install both role and collection requirements:

```sh
ansible-galaxy role install -r requirements.yml
ansible-galaxy collection install -r requirements.yml
```

See also:

- [Image tags](../images/tags.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Ansible lint](../usage/ansible-lint.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Galaxy roles and collections](../usage/galaxy-roles-collections.md)
- [Security reference](../reference/security.md)

## Pin exact tags

Use exact tags in CI configuration:

```yaml
image: willhallonline/ansible:2.21-alpine-3.22
```

Do not use this for production deployments:

```yaml
image: willhallonline/ansible:latest
```

!!! warning "Do not deploy from floating tags"
    Floating tags are convenient, but they turn every pipeline run into a possible Ansible runtime upgrade. Pin exact tags and update them intentionally.

## Handle secrets deliberately

Ansible deployment jobs commonly need:

- an SSH private key;
- a Vault password or Vault identity file;
- cloud provider credentials;
- inventory-specific tokens.

Store those values in the CI system's secret store, not in the repository. Write secret files with restrictive permissions before running Ansible:

```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cp "$SSH_PRIVATE_KEY_FILE" ~/.ssh/id_ed25519
chmod 600 ~/.ssh/id_ed25519
printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .vault-password
chmod 600 .vault-password
```

Then pass the Vault password file explicitly:

```sh
ansible-playbook -i inventories/production/hosts.yml site.yml \
  --vault-password-file .vault-password
```

!!! note "Prefer known_hosts over disabling checks"
    `ANSIBLE_HOST_KEY_CHECKING=False` is useful for short-lived test environments. Production deployment jobs should provision `~/.ssh/known_hosts` with `ssh-keyscan` output or a checked-in known-hosts file that matches your infrastructure policy.

## Common repository layout

The examples in this section assume a layout like this:

```text
.
├── ansible.cfg
├── requirements.yml
├── site.yml
├── inventories/
│   ├── staging/
│   │   └── hosts.yml
│   └── production/
│       └── hosts.yml
├── group_vars/
└── roles/
```

Adjust inventory paths and playbook names to match your repository.

## CI systems covered

| CI system | Container support | Secret features to use | Deployment gate pattern | Page |
| --- | --- | --- | --- | --- |
| GitHub Actions | Job containers and Docker actions | Secrets, environments, OpenID Connect where appropriate | Branch filters, environments, required reviewers | [GitHub Actions](github-actions.md) |
| GitLab CI | Job-level images | CI/CD variables, file variables, protected variables | `rules`, protected branches, environments | [GitLab CI](gitlab-ci.md) |
| Bitbucket Pipelines | Step images | Repository/workspace variables, secured variables, SSH key settings | Branch pipelines and deployments | [Bitbucket Pipelines](bitbucket-pipelines.md) |
| Azure Pipelines | Container jobs or `docker run` | Secure files, variable groups, secret variables | Multi-stage approvals and environments | [Azure Pipelines](azure-pipelines.md) |
| Jenkins | Docker agents and `inside` blocks | Credentials Binding plugin | Declarative stages, input gates, protected jobs | [Jenkins](jenkins.md) |
| CircleCI | Docker executors | Contexts, project environment variables, `add_ssh_keys` | Workflows with branch filters | [CircleCI](circleci.md) |
| Drone CI | Step images | Repository/org secrets with `from_secret` | `when` filters and protected events | [Drone CI](drone.md) |
| Woodpecker CI | Step images | Secrets injected as environment variables | `when` branch/event filters | [Woodpecker CI](woodpecker.md) |

## Minimal portable commands

These commands appear throughout the examples. Keep them in scripts if you want each CI system to call the same logic.

=== "Lint"

    ```sh
    ansible --version
    ansible-lint
    ```

=== "Syntax check"

    ```sh
    ansible-galaxy collection install -r requirements.yml
    ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
    ```

=== "Deploy"

    ```sh
    ansible-playbook -i inventories/production/hosts.yml site.yml \
      --vault-password-file .vault-password
    ```

## Upgrade workflow

Treat image upgrades as normal dependency updates:

1. Change `willhallonline/ansible:2.21-alpine-3.22` to the target tag.
2. Run lint and syntax-check jobs on a pull request.
3. Run a staging deployment.
4. Promote the same commit to production.
5. Keep a rollback commit ready if downstream collections or roles rely on old Ansible behaviour.

## Troubleshooting checklist

- Run `ansible --version` in the job to confirm the image tag used.
- Check `ansible.cfg` paths inside the container.
- Confirm the CI workspace is mounted as the working directory.
- Verify SSH key permissions are `600` and the `.ssh` directory is `700`.
- Print inventory hostnames with `ansible-inventory --list` when debugging inventory parsing.
- Use `--syntax-check` before deployment to catch YAML and playbook errors early.
- Install Galaxy dependencies before linting when lint rules import collection plugins.
- Use protected variables for production secrets.
- Avoid echoing secret values; write them directly to files.
- Prefer environment approvals for production deployments.
