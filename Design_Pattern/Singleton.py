class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance


if __name__ == '__main__':
    s1 = Singleton()
    s2 = Singleton()
    print(id(s1), id(s2))