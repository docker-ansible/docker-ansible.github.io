# FAQ

These questions cover common decisions and surprises when using the
`willhallonline/ansible` Docker images and related GitHub Action.

??? question "Which tag should I use?"
    Use the most specific tag that matches your required Ansible version and base
    operating system. For repeatable automation, prefer a tag shaped around an
    Ansible version and base OS instead of a floating tag.

    See the image tag reference for the exact tag list:
    [`../images/tags.md`](../images/tags.md).

??? question "Why is `latest` Alpine-based?"
    `latest` is intended to be a convenient default and has historically favoured
    Alpine because it is small and quick to pull. It is not the best choice for
    every workload.

    If you need glibc compatibility, apt packages, or easier native Python wheel
    support, choose a Debian or Ubuntu tag explicitly.

??? question "How do I run against localhost inside the container?"
    Use a local connection in the playbook:

    ```yaml
    - hosts: localhost
      connection: local
      gather_facts: false
      tasks:
        - debug:
            msg: "running locally in the container"
    ```

    Then run with an inline localhost inventory:

    ```bash
    docker run --rm       -v "$PWD:/ansible"       -w /ansible       willhallonline/ansible:latest       ansible-playbook -i localhost, playbook.yml
    ```

??? question "Where should I mount my playbooks?"
    The examples in this site use `/ansible`:

    ```bash
    docker run --rm -v "$PWD:/ansible" -w /ansible willhallonline/ansible:latest ansible --version
    ```

    `/ansible` is a convention, not a requirement. Use another path if your CI or
    local workflow needs it, but keep the working directory and relative paths
    consistent.

??? question "Is ARM or Apple Silicon supported?"
    Support depends on the published image manifest for the tag you choose and
    the upstream base images used for that tag. On Apple Silicon, Docker Desktop
    may run native ARM images when available or emulate another architecture when
    necessary.

    If architecture matters for your workflow, inspect the tag before relying on
    it in CI and consider pinning a digest.

??? question "Why do some pip packages fail on Alpine?"
    Alpine uses musl libc rather than glibc. Some Python packages with native
    extensions either need Alpine build dependencies or do not publish compatible
    wheels.

    Options include:

    - use a Debian or Ubuntu image;
    - install the required Alpine build packages in a derived image;
    - choose Python packages that publish musl-compatible wheels.

??? question "How do I add extra Python dependencies?"
    For repeatable usage, build a derived image:

    ```Dockerfile
    FROM willhallonline/ansible:2.21.0-debian-trixie
    RUN pip install --no-cache-dir netaddr jmespath
    ```

    See the guide to extending images:
    [`../usage/extending-images.md`](../usage/extending-images.md).

??? question "How often are images rebuilt?"
    The upstream repository uses Renovate for automated dependency updates and is
    rebuilt regularly as Ansible versions, base images, and dependencies change.

    Because rebuilds can refresh packages under the same moving tag, pin exact
    tags or digests for production jobs.

??? question "Are old Ansible versions available?"
    Older versions, including Ansible 2.9 through 2.15, may be present in the
    upstream `archive/` area or as historical tags. Treat those versions as
    legacy and potentially unmaintained.

    Prefer current maintained Ansible versions unless you are supporting a legacy
    estate that cannot yet move forward.

??? question "What is the difference between `ansible` and `ansible-core`?"
    `ansible-core` contains the core Ansible engine and built-in plugins.
    `ansible` is the community package that includes `ansible-core` plus a set of
    community collections.

    The images include both `ansible-core` and `ansible`, as well as
    `ansible-lint`, so common playbook and lint workflows work out of the box.

??? question "How do I pin exactly?"
    Pin at least the Ansible version and base OS, for example an
    AnsibleVersion-BaseOS style tag such as:

    ```text
    willhallonline/ansible:2.21.0-alpine-3.22
    ```

    For maximum immutability, pin the image digest:

    ```text
    willhallonline/ansible@sha256:<digest>
    ```

    Digests are the strongest way to guarantee that CI runs the same image bytes.

??? question "Can I use the images in GitHub Actions without the wrapper action?"
    Yes. You can run Docker directly in a workflow step, or you can use the
    Docker-based GitHub Action. The action is convenient when its interface fits
    your workflow; direct Docker commands are useful when you need complete
    control.

    See [`../ci/github-actions.md`](../ci/github-actions.md).

??? question "Why does Ansible try to SSH to localhost?"
    In Ansible, `localhost` can still use the default SSH connection unless you
    tell it otherwise. Add `connection: local` to the play or set the connection
    in inventory.

??? question "Can I install system packages at runtime?"
    You can, but it is usually better to build a derived image. Runtime package
    installation slows CI and can make jobs less repeatable.

    Use a derived image when dependencies are part of the automation contract.

??? question "Can I run these images on self-hosted CI?"
    Yes, as long as the runner can run Docker and pull the selected image. Pin
    tags, configure credentials safely, and avoid assuming interactive terminals
    are available.

??? question "Where do I start?"
    Start with the quick start:
    [`../getting-started/quick-start.md`](../getting-started/quick-start.md),
    then choose a specific tag in [`../images/tags.md`](../images/tags.md).
