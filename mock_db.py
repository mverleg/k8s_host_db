from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps


class MockDB(BaseHTTPRequestHandler):

    name = '???'

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(dumps(dict(
            status='you have reached the mock database \'{}\' using GET'.format(MockDB.name),
        )).encode('utf-8'))

    def do_POST(self):
        self._set_headers()
        self.wfile.write(dumps(dict(
            status='you have reached the mock database \'{}\' using POST'.format(MockDB.name),
        )).encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()


def run(name, host, port):
    # Setting static property name is ugly generally, but doesn't matter in this case,
    # as there's only one server instance, and very limited code.
    MockDB.name = name
    print('Starting mock db "{}" httpd at http://{}:{}...'.format(name, host, port))
    httpd = HTTPServer((host, port), MockDB)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print('first argument should be the name of the client')
        exit(1)
    if len(argv) < 3:
        print('second argument should be the bind host of the client')
        exit(1)
    if len(argv) < 4:
        print('third argument should be the bind port of the client')
        exit(1)
    try:
        port = int(argv[3])
    except ValueError:
        print('third argument should be the bind port, which must be a positive integer')
        exit(1)

    run(argv[1], argv[2], int(argv[3]))
