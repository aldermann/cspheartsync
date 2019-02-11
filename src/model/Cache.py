class Cache:
    __data = []
    __max_size = []

    def __init__(self, size=50):
        self.__max_size = size

    def put(self, data):
        self.__data.append(data)
        if len(self.__data) == self.__max_size:
            self.__data.pop(0)

    def empty(self):
        self.__data = []

    def check_in_cache(self, data):
        return data in self.__data

