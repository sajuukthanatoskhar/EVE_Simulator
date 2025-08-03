import simpy,pytest


from components.EconomicEntities import MarketOrder

def run_market_order_example(env : simpy.Environment, market_order: MarketOrder):
    """"""
    while(market_order.level > 0):
        market_order.get(500)
        print(f"{market_order.name} {market_order.level}")
        yield env.timeout(1)

def test_market_order(env):
    """
    Tests the basic initialisation and inventory reduction of a market order
    :param env:
    :return:
    """
    a_Market_order = MarketOrder(env,"Tritanium", 5000, "Owner", 1.5)
    env.process(run_market_order_example(env, a_Market_order))
    assert a_Market_order.name == "Tritanium"
    assert a_Market_order.level == 5000
    env.run()

    assert a_Market_order.level == 0