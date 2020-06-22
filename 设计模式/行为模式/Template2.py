"""
模版方法
https://refactoringguru.cn/design-patterns/template-method/python/example
"""
from abc import ABC, abstractmethod


class AbstractClass(ABC):
    def template_method(self) -> None:
        self.base_operation1()
        self.required_operations1()
        self.base_operation2()
        self.hook1()
        self.required_operations2()
        self.base_operation3()
        self.hook2()


    def base_operation1(self) -> None:
        print('AbstractClass says: I am doing the bulk of the work')

    def base_operation2(self) -> None:
        print('AbstractClass says: But I let subclasses override some operations')

    def base_operation3(self) -> None:
        print('AbstractClass says: But I am doing the bulk of the work anyway')

    @abstractmethod
    def required_operations1(self) -> None:
        pass

    @abstractmethod
    def required_operations2(self) -> None:
        pass

    def hook1(self) -> None:
        pass

    def hook2(self) -> None:
        pass


class ConcreteClass1(AbstractClass):
    def required_operations1(self) -> None:
        print('ConcreteClass1 says: Implemented Operation1')

    def required_operations2(self) -> None:
        print('ConcreteClass1 says: Implemented Operation2')


class ConcreteClass2(AbstractClass):
    def required_operations1(self) -> None:
        print('ConcreteClass2 says: Implemented Operation1')

    def required_operations2(self) -> None:
        print('ConcreteClass2 says: Implemented Operation2')


def client_code(abstract_class: AbstractClass) -> None:
    abstract_class.template_method()


if __name__ == '__main__':
    print('Same client code can work with different subclasses:')
    client_code(ConcreteClass1())

    print('Same client code can work with different subclasses:')
    client_code(ConcreteClass2())
