import matplotlib.pyplot as plt

class InteractivePoints:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.points = []
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        if event.button == 1:  # Left mouse button
            if event.key != None and 'shift' in event.key:
                self.points.append((x, y))
                self.ax.plot(x, y, 'bo')  # Add a point to 'Q'
                print(f"Point at ({x:.2f}, {y:.2f}) has been added.")
            else:
                self.points.append((x, y))
                self.ax.plot(x, y, 'ro')  # Add a point to 'P'
                print(f"Point at ({x:.2f}, {y:.2f}) has been added.")
        elif event.button == 3:  # Right mouse button
            # Find the closest point
            if self.points:
                closest_point = min(self.points, key=lambda point: (point[0] - x) ** 2 + (point[1] - y) ** 2)
                self.points.remove(closest_point)
                print(f"Point at ({closest_point[0]:.2f}, {closest_point[1]:.2f}) has been removed.")
                # Redraw all points
                self.ax.cla()
                self.ax.set_xlim(0, 1)
                self.ax.set_ylim(0, 1)
                for point in self.points:
                    self.ax.plot(point[0], point[1], 'ro')
        self.fig.canvas.draw()

# Create an instance of the interactive plot
interactive_plot = InteractivePoints()