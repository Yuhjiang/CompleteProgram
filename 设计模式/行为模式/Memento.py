from abc import ABC, abstractmethod
from datetime import datetime
from random import sample
from string import ascii_letters, digits


class Memento(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_state(self) -> str:
        pass


class ConcreteMemento(Memento):
    def __init__(self, state: str) -> None:
        self._state = state
        self._date = str(datetime.now())[:9]

    def get_state(self) -> str:
        return self._state

    def get_name(self) -> str:
        return f'{self._date} / ({self._state[0:9]}...)'

    def get_date(self) -> str:
        return self._date


class Originator(object):
    _state = None

    def __init__(self, state: str) -> None:
        self._state = state
        print(f'Originator: My initial state is: {self._state}')

    def do_something(self) -> None:
        print('Originator: Im doing something important.')
        self._state = self._generate_random_string(30)
        print(f'Originator: and my state has changed to: {self._state}')

    def _generate_random_string(self, length: int = 10) -> str:
        return ''.join(sample(ascii_letters, length))

    def save(self) -> Memento:
        return ConcreteMemento(self._state)

    def restore(self, memento: Memento) -> None:
        self._state = memento.get_state()
        print(f'Originator: My state has changed to: {self._state}')


class Caretaker(object):
    def __init__(self, originator: Originator) -> None:
        self._mementos = []
        self._originator = originator

    def backup(self) -> None:
        print('Caretaker: Saving Originators state...')
        self._mementos.append(self._originator.save())

    def undo(self) -> None:
        if not self._mementos:
            return

        memento = self._mementos.pop()
        print(f'Caretaker: Restoring state to: {memento.get_name()}')
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()

    def show_history(self) -> None:
        print('Caretaker: Heres the list of mementos:')
        for memento in self._mementos:
            print(memento.get_name())


if __name__ == '__main__':
    originator = Originator('Super-duper-super-puper-super.')
    caretaker = Caretaker(originator)

    caretaker.backup()
    originator.do_something()

    caretaker.backup()
    originator.do_something()

    caretaker.backup()
    originator.do_something()

    caretaker.show_history()

    print('Client: Now, lets rollback\n')
    caretaker.undo()

    print('Client: Now, lets rollback\n')
    caretaker.undo()

    caretaker.show_history()
