from dataclasses import dataclass


@dataclass
class Displacement:
    __displacement: tuple = None

    def __init__(self, displacement):
        self.__displacement = displacement

    @property
    def displacement(self):
        return self.__displacement

    @displacement.setter
    def displacement(self, obj):
        self.__displacement = obj

    def get_component(self, num):
        return self.displacement[num]

    def print_(self):
        print(self.displacement)


if __name__ == '__main__':
    obj = Displacement((1, 2, 3))
    print(obj.displacement)
    print(type(obj.displacement))
