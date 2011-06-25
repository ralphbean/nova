# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose, url
from tg import redirect, validate, flash

# third party imports
#from pylons.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from nova.lib.base import BaseController
from nova.model import DBSession, metadata, Node, Vocab
from sqlalchemy.orm.exc import MultipleResultsFound
from tw2.qrcode import QRCodeWidget

import markdown

class NodeEntryController(object):
    def __init__(self, node_name):
        self.node = DBSession.query(Node).filter(Node.key.like("%%%s%%"%node_name)).one()

    @expose('nova.templates.node.index')
    def index(self):
        qr = QRCodeWidget(id="nodeqr", data=url("http://127.0.0.1/%s"%self.node.key))

        for attr in self.node.attrs:
            v = DBSession.query(Vocab).filter(Vocab.key.like("%%%s%%"%attr)).one()
            
            if v.resolve:
                if self.node.attrs[attr] is not '':
                    t_obj = DBSession.query(Node).filter(Node.key.like("%%%s%%"%self.node.attrs[attr])).one()
                else:
                    t_obj = None    
                self.node.attrs[attr] = t_obj

            self.node.attrs[attr] = {'data':self.node.attrs[attr], 'vocab':v}

        return dict(page="node.index", node=self.node, markdown=markdown, qrcode=qr)

