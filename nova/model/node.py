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

class Vocab(DeclarativeBase):
    __tablename__ = 'vocab_model'

    #{ Columns
    id = Column(Integer, primary_key=True)

    key = Column(Unicode(255), nullable=False)
    name = Column(Unicode(255), nullable=False)

    description = Column(Unicode, nullable=True)

    #}

class NodeTypeModel(DeclarativeBase):
    __tablename__ = 'nodetype_model'
    
    #{ Columns

    id = Column(Integer, primary_key=True)

    name = Column(Unicode, nullable=False)

    icon = Column(Unicode(255), nullable=True)

    required_attrs = Column(PickleType(pickler=json), nullable=True)

    #}


class NodeModel(DeclarativeBase):
    __tablename__ = 'node_model'
    
    #{ Columns
    
    id = Column(Integer, primary_key=True)

    node_type_id = Column(Integer, ForeignKey('nodetype_model.id'))
    node_type = relationship("NodeTypeModel", backref=backref("NodeModel", uselist=False))

    name = Column(Unicode, nullable=False)
    short_name = Column(Unicode(255), nullable=False)
    #owner = Column()
 
    picture = Column(Unicode, nullable=True)
    attrs = Column(PickleType(pickler=json), nullable=True)

    description = Column(Unicode, nullable=True)

    modified = Column(DateTime, nullable=False, default=datetime.now)
    created = Column(DateTime, nullable=False, default=datetime.now)

    tags = Column(PickleType(pickler=json), nullable=True)

    revisions = relationship("NodeRevisionModel", backref="node_model")
    #}

class NodeRevisionModel(DeclarativeBase):
    __tablename__ = 'revision_model'
    
    #{ Columns

    id = Column(Integer, primary_key=True)

    node_id = Column(Integer, ForeignKey('node_model.id'))
    
    description = Column(Unicode(255), nullable=False)

    modified = Column(DateTime, nullable=False, default=datetime.now)

    #}
