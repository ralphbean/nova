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
from tg.controllers import RestController
from nova.model import DBSession, metadata, Node, NodeType, Vocab
from sqlalchemy.orm.exc import MultipleResultsFound
from tw2.qrcode import QRCodeWidget
import markdown


class NodeRestController(RestController):
    @expose('nova.templates.node.index')
    def get_one(self, node_name):
        obj = DBSession.query(Node).filter(
                Node.key.like("%%%s%%" % node_name)).one()
        qr = QRCodeWidget(id="nodeqr", data=url("http://127.0.0.1/" + obj.key))

        for attr in obj.attrs:
            v = DBSession.query(Vocab).filter(
                    Vocab.key.like("%%%s%%" % attr)).one()

            if v.resolve:
                if obj.attrs[attr] is not '':
                    t_obj = DBSession.query(Node).filter(
                        Node.key.like("%%%s%%" % obj.attrs[attr])).one()
                else:
                    t_obj = None
                obj.attrs[attr] = t_obj

            obj.attrs[attr] = {'data': obj.attrs[attr], 'vocab': v}

        return dict(page="node.index", node=obj, markdown=markdown, qrcode=qr)

    @expose('nova.templates.index')
    def get_all(self):
        page = "index"
        # must be the index
        latest_updates = DBSession.query(Node).order_by('modified desc')
        return dict(page="index", updates=latest_updates.limit(10))

    @expose('nova.templates.node.new')
    def new(self, *args, **kw):
        node_types = DBSession.query(NodeType).filter(NodeType.createable == True)
        node_attrs = {}
        for ty in node_types:
            node_attrs.append(ty.key,
                DBSession.query(Vocab).filter(Vocab.key.in_(ty.req_attrs)))

        return dict(page="node.new", types=node_types, req_attrs=node_attrs)
