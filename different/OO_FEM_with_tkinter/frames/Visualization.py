from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib as mpl


def fill_between_3d(ax, x1, y1, z1, x2, y2, z2, mode=1, c='steelblue', alpha=0.6):
    if mode == 1:

        for i in range(len(x1) - 1):
            verts = [(x1[i], y1[i], z1[i]), (x1[i + 1], y1[i + 1], z1[i + 1])] + \
                    [(x2[i + 1], y2[i + 1], z2[i + 1]), (x2[i], y2[i], z2[i])]

            ax.add_collection3d(Poly3DCollection([verts],
                                                 alpha=alpha,
                                                 linewidths=0,
                                                 color=c))

    if mode == 2:
        verts = [(x1[i], y1[i], z1[i]) for i in range(len(x1))] + \
                [(x2[i], y2[i], z2[i]) for i in range(len(x2))]

        ax.add_collection3d(Poly3DCollection([verts], alpha=alpha, color=c))


class Arrow3D(FancyArrowPatch):

    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0, 0), (0, 0), *args, **kwargs)
        self._xyz = (x, y, z)
        self._dxdydz = (dx, dy, dz)

    def draw(self, renderer):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        super().draw(renderer)

    def do_3d_projection(self, renderer=None):
        x1, y1, z1 = self._xyz
        dx, dy, dz = self._dxdydz
        x2, y2, z2 = (x1 + dx, y1 + dy, z1 + dz)

        xs, ys, zs = proj_transform((x1, x2), (y1, y2), (z1, z2), self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))

        return np.min(zs)


def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''

    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)


setattr(Axes3D, 'arrow3D', _arrow3D)


