---
name: dexcare-aws
description: Access DexCare AWS accounts through the toolbox and AWS CLI. Use only for DexCare accounts, roles, or environments.
agent: true
model: sonnet
---

# DexCare AWS Access

Authenticate to a DexCare AWS account via Okta SAML using `@dexcare/toolbox`, then use the standard AWS CLI with the role-scoped profile it writes.

## Prerequisites

- macOS or Linux shell
- Node.js (any LTS) + npm on `$PATH`
- AWS CLI v2 (`aws --version`)
- Okta account with access to the target DexCare AWS role
- `sudo` for first-time `toolbox setup` (installs SAML cert to system trust store)

## One-time setup

```shell
npm i -g @dexcare/toolbox
toolbox setup          # prompts for sudo; installs SAML certs
```

`toolbox setup` is interactive (sudo password). Cannot run headless. Ask the user to run it.

## Login (per session)

```shell
toolbox login <codename>      # e.g. toolbox login dev
toolbox login -t              # list all codenames
```

Opens browser → Okta auth → toolbox writes assumed-role creds to `~/.aws/credentials`. Profile names follow `<Role>@dexcare_<codename>`, e.g.:

- `Administrator@dexcare_appdev`
- `EngineeringMaintenanceRole@dexcare_appdev`
- `EngineeringReadOnlyRole@dexcare_appdev`

Multiple roles written per login (whatever Okta grants you). Tokens are STS session creds — default ~1h TTL. Re-run `toolbox login <codename>` when they expire.

## Codename → account mapping

Codenames map to AWS accounts/environments. Common ones:

| Codename                                                        | Environment                                                   |
| --------------------------------------------------------------- | ------------------------------------------------------------- |
| `dev`                                                           | Shared Dev cluster (`dexcare_appdev`, account `577638391766`) |
| `staging`                                                       | Staging                                                       |
| `spi`                                                           | SPI Prod                                                      |
| `appdev`                                                        | Legacy alias for the Dev app account                          |
| `frosh`, `komodo`, `kirkwood`, `musc`, `thr`, `hackensack`, ... | Customer-specific accounts                                    |

Full list: `toolbox login -t`.

## Use AWS CLI

Use the highest-privilege profile available for the requested DexCare account by default, as the user prefers. Verify its identity and keep operations within the authorized task scope, then export:

```shell
export AWS_PROFILE=EngineeringMaintenanceRole@dexcare_appdev
export AWS_REGION=us-west-2

aws sts get-caller-identity          # verify
aws rds describe-db-clusters \
  --query 'DBClusters[*].[DBClusterIdentifier,Endpoint,ReaderEndpoint]' \
  --output table
```

All DexCare workloads live in `us-west-2`.

## IAM DB auth (Aurora Postgres)

Dev/prod Aurora clusters enforce `rds.force_ssl=1` and IAM auth. Generate a short-lived (15 min) token to use as the DB password:

```shell
aws rds generate-db-auth-token \
  --hostname "<cluster-endpoint>.cluster-<id>.us-west-2.rds.amazonaws.com" \
  --port 5432 \
  --username <service>_reader
```

DB user pattern: `<service>_reader | <service>_writer | <service>_master`.

`generate-db-auth-token` is client-side signing — no API mutation, safe to run.

## Verify access (non-mutating)

```shell
aws sts get-caller-identity
aws rds describe-db-clusters --query 'DBClusters[*].DBClusterIdentifier'
aws ec2 describe-regions --query 'Regions[?RegionName==`us-west-2`]'
```

## Agent operating rules

- Always set both `AWS_PROFILE` and `AWS_REGION=us-west-2` on the command (or export them once per session).
- Never guess profile names; run `grep '^\[' ~/.aws/credentials` to list available profiles.
- The user's default is the highest-privilege available role for the requested account. Do not infer authorization for extra operations from that role.
- Reuse clear user authorization for AWS mutations within the same account, role, environment, and operation scope. Do not ask again for required follow-up operations within that scope.
- Ask before a mutation that adds scope or has an unresolved destructive consequence. Preserve explicit approval boundaries and perform only operations within the task scope.
- If `aws` returns `ExpiredToken` / `InvalidClientTokenId`, the STS session expired — tell the user to re-run `toolbox login <codename>`.
- `toolbox setup` needs interactive sudo; never attempt it from a non-TTY shell. Instruct the user instead.
- Codenames like `spi-dev` in repo code (helm values, RDS endpoint `spi-dev-usw2-01-aurora-psql...`) describe the _cluster name_, not the toolbox codename. The toolbox codename for Dev is `dev`.

## Troubleshooting

| Symptom                                                     | Cause / fix                                                                                                                                                                                                                                                                   |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `The config profile (...) could not be found`               | Profile not in `~/.aws/credentials`. Run `toolbox login <codename>` or pick a profile that exists.                                                                                                                                                                            |
| `ExpiredToken` / `InvalidClientTokenId`                     | STS session expired. Re-run `toolbox login <codename>`.                                                                                                                                                                                                                       |
| `AccessDenied` on RDS/EKS                                   | Role lacks the permission. Try a higher-priv profile from the same login, or request access.                                                                                                                                                                                  |
| `toolbox setup` fails with `sudo: a password is required`   | Must run interactively in a terminal — not from a subshell without TTY.                                                                                                                                                                                                       |
| psql `FATAL: password authentication failed` with IAM token | Token older than 15 min, wrong `--username`, or wrong `--hostname`/region. Regenerate.                                                                                                                                                                                        |
| psql SSL error                                              | Need the RDS CA bundle. App Dockerfiles install it to `/etc/ssl/certs/rds-combined-ca-bundle.pem`. For local psql: `curl -o ~/rds-ca.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem` then `PGSSLMODE=verify-full PGSSLROOTCERT=~/rds-ca.pem psql ...`. |
| Connection timeout to RDS                                   | VPN/VPC reachability. Ensure DexCare VPN is connected; RDS is private.                                                                                                                                                                                                        |

## Reference

- Confluence: "Using Toolbox and AWS CLI to generate IAM based credentials for DB login" (space `DEP`, page id `20469448768`)
- Toolbox repo: <https://github.com/DexCare/common/tree/main/packages/toolbox>
- AWS CLI install: <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>
