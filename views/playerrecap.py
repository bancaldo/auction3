import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango


class ViewPlayerRecap(Gtk.Window):
    def __init__(self, team_list):
        super().__init__(title="Players recap")
        self.set_border_width(10)
        # self.current_filter_role = None

        bbox = Gtk.HButtonBox()
        rb1 = Gtk.RadioButton.new_with_label_from_widget(None, "Goalkeeper")
        rb2 = Gtk.RadioButton.new_with_label_from_widget(rb1, "Defender")
        rb3 = Gtk.RadioButton.new_with_label_from_widget(rb1, "Midfielder")
        rb4 = Gtk.RadioButton.new_with_label_from_widget(rb1, "Forward")
        bbox.add(rb1)
        bbox.add(rb2)
        bbox.add(rb3)
        bbox.add(rb4)
        frame = Gtk.Frame(label="roles", label_xalign=0.5)
        frame.add(bbox)

        # Creo il ListStore model
        self.player_liststore = Gtk.ListStore(int, str, str, int, int, str)
        if team_list:
            for team in team_list:
                self.player_liststore.append(list(team))
        # Creo il model filter associandolo al liststore model
        self.role_filter = self.player_liststore.filter_new()

        # creo il treeview ed uso il filter come model
        self.treeview = Gtk.TreeView.new_with_model(
            Gtk.TreeModelSort(model=self.role_filter))
        # creo le colonne
        for i, column_title in enumerate(["code", "name", "real team",
                                          "value", "cost", "Fanta Team"]):
            renderer = Gtk.CellRendererText()
            if i == 0:
                renderer.props.weight_set = True
                renderer.props.weight = Pango.Weight.BOLD
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sort_column_id(i)
            self.treeview.append_column(column)
        # bindings
        self.treeview.connect("row-activated", self.on_select_row)
        rb1.connect("toggled", self.on_button_toggled)
        rb2.connect("toggled", self.on_button_toggled)
        rb3.connect("toggled", self.on_button_toggled)
        rb4.connect("toggled", self.on_button_toggled)
        # layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox.pack_start(frame, True, True, 0)
        vbox.pack_start(self.treeview, True, True, 0)
        self.add(vbox)

    # noinspection PyUnusedLocal
    @ staticmethod
    def on_select_row(tree_view, path, column):
        print("INFO: <%s> selected!" % tree_view.get_model()[path][0])

    @ staticmethod
    def on_button_toggled(button):
        if button.get_active():
            print("role {} selected".format(button.get_label()))
