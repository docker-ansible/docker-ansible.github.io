# Shell aliases

Shell aliases make the Docker Ansible workflow feel like a local command while still
running Ansible inside the `willhallonline/ansible` container.

This page shows two useful aliases:

- `docker-ansible-cli` for opening an interactive shell in the container
- `docker-ansible-cmd` for running Ansible commands directly

Add them to `~/.bashrc` or `~/.zshrc`, then reload your shell.

!!! note "What the aliases do"
    Both aliases mount the current directory at `/ansible`, mount an SSH private key
    at `/root/.ssh/id_rsa`, set `/ansible` as the working directory, and use the
    `willhallonline/ansible:latest` image.

## Aliases to copy

=== "Bash"

    Add this to `~/.bashrc`:

    ```bash
    alias docker-ansible-cli='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:latest /bin/sh'
    alias docker-ansible-cmd='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:latest '
    ```

    Reload your shell configuration:

    ```bash
    source ~/.bashrc
    ```

=== "Zsh"

    Add this to `~/.zshrc`:

    ```zsh
    alias docker-ansible-cli='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:latest /bin/sh'
    alias docker-ansible-cmd='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:latest '
    ```

    Reload your shell configuration:

    ```zsh
    source ~/.zshrc
    ```

## Open a container shell

From an Ansible project directory, run:

```bash
docker-ansible-cli
```

You will be placed inside the container with your current directory mounted at
`/ansible` and used as the working directory.

Inside the shell, run normal Ansible commands:

```bash
ansible --version
ansible-inventory --list
ansible-playbook playbook.yml
ansible-lint
```

Exit when finished:

```bash
exit
```

## Run a command directly

Use `docker-ansible-cmd` before the command you want to run:

```bash
docker-ansible-cmd ansible --version
```

Run a playbook:

```bash
docker-ansible-cmd ansible-playbook playbook.yml
```

Run `ansible-lint`:

```bash
docker-ansible-cmd ansible-lint
```

Because the alias ends with the image name and a trailing space, the command you type
after it becomes the command executed in the container.

!!! tip "Keep aliases project-neutral"
    These aliases use `$(pwd)`, so they operate on whichever project directory you are
    currently in. That makes the same aliases reusable across multiple Ansible repos.

## What each option means

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa \
  --workdir=/ansible \
  willhallonline/ansible:latest
```

| Option | Meaning |
| --- | --- |
| `docker run` | Start a new container from an image |
| `--rm` | Remove the container when it exits |
| `-it` | Allocate an interactive terminal |
| `-v $(pwd):/ansible` | Mount the current directory into the container |
| `-v ~/.ssh/id_rsa:/root/.ssh/id_rsa` | Mount the host SSH key for use by Ansible |
| `--workdir=/ansible` | Start in the mounted project directory |
| `willhallonline/ansible:latest` | Use the Docker Ansible image |

## Pinning an image in aliases

The canonical aliases use `latest`, which currently points to Ansible 2.21 on Alpine
3.22. For long-lived team workflows, consider pinning an exact tag:

```bash
alias docker-ansible-cli='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:2.21-alpine-3.22 /bin/sh'
alias docker-ansible-cmd='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_rsa:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:2.21-alpine-3.22 '
```

Choose a tag with [choosing an image](choosing-an-image.md) or review the full
[tag reference](../images/tags.md).

## Using a different SSH key

If your key is not `~/.ssh/id_rsa`, change the host side of the mount.

For example, if your key is `~/.ssh/id_ed25519`:

```bash
alias docker-ansible-cli='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_ed25519:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:latest /bin/sh'
alias docker-ansible-cmd='docker run --rm -it -v $(pwd):/ansible -v ~/.ssh/id_ed25519:/root/.ssh/id_rsa --workdir=/ansible willhallonline/ansible:latest '
```

This keeps the path inside the container stable while using a different host key.

!!! warning "Do not bake keys into images"
    Mount keys at runtime. Do not add private SSH keys to custom images, Dockerfiles,
    repositories, or CI logs.

## Working with inventories and playbooks

Because the alias sets `/ansible` as the working directory, relative paths work from
the root of your mounted project.

```bash
docker-ansible-cmd ansible-inventory -i inventory.yml --list
docker-ansible-cmd ansible-playbook -i inventory.yml playbook.yml
docker-ansible-cmd ansible-playbook -i inventories/prod.yml site.yml
```

If your project uses `ansible.cfg`, keep it in the mounted project directory so
Ansible can discover it when the container starts in `/ansible`.

## Working with ansible-lint

Run linting from the project root:

```bash
docker-ansible-cmd ansible-lint
```

Or lint a specific playbook:

```bash
docker-ansible-cmd ansible-lint playbook.yml
```

See [ansible-lint usage](../usage/ansible-lint.md) for more examples.

## Aliases versus scripts

Aliases are best for interactive use. For shared automation, a small script or CI job
may be clearer because it can pin the tag and document every option explicitly.

Use aliases when:

- you run Ansible manually from multiple project directories
- you want short commands for local testing
- each developer can customize their local SSH key path

Use scripts or CI configuration when:

- the command is part of a release process
- the image tag must be reviewed with code changes
- the project needs consistent options for every contributor

## Troubleshooting aliases

### The alias command is not found

Reload your shell file:

```bash
source ~/.bashrc
```

or:

```zsh
source ~/.zshrc
```

Then check:

```bash
alias docker-ansible-cli
alias docker-ansible-cmd
```

### The container cannot see my playbook

Make sure you are in the project directory before running the alias. The alias mounts
`$(pwd)`, so it uses your current directory at the time the command runs.

```bash
pwd
ls
docker-ansible-cmd ls
```

### SSH authentication fails

Confirm that the key path in the alias exists on the host:

```bash
ls -l ~/.ssh/id_rsa
```

If you use a different key, update the `-v` mount in the alias. For more detail, see
[SSH keys and authentication](../usage/ssh-keys-and-auth.md).

### I want a different image family

Replace `willhallonline/ansible:latest` with the tag you want:

```bash
willhallonline/ansible:2.21-debian-trixie-slim
```

See [choosing an image](choosing-an-image.md) for guidance.

## Next steps

- Run the [quick start](quick-start.md)
- Choose a pinned tag with [choosing an image](choosing-an-image.md)
- Learn more about [running playbooks](../usage/running-playbooks.md)
- Review [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- Bring the same workflow to [CI/CD](../ci/index.md)

