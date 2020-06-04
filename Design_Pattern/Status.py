"""
状态模式
"""
from abc import abstractmethod, ABCMeta


# class State(metaclass=ABCMeta):
#     @abstractmethod
#     def handle(self):
#         pass
#
#
# class ConcreteStateA(State):
#     def handle(self):
#         print(f'{type(self).__name__}')
#
#
# class ConcreteStateB(State):
#     def handle(self):
#         print(f'{type(self).__name__}')
#
#
# class Context(State):
#     def __init__(self):
#         self.state = None
#
#     def get_state(self):
#         return self.state
#
#     def set_state(self, state: State):
#         self.state = state
#
#     def handle(self):
#         self.state.handle()


class State(metaclass=ABCMeta):
    @abstractmethod
    def do_this(self):
        pass


class StartState(State):
    def do_this(self):
        print('TV Switching ON...')


class StopState(State):
    def do_this(self):
        print('TV Switching OFF...')


class TVContext(State):
    def __init__(self):
        self.state = None

    def get_state(self):
        return self.state

    def set_state(self, state: State):
        self.state = state

    def do_this(self):
        self.state.do_this()


class ComputeState(object):
    name = 'state'
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            print(f'Current: {self} => switched to new state {state.name}')
            self.__class__ = state
        else:
            print(f'Current: {self} => switching to {state.name} not possible')

    def __str__(self):
        return self.name


class Off(ComputeState):
    name = 'off'
    allowed = ['on']


class On(ComputeState):
    name = 'on'
    allowed = ['off', 'suspend', 'hibernate']


class Suspend(ComputeState):
    name = 'suspend'
    allowed = ['on']


class Hibernate(ComputeState):
    name = 'hibernate'
    allowed = ['on']


class Computer(object):
    def __init__(self, model='HP'):
        self.model = model
        self.state = Off()

    def change(self, state):
        self.state.switch(state)


if __name__ == '__main__':
    # context = Context()
    # state_a = ConcreteStateA()
    # state_b = ConcreteStateB()
    #
    # context.set_state(state_a)
    # context.handle()
    # ------------------------------
    # context = TVContext()
    # context.get_state()
    #
    # start = StartState()
    # context.set_state(start)
    # context.do_this()
    # stop = StopState()
    # context.set_state(stop)
    # context.do_this()
    # ------------------------------
    comp = Computer()
    comp.change(On)

    comp.change(Off)

    comp.change(On)
    comp.change(Suspend)
    comp.change(Hibernate)
    comp.change(On)
    comp.change(Off)