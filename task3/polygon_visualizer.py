import matplotlib.pyplot as plt
import numpy as np


class PolygonVisualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()

    def plot_polygon(self, points, color_hex):
        points = np.array(points)

        points = np.vstack([points, points[0]])

        x, y = points[:, 0], points[:, 1]

        self.ax.plot(x, y, color=color_hex)
        self.ax.fill(x, y, color=color_hex, alpha=0.3)

    def display(self, polygons):
        for polygon in polygons:
            self.plot_polygon(polygon["points"], polygon["color"])

        self.ax.set_aspect("equal", adjustable="box")
        plt.show()


polygons = [
    {"points": [(0, 0.4), (1, 0), (1, 1), (0, 1)], "color": "#ff5733"},
    {"points": [(2, 2), (3, 2), (2.5, 3.5)], "color": "#33ff57"},
    {
        "points": [(5, 5), (6, 5), (5, 6), (6, 6), (4.5, 5.5)],
        "color": "#3357ff",
    },
]

if __name__ == "__main__":
    visualizer = PolygonVisualizer()
    visualizer.display(polygons)
