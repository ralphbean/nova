# -*- coding: utf-8 -*-
"""Setup the nova application"""

import logging
from tg import config
from nova import model

import transaction

from sqlalchemy.orm import scoped_session, sessionmaker, mapper
from sqlalchemy import MetaData, create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from nova.util import slugify

def get_id_gen():
    i = 1000
    while True:
        yield i
        i = i + 1

from uuid import uuid4

def get_guid_gen():
    while True:
        yield str(uuid4())


def bootstrap(command, conf, vars):
    """Place any commands to setup nova here"""
    # <websetup.bootstrap.before.auth
    from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'manager'
        u.display_name = u'Example manager'
        u.email_address = u'manager@somedomain.com'
        u.password = u'password'
    
        model.DBSession.add(u)
    
        g = model.Group()
        g.group_name = u'managers'
        g.display_name = u'Managers Group'
    
        g.users.append(u)
    
        model.DBSession.add(g)
    
        p = model.Permission()
        p.permission_name = u'manage'
        p.description = u'This permission give an administrative right to the bearer'
        p.groups.append(g)
   
        model.DBSession.add(p)
    
        u1 = model.User()
        u1.user_name = u'editor'
        u1.display_name = u'Example editor'
        u1.email_address = u'editor@somedomain.com'
        u1.password = u'editpass'
    
        model.DBSession.add(u1)
        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print 'Warning, there was a problem adding your auth data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'
        
#        model.DBSession.autoflush = False
#    try:
#        import csv
#        from json import loads
        # Import Vocab Table
#        csv_vocab = csv.reader(open("nova/websetup/vocab.csv"), quoting=csv.QUOTE_MINIMAL, quotechar="'", doublequote=True)
#        csv_vocab.next()
#        for k, n, d, default, r in csv_vocab:
#            v = model.Vocab()
#            v.key = k
#            v.name = n
#            v.description = d
#            v.default = default
#            v.resolve = True if r.lower() == "t" else False

#            model.DBSession.add(v)
        
#        model.DBSession.flush()
#        transaction.commit()

        # Import NodeType Tables
#        csv_types = csv.reader(open("nova/websetup/types.csv"), quoting=csv.QUOTE_MINIMAL, quotechar="'", doublequote=True)
#        csv_types.next()
#        for k, n, d, c, i, attrs in csv_types:
#            t = model.NodeType()
#            t.key =  k
#            t.name = n
#            t.description = d
#            t.creatable = True if c is "T" else False
#            t.icon = i
#            dec_attrs = loads(attrs)
#            for attr in dec_attrs:
#                try:
#                    t.req_attrs.append(model.DBSession.query(model.Vocab).filter(model.Vocab.key == attr).one())

#                except MultipleResultsFound:
#                    raise IntegrityError

#            model.DBSession.add(t)

#        model.DBSession.flush()  
#        transaction.commit()

        # Import sample nodes
#        csv_nodes = csv.reader(open("nova/websetup/nodes.csv"), quoting=csv.QUOTE_MINIMAL, quotechar="'", doublequote=True)
#        csv_nodes.next()

#        for k, n, t, d, o, a in csv_nodes:
#            try:
#                node = model.Node()
#                node.key = k
#                node.name = n
#                node.content = d
#                node.node_type = (model.DBSession.query(model.NodeType).filter(model.NodeType.key.like("%%%s%%"%t)).one())
#                node.owner = (model.DBSession.query(model.User).filter(model.User.user_name.like("%%%s%%"%o)).one())
#                node.editors.append(node.owner)

                # Fill in the gaps in our attribute information
#                imp_attrs = loads(a)
#                req_attrs = node.node_type.req_attrs
#                for attr in req_attrs:
#                    if attr.key not in imp_attrs:
#                        imp_attrs[attr.key] = attr.default
#                node.attrs = imp_attrs

#                from nova.util import revise_and_commit

#                revise_and_commit(node)                

#            except MultipleResultsFound:
#                raise IntegrityError

#            model.DBSession.flush()
#            transaction.commit()
           
#    except IntegrityError:
#        print 'Warning, there was a problem adding the NOVA data, it may have already been added:'
#        import traceback
#        print traceback.format_exc()
#        transaction.abort()
#        print 'Continuing with bootstrapping...'

    # <websetup.bootstrap.after.auth>

