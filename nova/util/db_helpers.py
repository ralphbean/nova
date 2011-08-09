import re
from nova.model import DBSession, Node, BlogPost, Revision, ImageFile
from unicodedata import normalize
from nova.util.htmldiff import text_diff
from uuid import uuid4 
from nova.util.feed_helpers import *

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^`{|},.]+')

def slugify(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))

def gen_key_node(name):
    base_key = slugify(name)
    key = base_key
    i = 1
    try:
        while DBSession.query(Node).filter(Node.key.like("%%%s%%" % key)).one():
            key = u'%s_%i' % (base_key, i)
            i = i + 1
    except:
        pass # we want this to happen

    return key

def gen_key_image(name):
    base_key = slugify(name)
    key = base_key
    i = 1
    try:
        while DBSession.query(ImageFile).filter(ImageFile.key.like("%%%s%%" % key)).one():
            key = u'%s_%i' % (base_key, i)
            i = i + 1
    except:
        pass # we want this to happen

    return key


def gen_key_blogpost(node, name):
    base_key = slugify(name)
    key = base_key
    i = 1
    try:
        while DBSession.query(BlogPost).filter(
                Node.key.like("%%%s%%" % node)).filter(
                BlogPost.key.like("%%%s%%" % key)).one():
            key = u'%s_%i' % (base_key, i)
            i = i + 1
    except:
        pass # we want this to happen

    return key

from datetime import datetime
import transaction


def revise_and_commit(item, user=None):
    item_cls = item.__class__
    try:
        old_item = DBSession.query(item_cls).filter(item_cls.id==key).one()
        key = old_item.id
    except:
        old_item = None # This may be a new item so there wont be an old object
        key = str(uuid4())

    revision = Revision()
    revision.item_id = key
    revision.content = item.content

    item.modified = revision.modified = datetime.now()

    revision.title = (user.display_name+" " if user else '') + "Modified content"
    if old_item:
        revision.diff_cache = text_diff(old_item.content, item.content)
    else:
        revision.diff_cache = text_diff("", item.content)

    DBSession.add(item)
    DBSession.add(revision)
    DBSession.flush()

    if item_cls is Node:
        generate_node_revision_feed(item)
    elif item_cls is BlogPost:
        generate_blog_post_feed(item.node)

    transaction.commit()
