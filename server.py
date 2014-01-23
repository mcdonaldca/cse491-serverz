#!/usr/bin/env python
import random
import socket
import time

def handle_get(conn, path):
    # Set up information for each page type
    successful_meta =  "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
    failed_meta =  "HTTP/1.0 404 Not Foundr\nContent-Type: text/html\r\n\r\n"
    start = "<!DOCTYPE html><html><body>"
    end = "</body></html>"

    index_content = '<h1>Hello, world</h1> This is mcdonaldca\'s web server' + \
                    '<ul><li><a href="/content">Content</a>' + \
                    '<li><a href="/image">Image</a></li>' + \
                    '<li><a href="/file">File</a></li></ul>'
    content_content = "<h1>Hello, world</h1> This is mcdonaldca's content page"
    file_content = "<h1>Hello, world</h1> This is mcdonaldca's file page"
    image_content = "<h1>Hello, world</h1> This is mcdonaldca's image page"
    failed_content = "<h1>Uh Oh Oreo</h1> This is not the page you are looking for"

    web_page = successful_meta + start + index_content + end

    if path == '/':
        pass
    elif path == '/content':
        web_page = successful_meta + start + content_content + end
    elif path == '/file':
        web_page = successful_meta + start + file_content + end
    elif path == '/image':
        web_page = successful_meta + start + image_content + end
    else:
        web_page = failed_meta + start + failed_content + end

    conn.send(web_page)

def handle_post(conn):
    web_page = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + \
               "<!DOCTYPE html><html><body>" + \
               "<h1>Hello, World</h1></body></html>"
    conn.send(web_page)

def handle_connection(conn):
    
    request = conn.recv(1000)   # Get request information from client
    type_req = path = request.split()[0]

    if type_req == "GET":
    
        try:
            path = request.split()[1]
        except IndexError:          # No code breaks plz
            path = "/404"

        handle_get(conn, path)

    elif type_req == "POST":
        
        handle_post(conn)
        
    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn()     # Get local machine name
    port = random.randint(8000, 9999)
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

