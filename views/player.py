import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
import platform
from views.dialogs import WarningDialog, DeleteDialog


IMPORT_PATH = os.getcwd() + '/days/' if platform.system() == 'Linux' else\
              os.getcwd() + '\\days\\'


class ViewPlayer(Gtk.Window):
    def __init__(self, parent=None, edit=True, code=None):
        if parent:
            self.controller = parent.controller
        title = "Edit Player" if edit else "New Player"
        self.edit = edit
        super().__init__(title=title)
        self.set_default_size(300, 400)
        self.set_border_width(10)
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
        # Combobox
        self.real_team_combo = Gtk.ComboBoxText()
        self.player_combo = Gtk.ComboBoxText()
        self.player_combo.set_entry_text_column(0)
        # self.player_combo.set_wrap_width(5)
        self.code_entry = Gtk.Entry()
        self.name_entry = Gtk.Entry()
        self.rteam_entry = Gtk.Entry()
        self.cost_entry = Gtk.Entry()
        self.auction_value_entry = Gtk.Entry()
        self.fantateam_combo = Gtk.ComboBoxText()

        btn_save = Gtk.Button(label="SAVE")
        self.btn_delete = Gtk.Button(label="Delete")
        self.btn_delete.set_sensitive(False)
        btn_close = Gtk.Button(label="QUIT")
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox.pack_start(btn_save, True, True, 0)
        hbox.pack_start(self.btn_delete, True, True, 0)
        hbox.pack_start(btn_close, True, True, 0)

        grid = Gtk.Grid()
        if self.edit:
            grid.attach(Gtk.Label(label="Real Team"), left=0, top=0, width=1,
                        height=1)
            grid.attach(self.real_team_combo, left=1, top=0, width=1, height=1)
            grid.attach(Gtk.Label(label="Player"), left=0, top=1, width=1,
                        height=1)
            grid.attach(self.player_combo, left=1, top=1, width=1, height=1)
        grid.attach(Gtk.Label(label="Code"), left=0, top=2, width=1, height=1)
        grid.attach(Gtk.Label(label="Name"), left=0, top=3, width=1, height=1)
        grid.attach(Gtk.Label(label="real team"), left=0, top=4, width=1,
                    height=1)
        grid.attach(Gtk.Label(label="cost"), left=0, top=5, width=1, height=1)
        grid.attach(Gtk.Label(label="auction value"), left=0, top=6, width=1, 
                    height=1)
        grid.attach(Gtk.Label(label="Fanta Team"), left=0, top=7, width=1,
                    height=1)
        grid.attach(self.code_entry, left=1, top=2, width=1, height=1)
        grid.attach(self.name_entry, left=1, top=3, width=1, height=1)
        grid.attach(self.rteam_entry, left=1, top=4, width=1, height=1)
        grid.attach(self.cost_entry, left=1, top=5, width=1, height=1)
        grid.attach(self.auction_value_entry, left=1, top=6, width=1, height=1)
        grid.attach(self.fantateam_combo, left=1, top=7, width=1, height=1)
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)

        # layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox.pack_start(frm, False, False, 0)
        vbox.pack_start(grid, False, True, 0)
        vbox.pack_start(hbox, False, False, 0)
        self.add(vbox)

        # bindings
        btn_save.connect("clicked", self.on_save)
        self.btn_delete.connect("clicked", self.on_delete)
        btn_close.connect("clicked", self.on_close)
        for radiobutton in (rb1, rb2, rb3, rb4):
            radiobutton.connect("toggled", self.on_role)
        self.player_combo.connect('changed', self.on_player)
        self.real_team_combo.connect('changed', self.on_real_team)

        if code:
            self.fill_player_data(code)
            self.btn_delete.set_sensitive(True)
        else:
            real_teams = self.controller.get_real_teams()
            self.fill_combo(real_teams, self.real_team_combo)

    def fill_player_data(self, code):
        player = self.controller.get_player_by_code(int(code))
        if player:
            for rb in self.bbox.get_children():
                role = rb.get_label().lower()
                if role == player.role.lower():
                    rb.set_active(True)
            self.fill_entries(player)

    # noinspection PyUnusedLocal
    def on_real_team(self, widget):
        role = "goalkeeper"
        self.clean_fields()
        real_team = self.real_team_combo.get_active_text()
        for rb in self.bbox.get_children():
            if rb.get_active():
                role = rb.get_label().lower()
        players = self.controller.get_players_by_real_team(role, real_team)
        self.fill_combo(players, self.player_combo)

    # noinspection PyUnusedLocal
    def on_player(self, widget):
        player_name = self.player_combo.get_active_text()
        player = self.controller.get_player_by_name(player_name)
        if player:
            self.fill_entries(player)
            self.btn_delete.set_sensitive(True)

    def fill_entries(self, player):
        self.name_entry.set_text(player.name)
        self.code_entry.set_text(str(player.code))
        self.rteam_entry.set_text(player.real_team)
        self.cost_entry.set_text(str(player.cost))
        self.auction_value_entry.set_text(str(player.auction_value))

    @staticmethod
    def fill_combo(iterable, widget):
        widget.remove_all()
        for text in iterable:
            widget.append_text(text)

    def on_role(self, button):
        self.clean_fields()
        self.btn_delete.set_sensitive(False)
        if button.get_active():
            self.player_combo.remove_all()
            role = button.get_label().lower()
            real_team = self.real_team_combo.get_active_text()
            print("INFO: role <%s> selected" % role)
            players = self.controller.get_players_by_real_team(role, real_team)
            self.fill_combo(players, self.player_combo)

    def clean_fields(self):
        self.name_entry.set_text("")
        self.code_entry.set_text("")
        self.rteam_entry.set_text("")
        self.cost_entry.set_text("")
        self.auction_value_entry.set_text("")

    # noinspection PyUnusedLocal
    def on_save(self, button):
        name = self.name_entry.get_text()
        code = self.code_entry.get_text()
        real_team = self.rteam_entry.get_text()
        cost = self.auction_value_entry.get_text()
        auction_value = self.cost_entry.get_text()
        if not auction_value:
            auction_value = 0
        if name and code and real_team and cost and auction_value:
            data = {'name': name, 'code': int(code),
                    'real_team': real_team, 'cost': int(cost),
                    'auction_value': int(auction_value)}
            if self.edit:
                self.controller.update_player(data)
            else:
                if self.controller.get_player_by_name(name):
                    self.info_message('Player <span foreground="red" '
                                      'weight="bold">'
                                      '%s</span> already exists!' % name)
                else:
                        self.controller.new_player(data=data)
        else:
            self.info_message('<span foreground="red" weight="bold"> '
                              'No empty fields allowed</span>')

    def info_message(self, text):
        dialog = WarningDialog(parent=self, text=text)
        dialog.run()
        dialog.destroy()

    # noinspection PyUnusedLocal
    def on_delete(self, button):
        text = self.name_entry.get_text()
        dialog = DeleteDialog(parent=self, text=text)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            self.controller.delete_player(text)
            self.clean_fields()
            self.btn_delete.set_sensitive(False)
        else:
            print("INFO: Deleting operation aborted!")
        dialog.destroy()
        self.real_team_combo.set_active(-1)
        self.player_combo.set_active(-1)

    # noinspection PyUnusedLocal
    def on_close(self, button):
        self.destroy()
