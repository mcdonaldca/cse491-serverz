#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from StringIO import StringIO
from app import make_app
from wsgiref.validate import validator
from sys import stderr

## Quixhote
# import quixote
# from quixote.demo.altdemo import create_publisher
# p = create_publisher()
##

## Image app
# import quixote
# import imageapp
# imageapp.setup()
# p = imageapp.create_publisher()
##

def handle_connection(conn, port):

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
    environ['REQUEST_METHOD'] = 'GET'
    environ['PATH_INFO'] = path_information.path
    environ['QUERY_STRING'] = path_information.query
    environ['CONTENT_TYPE'] = 'text/html'
    environ['CONTENT_LENGTH'] = str(0)
    environ['SCRIPT_NAME'] = ''
    environ['SERVER_NAME'] = socket.getfqdn()
    environ['SERVER_PORT'] = str(port)
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.errors'] = stderr
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = False
    environ['wsgi.run_once'] = False
    environ['wsgi.url_scheme'] = 'http'
    env['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''
    

    # Start response function for WSGI interface
    def start_response(status, response_headers):
        """Send the initial HTTP header, with status code
            and any other provided header information"""

        # Send HTTP status
        conn.send('HTTP/1.0')
        conn.send(status)
        conn.send('\r\n')

        # Send the response headers
        for pair in response_headers:
            key, value = pair
            conn.send(key + ": " +  value + '\r\n')
        conn.send('\r\n')

    # If we received a POST request, collect the rest of the data
    content = ''
    if request[0] == "POST":
        # Set up extra environ variables
        environ['REQUEST_METHOD'] = 'POST'
        environ['CONTENT_LENGTH'] = header_information['Content-Length']
        environ['CONTENT_TYPE'] = header_information['Content-Type']


        # Continue receiving content up to content-length
        content_length = int(header_information['Content-Length'])
        while len(content) < content_length:
            content += conn.recv(1)

    # Set up a StringIO to mimic stdin for the FieldStorage in the app
    environ['wsgi.input'] = StringIO(content)

    # Get the application
    application = make_app()

    ## Quixote alt.demo
    # wsgi_app = quixote.get_wsgi_app()
    ##

    ## Imageapp
    # wsgi_app = quixote.get_wsgi_app()
    ##
    
    application = validator(application)

    result = application(environ, start_response)

    # Serve the processed data
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
        handle_connection(c, client_port)

if __name__ == '__main__':
    main()

