---
name: vpn
description: Manage the DexCare macOS VPN through the vpn CLI. Use for explicit DexCare VPN requests or connectivity to a known VPN-dependent DexCare resource.
---

# DexCare VPN Management

The user has a `vpn` CLI at `~/.local/bin/vpn` wrapping `scutil --nc` for macOS VPN management.

## Default VPN

**`techops-hub`** — Azure VPN (`com.microsoft.AzureVpnMac`). This is the default when no name is given.

## Commands

```bash
vpn list                  # list all VPN configs + status
vpn connect               # connect to techops-hub
vpn connect <name>        # connect to named VPN
vpn disconnect            # disconnect techops-hub
vpn disconnect <name>     # disconnect named VPN
vpn status                # check techops-hub status
vpn status <name>         # check named VPN status
vpn --help                # show help
```

## Typical Flows

**Connect:**
```bash
vpn connect
# polls every 2s, prints status, exits when Connected or Failed
```

**Check if down + reconnect:**
```bash
vpn status
# if output contains "Disconnected" → run vpn connect
```

**List all:**
```bash
vpn list
# shows name, connection state, enabled flag
```

## Auto-Reconnect Pattern

Use this pattern only when the failed destination is a DexCare resource known to require VPN. A generic AWS error or unrelated network timeout does not establish that condition:

1. Run `vpn status` — check if Disconnected
2. If disconnected → run `vpn connect`
3. Retry the failed operation after Connected

## Underlying Tool

`scutil --nc` — macOS System Configuration network connection manager. The `vpn` CLI is a thin wrapper; for debugging you can call scutil directly:

```bash
scutil --nc list                        # raw list
scutil --nc status "techops-hub"        # raw status
scutil --nc start "techops-hub"         # raw connect
scutil --nc stop "techops-hub"          # raw disconnect
```

## Troubleshooting

- **Stuck at Connecting >30s**: Azure VPN may need re-auth via the Microsoft Azure VPN app. Ask user to open the app and re-authenticate.
- **Command not found**: Verify `~/.local/bin` is on `$PATH`.
- **Permission denied**: Run `chmod +x ~/.local/bin/vpn`.
