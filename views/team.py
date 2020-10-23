import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango
from views.dialogs import WarningDialog, DeleteDialog
from settings import BUDGET, TRADES
from settings import GOALKEEPER, DEFENDERS, MIDFIELDERS, FORWARDS
from views.player import ViewPlayer


class ViewTeam(Gtk.Window):
    def __init__(self, parent=None, edit=True, team_name=None):
        self.edit = edit
        if parent:
            self.controller = parent.controller
        title = "Edit Team" if self.edit else "New Team"
        super().__init__(title=title)
        self.set_default_size(300, 300)
        self.set_border_width(10)

        self.fantateam_combo = Gtk.ComboBoxText()
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Team Name")
        self.budget_entry = Gtk.Entry()
        # self.budget_entry.set_placeholder_text("Team Budget")
        self.trades_entry = Gtk.Entry()
        self.max_gk_entry = Gtk.Entry()
        self.max_def_entry = Gtk.Entry()
        self.max_mf_entry = Gtk.Entry()
        self.max_for_entry = Gtk.Entry()
        if not self.edit:
            self.budget_entry.set_text(str(BUDGET))
            self.trades_entry.set_text(str(TRADES))
            self.max_gk_entry.set_text(str(GOALKEEPER))
            self.max_def_entry.set_text(str(DEFENDERS))
            self.max_mf_entry.set_text(str(MIDFIELDERS))
            self.max_for_entry.set_text(str(FORWARDS))
        else:
            if team_name:
                self.fill_data(team_name)

        # Role Box
        self.bbox = Gtk.VButtonBox()
        rb1 = Gtk.RadioButton.new_with_label_from_widget(None, "Goalkeeper")
        rb2 = Gtk.RadioButton.new_with_label_from_widget(rb1, "Defender")
        rb3 = Gtk.RadioButton.new_with_label_from_widget(rb1, "Midfielder")
        rb4 = Gtk.RadioButton.new_with_label_from_widget(rb1, "Forward")
        self.bbox.add(rb1)
        self.bbox.add(rb2)
        self.bbox.add(rb3)
        self.bbox.add(rb4)
        frm = Gtk.Frame(label="roles", label_xalign=0.5)
        frm.add(self.bbox)
        # Recap Players
        self.player_liststore = Gtk.ListStore(int, str, str, str, int, int)
        # Creo il model filter associandolo al liststore model
        self.role_filter = self.player_liststore.filter_new()

        # creo il treeview ed uso il filter come model
        self.treeview = Gtk.TreeView.new_with_model(
            Gtk.TreeModelSort(model=self.role_filter))
        # creo le colonne
        for i, column_title in enumerate(["code", "Name", "role", "Real Team",
                                          "value", "Auction value"]):
            renderer = Gtk.CellRendererText()
            if i == 0:
                renderer.props.weight_set = True
                renderer.props.weight = Pango.Weight.BOLD
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sort_column_id(i)
            self.treeview.append_column(column)

        # Buttons
        btn_save = Gtk.Button(label="SAVE")
        btn_close = Gtk.Button(label="QUIT")
        self.btn_delete = Gtk.Button(label="DELETE")
        self.btn_delete.set_sensitive(False)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox.pack_start(btn_save, True, True, 0)
        hbox.pack_start(self.btn_delete, True, True, 0)
        hbox.pack_start(btn_close, True, True, 0)

        grid = Gtk.Grid()
        if self.edit:
            grid.attach(Gtk.Label(label="Team"), left=0, top=0, width=1,
                        height=1)
            grid.attach(self.fantateam_combo, left=1, top=0, width=1, height=1)
            teams = self.controller.get_team_names()
            self.fill_combo(teams, self.fantateam_combo)

        grid.attach(Gtk.Label(label="name"), left=0, top=1, width=1, height=1)
        grid.attach(Gtk.Label(label="budget"), left=0, top=2, width=1, height=1)
        grid.attach(Gtk.Label(label="max trades"), left=0, top=3, width=1,
                    height=1)
        grid.attach(Gtk.Label(label="total GoalKeepers"), left=0, top=4,
                    width=1, height=1)
        grid.attach(Gtk.Label(label="total Defenders"), left=0, top=5, width=1,
                    height=1)
        grid.attach(Gtk.Label(label="total MidFielders"), left=0, top=6,
                    width=1, height=1)
        grid.attach(Gtk.Label(label="total Forwards"), left=0, top=7, width=1,
                    height=1)
        grid.attach(self.name_entry, left=1, top=1, width=1, height=1)
        grid.attach(self.budget_entry, left=1, top=2, width=1, height=1)
        grid.attach(self.trades_entry, left=1, top=3, width=1, height=1)
        grid.attach(self.max_gk_entry, left=1, top=4, width=1, height=1)
        grid.attach(self.max_def_entry, left=1, top=5, width=1, height=1)
        grid.attach(self.max_mf_entry, left=1, top=6, width=1, height=1)
        grid.attach(self.max_for_entry, left=1, top=7, width=1, height=1)
        if self.edit:
            grid.attach(frm, left=0, top=8, width=2, height=1)
            grid.attach(self.treeview, left=0, top=9, width=2, height=1)
        grid.set_column_homogeneous(True)
        # grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(grid, False, True, 0)
        vbox.pack_start(hbox, False, False, 0)
        self.add(vbox)

        # bindings
        btn_save.connect("clicked", self.on_save)
        btn_close.connect("clicked", self.on_close)
        self.btn_delete.connect("clicked", self.on_delete)
        self.fantateam_combo.connect('changed', self.on_team)
        for radiobutton in (rb1, rb2, rb3, rb4):
            radiobutton.connect("toggled", self.on_role)
        self.treeview.connect("row-activated", self.on_select_row)

    def on_role(self, button):
        if button.get_active():
            team_name = self.name_entry.get_text().upper()
            role = button.get_label().lower()
            self.fill_players(team_name, role)

    # noinspection PyUnusedLocal
    def on_team(self, widget):
        role = "goalkeeper"
        for rb in self.bbox.get_children():
            if rb.get_active():
                role = rb.get_label().lower()
        team_name = self.fantateam_combo.get_active_text()
        if team_name:
            team = self.controller.get_team(team_name)
            self.controller.set_temporary_object(team)
            self.name_entry.set_text(team.name)
            self.budget_entry.set_text(str(team.budget))
            self.trades_entry.set_text(str(team.max_trades))
            self.max_gk_entry.set_text(str(team.max_goalkeepers))
            self.max_def_entry.set_text(str(team.max_defenders))
            self.max_mf_entry.set_text(str(team.max_midfielders))
            self.max_for_entry.set_text(str(team.max_forwards))
            print("INFO: <%s> selected" % team.name)
            self.fill_players(team.name, role)
            self.btn_delete.set_sensitive(True)

    def fill_players(self, team_name, role=None):
        """Fill the treeview players with fanta team players filtered by role"""
        self.player_liststore.clear()
        players = self.controller.get_team_player_data(team_name, role)
        if players:
            for player in players:
                self.player_liststore.append(list(player))

    # noinspection PyUnusedLocal
    def on_save(self, button):
        """Callback bound to SAVE button"""
        # we have to use temporary objects to change the selected object which
        # is selected by name.
        name = self.name_entry.get_text()
        budget = self.budget_entry.get_text()
        max_trades = self.trades_entry.get_text()
        max_gk = self.max_gk_entry.get_text()
        max_def = self.max_def_entry.get_text()
        max_mf = self.max_mf_entry.get_text()
        max_for = self.max_for_entry.get_text()
        try:
            data = {'name': name.upper(), 'budget': int(budget),
                    'max_trades': int(max_trades),
                    'max_gk': int(max_gk), 'max_def': int(max_def),
                    'max_mf': int(max_mf), 'max_for': int(max_for)}
            if self.edit:
                self.controller.update_team(data)
                teams = self.controller.get_team_names()
                self.fill_combo(teams, self.fantateam_combo)
                self.clean_fields()
            else:
                if self.controller.get_team(name.upper()):
                    self.info_message('Team <span foreground="red" '
                                      'weight="bold">'
                                      '%s</span> already exists!' % name)
                else:
                    if name and budget and max_trades and max_gk and max_def \
                            and max_mf and max_for:
                        self.controller.new_team(data=data)
                        # self.clean_fields()  # comment to keep presets
                    else:
                        self.info_message('<span foreground="red" '
                                          'weight="bold">'
                                          'No empty fields allowed</span>')
        except ValueError:
            self.info_message('<span foreground="red" weight="bold">'
                              'No empty fields allowed</span>')

    @staticmethod
    def fill_combo(iterable, widget):
        widget.remove_all()
        for text in iterable:
            widget.append_text(text)

    def info_message(self, text):
        dialog = WarningDialog(parent=self, text=text)
        dialog.run()
        dialog.destroy()

    # noinspection PyUnusedLocal
    def on_close(self, button):
        self.destroy()

    # noinspection PyUnusedLocal
    def on_select_row(self, tree_view, path, column):
        code = tree_view.get_model()[path][0]
        print("INFO: <%s> selected!" % code)
        child_win = ViewPlayer(parent=self, edit=True, code=code)
        child_win.set_modal(True)
        child_win.show_all()

    def clean_fields(self):
        self.name_entry.set_text("")
        self.budget_entry.set_text("")
        self.trades_entry.set_text("")
        self.max_gk_entry.set_text("")
        self.max_def_entry.set_text("")
        self.max_mf_entry.set_text("")
        self.max_for_entry.set_text("")

    def fill_data(self, team_name):
        team = self.controller.get_team(team_name)
        if team:
            self.name_entry.set_text(team.name)
            self.budget_entry.set_text(str(team.budget))
            self.trades_entry.set_text(str(team.max_trades))
            self.max_gk_entry.set_text(str(team.max_goalkeepers))
            self.max_def_entry.set_text(str(team.max_defenders))
            self.max_mf_entry.set_text(str(team.max_midfielders))
            self.max_for_entry.set_text(str(team.max_forwards))

    # noinspection PyUnusedLocal
    def on_delete(self, button):
        text = self.fantateam_combo.get_active_text()
        dialog = DeleteDialog(parent=self, text=text)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            self.controller.delete_team(text)
            self.clean_fields()
            self.btn_delete.set_sensitive(False)
        else:
            print("INFO: Deleting operation aborted!")
        dialog.destroy()
        self.fantateam_combo.set_active(-1)
