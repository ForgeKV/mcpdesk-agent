# Published macOS binary checks

This harness tests public release executables on native Apple Silicon and Intel
GitHub-hosted macOS runners. It contains no agent implementation source and uses no
production credentials. The agent runs locally with isolated temporary identities,
loopback listeners, and the public hub/tunnel/updater disabled.

[v0.2.16 results](https://github.com/ForgeKV/mcpdesk-agent/actions/runs/39861126962):
35 checks each for universal and aarch64 on macOS 14.8.9 arm64, and 35 each for
universal and x86_64 on macOS 15.7.9 Intel. All 140 checks passed.

Checks include SHA-256 verification, native startup, HTTP and stdio MCP, file reads
and writes, allowed roots, binary transfer, shell execution and timeout, background
tasks, read-only refusal, PTY rendering, F1/F3 confirmation and clean shutdown.
macOS 11–13, Gatekeeper/browser quarantine, notarization, production hub/tunnel
connections, service installation and long-duration use are outside this run.

Re-run using the published tag:

```sh
gh workflow run macos-runtime.yml --repo ForgeKV/mcpdesk-agent -f tag=v0.2.16
```
