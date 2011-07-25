# -*- coding: utf-8 -*-
"""Node Internal Image REST controller module"""

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
from nova.model import DBSession, metadata, Node, ImageFile
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from tw2.jqplugins.ui import ButtonWidget
import tw2.forms
import tw2.core
from formencode.validators import NotEmpty, Regex, FileUploadKeeper
from nova.tw2.forms import NovaFormLayout
from nova.util import *

class ImageRestController(RestController):
    @expose()
    def get_one(self, name, *args, **kw):
        return dict()

    @expose()
    def get_all(self, *args, **kw):
        redirect("/")

    @expose('nova.templates.images.new')
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

            class FileField(tw2.forms.FileField):
                id = "image_file"
                label = "Image File"
            
            class Submit(tw2.forms.SubmitButton):
                id = "submit_button"
                label = "Create!"
                value = "Create!"

        return dict(_notags=True,form=BlogPostForm()
            )


    @validate( {'post_name': NotEmpty}, error_handler=new)
    @expose()
    @require(predicates.not_anonymous(msg='Only logged in users can upload images'))
    def post(self, **kw):
        raise Exception, kw
        from tg import request # HACK: Real wierd that I need this here. Possible TG2 Bug

        img = ImageFile()

        user = request.identity['user']
        b.owner = user

        revise_and_commit(b, user) # This is where the magic happens

        redirect("./"+key)
