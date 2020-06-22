"""
观察者模式
https://refactoringguru.cn/design-patterns/observer/python/example
"""
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Observer(ABC):
    @abstractmethod
    def update(self, subject) -> None:
        pass


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


class ConcreteSubject(Subject):
    _state: int = None

    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print('Subject: Attatched an observer.')
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        print('Subject: Notifying observers...')
        for observer in self._observers:
            observer.update(self)

    def some_business_logic(self) -> None:
        print('Subject: Im doing something important')
        self._state = randrange(0, 10)

        print(f'Subject: My state has just changed to: {self._state}')
        self.notify()


class ConcreteObserverA(Observer):
    def update(self, subject: ConcreteSubject) -> None:
        if subject._state < 3:
            print('ConcreteObserverA: Reacted to the event')


class ConcreteObserverB(Observer):
    def update(self, subject: ConcreteSubject) -> None:
        if subject._state == 0 or subject._state >= 2:
            print('ConcreteObserverB: Reacted to the event')


if __name__ == '__main__':
    subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    subject.attach(observer_b)

    subject.some_business_logic()
    subject.some_business_logic()

    subject.detach(observer_a)

    subject.some_business_logic()