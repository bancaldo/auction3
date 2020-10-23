import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Combo(Gtk.Window):
    def __init__(self, parent=None):
        if parent:
            self.controller = parent.controller
        title = "Edit number"
        super().__init__(title=title)
        self.set_default_size(300, 100)
        self.set_border_width(10)
        # Combobox
        self.combo_numbers = Gtk.ComboBoxText()
        self.combo_numbers.set_active(0)
        # self.combo_numbers.set_wrap_width(5)
        btn_close = Gtk.Button(label="QUIT")

        grid = Gtk.Grid()
        grid.attach(Gtk.Label(label="number"), left=0, top=0, width=1, height=1)
        grid.attach(self.combo_numbers, left=1, top=0, width=1, height=1)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(grid, False, True, 0)
        vbox.pack_start(btn_close, False, False, 0)
        self.add(vbox)

        # bindings
        btn_close.connect("clicked", self.on_close)
        self.combo_numbers.connect("scroll-event", self.combo_scrolling)
        self.fill_combo_numbers()

    def combo_scrolling(self, combobox, event):
        """Prevent the comboboxes from scrolling."""
        self.combo_numbers.emit_stop_by_name("scroll-event")

    def fill_combo_numbers(self):
        self.combo_numbers.remove_all()
        numbers = range(100)
        for number in numbers[:50]:
            self.combo_numbers.append_text(str(number))

    # noinspection PyUnusedLocal
    def on_close(self, button):
        self.destroy()


if __name__ == "__main__":
    win = Combo()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
