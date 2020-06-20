"""
模版方法模式
"""
from abc import ABCMeta, abstractmethod


class Compiler(metaclass=ABCMeta):
    @abstractmethod
    def collect_source(self):
        pass

    @abstractmethod
    def compile_to_object(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def compile_and_run(self):
        self.collect_source()
        self.compile_to_object()
        self.run()


class IOSCompile(Compiler):
    def collect_source(self):
        print('Collecting Swift Source Code')

    def compile_to_object(self):
        print('Compiling Swift Code to LLVM bitcode')

    def run(self):
        print('Program running on running environment')


"""
旅行社
"""
class Trip(metaclass=ABCMeta):
    @abstractmethod
    def set_transport(self):
        pass

    @abstractmethod
    def day1(self):
        pass

    @abstractmethod
    def day2(self):
        pass

    @abstractmethod
    def day3(self):
        pass

    @abstractmethod
    def return_home(self):
        pass

    def itinerary(self):
        self.set_transport()
        self.day1()
        self.day2()
        self.day3()
        self.return_home()


class VeniceTrip(Trip):
    def set_transport(self):
        print('Take a boat and find your way in the Grand Canal')

    def day1(self):
        print(f'day one in {type(self).__name__}')

    def day2(self):
        print(f'day two in {type(self).__name__}')

    def day3(self):
        print(f'day three in {type(self).__name__}')

    def return_home(self):
        print('Get souvenirs for friends and get back')


class MaldivesTrip(Trip):
    def set_transport(self):
        print('On foot, on any island')

    def day1(self):
        print(f'day one in {type(self).__name__}')

    def day2(self):
        print(f'day two in {type(self).__name__}')

    def day3(self):
        print(f'day three in {type(self).__name__}')

    def return_home(self):
        print('Dont feel like leaving the beach')


class TravelAgency:
    def arrange_trip(self):
        choice = input('What kind of place you\'d like')
        if choice == 'historical':
            self.trip = VeniceTrip()
            self.trip.itinerary()
        if choice == 'beach':
            self.trip = VeniceTrip()
            self.trip.itinerary()


if __name__ == '__main__':
    # ios = IOSCompile()
    # ios.compile_and_run()
    TravelAgency().arrange_trip()
