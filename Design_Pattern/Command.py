"""
命令设计模式
"""
from abc import ABCMeta, abstractmethod


class Wizard(object):
    def __init__(self, src: str, root_dir: str):
        self.choices = []
        self.root_dir = root_dir
        self.src = src

    def preference(self, command):
        self.choices.append(command)

    def execute(self):
        for choice in self.choices:
            if list(choice.values())[0]:
                print('Copy binaries --', self.src, ' to ', self.root_dir)
            else:
                print('no operation')


class StockTrade:
    def buy(self):
        print('You will buy stocks')

    def sell(self):
        print('You will sell stocks')


class Order(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


class BuyStockOrder(Order):
    def __init__(self, stock: StockTrade):
        self.stock = stock

    def execute(self):
        self.stock.buy()


class SellStockOrder(Order):
    def __init__(self, stock: StockTrade):
        self.stock = stock

    def execute(self):
        self.stock.sell()


class Agent:
    def __init__(self):
        self.__order_queue = []

    def place_order(self, order):
        self.__order_queue.append(order)
        order.execute()


if __name__ == '__main__':
    # wizard = Wizard('test.zip', '/usr/bin')
    # wizard.preference({'Python': True})
    # wizard.preference({'Java': False})
    # wizard.execute()
    stock = StockTrade()
    buy_stock = BuyStockOrder(stock)
    sell_stock = SellStockOrder(stock)

    agent = Agent()
    agent.place_order(buy_stock)
    agent.place_order(sell_stock)
