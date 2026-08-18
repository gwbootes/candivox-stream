"""Serve this folder AND report a steering position, on one port.

An OBS Browser source never receives mouse movement. It cannot, so no page
trick gets around it. What a page CAN do is ask something else where to look.
That is what this does.

    GET  /position     ->  {"x": -1..1, "y": -1..1, "src": "cursor"}
    POST /position     <-  {"x": -1..1, "y": -1..1}
    POST /layout.json  <-  the placement editor saving where things stand

The page asks about thirty times a second and leans that way.

By default the answer is where your mouse is on the desktop. Anything that
POSTs a position takes over instead, and keeps control while it keeps talking.
Go quiet for two seconds and it hands back to the mouse.

That POST is the hook for Silhouette. When the PNGTuber knows where it is on
screen, it posts that number here and the camera follows the avatar rather
than the mouse. The page needs no changes for that to work.

Serving the page and the position from the same port matters. Same origin
means no CORS headers to get wrong, and no mixed-content block from an https
page reaching for a plain http one.

Run stage.bat rather than calling this directly.
"""
import ctypes
import json
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 8777

# How long an external steer stays in charge after its last message. Long
# enough to ride out a dropped frame, short enough that a crashed sender
# hands control back instead of freezing the camera.
EXTERNAL_HOLD = 2.0

# Virtual-screen metrics cover every monitor as one rectangle, so the cursor
# still maps sensibly when it crosses onto a second display.
SM_XVIRTUALSCREEN, SM_YVIRTUALSCREEN = 76, 77
SM_CXVIRTUALSCREEN, SM_CYVIRTUALSCREEN = 78, 79

_lock = threading.Lock()
_external = {"x": 0.0, "y": 0.0, "at": 0.0}


class _Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def clamp(v):
    return max(-1.0, min(1.0, float(v)))


def cursor():
    """Cursor position as x,y in -1..1 from the centre of the desktop."""
    user32 = ctypes.windll.user32
    pt = _Point()
    if not user32.GetCursorPos(ctypes.byref(pt)):
        return 0.0, 0.0

    left = user32.GetSystemMetrics(SM_XVIRTUALSCREEN)
    top = user32.GetSystemMetrics(SM_YVIRTUALSCREEN)
    width = user32.GetSystemMetrics(SM_CXVIRTUALSCREEN) or 1
    height = user32.GetSystemMetrics(SM_CYVIRTUALSCREEN) or 1

    # Clamp rather than trust the numbers. A cursor parked on a screen edge
    # can report a pixel outside the virtual rectangle.
    return (
        clamp(((pt.x - left) / width) * 2 - 1),
        clamp(((pt.y - top) / height) * 2 - 1),
    )


def position():
    with _lock:
        fresh = (time.monotonic() - _external["at"]) < EXTERNAL_HOLD
        if fresh:
            return _external["x"], _external["y"], "external"
    x, y = cursor()
    return x, y, "cursor"


class Handler(SimpleHTTPRequestHandler):
    def _json(self, payload, code=200):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        # Polled thirty times a second, so any caching at all is wrong.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] in ("/position", "/cursor"):
            x, y, src = position()
            self._json({"x": round(x, 4), "y": round(y, 4), "src": src})
            return
        super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] in ("/layout.json", "/layout"):
            self._save_layout()
            return
        if self.path.split("?")[0] != "/position":
            self.send_error(404)
            return
        try:
            n = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
            with _lock:
                _external["x"] = clamp(data.get("x", 0))
                _external["y"] = clamp(data.get("y", 0))
                _external["at"] = time.monotonic()
            self._json({"ok": True})
        except (ValueError, TypeError) as exc:
            # A malformed steer must never take the server down mid-stream.
            self._json({"ok": False, "error": str(exc)}, code=400)

    def _save_layout(self):
        """Write layout.json for the editor.

        The editor is the only thing that posts here, and it posts the whole
        file every time. The previous version is kept as layout.json.bak, so a
        misplaced save is one file rename away from being undone.
        """
        try:
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n)
            data = json.loads(raw or b"{}")
            if not isinstance(data.get("models"), dict):
                raise ValueError('expected {"models": {...}}')
            cam = data.get("camera")
            if cam is not None and not isinstance(cam, dict):
                raise ValueError('"camera" must be an object if present')

            here = Path(__file__).parent
            target = here / "layout.json"
            tmp = here / "layout.json.tmp"

            # Write beside it and rename, so a crash mid-write cannot leave a
            # half-finished file where a good one used to be.
            tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
            if target.exists():
                target.replace(here / "layout.json.bak")
            tmp.replace(target)

            where = ""
            if cam:
                where = (
                    f", camera y={cam.get('y')} z={cam.get('z')} "
                    f"pitch={cam.get('pitch')}"
                )
            print(f"saved layout.json ({len(data['models'])} models placed{where})")
            self._json({"ok": True, "count": len(data["models"])})
        except (ValueError, TypeError, OSError) as exc:
            self._json({"ok": False, "error": str(exc)}, code=400)

    def log_message(self, *_args):
        """Thirty requests a second would bury the window in noise."""


def main():
    handler = lambda *a, **k: Handler(*a, directory=str(Path(__file__).parent), **k)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    print(f"Candivox stage running on http://localhost:{PORT}")
    print("")
    print("Put this in your OBS Browser source:")
    print(f"  http://localhost:{PORT}/index.html?gallery=1&spin=15&follow=1")
    print("")
    print("Close this window to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
