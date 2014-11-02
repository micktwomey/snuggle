# Snuggle

Snuggle up in WSGI.

A top leve, single WSGI middleware intended to handle 80% of your app's needs. Let your app snuggle up in this and you get a running start on setting up  your app.

Handles:

- Logging
- Request context
- Metrics
- Error handling
- Authentication
- Sessions
- Caching
- Transactions

# Why?

Most WSGI apps seems to accrue a lot of boilerplate WSGI middleware (if they go down the WSGI route), which in turn is very brittle due to dependencies between layers. Other frameworks do everything for you in their own terms. This sits in the middle of the two extremes, it lets you write a simple WSGI app as PEP 333 intended and be sure that all the important stuff is taken care of. It should even work with many existing frameworks (I hope).

This aims to be somewhat prescriptive, the goal is to ensure you don't have to think about stuff like supplying information to your exception handler, what to log or how.

This obviously acts somewhat as a framework, with plugin hooks for you to integrate your stuff into. However, unlike WSGI middleware, there is a defined path the code follows (and hopefully the defaults are useful).

# Example

An example from the wsgiref module:

```py

from wsgiref.simple_server import make_server

from snuggle import middleware

def hello_world_app(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain')]
    start_response(status, headers)
    return ["Hello World"]

hello_world_app = middleware.wrap(hello_world_app)
httpd = make_server('', 8000, hello_world_app)
httpd.serve_forever()

```

This should give you a bunch of useful default behaviours which should aid you in future development and deployments.


# Logging

- Default to INFO level
- Log to JSON
- 