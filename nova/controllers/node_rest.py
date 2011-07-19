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
from nova.model import DBSession, metadata, Node, NodeType, Vocab, Tag
from sqlalchemy.orm.exc import MultipleResultsFound
from tw2.qrcode import QRCodeWidget
from tw2.jqplugins.ui import ButtonWidget
import markdown
from nova.controllers.json import NodeJsonController
import tw2.forms
import tw2.core
from tw2.tinymce import TinyMCE, MarkupConverter
from formencode.validators import NotEmpty
from tw2.jqplugins.tagify import Tagify

class NodeRestController(RestController):

    json = NodeJsonController()

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
        tags = DBSession.query(Tag).all()
        return dict(page="node.index", tags=tags, node=obj, markdown=markdown, qrcode=qr)


    @expose('nova.templates.index')
    def get_all(self):
        page = "index"
        # must be the index
        latest_updates = DBSession.query(Node).order_by('modified desc')
        tags = DBSession.query(Tag).all()
        return dict(page="index", updates=latest_updates.limit(10), tags=tags)


    @expose('nova.templates.node.new')
    def new(self, *args, **kw):
        class NameForm(tw2.forms.TableLayout):
            children = [tw2.forms.TextField(
                            id = 'new_node_name',
                            label = "Name",
                            css_class = "ui-corner-all ui-widget-content",),
                        tw2.forms.Spacer(),
                        tw2.forms.TextField(
                            id = 'new_node_key',
                            label = "Key",
                            css_class = "ui-corner-all ui-widget-content",),
                        ]

        class DescriptionWidget(TinyMCE):
            id = "description_miu"
            rows = 20
            cols = 80

        class TagList(Tagify):
            id = "tag_miu"

        class Submit(tw2.forms.SubmitButton):
            id = "submit_button"
            value = "Create!"

        return dict(_notags=True,
            name_form=NameForm(submit=None),
            desc_widget=DescriptionWidget(),
            tag_list=TagList(),
            sub_button=Submit(),
            )

    @validate( {'new_node_name':NotEmpty,
                'new_node_key':NotEmpty,
                'description_miu':MarkupConverter}, error_handler=new)
    @expose()
    def post(self, **kw):
        raise Exception, kw
        return dict()
