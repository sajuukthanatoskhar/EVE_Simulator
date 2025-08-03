import dataclasses

import simpy
from simpy.resources import container


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

class MarketOrder(container.Container):

    def __init__(self, env: simpy.Environment, name, qty, owner="An Owner", price=1.00, time_placed = None):
        super().__init__(env, init=qty)
        self.name : str = name
        self.init_qty : int = qty
        self.owner : str = owner
        self.price : float = price
        self.time_placed : float = env.now if not time_placed else time_placed



    def create_marketorder(self,env : simpy.Environment, name, qty, owner, price, ):
        """
        Factory method
        :param name: Name of item being sold
        :param qty: quantity
        :param owner:
        :param env:
        :return:
        """
        return MarketOrder(env, name, qty, owner, price, env.now)


# def run_example(env : simpy.Environment, market_order: MarketOrder):
#     while(market_order.level > 0):
#         market_order.get(500)
#         print(f"{market_order.name} {market_order.level}")
#         yield env.timeout(1)
#
#
#
# if __name__ == '__main__':
#     env = simpy.Environment()
#
#     a_Market_order = MarketOrder(env,"Tritanium", 5000, "Owner", 1.5)
#     env.process(run_example(env, a_Market_order))
#     #print(a_Market_order.get(2000))
#     env.run()