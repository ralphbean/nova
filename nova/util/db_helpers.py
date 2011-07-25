import re
from nova.model import DBSession, Node, BlogPost, Revision
from unicodedata import normalize
from nova.util.htmldiff import text_diff

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')

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
    key = item.id
    item_cls = item.__class__
    try:
        old_item = DBSession.query(item_cls).filter(item_cls.id==key).one()
    except:
        old_item = None # This may be a new item so there wont be an old object

    revision = Revision()
    revision.item_id = key
    revision.content = item.content

    item.modified = revision.modified = datetime.now()
    revision.item_id = item.id

    revision.title = (user.display_name+" " if user else '') + "Modified content"
    if old_item:
        revision.diff_cache = text_diff(old_item.content, item.content)
    else:
        revision.diff_cache = text_diff("", item.content)

    DBSession.add(item)
    DBSession.add(revision)
    DBSession.flush()
    transaction.commit()