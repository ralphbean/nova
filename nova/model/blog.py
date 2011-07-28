# -*- coding: utf-8 -*-
"""Blog model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, String, Boolean
#from sqlalchemy.orm import relation, backref

from nova.model import DeclarativeBase, metadata, DBSession
from uuid import uuid4
from datetime import datetime

blog_tag_table = Table('blog_tag', metadata,
    Column('blog_id', String(36), ForeignKey('blog_items.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('tag_name', Unicode, ForeignKey('tags.name',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))

class BlogPost(DeclarativeBase):
    __tablename__ = 'blog_items'
    
    #{ Columns

    id = Column(String(36), primary_key=True, default=(lambda: str(uuid4())))
    
    node_id = Column(String(36), ForeignKey('node_model.id'), nullable=False)
    node = relation("Node", backref="blog_posts")

    name = Column(Unicode, nullable=False)
    key = Column(Unicode(255), nullable=False, unique=True)

    owner_id = Column(Integer, ForeignKey('tg_user.user_id'))
    owner = relation("User")

    content = Column(Unicode, nullable=False)

    modified = Column(DateTime, nullable=False, default=datetime.now)
    created = Column(DateTime, nullable=False, default=datetime.now)

    tags = relation("Tag", backref="blog_posts", secondary=blog_tag_table, uselist=True)
   
    draft = Column(Boolean)
    #}
