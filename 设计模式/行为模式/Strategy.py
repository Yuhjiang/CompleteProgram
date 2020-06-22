"""
策略模式
https://refactoringguru.cn/design-patterns/strategy/python/example
"""
from typing import List
from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def do_algorithm(self, data: List):
        pass


class Context(object):
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def do_some_business_logic(self) -> None:
        print('Context: Sorting data using the strategy (not sure how itll do it)')
        result = self._strategy.do_algorithm(['a', 'b', 'c', 'd', 'e'])
        print(','.join(result))


class ConcreteStrategyA(Strategy):
    def do_algorithm(self, data: List) -> List:
        return sorted(data)


class ConcreteStrategyB(Strategy):
    def do_algorithm(self, data: List) -> List:
        return list(reversed(sorted(data)))


if __name__ == '__main__':
    context = Context(ConcreteStrategyA())
    context.do_some_business_logic()
    print()

    print('Client: Strategy is set to reverse sorting')
    context.strategy = ConcreteStrategyB()
    context.do_some_business_logic()
