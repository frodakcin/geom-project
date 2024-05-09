import matplotlib.pyplot as plt
from BichromaticClosestPair import PQStructure
from Util import Point

def PREP(self):
    pass

class InteractivePoints:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.points = []
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.on_click)

        self.P = []
        self.Q = []
        self.PQ = PQStructure.new(self.P, self.Q)
        self.ctr = 0

        PREP(self)
        self.draw_all()
        plt.show(block=False)
    
    def remove_point(self, label):
        for point in self.P:
            if point.label == label:
                self.PQ.remove_p(point)
                self.P.remove(point)
                return
        for point in self.Q:
            if point.label == label:
                self.PQ.remove_q(point)
                self.Q.remove(point)
                return
            
    def draw_all(self):
        self.ax.cla()
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        for point in self.P:
            self.ax.plot(point.coordinates[0], point.coordinates[1], 'bo')
        for point in self.Q:
            self.ax.plot(point.coordinates[0], point.coordinates[1], 'ro')
        
        # Draw line for the closest pair
        closest_pair = self.PQ.find_closest_pair()
        if closest_pair.p1 and closest_pair.p2:
            p, q = closest_pair.p1, closest_pair.p2
            self.ax.plot([p.coordinates[0], q.coordinates[0]], [p.coordinates[1], q.coordinates[1]], 'g-')  # green line

        self.fig.canvas.draw()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        

        x, y = event.xdata, event.ydata
        if event.button == 1:  # Left mouse button
            if event.key != None and 'shift' in event.key:
                point = Point.new([x, y], label=self.ctr)
                self.ctr += 1
                self.Q.append(point)
                self.ax.plot(x, y, 'ro')  # Add a point to 'Q'
                self.PQ.insert_q(point)
                # print(f"point = {repr(point)}")
                # print(f"self.Q.append(point)")
                # print(f"self.PQ.insert_q(point)")
            else:
                point = Point.new([x, y], label=self.ctr)
                self.ctr += 1
                self.P.append(point)
                self.ax.plot(x, y, 'bo')  # Add a point to 'P'
                self.PQ.insert_p(point)
                # print(f"point = {repr(point)}")
                # print(f"self.P.append(point)")
                # print(f"self.PQ.insert_p(point)")
        elif event.button == 3:  # Right mouse button
            # Find the closest point
            if self.P or self.Q:
                closest_point = min(self.P + self.Q, key=lambda point: (point.coordinates[0] - x) ** 2 + (point.coordinates[1] - y) ** 2)
                self.remove_point(closest_point.label)
                # print(f"self.remove_point({closest_point.label})")
                # print(f"Point at ({closest_point[0]:.2f}, {closest_point[1]:.2f}) has been removed.")
                
        # Redraw all points and draw closest pair line
        self.draw_all()

# Create an instance of the interactive plot
interactive_plot = InteractivePoints()