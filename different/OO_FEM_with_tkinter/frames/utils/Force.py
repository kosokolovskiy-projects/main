from dataclasses import dataclass

@dataclass
class Force:
    __force: tuple = None

    def __init__(self, force):
        self.__force = force

    @property
    def force(self):
        return self.__force

    @force.setter
    def force(self, obj):
        self.__force = obj


    def get_component(self, num):
        return self.force[num]

    def print_(self):
        print(self.force)

if __name__ == '__main__':
    obj = Force((1, 2))
    print(obj.force)
    print(type(obj.force))