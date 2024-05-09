from typing import Optional
from Util import Point, distance

class NearestNeighborContainerNaive:
    def __init__(self, points: list[Point]):
        self.points = points.copy()

    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def remove_point(self, point: Point) -> None:
        self.points.remove(point)

    def query(self, point: Point) -> Optional[Point]:
        if len(self.points) == 0:
            return None
        best_point = None
        best_point_distance = float('inf')
        for p in self.points:
            p_dist = distance(point, p)
            if p_dist < best_point_distance:
                best_point = p
                best_point_distance = p_dist
        return best_point

