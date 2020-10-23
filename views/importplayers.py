import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from gi.repository import GdkPixbuf
from settings import IMG_PATH


class ViewImportPlayers(Gtk.Window):
    def __init__(self, controller=None):
        super().__init__(title="Import Players")
        self.controller = controller
        self.count = 0  # used for progressbar timeout
        self.data = []  # used as list of lines for progressbar
        self.length = 0  # used as length parameter of txt file for progressbar
        self.line = ""  # used as line parameter for progressbar
        self.value = 0
        self.set_default_size(400, 100)
        self.set_border_width(10)
        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_text("Ready".format(self.value))
        self.progressbar.set_show_text(True)
        self.button = Gtk.Button(label=" Load players")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(IMG_PATH + "import.png")
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        self.button.set_always_show_image(True)
        self.button.set_image(image)
        # bindings
        self.button.connect("clicked", self.on_toggle)
        self.connect('delete-event', self.on_destroy)
        # layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.pack_start(self.button, True, True, 0)
        vbox.pack_start(self.progressbar, True, True, 0)
        self.add(vbox)

    # noinspection PyUnusedLocal
    def on_destroy(self, widget=None, *data):
        self.count = 1000  # high value to stop GLib on_timeout function
        self.controller.stop_import()
        print("WARNING: Stop importing players!")
        return False

    # noinspection PyUnusedLocal
    def on_toggle(self, button):
        dialog = Gtk.FileChooserDialog(title="Choose a file", parent=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OK, Gtk.ResponseType.OK)
        # add dialog filters
        for name, pattern in [("Text files", "*.txt*"), ("all files", "*.*")]:
            file_filter = Gtk.FileFilter()
            file_filter.set_name(name)
            file_filter.add_pattern(pattern)
            dialog.add_filter(file_filter)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            player_file = dialog.get_filename()
            with open(player_file) as input_file:
                self.data = [line.strip() for line in input_file if line]
                GLib.timeout_add(75, self.on_timeout, 1.0)
                self.length = len(self.data)  # imported MCC file length
                self.count = 0
                self.line = ""
        elif response == Gtk.ResponseType.CANCEL:
            print("INFO: aborted.")
        dialog.destroy()

    def on_timeout(self, new_value):
        try:
            message = "INFO: processing line %s: %s" % (self.count,
                                                        self.data[self.count])
            print(message)
            # qui chiamo il controller
            self.controller.on_import_players(self.data[self.count])
            if self.count < self.length - 1:
                self.value = self.progressbar.get_fraction() + \
                             new_value/self.length
                self.progressbar.set_text(message)
                self.progressbar.set_fraction(self.value)
                self.count += 1
                return True  # chiamo di nuovo la callback on_timeout
            else:
                self.button.set_label("Ready")
                self.value = 0
                self.progressbar.set_fraction(self.value)
                self.progressbar.set_text("Success!")
                return False  # fermo la chiamata alla callback
        except IndexError:
            return False


if __name__ == "__main__":
    win = ViewImportPlayers()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
