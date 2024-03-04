import pandas as pd
from utils.Constraint import Constraint
from utils.Force import Force
from utils.Displacement import Displacement

from dataclasses import dataclass


@dataclass
class Node:
    __displ: Displacement = None
    __force: Force = None
    __constr: Constraint = None

    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

    @property
    def constr(self):
        if self.__constr is not None:
            return self.__constr
        else:
            raise Exception('There is no Constrains')

    @constr.setter
    def constr(self, constraint_obj: Constraint):
        self.__constr = (constraint_obj.u_1, constraint_obj.u_2, constraint_obj.u_3)
        return self.__constr


    @property
    def force(self):
        if self.__force is not None:
            return self.__force.force
        else:
            raise Exception('There is no Force')

    @force.setter
    def force(self, force_obj):
        self.__force = force_obj

    @property
    def displ(self):
        if self.__displ is not None:
            return self.__displ
        else:
            raise Exception('There is no Displacement')

    @displ.setter
    def displ(self, displ_obj):
        self.__displ = displ_obj

    def get_data(self):
        data = {'Displacement': self.__displ.displacement,
                'Force:': self.__force.force,
                'Constraint': [self.__constr[0], self.__constr[1], self.__constr[2]]
                }
        df = pd.DataFrame(data, index=['x_1', 'x_2', 'x_3'])
        return df.T

    def __str__(self):
        return (f'I am {self.__class__.__name__}  and I have the following properties:\n'
              f'Displacement: {self.__displ}\n'
              f'Force: {self.__force.force}\n'
              f'Constraint:: {self.__constr}\n')


if __name__ == '__main__':
    obj = Node(1, 2, 3)
