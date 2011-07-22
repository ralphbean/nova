# -*- coding: utf-8 -*-
"""Node Internal Blog REST controller module"""

# turbogears imports
from tg import expose, url, request
from tg import redirect, validate, flash
from tg import require

# third party imports
#from pylons.i18n import ugettext as _
from repoze.what import predicates

# project specific imports
from nova.lib.base import BaseController
from tg.controllers import RestController
from nova.model import DBSession, metadata, Node, Tag, BlogPost
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tw2.jqplugins.ui import ButtonWidget
import tw2.forms
import tw2.core
from tw2.tinymce import TinyMCE, MarkupConverter
from formencode.validators import NotEmpty, Regex
from tw2.jqplugins.tagify import Tagify


class BlogRestController(RestController):
    def __init__(self, *args, **kw):
        self.node_name = request.path.split('/')[-2]
        self.node = DBSession.query(Node).filter(
                Node.key.like("%%%s%%" % self.node_name)).one()


    @expose('nova.templates.node.blog.index')
    def get_one(self, name, *args, **kw):
        raise Exception, kw
        # TODO
        obj = DBSession.query(BlogPost).filter(
                Node.key.like("%%%s%%" % name)).one()

        tags = DBSession.query(Tag).all()
        return dict(tags=tags, blog=obj, node=self.node)


    @expose('nova.templates.node.blog.index_all')
    def get_all(self, *args, **kw):
        # must be the index
        latest_updates = DBSession.query(BlogPost).filter(BlogPost.node==self.node).order_by('modified desc')
        return dict(node=self.node,updates=latest_updates.limit(10))


    @expose('nova.templates.node.blog.new')
    @require(predicates.not_anonymous(msg='Only logged in users can create blog posts'))
    def new(self, *args, **kw):
        if len(kw) > 0:
            # TODO: if args came back, then validation failed. Need to restore all options here
            raise Exception, kw

        class BlogPostForm(tw2.forms.TableLayout):
            class NameField(tw2.forms.TextField):
                id = "post_name"
                label = "Title"
            
            class KeyField(tw2.forms.TextField):
                id = "post_slug"
                label = "Key"
    
            class DescriptionWidget(TinyMCE):
                id = "content_miu"
                rows = 20
                cols = 80

            class TagList(Tagify):
                id = "tag_miu"

            class Submit(tw2.forms.SubmitButton):
                id = "submit_button"
                value = "Create!"

        return dict(_notags=True,
            )


    @validate( {'post_name': NotEmpty,
                'post_slug': Regex(regex='^[\w\-.]+$'), #need a DB validator here
                'content_miu': MarkupConverter}, error_handler=new)
    @expose()
    @require(predicates.not_anonymous(msg='Only logged in users can create blog posts'))
    def post(self, **kw):
        tags = filter((lambda x: len(x) > 0), kw['tag_miu'].split(','))
        for i, tag in enumerate(tags):
            tags[i] = tag.strip()
        
        tags = [x for x in tags if len(x) is not 0]
        # Triple distilled tags

        b = BlogPost()
        # TODO: Fill rest of model

        from tg import request
        user = request.identity
        b.owner = user['user']
        b.attrs = attrs_list
        for tag in tags:
            try:
                t_obj = DBSession.query(Tag).filter(Tag.name==tag).one()
            except NoResultFound:
                t_obj = Tag(name=tag)

            b.tags.append(t_obj)

        import transaction

        DBSession.add(n)
        transaction.commit()

        redirect("./"+kw['post_slug'])
