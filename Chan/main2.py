import matplotlib.pyplot as plt
from BichromaticClosestPair import PQStructure
from Util import Point

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

    def on_click(self, event):
        if self.ctr == 0:
            point = Point.new([0.21370967741935484, 0.5443722943722944], label=0)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.311491935483871, 0.7824675324675325], label=1)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.5846774193548387, 0.8216991341991343], label=2)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.7691532258064516, 0.621482683982684], label=3)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.8125, 0.3698593073593074], label=4)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.7449596774193549, 0.1723484848484849], label=5)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.5735887096774194, 0.11823593073593072], label=6)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.27520161290322576, 0.15205627705627708], label=7)
            self.P.append(point)
            self.PQ.insert_p(point)
            point = Point.new([0.4233870967741936, 0.5064935064935066], label=8)
            self.Q.append(point)
            self.PQ.insert_q(point)
            point = Point.new([0.5201612903225806, 0.5579004329004329], label=9)
            self.Q.append(point)
            self.PQ.insert_q(point)
            point = Point.new([0.6028225806451613, 0.4862012987012987], label=10)
            self.Q.append(point)
            self.PQ.insert_q(point)
            point = Point.new([0.5625, 0.3793290043290043], label=11)
            self.Q.append(point)
            self.PQ.insert_q(point)
            point = Point.new([0.4707661290322581, 0.36444805194805197], label=12)
            self.Q.append(point)
            self.PQ.insert_q(point)
            point = Point.new([0.5070564516129032, 0.4510281385281385], label=13)
            self.P.append(point)
            self.PQ.insert_p(point)
            self.ctr = 14
            return
        
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
                # print(f"Point at ({closest_point[0]:.2f}, {closest_point[1]:.2f}) has been removed.")
                
        # Redraw all points and draw closest pair line
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

# Create an instance of the interactive plot
interactive_plot = InteractivePoints()