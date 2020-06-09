from abc import ABC, abstractmethod


class Creator(ABC):
    @abstractmethod
    def factory_method(self):
        pass

    def some_operation(self) -> str:
        product = self.factory_method()
        result = f'Creator: The same creator\'s code has just worked ' \
                 f'with {product.operation()}'

        return result


class Product(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass


class ConcreteProduct1(Product):
    def operation(self) -> str:
        return f'Result of the ConcreteProduct1'


class ConcreteProduct2(Product):
    def operation(self) -> str:
        return f'Result of the ConcreteProduct2'


class ConcreteCreator1(Creator):
    def factory_method(self) -> ConcreteProduct1:
        return ConcreteProduct1()


class ConcreteCreator2(Creator):
    def factory_method(self) -> ConcreteProduct2:
        return ConcreteProduct2()


def client_code(creator: Creator) -> None:
    print(f'Client: I\'m not aware of the creators class, but it still works.\n'
          f'{creator.some_operation()}', end='')


if __name__ == '__main__':
    print('App: Launched with the ConcreteCreator1.')
    client_code(ConcreteCreator1())
    print('\n')

    print('App: Launched with the ConcreteCreator2.')
    client_code(ConcreteCreator2())
