import http.server
import socketserver
import os

# 明确切换到目标目录
target_dir = os.path.join(os.getcwd(), 'frontend', 'build')
os.chdir(target_dir)

PORT = 3000
Handler = http.server.SimpleHTTPRequestHandler

print(f"当前工作目录: {os.getcwd()}")
print(f"目录内容:")
for item in os.listdir('.'):
    print(f"  - {item}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"服务器运行在 http://localhost:{PORT}")
    print(f"服务目录: {os.getcwd()}")
    httpd.serve_forever()
