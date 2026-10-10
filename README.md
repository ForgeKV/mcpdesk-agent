# MCP Desk Agent

MCP Desk Agent lets your AI reach this computer through MCP Desk — AnyDesk-style remote MCP for AI. Run the agent, get a desk code, approve connections, and choose which tools your desk exposes.

Website: https://mcpdesk.io

This repository holds release binaries only (no source code).

## Download (latest)

| Platform | File | VirusTotal |
|---|---|---|
| Windows x86_64 | [mcpdeskagent.exe](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.exe) | [scan](https://www.virustotal.com/gui/file/6fed7715184576a5042b172ea384f40681f804ae3015cce9bec2773e987eab71) |
| Linux x86_64 (static) | [mcpdeskagent-linux-x86_64](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-x86_64) | [scan](https://www.virustotal.com/gui/file/7456dd301aacba664ca8309004105407f4b717f0da77bc01098b899485208f8a) |
| Linux aarch64 (static) | [mcpdeskagent-linux-aarch64](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-aarch64) | [scan](https://www.virustotal.com/gui/file/a244af19dac40b0ed6ec77cf38f1b95495c7166a18a06cc54c730f1c4458a8cc) |
| Linux launcher + icon | [mcpdeskagent.desktop](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.desktop), [mcpdeskagent.png](https://github.com/osk999/mcpdesk-agent/releases/latest/download/mcpdeskagent.png) | |
| Checksums | [SHA256SUMS](https://github.com/osk999/mcpdesk-agent/releases/latest/download/SHA256SUMS) | |

macOS builds are not available yet. All releases: https://github.com/osk999/mcpdesk-agent/releases

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
