# Running playbooks

Use the `willhallonline/ansible` image to run Ansible without installing it directly on your workstation or CI runner.

The standard convention is:

- mount your project at `/ansible`
- set `--workdir=/ansible`
- keep `ansible.cfg`, inventories, roles, collections, and playbooks in the mounted project

## Interactive shell

Open a shell to inspect the image or debug commands:

```bash
docker run --rm -it willhallonline/ansible:latest /bin/sh
```

With your project mounted:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  /bin/sh
```

Inside the shell:

```bash
ansible --version
ansible-playbook --version
ansible-inventory -i inventory.ini --graph
```

## One-shot playbook run

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

With inventory and an SSH key:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

Canonical compact example:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/id_rsa \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

## Inventory files

INI inventory:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

YAML inventory:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventories/production.yml site.yml
```

Inspect inventory before running tasks:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-inventory -i inventory.ini --list
```

## Extra variables

Simple key-value variables:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml -e app_env=staging
```

JSON variables:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml \
  -e '{"app_env":"staging","deploy_version":"1.2.3"}'
```

Variables from a mounted file:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml -e @vars/staging.yml
```

## Limit and tags

Limit hosts:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --limit webservers
```

Run tagged tasks:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --tags deploy
```

Skip tagged tasks:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --skip-tags destructive
```

## Check mode and diff mode

Preview changes:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --check
```

Show supported file diffs:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --check --diff
```

!!! note
    Check mode depends on module support. Treat it as a safety preview, not a perfect simulation.

## Environment variables

Set Ansible variables with Docker `-e`:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e ANSIBLE_CONFIG=/ansible/ansible.cfg \
  -e ANSIBLE_HOST_KEY_CHECKING=False \
  -e ANSIBLE_FORCE_COLOR=true \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

Useful variables:

- `ANSIBLE_CONFIG=/ansible/ansible.cfg`
- `ANSIBLE_HOST_KEY_CHECKING=False`
- `ANSIBLE_FORCE_COLOR=true`
- `ANSIBLE_STDOUT_CALLBACK=yaml`
- `ANSIBLE_ROLES_PATH=/ansible/roles`
- `ANSIBLE_COLLECTIONS_PATH=/ansible/collections`

!!! warning "Host key checking"
    Disable host key checking only for disposable labs. Use a managed `known_hosts` file for production and CI.

## Project ansible.cfg

```ini
[defaults]
inventory = inventory.ini
roles_path = roles
collections_paths = collections
stdout_callback = yaml
retry_files_enabled = False
host_key_checking = True

[ssh_connection]
pipelining = True
```

Then run:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest ansible-playbook site.yml
```

## Exit codes

`ansible-playbook` returns `0` on success and non-zero on failure. This makes the same command suitable for scripts and CI:

```bash
set -euo pipefail
docker run --rm -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

## Related guides

- [SSH keys and authentication](ssh-keys-and-auth.md)
- [Ansible Vault](ansible-vault.md)
- [Docker Compose](docker-compose.md)
- [Troubleshooting](../reference/troubleshooting.md)
