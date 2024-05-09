import matplotlib.pyplot as plt
from BichromaticClosestPair import PQStructure
from Util import Point

def PREP(self):
    point = Point.new([0.360887, 0.536255], label=0)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.3608870967741936, 0.5362554112554113], label=1)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.2641129032258065, 0.5308441558441559], label=2)
    self.Q.append(point)
    self.PQ.insert_q(point)
    point = Point.new([0.2983870967741935, 0.6201298701298702], label=3)
    self.Q.append(point)
    self.PQ.insert_q(point)
    point = Point.new([0.3921370967741936, 0.6052489177489178], label=4)
    self.Q.append(point)
    self.PQ.insert_q(point)
    point = Point.new([0.42943548387096775, 0.5173160173160174], label=5)
    self.Q.append(point)
    self.PQ.insert_q(point)
    point = Point.new([0.3256048387096774, 0.44832251082251084], label=6)
    self.Q.append(point)
    self.PQ.insert_q(point)
    self.remove_point(0)
    self.remove_point(1)
    self.ctr = 8
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
                print(f"point = {repr(point)}")
                print(f"self.Q.append(point)")
                print(f"self.PQ.insert_q(point)")
            else:
                point = Point.new([x, y], label=self.ctr)
                self.ctr += 1
                self.P.append(point)
                self.ax.plot(x, y, 'bo')  # Add a point to 'P'
                self.PQ.insert_p(point)
                print(f"point = {repr(point)}")
                print(f"self.P.append(point)")
                print(f"self.PQ.insert_p(point)")
        elif event.button == 3:  # Right mouse button
            # Find the closest point
            if self.P or self.Q:
                closest_point = min(self.P + self.Q, key=lambda point: (point.coordinates[0] - x) ** 2 + (point.coordinates[1] - y) ** 2)
                self.remove_point(closest_point.label)
                print(f"self.remove_point({closest_point.label})")
                
        # Redraw all points and draw closest pair line
        self.draw_all()

# Create an instance of the interactive plot
interactive_plot = InteractivePoints()