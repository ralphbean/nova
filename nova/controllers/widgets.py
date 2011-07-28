# -*- coding: utf-8 -*-
"""Widget Injector controller module"""

# turbogears imports
from tg import expose, url
from tg import redirect, validate, flash

# third party imports
from pylons.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from nova.lib.base import BaseController
from nova.model import DBSession, Vocab
from tw2.qrcode import QRCodeWidget
from tw2.jqplugins.ui import TabsWidget
import tw2.jquery
import tw2.polymaps
import tw2.forms
import tw2.duckpunch

def BasicInputWidget(**kw):
    return tw2.duckpunch.Duckpunch(
        children=[tw2.forms.TableLayout(id='attr',
                children =[tw2.forms.TextField(
                    id = kw['name'] if 'name' in kw else 'textfield',
                    initial_value = kw['initial'] if 'initial' in kw else '',
                    label = kw['label'] if 'label' in kw else 'Text Field',
                    css_class = "ui-corner-all ui-widget-content",)
                    ]
            )]
        )

def PolyMapWidget(**kw):
    class PolyMapPunch(tw2.duckpunch.Duckpunch):
        class PMap(tw2.polymaps.PolyMap):
            id = kw['name'] if 'name' in kw else 'polymap'
            interact = False
            # You should get your own one of these at http://cloudmade.com/register
            cloudmade_api_key = "1a1b06b230af4efdbb989ea99e9841af"
            # To style the map tiles
            cloudmade_tileset = 'pale-dawn'
            # Both specify the css_class AND include your own custom css file that
            # specifies what it looks like.
        class LocPoint(tw2.forms.HiddenField):
            name = "attr:"+kw['name'] if 'name' in kw else 'textfield'
            initial_value = kw['initial'] if 'initial' in kw else ''
    return PolyMapPunch()


class WidgetPuncher(object):

    @expose('nova.templates.widgets.full')
    def default(self, *args, **kw):
        try:
            obj = DBSession.query(Vocab).filter(Vocab.key==args[0]).one()
        except:
            return ""
        kw['label'] = obj.name
        return dict(title=obj.name, desc=obj.description, w=BasicInputWidget(**kw), additional="_50")

    @expose('nova.templates.widgets.full')
    def location(self, **kw):
        obj = DBSession.query(Vocab).filter(Vocab.key=='location').one()
        return dict(title=obj.name, desc=obj.description, w=PolyMapWidget(**kw))

    @expose('nova.templates.widgets.full')
    def polymap(self, **kw):
        return dict(title="PolyMap PunchTest", w=PolyMapWidget(**kw))

widget_puncher = WidgetPuncher()


class WidgetController(BaseController):

    @expose()
    def _lookup(self, name, *kw):
        _kw = list(kw)
        _kw.insert(-1, name)
        
        return widget_puncher, _kw
