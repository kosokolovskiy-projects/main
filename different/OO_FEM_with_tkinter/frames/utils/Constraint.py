from dataclasses import dataclass

@dataclass
class Constraint:
    u_1: bool = None
    u_2: bool = None
    u_3: bool = None

    def __str__(self):
        print(f'This object has the following attributes:\nu_1 = {self.u_1}\nu_2 = {self.u_2}\nu_3 = {self.u_3}')

    def isFree(self, number):
        pass


if __name__ == '__main__':
    obj = Constraint(1, 2, 0)
    obj.__str__()

