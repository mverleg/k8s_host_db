from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps


class MockDB(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(dumps(dict(
            status='you have reached the mock database',
        )).encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()


def run(host, port):
    httpd = HTTPServer((host, port), MockDB)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print('first argument should be the bind host of the database')
        exit(1)
    if len(argv) < 3:
        print('second argument should be the bind port of the database')
        exit(1)
    try:
        port = int(argv[2])
    except ValueError:
        print('second argument should be the bind port, which must be a positive integer')
        exit(1)

    run(argv[1], int(argv[2]))

