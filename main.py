import random

import numpy as np
import simpy

from components.PoliticalEntities import Alliance
from components.SpaceStations import Citadel
from components.StellarComponents import StarSystem, Planet
from components.sim_constants import TIME_CONSTANT
from matplotlib import pyplot as plt

HOURS_IN_DAY = 24

DAYS_IN_MONTH = 31

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


    env.run(until=DAYS_IN_MONTH * HOURS_IN_DAY * TIME_CONSTANT)
    plt.plot(an_Alliance.pop_history, label='Alliance Population active')
    for an_activity in an_Alliance.get_alliance_activities_categories():
        plt.plot(an_Alliance.get_activity_type_history(an_activity), label=an_activity)
    plt.legend()
    plt.title('Alliance Activity Simulation')
    plt.ylabel('No of Pilots')
    plt.xlabel('Hour')

    fig,ax1 = plt.subplots()
    ax1.set_xlabel('Time (hour of simulation)')
    ax1.set_ylabel('Number of transactions', color="tab:blue")
    ax1.plot(an_Alliance.total_player_transactions, label="Transactions", color="tab:blue")
    ax2 = ax1.twinx()
    ax2.set_ylabel('Total Economic Value of players',color="tab:red")
    ax2.plot(an_Alliance.total_economic_value, label="Total Economic Value of all players",color="tab:red")
    plt.legend()
    plt.title('Alliance Economic Report')


    plt.show()
