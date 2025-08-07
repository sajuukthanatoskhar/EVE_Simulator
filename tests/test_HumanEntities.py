import pytest
import hypothesis as ht
import hypothesis.strategies as st
import simpy
from components import HumanEntities


import matplotlib.pyplot as plt

from components.HumanEntities import Timezone, DEFAULT_PILOT_PROPENSITY
from components.PoliticalEntities import Alliance
from components.SpaceStations import PLAYERPLAYTIME

TYPES_OF_PILOT_ACTIVITIES = 5


# @ht.given(timezoneduration = st.integers(2,8))
def test_create_timezone():
    created_timezones = []
    for timezonescreated in range(0, 500):
        a_timezone = HumanEntities.Timezone.create_random_timezone(8)

        timezonerange = a_timezone.get_timezone()
        print(f"Timezone Range = {timezonerange}")

        timezonerange = timezonerange[1] - timezonerange[1]
        if timezonerange < 0:
            timezonerange += 24

        assert 0 <= timezonerange <= 8
        created_timezones.append(a_timezone)

    return get_timezonedata(created_timezones)

    plt.plot(x, y, '-')
    plt.show()


def get_timezonedata(created_timezones):
    x = list(range(0, 24))
    y = [0 for i in range(0, 24)]
    for xval in x:
        for a_timezone in created_timezones:
            timezone = a_timezone.get_timezone()
            if is_active(timezone, xval):
                y[xval] += 1
    return y


def is_active(timezone, xval):
    return timezone[0] < xval <= timezone[1]


@pytest.fixture
def create_example_player():
    return HumanEntities.Player(simpy.Environment(), "Test Pilot", Timezone.create_random_timezone(PLAYERPLAYTIME), "Test Alliance")


class Test_PlayerU_F:



    def test_set_pilot_activity_propensity(self, create_example_player):
        assert len(create_example_player.propensity) == TYPES_OF_PILOT_ACTIVITIES
        assert create_example_player.propensity is DEFAULT_PILOT_PROPENSITY
        create_example_player.set_pilot_activity_propensity((0,0,1,2,3))
        assert create_example_player.propensity is not DEFAULT_PILOT_PROPENSITY



    def test_do_activities_process(self, create_example_player):




        assert False

    def test_get_current_alliance(self):
        assert False

    def test_change_alliances(self):
        assert False

    def test_is_active(self):
        assert False

    def test_create_player(self):
        assert False

    def test_create_player_with_random_timezone(self):
        assert False

    def test_do_activity(self):
        assert False
