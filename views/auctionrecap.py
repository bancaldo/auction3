import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from views.team import ViewTeam


class ViewAuctionRecap(Gtk.Window):
    def __init__(self, parent):
        super().__init__(title="Auction Recap")
        self.controller = parent.controller
        self.set_border_width(10)
        # self.current_filter_role = None

        # Creo il ListStore model
        self.player_liststore = Gtk.ListStore(str, int, int, int, int, int, int)
        teams = self.controller.get_teams()
        if teams:
            for team in teams:
                self.player_liststore.append(list(team))
        # Creo il model filter associandolo al liststore model
        self.role_filter = self.player_liststore.filter_new()

        # creo il treeview ed uso il filter come model
        self.treeview = Gtk.TreeView.new_with_model(
            Gtk.TreeModelSort(model=self.role_filter))
        # creo le colonne
        for i, column_title in enumerate(["Team", "Budget", "Trades",
                                          "Remaining GK", "Remaining DEF",
                                          "Remaining MF", "Remaining FOR"]):
            renderer = Gtk.CellRendererText()
            if i == 0:
                renderer.props.weight_set = True
                renderer.props.weight = Pango.Weight.BOLD
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sort_column_id(i)
            self.treeview.append_column(column)
        # bindings
        self.treeview.connect("row-activated", self.on_select_row)
        # layout
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.add(hbox)
        hbox.pack_start(self.treeview, True, True, 0)

    # noinspection PyUnusedLocal
    def on_select_row(self, tree_view, path, column):
        team_name = tree_view.get_model()[path][0]
        print("INFO: <%s> selected!" % team_name)
        child_win = ViewTeam(parent=self, edit=True, team_name=team_name)
        child_win.set_modal(True)
        child_win.show_all()
