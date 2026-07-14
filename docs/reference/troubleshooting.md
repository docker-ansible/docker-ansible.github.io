# Troubleshooting

This page lists common Docker Ansible failures and practical fixes.

!!! tip "Reproduce locally first"
    If a CI workflow fails, try to reproduce the same command locally with
    `docker run`, the same image tag, and the same mounted project directory.

## Quick checks

Run these first:

```bash
docker run --rm willhallonline/ansible:latest ansible --version
docker run --rm willhallonline/ansible:latest ansible-lint --version
```

Then test your mounted project:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible --version
```

## Host key verification failed

Ansible is refusing to connect because the SSH host key is unknown or does not
match the known host entry.

Fix options:

```bash
-e ANSIBLE_HOST_KEY_CHECKING=False
```

or provision a `known_hosts` file before running Ansible:

```bash
ssh-keyscan example.com >> known_hosts
```

Then mount or copy the file where SSH expects it.

!!! warning "Prefer known hosts in production"
    Disabling host key checking is convenient for tests, but production
    automation should verify host identities.

## Permission denied on mounted SSH key

SSH rejects private keys that are readable by other users.

Fix the host-side permissions before mounting:

```bash
chmod 600 ./id_rsa
```

Remember that many containers run as `root` by default. Ensure the key path is
readable inside the container and that SSH uses the expected file:

```bash
ansible-playbook -i inventory site.yml --private-key /ansible/id_rsa
```

## `the input device is not a TTY`

This often happens when a local command using `-it` is copied into CI.

In CI, drop `-it`:

```bash
docker run --rm willhallonline/ansible:latest ansible --version
```

Use `-it` only for interactive local debugging sessions.

## Files are created as root on the host

The container may run as `root`, so generated files in a mounted directory can be
owned by root on the host.

Options:

```bash
docker run --rm   --user "$(id -u):$(id -g)"   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook site.yml
```

You can also use Docker user namespaces or adjust ownership after the run.

!!! note "User IDs differ by platform"
    `$(id -u):$(id -g)` works on many Linux hosts. Docker Desktop, Windows, and
    some CI runners may need platform-specific handling.

## Python interpreter discovery warnings

Ansible may warn that it discovered a Python interpreter automatically.

Set the interpreter explicitly for the target host or group:

```ini
[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

For localhost container runs, you can also set it in the play or inventory if
needed.

## DNS or proxy issues

Symptoms include package installs failing, collection downloads timing out, or
hosts not resolving.

Check:

- Docker daemon DNS configuration;
- corporate proxy variables such as `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`;
- whether the target network is reachable from inside the container;
- whether CI masks or blocks outbound connections.

Example proxy pass-through:

```bash
docker run --rm   -e HTTP_PROXY   -e HTTPS_PROXY   -e NO_PROXY   willhallonline/ansible:latest   ansible-galaxy collection list
```

## Windows paths with Docker

Path syntax differs between PowerShell, Git Bash, WSL, and Docker Desktop.

PowerShell commonly works with:

```powershell
docker run --rm -v ${PWD}:/ansible -w /ansible willhallonline/ansible:latest ansible --version
```

Git Bash may require a path such as:

```bash
docker run --rm -v //c/Users/me/project:/ansible -w /ansible willhallonline/ansible:latest ansible --version
```

If mounted files are missing, check Docker Desktop file sharing settings.

## Alpine pip builds fail with musl or compiler errors

Alpine uses musl libc. Some Python packages need compilers, headers, or glibc
compatibility that is not present by default.

Options:

- use a Debian or Ubuntu image tag;
- install Alpine build dependencies in a derived image;
- use packages with musl-compatible wheels.

Example derived image pattern:

```Dockerfile
FROM willhallonline/ansible:2.21.0-alpine-3.22
RUN apk add --no-cache build-base python3-dev
RUN pip install --no-cache-dir example-package
```

## Playbook cannot find files

When using Docker, relative paths are resolved inside the container, not on your
host shell after the container starts.

Use a working directory:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook playbooks/site.yml
```

## `localhost` tries to connect over SSH

Add `connection: local`:

```yaml
- hosts: localhost
  connection: local
  gather_facts: false
```

or configure the inventory:

```ini
localhost ansible_connection=local
```

## Image tag not found

Check the tag spelling and confirm the selected Ansible version and base OS
combination exists.

Use the image tag reference:
[`../images/tags.md`](../images/tags.md).

## Still stuck?

When reporting an issue, include:

- image tag or digest;
- host operating system;
- Docker version;
- command being run;
- minimal playbook or inventory;
- full error message with secrets removed.

See [Contributing](../about/contributing.md) for issue and PR guidance.
