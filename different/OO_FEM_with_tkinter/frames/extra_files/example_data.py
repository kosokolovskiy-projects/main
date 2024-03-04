import numpy as np

lb = 15.0
r = 457.2 / 2000
t = 10 / 1000
A = np.pi * (r ** 2 - (r - t) ** 2)
E_modulus = 2.1e11

nodes_general = (
    (0, 0, lb * np.sqrt(2.0 / 3.0)),
    (0.0, lb / np.sqrt(3), 0),
    (-lb / 2, -lb / np.sqrt(12.0), 0),
    (lb / 2, -lb / np.sqrt(12.0), 0)
)

constraints_general = (
    (True, True, True),
    (False, False, False),
    (False, False, False),
    (True, True, False)
)

forces_general = (
    (0, -20e3, -100e3),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
)

displacements_general = (
    (0., 0., 0.),
    (0., 0., 0.),
    (0., 0., 0.),
    (0., 0., 0.)
)

connections_general = (
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 3),
    (3, 4),
    (2, 4)
)

elements_properties_general = (
    (E_modulus, A),
    (E_modulus, A),
    (E_modulus, A),
    (E_modulus, A),
    (E_modulus, A),
    (E_modulus, A)
)
