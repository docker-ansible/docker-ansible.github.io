# Docker Compose

Docker Compose makes Ansible commands shorter and more repeatable for teams. Define an `ansible` service once, then run playbooks, linting, dependency installs, and Vault commands with consistent mounts and environment variables.

## Basic service

```yaml
services:
  ansible:
    image: willhallonline/ansible:latest
    working_dir: /ansible
    volumes:
      - .:/ansible
      - ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro
    environment:
      ANSIBLE_CONFIG: /ansible/ansible.cfg
```

Run a playbook:

```bash
docker compose run --rm ansible ansible-playbook site.yml
```

Run with inventory:

```bash
docker compose run --rm ansible ansible-playbook -i inventory.ini site.yml
```

## Equivalent docker run

The service above replaces this boilerplate:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  -e ANSIBLE_CONFIG=/ansible/ansible.cfg \
  willhallonline/ansible:latest \
  ansible-playbook site.yml
```

## Pin the image

For teams and CI, prefer a pinned tag:

```yaml
services:
  ansible:
    image: willhallonline/ansible:2.21-alpine-3.22
    working_dir: /ansible
    volumes:
      - .:/ansible
      - ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro
      - ~/.ssh/known_hosts:/root/.ssh/known_hosts:ro
    environment:
      ANSIBLE_CONFIG: /ansible/ansible.cfg
      ANSIBLE_FORCE_COLOR: "true"
      ANSIBLE_HOST_KEY_CHECKING: "true"
```

!!! tip
    Use `latest` for experiments and pinned tags for repeatable automation.

## SSH agent on Linux

```yaml
services:
  ansible:
    image: willhallonline/ansible:latest
    working_dir: /ansible
    volumes:
      - .:/ansible
      - ${SSH_AUTH_SOCK}:/ssh-agent
    environment:
      SSH_AUTH_SOCK: /ssh-agent
      ANSIBLE_CONFIG: /ansible/ansible.cfg
```

Run:

```bash
ssh-add -l
docker compose run --rm ansible ansible-playbook -i inventory.ini site.yml
```

## SSH agent on macOS Docker Desktop

```yaml
services:
  ansible:
    image: willhallonline/ansible:latest
    working_dir: /ansible
    volumes:
      - .:/ansible
      - /run/host-services/ssh-auth.sock:/ssh-agent
    environment:
      SSH_AUTH_SOCK: /ssh-agent
      ANSIBLE_CONFIG: /ansible/ansible.cfg
```

Run:

```bash
docker compose run --rm ansible ssh-add -l
docker compose run --rm ansible ansible-playbook -i inventory.ini site.yml
```

## Lint profile

Use profiles for optional services:

```yaml
services:
  ansible:
    image: willhallonline/ansible:2.21-alpine-3.22
    working_dir: /ansible
    volumes:
      - .:/ansible
    environment:
      ANSIBLE_CONFIG: /ansible/ansible.cfg

  ansible-lint:
    image: willhallonline/ansible:2.21-alpine-3.22
    working_dir: /ansible
    profiles: ["lint"]
    volumes:
      - .:/ansible
    command: ansible-lint
```

Run lint:

```bash
docker compose run --rm ansible-lint
```

Or use the main service:

```bash
docker compose run --rm ansible ansible-lint
```

## Galaxy dependency service

```yaml
services:
  ansible:
    image: willhallonline/ansible:2.21-alpine-3.22
    working_dir: /ansible
    volumes:
      - .:/ansible
    environment:
      ANSIBLE_CONFIG: /ansible/ansible.cfg

  galaxy:
    image: willhallonline/ansible:2.21-alpine-3.22
    working_dir: /ansible
    profiles: ["deps"]
    volumes:
      - .:/ansible
    command: >
      /bin/sh -c "ansible-galaxy role install -r requirements.yml -p roles &&
      ansible-galaxy collection install -r requirements.yml -p collections"
```

Run:

```bash
docker compose run --rm galaxy
```

## Vault password files

```yaml
services:
  ansible:
    image: willhallonline/ansible:latest
    working_dir: /ansible
    volumes:
      - .:/ansible
      - ~/.ansible/vault-pass.txt:/run/secrets/vault-pass.txt:ro
    environment:
      ANSIBLE_VAULT_PASSWORD_FILE: /run/secrets/vault-pass.txt
```

Run:

```bash
docker compose run --rm ansible ansible-playbook -i inventory.ini site.yml
```

!!! warning
    Do not commit Vault password files or place them in a Docker build context.

## A repeatable team command set

```bash
docker compose run --rm ansible ansible --version
docker compose run --rm galaxy
docker compose run --rm ansible-lint
docker compose run --rm ansible ansible-playbook -i inventory.ini site.yml --check --diff
docker compose run --rm ansible ansible-playbook -i inventory.ini site.yml
```

Document those commands in your project README so contributors do not need local Ansible installs.

## Compose with a derived image

```yaml
services:
  ansible:
    image: registry.example.com/platform/ansible:2.21.0-20260714
    working_dir: /ansible
    volumes:
      - .:/ansible
      - ~/.ssh:/root/.ssh:ro
    environment:
      ANSIBLE_CONFIG: /ansible/ansible.cfg
```

This is useful when your project needs extra Python libraries or Galaxy dependencies.

## Related guides

- [Running playbooks](running-playbooks.md)
- [SSH keys and authentication](ssh-keys-and-auth.md)
- [Ansible Vault](ansible-vault.md)
- [Ansible Lint](ansible-lint.md)
