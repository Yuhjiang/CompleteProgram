class Singleton(object):
    def __new__(cls, *args, **kwargs):
        """
        new是生成实例的过程
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance


class LazySingleton(object):
    __instance = None

    def __init__(self):
        if not LazySingleton.__instance:
            print('__init__ method called...')
        else:
            print('Instance already created')

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = LazySingleton()
        return cls.__instance


def singleton(cls, *args, **kwargs):
    _instance = {}

    def _singleton():
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


class Decorate(object):
    __instance = {}

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        if self._cls not in self.__instance:
            self.__instance[self._cls] = self._cls(*args, **kwargs)
        return self.__instance[self._cls]


@Decorate
class DecorateSingleton(object):
    def __init__(self, name):
        self.name = name
        print(name)
        pass

"""
使用metaclass定义类的创建行为
"""


class MetaSingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MetaSingleton(metaclass=MetaSingletonType):
    def __init__(self):
        pass


if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()
    print(id(s1), id(s2))

    s1 = DecorateSingleton(123)
    s2 = DecorateSingleton(234)
    print(id(s1), id(s2))

    print(MetaSingleton(), MetaSingleton())