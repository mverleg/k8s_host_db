from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockClient(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_page(self, output):
        self._set_headers()
        self.wfile.write('''<html><body>
            <h1>Mock client</h1>
            <p>Here you can attempt to connect to the database</p>
            <p>
                <label for=host>Hostname (within k8s)</label>
                <input id=host name=host type=text />
            </p>
            <p>
                <label for=host>Port (within k8s)</label>
                <input id=port name=port type=number value=8080 />
            </p>
            <p>
                <input type=submit value=Connect />
            </p>
            <p>
                {}
            </p>
            </body></html>'''.format(output)
            .encode('utf-8'))

    def do_GET(self):
        self.send_page('Click connect to attempt a connection')

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            return parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            return parse_qs(
                self.rfile.read(length),
                keep_blank_values=1)
        raise Exception('post data not found')

    def do_POST(self):
        data = self.parse_POST()
        host = data['hostname']
        port = data['port']
        self.send_page('connecting to {}:{} NOT IMPLEMENTED YET'.format(host, port))

    def do_HEAD(self):
        self._set_headers()


def run(host, port):
    httpd = HTTPServer((host, port), MockClient)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print('first argument should be the bind host of the client')
        exit(1)
    if len(argv) < 3:
        print('second argument should be the bind port of the client')
        exit(1)
    try:
        port = int(argv[2])
    except ValueError:
        print('second argument should be the bind port, which must be a positive integer')
        exit(1)

    run(argv[1], int(argv[2]))

