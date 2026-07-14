# Ansible Vault

Ansible Vault encrypts variables and files so secrets can live alongside playbooks without being stored in plaintext. The `willhallonline/ansible` image includes Ansible Vault commands.

!!! warning "Never bake Vault secrets into images"
    Mount Vault password files or inject them at runtime. Do not copy Vault passwords into Dockerfiles, derived images, or committed files.

## Create an encrypted file

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault create group_vars/production/vault.yml
```

Set an editor if needed:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e EDITOR=vi \
  willhallonline/ansible:latest \
  ansible-vault create group_vars/production/vault.yml
```

## Edit an encrypted file

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e EDITOR=vi \
  willhallonline/ansible:latest \
  ansible-vault edit group_vars/production/vault.yml
```

## View an encrypted file

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault view group_vars/production/vault.yml
```

## Encrypt an existing file

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault encrypt group_vars/production/secrets.yml
```

## Decrypt temporarily

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault decrypt group_vars/production/secrets.yml
```

Re-encrypt after editing:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault encrypt group_vars/production/secrets.yml
```

!!! tip
    Prefer `ansible-vault edit` to decrypting files to disk. It reduces the chance of leaving plaintext secrets behind.

## Run with an interactive Vault prompt

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml --ask-vault-pass
```

The prompt requires `-it`. In non-interactive CI, use a mounted password file or injected secret.

## Use a Vault password file

Create the file outside the repository:

```bash
mkdir -p ~/.ansible
chmod 700 ~/.ansible
printf '%s
' 'replace-with-your-vault-password' > ~/.ansible/vault-pass.txt
chmod 600 ~/.ansible/vault-pass.txt
```

Mount it read-only:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ansible/vault-pass.txt:/run/secrets/vault-pass.txt:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml \
  --vault-password-file /run/secrets/vault-pass.txt
```

Use the same pattern for Vault commands:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ansible/vault-pass.txt:/run/secrets/vault-pass.txt:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault view group_vars/production/vault.yml \
  --vault-password-file /run/secrets/vault-pass.txt
```

## Use ANSIBLE_VAULT_PASSWORD_FILE

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ansible/vault-pass.txt:/run/secrets/vault-pass.txt:ro \
  --workdir=/ansible \
  -e ANSIBLE_VAULT_PASSWORD_FILE=/run/secrets/vault-pass.txt \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

You can also configure it in `ansible.cfg` when every environment uses the same path:

```ini
[defaults]
vault_password_file = /run/secrets/vault-pass.txt
```

## Multiple Vault IDs

Use Vault IDs to separate environments:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ansible/dev-pass.txt:/run/secrets/dev-pass.txt:ro \
  -v ~/.ansible/prod-pass.txt:/run/secrets/prod-pass.txt:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml \
  --vault-id dev@/run/secrets/dev-pass.txt \
  --vault-id prod@/run/secrets/prod-pass.txt
```

Create a file for one Vault ID:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ansible/prod-pass.txt:/run/secrets/prod-pass.txt:ro \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-vault create group_vars/production/vault.yml \
  --vault-id prod@/run/secrets/prod-pass.txt
```

## CI considerations

Inject Vault passwords from CI secrets, write them to a short-lived file, mount that file, and prevent it from becoming an artifact:

```yaml
script:
  - mkdir -p .secrets
  - printf '%s' "$ANSIBLE_VAULT_PASSWORD" > .secrets/vault-pass.txt
  - chmod 600 .secrets/vault-pass.txt
  - |
    docker run --rm \
      -v "$PWD:/ansible" \
      -v "$PWD/.secrets/vault-pass.txt:/run/secrets/vault-pass.txt:ro" \
      --workdir=/ansible \
      willhallonline/ansible:latest \
      ansible-playbook -i inventory.ini site.yml \
      --vault-password-file /run/secrets/vault-pass.txt
```

Do not print Vault passwords in logs. Clean up secret files if your CI runner reuses workspaces.

## Related guides

- [Running playbooks](running-playbooks.md)
- [SSH keys and authentication](ssh-keys-and-auth.md)
- [GitLab CI](../ci/gitlab-ci.md)
- [Security reference](../reference/security.md)
