# Jenkins

Jenkins can run `willhallonline/ansible` with Declarative Pipeline Docker agents or with scripted `docker.image().inside` blocks. Both approaches keep Ansible off the Jenkins node and inside a pinned container image.

!!! tip "Declarative first"
    Use `agent { docker { image 'willhallonline/ansible:2.21-alpine-3.22' } }` for straightforward pipelines.

!!! note "Use workspace paths for generated files"
    The Docker Pipeline plugin may run containers as the Jenkins host UID and GID. That UID may not have a passwd entry or home directory inside the image, so avoid `~/.ssh`; write keys, Vault files, and Ansible temporary files under `$WORKSPACE` instead.

## Prerequisites

- Jenkins with Pipeline support.
- Docker available on the agent that runs the job.
- The Docker Pipeline plugin for `agent docker` and `docker.image().inside` usage.
- Credentials Binding plugin for SSH keys and Vault passwords.
- A Jenkinsfile in the repository.

Related pages:

- [Image tags](../images/tags.md)
- [SSH keys and authentication](../usage/ssh-keys-and-auth.md)
- [Ansible Vault](../usage/ansible-vault.md)
- [Ansible lint](../usage/ansible-lint.md)

## Minimal Declarative Pipeline

```groovy
pipeline {
  agent {
    docker {
      image 'willhallonline/ansible:2.21-alpine-3.22'
      reuseNode true
    }
  }

  stages {
    stage('Lint') {
      steps {
        sh 'ansible --version'
        sh 'ansible-lint'
      }
    }
  }
}
```

## Full Declarative Pipeline

This Jenkinsfile runs lint, syntax check, and a main-branch production deployment.

```groovy
pipeline {
  agent none

  environment {
    ANSIBLE_FORCE_COLOR = 'true'
    ANSIBLE_HOST_KEY_CHECKING = 'False'
  }

  stages {
    stage('Lint') {
      agent {
        docker {
          image 'willhallonline/ansible:2.21-alpine-3.22'
          reuseNode true
        }
      }
      steps {
        checkout scm
        sh '''
          ansible --version
          if [ -f requirements.yml ]; then
            ansible-galaxy collection install -r requirements.yml
            ansible-galaxy role install -r requirements.yml || true
          fi
          ansible-lint
        '''
      }
    }

    stage('Syntax check') {
      agent {
        docker {
          image 'willhallonline/ansible:2.21-alpine-3.22'
          reuseNode true
        }
      }
      steps {
        checkout scm
        sh '''
          if [ -f requirements.yml ]; then
            ansible-galaxy collection install -r requirements.yml
            ansible-galaxy role install -r requirements.yml || true
          fi
          ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check
        '''
      }
    }

    stage('Deploy production') {
      when {
        branch 'main'
      }
      agent {
        docker {
          image 'willhallonline/ansible:2.21-alpine-3.22'
          reuseNode true
        }
      }
      steps {
        checkout scm
        withCredentials([
          sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEY_FILE', usernameVariable: 'SSH_USER'),
          string(credentialsId: 'ansible-vault-password', variable: 'ANSIBLE_VAULT_PASSWORD')
        ]) {
          sh '''
            export HOME="$WORKSPACE"
            export ANSIBLE_LOCAL_TEMP="$WORKSPACE/.ansible/tmp"
            export ANSIBLE_REMOTE_TEMP="$WORKSPACE/.ansible/remote-tmp"

            mkdir -p "$WORKSPACE/.ssh" "$ANSIBLE_LOCAL_TEMP" "$ANSIBLE_REMOTE_TEMP"
            chmod 700 "$WORKSPACE/.ssh"
            cp "$SSH_KEY_FILE" "$WORKSPACE/.ssh/id_ed25519"
            chmod 600 "$WORKSPACE/.ssh/id_ed25519"
            ssh-keyscan -H example.com >> "$WORKSPACE/.ssh/known_hosts"
            chmod 644 "$WORKSPACE/.ssh/known_hosts"

            printf '%s' "$ANSIBLE_VAULT_PASSWORD" > "$WORKSPACE/.vault-password"
            chmod 600 "$WORKSPACE/.vault-password"

            if [ -f requirements.yml ]; then
              ansible-galaxy collection install -r requirements.yml
              ansible-galaxy role install -r requirements.yml || true
            fi

            ansible-playbook \
              -i inventories/production/hosts.yml \
              site.yml \
              --user "$SSH_USER" \
              --private-key "$WORKSPACE/.ssh/id_ed25519" \
              --vault-password-file "$WORKSPACE/.vault-password"
          '''
        }
      }
    }
  }

  post {
    always {
      cleanWs(deleteDirs: true, disableDeferredWipeout: true)
    }
  }
}
```

