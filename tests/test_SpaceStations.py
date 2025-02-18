import pytest
import simpy

from components.SpaceStations import Citadel


simenv = simpy.Environment()
class Test_Citadel:

    @pytest.fixture(autouse=True)
    def _Citadel_gen(self):
        self.test_citadel = Citadel(simenv, pop = 100,has_market= True)

    @pytest.mark.parametrize('attrtotest,deftype',[('env', simpy.Environment), ('pop', int), ('has_market', bool)])
    def test_citadel(self, attrtotest, deftype):
        assert hasattr(self.test_citadel, attrtotest)
        assert isinstance(getattr(self.test_citadel, attrtotest),deftype)


