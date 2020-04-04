class RedisMock:
    __storage = None

    def __init__(self):
        self.__storage = {}

    def get(self, key):
        return self.__storage[key]

    def exists(self, key):
        return key in self.__storage

    def set(self, key, value):
        self.__storage[key] = value