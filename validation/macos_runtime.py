"""Black-box tests of published executables. Contains no agent implementation source.

All writes, identities, listeners and commands are confined to a disposable directory
and loopback. The agent never registers with the public hub during these tests.
"""
import base64
import hashlib
import json
import os
from pathlib import Path
import platform
import pty
import secrets
import selectors
import socket
import subprocess
import sys
import tempfile
import termios
import time
import urllib.error
import urllib.request

binary = str(Path(sys.argv[1]).resolve())
version = sys.argv[2]
checks = 0


def check(ok, label):
    global checks
    assert ok, label
    checks += 1
    print('PASS ' + label, flush=True)


class Client:
    def __init__(self, url, token):
        self.url, self.token, self.session, self.id = url, token, None, 0

    def request(self, method, params=None, notify=False):
        self.id += 1
        payload = {'jsonrpc': '2.0', 'method': method, 'params': params or {}}
        if not notify:
            payload['id'] = self.id
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Authorization': 'Bearer ' + self.token}
        if self.session:
            headers['Mcp-Session-Id'] = self.session
        req = urllib.request.Request(self.url, json.dumps(payload).encode(), headers)
        with urllib.request.urlopen(req, timeout=20) as response:
            self.session = response.headers.get('Mcp-Session-Id', self.session)
            data = response.read().decode()
            if response.status == 202 or not data:
                return None
            if 'text/event-stream' in response.headers.get('Content-Type', ''):
                return next(json.loads(line[5:]) for line in data.splitlines() if line.startswith('data:') and line[5:].strip() and json.loads(line[5:]).get('id') == self.id)
            return json.loads(data)

    def initialize(self):
        result = self.request('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'macos-public-runtime', 'version': '1'}})
        self.request('notifications/initialized', notify=True)
        return result['result']

    def tool(self, name, args=None, allow_error=False):
        result = self.request('tools/call', {'name': name, 'arguments': args or {}})
        if 'error' in result:
            assert allow_error, result
            return True, json.dumps(result['error'])
        result = result['result']
        text = ''.join(item.get('text', '') for item in result.get('content', []))
        error = result.get('isError', False)
        assert allow_error or not error, (name, text)
        return error, text


def wait_for(fn, seconds=15):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        result = fn()
        if result:
            return result
        time.sleep(0.1)
    raise AssertionError('condition timed out')


with tempfile.TemporaryDirectory(prefix='mcpdesk-macos-runtime-') as folder:
    root = Path(folder).resolve()
    home, data, runtime, allowed = [root/name for name in ('home', 'identity', 'run', 'files')]
    for directory in (home, data, runtime, allowed):
        directory.mkdir()
    env = {k: v for k, v in os.environ.items() if not k.startswith(('MCPDESK_', 'SERVERMCP_', 'ANYAI_', 'GITHUB_', 'ACTIONS_'))}
    env.update(HOME=str(home), MCPDESK_DATA_DIR=str(data), MCPDESK_RUNTIME_DIR=str(runtime), MCPDESK_LOCAL_ONLY='true', MCPDESK_NO_UPDATE='true')
    print(json.dumps({'host': platform.platform(), 'architecture': platform.machine(), 'binary': Path(binary).name}), flush=True)
    check(version in subprocess.check_output([binary, '--version'], env=env, text=True, timeout=10), '--version runs')
    check('--mode' in subprocess.check_output([binary, '--help'], env=env, text=True, timeout=10), '--help runs')
    token = secrets.token_hex(24)
    (root/'tokens.txt').write_text('runtime:' + token + '\n')
    (root/'outside.txt').write_text('outside-root')
    (allowed/'fixture.txt').write_text('macOS UTF-8 שלום\nline2\n')
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    url = f'http://127.0.0.1:{port}/mcp'
    args = [binary, '--listen', f'127.0.0.1:{port}', '--token-file', str(root/'tokens.txt'), '--data-dir', str(data), '--allowed-root', str(allowed), '--audit-log', str(root/'audit.log'), '--local-only', '--no-update']
    for mode in ('full', 'readonly'):
        with (root/(mode+'.log')).open('wb') as log:
            proc = subprocess.Popen(args + ['--mode', mode], env=env, stdout=log, stderr=log)
            try:
                def ready():
                    if proc.poll() is not None:
                        raise AssertionError('agent exited: ' + (root/(mode+'.log')).read_text())
                    try:
                        urllib.request.urlopen(urllib.request.Request(url, data=b'{}'), timeout=1)
                    except urllib.error.HTTPError as error:
                        return error.code == 401
                    except OSError:
                        return False
                wait_for(ready)
                check(True, mode + ': HTTP starts and rejects unauthenticated requests')
                client = Client(url, token)
                init = client.initialize()
                check(init['serverInfo']['version'] == version, mode + ': MCP initialize reports release version')
                tools = {t['name'] for t in client.request('tools/list')['result']['tools']}
                check({'system_info', 'read_file', 'list_directory'} <= tools, mode + ': MCP catalog')
                info = json.loads(client.tool('system_info')[1])
                check(bool(info.get('hostname')) and info.get('memory', {}).get('total_gb', 0) > 0 and bool(info.get('disks')), mode + ': macOS system information, memory and disks')
                check('macOS UTF-8 שלום' in client.tool('read_file', {'path': str(allowed/'fixture.txt')})[1], mode + ': UTF-8 file reading')
                check(client.tool('read_file', {'path': str(root/'outside.txt')}, allow_error=True)[0], mode + ': outside-root read denied')
                if mode == 'readonly':
                    check('run_command' not in tools and 'write_file' not in tools and 'start_task' not in tools, 'readonly: mutation tools hidden')
                    check(client.tool('run_command', {'command': 'echo forbidden'}, allow_error=True)[0], 'readonly: direct mutation rejected')
                    continue
                client.tool('write_file', {'path': str(allowed/'new.txt'), 'content': 'written by MCP שלום\n'})
                check((allowed/'new.txt').read_text() == 'written by MCP שלום\n', 'full: file write persisted')
                check('new.txt' in client.tool('list_directory', {'path': str(allowed)})[1], 'full: directory listing')
                batch = json.loads(client.tool('read_multiple_files', {'paths': [str(allowed/'fixture.txt'), str(allowed/'new.txt')]})[1])
                check(len(batch['files']) == 2 and all('content' in f for f in batch['files']), 'full: batch reads')
                output = client.tool('run_command', {'command': "printf 'mac-runtime שלום\\n'; printf 'stderr-ok\\n' >&2; exit 3"}, allow_error=True)[1]
                check('mac-runtime שלום' in output and 'stderr-ok' in output and 'exit_code: 3' in output, 'full: shell, UTF-8, stderr and exit status')
                output = client.tool('run_command', {'command': 'sleep 20', 'timeout_secs': 1}, allow_error=True)[1]
                check('TIMED OUT' in output, 'full: command timeout')
                blob = secrets.token_bytes(256 * 1024)
                client.tool('upload_file', {'path': str(allowed/'payload.bin'), 'data': base64.b64encode(blob).decode(), 'sha256': hashlib.sha256(blob).hexdigest()})
                check((allowed/'payload.bin').read_bytes() == blob, 'full: binary upload hash')
                download = client.tool('download_file', {'path': str(allowed/'payload.bin')})[1]
                check(base64.b64decode(download.split('data_base64:\n', 1)[1]) == blob, 'full: binary download round trip')
                task = json.loads(client.tool('start_task', {'shell': 'sh', 'command': "printf 'task-start\\n'; sleep 1; printf 'task-done\\n'"})[1])
                task_id = task['task_id']
                other = Client(url, token); other.initialize()
                def completed():
                    result = json.loads(other.tool('task_status', {'task_id': task_id})[1])
                    return result if result['status'] not in ('running', 'stopping') else None
                check(wait_for(completed)['status'] == 'completed', 'full: background task survives a new MCP session')
                check('task-done' in json.loads(other.tool('read_task_output', {'task_id': task_id})[1])['text'], 'full: task output')
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill(); proc.wait()
                print((root/(mode+'.log')).read_text()[-4000:], flush=True)
                check(proc.returncode == 0, mode + ': clean SIGTERM shutdown')
    # JSON-lines stdio transport, independently from the HTTP listener.
    messages = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'macos-stdio-runtime', 'version': '1'}}},
        {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
        {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/list', 'params': {}},
    ]
    proc = subprocess.Popen([binary, '--stdio', '--mode', 'readonly', '--local-only', '--no-update'], env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    selector = selectors.DefaultSelector(); selector.register(proc.stdout, selectors.EVENT_READ)
    try:
        replies = {}
        for message in messages:
            proc.stdin.write((json.dumps(message)+'\n').encode()); proc.stdin.flush()
            if 'id' not in message:
                continue
            while message['id'] not in replies:
                assert selector.select(15), 'stdio reply timed out'
                line = proc.stdout.readline()
                assert line, 'stdio closed before reply'
                reply = json.loads(line)
                if 'id' in reply:
                    replies[reply['id']] = reply
        check(replies[1]['result']['serverInfo']['version'] == version, 'stdio: initialize')
        check('system_info' in {t['name'] for t in replies[2]['result']['tools']}, 'stdio: tool catalog')
        proc.stdin.close(); proc.wait(timeout=10)
        check(proc.returncode == 0, 'stdio: clean EOF shutdown')
    finally:
        selector.close()
        if proc.poll() is None:
            proc.kill(); proc.wait()
    # Exercise real terminal input/termios and local permission changes, not just pipes.
    import fcntl
    import signal
    import struct
    terminal_runtime = root/'terminal-run'
    tty_env = dict(env, TERM='xterm-256color', MCPDESK_RUNTIME_DIR=str(terminal_runtime))
    tty_args = args + ['--mode', 'full']
    tty_args[tty_args.index('--data-dir') + 1] = str(root/'terminal-identity')
    pid, fd = pty.fork()
    if pid == 0:
        os.execve(binary, tty_args, tty_env)
    os.set_blocking(fd, False)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack('HHHH', 34, 120, 0, 0))
    output = bytearray()
    exited = False
    def drain():
        while True:
            try:
                chunk = os.read(fd, 65536)
                if not chunk:
                    break
                output.extend(chunk)
            except (BlockingIOError, OSError):
                break
    def mode_is(mode):
        drain()
        try:
            return json.loads((terminal_runtime/'master.json').read_text())['mode'] == mode
        except (OSError, ValueError):
            return False
    try:
        wait_for(lambda: mode_is('full'))
        check(b'\x1b[' in output and b'FULL' in output, 'terminal: interactive UI renders')
        os.write(fd, b'\x1bOP')
        wait_for(lambda: mode_is('readonly'))
        check(True, 'terminal: F1 lowers access to readonly')
        output.clear()
        os.write(fd, b'\x1bOR')
        wait_for(lambda: (drain(), b'Confirm' in output)[1])
        check(mode_is('readonly'), 'terminal: F3 requires confirmation before raising access')
        os.write(fd, b'\r')
        wait_for(lambda: mode_is('full'))
        check(True, 'terminal: confirmation restores full access')
        os.write(fd, b'\x03')
        def terminal_exited():
            drain()
            return os.waitpid(pid, os.WNOHANG)
        status = wait_for(lambda: (r if r[0] else None) if (r := terminal_exited()) else None)
        exited = True
        check(os.waitstatus_to_exitcode(status[1]) == 0, 'terminal: Ctrl+C exits cleanly')
    finally:
        if not exited:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
        os.close(fd)
    print(json.dumps({'passed': checks, 'failed': 0, 'version': version, 'architecture': platform.machine(), 'binary': Path(binary).name}), flush=True)
