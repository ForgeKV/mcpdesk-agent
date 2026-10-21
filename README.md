# MCP Desk Agent

MCP Desk Agent lets your AI reach this computer through MCP Desk — AnyDesk-style remote MCP for AI. Run the agent, get a desk code, approve connections, and choose which tools your desk exposes.

Website: https://mcpdesk.io

This repository holds release binaries only (no source code).

## Download (latest)

Latest: **v0.2.12**. All binaries below contain the same release.

| Platform | File |
|---|---|
| Windows x86_64 | [mcpdeskagent.exe](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent.exe) |
| Windows ARM64 | [mcpdeskagent-windows-aarch64.exe](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-windows-aarch64.exe) |
| Linux x86_64 (static) | [mcpdeskagent-linux-x86_64](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-x86_64) |
| Linux aarch64 (static) | [mcpdeskagent-linux-aarch64](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-aarch64) |
| Linux launcher + icon | [mcpdeskagent.desktop](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent.desktop), [mcpdeskagent.png](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent.png) |
| Checksums | [SHA256SUMS](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/SHA256SUMS) |

macOS builds are not available yet. All releases: https://github.com/ForgeKV/mcpdesk-agent/releases

## In v0.2.12

- **Files without tokens.** In end-to-end mode the bridge adds `push_file` (this machine → desk), `pull_file` (desk → this machine) and `transfer_status`. The file streams inside the encrypted session as raw chunks: no base64, and nothing passes through the AI conversation, so a multi-GB copy costs the model one receipt line (size, sha256, time). Measured through the production relay: 100 MB in 6 s (16 MB/s), a 749 MB ISO in 41 s up / 46 s down, hashes identical on both ends. Receiving on the desk needs full access; `--allowed-root` and the tool allow/deny lists apply; every transfer is in the desk's audit log. Half-received files are removed if a transfer or its session ends early. Details: https://mcpdesk.io/security/end-to-end#files
- **Default access mode is now `full`** (was `readonly`). Pass `--mode readonly` (or `SERVERMCP_MODE=readonly`) to keep the old default. Access still needs the desk code, the current one-time code and (for invites) Approve on the desk.
- Fix: a desk no longer drops an end-to-end handshake in progress while flushing results for another session.
## In v0.2.11

- **End-to-end encrypted sessions** with local AI clients (Claude Code, Claude Desktop, Cursor, Codex). The conversation is encrypted between your machine and the desk; MCP Desk's servers only relay ciphertext and cannot read it. Encryption and compression run on the two endpoints. Claude.ai and ChatGPT connectors cannot use it (the cloud service is the client). Setup and limits: https://mcpdesk.io/security/end-to-end
  - On the desk: `mcpdeskagent pair-code` (10-minute single-use code that never leaves that machine)
  - On the client machine, once: `mcpdeskagent pair --desk <9 digits> --code <6 digits> --mcp-url https://mcp.mcpdesk.io/<user-id> --bearer <mdu_...>`
  - In your AI client: `mcpdeskagent bridge --desk <9 digits> --mcp-url https://mcp.mcpdesk.io/<user-id>` (bearer in `MCPDESK_BEARER`)
  - Manage clients on the desk: `mcpdeskagent clients [--revoke <label>]`; on the client: `bridge --forget-desk`.
- The desk's rotating one-time code now changes every 10 minutes (was 5).
- New binary: Windows ARM64.
- Known caveats: binaries are not code-signed (verify with `SHA256SUMS`); macOS is not built; the ARM64 builds were not run on real ARM hardware.
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
