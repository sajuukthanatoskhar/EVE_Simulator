
from __future__ import annotations

from components.sim_constants import TIME_CONSTANT


class StarSystem:


    def __init__(self, name, star_system_links : set[StarSystem]= []):
        self.name = name
        self.star_system_links : set[StarSystem] = star_system_links
        self.planets = set()

    def set_name(self, name):
        self.name = name

    def add_link(self, starsystemlink : StarSystem):
        self.star_system_links.add(starsystemlink)

    def add_Planet(self, a_Planet : Planet):


        self.planets.add(a_Planet)

class Planet:

    def __init__(self, location : StarSystem, produces = "Metals"):
        self.location : StarSystem = location

        self.name = f"{self.location.name}-P{len(self.location.planets) + 1}"
        self.productionoutput = produces









