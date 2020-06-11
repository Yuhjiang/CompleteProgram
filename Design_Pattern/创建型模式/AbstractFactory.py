from abc import ABC, abstractmethod


class AbstractProductA(ABC):
    @abstractmethod
    def useful_function_a(self) -> str:
        pass


class AbstractProductB(ABC):
    @abstractmethod
    def useful_function_b(self) -> str:
        pass

    @abstractmethod
    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        pass


class ConcreteProductA1(AbstractProductA):
    def useful_function_a(self) -> str:
        return 'The result of the product A1'


class ConcreteProductA2(AbstractProductA):
    def useful_function_a(self) -> str:
        return 'The result of the product A2'


class ConcreteProductB1(AbstractProductB):
    def useful_function_b(self) -> str:
        return 'The result of the product B1'

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f'Th result of the B1 collaborating with the ({result}'


class ConcreteProductB2(AbstractProductB):
    def useful_function_b(self) -> str:
        return 'The result of the product B2'

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f'Th result of the B2 collaborating with the ({result}'


class AbstractFactory(ABC):
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class ConcreteFactory1(AbstractFactory):
    def create_product_a(self) -> ConcreteProductA1:
        return ConcreteProductA1()

    def create_product_b(self) -> ConcreteProductB1:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    def create_product_a(self) -> ConcreteProductA2:
        return ConcreteProductA2()

    def create_product_b(self) -> ConcreteProductB2:
        return ConcreteProductB2()


def client_code(factory: AbstractFactory) -> None:
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()

    print(f'{product_b.useful_function_b()}')
    print(f'{product_b.another_useful_function_b(product_a)}')


if __name__ == '__main__':
    print('Client: Testing client code with the first factory type:')
    client_code(ConcreteFactory1())

    print('\n')
    print('Client: Testing client code with the second factory type:')
    client_code(ConcreteFactory2())