### Migrate old DB

    old_engine = create_engine("sqlite:///old.db")
    old_metadata = MetaData(bind=old_engine)

    OldSession = sessionmaker(bind=old_engine)
    OldDBSession = OldSession()

    ##### MIGRATE USERS

    class auth_user(object):
        pass
    t_old_users = Table("auth_user", old_metadata, autoload=True, autoload_with=old_engine)
    mapper(auth_user, t_old_users)


    class old_vocab(object):
        pass
    t_old_vocab = Table('vocab', old_metadata, autoload=True, autoload_with=old_engine)
    mapper(old_vocab, t_old_vocab)


    class old_node_type(object):
        pass
    t_old_nodetype = Table('nodetype', old_metadata, autoload=True, autoload_with=old_engine)
    mapper(old_node_type, t_old_nodetype)

    
    class old_node(object):
        pass
    t_old_node = Table('node', old_metadata, autoload=True, autoload_with=old_engine)
    mapper(old_node, t_old_node)


    old_metadata.reflect(bind=old_engine)
    OldDBSession.configure(bind=old_engine)

    ##### MIGRATE USERS

    old_users = t_old_users
    o_users = OldDBSession.query(old_users)

    user_translation = {}
    g = get_id_gen()

    for u in o_users:
        new_u = model.User(user_id=g.next())
        new_u.user_name = u.username
        new_u.password = "password"
        new_u.email_address = u.email
        new_u.display_name = u.first_name + " " + u.last_name

        print "Adding user: %s" % new_u.user_name

        model.DBSession.add(new_u)
        model.DBSession.flush()

        user_translation[str(u.id)] = new_u.user_id

        transaction.commit()


    ##### MIGRATE VOCAB
    old_vocab = t_old_vocab

    vocab_translation = {}

    o_vocab = OldDBSession.query(old_vocab)

    g = get_id_gen()

    for v in o_vocab:
        new_v = model.Vocab(id=g.next())
        new_v.key = slugify(v.value)
        new_v.name = v.value
        new_v.description = ""
        print "Adding vocab: '%s'" % new_v.name

        model.DBSession.add(new_v)
        model.DBSession.flush()

        vocab_translation[str(v.id)] = new_v.id
    
        transaction.commit()


    ##### MIGRATE NODETYPES
    old_nodetypes = t_old_nodetype
    
    nodetype_translation = {}

    o_nodetypes = OldDBSession.query(old_nodetypes)
    
    g = get_id_gen()

    for t in o_nodetypes:
        new_t = model.NodeType(id=g.next())
        new_t.key = slugify(t.value)
        new_t.name = t.value_node
        new_t.creatable = True #(True if t.public is 'T' else False)
        new_t.description = "" 
        old_v = t.required_vocab.encode().split('|')
        old_v = filter((lambda x: x is not ''), old_v)

        for v in old_v:
            voc = model.DBSession.query(model.Vocab).filter(model.Vocab.id==vocab_translation[v]).one()
            new_t.req_attrs.append(voc)
        
        model.DBSession.add(new_t)
        model.DBSession.flush()

        nodetype_translation[str(t.id)] = new_t.id

        transaction.commit()



    ##### MIGRATE NODES
    old_nodes = t_old_node

    node_translation = {}
    o_nodes = OldDBSession.query(old_node)

    g = get_guid_gen()

    for n in o_nodes:
        new_n = model.Node(id=g.next())
        new_n.key = slugify(n.url)
        new_n.name = n.name
        new_n.node_type = model.DBSession.query(model.NodeType).filter(model.NodeType.id==nodetype_translation[str(n.type)]).one()
        new_n.content = n.description
        new_n.owner = model.DBSession.query(model.User).filter(model.User.user_id==user_translation[str(n.modified_by)]).one()
        new_n.attrs = {}

        if n.tags is not None:
            old_t = n.tags.encode().split('|')
            old_t = filter((lambda x: x is not ''), old_t)

            for t in old_t:
                t = slugify(u'%s'%t)

                try:
                    t_obj = model.DBSession.query(model.Tag).filter(model.Tag.name==t).one()
                except NoResultFound:
                    t_obj = model.Tag(name=t)

                new_n.tags.append(t_obj)

        model.DBSession.add(new_n)

        try:
            model.DBSession.flush()

            transaction.commit()
        except IntegrityError:
            new_n.key = new_n.key + "_"

            model.DBSession.flush()
            transaction.commit()
