import numpy as np
from dataclasses import dataclass
import logging
import pandas as pd

from utils.Node import Node
from utils.Force import Force

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('log_folder/element.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.disabled = True

@dataclass
class Element:

    area: float = None
    eModulus: float = None
    dofNumbers: int = None

    def __init__(self, n1: Node, n2: Node, e: float, a: float,):
        self.n1 = n1
        self.n2 = n2
        self.area = a
        self.eModulus = e


    def computeStiffnessMatrix(self):
        return self.__prepare_matrix()

    def computeForce(self):
        return self.__prepare_force()

    def getLength(self):
        return np.sqrt((self.n2.x1 - self.n1.x1) ** 2 + (self.n2.x2 - self.n1.x2) ** 2 + (self.n2.x3 - self.n1.x3) ** 2)

    def getNode1(self) -> Node:
        return self.n1

    def getNode2(self) -> Node:
        return self.n2

    def getArea(self) -> float:
        return self.area

    def getEModulus(self) -> float:
        return self.eModulus

    def __prepare_matrix(self):
        ex = np.array([self.n1.x1 + self.n1.displ.displacement[0], self.n2.x1 + self.n2.displ.displacement[0]])
        ey = np.array([self.n1.x2 + self.n1.displ.displacement[1], self.n2.x2 + self.n2.displ.displacement[1]])
        ez = np.array([self.n1.x3 + self.n1.displ.displacement[2], self.n2.x3 + self.n2.displ.displacement[2]])
        ep = np.array([self.eModulus, self.area])
        Ke = self.bar3e(ex, ey, ez, ep)
        return Ke

    def __prepare_force(self):
        ex = np.array([self.n1.x1, self.n2.x1])
        ey = np.array([self.n1.x2, self.n2.x2])
        ez = np.array([self.n1.x3, self.n2.x3])
        ep = np.array([self.eModulus, self.area])
        ed = self.n1.displ.displacement + self.n2.displ.displacement
        forces = self.bar3s(ex, ey, ez, ep, ed)
        logger.debug(forces)
        return forces


    def bar3e(self, ex, ey, ez, ep):
        """
            Compute element STIFFNESS MATRIX for three dimensional bar element.

            :param list ex: element x coordinates [x1, x2]
            :param list ey: element y coordinates [y1, y2]
            :param list ez: element z coordinates [z1, z2]
            :param list ep: element properties [E, A], E - Young's modulus, A - Cross section area
            :return mat Ke: stiffness matrix, [6 x 6]
        """
        E = ep[0]
        A = ep[1]

        b = np.mat([
            [ex[1] - ex[0]],
            [ey[1] - ey[0]],
            [ez[1] - ez[0]]
        ])
        L = np.sqrt(b.T * b).item()

        n = np.asarray(b.T / L).reshape(3)

        G = np.mat([
            [n[0], n[1], n[2], 0., 0., 0.],
            [0., 0., 0., n[0], n[1], n[2]]
        ])

        Kle = E * A / L * np.mat([
            [1, -1],
            [-1, 1]
        ])

        return G.T * Kle * G

    def bar3s(self, ex, ey, ez, ep, ed):
        """
        Compute NORMAL FORCE in three dimensional bar element.

        :param list ex: element x coordinates [x1, x2]
        :param list ey: element y coordinates [y1, y2]
        :param list ez: element z coordinates [z1, z2]
        :param list ep: element properties [E, A], E - Young's modulus, A - Cross section area
        :param list ed: element displacements [u1, ..., u6]
        :return float N: normal force
        """
        E = ep[0]
        A = ep[1]

        b = np.mat([
            [ex[1] - ex[0]],
            [ey[1] - ey[0]],
            [ez[1] - ez[0]]
        ])
        # print(b)
        L = np.sqrt(b.T * b).item()

        # print(f'L = {L}')

        n = np.asarray(b.T / L).reshape(3)

        G = np.mat([
            [n[0], n[1], n[2], 0., 0., 0.],
            [0., 0., 0., n[0], n[1], n[2]]
        ])


        u = np.asmatrix(ed).T
        N = E * A / L * np.mat([[-1., 1.]]) * G * u

        return N.item()

    def get_data(self, n1=0, n2=0):
        if n1 == 1:
            print(self.n1.get_data(), end='\n\n')
        elif n2 == 1:
            print(self.n2.get_data(), end='\n\n')




