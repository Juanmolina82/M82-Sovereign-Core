from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os

class M82Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Evitar caché en data.json para telemetría fresca, cachear estáticos
        if self.path.endswith('.json'):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        else:
            self.send_header("Cache-Control", "max-age=60")
        super().end_headers()

os.chdir(os.path.expanduser("~/M82/app"))
server = ThreadingHTTPServer(("127.0.0.1", 8000), M82Handler)
server.serve_forever()
