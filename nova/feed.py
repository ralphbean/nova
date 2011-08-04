import os

from webhelpers.feedgenerator import Atom1Feed

from nova.model import DBSession
from nova.model.node import Node, Revision

def generate_blog_feed_from_node(node):
    node_name = node.name
    feed = Atom1Feed(
            title=node_name,
            link='/path/to/%s' % node_name,
            description='',
            language=u'en',
            updated=node.modified,
    )

    for entry in node.blog_posts:
        feed.add_item(
                title=entry.name,
                link ='',
                description='',
        )

    feed_xml = file(os.path.join('nova/public/feeds/', node_name), 'w')
    feed_xml.write(feed.writeString('utf-8'))
    feed_xml.close()
    print("Wrote %s" % feed_xml)


def generate_revision_feed_from_node(node):
    node_name = node.name
    feed = Atom1Feed(
            title="Revision history of %s" % node_name,
            link='/path/to/%s' % node_name,
            description='',
            language=u'en',
            updated=node.modified,
    )

    revisions = DBSession.query(Revision).filter_by(item_id=node.id).order_by(Revision.modified.desc())
    for entry in revisions:
        feed.add_item(
                title=entry.name,
                link ='',
                description='',
        )

    feed_xml = file(os.path.join('nova/public/feeds/', node_name), 'w')
    feed_xml.write(feed.writeString('utf-8'))
    feed_xml.close()
    print("Wrote %s" % feed_xml)


if __name__ == "__main__":
    node = Node()
    node.name = "Example node"
    generate_blog_feed_from_node(node)
    generate_revision_feed_from_node(node)
