import matplotlib.pyplot as plt
import numpy as np


import matplotlib.pyplot as plt
import numpy as np


class PolygonVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def plot_polygon(self, points, color_hex, scale, x_start, y_start):
        points = np.array(points) * scale
        points[:, 0] += x_start
        points[:, 1] += y_start

        points = np.vstack([points, points[0]])
        x, y = points[:, 0], points[:, 1]

        self.ax.plot(x, y, color=color_hex)
        self.ax.fill(x, y, color=color_hex, alpha=0.3)

    def display(self, polygons):
        for polygon in polygons:
            self.plot_polygon(
                points=polygon["points"],
                color_hex=polygon["color"],
                scale=polygon["scale"],
                x_start=polygon["x_start"],
                y_start=polygon["y_start"],
            )

        self.ax.set_aspect("equal", adjustable="box")
        plt.show()
