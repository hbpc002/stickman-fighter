#!/usr/bin/env python3
"""
简单的HTTP服务器用于测试修复后的游戏
"""

import http.server
import socketserver
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

def main():
    os.chdir('/home/hbpc/stickman-fighter')

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        print(f"🚀 测试服务器启动: http://localhost:{PORT}")
        print("=" * 50)
        print("可用的测试文件:")
        print(f"  - 完整版: http://localhost:{PORT}/standalone_test.html")
        print(f"  - 修复后的app.py需要Flask，但可用独立版测试")
        print("=" * 50)
        print("💡 测试步骤:")
        print("1. 访问 standalone_test.html")
        print("2. 检查控制台是否有错误")
        print("3. 测试重置按钮")
        print("4. 测试暂停按钮")
        print("5. 测试键盘控制")
        print("=" * 50)
        print("按 Ctrl+C 停止服务器")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")

if __name__ == '__main__':
    main()