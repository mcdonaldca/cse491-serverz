# from http://docs.python.org/2/library/wsgiref.html

from wsgiref.util import setup_testing_defaults
from jinja2 import FileSystemLoader, Environment
import cgi
from urlparse import parse_qs

# A relatively simple WSGI application. It's going to print out the
# environment dictionary after being updated by setup_testing_defaults
def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    # Basically this is Ben's code. My brain is tired, and I think
    # I'm overcomplicating things in my head

    # Link paths to their associated html pages
    paths = {
        '/'        : 'index.html',   \
        '/content' : 'content.html', \
        '/file'    : 'file.html',    \
        '/image'   : 'image.html',   \
        '/form'    : 'form.html',    \
        '/submit'  : 'submit.html'
        }

    # Load templates
    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader)
    response_headers = [('Content-type', 'text/html; charset="UTF-8"')]

    if environ['PATH_INFO'] in paths:
        status = '200 OK'
        template = env.get_template(paths[environ['PATH_INFO']])
    else:
        status = '404 Not Found'
        template = env.get_template('404.html')

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

    # Return the page
    start_response(status, response_headers)
    return [bytes(template.render(data))]

def make_app():
    return simple_app
