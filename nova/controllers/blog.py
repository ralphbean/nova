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
from nova.tw2.forms import NovaFormLayout
from nova.util import *

class BlogRestController(RestController):
    @expose('nova.templates.blog.index')
    def get_one(self, name, *args, **kw):
        node_name = request.path.split('/')[2]
        node = DBSession.query(Node).filter(Node.key.like("%%%s%%" % node_name)).one()
        
        obj = DBSession.query(BlogPost).filter(
                BlogPost.node==node).filter(
                BlogPost.key.like("%%%s%%" % name)).one()

        tags = DBSession.query(Tag).all()
        return dict(tags=tags, blog=obj)


    @expose('nova.templates.blog.index_all')
    def get_all(self, *args, **kw):
        # must be the index
        node_name = request.path.split('/')[2]
        node = DBSession.query(Node).filter(Node.key.like("%%%s%%" % node_name)).one()

        latest_posts = DBSession.query(BlogPost).filter(
                        BlogPost.node==node).order_by('modified desc')

        return dict(node=node, updates=latest_posts)


    @expose('nova.templates.blog.new')
    @require(predicates.not_anonymous(msg='Only logged in users can create blog posts'))
    def new(self, *args, **kw):
        node_name = request.path.split('/')[2]
        if len(kw) > 0:
            # TODO: if args came back, then validation failed. Need to restore all options here
            raise Exception, kw

        class BlogPostForm(NovaFormLayout):
            class NameField(tw2.forms.TextField):
                id = "post_name"
                label = "Title"
            
            class DescriptionWidget(TinyMCE):
                id = "content_miu"
                label = "Content"
                rows = 20
                cols = 80

            class TagList(Tagify):
                label = "Tags"
                id = "tag_miu"

            class Submit(tw2.forms.SubmitButton):
                id = "submit_button"
                label = "Create!"
                value = "Create!"

        return dict(_notags=True,form=BlogPostForm()
            )


    @validate( {'post_name': NotEmpty,
                #'post_slug': Regex(regex='^[\w\-.]+$'), #need a DB validator here
                'content_miu': MarkupConverter}, error_handler=new)
    @expose()
    @require(predicates.not_anonymous(msg='Only logged in users can create blog posts'))
    def post(self, **kw):
        from tg import request # HACK: Real wierd that I need this here. Possible TG2 Bug
        node_name = request.path.split('/')[2]
        tags = filter((lambda x: len(x) > 0), kw['tag_miu'].split(','))
        for i, tag in enumerate(tags):
            tags[i] = tag.strip()
        
        tags = [x for x in tags if len(x) is not 0]
        # Triple distilled tags
        
        node = DBSession.query(Node).filter(Node.key.like("%%%s%%" % node_name)).one()

        b = BlogPost()
        key = gen_key_blogpost(node_name, kw['post_name'])
        b.key = key
        b.name = kw['post_name']
        b.content = kw['content_miu']
        b.node = node

        user = request.identity['user']
        b.owner = user

        for tag in tags:
            try:
                t_obj = DBSession.query(Tag).filter(Tag.name==tag).one()
            except NoResultFound:
                t_obj = Tag(name=tag)

            b.tags.append(t_obj)

        revise_and_commit(b, user) # This is where the magic happens

        redirect("./"+key)
