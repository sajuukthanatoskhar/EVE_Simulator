import dataclasses

import simpy


import numpy as np

from components.StellarComponents import StarSystem
from components.sim_constants import TIME_CONSTANT

@dataclasses.dataclass
class Commodity:
    name : str
    quantity : int

@dataclasses.dataclass
class HarvestedCommodity(Commodity):
    pass



class ProducedCommodity(Commodity):
    requiredCommodities = []

class PI_Colony:
    def __init__(self, env : simpy.Environment, planet):
        self.env = env
        self.location : StarSystem = planet.location
        self.planet = planet
        self.storage = simpy.Container(capacity=40000)
        self.currentoutput : float = np.random.randint(2500,5000)/TIME_CONSTANT
        self.produces = self.planet.productionoutput

    def set_output_rate_pi_colony(self, minrate, maxrate):
        """
        Sets teh output rate
        :param minrate:
        :param maxrate:
        :return:
        """
        if isinstance(minrate, float) and isinstance(maxrate, float):
            self.currentoutput = np.random.randint(minrate, maxrate)/TIME_CONSTANT
        else:
            raise TypeError('Invalid Types')

    def get_output_from_planet(self):
        self.storage.put(self.currentoutput)
        yield self.env.timeout(TIME_CONSTANT)

    def empty_planet(self) -> Commodity:
        commodity_to_get =  Commodity(self.produces, self.storage.level)
        self.storage.get(self.storage.level)
        return commodity_to_get

@dataclasses.dataclass
class MarketOrder:

    name : str
    qty : int
    owner : str
    price : float
    time_placed : float

    def __post_init__(self):
        self.init_qty = self.qty




    def create_marketorder(self, name, qty, owner, price, env : simpy.Environment):
        """
        Factory method
        :param name: Name of item being sold
        :param qty: quantity
        :param owner:
        :param env:
        :return:
        """
        return MarketOrder(name, qty, owner, price, env.now)