import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GdkPixbuf

from views.importplayers import ViewImportPlayers
from views.auction import ViewAuction
from views.auctionrecap import ViewAuctionRecap
from views.team import ViewTeam
from views.sell import ViewSell
from views.trades import ViewTrade
from views.player import ViewPlayer
from views.dialogs import InfoDialog
from views.dialogs import WarningDialog
from settings import IMG_PATH


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, controller=None):
        self.controller = controller
        super().__init__()
        self.set_default_size(500, 600)
        # Auction actions
        act_auc_new = Gio.SimpleAction.new(name='AucNew', parameter_type=None)
        act_auc_rec = Gio.SimpleAction.new(name='AucRec', parameter_type=None)
        act_quit = Gio.SimpleAction.new(name='AucQuit', parameter_type=None)
        act_export = Gio.SimpleAction.new(name='AucExport', parameter_type=None)
        self.add_action(act_auc_new)
        self.add_action(act_auc_rec)
        self.add_action(act_export)
        self.add_action(act_quit)
        # Team actions
        act_team_new = Gio.SimpleAction.new(name='TeamNew', parameter_type=None)
        act_team_ed = Gio.SimpleAction.new(name='TeamEdit', parameter_type=None)
        act_trades = Gio.SimpleAction.new(name='Trades', parameter_type=None)
        act_sell = Gio.SimpleAction.new(name='Sell', parameter_type=None)
        self.add_action(act_team_new)
        self.add_action(act_team_ed)
        self.add_action(act_trades)
        self.add_action(act_sell)
        # Player actions
        act_pl_new = Gio.SimpleAction.new(name='PlayerNew', parameter_type=None)
        act_pl_ed = Gio.SimpleAction.new(name='PlayerEdit', parameter_type=None)
        act_import = Gio.SimpleAction.new(name='Import', parameter_type=None)
        act_pl_rec = Gio.SimpleAction.new(name='PlayerRec', parameter_type=None)
        self.add_action(act_pl_new)
        self.add_action(act_pl_ed)
        self.add_action(act_import)
        self.add_action(act_pl_rec)
        # Info actions
        act_info = Gio.SimpleAction.new(name='AboutInfo', parameter_type=None)
        self.add_action(act_info)
        # model menu
        menu_model = Gio.Menu.new()
        # menu Auction
        menu_auction = Gio.Menu.new()
        auction_new = Gio.MenuItem.new('New', 'win.AucNew')
        auction_recap = Gio.MenuItem.new('Recap', 'win.AucRec')
        auction_export = Gio.MenuItem.new('Export to csv', 'win.AucExport')
        auction_quit = Gio.MenuItem.new('Quit', 'win.AucQuit')
        menu_auction.append_item(auction_new)
        menu_auction.append_item(auction_recap)
        menu_auction.append_item(auction_export)
        menu_auction.append_item(auction_quit)
        # menu Team
        menu_teams = Gio.Menu.new()
        team_new = Gio.MenuItem.new('New', 'win.TeamNew')
        team_edit = Gio.MenuItem.new('Edit', 'win.TeamEdit')
        trades = Gio.MenuItem.new('Trades', 'win.Trades')
        sell = Gio.MenuItem.new('Sell', 'win.Sell')
        menu_teams.append_item(team_new)
        menu_teams.append_item(team_edit)
        menu_teams.append_item(trades)
        menu_teams.append_item(sell)
        # menu Player
        menu_players = Gio.Menu.new()
        pl_import = Gio.MenuItem.new('Import', 'win.Import')
        pl_new = Gio.MenuItem.new('New', 'win.PlayerNew')
        pl_edit = Gio.MenuItem.new('Edit', 'win.PlayerEdit')
        menu_players.append_item(pl_import)
        menu_players.append_item(pl_new)
        menu_players.append_item(pl_edit)
        # menu Info
        menu_info = Gio.Menu.new()
        about_info = Gio.MenuItem.new('about', 'win.AboutInfo')
        menu_info.append_item(about_info)

        menu_model.append_submenu('Auction', menu_auction)
        menu_model.append_submenu('Team', menu_teams)
        menu_model.append_submenu('Players', menu_players)
        menu_model.append_submenu('Info', menu_info)

        menu_bar = Gtk.MenuBar.new_from_model(menu_model)

        # layout
        layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        layout.pack_start(menu_bar, False, False, 0)
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("%sFantacalcio.bmp" % IMG_PATH)
        image = Gtk.Image.new_from_pixbuf(pixbuf)
        layout.pack_start(image, True, True, 0)
        self.add(layout)

        # bindings auction
        act_auc_new.connect('activate', self.on_new_auction)
        act_auc_rec.connect('activate', self.on_auction_recap)
        act_export.connect('activate', self.on_export)
        # bindings team
        act_team_new.connect('activate', self.on_new_team)
        act_team_ed.connect('activate', self.on_edit_team)
        act_trades.connect('activate', self.on_trades)
        act_sell.connect('activate', self.on_sell)
        # bindings players
        act_pl_new.connect('activate', self.on_new_player)
        act_pl_ed.connect('activate', self.on_edit_player)

        act_quit.connect('activate', self.on_quit)
        act_info.connect('activate', self.on_info)
        act_import.connect('activate', self.on_import)
        self.connect('destroy', Gtk.main_quit)
        self.check_initial_data()

    # noinspection PyUnusedLocal
    def on_info(self, action, value):
        dialog = InfoDialog(parent=self)
        dialog.run()
        dialog.destroy()

    # noinspection PyUnusedLocal
    def on_new_auction(self, action, value):
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewAuction(parent=self)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_auction_recap(self, action, value):
        """Callback bound to 'Auction Recap' menu"""
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewAuctionRecap(parent=self)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_new_team(self, action, value):
        """Callback bound to 'New Team' menu"""
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewTeam(parent=self, edit=False)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_edit_team(self, action, value):
        # print('DEBUG: menu <%s>' % action.props.name)
        child_win = ViewTeam(parent=self, edit=True)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_trades(self, action, value):
        if self.check_initial_data():
            print('INFO: menu <%s>' % action.props.name)
            child_win = ViewTrade(parent=self)
            child_win.set_modal(True)
            child_win.show_all()

    # noinspection PyUnusedLocal
    def on_sell(self, action, value):
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewSell(parent=self)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_import(self, action, value):
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewImportPlayers(controller=self.controller)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_new_player(self, action, value):
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewPlayer(parent=self, edit=False)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_edit_player(self, action, value):
        print('INFO: menu <%s>' % action.props.name)
        child_win = ViewPlayer(parent=self, edit=True)
        child_win.set_modal(True)
        child_win.show_all()

    # noinspection PyUnusedLocal
    def on_export(self, action, value):
        print('INFO: exporting data to csv file...')
        self.controller.export_to_csv()

    def info_message(self, text):
        dialog = WarningDialog(parent=self, text=text)
        dialog.run()
        dialog.destroy()

    def check_initial_data(self):
        teams = self.controller.get_team_names()
        players = self.controller.get_players()
        if not teams:
            self.info_message('<span foreground="red" weight="bold"> '
                              'No teams found</span>\n Please create them:\n'
                              'Menu <span foreground="blue" weight="bold">'
                              'Team -> New</span>')
            return False
        if not players:
            self.info_message('<span foreground="red" weight="bold"> '
                              'No players found</span>\n Please import them:\n'
                              'Menu <span foreground="blue" weight="bold">'
                              'Player -> Import</span>')
            return False
        return True

    # noinspection PyUnusedLocal
    @staticmethod
    def on_quit(action, param):
        Gtk.main_quit()


if __name__ == '__main__':
    win = AppWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
