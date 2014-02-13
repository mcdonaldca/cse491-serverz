#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs
from jinja2 import FileSystemLoader, Environment
from cgi import FieldStorage
from StringIO import StringIO

def handle_connection(conn):

    # Get request information from client
    # Will grab arbitrarily (n) sized information
    request = conn.recv(1)
    while request[-4:] != "\r\n\r\n":
        request += conn.recv(1)

    print repr(request)

    # Separate the status from the necessary information from header
    # Split only once as teh request status is a single line
    request, data = request.split("\r\n", 1)

    # Gather specific information from the header
    # Last two items in the list are empty strings (hence the [:-2])
    header_information = {}
    
    for line in data.split('\r\n')[:-2]:
        key, value = line.split(':', 1)
        header_information[key] = value

    # Split into thre pieces of information:
    # HTTP method -- path -- HTTP version
    request = request.split(' ', 2)


    path_information = urlparse(request[1])

    # Link paths to their associated html pages
    paths = {
        '/'        : 'index.html',   \
        '/content' : 'content.html', \
        '/file'    : 'file.html',    \
        '/image'   : 'image.html',   \
        '/form'    : 'form.html',    \
        '/submit'  : 'submit.html',  \
        }

    # Load templates & prepare basic HTML
    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader)
    meta =  "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
    content = ''

    # Grab query information from GET request
    data = parse_qs(path_information.query)
    # Query info is stored in an odd way
    # Change the values from ['value'] to 'value'
    for key, value in data.items():
        data[key] = data[key][0]

    # Extra handling for POST request
    if request[0] == 'POST':
        # Continue to gather the content body
        while len(content) < int(header_information['Content-Length']):
            content += conn.recv(1)

        # Using CGI.FieldStorage to support multipart/form-data
        fs= FieldStorage(
            fp=StringIO(content),               \
            headers=header_information,         \
            environ={'REQUEST_METHOD' : 'POST'} \
            )

        # Take parsed information and add it to our data dictionary
        additional_data = {}
        for item in fs.keys():
            additional_data[item] = fs[item].value
        data.update(additional_data)

    # Validate requested path
    if path_information.path in paths:
        template = env.get_template(paths[path_information.path])

    # Send to 404 if not a valid path
    else:
        meta = "HTTP/1.0 404 Not Found\r\n\r\n"
        data['path'] = path_information.path
        template = env.get_template('404.html')
        

    # Build our webpage
    webpage = meta + template.render(data)

    # Send that puppy
    conn.send(webpage)
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

