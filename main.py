import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from models import Model
from views.core import AppWindow
from views.dialogs import WarningDialog


class Controller:
    def __init__(self):
        super(Controller, self).__init__()
        self.model = Model()
        self.view = AppWindow(controller=self)
        self.view.connect("destroy", Gtk.main_quit)
        self.view.show_all()

    def set_temporary_object(self, obj):
        """
        set_temporary_object(obj)
        set model temporary object for editing purposes (i.e. when name of
        the object changes)
        """
        self.model.set_temporary_object(obj)

    def get_temporary_object(self):
        """
        get_temporary_object() -> object
        get model temporary object previously set for editing purposes
        """
        return self.model.get_temporary_object()

    def delete_team(self, team_name):
        """
        delete_team(team_name)
        delete Team object from database
        """
        self.model.delete_team(team_name)

    def delete_player(self, player_name):
        """
        delete_object(player_name)
        delete Player object from database.
        """
        self.model.delete_player(player_name)

    # TEAM methods -------------------------------------------------------------
    def get_team(self, name):
        """
        get_team(name) -> Team object
        Return Team object filtered by name if exists or None
        """
        return self.model.get_team_by_name(name)

    def get_teams(self):
        """
        get_teams() -> list of tuples
        Return a list of Team data tuples. The tuples have this format:
        (name, budget, max_trades, max_goalkeepers, max_defenders,
         max_midfielders, max_forwards)
        """
        return [(t.name, t.budget, t.max_trades, t.max_goalkeepers,
                 t.max_defenders, t.max_midfielders, t.max_forwards)
                for t in self.model.get_teams()]

    def get_team_names(self):
        """
        get_team_names() -> list of team names
        Return a list of all Team names present in database
        """
        return [t.name for t in self.model.get_teams()]

    def new_team(self, data):
        """
        new_team(dict) -> Team object
        Add new Team to database and return the new object created
        """
        return self.model.new_team(data)

    def update_team(self, data):
        """
        update_team(dict) -> Team object
        update the team data and return the updated object
        """
        name = data.get("name")
        budget = data.get("budget")
        max_trades = data.get("max_trades")
        max_gk = data.get("max_gk")
        max_def = data.get("max_def")
        max_mf = data.get("max_mf")
        max_for = data.get("max_for")
        print("INFO: Team %s updated" % name)
        return self.model.update_team(name, budget, max_trades, max_gk, max_def,
                                      max_mf, max_for)

    def get_team_player_data(self, team_name, role=None):
        """"
        get_team_player_data(team_name) -> list
        Return a list of tuple with the team player data as
        (code, name, role, real_team, value, auction_value)
        """
        return [(p.code, p.name, self.model.get_role_by_code(p.code),
                 p.real_team, p.cost, p.auction_value)
                for p in self.model.get_team_player_by_role(team_name, role)]

    def sell_player(self, player_name):
        """
        sell_player(player_name) -> bool
        Sell Player and update the team budget
        """
        self.model.sell_player(player_name)

    def get_auction_flag(self):
        """get_auction_flag() -> bool
        return the boolean auction_flag
        True is used when we use a player auction value during the sale,
        False is used when we use a player cost durint the sale
        """
        return self.model.get_auction_flag()

    def set_auction_flag(self, auction_flag):
        """
        set_auction_flag(bool)
        set the boolean auction_flag to True if we use the player auction value
        during the sale, otherwise False to use the player cost
        """
        self.model.set_auction_flag(auction_flag=auction_flag)

    # PLAYER methods -----------------------------------------------------------
    def on_import_players(self, data):
        """
        on_import_players(data)
        Import player by txt file, if player exists its data are updated else
        a new player is created.
        data is a line of text formatted as:
        'code|name|real_team|v|fv|cost'
        """
        code, name, real_team, v, fv, cost = data.strip().split("|")
        player = self.model.get_player_by_code(code)
        if player:
            self.model.update_player(code, name, real_team, cost)
        else:
            self.model.new_player(code=code, name=name, real_team=real_team,
                                  cost=cost)

    def buy_player(self, player_name, auction_value, team):
        """
        buy_player(player_name, auction_value, team) -> bool
        Bind player to fanta_team and update the team budget
        """
        return self.model.buy_player(player_name, auction_value, team)

    def new_player(self, data):
        """
        new_player(data) -> Player object
        Insert a new player into database manually.
        Usually you have to use 'import players' menu
        """
        code = data.get("code")
        name = data.get("name")
        real_team = data.get("real_team")
        cost = data.get("cost")
        return self.model.new_player(code=code, name=name, real_team=real_team,
                                     cost=cost)

    def update_player(self, data):
        """
        update_player(data) -> Player object
        Update the values of an existing Player
        """
        code = data.get("code")
        name = data.get("name")
        real_team = data.get("real_team")
        cost = data.get("cost")
        auction_value = data.get("auction_value")
        return self.model.update_player(code, name, real_team, cost,
                                        auction_value)

    def stop_import(self):
        """
        Stop the import operation rolling back the session
        """
        self.model.rollback_session()

    def get_free_players(self, role=None):
        """get_free_players(role) -> list of free players
        With role argument it returns all free players with role passed as arg;
        with no arguments, it returns all free players
        Free Player means no fanta team.
        """
        return self.model.get_free_players(role)

    def get_players(self, role=None, real_team=None):
        """get_players(**kwargs) -> player list.
        With role argument it returns all players with role passed as arg;
        with real_team argument it returns all players with the same real team;
        with both args, it returns all players by role and same real team;
        with no arguments, it returns all players"""
        return [p.name for p in self.model.get_players(role, real_team)]

    def get_sorted_players(self, id_c, role):
        """
        get_sorted_players(id_c, role) -> list of Players
        Get Player list filtered by id_c and sorted by role.
        'id_c' stays for 'index of column', the filter used by SQLAlchemy during
        query operation. 'id_c' can be:
        0: players are filtered by 'code';
        1: players are filtered by 'name';
        2: players are filtered by 'real_team';
        3: players are filtered by '-cost' (- stays for descending mode);
        4: players are filtered by '-auction_value' (descending mode);
        5: players are filtered by 'team';
        Roles are: goalkeeper, defender, midfielder, forward
        """
        columns = {0: 'code', 1: 'name', 2: 'real_team', 3: '-cost',
                   4: '-auction_value', 5: 'team'}
        players = self.model.get_players_ordered_by_filter(columns.get(id_c),
                                                           role)
        return [player.name for player in players]

    def get_players_by_real_team(self, role, real_team):
        """
        get_players_by_real_team(role, real_team) -> Player list
        Get Player list sorted by role.
        Roles are: goalkeeper, defender, midfielder, forward
        """
        players = self.model.get_players_by_real_team(role, real_team)
        return [player.name for player in players]

    def get_player_by_name(self, player_name):
        """
        get_player_by_name(name) -> Player object
        Return Player object by name if name exists else it returns None
        """
        return self.model.get_player_by_name(player_name)

    def get_players_count(self):
        """
        get_players_count -> int
        Return the total number of players stored in the database
        """
        return self.model.get_players_count()

    def get_player_by_code(self, player_code):
        """
        get_player_by_code(int) -> Player object
        Return Player object by code if code exists else it returns None
        """
        return self.model.get_player_by_code(player_code)

    def available_players(self, role=None, prefix=''):
        """
        available_players(role, prefix) -> player list.
        Return all players with role passed as argument and/or name starts
        with prefix.
        """
        return self.model.available_players(role=role, prefix=prefix)

    def get_player_values(self, name):
        """
        get_player_values(name) -> tuple
        Return the player values:
        code, name, real_team, value, auction_value, role
        """
        p = self.model.get_player_by_name(name)
        if p:
            return p.code, p.name, p.real_team, p.value, p.auction_value, p.role

    def update_budget(self, team_name, difference):
        """
        update_budget(team_name, difference)
        Update the Team budget
        """
        self.model.update_budget(team_name, difference)

    def get_teams_count(self):
        """
        get_teams_count() -> int
        Return the number of Fanta Team
        """
        return self.model.get_teams_count()

    def get_real_teams(self):
        """get_real_teams() -> list
        Return the list of real_team present in the database
        """
        return self.model.get_real_teams()

    def do_transfer(self, player_name, team_name):
        """
        Execute the transfer, so player team and team player list are updated
        team budget and team remaining trades are updated too.
        """
        self.model.do_transfer(player_name, team_name)
        print("INFO: Transfer %s --> %s" % (player_name, team_name))

    def discard_player(self, code):
        """
        discard_player(code)
        Discard a Player from Team and update the budget
        """
        self.model.discard_player(code)

    def set_role(self, role):
        """
        Set the actual role
        """
        self.model.role = role

    def change_budgets(self, left_team_name, left_extra_budget,
                       right_team_name, right_extra_budget):
        """
        Change budgets after Player transfer between two teams
        """
        self.model.change_budgets(left_team_name, left_extra_budget,
                                  right_team_name, right_extra_budget)

    def split_players(self, left_team, left_player, left_extra,
                      right_team, right_player, right_extra):
        """split_players(left_team, left_player, left_extra,
                         right_team, right_player, right_extra) -> Bool
        Do trade between two teams.
        Left player pass to right team and viceversa.
        If extra money are present, the team budgets are updated
        """
        return self.model.split_players(left_team, left_player, left_extra,
                                        right_team, right_player, right_extra)

    def export_to_csv(self):
        """Export all the auctions to auction.csv file"""
        print("INFO: Exporting teams to 'auction.csv' file...")
        teams = self.get_team_names()
        if teams:
            with open('auction.csv', 'w') as output:
                # write header
                for team_name in teams:
                    header = "%s;;"
                    output.write("%s\n" % (header % team_name))
                    team = self.get_team(team_name)
                    if team.get_players_bought() != team.get_max_players():
                        print("ERROR: Missing players in team %s" % team.name)
                        dialog = WarningDialog(
                            parent=self.view,
                            text='Missing players in team\n<span foreground='
                                 '"red" weight="bold"> %s</span>!' % team.name)
                        dialog.run()
                        dialog.destroy()
                    for player in team.players:
                        if player:
                            output.write("%s;%s;\n" % (player.name,
                                                       player.auction_value))
                    # write team footer
                    output.write("budget;%s;\n" % team.budget)
                print("INFO: Auction exported to auction.csv file")
                dialog = WarningDialog(
                    parent=self.view, text="Auction exported to auction.csv")
                dialog.run()
                dialog.destroy()
        else:
            print("WARNING: No Teams in db, please create them")
            dialog = WarningDialog(
                parent=self.view, text="No Teams in db, please create them")
            dialog.run()
            dialog.destroy()


class App:
    def __init__(self):
        self.controller = Controller()

    @staticmethod
    def run():
        Gtk.main()


if __name__ == '__main__':
    app = App()
    app.run()
