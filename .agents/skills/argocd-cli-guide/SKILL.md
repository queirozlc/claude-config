---
name: argocd-cli-guide
description: Use when managing, inspecting, syncing, or troubleshooting Kubernetes applications via the argocd CLI, including checking app health, running diffs, syncing deployments, viewing logs, or switching between ArgoCD server contexts
---

# ArgoCD CLI Guide

You are an expert Kubernetes operator. Use these command patterns when interacting with the `argocd` CLI.

## 0. Context Management

With multiple ArgoCD servers, switch context before any command. Tokens are bound to the server in the current context, so a stale context gives auth errors.

```bash
# List all configured contexts (shows current context with *)
argocd context

# Switch context before operating on a different server
argocd context <SERVER_ADDRESS>

# Or use per-command flags (no context switch needed)
argocd app get <APP> --argocd-context <SERVER_ADDRESS>
argocd app get <APP> --server <SERVER_ADDRESS>
```

**Multi-server pattern:**
```bash
argocd context argocd.example.com
argocd app sync argocd/my-app
argocd context argocd.other.com
argocd app sync argocd/other-app
```

**Login:**
```bash
argocd login <SERVER_ADDRESS> --grpc-web --sso --skip-test-tls
```

Always pass `--skip-test-tls` on a first login. Without it, the login can hang on the TLS probe. It then fails with `gRPC connection not ready: context deadline exceeded` (exit 20), before the browser opens. The server can still answer `curl https://<SERVER>/api/version` and `argocd version --server <SERVER> --grpc-web`.

SSO runs in the background: run the login with `run_in_background`, then wait for the callback listener (`lsof -iTCP:8085 -sTCP:LISTEN`). When it listens, the output says "Opening system default browser for authentication". Tell the user to finish the login in the browser.

DexCare servers are on the techops-hub VPN. Each customer can have its own server, for example `argo-cd.urmc-uat-use2-01.dexcare.engineering`. `spi-uat` is the SPI tenant only.

Per-server settings like `grpc-web` can be persisted in `~/.config/argocd/config` so you don't need to pass flags every time. See [references/argocd-config.md](references/argocd-config.md) for config details.

## 1. Information Retrieval

When asked to check an application's status, **always start here**.

```bash
# High-level status (health + sync)
argocd app get <APP_NAME>

# JSON output for scripting
argocd app get <APP_NAME> -o json

# Show parameters and last operation details
argocd app get <APP_NAME> --show-params --show-operation

# Get a specific resource's live manifest
argocd app get-resource <APP_NAME> --kind <KIND> --resource-name <NAME> -o json

# List all applications
argocd app list
```

**Application Logs:**
```bash
# All pods in the app
argocd app logs <APP_NAME>

# Stream logs in real-time
argocd app logs <APP_NAME> -f

# Last N lines
argocd app logs <APP_NAME> --tail 100

# Filter by resource kind/name/namespace
argocd app logs <APP_NAME> --kind Deployment --name <RESOURCE_NAME>
```

## 2. Safe Inspection (Diffing)

Run a diff before a manual sync, so you know what will change.

```bash
argocd app diff <APP_NAME>
```

If the diff shows unexpected massive deletions, STOP and ask the user for confirmation.

**Reading diffs:** Image-only changes can still be material releases. Verify the intended revision, environment, and authorized rollout stage before syncing.

## 3. Sync & Deployment

```bash
# Standard sync
argocd app sync <APP_NAME>

# Async sync (don't wait for completion — good for batch)
argocd app sync <APP_NAME> --async

# Dry-run (preview without applying)
argocd app sync <APP_NAME> --dry-run

# Sync specific resource only (GROUP:KIND:NAME format)
argocd app sync <APP_NAME> --resource :Service:my-service
argocd app sync <APP_NAME> --resource argoproj.io:Rollout:my-rollout
# With namespace
argocd app sync <APP_NAME> --resource argoproj.io:Rollout:my-namespace/my-rollout

# Force sync with prune (USE WITH CAUTION — only when user explicitly asks)
argocd app sync <APP_NAME> --prune --force
```

## 4. Rollback & History

```bash
# View deployment history
argocd app history <APP_NAME>

# Rollback to a specific revision
argocd app rollback <APP_NAME> <HISTORY_ID>
```

## 5. Resource Actions (Rollouts, Restarts)

```bash
# List available actions for an app
argocd app actions list <APP_NAME>

# Promote a Rollout (e.g., canary → full)
argocd app actions run <APP_NAME> promote-full --kind Rollout --resource-name <NAME>

# Restart a Deployment
argocd app actions run <APP_NAME> restart --kind Deployment --resource-name <NAME>
```

**Argo Rollouts workflow:** Inspect the application's rollout strategy and requested stage. Sync within the authorized environment and revision. Verify the reached stage. Run `promote-full` only when the requested scope and project policy call for full promotion; a sync request alone does not authorize it.

## 6. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Unauthenticated` / `token expired` | Auth token expired | `argocd relogin` or `argocd login <SERVER> --grpc-web --sso --skip-test-tls` |
| `argocd login` hangs, then `gRPC connection not ready: context deadline exceeded` | TLS probe hangs before SSO starts | Add `--skip-test-tls` |
| Perpetual diff on HPA | Metrics field ordering | Ensure HPA metrics order: memory first, cpu second (matches K8s API server return order) |
| Diff shows only image tag changes | CI/CD auto-updated image | Verify revision and authorized rollout stage before syncing |

## Best Practices

1. **Context First:** MUST `argocd context <server>` before operating on a different server.
2. **Read Before Write:** Always `app get` + `app diff` before any `app sync` or `app rollback`.
3. **GitOps Awareness:** ArgoCD reconciles from Git. Manual `kubectl` changes will be overwritten on next sync. Prefer Git commits + ArgoCD sync.
4. **Async for Batch:** Use `--async` when syncing multiple apps to avoid blocking.
5. **Targeted Sync:** Use `--resource` to sync only the changed resource instead of the entire app.
6. **Rollout Awareness:** Stop at the requested rollout stage. Do not promote beyond the authorized scope.
