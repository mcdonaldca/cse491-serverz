# from http://docs.python.org/2/library/wsgiref.html

from wsgiref.util import setup_testing_defaults
from jinja2 import FileSystemLoader, Environment
import cgi

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
        '/submit'  : 'submit.html',  \
        }

    # Load templates
    loader = FileSystemLoader('./templates')
    env = Environment(loader=loader)
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]

    if environ['PATH_INFO'] in paths:
        template = env.get_template(response[environ['PATH_INFO']])
    else:
        status = '404 Not Found'
        template = env.get_template('404.html')

    x = parse_qs(environ['QUERY_STRING']).iteritems()
    for key, value in data.items():
        data[key] = data[key][0]
    args['path'] = environ['PATH_INFO']

    # Okay this is straight from Ben's code and WHAT
    if environ['REQUEST_METHOD'] == 'POST':
        headers = {k[5:].lower().replace('_','-') : v \
                   for k,v in environ.iteritems() if(k.startswith('HTTP'))}
        headers['content-type'] = environ['CONTENT_TYPE']
        headers['content-length'] = environ['CONTENT_LENGTH']
        fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
                              headers=headers, environ=environ)
        args.update({x : fs[x].value for x in fs.keys()})

    args = {unicode(k, "utf-8") : unicode(v, "utf-8") for k,v in args.iteritems()}

    # Return the page
    start_response(status, headers)
    return [bytes(template.render(args))]

def make_app():
    return simple_app
