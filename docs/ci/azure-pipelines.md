# Azure Pipelines

Azure Pipelines supports `willhallonline/ansible` through container jobs and through explicit `docker run` commands. Container jobs are usually simpler because every script step runs inside the Ansible image.

!!! tip "Use container jobs first"
    Prefer `container: willhallonline/ansible:2.21-alpine-3.22` unless you need to mix several containers inside one job.

## Prerequisites

- An Azure DevOps project with Pipelines enabled.
- An `azure-pipelines.yml` file.
- A hosted or self-hosted Linux agent that can run containers.
- Secure files for SSH keys, or secret variables if your key is stored as text.
- A variable group for Vault and environment settings.

Related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Security reference](../reference/security.md)

## Minimal container job

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: ubuntu-latest

container: willhallonline/ansible:2.21-alpine-3.22

steps:
  - checkout: self

  - script: |
      ansible --version
      ansible-lint
    displayName: Lint
```

## Full multi-stage pipeline

This example uses separate stages for lint, syntax check, and production deployment.

```yaml
trigger:
  branches:
    include:
      - main

pr:
  branches:
    include:
      - main

variables:
  ANSIBLE_FORCE_COLOR: "true"
  ANSIBLE_HOST_KEY_CHECKING: "False"
  ANSIBLE_COLLECTIONS_PATH: "$(Pipeline.Workspace)/.ansible/collections"

stages:
  - stage: Lint
    displayName: Lint
    jobs:
      - job: AnsibleLint
        displayName: Run ansible-lint
        pool:
          vmImage: ubuntu-latest
        container: willhallonline/ansible:2.21-alpine-3.22
        steps:
          - checkout: self

          - script: |
              ansible --version
              if [ -f requirements.yml ]; then
                ansible-galaxy collection install -r requirements.yml -p "$(Pipeline.Workspace)/.ansible/collections"
                ansible-galaxy role install -r requirements.yml -p "$(Pipeline.Workspace)/.ansible/roles" || true
              fi
              ansible-lint
            displayName: Run lint

  - stage: Syntax
    displayName: Syntax check
    dependsOn: Lint
    jobs:
      - job: SyntaxCheck
        displayName: Check playbook syntax
        pool:
          vmImage: ubuntu-latest
        container: willhallonline/ansible:2.21-alpine-3.22
        steps:
          - checkout: self

          - script: |
              if [ -f requirements.yml ]; then
                ansible-galaxy collection install -r requirements.yml -p "$(Pipeline.Workspace)/.ansible/collections"
                ansible-galaxy role install -r requirements.yml -p "$(Pipeline.Workspace)/.ansible/roles" || true
              fi
              ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
            displayName: Syntax check

  - stage: Deploy
    displayName: Deploy production
    dependsOn: Syntax
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployProduction
        displayName: Deploy production
        environment: production
        pool:
          vmImage: ubuntu-latest
        container: willhallonline/ansible:2.21-alpine-3.22
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self

                - task: DownloadSecureFile@1
                  name: ansibleSshKey
                  inputs:
                    secureFile: ansible_id_ed25519

                - script: |
                    mkdir -p ~/.ssh
                    chmod 700 ~/.ssh
                    cp "$(ansibleSshKey.secureFilePath)" ~/.ssh/id_ed25519
                    chmod 600 ~/.ssh/id_ed25519
                    ssh-keyscan -H example.com >> ~/.ssh/known_hosts
                    chmod 644 ~/.ssh/known_hosts
                  displayName: Prepare SSH

                - script: |
                    printf '%s' "$(ANSIBLE_VAULT_PASSWORD)" > .vault-password
                    chmod 600 .vault-password
                  displayName: Prepare Vault password

                - script: |
                    if [ -f requirements.yml ]; then
                      ansible-galaxy collection install -r requirements.yml -p "$(Pipeline.Workspace)/.ansible/collections"
                      ansible-galaxy role install -r requirements.yml -p "$(Pipeline.Workspace)/.ansible/roles" || true
                    fi
                    ansible-playbook -i inventories/production/hosts.yml site.yml --vault-password-file .vault-password
                  displayName: Deploy with Ansible
```

## Alternative: docker run from a script step

Use `docker run` when the job itself should not be a container job.

```yaml
steps:
  - checkout: self

  - script: |
      docker run --rm \
        -v "$(System.DefaultWorkingDirectory):/work" \
        -w /work \
        willhallonline/ansible:2.21-alpine-3.22 \
        ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
    displayName: Syntax check in docker-ansible
```

## Secrets handling

=== "Secure file SSH key"

    ```yaml
    - task: DownloadSecureFile@1
      name: ansibleSshKey
      inputs:
        secureFile: ansible_id_ed25519

    - script: |
        mkdir -p ~/.ssh
        cp "$(ansibleSshKey.secureFilePath)" ~/.ssh/id_ed25519
        chmod 600 ~/.ssh/id_ed25519
    ```

=== "Variable group Vault password"

    ```yaml
    variables:
      - group: ansible-production

    steps:
      - script: |
          printf '%s' "$(ANSIBLE_VAULT_PASSWORD)" > .vault-password
          chmod 600 .vault-password
    ```

Mark Vault variables secret in the variable group. Limit edit permissions on production variable groups.

## Caching

Azure Pipelines can cache Galaxy dependencies with `Cache@2`:

```yaml
- task: Cache@2
  inputs:
    key: 'ansible | "$(Agent.OS)" | requirements.yml'
    path: $(Pipeline.Workspace)/.ansible/collections
  displayName: Cache Ansible collections
```

Add the cache step before `ansible-galaxy collection install`.

## Tips

- Use deployment jobs and environments for approval gates.
- Keep secure files scoped to the pipeline that needs them.
- Prefer variable groups for shared non-file secrets.
- Pin exact image tags in every container job.
- Use `docker run` only when container jobs do not fit your agent setup.
- Keep branch conditions on deployment stages, not only on individual steps.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Container job cannot start | Confirm the selected agent supports Docker and Linux containers. |
| Secure file path is empty | Ensure the `DownloadSecureFile@1` task name matches the variable reference. |
| Secret appears as `***` in command | That is expected masking; write it to a file without printing it. |
| Deployment skipped | Check the `Build.SourceBranch` condition. |
| Docker volume path fails | Use `$(System.DefaultWorkingDirectory)` and quote the mount path. |
