# Testing

The Docker Ansible ecosystem uses dedicated repositories and in-repository
utilities to exercise images and the GitHub Action.

This page explains how the project is tested and how you can run quick smoke
tests before relying on an image in your own automation.

## Test-related repositories

| Project | Repository | Purpose |
| --- | --- | --- |
| Image testing | [`willhallonline/docker-ansible-test`](https://github.com/willhallonline/docker-ansible-test) | Exercises the published Docker Ansible images. |
| Action testing | [`willhallonline/docker-ansible-github-action-test`](https://github.com/willhallonline/docker-ansible-github-action-test) | Exercises the Docker Ansible GitHub Action. |
| Test utilities | [`testing-utils/`](https://github.com/willhallonline/docker-ansible/tree/main/testing-utils) | Helpers kept in the core repository for image testing. |

!!! note "What these tests prove"
    The test repositories help confirm that images start, Ansible commands are
    available, and representative workflows keep working. They do not prove that
    every playbook, collection, Python dependency, or target platform will work
    in your environment.

## What is exercised

The ecosystem tests focus on practical behaviours:

- the image can be pulled and started;
- `ansible` is installed;
- `ansible-playbook` is available;
- `ansible-lint` is installed;
- supported Ansible and base-OS combinations build successfully;
- the GitHub Action can invoke the Docker-based runtime;
- examples continue to represent realistic usage.

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
docker run --rm willhallonline/ansible:2.21.0-alpine-3.22 ansible --version
```

Replace the tag with the Ansible-version and base-OS combination you selected.

## Test with extra dependencies

Some playbooks require collections or Python packages. Prefer testing those in a
small derived image or a controlled CI step rather than mutating a long-lived
container manually.

```Dockerfile
FROM willhallonline/ansible:2.21.0-debian-trixie
RUN pip install --no-cache-dir example-package
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
- [GitHub Action](github-action.md)
- [Quick start](../getting-started/quick-start.md)
- [Troubleshooting](../reference/troubleshooting.md)
