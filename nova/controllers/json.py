# -*- coding: utf-8 -*-
"""Node REST controller module"""

# turbogears imports
from tg import expose, url
from tg import redirect, validate, flash

# third party imports
from pylons.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from nova.lib.base import BaseController
from nova.model import DBSession, metadata, Node, NodeType, Vocab
from sqlalchemy.orm.exc import MultipleResultsFound
from tw2.qrcode import QRCodeWidget
from tw2.jqplugins.ui import TabsWidget
import tw2.jquery
import markdown

class NodeJsonController(BaseController):
    @expose('json')
    def get_types(self):
        types = DBSession.query(NodeType).filter(
            NodeType.creatable==True).all()

        types_array = []
        for t in types:
            item = dict(
                key = t.key,
                name = t.name,
                description = t.description,
                icon = t.icon)
            types_array.append(item)

        return dict(types=types_array)

    @expose('json')
    def get_type(self, _type=None):
        t = DBSession.query(NodeType).filter(
            NodeType.key==_type).one()

        attrs = []
        for a in t.req_attrs:
            attrs.append(dict(
                    key = a.key,
                    name = a.name,
                    description = a.description.format(t.name),
                    default_val = a.default,
                    auto_complete_node = a.resolve))

        data = dict(
                key = t.key,
                name = t.name,
                description = t.description,
                icon = t.icon,
                req_attrs = attrs)

        return {t.key : data}

    @expose('json')
    def check_name(self, key=None):
        if key is None:
            return {"error": "Cannot ask for a empty key"}

        n = DBSession.query(Node).filter(
            Node.key == key.lower()).count()

        return {"exists": True if n > 0 else False}
