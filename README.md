# MCP Desk Agent

MCP Desk Agent lets your AI reach this computer through MCP Desk — AnyDesk-style remote MCP for AI. Run the agent, get a desk code, approve connections, and choose which tools your desk exposes.

Website: https://mcpdesk.ai

This repository holds release binaries and black-box validation tooling. Agent implementation source is not published here.

## Download (latest)

Latest: **v0.2.30**. All binaries below contain the same release.

| Platform | File |
|---|---|
| Windows x86_64 | [mcpdeskagent.exe](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent.exe) |
| Windows ARM64 | [mcpdeskagent-windows-aarch64.exe](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-windows-aarch64.exe) |
| macOS universal (Apple Silicon + Intel, macOS 11+) | [mcpdeskagent-macos-universal](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-macos-universal), [.tar.gz](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-macos-universal.tar.gz) |
| macOS Apple Silicon (M1+) | [mcpdeskagent-macos-aarch64](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-macos-aarch64) |
| macOS Intel | [mcpdeskagent-macos-x86_64](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-macos-x86_64) |
| macOS service installer | [install-macos.sh](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/install-macos.sh) |
| Linux x86_64 (static) | [mcpdeskagent-linux-x86_64](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-x86_64) |
| Linux aarch64 (static) | [mcpdeskagent-linux-aarch64](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-linux-aarch64) |
| Linux launcher + icon | [mcpdeskagent.desktop](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent.desktop), [mcpdeskagent.png](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent.png) |
| Checksums | [SHA256SUMS](https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/SHA256SUMS) |

Mac quick start: `curl -LO https://github.com/ForgeKV/mcpdesk-agent/releases/latest/download/mcpdeskagent-macos-universal && chmod +x mcpdeskagent-macos-universal && ./mcpdeskagent-macos-universal`. v0.2.16 passed [140 native runtime checks](https://github.com/ForgeKV/mcpdesk-agent/actions/runs/39861126962) on macOS 14 Apple Silicon and macOS 15 Intel. See [validation coverage](validation/README.md) and [Mac first-run instructions](https://mcpdesk.ai/docs#macos). All releases: https://github.com/ForgeKV/mcpdesk-agent/releases

## In v0.2.30

- **Default endpoints are now mcpdesk.ai**, with automatic fallback to mcpdesk.io. The agent’s default hub is `https://hub.mcpdesk.ai` (MCP/gateway `https://mcp.mcpdesk.ai`). If that hub is unreachable — TLS failure or HTTP 5xx, including Cloudflare 526 — it tries the matching `.io` host once. Desks already registered on `.io` stay on `.io`.
- Windows builds in this release are unsigned (Trusted Signing is being wired separately). macOS 11+; still not Developer ID signed or notarized.

## In v0.2.29

- **Link a desk from inside your AI.** Ask your AI to "link desk <9 digits> code <6 digits>"; the desk asks Allow? (a dialog, a console line, or `mcpdeskagent link approve --wait 120` on a headless server). **This is a permanent link!** The desk becomes private to that account: its desk code and one-time code no longer let anyone else connect. Linking to another account needs Allow again and removes the previous owner. `mcpdeskagent link status|approve|deny|revoke`. Needs the updated MCP Desk service; until then desks stay public as before.
- **First screen checklist**: online, linked owner or what to tell your AI, and on macOS Screen Recording / Accessibility with Fix buttons (`mcpdeskagent screen permissions --open screen|accessibility`).
- **macOS per-user agent**: `./mcpdeskagent-macos-universal install-service --user` (no sudo) starts at login in your session and can capture the screen once allowed; `uninstall-service --user` removes it. Still not Developer ID signed or notarized.
- Unchanged: OAuth, the 10-minute one-time code, public desks, the tools.

## In v0.2.28

- **Live Browser tab no longer stays white.** An address typed while the desk was still asking for approval or starting the browser used to be dropped, leaving a blank page at 0 fps. The desk now opens it as soon as the stream starts.
- **Key-only desks** no longer log a `public_key_conflict` re-register warning on every start. **Linux installer**: `--from DIR` wins over an old identity in root's home, and stops with an error if DIR has no identity.
- **macOS**: `--data-dir /tmp/...` works (data dirs behind a symlink such as /tmp -> /private/tmp are resolved first). A device.key in the wrong format (OpenSSL PEM, OpenSSH, PKCS#8 v1) gets an error that says so. A desk with no usable display reports that before asking for screen approval.
- Unchanged: OAuth, the 10-minute one-time code, the wire protocol and the tools.

## In v0.2.27

- **Live links are sign-in only.** The desk's guide tells the AI to hand over the `open_live_view` link only, with no confirm code. The link opens in a browser signed in to mcpdesk.io as the connection's own account. Without a link, https://mcpdesk.io/live still works with the desk code and one-time code.
- Unchanged: OAuth, the 10-minute one-time code, the wire protocol, the tools and the live view itself (including monitor switching).

## In v0.2.26

- **Monitor switching in the live view.** A desk with several displays shows a monitor picker in the /live toolbar. The picture, pointer and input follow the chosen monitor (Windows, macOS and Linux X11). On Windows, clicks now land correctly on monitors left of or above the primary one.
- On Windows and macOS a viewer the desk has approved can now pick any monitor, not only the primary one.
- Unchanged: OAuth, the 10-minute one-time code, the wire protocol and the MCP screenshot tools.

## In v0.2.25

- **Sharp, smooth live view.** The picture stays at native size (up to 1920 px wide; the frame rate drops before the size does), with area-averaged scaling so small text stays readable. About 0.5 Mbit/s at 1920×1200 on a normal screen.
- **Smooth mouse.** The viewer's browser draws the pointer itself and input is sent ahead of frames.
- **Colored /live toolbar** and a clear message when a one-time live link is reused in a second tab (the first tab stays live).
- **Faster WebRTC start** for browsers that send congestion feedback, with quick backoff on heavy packet loss.
- Remote screen still starts on VIEW, even when access is FULL; CONTROL needs a click and a confirm on the desk.

## In v0.2.13

- **The ready line names the server.** The desk now prints `Tell your AI: mcpdesk connect device 123456789 code 000000` (placeholder values). An AI client with several MCP servers did not always know which server `connect device …` referred to; the leading `mcpdesk` fixes that. The plain form is still accepted.
- **The file tools explain themselves.** `download_file` / `upload_file` now say what they are — base64 through the conversation, for small files — and point the AI at `pull_file` / `push_file` (through `mcpdeskagent bridge --desk`) for a real copy, asking you for the bridge when those tools are not in its list. Through the bridge the two base64 tools lead with "Prefer pull_file / push_file in this session", and a `download_file` of a file over 1 MB carries a one-line note on its first chunk. AIs were picking `download_file` and ending up with base64 they could not use.

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
- Known caveats: binaries are not code-signed (verify with `SHA256SUMS`); the ARM64 builds were not run on real ARM hardware.
For a stopped headless/service identity, recover access with `mcpdeskagent access resume --data-dir <exact-identity-directory>`. Stop the service and close all mirrors first. Resume permits still-valid credentials to create fresh sessions under the selected mode.

## Windows code signing

Windows EXEs are Authenticode-signed with Azure Trusted Signing (account `mcpdesk-signing`, profile `mcpdesk-public`) when that certificate profile is available. Until Microsoft finishes identity validation, releases stay unsigned; verify them with `SHA256SUMS`. After the profile exists, re-run the **Sign Windows release** workflow against the release tag.

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
