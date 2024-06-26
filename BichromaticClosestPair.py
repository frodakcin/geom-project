from typing import Optional
import matplotlib.pyplot as plt
from NearestNeighbor import NearestNeighborContainerNaive, NearestNeighborContainerFast
from Util import Point, distance, MinHeap, ClosestPairElem
import math


print("WARNING: Using fast NN container will encounter issues when two points are at exactly the same coordinates")
def make_nn_container(points: list[Point]):
    return NearestNeighborContainerFast(points)
    # return NearestNeighborContainerNaive(points)

param_b = 2
param_Delta = 5

class PQStructureOneWay:
    def __init__(self, P: set[Point], Q: set[Point]):
        self.P = set(P)
        self.Q = set(Q)
        self.construct()

    def construct(self):
        self.Q_bad = set()
        self.pq_map = {}
        self.pq_edge = {}
        self.q_deg = {q: [] for q in self.Q}

        self.heap = MinHeap.new_heap()
        self.nn_structure = make_nn_container(self.Q)

        # Draw edges from p -> q
        for p in self.P:
            self.insert_p(p, add=False, recurse=False)

    def insert_p(self, p: Point, add: bool, recurse: bool):
        if add:
            self.P.add(p)
        q = self.nn_structure.query(p)
        if q is None:
            return
        self.pq_map[p] = q
        self.pq_edge[p] = self.heap.push(distance(p, q), (p, q))
        self.q_deg[q].append(p)
        if len(self.q_deg[q]) >= param_Delta:
            self.nn_structure.remove_point(q)
            self.Q.remove(q)
            if recurse:
                self.next_PQ.insert_q(q)
            else:
                self.Q_bad.add(q)

    def remove_p(self, p: Point):
        if p in self.pq_map:
            self.P.remove(p)
            self.heap.remove(self.pq_edge[p])
            self.q_deg[self.pq_map[p]].remove(p)
            del self.pq_edge[p]
            del self.pq_map[p]

    def remove_q(self, q: Point):
        if q in self.Q_bad:
            self.next_PQ.remove_q(q)
        else:
            self.Q.remove(q)
            self.nn_structure.remove_point(q)

        to_rem = []
        if q in self.q_deg:
            to_rem = self.q_deg[q]
            del self.q_deg[q]
        for p in to_rem:
            self.heap.remove(self.pq_edge[p])
            del self.pq_edge[p]
            del self.pq_map[p]

        for p in to_rem:
            self.insert_p(p, add=False, recurse=True)


    def find_closest_pair(self) -> ClosestPairElem:
        val = self.heap.peek()
        if val is None:
            return ClosestPairElem.new_empty_elem()
        return ClosestPairElem.new_elem(val.val[0], val.val[1])
    
    def display(self, ax, pColor='black', qColor='black', qBadColor='gray', edgeColor='black'):
        sz = 20
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])

        if len(self.P) > 0:
            p_x, p_y = zip(*[(p.coordinates[0], p.coordinates[1]) for p in self.P])
            ax.scatter(p_x, p_y, c=pColor, label='P Points', s=sz)


        q_good_x, q_good_y = [], []
        q_bad_x, q_bad_y = [], []
        for q in self.Q:
            q_good_x.append(q.coordinates[0])
            q_good_y.append(q.coordinates[1])
        for q in self.Q_bad:
            q_bad_x.append(q.coordinates[0])
            q_bad_y.append(q.coordinates[1])
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
    
