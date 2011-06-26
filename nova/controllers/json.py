# -*- coding: utf-8 -*-
"""Node REST controller module"""

# turbogears imports
from tg import expose, url
from tg import redirect, validate, flash

# third party imports
#from pylons.i18n import ugettext as _
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
