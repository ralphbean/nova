# -*- coding: utf-8 -*-
"""Node model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relationship
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation, backref

from nova.model import DeclarativeBase, metadata, DBSession

import json
from datetime import datetime
from uuid import uuid4

vocab_nodetype_table = Table('vocab_nodetype_table', metadata,
    Column('vocab_id', Integer, ForeignKey('vocab_model.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('nodetype_id', Integer, ForeignKey('nodetype_model.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))

node_editor_table = Table('nodeeditor_tg_user', metadata,
    Column('node_id', String(36), ForeignKey('node_model.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('user_id', Integer, ForeignKey('tg_user.user_id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))

node_tag_table = Table('node_tag', metadata,
    Column('node_id', String(36), ForeignKey('node_model.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('tag_name', Unicode, ForeignKey('tags.name',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))

node_pic_table = Table('node_picture_links', metadata,
    Column('node_id', String(36), ForeignKey('node_model.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('image_id', String(36), ForeignKey('images.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))


class Vocab(DeclarativeBase):
    '''An object defining an node attribute'''
    __tablename__ = 'vocab_model'

    #{ Columns
    id = Column(Integer, primary_key=True)

    key = Column(Unicode(255), nullable=False, unique=True)
    name = Column(Unicode(255), nullable=False)

    description = Column(Unicode, nullable=True)

    default = Column(Unicode, nullable=True)

    resolve = Column(Boolean)
    #}

class NodeType(DeclarativeBase):
    '''An object defining a node'''
    __tablename__ = 'nodetype_model'
    
    #{ Columns

    id = Column(Integer, primary_key=True)
    key = Column(Unicode(255), nullable=False, unique=True)

    name = Column(Unicode, nullable=False)
    description = Column(Unicode, nullable=True)
    creatable = Column(Boolean)

    icon = Column(Unicode(255), nullable=True)

    req_attrs = relation('Vocab', secondary=vocab_nodetype_table, uselist=True)
    #}


class Node(DeclarativeBase):
    '''An object describing an item in the NOVA'''
    __tablename__ = 'node_model'
    
    #{ Columns
    
    id = Column(String(36), primary_key=True, default=lambda : str(uuid4()))

    node_type_id = Column(Integer, ForeignKey('nodetype_model.id'), nullable=False)
    node_type = relationship("NodeType")

    name = Column(Unicode, nullable=False)
    key = Column(Unicode(255), nullable=False, unique=True)

    owner_id = Column(Integer, ForeignKey('tg_user.user_id'))
    owner = relationship("User") 

    pictures = relationship("ImageFile", backref="linked_to", secondary=node_pic_table, uselist=True)
    attrs = Column(PickleType(pickler=json), nullable=True)

    content = Column(Unicode, nullable=True)

    modified = Column(DateTime, nullable=False, default=datetime.now)
    created = Column(DateTime, nullable=False, default=datetime.now)

    tags = relationship("Tag", backref="nodes", secondary=node_tag_table, uselist=True)

    #revisions = relationship("Revision", backref="node")

    editors = relationship('User', backref="editing", secondary=node_editor_table, uselist=True)

    #}

class Tag(DeclarativeBase):
    __tablename__ = "tags"

    name = Column(Unicode, primary_key=True)

    @property
    # TODO: SLOPPY
    def count(self):
        if not hasattr(self, "_count"):
            n_list = node_tag_table.count(node_tag_table.c.tag_name==str(self.name))
            self._count =  len(DBSession.execute(n_list).fetchall()) 
        return self._count


class NodeWatch(DeclarativeBase):
    __tablename__ = "node_watch"
    id = Column(String(36), primary_key=True, default=lambda : str(uuid4()))

    watched_by_id = Column("watched_by_id", String(36), ForeignKey("node_model.id"))
    watched_by = relationship("Node", backref="watching",  primaryjoin=(Node.id == watched_by_id))
    watched_id = Column("watch_id", String(36), ForeignKey("node_model.id"))
    watched = relationship("Node", backref="watched_by",  primaryjoin=(Node.id == watched_id))


class Revision(DeclarativeBase):
    '''An object containing information about a modification done to a node'''
    __tablename__ = 'revision_model'
    
    #{ Columns

    id = Column(String(36), primary_key=True, default=lambda : str(uuid4()))

    item_id = Column(String(36), nullable=False)
    
    title = Column(Unicode(255), nullable=False)

    content = Column(Unicode)

    diff_cache = Column(Unicode)

    modified = Column(DateTime, nullable=False, default=datetime.now)

    #}
