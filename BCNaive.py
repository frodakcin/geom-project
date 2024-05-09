def distance(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

class BCNaive:
    def __init__(self, p, q):
        self.points = [list(p), list(q)]

    def add_point(self, point, s):
        self.points[s].append(point)

    def remove_point(self, point, s):
        self.points[s].remove(point)

    def query(self):
        best_distance = float('inf')
        best = None, None
        for p in self.points[0]:
            for q in self.points[1]:
                if distance(p, q) < best_distance:
                    best_distance = distance(p, q)
                    best = (p, q)
        return best