class PQStructure:
    @classmethod
    def make_clone(cls, clone: 'PQStructure') -> 'PQStructure':
        self = cls.__new__(cls)
        self.base = clone.base
        self.P = clone.Q
        self.Q = clone.P
        self.clone = clone
        if self.base:
            return self
        self.PQ = clone.QP
        self.QP = clone.PQ
        self.P_bad = clone.Q_bad
        self.Q_bad = clone.P_bad
        self.next_pq_structure = clone.next_pq_structure.clone
        return self
    
    def copy_to_clone(self, clone):
        clone.base = self.base
        clone.P = self.Q
        clone.Q = self.P
        clone.clone = self
        if self.base:
            return
        clone.PQ = self.QP
        clone.QP = self.PQ
        clone.P_bad = self.Q_bad
        clone.Q_bad = self.P_bad
        clone.next_pq_structure = self.next_pq_structure.clone

    @classmethod
    def new(cls, P: list[Point], Q: list[Point]) -> 'PQStructure':
        return cls.new_alias(set(P), set(Q))

    @classmethod
    def new_alias(cls, P: set[Point], Q: set[Point]) -> 'PQStructure':
        self = cls.__new__(cls)
        self.base = True
        self.P = P
        self.Q = Q
        if len(self.P) == 0 or len(self.Q) == 0:
            self.clone = PQStructure.make_clone(self)
            return self
        if len(self.P) + len(self.Q) <= param_b * 2:
            self.clone = PQStructure.make_clone(self)
            return self
        self.base = False
        self.PQ = PQStructureOneWay(self.P, self.Q)
        self.QP = PQStructureOneWay(self.Q, self.P)

        self.Q_bad = self.PQ.Q_bad
        self.P_bad = self.QP.Q_bad
        self.next_pq_structure: PQStructure = PQStructure.new_alias(self.P_bad, self.Q_bad)

        self.PQ.next_PQ = self.next_pq_structure
        self.QP.next_PQ = self.next_pq_structure.clone
        self.clone = PQStructure.make_clone(self)
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
        
    def reconstruct(self):
        self.base = True
        if len(self.P) == 0 or len(self.Q) == 0:
            self.copy_to_clone(self.clone)
            return
        if len(self.P) + len(self.Q) <= param_b * 2:
            self.copy_to_clone(self.clone)
            return
        self.base = False
        self.PQ = PQStructureOneWay(self.P, self.Q)
        self.QP = PQStructureOneWay(self.Q, self.P)

        self.Q_bad = self.PQ.Q_bad
        self.P_bad = self.QP.Q_bad
        self.next_pq_structure: PQStructure = PQStructure.new_alias(self.P_bad, self.Q_bad)

        self.PQ.next_PQ = self.next_pq_structure
        self.QP.next_PQ = self.next_pq_structure.clone

        self.copy_to_clone(self.clone)

    def check_size(self):
        if self.base:
            self.reconstruct()
            return False
        
        if len(self.P) > param_b * len(self.P_bad) and len(self.Q) > param_b * len(self.Q_bad):
            return True
        
        self.reconstruct()
        return False

    def insert_p(self, p: Point):
        assert p not in self.P
        self.P.add(p)
        if self.base:
            self.check_size()
        else:
            self.PQ.insert_p(p, True, True)
            if self.check_size():
                self.next_pq_structure.insert_p(p)

    def insert_q(self, q: Point):
        self.clone.insert_p(q)
            
    def remove_q(self, q: Point):
        assert q in self.Q
        self.Q.remove(q)
        if self.base:
            self.check_size()
        else:
            self.PQ.remove_q(q)
            pqs = self
            while not pqs.base:
                pqs.QP.remove_p(q)
                pqs = pqs.next_pq_structure
            self.check_size()
    
    def remove_p(self, p: Point):
        self.clone.remove_q(p)

    def display_on(self, axl, axr):
        if self.base:
            axl.set_xlim([0, 1])
            axl.set_ylim([0, 1])
            axl.scatter([p.coordinates[0] for p in self.P], [p.coordinates[1] for p in self.P], c='blue', label='P points')
            axl.scatter([q.coordinates[0] for q in self.Q], [q.coordinates[1] for q in self.Q], c='red', label='Q points')
            return

        # Plot for PQ structure
        self.PQ.display(axl, pColor='blue', qColor='red', qBadColor='firebrick', edgeColor='gray')

        # Plot for QP structure
        self.QP.display(axr, pColor='red', qColor='blue', qBadColor='darkblue', edgeColor='gray')

    def display(self, block=False):
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        self.display_on(axes[0], axes[1])

        plt.show(block=block)

    def display_all(self, on=None, block=False):
        pq_structs = [self]
        tmp = self
        while not tmp.base:
            pq_structs.append(tmp.next_pq_structure)
            tmp = tmp.next_pq_structure

        h, w = max(len(pq_structs), 2), 2
        if on is None:
            fig, axes = plt.subplots(h, w, figsize=(12, 6))
        else:
            on.clf()
            axes = on.subplots(h, w)
            on.tight_layout(pad=1)

        for i, pq_struct in enumerate(pq_structs):
            pq_struct.display_on(axes[i, 0], axes[i, 1])

        if on is None:
            plt.show(block=block)
        else:
            on.canvas.draw()

class BichromaticClosestPair:
    def __init__(self, p, q):
        self.map = {}
        self.PQ = PQStructure.new([self.get_point(point) for point in p], [self.get_point(point) for point in q])

    def get_point(self, point):
        if point in self.map:
            return self.map[point]
        self.map[point] = Point.new(list(point))
        return self.map[point]

    def add_point(self, point, s):
        match s:
            case 0:
                self.PQ.insert_p(self.get_point(point))
            case 1:
                self.PQ.insert_q(self.get_point(point))

    def remove_point(self, point, s):
        match s:
            case 0:
                self.PQ.remove_p(self.get_point(point))
            case 1:
                self.PQ.remove_q(self.get_point(point))

    def query(self):
        closestElm = self.PQ.find_closest_pair()
        if closestElm.p1 is None:
            return (None, None)
        return (closestElm.p1.coordinates[0], closestElm.p1.coordinates[1]), (closestElm.p2.coordinates[0], closestElm.p2.coordinates[1])
