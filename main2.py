import matplotlib.pyplot as plt
from BichromaticClosestPair import PQStructure
from Util import Point

def PREP(self):
    point = Point.new([0.3578629032258065, 0.3428030303030304], label=0)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.33366935483870963, 0.5727813852813853], label=1)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5705645161290323, 0.6093073593073594], label=2)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.6945564516129032, 0.5051406926406927], label=3)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.6048387096774194, 0.2426948051948052], label=4)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.47782258064516125, 0.4050324675324676], label=5)
    self.Q.append(point)
    self.PQ.insert_q(point)
    point = Point.new([0.47580645161290325, 0.47537878787878796], label=6)
    self.Q.append(point)
    self.PQ.insert_q(point)
    point = Point.new([0.5715725806451613, 0.49837662337662336], label=7)
    self.Q.append(point)
    self.PQ.insert_q(point)

    point = Point.new([0.5866935483870968, 0.4686147186147186], label=8)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=9)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=10)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=11)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=12)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=13)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=14)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=15)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=16)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=17)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=18)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=19)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=20)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=21)
    self.P.append(point)
    self.PQ.insert_p(point)
    point = Point.new([0.5866935483870968, 0.4686147186147186], label=22)
    self.P.append(point)
    self.PQ.insert_p(point)
    self.remove_point(8)
    self.remove_point(9)
    self.remove_point(10)
    self.remove_point(11)
    self.remove_point(12)
    self.remove_point(13)
    self.remove_point(14)
    self.remove_point(15)
    self.remove_point(16)
    self.remove_point(17)
    self.remove_point(18)
    self.remove_point(19)
    self.remove_point(20)
    self.remove_point(21)
    self.remove_point(22)
    self.remove_point(7)
    self.remove_point(3)
    # point = Point.new([0.47681451612903225, 0.4415584415584416], label=38)
    # self.P.append(point)
    # self.PQ.insert_p(point)
    # self.remove_point(38)
    self.ctr = 40

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