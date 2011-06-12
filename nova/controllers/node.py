# -*- coding: utf-8 -*-
"""Sample controller module"""

# turbogears imports
from tg import expose
from tg import redirect, validate, flash

# third party imports
#from pylons.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from nova.lib.base import BaseController
from nova.model import DBSession, metadata, Node, Vocab
from sqlalchemy.orm.exc import MultipleResultsFound

class NodeController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()
    
    @expose('nova.templates.index')
    def index(self):
        page = "index"
        # must be the index
        latest_updates = DBSession.query(Node).order_by('modified desc').limit(10)
        return dict(page="index", updates=latest_updates)

    @expose()
    def _lookup(self, node_name, *remainder):
        nc = NodeEntryController(node_name)
        return nc, remainder


class NodeEntryController(object):
    def __init__(self, node_name):
        self.node = DBSession.query(Node).filter(Node.key.like("%%%s%%"%node_name)).one()

    @expose('nova.templates.node.index')
    def index(self):
        for attr in self.node.attrs:
            v = DBSession.query(Vocab).filter(Vocab.key.like("%%%s%%"%attr)).one()
            
            if v.resolve:
                if self.node.attrs[attr] is not '':
                    t_obj = DBSession.query(Node).filter(Node.key.like("%%%s%%"%self.node.attrs[attr])).one()
                else:
                    t_obj = None    
                self.node.attrs[attr] = t_obj

            self.node.attrs[attr] = {'data':self.node.attrs[attr], 'vocab':v}

        #raise ValueError(self.node.attrs.__class__.__name__)

        return dict(page="node.index", node=self.node)


