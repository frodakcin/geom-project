from scipy.spatial import Delaunay
import numpy as np

def distance(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

class BCFaster:
    def __init__(self, p, q):
        self.points = [list(p), list(q)]

    def add_point(self, point, s):
        self.points[s].append(point)

    def remove_point(self, point, s):
        self.points[s].remove(point)

    def query(self):
        s1 = set(self.points[0])
        s2 = set(self.points[1])

        points = self.points[0] + self.points[1]

        # Combine all points and find the Delaunay triangulation
        all_points = np.array(points)
        triangulation = Delaunay(all_points)
        min_edge_length = float('inf')
        min_edge = None

        for simplex in triangulation.simplices:
            for i in range(len(simplex)):
                for j in range(i + 1, len(simplex)):
                    p1 = all_points[simplex[i]]
                    p1 = (p1[0], p1[1])
                    p2 = all_points[simplex[j]]
                    p2 = (p2[0], p2[1])
                    if (p1 in s1 and p2 in s2) or (p1 in s2 and p2 in s1):
                        edge_length = distance(p1, p2)
                        if edge_length < min_edge_length:
                            min_edge_length = edge_length
                            min_edge = (p1, p2)
        # Output the vertices of the triangles in the triangulation
        
        return min_edge

