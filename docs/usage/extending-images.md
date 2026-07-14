# Extending images

Create a derived image when automation needs extra operating-system packages, Python libraries, Galaxy collections, roles, or wrapper scripts. Pin the base tag so builds are reproducible.

This guide uses:

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22
```

See [image tags](../images/tags.md) for available variants.

!!! warning "Do not bake secrets"
    Do not copy SSH keys, Vault passwords, cloud credentials, or private tokens into Dockerfiles. Inject secrets at runtime with mounts or CI secrets.

## Add OS packages

=== "Alpine"

    ```dockerfile
    FROM willhallonline/ansible:2.21-alpine-3.22

    USER root
    RUN apk add --no-cache \
          git \
          openssh-client \
          rsync \
          curl \
          jq

    WORKDIR /ansible
    ```

=== "Debian or Ubuntu"

    ```dockerfile
    FROM willhallonline/ansible:2.20-ubuntu-24.04

    USER root
    RUN apt-get update \
     && apt-get install -y --no-install-recommends \
          git \
          openssh-client \
          rsync \
          curl \
          jq \
     && rm -rf /var/lib/apt/lists/*

    WORKDIR /ansible
    ```

=== "Rocky Linux"

    ```dockerfile
    FROM willhallonline/ansible:2.18-rockylinux-10

    USER root
    RUN dnf install -y \
          git \
          openssh-clients \
          rsync \
          curl \
          jq \
     && dnf clean all

    WORKDIR /ansible
    ```

Build:

```bash
docker build -t registry.example.com/platform/ansible:2.21-alpine .
```

## Add Python libraries

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

RUN pip install --no-cache-dir \
      boto3 \
      botocore \
      netaddr \
      pywinrm \
      kubernetes

WORKDIR /ansible
```

Common control-node libraries:

- `boto3` and `botocore` for AWS
- `netaddr` for IP address filters
- `pywinrm` for Windows hosts
- `kubernetes` for Kubernetes modules
- `requests` for HTTP APIs

## Install Galaxy collections

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

WORKDIR /build
COPY requirements.yml requirements.yml
RUN ansible-galaxy collection install \
      -r requirements.yml \
      -p /usr/share/ansible/collections

ENV ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
WORKDIR /ansible
```

Example `requirements.yml`:

```yaml
collections:
  - name: community.general
    version: 9.5.0
  - name: ansible.posix
    version: 1.6.2
  - name: kubernetes.core
    version: 3.2.0
```

## Install roles

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

WORKDIR /build
COPY requirements.yml requirements.yml
RUN ansible-galaxy role install \
      -r requirements.yml \
      -p /usr/share/ansible/roles

ENV ANSIBLE_ROLES_PATH=/usr/share/ansible/roles
WORKDIR /ansible
```

## Combine OS, Python, and Galaxy content

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

USER root
RUN apk add --no-cache git openssh-client rsync jq

RUN pip install --no-cache-dir boto3 netaddr pywinrm kubernetes

WORKDIR /build
COPY requirements.yml requirements.yml
RUN ansible-galaxy collection install -r requirements.yml -p /usr/share/ansible/collections

ENV ANSIBLE_COLLECTIONS_PATH=/usr/share/ansible/collections
WORKDIR /ansible
```

Run your derived image:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  registry.example.com/platform/ansible:2.21-custom \
  ansible-playbook -i inventory.ini site.yml
```

## Custom entrypoint

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

WORKDIR /ansible
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["ansible-playbook", "site.yml"]
```

Example entrypoint:

```bash
#!/bin/sh
set -e

if [ -f requirements.yml ]; then
  ansible-galaxy collection install -r requirements.yml -p collections
fi

exec "$@"
```

!!! note
    Keep entrypoints simple and visible. Hidden setup can make CI failures harder to diagnose.

## Multi-stage builds

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22 AS builder

USER root
RUN apk add --no-cache build-base python3-dev
RUN pip wheel --wheel-dir /wheels cryptography

FROM willhallonline/ansible:2.21-alpine-3.22

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* \
 && rm -rf /wheels

WORKDIR /ansible
```

Use this pattern when build tools are needed only temporarily.

## Pin and push

```bash
docker build -t registry.example.com/platform/ansible:2.21.0-20260714 .
docker push registry.example.com/platform/ansible:2.21.0-20260714
```

Use the pushed image in Compose or CI:

```yaml
services:
  ansible:
    image: registry.example.com/platform/ansible:2.21.0-20260714
    working_dir: /ansible
    volumes:
      - .:/ansible
```

## Related guides

- [Galaxy roles and collections](galaxy-roles-collections.md)
- [Docker Compose](docker-compose.md)
- [Mitogen](mitogen.md)
- [Security reference](../reference/security.md)
