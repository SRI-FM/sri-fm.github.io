#!/usr/bin/env python3
"""Watch Org/site sources and reload local browser previews after successful builds."""
import argparse
import json
from pathlib import Path
import subprocess
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
version = str(time.time_ns())
reload_client = b"""<script>
(() => {
  let version;
  setInterval(async () => {
    try {
      const next = await (await fetch('/__dev_version', {cache: 'no-store'})).json();
      if (version !== undefined && version !== next) location.reload();
      version = next;
    } catch (_) { /* Keep the current page while the preview restarts. */ }
  }, 800);
})();
</script>"""


def sources():
    files = [ROOT / "publish.el", ROOT / "scripts/source-highlight.el"]
    for directory in (ROOT / "content", ROOT / "static", ROOT / "examples/tools"):
        files.extend(p for p in directory.rglob("*") if p.is_file() and not p.name.startswith("."))
    return tuple(sorted((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in files))


def watch():
    global version
    previous = sources()
    while True:
        time.sleep(0.5)
        current = sources()
        if current == previous:
            continue
        time.sleep(0.25)
        current = sources()
        print("Sources changed; rebuilding…", flush=True)
        result = subprocess.run(["make", "build"], cwd=ROOT, capture_output=True, text=True)
        previous = current
        if result.returncode == 0:
            version = str(time.time_ns())
            print("Build complete; refreshing browsers.", flush=True)
        else:
            print(result.stdout + result.stderr, flush=True)
            print("Build failed; fix the source to trigger another build.", flush=True)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PUBLIC), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?")[0] == "/__dev_version":
            data = json.dumps(version).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path /= "index.html"
        if path.suffix == ".html" and path.is_file():
            data = path.read_bytes().replace(b"</body>", reload_client + b"</body>")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()

    def log_message(self, format, *args):
        if self.path != "/__dev_version":
            super().log_message(format, *args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=1313)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    threading.Thread(target=watch, daemon=True).start()
    print(f"Live preview: http://localhost:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
