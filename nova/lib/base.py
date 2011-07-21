# -*- coding: utf-8 -*-

"""The base Controller API."""

from tg import TGController, tmpl_context
from tg.render import render
from tg import request
from pylons.i18n import _, ungettext, N_
import nova.model as model
import tw2.jqplugins.ui as jqui
from tw2.core import JSLink
import tw2.duckpunch

__all__ = ['BaseController']


class BaseController(TGController):
    """
    Base class for the controllers in the application.

    Your web application should have one of these. The root of
    your application is used to compute URLs used by your app.

    """

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # TGController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        tw2.duckpunch.base.js_puncher.req().prepare()
        JSLink(link="/javascript/master.js").req().prepare()
        jqui.set_ui_theme_name('smoothness')
        jqui.jquery_ui.req().prepare()
        request.identity = request.environ.get('repoze.who.identity')
        tmpl_context.identity = request.identity
        return TGController.__call__(self, environ, start_response)
