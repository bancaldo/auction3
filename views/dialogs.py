import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from settings import IMG_PATH


ABOUT = """
<span foreground="blue" weight="bold">Auction 3.0</span>
by Bancaldo

<span weight="bold">Auction 3.0</span> 
is a simple app to manage a FantaLeague Auction.
When all auctions end, it is possible to export data to a csv file.

<b>packages:</b>
- Python 3.7.1
- <b>PyGObject</b> for Graphics
- <b>SQLAlchemy</b> for database and Object Ralation Mapping

<b>links:</b>
web-site: www.bancaldo.wordpress.com
web-site: www.bancaldo.altervista.org

last revision: Oct 23, 2020
author: bancaldo
"""


class InfoDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Custom Dialog", parent=parent)
        self.result = None
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.set_default_size(250, 100)
        image = Gtk.Image.new_from_file(IMG_PATH + "info.png")
        image.show()
        label = Gtk.Label()
        label.set_markup(ABOUT)
        box = self.get_content_area()
        box.set_spacing(15)
        box.add(image)
        box.add(label)
        self.show_all()


class WarningDialog(Gtk.Dialog):
    def __init__(self, parent, text):
        super().__init__(title="Warning", parent=parent)
        self.result = None
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(250, 100)
        image = Gtk.Image.new_from_file(IMG_PATH + "warning.png")
        image.show()
        label = Gtk.Label()
        label.set_markup(text)
        box = self.get_content_area()
        box.set_spacing(15)
        box.add(image)
        box.add(label)
        self.show_all()


class DeleteDialog(Gtk.Dialog):
    def __init__(self, parent, text=""):
        super().__init__(title="Attention", parent=parent)
        self.result = None
        self.add_buttons(Gtk.STOCK_YES, Gtk.ResponseType.YES,
                         Gtk.STOCK_NO, Gtk.ResponseType.NO)
        self.set_default_size(250, 100)
        image = Gtk.Image.new_from_file(IMG_PATH + "question.png")
        image.show()
        label = Gtk.Label()
        label.set_markup('Deleting <span foreground="blue">%s</span>...\n'
                         '<span foreground="red" weight="bold">Are you sure?'
                         '</span>' % text)
        box = self.get_content_area()
        box.set_spacing(15)
        box.add(image)
        box.add(label)
        self.show_all()
