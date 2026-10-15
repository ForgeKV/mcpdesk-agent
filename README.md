# MCP Desk Agent

MCP Desk Agent lets your AI reach this computer through MCP Desk — AnyDesk-style remote MCP for AI. Run the agent, get a desk code, approve connections, and choose which tools your desk exposes.

Website: https://mcpdesk.io

This repository holds release binaries only (no source code).

## Download (latest)

Latest: **v0.2.7**. All three binaries below contain the same release.

| Platform | File |
|---|---|
| Windows x86_64 | [mcpdeskagent.exe](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.exe) |
| Linux x86_64 (static) | [mcpdeskagent-linux-x86_64](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-x86_64) |
| Linux aarch64 (static) | [mcpdeskagent-linux-aarch64](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-aarch64) |
| Linux launcher + icon | [mcpdeskagent.desktop](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.desktop), [mcpdeskagent.png](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.png) |
| Checksums | [SHA256SUMS](https://github.com/osk999/mcpdesk-agent/releases/latest/download/SHA256SUMS) |

macOS builds are not available yet. All releases: https://github.com/osk999/mcpdesk-agent/releases

## In v0.2.7

- Clear terminal UI with the running version, desk ID and OTP cards, and distinct READ / PLAYBOOKS / FULL colors.
- Use F1/F2/F3 or Tab, Shift+Tab, Enter and Escape to change modes. Higher access requires local confirmation.
- Disconnect all & pause ends all MCP sessions, cancels pending calls and stops managed tasks. The pause survives restart and mirror takeover until the main window selects Resume access.
- Background task tools start long commands promptly and support status, live output, cancellation and timeouts.
- Read up to 50 files in one call, with paging, encodings, per-file errors and a combined response-size cap.

For a stopped headless/service identity, recover access with `mcpdeskagent access resume --data-dir <exact-identity-directory>`. Stop the service and close all mirrors first. Resume permits still-valid credentials to create fresh sessions under the selected mode.

## Verify

Download the files and SHA256SUMS into one folder, then:

```sh
sha256sum -c SHA256SUMS
```

On Windows (PowerShell): `Get-FileHash .\mcpdeskagent.exe -Algorithm SHA256` and compare with the line in SHA256SUMS.

## Quick start

- Windows: double-click `mcpdeskagent.exe`; it prints your desk code and OTP guidance.
- Linux: `chmod +x mcpdeskagent-linux-x86_64 && ./mcpdeskagent-linux-x86_64`
- Link the desk to your account: `mcpdeskagent claim <code>`
- Limit tools: `--allow-tools <list>` / `--deny-tools <list>`