## Scripted Pipeline example

```groovy
node('docker') {
  checkout scm

  docker.image('willhallonline/ansible:2.21-alpine-3.22').inside {
    stage('Lint') {
      sh 'ansible --version'
      sh 'ansible-lint'
    }

    stage('Syntax check') {
      sh 'ansible-playbook -i inventories/staging/hosts.yml site.yml --syntax-check'
    }
  }
}
```

## Scripted deploy with credentials

```groovy
node('docker') {
  checkout scm

  docker.image('willhallonline/ansible:2.21-alpine-3.22').inside {
    withCredentials([
      sshUserPrivateKey(credentialsId: 'ansible-ssh-key', keyFileVariable: 'SSH_KEY_FILE'),
      string(credentialsId: 'ansible-vault-password', variable: 'ANSIBLE_VAULT_PASSWORD')
    ]) {
      sh '''
        export HOME="$WORKSPACE"
        export ANSIBLE_LOCAL_TEMP="$WORKSPACE/.ansible/tmp"
        export ANSIBLE_REMOTE_TEMP="$WORKSPACE/.ansible/remote-tmp"

        mkdir -p "$WORKSPACE/.ssh" "$ANSIBLE_LOCAL_TEMP" "$ANSIBLE_REMOTE_TEMP"
        chmod 700 "$WORKSPACE/.ssh"
        cp "$SSH_KEY_FILE" "$WORKSPACE/.ssh/id_ed25519"
        chmod 600 "$WORKSPACE/.ssh/id_ed25519"
        printf '%s' "$ANSIBLE_VAULT_PASSWORD" > "$WORKSPACE/.vault-password"
        chmod 600 "$WORKSPACE/.vault-password"
        ansible-playbook \
          -i inventories/production/hosts.yml \
          site.yml \
          --private-key "$WORKSPACE/.ssh/id_ed25519" \
          --vault-password-file "$WORKSPACE/.vault-password"
      '''
    }
  }
}
```

## Secrets handling

=== "SSH private key credential"

    Use an **SSH Username with private key** credential and bind it with `sshUserPrivateKey`.

    ```groovy
    sshUserPrivateKey(
      credentialsId: 'ansible-ssh-key',
      keyFileVariable: 'SSH_KEY_FILE',
      usernameVariable: 'SSH_USER'
    )
    ```

=== "Vault password credential"

    Use a **Secret text** credential and bind it with `string`.

    ```groovy
    string(credentialsId: 'ansible-vault-password', variable: 'ANSIBLE_VAULT_PASSWORD')
    ```

## Caching

Jenkins caching depends on your node strategy. For reproducibility, install Galaxy dependencies during each run. If you cache, mount a controlled workspace directory into the container and key it by `requirements.yml`.

```groovy
docker.image('willhallonline/ansible:2.21-alpine-3.22').inside('-v $WORKSPACE/.ansible-cache:/root/.ansible') {
  sh 'ansible-galaxy collection install -r requirements.yml'
}
```

## Tips

- Keep production deployment in a separate stage with a `when` condition.
- Use Jenkins credentials, not plain environment variables in job configuration.
- Use `reuseNode true` if you need the same workspace inside Docker agent stages.
- Clean workspaces after jobs that write secret files.
- Pin the image tag in every `docker` agent and `docker.image()` call.
- Add `input` before production if human approval is required.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `docker: not found` | The Jenkins agent needs Docker or a compatible container runtime. |
| Workspace missing in container | Use `reuseNode true` or call `checkout scm` inside the stage. |
| SSH key permission error | Copy the credential file and `chmod 600` the copy. |
| Vault secret leaked in logs | Do not run shell with `set -x`; rely on Jenkins masking. |
| Deploy stage skipped | Confirm the multibranch branch name is exactly `main`. |
