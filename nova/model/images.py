# -*- coding: utf-8 -*-
"""Image model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, String, Boolean
#from sqlalchemy.orm import relation, backref

from nova.model import DeclarativeBase, metadata, DBSession
from uuid import uuid4
from datetime import datetime

class ImageFile(DeclarativeBase):
    __tablename__ = 'images'
    
    #{ Columns

    id = Column(String(36), primary_key=True, default=(lambda: str(uuid4())))
    
    name = Column(Unicode, nullable=False)
    key = Column(Unicode(255), nullable=False, unique=True)

    owner_id = Column(Integer, ForeignKey('tg_user.user_id'))
    owner = relation("User")

    image_path = Column(Unicode, nullable=False)

    modified = Column(DateTime, nullable=False, default=datetime.now)
    created = Column(DateTime, nullable=False, default=datetime.now)

    #}
