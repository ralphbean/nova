import os
from webhelpers.feedgenerator import Atom1Feed
from nova.model import DBSession, Node, Revision

def get_blog_posts_feed(node):
    feed_file = os.path.join('nova/public/feeds', "%s-blog.atom" % node.key)
    if not os.path.exists(feed_file):
        return generate_blog_feed_from_node(node)
    else:
        return feed_file

def generate_blog_post_feed(node):
    node_name = node.key
    feed = Atom1Feed(
            title=node.name,
            link='/node/%s/blog' % node_name,
            description="Feed for the %s blog." % node.name,
            language=u'en',
            updated=node.modified,
    )

    for entry in node.blog_posts:
        feed.add_item(
                title=entry.name,
                link ='/node/%s/blog/%s' % (node_name, entry.key),
                description=entry.content,
        )

    feed_file = os.path.join('nova/public/feeds/', "%s-blog.atom" % node_name)
    feed_xml = file(feed_file, 'w')
    feed_xml.write(feed.writeString('utf-8'))
    feed_xml.close()
    print("Wrote %s" % feed_xml)

    return feed_file

def generate_node_revision_feed(node):
    node_name = node.name
    feed = Atom1Feed(
            title="Revision history of %s" % node_name,
            link='/node/%s' % node_name,
            description='',
            language=u'en',
            updated=node.modified,
    )

    revisions = DBSession.query(Revision).filter(Revision.item_id==node.id).order_by(Revision.modified.desc())
    for entry in revisions:
        feed.add_item(
                title=entry.title,
                link ='',
                description=entry.title,
        )

    feed_file = os.path.join('nova/public/feeds/',"%s-revisions.atom" % node_name)
    feed_xml = file(os.path.join('nova/public/feeds/', node_name), 'w')
    feed_xml.write(feed.writeString('utf-8'))
    feed_xml.close()
    print("Wrote %s" % feed_xml)

    return feed_file
