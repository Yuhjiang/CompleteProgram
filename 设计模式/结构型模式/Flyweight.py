"""
享元模式
"""
import json
from typing import List, Dict


class FlyWeight:
    def __init__(self, shared_state: List) -> None:
        self._shared_state = shared_state

    def operation(self, unique_state: List) -> None:
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print(f'Flyweight: Displaying shared ({s}) and unique ({u}) state.', end='')


class FlyweightFactory:
    _flyweights: Dict[str, FlyWeight] = {}

    def __init__(self, initial_flyweights: List) -> None:
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = FlyWeight(state)

    def get_key(self, state: List) -> str:
        return '_'.join(sorted(state))

    def get_flyweight(self, shared_state: List) -> FlyWeight:
        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            print(f'FlyWeightFactory: Cant find a flyweight, creating new one.')
            self._flyweights[key] = FlyWeight(shared_state)
        else:
            print(f'FlyWeightFactory: Reusing existing flyweight.')

        return self._flyweights[key]

    def list_flyweights(self) -> None:
        count = len(self._flyweights)
        print(f'FlyWeightFactory: I have {count} flyweights')
        print('\n'.join(map(str, self._flyweights.keys())), end='')


def add_car_to_police_database(
        factory: FlyweightFactory, plates: str, owner: str, brand: str,
        model: str, color: str) -> None:
    print('\n\nClient: Adding a car to database.')
    flyweight = factory.get_flyweight([brand, model, color])

    flyweight.operation([plates, owner])


if __name__ == '__main__':
    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])

    factory.list_flyweights()

    add_car_to_police_database(factory, "CL234IR", "James Doe", "BMW", "M5", "red")

    add_car_to_police_database(factory, "CL234IR", "James Doe", "BMW", "X1", "red")

    print("\n")
    factory.list_flyweights()