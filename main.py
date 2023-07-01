from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_file('D:\\GO_IT\\My Bot\\WEB\\my_web\\index.html')
        elif pr_url.path == '/message':
            self.send_file('D:\\GO_IT\\My Bot\\WEB\\my_web\\message.html')
        elif pr_url.path == '/style.css':
            self.send_file('D:\\GO_IT\\My Bot\\WEB\\my_web\\style.css')
        elif pr_url.path == '/logo.png':
            self.send_file('D:\\GO_IT\\My Bot\\WEB\\my_web\\logo.png')
        else:
            self.send_file('D:\\GO_IT\\My Bot\\WEB\\my_web\\error.html', 404)

    def send_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == '__main__':
    run()



#http://localhost:3000