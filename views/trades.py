import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from views.dialogs import WarningDialog


class ViewTrade(Gtk.Window):
    def __init__(self, parent=None):
        super().__init__(title="Trades")
        self.set_default_size(300, 400)
        self.set_border_width(10)
        if parent:
            self.controller = parent.controller
        self.team_a_combo = Gtk.ComboBoxText()
        self.team_b_combo = Gtk.ComboBoxText()
        self.player_a_combo = Gtk.ComboBoxText()
        self.player_b_combo = Gtk.ComboBoxText()
        self.budget_a_entry = Gtk.Entry()
        self.budget_b_entry = Gtk.Entry()
        self.extra_a_entry = Gtk.Entry()
        self.extra_b_entry = Gtk.Entry()
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
        # Buttons
        self.btn_trade = Gtk.Button(label="TRADE")
        self.btn_trade.set_sensitive(False)
        btn_close = Gtk.Button(label="QUIT")

        grid = Gtk.Grid()
        grid.attach(frm, left=0, top=0, width=2, height=1)
        grid.attach(Gtk.Label(label="Team A"), left=0, top=1, width=1, height=1)
        grid.attach(Gtk.Label(label="Team B"), left=1, top=1, width=1, height=1)
        grid.attach(self.team_a_combo, left=0, top=2, width=1, height=1)
        grid.attach(self.team_b_combo, left=1, top=2, width=1, height=1)
        grid.attach(Gtk.Label(label="Player A"), left=0, top=3, width=1,
                    height=1)
        grid.attach(Gtk.Label(label="Player B"), left=1, top=3, width=1,
                    height=1)
        grid.attach(self.player_a_combo, left=0, top=4, width=1, height=1)
        grid.attach(self.player_b_combo, left=1, top=4, width=1, height=1)
        grid.attach(Gtk.Label(label="Budget A"), left=0, top=5, width=1,
                    height=1)
        grid.attach(Gtk.Label(label="Budget B"), left=1, top=5, width=1,
                    height=1)
        grid.attach(self.budget_a_entry, left=0, top=6, width=1, height=1)
        grid.attach(self.budget_b_entry, left=1, top=6, width=1, height=1)
        grid.attach(Gtk.Label(label="Extra A"), left=0, top=7, width=1,
                    height=1)
        grid.attach(Gtk.Label(label="Extra B"), left=1, top=7, width=1,
                    height=1)
        grid.attach(self.extra_a_entry, left=0, top=8, width=1, height=1)
        grid.attach(self.extra_b_entry, left=1, top=8, width=1, height=1)

        grid.attach(self.btn_trade, left=0, top=10, width=1, height=1)
        grid.attach(btn_close, left=1, top=10, width=1, height=1)
        grid.set_column_homogeneous(True)
        # grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # layout
        self.add(grid)

        # bindings
        self.btn_trade.connect("clicked", self.on_trade)
        btn_close.connect("clicked", self.on_close)
        for radiobutton in (rb1, rb2, rb3, rb4):
            radiobutton.connect("toggled", self.on_role)
        self.team_a_combo.connect('changed', self.on_team_a)
        self.team_b_combo.connect('changed', self.on_team_b)
        self.player_a_combo.connect('changed', self.on_player_a)
        self.player_b_combo.connect('changed', self.on_player_b)

        # fill fantateam_combos with initial data
        teams = self.controller.get_team_names()
        self.fill_combo(teams, self.team_a_combo)

    @staticmethod
    def fill_combo(iterable, widget):
        widget.remove_all()
        for text in iterable:
            widget.append_text(text)

    # noinspection PyUnusedLocal
    def on_trade(self, button):
        team_a = self.team_a_combo.get_active_text()
        team_b = self.team_b_combo.get_active_text()
        player_a = self.player_a_combo.get_active_text()
        player_b = self.player_b_combo.get_active_text()
        try:
            extra_a = int(self.extra_a_entry.get_text())
            extra_b = int(self.extra_b_entry.get_text())
        except ValueError:
            self.info_message('<span foreground="red" weight="bold">ERROR'
                              '</span>: Only integer accepted as extra values!')
        else:
            result = self.controller.split_players(team_a, player_a, extra_a,
                                                   team_b, player_b, extra_b)
            self.info_message(result)
        self.clean_fields()
        self.clean_comboboxes()
        # refill team_a for another trade operation
        print("INFO: refilling teams for extra trade operations...")
        teams = self.controller.get_team_names()
        self.fill_combo(teams, self.team_a_combo)

    # noinspection PyUnusedLocal
    def on_close(self, button):
        self.destroy()

    # noinspection PyUnusedLocal
    def on_team_a(self, widget):
        role = "goalkeeper"
        team_a_name = self.team_a_combo.get_active_text()
        if team_a_name:
            teams_b = self.controller.get_team_names()
            teams_b.pop(teams_b.index(team_a_name))
            self.fill_combo(teams_b, self.team_b_combo)
            team = self.controller.get_team(team_a_name)
            self.budget_a_entry.set_text(str(team.budget))
            for rb in self.bbox.get_children():
                if rb.get_active():
                    role = rb.get_label().lower()
            players = [p.name for p in team.players if p.role == role]
            self.info_message("Click on player to trade")
            if players:
                print("INFO: players available\n", players)
                self.fill_combo(players, self.player_a_combo)

    # noinspection PyUnusedLocal
    def on_team_b(self, widget):
        role = "goalkeeper"
        team_name = self.team_b_combo.get_active_text()
        if team_name:
            team = self.controller.get_team(team_name)
            self.budget_b_entry.set_text(str(team.budget))
            for rb in self.bbox.get_children():
                if rb.get_active():
                    role = rb.get_label().lower()
            players = [p.name for p in team.players if p.role == role]
            self.info_message("Click on player to trade")
            if players:
                print("INFO: players available\n", players)
                self.fill_combo(players, self.player_b_combo)

    def check_fields(self):
        team_a = self.team_a_combo.get_active_text()
        team_b = self.team_b_combo.get_active_text()
        player_a = self.player_a_combo.get_active_text()
        player_b = self.player_b_combo.get_active_text()
        if team_a and team_b and player_a and player_b:
            return True

    # noinspection PyUnusedLocal
    def on_player_a(self, widget):
        self.extra_a_entry.set_text(str(0))

    # noinspection PyUnusedLocal
    def on_player_b(self, widget):
        self.extra_b_entry.set_text(str(0))
        if self.check_fields():
            self.btn_trade.set_sensitive(True)

    def on_role(self, button):
        # self.clean_fields()
        if button.get_active():
            self.player_a_combo.remove_all()
            self.player_b_combo.remove_all()
            role = button.get_label().lower()
            team_a_name = self.team_a_combo.get_active_text()
            team_b_name = self.team_b_combo.get_active_text()
            if team_a_name:
                self.fill_players(role, team_a_name, self.player_a_combo)
            if team_b_name:
                self.fill_players(role, team_b_name, self.player_b_combo)

    def fill_players(self, role, team_name, widget):
        team = self.controller.get_team(team_name)
        players = [p.name for p in team.players if p.role == role]
        if players:
            print("INFO: players available\n", players)
            self.fill_combo(players, widget)

    def clean_fields(self):
        self.budget_a_entry.set_text("")
        self.budget_b_entry.set_text("")
        self.extra_a_entry.set_text("")
        self.extra_b_entry.set_text("")

    def clean_comboboxes(self):
        self.team_a_combo.set_active(-1)
        self.team_b_combo.remove_all()
        self.player_a_combo.remove_all()
        self.player_b_combo.remove_all()

    def info_message(self, text):
        dialog = WarningDialog(parent=self, text=text)
        dialog.run()
        dialog.destroy()


if __name__ == "__main__":
    win = ViewTrade(None)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
