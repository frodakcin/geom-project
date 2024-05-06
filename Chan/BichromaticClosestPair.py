import matplotlib.pyplot as plt
from NearestNeighbor import NearestNeighborContainerNaive
from Util import Point, distance, MinHeap, ClosestPairElem
import math


def make_nn_container(points: list[Point]):
    return NearestNeighborContainerNaive(points)

param_b = 2
param_Delta = 5

class PQStructureOneWay:
    def __init__(self, P: list[Point], Q: list[Point]):
        self.P = P
        self.Q = Q
        self.construct()

    def construct(self):
        self.Q_good = []
        self.Q_bad = []
        self.pq_map = {}
        self.pq_edge = {}
        self.q_deg = {q: [] for q in self.Q}

        self.heap = MinHeap.new_heap()
        self.nn_structure = make_nn_container(self.Q)

        # Draw edges from p -> q
        for p in self.P:
            q = self.nn_structure.query(p)
            self.pq_map[p] = q
            self.pq_edge[p] = self.heap.push(distance(p, q), (p, q))
            self.q_deg[q].append(p)
            if len(self.q_deg[q]) >= param_Delta:
                self.Q_bad.append(q)
                self.nn_structure.remove_point(q)

        # OK

    def find_closest_pair(self) -> ClosestPairElem:
        val = self.heap.peek()
        if val is None:
            return ClosestPairElem.new_empty_elem()
        return ClosestPairElem.new_elem(val.val[0], val.val[1])
    
    def display(self, ax, pColor='black', qColor='black', qBadColor='gray', edgeColor='black'):
        p_x, p_y = zip(*[(p.coordinates[0], p.coordinates[1]) for p in self.P])
        sz = 20
        ax.scatter(p_x, p_y, c=pColor, label='P Points', s=sz)

        q_good_x, q_good_y = [], []
        q_bad_x, q_bad_y = [], []
        for q in self.Q:
            if q in self.Q_bad:
                q_bad_x.append(q.coordinates[0])
                q_bad_y.append(q.coordinates[1])
            else:
                q_good_x.append(q.coordinates[0])
                q_good_y.append(q.coordinates[1])
        ax.scatter(q_good_x, q_good_y, c=qColor, label='Good Q Points', s=sz)
        ax.scatter(q_bad_x, q_bad_y, c=qBadColor, label='Bad Q Points', s=sz, marker='x')

        for p in self.P:
            q = self.pq_map.get(p)
            if q:
                
                dx = q.coordinates[0] - p.coordinates[0]
                dy = q.coordinates[1] - p.coordinates[1]

                # Calculate the length of the vector (distance between p and q)
                length = math.sqrt(dx**2 + dy**2)

                # Normalize the vector to get the unit vector
                unit_dx = dx / length
                unit_dy = dy / length

                # Set the offset distance
                offset = min(0.03, length * 0.5)  # Adjust this value as needed

                # Calculate new starting and ending points with offset
                start_x = p.coordinates[0]
                start_y = p.coordinates[1]
                end_x = q.coordinates[0] - unit_dx * offset
                end_y = q.coordinates[1] - unit_dy * offset

                # Draw the arrow with offsets
                ax.arrow(start_x, start_y, end_x - start_x, end_y - start_y, head_width=0.01, head_length=0.01, fc=(1, 1, 1, 0), ec=edgeColor, linestyle='-')

        ax.legend()
    
class PQStructure:
    @classmethod
    def new(cls, P: list[Point], Q: list[Point]) -> 'PQStructure':
        self = cls.__new__(cls)
        self.base = True
        self.P = P
        self.Q = Q
        if len(P) == 0 or len(Q) == 0:
            return self
        if len(P) + len(Q) <= param_b * 2:
            return self
        self.base = False
        self.PQ = PQStructureOneWay(P, Q)
        self.QP = PQStructureOneWay(Q, P)

        self.Q_bad = self.PQ.Q_bad
        self.P_bad = self.QP.Q_bad
        self.next_pq_structure: PQStructure = PQStructure.new(self.P_bad, self.Q_bad)
        return self

    def find_closest_pair(self) -> ClosestPairElem:
        if self.base:
            cp = ClosestPairElem.new_empty_elem()
            for p in self.P:
                for q in self.Q:
                    cp_new = ClosestPairElem.new_elem(p, q)
                    if cp_new < cp:
                        cp = cp_new
            return cp
        else:
            my_cp1 = self.PQ.find_closest_pair()
            my_cp2 = self.QP.find_closest_pair()
            return min([my_cp1, my_cp2, self.next_pq_structure.find_closest_pair()])
    
    def display(self):
        if self.base:
            return

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        
        # Plot for PQ structure
        self.PQ.display(axes[0], pColor='blue', qColor='red', qBadColor='firebrick', edgeColor='gray')

        # Plot for QP structure
        self.QP.display(axes[1], pColor='red', qColor='blue', qBadColor='darkblue', edgeColor='gray')

        plt.show()

class BichromaticClosestPair:
    pass
