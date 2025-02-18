import pytest
from components import HumanEntities
import simpy
import hypothesis as ht
import hypothesis.strategies as st

import matplotlib.pyplot as plt


#@ht.given(timezoneduration = st.integers(2,8))
def test_create_timezone():
    created_timezones = []
    for timezonescreated in range(0,500):
        a_timezone = HumanEntities.Timezone.create_random_timezone(8)

        timezonerange = a_timezone.get_timezone()
        print(f"Timezone Range = {timezonerange}")

        timezonerange = timezonerange[1] - timezonerange[1]
        if timezonerange < 0:
            timezonerange += 24

        assert 0 <= timezonerange <= 8
        created_timezones.append(a_timezone)

    return get_timezonedata(created_timezones)

    plt.plot(x,y, '-')
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



