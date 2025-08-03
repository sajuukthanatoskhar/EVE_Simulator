from collections import Counter

import simpy

from components.AccountingComponents import Wallet
from components.HumanEntities import Player
from components.SpaceStations import Citadel
from components.sim_constants import TIME_CONSTANT

STARTING_CORPORATION_MONEY = 50000000


class PlayerGroup:
    """
    A Corporation!
    """
    def __init__(self, env : simpy.Environment, noofplayers = 50, name = "A Playergroup", startingcash =STARTING_CORPORATION_MONEY):

        self.noofplayers = noofplayers
        self.name = name
        self.env = env
        self.players = [Player.create_player_with_random_timezone(env, self,f'RandomPilot{player}', 6) for player in range(self.noofplayers)]
        self.pop_history = []
        self.activity_history = []
        self.Wallet = Wallet(self.env, startingcash)

    def remove_players(self, noofplayers_to_remove: int):
        for player in range(noofplayers_to_remove):
            self.players.pop()

    def add_players(self, noofplayerstoadd):
        playerslen = len(self.players)
        for player in range(noofplayerstoadd):
            self.players.append(f'RandomPilot{player+playerslen}')

class Alliance(PlayerGroup):
    def __init__(self,env, noofplayers):
        super().__init__(env,noofplayers, name="An Alliance")

        self.total_player_transactions : list[int] = []
        self.total_economic_value : list[float] = []
        self.owned_Citadels : list[Citadel] = []
        self.env.process(self.alliance_things())

    def get_total_alliance_economic_value(self) -> float:
        return sum([player.Wallet.level for player in self.players])

    def get_total_alliance_wallet_transfers(self) -> int:
        return sum([len(player.Wallet.transactionhistory.log_history) for player in self.players])

    def get_alliance_activities_categories(self)-> set:
        return set(activity for counter in self.activity_history for activity in counter.keys())

    def alliance_things(self):
        while(True):
            print(f"{self.env.now:0.2f}: There are {self.get_active_pilots()} Pilots active in {self.name}")
            self.pop_history.append(self.get_active_pilots())
            self.activity_history.append((self.survey_activities()))
            self.total_economic_value.append(self.get_total_alliance_economic_value())
            if len(self.total_player_transactions):
                instantaneous_wallet_xfer_count = self.get_total_alliance_wallet_transfers()-sum(self.total_player_transactions)
                self.total_player_transactions.append(instantaneous_wallet_xfer_count)
            else:
                self.total_player_transactions.append(self.get_total_alliance_wallet_transfers())
            yield self.env.timeout(TIME_CONSTANT)


    def add_owned_citadel(self, a_citadel : Citadel) -> None:
        self.owned_Citadels.append(a_citadel)

    def remove_owned_citadel(self, a_Citadel):
        for n,cit in enumerate(self.owned_Citadels):
            if self.owned_Citadels[n] == a_Citadel:
                self.owned_Citadels.pop(n)
                break


    def get_active_pilots(self):
        return sum([1 for pilot in self.players if pilot.is_active()])

    def survey_activities(self):
        activitylist = []
        for pilot in self.players:
            if pilot.is_active():
                activitylist.append(pilot.current_activity)

        activity_counter = Counter(activitylist)
        print(f"Activities -> {activity_counter}")
        return activity_counter




    def get_activity_type_history(self, activity : str):
        return [activity_participants.get(activity,0)  for activity_participants in self.activity_history]

