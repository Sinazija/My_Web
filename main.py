import os
import json
import socket
import threading
from datetime import datetime

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

PORT = 3000
SOCKET_PORT = 5000
CONTENT_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.png': 'image/png'
}

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_file('index.html')
        elif pr_url.path == '/message':
            self.send_file('message.html')
        elif pr_url.path == '/style.css':
            self.send_file('style.css', content_type='text/css')
        elif pr_url.path == '/logo.png':
            self.send_file('logo.png', content_type='image/png')
        else:
            self.send_file('error.html', status=404)

    def do_POST(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Отримуємо дані з форми
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            username = data['username'][0]
            message = data['message'][0]

            # Відправляємо дані на Socket сервер
            send_to_socket_server(username, message)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Thank you for your message!')
        else:
            self.send_file('error.html', status=404)

    def send_file(self, filename, status=200, content_type='text/html'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        file_path = os.path.join(os.path.dirname(__file__), filename)
        with open(file_path, 'rb') as fd:
            self.wfile.write(fd.read())


def run_http_server():
    server_address = ('', PORT)
    http = HTTPServer(server_address, HttpHandler)
    try:
        print(f'Starting HTTP server on port {PORT}')
        http.serve_forever()
    except KeyboardInterrupt:
        print('HTTP server interrupted, shutting down...')
        http.server_close()


def send_to_socket_server(username, message):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    data = {
        current_time: {
            'username': username,
            'message': message
        }
    }

    # Перетворюємо дані у формат JSON
    json_data = json.dumps(data)

    # Відправляємо дані на Socket сервер
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', SOCKET_PORT)
    sock.sendto(json_data.encode('utf-8'), server_address)
    sock.close()


def run_socket_server():
    server_address = ('', SOCKET_PORT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    try:
        print(f'Starting Socket server on port {SOCKET_PORT}')
        while True:
            data, address = sock.recvfrom(4096)
            handle_socket_data(data)
    except KeyboardInterrupt:
        print('Socket server interrupted, shutting down...')
    finally:
        sock.close()


def handle_socket_data(data):
    # Отримуємо дані з Socket сервера
    json_data = data.decode('utf-8')
    data = json.loads(json_data)

    # Зберігаємо дані у файлі data.json
    file_path = os.path.join(os.path.dirname(__file__), 'storage', 'data.json')
    with open(file_path, 'a+') as f:
        f.seek(0)
        contents = f.read()
        if contents:
            f.seek(0, os.SEEK_END)
            f.write(',\n')
        f.write(json_data)


if __name__ == '__main__':
    # Створюємо папку "storage", якщо вона не існує
    os.makedirs('storage', exist_ok=True)

    # Запускаємо HTTP сервер у окремому потоці
    http_thread = threading.Thread(target=run_http_server)
    http_thread.start()

    # Запускаємо Socket сервер у головному потоці
    run_socket_server()


#http://localhost:3000