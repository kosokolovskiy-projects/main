import matplotlib.pyplot as plt
import numpy as np

from utils.Constraint import Constraint
from utils.Displacement import Displacement
from utils.Element import Element
from utils.Force import Force
from utils.Node import Node
from utils.Structure import Structure

lb = 15.0
r = 457.2 / 2000
t = 10 / 1000
A = np.pi * (r ** 2 - (r - t) ** 2)
E_modulus = 2.1e11

node_1 = Node(0, 0, lb * np.sqrt(2.0 / 3.0))
node_2 = Node(0.0, lb / np.sqrt(3), 0)
node_3 = Node(-lb / 2, -lb / np.sqrt(12.0), 0)
node_4 = Node(lb / 2, -lb / np.sqrt(12.0), 0)

node_1.constr = Constraint(True, True, True)
node_2.constr = Constraint(False, False, False)
node_3.constr = Constraint(False, False, False)
node_4.constr = Constraint(True, True, False)

node_1.force = Force((0, -20e3, -100e3))
node_2.force = Force((0, 0, 0))
node_3.force = Force((0, 0, 0))
node_4.force = Force((0, 0, 0))

node_1.displ = Displacement((0., 0., 0.))
node_2.displ = Displacement((0., 0., 0.))
node_3.displ = Displacement((0., 0., 0.))
node_4.displ = Displacement((0., 0., 0.))

element_1 = Element(node_1, node_2, E_modulus, A)
element_2 = Element(node_1, node_3, E_modulus, A)
element_3 = Element(node_1, node_4, E_modulus, A)
element_4 = Element(node_2, node_3, E_modulus, A)
element_5 = Element(node_3, node_4, E_modulus, A)
element_6 = Element(node_2, node_4, E_modulus, A)

connection_str = (('node_1', 'node_2'), ('node_1', 'node_3'), ('node_1', 'node_4'),
                  ('node_2', 'node_3'), ('node_3', 'node_4'), ('node_2', 'node_4'))
structure = Structure(connection_str, element_1, element_2, element_3, element_4, element_5, element_6)

for one_connect in connection_str:
    structure.add_element(one_connect)

structure.create_connections_nodes()

structure.create_r0()

fig, ax = plt.subplots(dpi=100)

for i in range(1):

    if i == 0:
        pass
        #structure.visualize(fig, 0, ax)
    structure.create_global_matrix()

    structure.solution()
    structure.print_results()
    # structure.visualize_deformed(fig, 0, ax)

