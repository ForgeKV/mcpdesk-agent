# MCP Desk Agent

MCP Desk Agent lets your AI reach this computer through MCP Desk — AnyDesk-style remote MCP for AI. Run the agent, get a desk code, approve connections, and choose which tools your desk exposes.

Website: https://mcpdesk.io

This repository holds release binaries only (no source code).

## Download (latest)

Latest: **v0.2.10**. All three binaries below contain the same release.

| Platform | File |
|---|---|
| Windows x86_64 | [mcpdeskagent.exe](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.exe) |
| Linux x86_64 (static) | [mcpdeskagent-linux-x86_64](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-x86_64) |
| Linux aarch64 (static) | [mcpdeskagent-linux-aarch64](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-aarch64) |
| Linux launcher + icon | [mcpdeskagent.desktop](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.desktop), [mcpdeskagent.png](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.png) |
| Checksums | [SHA256SUMS](https://github.com/osk999/mcpdesk-agent/releases/latest/download/SHA256SUMS) |

macOS builds are not available yet. All releases: https://github.com/osk999/mcpdesk-agent/releases

## In v0.2.10

- The agent prints one ready line for your AI wherever it shows the desk code: `Tell your AI: connect device 123456789 code 000000` (example values). `status` and `status --json` include it too.
- A second launch with no terminal now prints the running agent's details and exits 5 (or 0 with `--exit-if-running`) instead of hanging as a mirror. This also applies when the running agent belongs to another OS user or a service. In a terminal you still get the read-only mirror.
- `MCPDESK_LOCAL_ONLY`, `MCPDESK_EXIT_IF_RUNNING` and `MCPDESK_INSTALLED` accept `1/0/true/false/yes/no/on/off`.
- Names and labels in `status --json` and the mirror are cleaned of invisible characters.
- Known caveats: the Windows second-launch check is only cross-compiled so far; macOS is not built; Windows binaries are unsigned.

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
