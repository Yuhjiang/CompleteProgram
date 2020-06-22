"""
访问者模式
https://refactoringguru.cn/design-patterns/visitor/python/example
"""
from abc import ABC, abstractmethod
from typing import List


class Component(ABC):
    @abstractmethod
    def accept(self, visitor) -> None:
        pass


class ConcreteComponentA(Component):
    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_a(self)

    def exclusive_method_of_concrete_component_a(self) -> str:
        return 'A'


class ConcreteComponentB(Component):
    def accept(self, visitor) -> None:
        visitor.visit_concrete_component_b(self)

    def exclusive_method_of_concrete_component_b(self) -> str:
        return 'B'


class Visitor(ABC):
    @abstractmethod
    def visit_concrete_component_a(self, element: ConcreteComponentA) -> None:
        pass

    @abstractmethod
    def visit_concrete_component_b(self, element: ConcreteComponentB) -> None:
        pass


class ConcreteVisitor1(Visitor):
    def visit_concrete_component_a(self, element: ConcreteComponentA) -> None:
        print(f'{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor1')

    def visit_concrete_component_b(self, element: ConcreteComponentB) -> None:
        print(f'{element.exclusive_method_of_concrete_component_b()} + ConcreteVisitor1')


class ConcreteVisitor2(Visitor):
    def visit_concrete_component_a(self, element: ConcreteComponentA) -> None:
        print(
            f'{element.exclusive_method_of_concrete_component_a()} + ConcreteVisitor2')

    def visit_concrete_component_b(self, element: ConcreteComponentB) -> None:
        print(
            f'{element.exclusive_method_of_concrete_component_b()} + ConcreteVisitor2')


def client_code(components: List[Component], visitor: Visitor) -> None:
    for component in components:
        component.accept(visitor)


if __name__ == "__main__":
    components = [ConcreteComponentA(), ConcreteComponentB()]
    print('The client code works with all visitors via the base Visitor interface:')
    visitor1 = ConcreteVisitor1()
    client_code(components, visitor1)

    print('It allows the same client code to work with different types of visitors:')
    visitor2 = ConcreteVisitor2()
    client_code(components, visitor2)
