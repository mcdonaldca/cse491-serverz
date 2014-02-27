# from http://docs.python.org/2/library/wsgiref.html
# encoding: utf-8

from wsgiref.util import setup_testing_defaults
from jinja2 import FileSystemLoader, Environment
import cgi
from urlparse import parse_qs
from StringIO import StringIO

# Helper functions (They're baaack)
def file_data(name):
    file = open(name, 'rb')
    data = [file.read()]
    file.close()
    return data

def index(env, **args):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    
    template = env.get_template('index.html')
    data = [template.render(args).encode('utf-8')]
    
    return (response_headers, data)

def content(env, **args):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    
    template = env.get_template('content.html')
    data = [template.render(args).encode('utf-8')]
    
    return (response_headers, data)

def serve_file(env, **args):
    response_headers = [('Content-type', 'text/plain; charset="UTF-8"')]

    data = file_data(args['path'][1:])

    return (response_headers, data)

def file(env, **args):
    args['path'] = '/files/cse491.txt'
    return serve_file(env, **args)

def serve_image(env, **args):
    response_headers = [('Content-type', 'text/plain; charset="UTF-8"')]

    data = file_data(args['path'][1:])

    return (response_headers, data)

def image(env, **args):
    args['path'] = '/img/cse491.jpg'
    return serve_file(env, **args)

def form(env, **args):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]

    template = env.get_template('form.html')
    data = [template.render(args).encode('utf-8')]

    return (response_headers, data)

def submit(env, **args):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    
    template = env.get_template('submit.html')
    data = [template.render(args).encode('utf-8')]
    
    return (response_headers, data)

def not_found(env, **args):
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]
    
    template = env.get_template('404.html')
    data = [template.render(args).encode('utf-8')]
    
    return (response_headers, data)


def app(environ, start_response):
    """A relatively simple WSGI application."""

    # Basically this is Ben's code. My brain is tired, and I think
    # I'm overcomplicating things in my head
    # UPDATE: Ben's code round 2. It's 5AM aka the point of no return

    # Link paths to their associated html pages
    paths = {
        '/'        : index,   \
        '/content' : content, \
        '/file'    : file,    \
        '/image'   : image,   \
        '/form'    : form,    \
        '/submit'  : submit,   \
        '/404'     : not_found,  \
        '/img/cse491.jpg'   : serve_image, \
        '/files/cse491.txt' : serve_file
        }

    # Load templates
    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader)

    data = {}
    qs = parse_qs(environ['QUERY_STRING']).iteritems()
    for key, value in qs:
        data[key] = value[0]
    data['path'] = environ['PATH_INFO']

    # Grab POST args if there are any
    if environ['REQUEST_METHOD'] == 'POST':
        # Re-parse the headers into a format field storage can use
        # Dashes instead of underscores, all lowercased
        headers = { 
                    key[5:].lower().replace('_','-') : val \
                    for key, val in environ.iteritems() \
                    if(key.startswith('HTTP'))
                  }
        # Pull in the non-HTTP variables that field storage needs manually
        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']

        ## Bad hack to get around validator problem
        if "multipart/form-data" in environ['CONTENT_TYPE']:
            content_length = int(environ['CONTENT_LENGTH'])
            info = environ['wsgi.input'].read(content_length)
            environ['wsgi.input'] = StringIO(info)
        
        # Create a field storage to process POST args
        fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                headers=headers, environ=environ)
        # Add these new args to the existing set
        data.update({key : fs[key].value for key in fs.keys()})

    # Get all the arguments in unicode form for Jinja
    data = {
            key.decode('utf-8') : val.decode('utf-8') \
            for key, val in data.iteritems()
           }

    # Check if we got a path to an existing page
    if environ['PATH_INFO'] in paths:
        # If we have that page, serve it with a 200 OK
        status = ' 200 OK'
        path = environ['PATH_INFO']
        
    else:
        # If we did not, redirect to the 404 page, with appropriate status
        status = ' 404 Not Found'
        path = '/404'

    data['path'] = path
    response_headers, info = paths[path](env, **data)


    # Return the page
    start_response(status, response_headers)
    return info

def make_app():
    return app
