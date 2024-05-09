from KDTree import KDTree

def distance(p1, p2):
    return sum((x - y) ** 2 for x, y in zip(p1, p2)) ** 0.5

class NearestNeighborNaive:
    def __init__(self, points):
        self.points = set(points)

    def remove(self, point):
        if point in self.points:
            self.points.remove(point)

    def nearest_neighbor(self, point):
        ans = min(self.points, key=lambda p: distance(point, p))
        return distance(ans, point), ans

class NearestNeighborFast:
    def __init__(self, points):
        self.tree = KDTree(points)

    def remove(self, point):
        self.tree.remove(point)

    def nearest_neighbor(self, point):
        return self.tree.nearest_neighbor(point)

import random

class Tester:
    def __init__(self, N):
        self.points = [(random.random(), random.random()) for _ in range(N)]
        self.N1 = NearestNeighborNaive(self.points)
        self.N2 = NearestNeighborFast(self.points)

    def test_remove(self):
        if len(self.points) <= 2:
            return
        idx = random.randint(0, len(self.points) - 1)
        self.N1.remove(self.points[idx])
        self.N2.remove(self.points[idx])
        self.points[idx] = self.points[-1]
        self.points.pop()
    
    def test_query(self):
        point = (random.random(), random.random())
        ans1 = self.N1.nearest_neighbor(point)
        ans2 = self.N2.nearest_neighbor(point)
        assert ans1 == ans2

    def test(self, M):
        for i in range(M):
            if random.random() < 0.5:
                self.test_remove()
            else:
                self.test_query()

# tester = Tester(12)
# tester.test(10000)
# tester.N2.tree.plot()


# print(tree.search_path)
