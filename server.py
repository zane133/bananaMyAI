"""
🍌 Nano Banana Studio - Local Server
用法: python server.py
然后浏览器访问 http://localhost:8765
生成的图片自动保存到本文件所在目录
"""

import os
import json
import base64
import time
import urllib.request
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8765
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):

    def do_OPTIONS(self):
        self._cors()
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if self.path == '/save-image':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = json.loads(self.rfile.read(length))

                idx = body.get('idx', 0)
                ts = int(time.time() * 1000)
                filename = f"nanobanana_{ts}_{idx + 1}.png"
                filepath = os.path.join(SAVE_DIR, filename)

                if 'data' in body:
                    # base64 inline data
                    raw = base64.b64decode(body['data'])
                    with open(filepath, 'wb') as f:
                        f.write(raw)
                    print(f"  ✅ 已保存: {filename}  ({len(raw) // 1024} KB)")

                elif 'url' in body:
                    # remote URL
                    req = urllib.request.Request(
                        body['url'],
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        raw = resp.read()
                    with open(filepath, 'wb') as f:
                        f.write(raw)
                    print(f"  ✅ 已保存: {filename}  ({len(raw) // 1024} KB)")

                else:
                    raise ValueError('请求体中缺少 data 或 url 字段')

                self._cors()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'ok': True,
                    'filename': filename,
                    'path': filepath,
                }).encode())

            except Exception as e:
                print(f"  ❌ 保存失败: {e}")
                self._cors()
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode())
        else:
            self._cors()
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        # Serve static files (index.html etc.)
        super().do_GET()

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def end_headers(self):
        self._cors()
        super().end_headers()

    def log_message(self, fmt, *args):
        # Suppress default noisy GET logs; only print POST manually
        if self.command == 'POST':
            pass  # already printed above
        # Uncomment below to see all requests:
        # print(f"[{self.address_string()}] {fmt % args}")


def open_browser():
    time.sleep(0.8)
    webbrowser.open(f'http://localhost:{PORT}')


if __name__ == '__main__':
    os.chdir(SAVE_DIR)
    server = HTTPServer(('localhost', PORT), Handler)

    print(f"\n🍌  Nano Banana Studio 本地服务器")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"🌐  地址:    http://localhost:{PORT}")
    print(f"📁  保存至:  {SAVE_DIR}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   按 Ctrl+C 停止服务器\n")

    threading.Thread(target=open_browser, daemon=True).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋  服务器已停止")
