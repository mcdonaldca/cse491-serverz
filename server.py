#!/usr/bin/env python
import random
import socket
import time
from urlparse import *

# Build various site pages

def index_page(conn, meta, start, end):
    content = '<h1>Hello, world</h1> This is mcdonaldca\'s web server' + \
              '<ul><li><a href="/content">Content</a>' + \
              '<li><a href="/image">Image</a></li>' + \
              '<li><a href="/file">File</a></li>' + \
              '<li><a href="/form">Form</a></li></ul>'
    conn.send(meta + start + content + end)

def content_page(conn, meta, start, end):
    content = '<h1>Hello, world</h1> This is mcdonaldca\'s content page'
    conn.send(meta + start + content + end)

def file_page(conn, meta, start, end):
    content = '<h1>Hello, world</h1> This is mcdonaldca\'s file page'
    conn.send(meta + start + content + end)

def image_page(conn, meta, start, end):
    content = '<h1>Hello, world</h1> This is mcdonaldca\'s image page'
    conn.send(meta + start + content + end)

def form_page(conn, meta, start, end):
    content = '<h1>Who goes there?</h1> This is mcdonaldca\'s web server' + \
              '<form action="submit" method="POST">' + \
              '<input type="text" name="firstname">' + \
              '<input type="text" name="lastname">' + \
              '<input type="submit" value="Submit"></form>'
    conn.send(meta + start + content + end)

def submit_page(conn, meta, start, end, information):
    # For GET
##    o = urlparse(information)
##    data = parse_qs(o.query)
##    content = '<h1>Hello, Ms. %s %s</h1> This is mcdonaldca\'s web server' % (data["firstname"][0], data["lastname"][0])

    # For POST
    data = parse_qs(information)

    firstname = data["firstname"][0]
    lastname = data["lastname"][0]
    
    content = '<h1>Hello, Ms. %s %s</h1> This is mcdonaldca\'s web server' % (firstname, lastname)
    conn.send(meta + start + content + end)

def invalid_page(conn, meta, start, end):
    content = '<h1>Uh Oh Oreo</h1> This is not the page you are looking for'
    conn.send(meta + start + content + end)

def handle_post(conn):
    web_page = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n" + \
               "<!DOCTYPE html><html><body>" + \
               "<h1>Hello, World</h1></body></html>"
    conn.send(web_page)

def handle_connection(conn):

    # Get request information from client
    request = conn.recv(1000)   

    # Find type of request (GET or POST)
    try:
        type_req = request.split()[0]
    except IndexError:
        type_req = "GET"

    # Find path
    try:
        path = request.split()[1]
    except IndexError:          
        path = "/404"

    # HTML for every page
    successful_meta =  "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
    post_meta =  "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n"
    failed_meta =  "HTTP/1.0 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
    start = "<!DOCTYPE html><html><body>"
    end = "</body></html>"

    
    if type_req == "GET":
    
        if path == '/':
            index_page(conn, successful_meta, start, end)
        elif path == '/content':
            content_page(conn, successful_meta, start, end)
        elif path == '/file':
            file_page(conn, successful_meta, start, end)
        elif path == '/image':
            image_page(conn, successful_meta, start, end)
        elif path == '/form':
            form_page(conn, successful_meta, start, end)
        elif '/submit' in path:
            submit_page(conn, successful_meta, start, end, path)
        else:
            invalid_page(conn, failed_meta, start, end)

    elif type_req == "POST":
        
        if '/submit' in path:
            # For GET
            # submit_page(conn, post_meta, start, end, path)

            # For POST
            submit_page(conn, post_meta, start, end, request.split()[-1])
        else:
            invalid_page(conn, failed_meta, start, end)
        
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

