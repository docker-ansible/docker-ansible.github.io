# Quick start

This quick start gets you from Docker to a containerized Ansible command. You will
run the `willhallonline/ansible` image, mount your working directory, and execute a
playbook without installing Ansible on the host.

The examples use the `latest` tag for readability. At the time documented here,
`latest` points to **Ansible 2.21 on Alpine 3.22**.

!!! tip "Use exact tags once the command works"
    `latest` is convenient while learning. For CI/CD and shared project docs, pin an
    exact tag such as `2.21-alpine-3.22` or `2.21-debian-trixie-slim`.

## Prerequisites

You need:

- Docker installed and able to run containers
- an Ansible project, inventory, or playbook directory
- an SSH key if your playbook connects to remote hosts over SSH

You do **not** need to install Python, `ansible-core`, the `ansible` community
package, or `ansible-lint` on the host.

## 1. Start an interactive shell

Run the image and open a shell:

```bash
docker run --rm -it willhallonline/ansible:latest /bin/sh
```

Inside the container, you can run Ansible commands provided by the image.

```bash
ansible --version
ansible-playbook --version
ansible-lint --version
```

Exit the shell when finished:

```bash
exit
```

The `--rm` flag removes the container when it exits, keeping your machine clean.

## 2. Mount your Ansible project

From your Ansible project directory, mount the current directory into the container:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/id_rsa \
  willhallonline/ansible:latest \
  /bin/sh
```

This command does three important things:

| Option | Purpose |
| --- | --- |
| `--rm` | Remove the container after it exits |
| `-it` | Run interactively with a terminal |
| `-v $(pwd):/ansible` | Mount the current project at `/ansible` |
| `-v ~/.ssh/id_rsa:/root/id_rsa` | Mount an SSH private key inside the container |

!!! warning "Protect private keys"
    Mount only the key you need. Avoid copying private keys into images or committing
    them to a repository.

Inside the container, change to the mounted project if needed:

```bash
cd /ansible
ls
```

## 3. Run a playbook directly

You can run `ansible-playbook` directly without opening an interactive shell:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/id_rsa \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

This is the canonical pattern for one-off playbook execution. It works well in local
scripts and CI/CD jobs because the command exits with the status of `ansible-playbook`.

## 4. Use a working directory

For repeated use, setting the container working directory avoids needing to `cd` into
the mounted project.

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

Notice that this example mounts the key at `/root/.ssh/id_rsa`, which matches the
alias examples in [shell aliases](shell-aliases.md).

## Common first commands

=== "Check Ansible"

    ```bash
    docker run --rm -it willhallonline/ansible:latest ansible --version
    ```

=== "Run a playbook"

    ```bash
    docker run --rm -it \
      -v $(pwd):/ansible \
      -v ~/.ssh/id_rsa:/root/id_rsa \
      willhallonline/ansible:latest \
      ansible-playbook playbook.yml
    ```

=== "Lint a project"

    ```bash
    docker run --rm -it \
      -v $(pwd):/ansible \
      --workdir=/ansible \
      willhallonline/ansible:latest \
      ansible-lint
    ```

=== "Open a project shell"

    ```bash
    docker run --rm -it \
      -v $(pwd):/ansible \
      -v ~/.ssh/id_rsa:/root/.ssh/id_rsa \
      --workdir=/ansible \
      willhallonline/ansible:latest \
      /bin/sh
    ```

## Example project layout

The image does not require a special layout. A common structure is:

```text
.
├── ansible.cfg
├── inventory.yml
├── playbook.yml
├── group_vars/
├── host_vars/
├── roles/
└── collections/
```

When you run `-v $(pwd):/ansible --workdir=/ansible`, files in the current directory
are available to Ansible inside the container.

## Selecting a tag

The full tag format is:

```text
<ansible-version>-<os>
```

Examples:

```text
2.21-alpine-3.22
2.19-debian-bookworm
2.20-ubuntu-24.04
2.18-rockylinux-10
2.19-debian-bookworm-slim
2.21-debian-trixie
2.21-debian-trixie-slim
```

Use [choosing an image](choosing-an-image.md) for a practical decision guide, or go
directly to the [tag reference](../images/tags.md).

## Current version choices

Current Ansible core versions in the containers are:

- 2.16.14
- 2.17.14
- 2.18.9
- 2.19.2
- 2.20.0
- 2.21.0

Older versions 2.9 through 2.15 exist but are unmaintained. Prefer a current version
for new automation.

## Troubleshooting quick checks

### Docker cannot find the image

Confirm the image name and tag:

```bash
docker pull willhallonline/ansible:latest
```

The Docker Hub repository is
[willhallonline/ansible](https://hub.docker.com/r/willhallonline/ansible).

### The playbook cannot see local files

Make sure you run the command from the project directory and mount it:

```bash
-v $(pwd):/ansible
```

If your command uses relative paths, add:

```bash
--workdir=/ansible
```

### SSH authentication fails

Check that the private key exists on the host and is mounted where your Ansible
configuration expects it. See [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
for a deeper guide.

### The container behaves differently from the host

That is expected when moving from a host installation to a containerized control
environment. Compare the base image family and installed tooling in
[what's inside](../images/whats-inside.md), then check
[troubleshooting](../reference/troubleshooting.md).

## Next steps

- Add the recommended [shell aliases](shell-aliases.md)
- Learn how to [choose an image](choosing-an-image.md)
- Read the guide to [running playbooks](../usage/running-playbooks.md)
- Review [ansible-lint usage](../usage/ansible-lint.md)
- Bring the workflow to [CI/CD](../ci/index.md)

