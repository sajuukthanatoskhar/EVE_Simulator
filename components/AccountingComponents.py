from __future__ import annotations

import simpy

# from components.HumanEntities import Player
# from components.PoliticalEntities import PlayerGroup


class TransactionEntry:
    def __init__(self, from_who, to_who, item_bought, quantity, money_amount):
        self.source_entity = from_who
        self.destination_entity = to_who
        self.item : str = item_bought
        self.quantity = quantity
        self.total_value = money_amount


class WalletLog():
    def __init__(self):
        self.log_history : list[TransactionEntry] = []


    def add_to_log(self, aTransactionEntry : TransactionEntry):
        self.log_history.append(aTransactionEntry)


class Wallet(simpy.Container):
    def __init__(self, env : simpy.Environment, initialcash):
        super().__init__(env, init=initialcash)
        self.transactionhistory = WalletLog()


    def make_payment_to(self, source : str, destination : str, moneyamount : float,
                             item : str, quantity):
        aTransactionEntry = TransactionEntry(source, destination, item, quantity, -1*moneyamount)
        self.transactionhistory.add_to_log(aTransactionEntry)

    def receive_payment_from(self, source : str, destination : str, moneyamount : float,
                             item : str, quantity):
        aTransactionEntry = TransactionEntry(source, destination, item, quantity, moneyamount)
        self.transactionhistory.add_to_log(aTransactionEntry)

    def give_transfer(self, amount : float):
        self.get(amount)

    def get_transfer(self, amount : float):
        self.put(amount)

class PlayerWallet(Wallet):
    def __init__(self,env : simpy.Environment, initialcash = 100000000):
        super().__init__(env,initialcash)
