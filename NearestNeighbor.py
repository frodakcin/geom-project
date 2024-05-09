from typing import Optional
from Util import Point, distance
from KDTree import KDTree

class NearestNeighborContainerNaive:
    def __init__(self, points: list[Point]):
        self.points = set(points)

    def add_point(self, point: Point) -> None:
        self.points.add(point)

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

ops = 0

from math import log2, ceil
class NearestNeighborContainerFast:
    def __init__(self, points: list[Point]):
        self.map = {self.point_to_tuple(point): point for point in points}
        self.tree = KDTree([self.point_to_tuple(point) for point in points])
        global ops
        self.loglen = int(ceil(log2(len(points))))
        ops += len(points) * self.loglen

    def point_to_tuple(self, point: Point) -> tuple[float, float]:
        return tuple(point.coordinates)

    def tuple_to_point(self, point: tuple[float, float]) -> Point:
        return self.map[point]

    def add_point(self, point: Point) -> None:
        global ops
        ops += self.loglen
        raise NotImplementedError

    def remove_point(self, point: Point) -> None:
        global ops
        ops += self.loglen
        self.tree.remove(self.point_to_tuple(point))

    def query(self, point: Point) -> Optional[Point]:
        global ops
        ops += self.loglen
        dist, out = self.tree.nearest_neighbor(self.point_to_tuple(point))
        if out is None:
            return None
        return self.tuple_to_point(out)