class Plot_creator:
    ax = None
    fig = None
    # CHANGE
    __scale = None

    def __init__(self, length, max_coord, min_coord, max_force, element_forces=0, displacement=0):

        # self.fig = plt.figure()
        self.fig = plt.figure(figsize=plt.figaspect(0.5) * 1.5)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.length_koeff = length
        self.max_coord = max_coord
        self.min_coord = min_coord
        self.max_force = max_force
        self.final_element_forces = element_forces
        self.displacement = displacement
        self.count = 0
        if element_forces != 0:
            self.c = np.linspace(min(self.final_element_forces), max(self.final_element_forces),
                               len(self.final_element_forces))

    def plotting(self, nodes):
        plt.rcParams['text.usetex'] = True
        self.ax.grid()

        x_coord = np.linspace(getattr(nodes[0], 'x' + str(1)), getattr(nodes[1], 'x' + str(1)), 300)
        y_coord = np.linspace(getattr(nodes[0], 'x' + str(2)), getattr(nodes[1], 'x' + str(2)), 300)
        z_coord = np.linspace(getattr(nodes[0], 'x' + str(3)), getattr(nodes[1], 'x' + str(3)), 300)

        self.ax.scatter(x_coord, y_coord, z_coord, color='black', s=1)

    def plotting_then(self, nodes):
        self.__add_constraints(nodes)
        koef = 10000

        cmap = mpl.cm.get_cmap('rainbow', len(self.final_element_forces))

        dummie_cax = self.ax.scatter(self.c, self.c, c=self.c, cmap=cmap)

        points = 300
        x_coord = np.linspace(getattr(nodes[0], 'x' + str(1)) + nodes[0].displ.displacement[0] * koef,
                              getattr(nodes[1], 'x' + str(1)) + nodes[1].displ.displacement[0] * koef,
                              points)
        y_coord = np.linspace(getattr(nodes[0], 'x' + str(2)) + nodes[0].displ.displacement[1] * koef,
                              getattr(nodes[1], 'x' + str(2)) + nodes[1].displ.displacement[1] * koef,
                              points)
        z_coord = np.linspace(getattr(nodes[0], 'x' + str(3)) + nodes[0].displ.displacement[2] * koef,
                              getattr(nodes[1], 'x' + str(3)) + nodes[1].displ.displacement[2] * koef,
                              points)

        self.ax.scatter(x_coord, y_coord, z_coord, c=cmap(self.count), s=2)
        if not self.count:
            self.fig.colorbar(dummie_cax, ticks=self.c)
        self.count += 1

    def add_bar(self, nodes):
        self.plotting((nodes[0], nodes[1]))
        self.__add_forces(nodes)
        self.__add_constraints(nodes)

    def final_plot(self, koeff):
        koef = self.length_koeff / 10
        self.ax.set_xlim3d(self.min_coord[0] - koef, self.max_coord[0] + koef)
        self.ax.set_ylim3d(self.min_coord[0] - koef, self.max_coord[1] + koef)
        if self.max_coord[2] != 0:
            self.ax.set_zlim3d(self.min_coord[2] - koef, self.max_coord[2] + koef)
        else:
            self.ax.set_zlim3d(-0.2, 1.2 * self.max_coord[0])

        # plt.show()

    def __add_constraints(self, nodes, koef_new=1, color='black'):

        # z restrictions
        koef = self.length_koeff / 30
        if koef_new == 1:
            koef_new = 0
        else:
            koef_new = 10000

        const = 2
        for j in range(2):
            if nodes[j].constr[2] == 0:
                num_points = 2
                x_coord_minus = np.linspace(nodes[j].x1 - koef + nodes[j].displ.displacement[0] * koef_new,
                                            nodes[j].x1 + nodes[j].displ.displacement[0] * koef_new, num_points)
                x_coord_plus = np.linspace(nodes[j].x1 + koef + nodes[j].displ.displacement[0] * koef_new,
                                           nodes[j].x1 + nodes[j].displ.displacement[0] * koef_new, num_points)
                y_coord_1 = np.linspace(nodes[j].x2 - koef + nodes[j].displ.displacement[1] * koef_new,
                                        nodes[j].x2 + nodes[j].displ.displacement[1] * koef_new, num_points)
                y_coord_2 = np.linspace(nodes[j].x2 + koef + nodes[j].displ.displacement[1] * koef_new,
                                        nodes[j].x2 + nodes[j].displ.displacement[1] * koef_new, num_points)
                z_coord = np.linspace(nodes[j].x3 - koef * const + nodes[j].displ.displacement[2] * koef_new,
                                      nodes[j].x3 + nodes[j].displ.displacement[2] * koef_new, num_points)

                set05 = [x_coord_plus, y_coord_2, z_coord]
                set5 = [x_coord_plus, y_coord_1, z_coord]

                set06 = [x_coord_plus, y_coord_1, z_coord]
                set6 = [x_coord_minus, y_coord_1, z_coord]

                set07 = [x_coord_minus, y_coord_1, z_coord]
                set7 = [x_coord_minus, y_coord_2, z_coord]

                set08 = [x_coord_minus, y_coord_2, z_coord]
                set8 = [x_coord_plus, y_coord_2, z_coord]

                fill_between_3d(self.ax, *set05, *set5, mode=1, c="C0")

                fill_between_3d(self.ax, *set06, *set6, mode=1, c="C0")

                fill_between_3d(self.ax, *set07, *set7, mode=1, c="C0")

                fill_between_3d(self.ax, *set08, *set8, mode=1, c="C0")

        # x restrictions
        for j in range(2):
            if nodes[j].constr[0] == 0:
                num_points = 2
                y_coord_minus = np.linspace(nodes[j].x2 - koef, nodes[j].x2, num_points)
                y_coord_plus = np.linspace(nodes[j].x2 + koef, nodes[j].x2, num_points)
                z_coord_1 = np.linspace(nodes[j].x3 - koef, nodes[j].x3, num_points)
                z_coord_2 = np.linspace(nodes[j].x3 + koef, nodes[j].x3, num_points)
                x_coord = np.linspace(nodes[j].x1 - koef * const, nodes[j].x1, num_points)

                set05 = [x_coord, y_coord_plus, z_coord_2]
                set5 = [x_coord, y_coord_plus, z_coord_1]

                set06 = [x_coord, y_coord_plus, z_coord_1]
                set6 = [x_coord, y_coord_minus, z_coord_1]

                set07 = [x_coord, y_coord_minus, z_coord_1]
                set7 = [x_coord, y_coord_minus, z_coord_2]

                set08 = [x_coord, y_coord_minus, z_coord_2]
                set8 = [x_coord, y_coord_plus, z_coord_2]

                fill_between_3d(self.ax, *set05, *set5, mode=1, c="C0")
                fill_between_3d(self.ax, *set06, *set6, mode=1, c="C0")
                fill_between_3d(self.ax, *set07, *set7, mode=1, c="C0")
                fill_between_3d(self.ax, *set08, *set8, mode=1, c="C0")

        # y restrictions
        for j in range(2):
            if nodes[j].constr[1] == 0:
                num_points = 2
                z_coord_minus = np.linspace(nodes[j].x3 - koef, nodes[j].x3, num_points)
                z_coord_plus = np.linspace(nodes[j].x3 + koef, nodes[j].x3, num_points)
                x_coord_1 = np.linspace(nodes[j].x1 - koef, nodes[j].x1, num_points)
                x_coord_2 = np.linspace(nodes[j].x1 + koef, nodes[j].x1, num_points)
                y_coord = np.linspace(nodes[j].x2 - koef * const, nodes[j].x2, num_points)

                set05 = [x_coord_2, y_coord, z_coord_plus]
                set5 = [x_coord_1, y_coord, z_coord_plus]

                set06 = [x_coord_1, y_coord, z_coord_plus]
                set6 = [x_coord_1, y_coord, z_coord_minus]

                set07 = [x_coord_1, y_coord, z_coord_minus]
                set7 = [x_coord_2, y_coord, z_coord_minus]

                set08 = [x_coord_2, y_coord, z_coord_minus]
                set8 = [x_coord_2, y_coord, z_coord_plus]

                fill_between_3d(self.ax, *set05, *set5, mode=1, c="C0")
                fill_between_3d(self.ax, *set06, *set6, mode=1, c="C0")
                fill_between_3d(self.ax, *set07, *set7, mode=1, c="C0")
                fill_between_3d(self.ax, *set08, *set8, mode=1, c="C0")

        # pass

    def __add_forces(self, nodes):
        self.__scale = self.length_koeff / 2
        # x arrow node_1
        if nodes[0].force[0] != 0:
            self.ax.arrow3D(nodes[0].x1, nodes[0].x2, nodes[0].x3, nodes[0].force[0] / self.max_force * self.__scale, 0,
                            0,
                            mutation_scale=10,
                            arrowstyle="-|>",
                            linewidth=3)
        # y arrow node_1
        if nodes[0].force[1] != 0:
            self.ax.arrow3D(nodes[0].x1, nodes[0].x2, nodes[0].x3, 0,
                            nodes[0].force[1] / self.max_force * self.__scale,
                            0, mutation_scale=10,
                            arrowstyle="-|>",
                            linewidth=3)

        # z arrow node_1
        if nodes[0].force[2] != 0:
            self.ax.arrow3D(nodes[0].x1, nodes[0].x2, nodes[0].x3, 0, 0,
                            nodes[0].force[2] / self.max_force * self.__scale,
                            mutation_scale=10,
                            arrowstyle="-|>",
                            linewidth=3)

        # x arrow node_2
        if nodes[1].force[0] != 0:
            self.ax.arrow3D(nodes[1].x1, nodes[1].x2, nodes[1].x3,
                            nodes[1].force[0] / self.max_force * self.__scale, 0,
                            0, mutation_scale=10,
                            arrowstyle="-|>",
                            linewidth=3)
        # y arrow node_2
        if nodes[1].force[1] != 0:
            self.ax.arrow3D(nodes[1].x1, nodes[1].x2, nodes[1].x3, 0,
                            nodes[1].force[1] / self.max_force * self.__scale,
                            0, mutation_scale=10,
                            arrowstyle="-|>",
                            linewidth=3)

        # z arrow node_2
        if nodes[1].force[2] != 0:
            self.ax.arrow3D(nodes[1].x1, nodes[1].x2, nodes[1].x3, 0, 0,
                            nodes[1].force[2] / self.max_force * self.__scale,
                            mutation_scale=10,
                            arrowstyle="-|>",
                            linewidth=3)


if __name__ == '__main__':
    pass
