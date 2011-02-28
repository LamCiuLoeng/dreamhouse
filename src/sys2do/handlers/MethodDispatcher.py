# -*- coding: utf-8 -*-

import tornado.web

def delist_arguments(args):
    """
    Takes a dictionary, 'args' and de-lists any single-item lists then
    returns the resulting dictionary.

    In other words, {'foo': ['bar']} would become {'foo': 'bar'}
    """
    for arg, value in args.items():
        if len(value) == 1:
            args[arg] = value[0]
    return args

class MethodDispatcher(tornado.web.RequestHandler):
    """
    Subclasss this to have all of your class's methods exposed to the web
    for both GET and POST requests.  Class methods that start with an
    underscore (_) will be ignored.
    """

    def _dispatch(self):
        """
        Load up the requested URL if it matches one of our own methods.
        Skip methods that start with an underscore (_).
        """
        args = None
        # Sanitize argument lists:
        if self.request.arguments:
            args = delist_arguments(self.request.arguments)
        # Special index method handler:
        if self.request.uri.endswith('/'):
            func = getattr(self, 'index', None)
            if args:
                return func(**args)
            else:
                return func()
        path = self.request.uri.split('?')[0]
        method = path.split('/')[-1]
        if not method.startswith('_'):
            func = getattr(self, method, None)
            if func:
                if args:
                    return func(**args)
                else:
                    return func()
            else:
                raise tornado.web.HTTPError(404)
        else:
            raise tornado.web.HTTPError(404)

    def get(self):
        """Returns self._dispatch()"""
        return self._dispatch()

    def post(self):
        """Returns self._dispatch()"""
        return self._dispatch()
