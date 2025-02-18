import random

import numpy as np
import simpy

from components.PoliticalEntities import Alliance
from components.SpaceStations import Citadel
from components.StellarComponents import StarSystem, Planet
from components.sim_constants import TIME_CONSTANT
from matplotlib import pyplot as plt

planet_materials = ['Metals','Gases','Water','Fuel']

if __name__ == '__main__':
    env = simpy.Environment()
    a_Citadel = Citadel(env, has_market=True, pop = 500, name="Main Staging 3T7")
    an_Alliance = Alliance(env, noofplayers=500)
    a_Starsystem = StarSystem(name="3T7-M8")

    a_Citadel.set_location(a_Starsystem)

    for planet in range(0,np.random.randint(1,13)):
        a_Starsystem.add_Planet(Planet(a_Starsystem, produces = random.choice(planet_materials)))

    an_Alliance.add_owned_citadel(a_Citadel)


    env.run(until=31*24 * TIME_CONSTANT)
    plt.plot(an_Alliance.pop_history, label='Alliance Population active')
    for an_activity in an_Alliance.get_alliance_activities_categories():
        plt.plot(an_Alliance.get_activity_type_history(an_activity), label=an_activity)


    plt.legend()


    plt.title('Alliance Activity Simulation')
    plt.ylabel('No of Pilots')
    plt.xlabel('Hour')
    plt.show()
