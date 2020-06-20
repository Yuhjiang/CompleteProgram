"""
生成器模式
"""
from abc import ABC, abstractmethod, abstractproperty
from typing import Any


class Product1(object):
    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f'Product parts: {", ".join(self.parts)}', end='')


class Builder(ABC):

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass


class ConcreteBuilder1(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self) -> Product1:
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add('PartA1')

    def produce_part_b(self) -> None:
        self._product.add('PartB1')

    def produce_part_c(self) -> None:
        self._product.add('PartC1')


class ConcreteBuilder2(Builder):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self) -> Product1:
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add('PartA2')

    def produce_part_b(self) -> None:
        self._product.add('PartB2')

    def produce_part_c(self) -> None:
        self._product.add('PartC2')


class Director(object):
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_viable_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()


if __name__ == '__main__':
    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    print('Standard basic product: ')
    director.build_minimal_viable_product()
    builder.product.list_parts()

    print('\n')
    print('Standard full featured product: ')
    director.build_full_viable_product()
    builder.product.list_parts()

    print('\n')
    print('Custom product: ')
    builder.produce_part_a()
    builder.produce_part_b()
    builder.product.list_parts()

    print('\n')
    builder.product.list_parts()