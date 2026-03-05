"""
Movie Launcher — starts Scene 1 (HTML poster) and Scene 2 (Shiny app),
then opens the browser.

Usage:
    uv run python src/movie_launcher.py
"""
from __future__ import annotations

import http.server
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

SCENE1_PORT = 8001
SCENE2_PORT = 8000
SCENE1_HTML = Path(__file__).parent / "movie_scene1.html"


# ---------------------------------------------------------------------------
# Scene 1 — minimal HTTP server that serves movie_scene1.html for any request
# ---------------------------------------------------------------------------

class Scene1Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            content = SCENE1_HTML.read_bytes()
        except FileNotFoundError:
            self.send_error(404, "movie_scene1.html not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, fmt, *args):  # silence request logs
        pass


def _run_scene1_server() -> None:
    try:
        server = http.server.HTTPServer(("127.0.0.1", SCENE1_PORT), Scene1Handler)
        server.serve_forever()
    except Exception as exc:
        print(f"  Scene 1 server error: {exc}")


# ---------------------------------------------------------------------------
# Scene 2 — launch lesson01_app.py via uvicorn (Shiny)
# ---------------------------------------------------------------------------

def _run_scene2_server() -> subprocess.Popen:
    script = Path(__file__).parent / "lesson01_app.py"
    # Use uv run so the subprocess gets the correct virtual environment
    return subprocess.Popen(
        ["uv", "run", "python", str(script)],
        cwd=Path(__file__).parent.parent,  # project root
    )


def _wait_for_scene2(timeout: float = 15.0) -> bool:
    """Poll until the Shiny app responds or timeout expires."""
    import urllib.request
    import urllib.error

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{SCENE2_PORT}/", timeout=1)
            return True
        except Exception:
            time.sleep(0.4)
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("  Starting Scene 2 (Shiny app) on port", SCENE2_PORT, "...")
    scene2_proc = _run_scene2_server()

    print("  Starting Scene 1 (poster) on port", SCENE1_PORT, "...")
    t = threading.Thread(target=_run_scene1_server, daemon=True)
    t.start()

    print("  Waiting for Shiny to be ready ...")
    ready = _wait_for_scene2()
    if not ready:
        print("  WARNING: Shiny did not respond in time — opening anyway.")

    url = f"http://127.0.0.1:{SCENE1_PORT}/"
    print(f"\n  Opening browser -> {url}")
    print("  Press Ctrl-C to stop.\n")
    webbrowser.open(url)

    try:
        scene2_proc.wait()
    except KeyboardInterrupt:
        print("\n  Shutting down...")
        scene2_proc.terminate()


if __name__ == "__main__":
    main()
