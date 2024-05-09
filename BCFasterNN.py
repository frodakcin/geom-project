from KDTree import KDTree

def distance(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

class BCFasterNN:
    def __init__(self, p, q):
        self.points = [list(p), list(q)]

    def add_point(self, point, s):
        self.points[s].append(point)

    def remove_point(self, point, s):
        self.points[s].remove(point)

    def query(self):
        k1 = KDTree(self.points[0])
        k2 = KDTree(self.points[1])
        best_distance = float('inf')
        best = None, None

        for p1 in self.points[0]:
            dist, point = k2.nearest_neighbor(p1)
            if dist < best_distance:
                best_distance = dist
                best = p1, point
        for p2 in self.points[1]:
            dist, point = k1.nearest_neighbor(p2)
            if dist < best_distance:
                best_distance = dist
                best = p2, point

        return best

