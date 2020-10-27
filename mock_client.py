from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer


class MockClient(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def send_page(self, output, host, port):
        self._set_headers()
        self.wfile.write('''<html><body>
            <h1>Mock client</h1>
            <p>Here you can attempt to connect to the database</p>
            <form action=. method=GET>
            <p>
                <label for=host>Hostname (within k8s)</label>
                <input id=host name=host type=text value="{}" />
            </p>
            <p>
                <label for=host>Port (within k8s)</label>
                <input id=port name=port type=number value="{}" />
            </p>
            <p>
                <input type=submit value=Connect />
            </p>
            <p>
                {}
            </p>
            </form>
            </body></html>'''.format(host, port, output)
            .encode('utf-8'))

    def get_host_port(self):
        params = parse_qs(self.path[2:])
        return (
            params.get('host', ['localhost'])[0],
            params.get('port', [None])[0],
        )

    def do_GET(self):
        host, port = self.get_host_port()
        if not port:
            self.send_page('Click connect to attempt a connection', host, port)
            return
        data = 'TODO'  #TODO @mark:
        self.send_page('connecting to {}:{} returned:<br/><pre>{}</pre>'.format(host, port, data), host, port)

    def do_HEAD(self):
        self._set_headers()


def run(host, port):
    print('Starting mock client httpd at http://{}:{}...'.format(host, port))
    httpd = HTTPServer((host, port), MockClient)
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

