import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_index_page():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is mcdonaldca\'s web server' + \
                      '<ul><li><a href="/content">Content</a>' + \
                      '<li><a href="/image">Image</a></li>' + \
                      '<li><a href="/file">File</a></li>' + \
                      '<li><a href="/form">Form</a></li></ul>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, '%s Got: %s' % (repr(expected_return), repr(conn.sent))

def test_content_page():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is mcdonaldca\'s content page</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent))

def test_image_page():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is mcdonaldca\'s image page</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent))

def test_file_page():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-Type: text/html\r\n\r\n' + \
                      '<!DOCTYPE html><html><body><h1>Hello, world</h1> ' + \
                      'This is mcdonaldca\'s file page</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent))

def test_post_request():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + \
                      "<!DOCTYPE html><html><body>" + \
                      "<h1>Hello, World</h1></body></html>"
    
    server.handle_connection(conn)
    
    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent))
