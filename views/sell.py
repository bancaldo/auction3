import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class ViewSell(Gtk.Window):
    def __init__(self, parent=None):
        if parent:
            self.controller = parent.controller
        super().__init__(title="Sell Player")
        self.set_default_size(300, 300)
        self.set_border_width(10)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        hbox1.pack_start(Gtk.Label("Use Auction Value on sell"), True, True, 0)
        switch = Gtk.Switch()
        switch.set_property("name", "AuctionValueOn")
        switch.props.valign = Gtk.Align.CENTER
        hbox1.pack_start(switch, False, True, 0)
        self.fantateam_combo = Gtk.ComboBoxText()
        teams = self.controller.get_teams()
        for index, team in enumerate(teams):
            self.fantateam_combo.insert(index, "%s" % index, team[0])
        self.player_combo = Gtk.ComboBoxText()
        self.budget = Gtk.Label()
        self.value = Gtk.Label()
        # Buttons
        self.btn_sell = Gtk.Button(label="SELL")
        self.btn_sell.set_sensitive(False)
        btn_close = Gtk.Button(label="QUIT")

        grid = Gtk.Grid()
        grid.attach(hbox1, left=0, top=0, width=2, height=1)
        grid.attach(Gtk.Label(label="Team"), left=0, top=1, width=1,
                    height=1)
        grid.attach(self.fantateam_combo, left=1, top=1, width=1, height=1)
        grid.attach(Gtk.Label(label="Player"), left=0, top=2, width=1,
                    height=1)
        grid.attach(self.player_combo, left=1, top=2, width=1, height=1)
        grid.attach(Gtk.Label(label="player value"), left=0, top=3, width=1,
                    height=1)
        grid.attach(self.value, left=1, top=3, width=1, height=1)
        grid.attach(Gtk.Label(label="budget"), left=0, top=4, width=1, height=1)
        grid.attach(self.budget, left=1, top=4, width=1, height=1)
        grid.attach(self.btn_sell, left=0, top=5, width=1, height=1)
        grid.attach(btn_close, left=1, top=5, width=1, height=1)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # layout
        self.add(grid)

        # bindings
        switch.connect("notify::active", self.on_switch_activated)
        self.btn_sell.connect("clicked", self.on_sell)
        btn_close.connect("clicked", self.on_close)
        self.fantateam_combo.connect('changed', self.on_team)
        self.player_combo.connect('changed', self.on_player)

    # noinspection PyUnusedLocal
    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            self.controller.set_auction_flag(True)
        else:
            self.controller.set_auction_flag(False)
        self.player_combo.set_active(-1)
        self.fantateam_combo.set_active(-1)
        self.value.set_text("")
        self.budget.set_text("")

    def on_team(self, widget):
        team_name = widget.get_active_text()
        if team_name:
            team = self.controller.get_team(team_name)
            self.player_combo.remove_all()
            self.budget.set_text(str(team.budget))
            self.fill_players(team.name)

    def on_player(self, widget):
        player_name = widget.get_active_text()
        if player_name:
            player = self.controller.get_player_by_name(player_name)
            self.value.set_text(str(player.cost))
            new_total = player.team.budget + player.cost
            if self.controller.get_auction_flag():
                aucv = player.auction_value
                if not aucv:
                    aucv = 0
                self.value.set_text(str(aucv))
                new_total = player.team.budget + aucv
            self.budget.set_text("%s (%s)" % (new_total, player.team.budget))
            print("INFO: player %s selected" % player_name)

    def fill_players(self, team_name):
        """Fill the treeview players with fanta team players filtered by role"""
        team = self.controller.get_team(team_name)
        for index, player in enumerate(team.players):
            self.player_combo.insert(index, "%s" % index, player.name)

    # noinspection PyUnusedLocal
    def on_sell(self, button):
        """Callback bound to SAVE button"""
        player_id = self.player_combo.get_active()
        player_model = self.player_combo.get_model()
        player_name = player_model[player_id][0]
        print("INFO: sell player %s" % player_name)
        # controller
        self.player_combo.set_active(-1)
        # refill player
        team_name = self.fantateam_combo.get_active_text()
        team = self.controller.get_team(team_name)
        self.budget.set_text(str(team.budget))
        self.value.set_text("")
        self.fill_players(team.name)

    # noinspection PyUnusedLocal
    def on_close(self, button):
        self.destroy()

    # noinspection PyUnusedLocal
    @ staticmethod
    def on_select_row(tree_view, path, column):
        print("INFO: <%s> selected!" % tree_view.get_model()[path][0])
