# Security

The Docker Ansible images are designed to make Ansible easier to run in Docker
and CI. You are still responsible for choosing safe tags, handling secrets
carefully, and limiting what the container can access.

!!! warning "Containers are not a secret boundary"
    Do not assume a container protects secrets from commands you run inside it.
    Treat playbooks, collections, roles, and shell commands as code with access
    to mounted files and environment variables.

## Pin images

For development, a floating tag can be convenient. For production and CI, pin the
image version explicitly:

```text
willhallonline/ansible:2.21.0-alpine-3.22
```

For the strongest repeatability, pin the digest:

```text
willhallonline/ansible@sha256:<digest>
```

| Pinning method | Repeatability | Notes |
| --- | --- | --- |
| `latest` | Low | Convenient, but can change under you. |
| Version/base tag | Good | Recommended default for CI. |
| Digest | Highest | Best for regulated or high-assurance environments. |

## Scan images

Use your preferred image scanner before adopting a tag.

With Trivy:

```bash
trivy image willhallonline/ansible:2.21.0-alpine-3.22
```

With Grype:

```bash
grype willhallonline/ansible:2.21.0-alpine-3.22
```

!!! note "Scanner output needs triage"
    Vulnerability scanners report packages, severities, and available fixes.
    Review whether the vulnerable package is present, reachable, fixable in the
    selected base image, and relevant to your use case.

## Keep images updated

The upstream repository uses Renovate to automate dependency updates and rebuilds
images regularly. Rebuilds help pick up base image and Python package fixes.

Do not stay on old Ansible versions unless you have a clear compatibility need.
Legacy versions may be available in `archive/`, but old Ansible and base OS
combinations can be unmaintained.

## Do not bake secrets into images

Never place these in a Dockerfile or committed derived image:

- SSH private keys;
- Ansible Vault passwords;
- cloud credentials;
- API tokens;
- inventory passwords;
- private certificates.

Pass secrets at runtime through your CI secret store, a vault system, or a local
secret-management process.

## Handle Ansible Vault passwords carefully

Prefer short-lived files or commands that are created only for the job that needs
them.

Example pattern:

```bash
docker run --rm   -v "$PWD:/ansible"   -v "$PWD/.vault-pass:/run/secrets/ansible-vault:ro"   -w /ansible   willhallonline/ansible:2.21.0-debian-trixie   ansible-playbook site.yml --vault-password-file /run/secrets/ansible-vault
```

Make sure the vault password file is not committed and is readable only by the
user or CI step that needs it.

## Use least-privilege mounts

Mount only what the playbook needs.

| Mount | Safer approach |
| --- | --- |
| Entire home directory | Mount the project directory only. |
| Writable SSH directory | Mount a single key read-only. |
| Docker socket | Avoid unless absolutely required. |
| Cloud credential directory | Prefer a short-lived token or dedicated secret file. |

Use read-only mounts where possible:

```bash
docker run --rm   -v "$PWD:/ansible:ro"   -w /ansible   willhallonline/ansible:2.21.0-alpine-3.22   ansible --version
```

If the playbook needs to write generated files, mount a specific output directory
instead of the whole project as writable.

## Avoid privileged containers

Most Ansible linting and remote automation does not need `--privileged`, host
networking, or the Docker socket.

!!! warning "Docker socket access is powerful"
    Mounting `/var/run/docker.sock` gives the container control over the Docker
    daemon and can be equivalent to host-level access. Avoid it unless the job is
    specifically intended to manage Docker.

## SSH host key verification

For production, provision `known_hosts` rather than disabling host key checking.

```bash
ssh-keyscan example.com >> known_hosts
```

Disabling checks with `ANSIBLE_HOST_KEY_CHECKING=False` is useful for isolated
tests, but it weakens protection against man-in-the-middle attacks.

## Run as a non-root user when practical

If generated files should be owned by your host user, run Docker with your UID
and GID on Linux:

```bash
docker run --rm   --user "$(id -u):$(id -g)"   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:2.21.0-debian-trixie   ansible-playbook site.yml
```

## Report vulnerabilities

Use the upstream security policy for vulnerability reports:

<https://github.com/willhallonline/docker-ansible/blob/main/SECURITY.md>

Do not open public issues containing unpatched vulnerability details, private
keys, tokens, or exploit instructions.

## Related documentation

- [FAQ](faq.md)
- [Troubleshooting](troubleshooting.md)
- [Extending images](../usage/extending-images.md)
- [GitHub Actions](../ci/github-actions.md)
