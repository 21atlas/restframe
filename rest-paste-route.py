# 1 simple case
"""

from __future__ import print_function

from wsgiref.simple_server import make_server
from urlparse import parse_qs

def myapp(environ, start_response):
    msg = 'no message!'
    response_headers = [('content-type','text/plain')]
    start_response('200 OK',response_headers)
    qs_params =  parse_qs(environ.get('QUERY_STRING'))
    if  'msg' in qs_params:
        msg = qs_params.get('msg')[0]
    return ['Your message was: {}'.format(msg)]


class Middleware:
    def __init__(self, app):
         self.wrapped_app = app

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('X-A-SIMPLE-TOKEN',"1234567890"))
            return start_response(status, headers, exc_info)

        return self.wrapped_app(environ, custom_start_response)

app = Middleware(myapp)

httpd = make_server('', 8080,app)

print("Starting the server on port 8080")

httpd.serve_forever()

"""
import os
from wsgiref.simple_server import make_server
from paste.deploy import loadapp

config = "./python_paste.ini"
appname = "common"
wsgi_app = loadapp("config:%s" % os.path.abspath(config), appname)
server = make_server('localhost',80,wsgi_app)
server.serve_forever()