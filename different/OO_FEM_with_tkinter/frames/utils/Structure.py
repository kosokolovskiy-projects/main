import numpy as np
import pandas as pd
import logging

import matplotlib.pyplot as plt
from utils.Force import Force
from utils.Element import Element
from Visualization import Plot_creator as plcr
from utils.Displacement import Displacement
# from arclength import ArcLengthClass
from arclength_method_functions import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('log_folder/structure.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# logger.disabled = True


class Structure:
    __force: dict = {}
    __bc: dict = {}
    __K_global = None
    __a = None
    __r = None
    __nodes: dict = {}
    di_1 = {}
    di_2 = {}
    counter: int = 1
    u_n = None
    u_n_1 = None
    force_elements: dict = {}

    def __init__(self, connection, *args):
        self.connections = connection
        self.elements = [elem for elem in args]

    @property
    def nodes(self):
        return self.__nodes

    def add_element(self, names):
        self.__nodes[names[0]] = (int(names[0][-1]) * 3 - 2, int(names[0][-1]) * 3 - 1, int(names[0][-1]) * 3)
        self.__nodes[names[1]] = (int(names[1][-1]) * 3 - 2, int(names[1][-1]) * 3 - 1, int(names[1][-1]) * 3)

    def nodes_info(self):
        d = {}
        for idx, (node_first, node_second) in enumerate(self.connections):
            if node_first not in d:
                print(node_first.title().replace('_', ' '))
                self.elements[idx].get_data(1, 0)
                d[node_first] = 0
            if node_second not in d:
                print(node_second.title().replace('_', ' '))
                self.elements[idx].get_data(0, 1)
                d[node_second] = 0

    def __bc_func(self):

        if self.counter == 1:
            for idx, elem in enumerate(self.elements):
                self.__bc[self.connections[idx][0]] = (
                    elem.getNode1().constr[0], elem.getNode1().constr[1], elem.getNode1().constr[2])
                self.__bc[self.connections[idx][1]] = (
                    elem.getNode2().constr[0], elem.getNode2().constr[1], elem.getNode2().constr[2])
            self.__bc = np.array(list(self.__bc.values())).flatten() * 1

            new_bc = [i + 1 for i in range(len(self.__bc)) if self.__bc[i] == 0]
            self.__bc = np.copy(new_bc)

    def __max_coords(self):
        x_coord = []
        y_coord = []
        z_coord = []
        for elem in self.elements:
            x_coord.append(elem.getNode1().x1)
            y_coord.append(elem.getNode1().x2)
            z_coord.append(elem.getNode1().x3)
            x_coord.append(elem.getNode2().x1)
            y_coord.append(elem.getNode2().x2)
            z_coord.append(elem.getNode2().x3)
        max_coord = (max(x_coord), max(y_coord), max(z_coord))

        return max_coord

    def __min_coords(self):
        x_coord = []
        y_coord = []
        z_coord = []
        for elem in self.elements:
            x_coord.append(elem.getNode1().x1)
            y_coord.append(elem.getNode1().x2)
            z_coord.append(elem.getNode1().x3)
            x_coord.append(elem.getNode2().x1)
            y_coord.append(elem.getNode2().x2)
            z_coord.append(elem.getNode2().x3)
        min_coord = (min(x_coord), min(y_coord), min(z_coord))

        return min_coord

    def max_force_initial(self):
        s = set()
        for elem in self.elements:
            s.add(elem.getNode1().force)
        return max(abs(np.array(list(s)).flatten()))

    def create_connections_nodes(self):
        self.lst = []

        for one_connect in self.connections:
            self.lst += self.nodes[one_connect[0]]
            self.lst += self.nodes[one_connect[1]]
        # CHANGE SHAPE OF ARRAY
        self.lst = np.array(self.lst).reshape((6, 6))

    def create_global_matrix(self):

        # assembling global matrix
        K_empty = np.zeros((len(self.__nodes) * 3, len(self.__nodes) * 3))
        for idx, elem in enumerate(self.elements):
            local_matrix = elem.computeStiffnessMatrix()
            self.assem(self.lst[idx, :], K_empty, local_matrix)

        self.__K_global = K_empty

    def create_global_force(self):
        force_temp = {}

        for idx, elem in enumerate(self.elements):
            force_temp[self.connections[idx][0]] = elem.getNode1().force
            force_temp[self.connections[idx][1]] = elem.getNode2().force

        self.__force = np.array(list(force_temp.values())).flatten()

    def __fill_displacement(self):
        displacement_temp = {}

        for idx, elem in enumerate(self.elements):
            displacement_temp[self.connections[idx][0]] = elem.getNode1().displ.displacement
            displacement_temp[self.connections[idx][1]] = elem.getNode2().displ.displacement

        self.__u_n = np.array(list(displacement_temp.values())).flatten()

        logger.info(f'\nfill_displacement: {self.__u_n}')

    def create_r0(self):
        force_temp = {}

        for idx, elem in enumerate(self.elements):
            force_temp[self.connections[idx][0]] = elem.getNode1().force
            force_temp[self.connections[idx][1]] = elem.getNode2().force

        self.__force = np.array(list(force_temp.values())).flatten()

    def solveq(self, K, f, bcPrescr, bcVal=None):

        nDofs = K.shape[0]
        nPdofs = bcPrescr.shape[0]

        if bcVal is None:
            bcVal = np.zeros([nPdofs], 'd')

        bc = np.ones(nDofs, 'bool')
        bcDofs = np.arange(nDofs)

        bc[np.ix_(bcPrescr - 1)] = False
        bcDofs = bcDofs[bc]

        fsys = f[bcDofs] - K[np.ix_((bcDofs), (bcPrescr - 1))] * \
               np.asmatrix(bcVal).reshape(nPdofs, 1)
        asys = np.linalg.solve(K[np.ix_((bcDofs), (bcDofs))], fsys)

        a = np.zeros([nDofs, 1])
        a[np.ix_(bcPrescr - 1)] = np.asmatrix(bcVal).reshape(nPdofs, 1)
        a[np.ix_(bcDofs)] = asys

        Q = K * np.asmatrix(a) - f

        return (np.asmatrix(a), Q)

    def solution(self):

        for idx, elem in enumerate(self.elements):
            self.di_1[self.connections[idx][0]] = elem.n1.displ.displacement
            self.di_1[self.connections[idx][1]] = elem.n2.displ.displacement
            self.di_2[self.connections[idx][0]] = elem.n1.force
            self.di_2[self.connections[idx][1]] = elem.n2.force

        # Who is connected to whom
        self.__bc_func()

        # DEFAULT SOLVER

        self.__a, self.__r = self.solveq(self.__K_global, self.__force.reshape(-1, 1), self.__bc)

        ##################################### ARC LENGTH METHOD
        # print(self.__K_global.shape)

        # obj = ArcLengthClass(r_0, displacements_all, )
        # self.arclength()

        ##################################### ARC LENGTH METHOD

        temp_a = np.mat(np.copy(self.__a))
        temp_a = np.reshape(temp_a, (len(list(self.di_1.keys())), 3))

        temp_r = np.mat(np.copy(self.__r))
        temp_r = np.reshape(temp_r, (len(list(self.di_2.keys())), 3))

        for idx, (key, value) in enumerate(self.di_1.items()):
            value = np.add(value, temp_a[idx])
            self.di_1[key] = value.tolist()[0]

        for idx, (key, value) in enumerate(self.di_2.items()):
            value = np.add(value, temp_r[idx])
            self.di_2[key] = value.tolist()[0]

        di_1_pd = pd.DataFrame.from_dict(self.di_1)
        di_2_pd = pd.DataFrame.from_dict(self.di_2)



        ###################### ADDITION OF NEW DISPLACEMENTS AND FORCES ########################
        s = set()
        for idx, (n1, n2) in enumerate(self.connections):
            if n1 not in s:
                s.add(n1)
                self.elements[idx].n1.displ = Displacement(tuple(di_1_pd[n1]))
                #self.elements[idx].n1.force = Force(tuple(di_2_pd[n1]))
            if n2 not in s:
                s.add(n2)
                self.elements[idx].n2.displ = Displacement(tuple(di_1_pd[n2]))
                #self.elements[idx].n2.force = Force(tuple(di_2_pd[n2]))

            #s.add(n2)

        for idx, elem in enumerate(self.elements):

            x = [elem.getNode1().x1, elem.getNode2().x1]
            y = [elem.getNode1().x2, elem.getNode2().x2]
            z = [elem.getNode1().x3, elem.getNode2().x3]
            displ_temp = [
                elem.getNode1().displ.displacement[0],
                elem.getNode1().displ.displacement[1],
                elem.getNode1().displ.displacement[2],
                elem.getNode2().displ.displacement[0],
                elem.getNode2().displ.displacement[1],
                elem.getNode2().displ.displacement[2]
            ]
            self.force_elements[idx] = elem.bar3s(x, y, z, [elem.getEModulus(), elem.getArea()], displ_temp)

        return self.__a, self.__r

    ########### ADDITIONAL FUNCTIONS ####################

    def assem(self, edof, K, Ke, f=None, fe=None):

        if edof.ndim == 1:
            idx = edof - 1
            K[np.ix_(idx, idx)] = K[np.ix_(idx, idx)] + Ke
            if (not f is None) and (not fe is None):
                f[np.ix_(idx)] = f[np.ix_(idx)] + fe
        else:
            for row in edof:
                idx = row - 1
                K[np.ix_(idx, idx)] = K[np.ix_(idx, idx)] + Ke
                if (not f is None) and (not fe is None):
                    f[np.ix_(idx)] = f[np.ix_(idx)] + fe

        if f is None:
            return K
        else:
            return K, f

    def visualize(self, fig_undeformed, canvas_undeformed, ax_undeformed, show=0):
        longest = max([elem.getLength() for elem in self.elements])

        obj = plcr(longest, self.__max_coords(), self.__min_coords(), self.max_force_initial())
        obj.ax = ax_undeformed
        obj.fig = fig_undeformed

        for idx, elem in enumerate(self.elements):
            obj.add_bar((elem.getNode1(), elem.getNode2()))

        return obj.final_plot(0)

    def visualize_deformed(self, fig_deformed, canvas_deformed, ax_deformed, show=0):
        longest = max([elem.getLength() for elem in self.elements])
        obj = plcr(longest, self.__max_coords(), self.__min_coords(), self.max_force_initial(),
                   list(self.force_elements.values()), np.array(list(self.di_1.values())).flatten())
        obj.ax = ax_deformed
        obj.fig = fig_deformed
        for idx, elem in enumerate(self.elements):
            obj.plotting_then((elem.getNode1(), elem.getNode2()))


        return obj.final_plot(1)

    def print_results(self):

        self.counter += 1
        logger.info(f'\nNODES:\n{self.__nodes}')

        # print(f'COUNTER = {self.counter}')
        new_displ = pd.DataFrame.from_dict(self.di_1)
        logger.info(f"\n{new_displ}")
        new_force = pd.DataFrame.from_dict(self.di_2)
        logger.info(f"\n{new_force}")

        with pd.ExcelWriter('Results/output.xlsx') as writer:
            new_displ.to_excel(writer, sheet_name='Displacement')
            new_force.to_excel(writer, sheet_name='Force')

    #######################################################

    def __update_displacements(self, displacement):

        temp_d = np.mat(np.copy(displacement))
        temp_d = np.reshape(temp_d, (len(list(self.di_1.keys())), 3))

        for idx, (key, value) in enumerate(self.di_1.items()):
            value = np.add(value, temp_d[idx])
            self.di_1[key] = value.tolist()[0]

        di_1_pd = pd.DataFrame.from_dict(self.di_1)

        ###################### ADDITION OF NEW DISPLACEMENTS ########################
        s = set()
        for idx, (n1, n2) in enumerate(self.connections):
            if n1 not in s:
                s.add(n1)
                self.elements[idx].n1.displ = Displacement(tuple(di_1_pd[n1]))
            if n2 not in s:
                s.add(n2)
                self.elements[idx].n2.displ = Displacement(tuple(di_1_pd[n2]))
            s.add(n2)

    def arclength(self):
        r_0 = np.copy(self.__force)
        self.__fill_displacement()
        u_n = np.copy(self.__u_n)

        s_pr = 0.05
        tol = 1e-4
        num_iter = 1
        max_iter = 10
        u_final = np.copy(u_n)
        lambda_n = np.array([0])
        lambda_final = np.array([0])

        for i in range(num_iter):

            self.create_global_matrix()
            k_t = np.copy(self.__K_global)
            # print(f'k_t: {k_t}')

            k_t_inverse = np.linalg.inv(k_t)
            # print(f'inverse: {k_t_inverse}')

            k_t_det = np.linalg.det(k_t)
            # print(f'determinant: {k_t_det}')

            delta_u_lambda = compute_Du_lambda(k_t_inverse, r_0)
            print(f'delta_u_lambda = \n{delta_u_lambda}')

            s_0 = np.sqrt(np.matmul(delta_u_lambda, delta_u_lambda) + 1)
            print(f'\ns_0 = {s_0}')

            delta_u = delta_u_lambda * s_pr / s_0
            print(f'\ndelta_u = \n{delta_u}\n')

            delta_lambda = 1 * s_pr / s_0
            print(f'delta_lambda = {delta_lambda}\n')

            u_n_1, lambda_n_1 = increment(k_t_det, u_n, delta_u, lambda_n, delta_lambda)
            print(f'u_n_1 = \n{u_n_1}\n')
            print(f'lambda_n_1 = {lambda_n_1}')

            k = 0
            error = 5

            # koef = 3
            # print("LAMBDA :", lambda_n_1)
            # print("S_0: ", s_0)

            # print(self.elements[koef].n1.displ)
            # print(self.elements[koef].n2.displ)

            self.__update_displacements(u_n_1)

            # print(self.elements[koef].n1.displ)
            # print(self.elements[koef].n2.displ)

            # print('QQQ: ', self.__u_n)

            # corrector steps
            print("\n############################################################################################")

            while error > tol and k < max_iter:
                # print(f'K = {k}')
                ##### compute internal force
                r_int = np.matmul(k_t, u_n_1) - lambda_n_1 * r_0
                # print(f'\nr_int: {r_int}\n')

                ##### compute K_t
                self.create_global_matrix()
                k_t = np.copy(self.__K_global)
                # logger.info(self.__K_global)
                # print(f'k_t = {k_t}')
                k_t_inverse = np.linalg.inv(k_t)
                # print(f'k_t_inverse = {k_t_inverse}')
                k_t_det = np.linalg.det(k_t)
                # print(f'k_t_det = {k_t_det}')

                ##### compute du_r
                delta_u_r = compute_Du_r(k_t_inverse, r_int, lambda_n_1, r_0)
                # print(f'delta_u_r = {delta_u_r}')

                ##### compute du_lambda
                delta_u_lambda = compute_Du_lambda(k_t_inverse, r_0)
                # print(f'delta_u_lambda = {delta_u_lambda}')

                ##### compute constraint function
                s = compute_ConstrainFunction_Sphere(u_n_1, u_n, lambda_n_1, lambda_n, s_pr)
                # print(f's = {s}')

                ##### compute d_lambda
                delta_lambda = compute_Dlambda(s, s_pr, delta_u_r, delta_u_lambda, lambda_n_1, lambda_n, u_n_1,
                                               u_n)
                # print(f'delta_lambda = {delta_lambda}')

                ##### compute du
                delta_u = delta_u_r + delta_u_lambda * delta_lambda
                # print(f'delta_u = {delta_u}')

                ##### update u_k+1  and lambda
                u_n_1 += delta_u
                print(f'u_n_1 = {u_n_1}')
                lambda_n_1 += delta_lambda
                # print(f'lambda_n_1 = {lambda_n_1}')

                ##### calculate error
                error = abs(compute_Error(delta_u, u_n_1, u_n))
                # print(f'error = {error}')
                k += 1
            # print(k)
            u_n = u_n_1
            lambda_n = lambda_n_1

            u_final = np.vstack((u_final, u_n_1))
            lambda_final = np.hstack((lambda_final, lambda_n_1))

        print(u_final)
        print(k)



if __name__ == '__main__':
    pass
