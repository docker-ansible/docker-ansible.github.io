# SSH keys and authentication

Ansible usually connects to managed hosts over SSH. In a container workflow, SSH material must be mounted or forwarded into the container at runtime.

## Mount a single key

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml \
  --private-key /root/.ssh/id_rsa
```

The documented canonical pattern also works:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/id_rsa \
  willhallonline/ansible:latest \
  ansible-playbook playbook.yml
```

Prefer `:ro` for read-only key mounts.

!!! warning "Private key permissions"
    SSH may reject keys that are too open. Fix permissions on the host:

    ```bash
    chmod 600 ~/.ssh/id_rsa
    ```

## Configure keys in inventory

```ini
[web]
web-01 ansible_host=192.0.2.10

[web:vars]
ansible_user=deploy
ansible_ssh_private_key_file=/root/.ssh/id_rsa
```

Run:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

## Mount all of ~/.ssh

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh:/root/.ssh:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

This exposes `config`, `known_hosts`, and multiple keys to the container.

!!! note
    Mounting the whole directory is convenient for development, but a single-key mount has a smaller secret footprint.

## Forward ssh-agent on Linux

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v $SSH_AUTH_SOCK:/ssh-agent \
  -e SSH_AUTH_SOCK=/ssh-agent \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

Verify the agent:

```bash
docker run --rm -it \
  -v $SSH_AUTH_SOCK:/ssh-agent \
  -e SSH_AUTH_SOCK=/ssh-agent \
  willhallonline/ansible:latest ssh-add -l
```

## Forward ssh-agent on macOS

Docker Desktop exposes a host services socket:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v /run/host-services/ssh-auth.sock:/ssh-agent \
  -e SSH_AUTH_SOCK=/ssh-agent \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

This avoids mounting private key files.

## known_hosts

Generate known host entries on the host:

```bash
ssh-keyscan -H web-01.example.com >> ~/.ssh/known_hosts
```

Mount them:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  -v ~/.ssh/known_hosts:/root/.ssh/known_hosts:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

Disable checking only for disposable labs:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e ANSIBLE_HOST_KEY_CHECKING=False \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

Or in `ansible.cfg`:

```ini
[defaults]
host_key_checking = False
```

!!! warning
    Disabling host key checking can hide man-in-the-middle attacks. Prefer pinned `known_hosts` entries.

## Password authentication

If SSH password authentication is required, use an interactive prompt:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini legacy.yml --ask-pass
```

Short form:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest ansible-playbook -i inventory.ini legacy.yml -k
```

Ansible uses `sshpass` for this style of SSH password workflow. Verify the selected image variant contains what your environment requires before standardising on password auth.

Avoid plaintext passwords in inventory. Store password variables with [Ansible Vault](ansible-vault.md).

## Become passwords

Prompt for privilege escalation:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --ask-become-pass
```

Short form:

```bash
docker run --rm -it -v $(pwd):/ansible --workdir=/ansible \
  willhallonline/ansible:latest ansible-playbook -i inventory.ini site.yml -K
```

Inventory become settings:

```ini
[all:vars]
ansible_become=true
ansible_become_method=sudo
ansible_become_user=root
```

## Troubleshooting

Run with SSH verbosity:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh:/root/.ssh:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml -vvv
```

Test SSH from the same container context:

```bash
docker run --rm -it -v ~/.ssh:/root/.ssh:ro \
  willhallonline/ansible:latest ssh -v deploy@web-01.example.com
```

Check:

- `ansible_user` is correct
- the key or agent is mounted
- the key passphrase is loaded in the agent
- target hosts are reachable from Docker
- `known_hosts` contains the host key

## Related guides

- [Running playbooks](running-playbooks.md)
- [Ansible Vault](ansible-vault.md)
- [Security reference](../reference/security.md)
