# Ansible Lint

The `willhallonline/ansible` images include `ansible-lint`, so you can validate playbooks, roles, and collections with the same image used to run Ansible.

## Run ansible-lint

Run against a single playbook:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint playbook.yml
```

Run against a site playbook:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint site.yml
```

Run discovery from the project root:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint
```

## Lint roles and directories

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint roles/webserver
```

Multiple paths:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint playbooks roles
```

## Example output

```text
WARNING  Listing 2 violation(s) that are fatal
fqcn[action-core]: Use FQCN for builtin module actions (copy).
roles/webserver/tasks/main.yml:12 Use `ansible.builtin.copy` or `ansible.legacy.copy` instead.

name[missing]: All tasks should be named.
playbooks/site.yml:8 Task/Handler: package
```

Fix the reported files, then rerun the same command.

## Configure .ansible-lint

Create `.ansible-lint` in the project root:

```yaml
profile: production
exclude_paths:
  - .cache/
  - collections/
  - roles/external/
warn_list:
  - experimental
skip_list:
  - yaml[line-length]
```

Run normally:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint
```

!!! note
    Keep skipped rules small and intentional. Skipping too much can hide portability, idempotency, and safety issues.

## Install dependencies before linting

If playbooks depend on Galaxy roles or collections, install them first:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-galaxy install -r requirements.yml
```

Then lint:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint
```

Or combine both steps:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  /bin/sh -c 'ansible-galaxy install -r requirements.yml && ansible-lint'
```

## Pre-commit style local usage

Run before committing:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint --force-color
```

Run against files you changed:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint playbooks/site.yml roles/webserver
```

## Exit codes for CI

`ansible-lint` exits with `0` when no fatal violations are found and non-zero when linting fails.

```bash
docker run --rm \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-lint
```

Example GitLab-style job:

```yaml
ansible_lint:
  image: docker:stable
  services:
    - docker:dind
  script:
    - docker run --rm -v "$PWD:/ansible" --workdir=/ansible willhallonline/ansible:latest ansible-lint
```

See [CI usage](../ci/index.md) for more CI patterns.

## Useful options

```bash
ansible-lint --list-rules
ansible-lint --profile production
ansible-lint --offline
ansible-lint --fix
```

Through Docker:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest ansible-lint --list-rules
```

!!! warning "Review automatic fixes"
    `ansible-lint --fix` can modify files. Review the diff before committing.

## Related guides

- [Galaxy roles and collections](galaxy-roles-collections.md)
- [Docker Compose](docker-compose.md)
- [GitLab CI](../ci/gitlab-ci.md)
- [Troubleshooting](../reference/troubleshooting.md)
