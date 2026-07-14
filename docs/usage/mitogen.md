# Mitogen

Mitogen can accelerate some Ansible runs by replacing the default execution strategy with Mitogen's strategy plugin. It is most useful for many-host, many-task playbooks where connection setup and module transfer overhead are significant.

In a container workflow, install Mitogen in a derived image or mount it into the container, then configure `ansible.cfg` with `strategy_plugins` and `strategy = mitogen_linear`.

!!! warning "Check compatibility"
    Mitogen must support the `ansible-core` version in your selected image tag. Test with a small inventory before enabling it in CI or production.

## When Mitogen helps

Mitogen is worth testing when you have:

- many hosts
- many short tasks
- slow SSH connection setup
- high-latency links
- repeated deployment runs

It may help less when you have:

- one or two hosts
- playbooks dominated by long remote commands
- cloud API calls from the control node
- modules or plugins incompatible with your Mitogen and Ansible versions

## Install Mitogen in a derived image

```dockerfile
FROM willhallonline/ansible:2.21-alpine-3.22

RUN pip install --no-cache-dir mitogen

WORKDIR /ansible
```

Build:

```bash
docker build -t registry.example.com/platform/ansible-mitogen:2.21 .
```

Check the installed version:

```bash
docker run --rm -it registry.example.com/platform/ansible-mitogen:2.21 \
  python -c "import mitogen; print(mitogen.__version__)"
```

## Find the strategy plugin path

Use Python inside the same image:

```bash
docker run --rm -it registry.example.com/platform/ansible-mitogen:2.21 \
  python -c "import os, mitogen; print(os.path.join(os.path.dirname(mitogen.__file__), 'ansible_mitogen', 'plugins', 'strategy'))"
```

Or inspect package metadata:

```bash
docker run --rm -it registry.example.com/platform/ansible-mitogen:2.21 \
  pip show mitogen
```

Typical paths include:

```text
/usr/lib/python3.12/site-packages/ansible_mitogen/plugins/strategy
/usr/local/lib/python3.12/site-packages/ansible_mitogen/plugins/strategy
```

Use the path from your image, not a path copied from another host.

## Configure ansible.cfg

```ini
[defaults]
inventory = inventory.ini
strategy_plugins = /usr/local/lib/python3.12/site-packages/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

Run with the Mitogen image:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro \
  --workdir=/ansible \
  registry.example.com/platform/ansible-mitogen:2.21 \
  ansible-playbook -i inventory.ini site.yml
```

## Use a separate Mitogen config

Create `ansible-mitogen.cfg` when you do not want Mitogen enabled for every run:

```ini
[defaults]
inventory = inventory.ini
roles_path = roles
collections_paths = collections
strategy_plugins = /usr/local/lib/python3.12/site-packages/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

Run with `ANSIBLE_CONFIG`:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e ANSIBLE_CONFIG=/ansible/ansible-mitogen.cfg \
  registry.example.com/platform/ansible-mitogen:2.21 \
  ansible-playbook site.yml
```

## Mount Mitogen for experiments

Install Mitogen into a project-local directory on the host:

```bash
python -m pip install --target .vendor/mitogen mitogen
```

Configure Ansible:

```ini
[defaults]
strategy_plugins = /ansible/.vendor/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

Run with the standard image:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

!!! note
    A derived image is cleaner for CI. A mounted `.vendor/` directory is useful for quick compatibility tests.

## Verify Mitogen is active

Run with verbosity:

```bash
docker run --rm -it \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  registry.example.com/platform/ansible-mitogen:2.21 \
  ansible-playbook -i inventory.ini site.yml -vv
```

Look for Mitogen strategy loading or `mitogen_linear` in startup output.

## Benchmark before adopting

Normal run:

```bash
time docker run --rm \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  willhallonline/ansible:latest \
  ansible-playbook -i inventory.ini site.yml
```

Mitogen run:

```bash
time docker run --rm \
  -v $(pwd):/ansible \
  --workdir=/ansible \
  -e ANSIBLE_CONFIG=/ansible/ansible-mitogen.cfg \
  registry.example.com/platform/ansible-mitogen:2.21 \
  ansible-playbook site.yml
```

Benchmark with representative inventories. A localhost-only playbook is not a meaningful test.

## Troubleshooting

If Ansible cannot find the strategy plugin:

- rerun the Python path discovery command inside the same image
- check Python version differences between tags
- verify `ANSIBLE_CONFIG` points at the expected file
- verify the configured path exists inside the container

If failures happen only with Mitogen enabled:

- check Mitogen support for your `ansible-core` version
- run with fewer hosts and `-vvv`
- switch back to `strategy = linear` to isolate the issue
- pin a known-good Mitogen version if needed

## Related guides

- [Extending images](extending-images.md)
- [Running playbooks](running-playbooks.md)
- [Docker Compose](docker-compose.md)
- [Troubleshooting](../reference/troubleshooting.md)
