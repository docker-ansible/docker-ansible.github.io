# Usage guides

The `willhallonline/ansible` images provide a containerised Ansible toolchain for local development, automation, and CI. The image name is `willhallonline/ansible` and tags include `latest`, `alpine`, `ubuntu`, `2.21-alpine-3.22`, `2.19-debian-bookworm`, `2.20-ubuntu-24.04`, and `2.18-rockylinux-10`.

Each image includes Ansible components and supporting runtime tools:

- `ansible-core`
- the `ansible` community package
- `ansible-lint`
- Python

!!! tip "Project mount convention"
    Mount the current project at `/ansible` and run commands with `--workdir=/ansible`:

    ```bash
    docker run --rm -it \
      -v $(pwd):/ansible \
      --workdir=/ansible \
      willhallonline/ansible:latest ansible --version
    ```

## Quick shell

Open a shell inside the image:

```bash
docker run --rm -it willhallonline/ansible:latest /bin/sh
```

With the current project mounted:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  /bin/sh
```

## Canonical playbook example

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/id_rsa \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

Recommended day-to-day form:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

## Choose a tag

Use mutable tags for exploration:

- `latest`
- `alpine`
- `ubuntu`

Use pinned tags for repeatable team and CI workflows:

- `2.21-alpine-3.22`
- `2.19-debian-bookworm`
- `2.20-ubuntu-24.04`
- `2.18-rockylinux-10`

See [image tags](../images/tags.md) for tag details.

## Guides

### Running Ansible

- [Running playbooks](running-playbooks.md) — volume mounts, inventories, extra variables, tags, limits, check mode, diff mode, environment variables, and exit codes.
- [SSH keys and authentication](ssh-keys-and-auth.md) — private keys, whole `~/.ssh` mounts, SSH agent forwarding, `known_hosts`, password authentication, and become prompts.
- [Ansible Vault](ansible-vault.md) — create, edit, view, encrypt, and use Vault data from a container.

### Quality and dependencies

- [Ansible Lint](ansible-lint.md) — run `ansible-lint`, configure `.ansible-lint`, and use non-zero exit codes in CI.
- [Galaxy roles and collections](galaxy-roles-collections.md) — install `requirements.yml`, configure paths, cache dependencies, and bake dependencies into derived images.

### Team workflows

- [Docker Compose](docker-compose.md) — define a reusable `ansible` service for playbooks, linting, dependencies, Vault, and SSH.
- [Extending images](extending-images.md) — add OS packages, Python libraries, Galaxy content, and entrypoints to pinned base images.
- [Mitogen](mitogen.md) — install and configure Mitogen strategy plugins for compatible Ansible versions.

## Suggested project layout

```text
.
├── ansible.cfg
├── inventory.ini
├── site.yml
├── playbooks/
├── group_vars/
├── host_vars/
├── roles/
├── collections/
└── requirements.yml
```

Keep project configuration in the mounted directory so the same command works locally and in CI.

## Common ansible.cfg

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

## Common Docker options

- `--rm` removes the container after the command exits.
- `-it` gives interactive prompts for Vault, SSH, and become passwords.
- `-v $(pwd):/ansible` mounts the project.
- `--workdir=/ansible` makes relative paths predictable.
- `:ro` mounts secrets read-only.
- `-e ANSIBLE_CONFIG=/ansible/ansible.cfg` selects project config.
- `--pull=always` refreshes mutable tags.

!!! warning "Keep secrets out of images"
    Mount SSH keys, Vault password files, cloud credentials, and CI secrets at runtime. Do not copy them into Dockerfiles or commit them to the project.

## Related sections

- [Quick start](../getting-started/quick-start.md)
- [GitLab CI](../ci/gitlab-ci.md)
- [Troubleshooting](../reference/troubleshooting.md)
- [Security reference](../reference/security.md)
