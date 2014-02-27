#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from StringIO import StringIO
from app import make_app

def handle_connection(conn):

    # Get request information from client
    # Will grab arbitrarily (n) sized information
    request = conn.recv(1)
    while request[-4:] != "\r\n\r\n":
        add = conn.recv(1)
        if add:
            request += add
        else:
            return

    # Separate the status from the necessary information from header
    # Split only once as teh request status is a single line
    request, data = request.split("\r\n", 1)

    # Gather specific information from the header
    # Last two items in the list are empty strings (hence the [:-2])
    header_information = {}
    
    for line in data.split('\r\n')[:-2]:
        key, value = line.split(':', 1)
        header_information[key] = value

    # Split into three pieces of information:
    # HTTP method -- path -- HTTP version
    request = request.split(' ', 2)

    path_information = urlparse(request[1])

    # Build the environ object
    environ = {}
    path = urlparse(req.split(' ', 3)[1])
    environ['REQUEST_METHOD'] = 'GET'
    environ['PATH_INFO'] = path.path
    environ['QUERY_STRING'] = path.query
    environ['CONTENT_TYPE'] = 'text/html'
    environ['CONTENT_LENGTH'] = 0

    def start_response(status, response_headers):
        conn.send('HTTP/1.0')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, value = pair
            conn.send(key + ": " +  value + '\r\n')
        conn.send('\r\n')

    content = ''
    if req.startswith('POST '):
        environ['REQUEST_METHOD'] = 'POST'
        environ['CONTENT_LENGTH'] = header_information['Content-Length']
        environ['CONTENT_TYPE'] = header_information['Content-Type']
        while len(content) < int(header_information['Content-Length']):
            content += conn.recv(1)

    environ['wsgi.input'] = StringIO(content)
    application = make_app()
    result = application(environ, start_response)
    
    for data in result:
        conn.send(data)

    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
#    port = 3748
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

if __name__ == '__main__':
    main()

