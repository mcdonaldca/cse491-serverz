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


# Simple tests for each page of site
# Tests for the correct response header & simple keywords

def test_index_page():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, '3748')
    
    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')
    assert 'This is mcdonaldca\'s web server' in conn.sent
    
def test_content_page():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')
    assert 'For a "content page" there appears to be very little content...' in conn.sent


def test_image_page():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')


def test_file_page():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')


def test_form_page():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')
    assert '<form action = \'submit\'>' in conn.sent
    assert '<form action = \'submit\' method=\'POST\'>' in conn.sent
    

def test_404_page():
    conn = FakeConnection("GET /yolo HTTP/1.0\r\n\r\n")

    server.handle_connection(conn, '3748')

    print conn.sent

    assert conn.sent.startswith('HTTP/1.0 404 Not Found\r\n')
    assert 'Maybe someday we\'ll have a cool /404' in conn.sent

# Tests GET version of form submission

def test_submit_page():
    first = 'Caitlin'
    last = 'McDonald'
    conn = FakeConnection("GET\
 /submit?firstname={}&lastname={}\
 HTTP/1.0\r\n\r\n".format(first, last))

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')
    assert 'Hello, Ms. {} {}'.format(first, last) in conn.sent

# Tests POST version of form submission

def test_submit_page_urlencoded():
    first = 'Caitlin'
    last = 'McDonald'

    header_message = "POST /submit HTTP/1.1\r\n\
Connection: keep-alive\r\n\
Content-Length: 35\r\n\
Cache-Control: max-age=0\r\n\
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n\
Content-Type: application/x-www-form-urlencoded\r\n\
Accept-Encoding: gzip,deflate,sdch\r\n\
Accept-Language: en-US,en;q=0.8\r\n\r\n\
firstname={}&lastname={}".format(first, last)
    
    conn = FakeConnection(header_message)

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')
    assert 'Hello, Ms. {} {}'.format(first, last) in conn.sent

def test_submit_page_multipart():
    first = 'Caitlin'
    last = 'McDonald'

    header_message = 'POST /submit HTTP/1.0\r\n\
Content-Length: 374\r\n\
Content-Type: multipart/form-data;\
boundary=32452685f36942178a5f36fd94e34b63\r\n\r\n\
--32452685f36942178a5f36fd94e34b63\r\n\
Content-Disposition: form-data; name="lastname";\
 filename="lastname"\r\n\r\n\
{}\r\n\
--32452685f36942178a5f36fd94e34b63\r\n\
Content-Disposition: form-data; name="firstname";\
 filename="firstname"\r\n\r\n\
{}\r\n\
--32452685f36942178a5f36fd94e34b63\r\n\
Content-Disposition: form-data; name="key\
filename="key"\r\n\r\n\
value\r\n\
--32452685f36942178a5f36fd94e34b63--\r\n'.format(last, first)

    conn = FakeConnection(header_message)

    server.handle_connection(conn, '3748')

    assert conn.sent.startswith('HTTP/1.0 200 OK\r\n')
    assert 'Hello, Ms. {} {}'.format(first, last) in conn.sent
