# Docker Ansible Test

The Docker Ansible ecosystem uses dedicated repositories and in-repository
utilities to exercise images and the GitHub Action.

This page explains how the project is tested and how you can run quick smoke
tests before relying on an image in your own automation.

The current image-test release is `v2.7.4`. The action integration-test release
is `v1.1.0`. The current default-branch snapshot, verified on 2026-10-06, is:

| Project | `main` commit | Release/tag |
| --- | --- | --- |
| Docker Ansible | [`d4640b92cc34abfa2444ef9aa1c01769a0f0c5bc`](https://github.com/willhallonline/docker-ansible/commit/d4640b92cc34abfa2444ef9aa1c01769a0f0c5bc) | `v6.4.9` source tag; formal release `v6.4.2` |
| Docker Ansible Test | [`2c8f289ef8f59e79b58473a405b89850b6c3f2b4`](https://github.com/willhallonline/docker-ansible-test/commit/2c8f289ef8f59e79b58473a405b89850b6c3f2b4) | `v2.7.4` |
| Docker Ansible GitHub Action | [`fb244e71e224dba83fa95631cfafb42f038ba191`](https://github.com/willhallonline/docker-ansible-github-action/commit/fb244e71e224dba83fa95631cfafb42f038ba191) | `v1.1.0` |
| Docker Ansible GitHub Action Test | [`cd0eae4810fec5692d33df6e7c9c9bff35f972ec`](https://github.com/willhallonline/docker-ansible-github-action-test/commit/cd0eae4810fec5692d33df6e7c9c9bff35f972ec) | `v1.1.0` |

## Test-related repositories

| Project | Repository | Purpose |
| --- | --- | --- |
| Docker Ansible Test | [`willhallonline/docker-ansible-test`](https://github.com/willhallonline/docker-ansible-test) | Exercises the published Docker Ansible images. |
| Docker Ansible GitHub Action Test | [`willhallonline/docker-ansible-github-action-test`](https://github.com/willhallonline/docker-ansible-github-action-test) | Exercises the Docker Ansible GitHub Action. |
| Test utilities | [`testing-utils/`](https://github.com/willhallonline/docker-ansible/tree/main/testing-utils) | Helpers kept in the core repository for image testing. |

!!! note "What these tests prove"
    The image-test workflow confirms that each matrix image builds and that
    `ansible-playbook --version` runs from the pushed digest. The action-test
    workflow runs a localhost playbook and checks the action's reported exit
    code. Neither workflow is a systemd or general playbook-integration test,
    and neither proves SSH, Vault, Galaxy, extra-vars, working-directory,
    host-key-checking, deployment-host behaviour, every Python dependency, or
    every target platform.

## What is exercised

The ecosystem tests focus on practical behaviours:

- the image can be pulled and started;
- supported Ansible and base-OS combinations build successfully;
- the published image digest runs `ansible-playbook --version`; and
- the GitHub Action can invoke a localhost playbook and report its exit code.

The `docker-ansible-test` systemd-image workflow currently exercises 22 explicit
image/version combinations and emits `latest` only for
`2.21-debian-trixie`. The active matrix covers Debian Bookworm and Bookworm
Slim (2.18 and 2.19 each), Debian Trixie and Trixie Slim (2.18 through 2.21
each), Rocky Linux 10 (2.18 through 2.21), Ubuntu 24.04 (2.18 through 2.21),
and Ubuntu 26.04 (2.20 and 2.21). Alpine is intentionally excluded because
these images provide systemd, while Alpine uses OpenRC. Ubuntu 22.04 has a
repository Dockerfile but no active workflow entries. The current/retained
image-test set contains 35 tags: 22 active matrix tags, 12 retained 2.16 and
2.17 compatibility tags, and the `latest` alias. Docker Hub currently lists 59
tags in total because 24 older historical tags from Ansible 2.5 through 2.10
remain visible. Neither the retained compatibility tags nor the older
historical tags are active support.

Successful push and scheduled builds publish to both
[`willhallonline/ansible-test`](https://hub.docker.com/r/willhallonline/ansible-test)
and
[`ghcr.io/willhallonline/docker-ansible-test`](https://github.com/willhallonline/docker-ansible-test/pkgs/container/docker-ansible-test);
pull requests build without publishing. The workflow runs once weekly on
Monday at 02:00 UTC, and also supports pushes to `main` and manual dispatch.

After a published image is built, CI runs the exact GHCR image by its immutable
build digest with cgroup support, `/run` and `/run/lock` tmpfs mounts, and
`--user root`, then executes only `ansible-playbook --version`:

```bash
docker run --rm \
  --cgroupns=private \
  --user root \
  --tmpfs /run --tmpfs /run/lock \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
  ghcr.io/willhallonline/docker-ansible-test:2.21-debian-trixie@sha256:<build-digest> \
  ansible-playbook --version
```

This digest smoke test does not validate default systemd/PID 1 startup,
service-management behaviour, a localhost playbook, the default non-root
`ansible` user, or healthcheck behaviour. These systemd test images explicitly
run as `root`, so this smoke test does not represent the core image family's
default user. See the systemd usage guidance below when testing those
behaviours yourself. Current image-test builds publish
AMD64 and ARM64 except Ubuntu 24.04, which is AMD64-only; no ARMv7 variants
are built.

The action-test repository's current workflow enumerates 61 image tags: three
aliases (`latest`, `alpine`, and `ubuntu`) plus 58 versioned tags. This is
broader compatibility coverage, including retained 2.16/2.17 and Ubuntu 22.04
tags, rather than the active core image support matrix. Each job pins
`willhallonline/docker-ansible-github-action@v1.1.0`, runs a localhost playbook
smoke test, and asserts the `exit-code` output is zero. The playbook validates
Ansible/system facts, the non-root `ansible` UID/GID 1000, and a ping. It does
not exercise SSH, Vault, Galaxy, extra-vars, working-directory,
host-key-checking, linting, failure paths, or architecture variants. The
61 image-tag entries are all available for AMD64; 54 also have ARM64 manifests.
The seven AMD64-only entries are the `ubuntu` alias and the
`2.16`-through-`2.21` Ubuntu 24.04 tags. No ARMv7 variants are published.
`v1.1.0` test-repository tag predates the current fact-key fix; the current main
commit
`cd0eae4810fec5692d33df6e7c9c9bff35f972ec` passed all 61 jobs in [workflow run
#37318397873](https://github.com/willhallonline/docker-ansible-github-action-test/actions/runs/37318397873)
on 2026-10-05. The workflow also runs on pushes to `main`, pull requests, and
manual dispatch; scheduled runs start Monday at 06:00 UTC with up to 20
parallel jobs and fail-fast disabled.

## Use the systemd test images

`willhallonline/ansible-test` starts systemd as PID 1 and needs a delegated
cgroup hierarchy. Start it in the background so commands can be run with
`docker exec`; a modern cgroup v2 host normally works without `--privileged`:

```bash
docker run -d --name ansible-test \
  --cgroupns=private \
  --tmpfs /run --tmpfs /run/lock \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
  willhallonline/ansible-test:2.21-debian-trixie

docker exec -it ansible-test /bin/bash
docker rm -f ansible-test
```

For role or playbook testing, add the project mount and run the selected image:

```bash
docker run -d --name ansible-test \
  --cgroupns=private \
  --tmpfs /run --tmpfs /run/lock \
  -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
  -v "$PWD:/ansible" \
  willhallonline/ansible-test:2.21-debian-trixie

docker exec ansible-test ansible-playbook /ansible/playbook.yml
docker rm -f ansible-test
```

Prefer rootless Podman or the cgroup v2 configuration above. Use
`--privileged` only as a last resort on older CI hosts because it removes
important container isolation.

## Smoke-test an image

Start with the smallest possible command:

```bash
docker run --rm willhallonline/ansible:latest ansible --version
```

You should see Ansible version output, Python details, and configured module
search paths.

Test `ansible-lint` too:

```bash
docker run --rm willhallonline/ansible:latest ansible-lint --version
```

If both commands work, Docker can start the image and the main tools are present.

## Smoke-test a mounted project

Mount your current directory into `/ansible` and set it as the working directory:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible --version
```

This confirms that Docker volume mounting works in your shell and that the
container can read your project files.

## Run a localhost playbook

Create a small playbook in your project:

```yaml
- name: Localhost smoke test
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Show the container runtime
      debug:
        msg: "Ansible is running inside the container"
```

Run it with a one-host inline inventory:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook -i localhost, smoke.yml
```

!!! tip "Use `connection: local`"
    Without `connection: local`, Ansible may try to SSH to `localhost`. Inside a
    container that is usually not what you want for a local smoke test.

## Run a syntax check

For playbooks that should not make changes during a quick validation, run a
syntax check:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-playbook --syntax-check -i localhost, smoke.yml
```

## Run ansible-lint

If your project has Ansible content, run:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-lint
```

If you need a specific lint target:

```bash
docker run --rm   -v "$PWD:/ansible"   -w /ansible   willhallonline/ansible:latest   ansible-lint playbooks/site.yml
```

## Test a pinned tag

For CI and production, smoke-test the same tag you plan to use:

```bash
docker run --rm willhallonline/ansible:2.21.5-alpine-3.24 ansible --version
```

Replace the tag with the Ansible-version and base-OS combination you selected.

## Test with extra dependencies

Some playbooks require collections or Python packages. Prefer testing those in a
small derived image or a controlled CI step rather than mutating a long-lived
container manually.

```Dockerfile
FROM willhallonline/ansible:2.21.5-debian-trixie
USER root
RUN uv pip install --system --break-system-packages --no-cache example-package
USER ansible
```

!!! warning "Keep customisations repeatable"
    If an extra package is required for automation, encode it in a Dockerfile,
    requirements file, or CI step. Avoid undocumented manual container changes.

## Troubleshooting failed smoke tests

| Symptom | Next step |
| --- | --- |
| Image cannot be pulled | Check the tag and network access to Docker Hub. |
| `ansible` not found | Confirm you are using a `willhallonline/ansible` image tag. |
| Mounted files are missing | Check the `-v "$PWD:/ansible"` path and Docker Desktop file sharing settings. |
| Localhost playbook tries SSH | Add `connection: local` to the play. |
| Native Python dependency fails on Alpine | Try a Debian or Ubuntu image, or add Alpine build dependencies. |

## Related documentation

- [Docker Ansible](docker-ansible.md)
- [Docker Ansible GitHub Action](github-action.md)
- [Quick start](../getting-started/quick-start.md)
- [Troubleshooting](../reference/troubleshooting.md)
