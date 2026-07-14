# Galaxy roles and collections

Use `ansible-galaxy` inside the container to install roles and collections from Ansible Galaxy, Automation Hub, Git repositories, or local paths.

A repeatable project usually stores dependencies in `requirements.yml` and installs them into mounted `roles/` and `collections/` directories.

## requirements.yml

```yaml
roles:
  - name: geerlingguy.nginx
    version: 3.2.0
  - name: geerlingguy.docker
    version: 7.4.1
  - name: internal_role
    src: git+https://github.com/example/ansible-role-internal.git
    version: main

collections:
  - name: community.general
    version: 9.5.0
  - name: ansible.posix
    version: 1.6.2
  - name: kubernetes.core
    version: 3.2.0
```

Pin versions for CI and team reproducibility.

## Install requirements

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-galaxy install -r requirements.yml
```

Install roles explicitly:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-galaxy role install -r requirements.yml -p roles
```

Install collections into the project:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-galaxy collection install -r requirements.yml -p collections
```

Collections install under:

```text
collections/ansible_collections/<namespace>/<collection>
```

## Configure paths

```ini
[defaults]
roles_path = roles
collections_paths = collections
```

Then run playbooks normally:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest ansible-playbook -i inventory.ini site.yml
```

## Separate requirement files

Some teams prefer separate role and collection files:

```text
requirements.yml
collections.yml
```

Install both:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  /bin/sh -c 'ansible-galaxy role install -r requirements.yml -p roles && ansible-galaxy collection install -r collections.yml -p collections'
```

## Git-based roles

```yaml
roles:
  - name: app_deploy
    src: git+ssh://git@github.com/example/ansible-role-app-deploy.git
    version: v1.4.0
```

Forward SSH agent for private Git URLs:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v $SSH_AUTH_SOCK:/ssh-agent \
  -e SSH_AUTH_SOCK=/ssh-agent \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-galaxy role install -r requirements.yml -p roles
```

See [SSH keys and authentication](ssh-keys-and-auth.md).

## Cache dependencies in CI

Cache these paths when your CI platform supports it:

```text
roles/
collections/
```

Install during the job:

```bash
docker run --rm \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-galaxy collection install -r requirements.yml -p collections
```

!!! note
    If you commit dependencies, updates are explicit but the repository grows. If you cache them, CI is faster but caches must be invalidated when `requirements.yml` changes.

## Bake dependencies into an image

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

WORKDIR /ansible
COPY requirements.yml /ansible/requirements.yml
RUN ansible-galaxy role install -r requirements.yml -p /usr/share/ansible/roles \
 && ansible-galaxy collection install -r requirements.yml -p /usr/share/ansible/collections

ENV ANSIBLE_ROLES_PATH=/usr/share/ansible/roles
ENV ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
```

Build and run:

```bash
docker build -t registry.example.com/platform/ansible:2.21 .

docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  registry.example.com/platform/ansible:2.21 \
  ansible-playbook -i inventory.ini site.yml
```

## Private Galaxy servers

```ini
[galaxy]
server_list = private, galaxy

[galaxy_server.private]
url = https://automation-hub.example.com/api/galaxy/
token = ${GALAXY_TOKEN}

[galaxy_server.galaxy]
url = https://galaxy.ansible.com/
```

Pass tokens at runtime:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e GALAXY_TOKEN \
  willhallonline/ansible:latest \
  ansible-galaxy collection install -r requirements.yml -p collections
```

## Related guides

- [Ansible Lint](ansible-lint.md)
- [Docker Compose](docker-compose.md)
- [Extending images](extending-images.md)
- [CI usage](../ci/index.md)
