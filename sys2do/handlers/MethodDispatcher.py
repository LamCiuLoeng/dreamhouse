# -*- coding: utf-8 -*-
import os
import tornado.web
from sys2do.util.session import TornadoSession

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

    def initialize(self, **kw):
        self.session = TornadoSession(self.application.session_manager, self)

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

    #===========================================================================
    # add the login function
    #===========================================================================
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_current_user(self, name):
        self.set_secure_cookie("user", name)

    def clear_current_user(self):
        self.clear_cookie("user")

    #===========================================================================
    # add the flash function
    #===========================================================================

    def flash(self, msg = None, status = "OK"):
        if msg:
            self.session["message"] = msg
            self.session.save()
        else:
            tmp = self.session.pop("message")
            self.session.save()
            return tmp

    def need_flash(self):
        return bool(self.session.get("message", False))

    #===========================================================================
    # overwrite the render function
    #===========================================================================
#    def render(self, template_name, **kwargs):
#        if hasattr(self, "template_folder"):
#            template_name = os.path.join(self.template_folder, template_name)
#        super(self.__class__, self).render(template_name, **kwargs)
