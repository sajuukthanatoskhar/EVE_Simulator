

import simpy
import numpy as np
from components.EconomicEntities import MarketOrder
from components.HumanEntities import Player, Timezone
from components.StellarComponents import StarSystem
from components.sim_constants import TIME_CONSTANT

PLAYERPLAYTIME = 4


class Marketplace:
    def __init__(self):
        self.orders : MarketOrder = []


    def add_order(self, an_order : MarketOrder):
        self.orders

class Citadel:


    def __init__(self, env : simpy.Environment, pop : int = 100, has_market : bool = True, name = "A Station"):
        self.has_market = has_market
        self.pop = pop
        self.env = env
        self.name = name
        self.pop_history = []
        self.location = None
        if self.has_market:
            self.market = Marketplace()

    def set_location(self, star_system : StarSystem):
        self.location : StarSystem = star_system

