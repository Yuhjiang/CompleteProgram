from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler(ABC):
    """
    处理器接口，用于构建处理链
    """
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler

        return handler

    @abstractmethod
    def handle(self, request: Any) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


class MonkeyHandler(AbstractHandler):
    def handle(self, request: Any) -> Optional[str]:
        if request == 'Banana':
            return f'Monkey: I\'ll eat the {request}'
        else:
            return super().handle(request)


class SquirrelHandler(AbstractHandler):
    def handle(self, request: Any) -> Optional[str]:
        if request == 'Nut':
            return f'Squirrel: I\'ll eat the {request}'
        else:
            return super().handle(request)


class DogHandler(AbstractHandler):
    def handle(self, request: Any) -> Optional[str]:
        if request == 'MeatBall':
            return f'Dog: I\'ll eat the {request}'
        else:
            return super().handle(request)


def client_code(handler: Handler) -> None:
    for food in ['Nut', 'Banana', 'Cup of coffee']:
        print(f'\nClient: Who wants a {food}')
        result = handler.handle(food)
        if result:
            print(f'    {result}', end='')
        else:
            print(f'    {food} was left untouched.', end='')


if __name__ == '__main__':
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)

    print('Chain: Monkey -> Squirrel -> Dog')
    client_code(monkey)
    print('\n')

    print('Chain: Squirrel -> Dog')
    client_code(squirrel)
