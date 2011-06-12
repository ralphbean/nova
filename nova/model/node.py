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

vocab_nodetype_table = Table('vocab_nodetype_table', metadata,
    Column('vocab_id', Integer, ForeignKey('vocab_model.id',
        onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('nodetype_id', Integer, ForeignKey('nodetype_model.id',
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

    icon = Column(Unicode(255), nullable=True)

    req_attrs = relation('Vocab', secondary=vocab_nodetype_table, uselist=True)
    #}


class Node(DeclarativeBase):
    '''An object describing an item in the NOVA'''
    __tablename__ = 'node_model'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)

    node_type_id = Column(Integer, ForeignKey('nodetype_model.id'))
    node_type = relationship("NodeType")

    name = Column(Unicode, nullable=False)
    key = Column(Unicode(255), nullable=False, unique=True)

    owner_id = Column(Integer, ForeignKey('tg_user.user_id'))
    owner = relationship("User") 

    picture = Column(Unicode, nullable=True)
    attrs = Column(PickleType(pickler=json), nullable=True)

    description = Column(Unicode, nullable=True)

    modified = Column(DateTime, nullable=False, default=datetime.now)
    created = Column(DateTime, nullable=False, default=datetime.now)

    tags = Column(PickleType(pickler=json), nullable=True)

    revisions = relationship("NodeRevision", backref="node")
    #}

class NodeRevision(DeclarativeBase):
    '''An object containing information about a modification done to a node'''
    __tablename__ = 'revision_model'
    
    #{ Columns

    id = Column(Integer, primary_key=True)

    node_id = Column(Integer, ForeignKey('node_model.id'))
    
    description = Column(Unicode(255), nullable=False)

    modified = Column(DateTime, nullable=False, default=datetime.now)

    #}
