from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from settings import DATABASE


Base = declarative_base()


class Team(Base):
    """SQLAlchemy Team Class"""
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    budget = Column(Integer)
    max_trades = Column(Integer)
    max_goalkeepers = Column(Integer)
    max_defenders = Column(Integer)
    max_midfielders = Column(Integer)
    max_forwards = Column(Integer)
    players = relationship("Player")

    def __repr__(self):
        return "< Team(name='%s', budget='%s')>" % (self.name, self.budget)

    def get_max_players(self):
        """
        get_max_players() -> int
        return the number max players allowed
        """
        return sum([self.max_goalkeepers, self.max_defenders,
                   self.max_midfielders, self.max_forwards])

    def get_players_bought(self):
        """
        get_players_bought() -> int
        return the total number of players bought by team
        """
        return len(self.players)


class Player(Base):
    """SQLAlchemy Player Class"""
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship("Team", back_populates="players")
    code = Column(Integer)
    name = Column(String)
    real_team = Column(String)
    cost = Column(Integer)
    auction_value = Column(Integer)
    role = Column(String)

    def __repr__(self):
        return "< Player(name='%s')>" % self.name


class Model:
    """Model class with common application data"""
    def __init__(self):
        self.engine = create_engine(DATABASE, echo=False)
        Base.metadata.create_all(self.engine)
        m_session = sessionmaker(bind=self.engine)
        self.session = m_session()
        print("INFO: initializing database...")
        self.temporary_object = None
        self.bulk_players_to_update = []
        self.bulk_players_to_create = []
        self.auction_flag = False  # used on player sale

    def get_new_session(self):
        m_session = sessionmaker(bind=self.engine)
        self.session = m_session()

    def get_auction_flag(self):
        return self.auction_flag

    def set_auction_flag(self, auction_flag):
        """auction_flag is the boolean used to define what value use
        to increase team budget after a player sale.
        If auction_flag is True, then team budget increases by the player's
        auction_value, instead if auction_flag is false, the budget increases
        by player's value"""
        self.auction_flag = auction_flag
        print("INFO: set auction_flag_on to %s" % auction_flag)

    def set_temporary_object(self, obj):
        """
        set_temporary_object(obj)
        set model temporary object for editing purposes (i.e. when name of
        the object changes)
        """
        print("INFO: store '%s' as temporary object" % obj)
        self.temporary_object = obj

    def get_temporary_object(self):
        """
        get_temporary_object() -> object
        get model temporary object previously set for editing purposes
        """
        print("INFO: retrieve temporary object")
        return self.temporary_object

    @staticmethod
    def delete_object(obj):
        """
        delete_object(obj) -> obj
        delete object from database and return it
        """
        deleted_object = obj.delete()
        return deleted_object

    # TEAM methods -------------------------------------------------------------
    def get_teams(self):
        """
        get_teams() -> list of Team objects
        Get a list of all Teams present in database
        """
        return self.session.query(Team).all()

    def get_team_by_name(self, name):
        """
        get_team_by_name(name) -> Team object
        Get Team object by name
        """
        return self.session.query(Team).filter_by(name=name.upper()).first()

    def new_team(self, data):
        """
        new_team(dict) -> Team object
        Add new Team to database with dict data as parameter.
        data keys are:
        'name': string representing the name of the fanta team;
        'budget': integer representing the initial budget of fanta team;
        'max_trades': integer representing the max number of trades;
        'max_gk': integer representing the number of goalkeepers;
        'max_def': integer representing the number of defenders;
        'max_mf': integer representing the number of midfielders;
        'max_for': integer representing the number of forwards
        """
        team = Team()
        team.name = data.get("name").upper()
        team.budget = data.get("budget")
        team.max_trades = data.get("max_trades")
        team.max_goalkeepers = data.get("max_gk")
        team.max_defenders = data.get("max_def")
        team.max_midfielders = data.get("max_mf")
        team.max_forwards = data.get("max_for")
        self.session.add(team)
        self.session.commit()
        print("INFO: new team <%s> added to database" % team.name)
        return team

    def update_team(self, team_name, budget, max_t, max_g, max_d, max_m, max_f):
        """
        update_team(team_name, budget, max_t, max_g, max_d, max_m, max_f)
        Update Team data in the database
        """
        team = self.get_team_by_name(team_name)
        if not team:
            team = self.get_temporary_object()
        team.name = team_name.upper()
        team.budget = budget
        team.max_trades = max_t
        team.max_goalkeepers = max_g
        team.max_defenders = max_d
        team.max_midfielders = max_m
        team.max_forwards = max_f
        self.session.commit()
        return team

    def update_budget(self, team_name, difference):
        """
        update_budget(team_name, difference)
        Update the Team budget
        """
        team = self.get_team_by_name(team_name)
        old_budget = team.budget
        team.budget += int(difference)
        print("INFO: %s budget updated: %s --> %s" % (team_name, old_budget,
                                                      team.budget))
        self.session.commit()

    def get_teams_count(self):
        """
        get_teams_count() -> int
        Return the number of Fanta Team
        """
        return self.session.query(Team).count()

    def discard_player(self, code):
        """
        discard_player(code)
        Discard a Player from Team and update the budget
        """
        player = self.get_player_by_code(int(code))
        team = player.team
        auction_value = player.auction_value
        if not auction_value:
            auction_value = 0
        team.budget += auction_value
        print("INFO: Team %s budget: +%s" % (team.name, auction_value))
        player.team = None
        player.auction_value = None
        print("INFO: Player %s updated" % player.name)
        self.session.commit()

    def get_team_player_by_role(self, team_name, role=None):
        """"
        get_team_player_by_role(team_name, role) -> player list
        Return the Fantateam player list filtered by role
        """
        team = self.get_team_by_name(team_name)
        if not role:
            return team.players
        return [p for p in team.players if p.role == role]

    # PLAYER methods -----------------------------------------------------------
    def new_player(self, code, name, real_team, cost):
        """
        new_player(code, name, real_team, cost) -> Player object
        Add new Player to database
        """
        role = self.get_role_by_code(code)
        player = Player(code=code, name=name, real_team=real_team, cost=cost,
                        role=role)
        self.session.add(player)
        self.session.commit()
        print("INFO: new player <%s> added to database" % player.name)
        return player

    def get_players_count(self):
        """
        get_players_count -> int
        Return the total number of players stored in the database
        """
        return self.session.query(Player).count()

    def get_player_by_name(self, name):
        """
        get_player_by_name(name) -> Player object
        Return Player object by name if name exists else it returns None
        """
        return self.session.query(Player).filter_by(name=name).first()

    def get_player_by_code(self, code):
        """
        get_player_by_code(int) -> Player object
        Return Player object by code if code exists else it returns None
        """
        return self.session.query(Player).filter_by(code=int(code)).first()

    def buy_player(self, player_name, auction_value, team_name):
        """buy_player(player_name, auction_value, team) -> bool
        Bind player to fanta_team and update the team budget"""
        team = self.get_team_by_name(team_name)
        player = self.get_player_by_name(player_name)
        in_team = [p for p in team.players if p.role == player.role]

        if player in team.players:
            message = "ERROR: Player previously bought"
        elif player.team_id and not player.team_id == team.id:
            message = "ERROR: Player already bought by another team"
        else:
            if player.role.lower() == 'goalkeeper':
                max_p = team.max_goalkeepers
                team.max_goalkeepers -= 1
            elif player.role.lower() == 'defender':
                max_p = team.max_defenders
                team.max_defenders -= 1
            elif player.role.lower() == 'midfielder':
                max_p = team.max_midfielders
                team.max_midfielders -= 1
            else:
                max_p = team.max_forwards
                team.max_forwards -= 1

            if len(in_team) < max_p:
                bought = len(team.players)
                max_players = team.get_max_players()
                remaining = max_players - bought
                cash = int(team.budget)
                if (cash - remaining) > 0:
                    team.players.append(player)
                    team.budget -= int(auction_value)
                    #                        self.session.commit()
                    player.auction_value = auction_value
                    self.session.commit()
                    message = "INFO: '%s' (%s) [%s] saved!" % (
                        player.name, auction_value, team.name)
                else:
                    message = "ERROR: Not enough money to complete team"
            else:
                message = "ERROR: players limit reached"
        print(message)
        return message

    def get_players_ordered_by_filter(self, filter_name, role):
        """
        get_players_ordered_by_filter(filter_name, role) -> list of Players
        Get Player list sorted by role.
        Roles are: goalkeeper, defender, midfielder, forward
        """
        return self.session.query(Player).filter_by(
            role=role).order_by(filter_name)

    def get_players_by_real_team(self, role, real_team):
        """
        get_players_by_real_team(role, real_team) -> Player list
        Get Player list sorted by role.
        Roles are: goalkeeper, defender, midfielder, forward
        """
        return self.session.query(Player).filter_by(
            role=role, real_team=real_team).all()

    def sell_player(self, player_name):
        """Sell a Player and remove him from previous Team"""
        player = self.get_player_by_name(player_name)
        role = player.role
        team = player.team
        team.players.remove(player)
        print("INFO: updating max player per role remaining...")
        if role == "goalkeeper":
            team.max_goalkeepers += 1
        elif role == "defender":
            team.max_defenders += 1
        elif role == "midfielder":
            team.max_midfielders += 1
        else:
            team.max_forwards += 1
        print("INFO: updating team budget...")
        if self.auction_flag:
            print("INFO: [auction flag = True], updating team budget...")
            team.budget += player.auction_value
        else:
            print("INFO: [auction flag = False], updating team budget...")
            team.budget += player.cost
        self.session.commit()
        return team.players.all()

    def delete_player(self, player_name):
        """
        delete_player(player_name)
        delete Player object from database.
        """
        player = self.get_player_by_name(player_name)
        role = player.role
        cost = player.cost
        team = player.team
        if team:
            old_budget = team.budget
            print("WARNING: association %s <-> %s removed"
                  % (player_name, team.name))
            team.players.remove(player)
            print("INFO: updating team %s budget -> %s (+%s)"
                  % (team.name, old_budget + cost, cost))
            team.budget += cost
            print("INFO: updating team %s remaining players" % team.name)
            if role == "goalkeeper":
                team.max_goalkeepers += 1
            elif role == "defender":
                team.max_defenders += 1
            elif role == "midfielder":
                team.max_midfielders += 1
            else:
                team.max_forwards += 1
        self.session.commit()
        self.session.delete(player)
        self.session.commit()

    def delete_players(self):
        """Delete all players from database"""
        self.session.query(Player).delete()

    def delete_team(self, team_name):
        """
        delete_team(player_name)
        delete Team object from database.
        """
        team = self.get_team_by_name(team_name)
        if team.players:
            print("WARNING: freeing players present in team...")
            for player in team.players:
                team.players.remove(player)
                print("INFO: removing player %s from team %s"
                      % (player.name, team_name))
                player.auction_value = None
        self.session.commit()
        self.session.delete(team)
        self.session.commit()

    def get_players(self, role=None, real_team=None):
        """get_players(**kwargs) -> player list.
        With role argument it returns all players with role passed as arg;
        with real_team argument it returns all players with the same real team;
        with both args, it returns all players by role and same real team;
        with no arguments, it returns all players"""
        if role and not real_team:
            return self.session.query(Player).filter_by(role=role).all()
        elif real_team and not role:
            return self.session.query(Player).filter_by(
                real_team=real_team).all()
        elif role and real_team:
            return self.session.query(Player).filter_by(
                role=role, real_team=real_team).all()
        else:
            return self.session.query(Player).all()

    def get_free_players(self, role=None):
        """get_free_players(role) -> free player list.
        With role argument it returns all free players with role passed as arg;
        with no arguments, it returns all free players
        Free Player means no fanta team.
        """
        players = self.session.query(Player).filter_by(team=None).all()
        if role:
            players = self.session.query(Player).filter_by(
                team=None, role=role).all()
        return players

    def get_team_by_name_players(self, team_name, role):
        """get_team_by_name_players(team_name, role) -> player list.
        Return all players of a Fanta team, sorted by role, passed as argument.
        """
        team = self.get_team_by_name(team_name)
        return self.session.query(Player).filter_by(team=team, role=role).all()

    def employed(self):
        """employed() -> player list.
        Return all players with a Fanta team.
        It's the opposite of the get_free_players() method.
        """
        return [p for p in self.get_players() if p.team is not None]

    def available_players(self, role=None, prefix=''):
        """
        available_players(role, prefix) -> player list.
        Return all players with role passed as argument and/or name starts
        with prefix.
        """
        free = [g for g in self.get_players() if g.team is None]
        if role is None and prefix == '':
            available = free
        elif role and prefix == '':
            available = [p for p in free if p.role == role.strip()]
        elif prefix and role is None:
            available = [p for p in free if p.name.startswith(
                prefix.strip().upper())]
        else:
            available = [p for p in free if p.role == role.strip() and
                         p.name.startswith(prefix.upper().strip())]
        return available

    def do_transfer(self, player_name, team_name):
        """
        Execute the transfer, so player team and team player list are updated
        team budget and team remaining trades are updated too.
        """
        player = self.get_player_by_name(player_name)
        team = self.get_team_by_name(team_name)
        team.budget -= player.cost
        team.max_trades -= 1
        player.team = team
        role = player.role
        print("INFO: updating max player per role remaining...")
        if role == "goalkeeper":
            team.max_goalkeepers -= 1
        elif role == "defender":
            team.max_defenders -= 1
        elif role == "midfielder":
            team.max_midfielders -= 1
        else:
            team.max_forwards -= 1
        self.session.commit()

    def get_real_teams(self):
        """get_real_teams -> list
         return a list of all real_team name present in database"""
        return [t[0] for t in
                self.session.query(Player.real_team).distinct().order_by(
                    Player.real_team).all()]

    def update_player(self, code, name, real_team, cost, auction_value=0):
        """Update Player to database"""
        player = self.get_player_by_code(code)
        if not player:
            player = self.get_temporary_object()
        player.code = int(code)
        player.name = name.strip()
        player.real_team = real_team.strip().upper()
        difference = player.auction_value - auction_value
        player.cost = int(cost)
        player.auction_value = auction_value
        if player.team and difference != 0:
            print("INFO: cost for player %s changed, budget of %s updated"
                  % (player.name, player.team.name))
            self.update_budget(player.team.name, difference)
        player.auction_value = int(auction_value)
        player.role = self.get_role_by_code(code).strip().lower()
        if auction_value:
            player.auction_value = auction_value
        self.session.commit()
        print("INFO: Player <%s> updated!" % player.name)

    def change_budgets(self, left_team_name, left_extra_budget,
                       right_team_name, right_extra_budget):
        """
        Change budgets after Player transfer between two teams
        """
        left_team = self.get_team_by_name(left_team_name)
        old_left_budget = left_team.budget
        left_team.budget += (int(right_extra_budget) - int(left_extra_budget))
        self.session.commit()
        print("INFO: team %s budget: %s --> %s" % (left_team, old_left_budget,
                                                   left_team.budget))
        right_team = self.get_team_by_name(right_team_name)
        old_right_budget = right_team.budget
        right_team.budget += (int(left_extra_budget) - int(right_extra_budget))
        self.session.commit()
        print("INFO: team %s budget: %s --> %s" % (right_team, old_right_budget,
                                                   right_team.budget))

    def split_players(self, left_team, left_player, left_extra,
                      right_team, right_player, right_extra):
        """split_players(left_team, left_player, left_extra,
                         right_team, right_player, right_extra) -> bool
        Split two players between two teams and update budgets
        if extra money are present during trade operation"""
        left_player = self.get_player_by_name(left_player)
        left_team = self.get_team_by_name(left_team)
        right_player = self.get_player_by_name(right_player)
        right_team = self.get_team_by_name(right_team)
        if left_team.max_trades < 1 or right_team.max_trades < 1:
            return "ERROR: no more trade operation remaining"
        elif left_team.budget < left_extra or right_team.budget < right_extra:
            return "ERROR: not enough money for extra offer"
        else:
            print("INFO: removing %s from team %s..." % (left_player,
                                                         left_team))
            left_team.players.remove(left_player)
            print("INFO: removing %s from team %s..." % (right_player,
                                                         right_team))
            right_team.players.remove(right_player)
            print("INFO: adding %s from team %s..." % (right_player, left_team))
            left_team.players.append(right_player)
            print("INFO: adding %s from team %s..." % (left_player, right_team))
            right_team.players.append(left_player)
            if left_extra:
                old_budget = right_team.budget
                new_budget = right_team.budget + left_extra
                print("INFO: update %s budget: %s -> %s" % (right_team,
                                                            old_budget,
                                                            new_budget))
            if right_extra:
                old_budget = left_team.budget
                new_budget = left_team.budget + right_extra
                print("INFO: update %s budget: %s -> %s" % (left_team,
                                                            old_budget,
                                                            new_budget))
            print("INFO: updating %s max trades remaining..." % left_team)
            left_team.max_trades -= 1
            print("INFO: updating %s max trades remaining..." % right_team)
            right_team.max_trades -= 1
            self.session.commit()
            return "INFO: trade operation done!"

    def rollback_session(self):
        """Rollback session"""
        self.session.rollback()

    @staticmethod
    def get_role_by_code(code):
        if int(code) < 200:
            role = 'goalkeeper'
        elif 200 <= int(code) < 500:
            role = 'defender'
        elif 500 <= int(code) < 800:
            role = 'midfielder'
        else:
            role = 'forward'
        return role


if __name__ == "__main__":
    m = Model()
