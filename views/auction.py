import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import platform
from views.dialogs import WarningDialog


IMPORT_PATH = os.getcwd() + '/days/' if platform.system() == 'Linux' else\
              os.getcwd() + '\\days\\'


class ViewAuction(Gtk.Window):
    def __init__(self, parent=None):
        self.controller = parent.controller
        super().__init__(title="New auction")
        self.set_default_size(300, 500)
        self.set_border_width(10)
        role_label = Gtk.Label.new()
        role_label.set_markup('<span foreground="blue" weight="bold">'
                              'Select a player to buy</span>')
        role_label.set_justify(Gtk.Justification.LEFT)
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

        rteam_label = Gtk.Label.new()
        rteam_label.set_markup('<span foreground="green" weight="bold">'
                               'real team</span>')
        player_label = Gtk.Label.new()
        player_label.set_markup('<span foreground="green" weight="bold">'
                                'player</span>')
        self.real_team_combo = Gtk.ComboBoxText()
        self.player_combo = Gtk.ComboBoxText()
        cost_label = Gtk.Label.new()
        cost_label.set_markup('<span foreground="green" weight="bold">'
                              'cost</span>')
        fantateam_label = Gtk.Label.new()
        fantateam_label.set_markup('<span foreground="green" weight="bold">'
                                   'FantaTeam</span>')
        self.fantateam_combo = Gtk.ComboBoxText()
        self.name_label = Gtk.Label()
        self.code_label = Gtk.Label()
        self.rteam_label = Gtk.Label()
        self.cost_label = Gtk.Label()
        self.auction_value_label = Gtk.Entry()

        self.btn_save = Gtk.Button(label="SAVE")
        self.btn_save.set_sensitive(False)
        btn_close = Gtk.Button(label="QUIT")
        # GRID LAYOUT
        grid = Gtk.Grid()
        grid.add(rteam_label)
        grid.attach(child=self.real_team_combo, left=1, top=0, width=1,
                    height=1)
        # 1st line
        grid.attach(child=player_label, left=0, top=1, width=1, height=1)
        grid.attach(child=self.player_combo, left=1, top=1, width=1, height=1)
        # 2nd line and so on
        grid.attach(Gtk.Label(label="Name"), left=0, top=2, width=1, height=1)
        grid.attach(self.name_label, left=1, top=2, width=1, height=1)

        grid.attach(Gtk.Label(label="code"), left=0, top=3, width=1, height=1)
        grid.attach(self.code_label, left=1, top=3, width=1, height=1)

        grid.attach(Gtk.Label(label="team"), left=0, top=4, width=1, height=1)
        grid.attach(self.rteam_label, left=1, top=4, width=1, height=1)

        grid.attach(Gtk.Label(label="cost"), left=0, top=5, width=1, height=1)
        grid.attach(self.cost_label, left=1, top=5, width=1, height=1)

        grid.attach(Gtk.Label(label="auction value"), left=0, top=6, width=1,
                    height=1)
        grid.attach(self.auction_value_label, left=1, top=6, width=1, height=1)

        grid.attach(fantateam_label, left=0, top=7, width=1, height=1)
        grid.attach(self.fantateam_combo, left=1, top=7, width=1, height=1)

        grid.attach(self.btn_save, left=0, top=8, width=1, height=1)
        grid.attach(btn_close, left=1, top=8, width=1, height=1)

        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(role_label, False, False, 0)
        vbox.pack_start(frm, False, False, 0)
        vbox.pack_start(grid, False, True, 0)
        self.add(vbox)

        # bindings
        self.btn_save.connect("clicked", self.on_save)
        btn_close.connect("clicked", self.on_close)
        for radiobutton in (rb1, rb2, rb3, rb4):
            radiobutton.connect("toggled", self.on_role)
        self.real_team_combo.connect('changed', self.on_real_team)
        self.player_combo.connect('changed', self.on_player)
        self.fantateam_combo.connect('changed', self.on_fanta_team)

        # fill real teams combobox
        real_teams = self.controller.get_real_teams()
        self.fill_combo(real_teams, self.real_team_combo)

    def on_role(self, button):
        self.clean_fields()
        if button.get_active():
            self.player_combo.remove_all()
            role = button.get_label().lower()
            real_team = self.real_team_combo.get_active_text()
            players = self.controller.get_players_by_real_team(role, real_team)
            self.fill_combo(players, self.player_combo)

    # noinspection PyUnusedLocal
    def on_real_team(self, widget):
        self.clean_fields()
        for rb in self.bbox.get_children():
            role = "goalkeeper"
            if rb.get_active():
                role = rb.get_label().lower()
                real_team = self.real_team_combo.get_active_text()
                players = self.controller.get_players_by_real_team(role,
                                                                   real_team)
                self.fill_combo(players, self.player_combo)

    # noinspection PyUnusedLocal
    def on_player(self, widget):
        player_name = self.player_combo.get_active_text()
        player = self.controller.get_player_by_name(player_name)
        if player:
            self.name_label.set_text(player.name)
            self.code_label.set_text(str(player.code))
            self.rteam_label.set_text(player.real_team)
            self.cost_label.set_text(str(player.cost))
            if player.auction_value:
                self.auction_value_label.set_text(str(player.auction_value))
            if player.team:
                dialog = WarningDialog(
                    parent=self,
                    text='Player <span foreground="red" weight="bold">'
                         '%s</span>\nbelongs to <span foreground="red" '
                         'weight="bold">%s</span>!' % (player.name,
                                                       player.team.name))
                dialog.run()
                dialog.destroy()
            else:
                fantateams = self.controller.get_team_names()
                self.fill_combo(fantateams, self.fantateam_combo)

    # noinspection PyUnusedLocal
    def on_fanta_team(self, widget):
        self.btn_save.set_sensitive(True)

    def clean_fields(self):
        self.name_label.set_text("")
        self.code_label.set_text("")
        self.rteam_label.set_text("")
        self.cost_label.set_text("")
        self.auction_value_label.set_text("")

    @staticmethod
    def fill_combo(iterable, widget):
        widget.remove_all()
        for text in iterable:
            widget.append_text(text)

    # noinspection PyUnusedLocal
    def on_save(self, button):
        player_name = self.name_label.get_text()
        try:
            auction_value = int(self.auction_value_label.get_text())
        except ValueError:
            auction_value = 0
        fanta_team_name = self.fantateam_combo.get_active_text()
        result = self.controller.buy_player(player_name, auction_value,
                                            fanta_team_name)
        self.info_message(result)
        self.clean_fields()
        self.player_combo.set_active(-1)
        self.real_team_combo.set_active(-1)
        self.fantateam_combo.set_active(-1)
        self.btn_save.set_sensitive(False)

    # noinspection PyUnusedLocal
    def on_close(self, button):
        self.destroy()

    def info_message(self, text):
        dialog = WarningDialog(parent=self, text=text)
        dialog.run()
        dialog.destroy()


if __name__ == "__main__":
    win = ViewAuction()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
