#!/usr/bin/env python3
"""
前端服务器启动脚本
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

def start_server():
    """启动前端服务器"""
    try:
        # 切换到build目录
        build_dir = Path(__file__).parent / "build"
        
        if not build_dir.exists():
            print("错误: build目录不存在，请先运行 'npm run build'")
            return
        
        # 切换到build目录
        os.chdir(build_dir)
        
        # 设置端口
        PORT = 3000
        
        # 创建HTTP服务器
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"前端服务器运行在 http://localhost:{PORT}")
            print(f"服务目录: {build_dir.absolute()}")
            print("按 Ctrl+C 停止服务器")
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n服务器已停止")
                httpd.shutdown()
                
    except Exception as e:
        print(f"启动服务器失败: {e}")
        return

if __name__ == "__main__":
    start_server()
