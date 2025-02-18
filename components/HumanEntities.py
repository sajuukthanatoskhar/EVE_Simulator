from __future__ import annotations

import random

import simpy

import numpy as np

from components.EconomicEntities import PI_Colony, Commodity
from components.sim_constants import TIME_CONSTANT

pilot_activity_list = ['Mining','PvP','PI', '"Industry"', 'Ship Spinning']

class Timezone:

    def __init__(self, start : int, finish : int):
        self.start = start
        self.finish = finish
        self.isactive = False

    def get_timezone(self) -> tuple[int, int]:
        return self.start, self.finish

    def is_active(self, currenttime : float) -> None:
        self.isactive = self.start <= currenttime <= self.finish

    @staticmethod
    def create_random_timezone(PLAYERPLAYTIME):
        start = (np.random.randint(0,23))
        finish =(np.random.randint(start+1, start+PLAYERPLAYTIME))

        return Timezone((start%24)*TIME_CONSTANT, (finish%24)*TIME_CONSTANT)

class PI_ColonyManager:
    def __init__(self, no_of_colonies : int):
        self.max_colonies = no_of_colonies
        self.current_colonies : set[PI_Colony] = set()

    def add_colony(self, colony : PI_Colony):
        self.current_colonies.add(colony)

    def remove_colony(self, colony : PI_Colony):
        self.current_colonies.remove(colony)

    def get_outputs_of_all_colonies(self) -> list[Commodity]:
        resources = []
        for colony in self.current_colonies:
            resources.append(colony.empty_planet())
        return resources


class Player:

    def __init__(self, env, name ,  timezone : Timezone, current_alliance: Alliance):
        self.name = name
        self.timezone = timezone
        self.env  : simpy.Environment = env
        self.current_alliance : Alliance = current_alliance

        self.pi_colonymanager = PI_ColonyManager(no_of_colonies = np.random.randint(0,6))
        self.current_activity = 'idle'

        self.do_activities = self.env.process(self.do_activities_process())
        self.propensity = (1, 5, 3, 1,2)

    def set_pilot_activity_propensity(self, propensitytuple : tuple):
        self.propensity = propensitytuple

    def do_activities_process(self):
        while True:
            if self.is_active():
                self.do_activity()


            yield self.env.timeout(TIME_CONSTANT)


    def get_current_alliance(self) -> Alliance:
        return self.current_alliance

    def change_alliances(self, alliance : Alliance):
        self.current_alliance = alliance

    def is_active(self):
        start,finish = self.timezone.get_timezone()


        if start > finish:
            xval_finish = start+1 > (self.env.now % 2) <= finish
            #print(f"Ship is ready? {xval_finish} vs {finish}|{start+1}|{self.env.now % 2}")
        else:
            xval_finish = start < (self.env.now % 1) <= finish
            #print(f"Ship is ready? {xval_finish} vs {start}|{finish}|{self.env.now % 1}")
        return xval_finish

    @staticmethod
    def create_player(env, name = "aname", start = 0, finish = 8) -> Player:
        timezone = Timezone(start,finish)
        return Player(env, name, timezone)

    @staticmethod
    def create_player_with_random_timezone(env,alliance, name = "random_tz_player", hoursplayed = 8):
        return Player(env, name, Timezone.create_random_timezone(hoursplayed),alliance)

    def do_activity(self):
        self.current_activity = random.choices(pilot_activity_list, self.propensity, k=1)[0]
