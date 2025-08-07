import pytest
import hypothesis as ht
import hypothesis.strategies as st
import simpy

from components import HumanEntities


@pytest.fixture
def log():
    return []


@pytest.fixture
def env():
    return simpy.Environment()


