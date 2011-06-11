# -*- coding: utf-8 -*-
"""Setup the nova application"""

import logging
from tg import config
from nova import model

import transaction


def bootstrap(command, conf, vars):
    """Place any commands to setup nova here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = u'manager'
        u.display_name = u'Example manager'
        u.email_address = u'manager@somedomain.com'
        u.password = u'managepass'
    
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
        
    try:
        import csv
        csv_vocab = csv.reader(open("nova/websetup/vocab.csv"), quoting=csv.QUOTE_MINIMAL, quotechar='"')
        csv_vocab.next()
        for k, n, d in csv_vocab:
            v = model.Vocab()
            v.key = k
            v.name = n
            v.description = d

            model.DBSession.add(v)

        model.DBSession.flush()        
        transaction.commit()

    except IntegrityError:
        print 'Warning, there was a problem adding your vocab data, it may have already been added:'
        import traceback
        print traceback.format_exc()
        transaction.abort()
        print 'Continuing with bootstrapping...'

    # <websetup.bootstrap.after.auth>
