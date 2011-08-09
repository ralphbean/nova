# -*- coding: utf-8 -*-
"""Node REST controller module"""

# turbogears imports
from tg import expose, url
from tg import redirect, validate, flash
from tg import require

# third party imports
#from pylons.i18n import ugettext as _
from repoze.what import predicates

# project specific imports
from nova.lib.base import BaseController
from tg.controllers import RestController
from nova.model import DBSession, metadata, Node, NodeType, Attribute, Vocab, Tag, Revision, ImageFile
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tw2.qrcode import QRCodeWidget
from tw2.jqplugins.ui import ButtonWidget
from nova.controllers.json import NodeJsonController
from nova.controllers.blog import BlogRestController
import tw2.forms
import tw2.core
from tw2.tinymce import TinyMCE, MarkupConverter
from formencode.validators import NotEmpty, Regex
from tw2.jqplugins.tagify import Tagify
from nova.util import distill, revise_and_commit, get_revision_feed, get_blog_posts_feed

class NodeRestController(RestController):

    json = NodeJsonController()

    blog =  BlogRestController()

    @expose('nova.templates.node.index')
    def get_one(self, node_name):
        obj = DBSession.query(Node).filter(
                Node.key.like("%%%s%%" % node_name)).one()
        qr = QRCodeWidget(id="nodeqr", data=url("http://127.0.0.1/" + obj.key))

        tags = DBSession.query(Tag).all()

        revisions = DBSession.query(Revision).filter(Revision.item_id==obj.id).order_by('modified desc')

        get_revision_feed(obj)
        get_blog_posts_feed(obj)

        return dict(tags=tags, node=obj, qrcode=qr, revisions=revisions,
                    blog_link="/feeds/%s-blog.atom"%obj.key,
                    rev_link="/feeds/%s-revisions.atom"%obj.key
        )


    @expose('nova.templates.index')
    def get_all(self, *args, **kw):
        # must be the index
        latest_updates = DBSession.query(Node).order_by('modified desc')
        tags = DBSession.query(Tag).all()
        return dict(updates=latest_updates.limit(10), tags=tags)


    @expose('nova.templates.node.new')
    @require(predicates.not_anonymous(msg='Only logged in users can create nodes'))
    def new(self, *args, **kw):
        if len(kw) > 0:
            # TODO: if args came back, then validation failed. Need to restore all options here
            raise Exception, kw

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
            id = "tags_miu"

        class Submit(tw2.forms.SubmitButton):
            id = "submit_button"
            value = "Create!"

        return dict(_notags=True,
            name_form=NameForm(submit=None),
            desc_widget=DescriptionWidget(),
            tag_list=TagList(),
            sub_button=Submit(),
            )

    @validate( {'new_node_name': NotEmpty,
                'sel_type': NotEmpty, # need better validator here
                'new_node_key': Regex(regex='^[\w\-.]+$'), #need a DB validator here
                'description_miu': MarkupConverter}, error_handler=new)
    @expose()
    @require(predicates.not_anonymous(msg='Only logged in users can create nodes'))
    def post(self, **kw):
        from tg import request # HACK: Don't know why i need this here but i do

        attrs_list = dict((k[5-len(k):], v) for k, v in kw.iteritems() if k[0:5] == u'attr:')
  
        tags = distill(kw['tags_miu'])
        pic_links = distill(kw['node_def_images'])
        # Triple distilled tags

        n_type = DBSession.query(NodeType).filter(NodeType.key==kw['sel_type'].encode()).one()

        n = Node()
        n.node_type = n_type
        n.name = kw['new_node_name']
        n.key = kw['new_node_key']
        n.content = kw['description_miu']
        
        user = request.identity
        n.owner = user['user']

        for attr in attrs_list:
            vocab = DBSession.query(Vocab).filter(Vocab.key==attr).one()
            n.attrs.append(Attribute(vocab=vocab, value=attrs_list[attr]))

        for tag in tags:
            try:
                t_obj = DBSession.query(Tag).filter(Tag.name==tag).one()
            except NoResultFound:
                t_obj = Tag(name=tag)

            n.tags.append(t_obj)

        for pic in pic_links:
            try:
                p_obj = DBSession.query(ImageFile).filter(ImageFile.key==pic).one()
                n.pictures.append(p_obj)
            except:
                raise
                pass # Picture key doesnt exist, ignore it

        revise_and_commit(n, user['user']) # This is where the magic happens

        redirect("./node/"+kw['new_node_key'])
