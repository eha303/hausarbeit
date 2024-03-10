from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np


class VisualizeData:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def visualize(self):
        style.use('ggplot')
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(self.x, self.y, label="line plot example", linewidth=2)
        ax.legend()
        ax.grid(True, color="k")
        plt.ylabel('y axis')
        plt.xlabel('x axis')
        plt.title('Line Plot')
        plt.show()
