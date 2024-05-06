import random
from typing import Optional
import math

#####################
# CLOSEST PAIR UTIL #
#####################

class Point:
    @classmethod
    def new(cls, coordinates: list[int], label: str = "") -> 'Point':
        self = cls.__new__(cls)
        self.coordinates = coordinates
        self.label = label
        return self
    
    @classmethod
    def new_random(cls, dim: int, label: str = "") -> 'Point':
        self = cls.__new__(cls)
        self.coordinates = [random.uniform(0, 1) for _ in range(dim)]
        self.label = label
        return self
    
    def __init__(self) -> None:
        raise Exception("[Point] Use a classmethod instead")
    
    def __str__(self) -> str:
        return f"Point(\"{self.label}\" {self.coordinates})"

def distance(p1: Point, p2: Point):
    return math.sqrt(sum((v1 - v2) ** 2 for v1, v2 in zip(p1.coordinates, p2.coordinates)))


############
# MIN HEAP #
############

class MinHeapElem:
    @classmethod
    def new(cls, key, idx, val = None):
        self = cls.__new__(cls)
        self.key = key
        self.idx = idx
        if val is not None:
            self.val = val # Extra info you might store
        return self
    
    def __init__(self) -> None:
        raise Exception("[MinHeapElem] Use a classmethod instead")

    def __lt__(self, other):
        return self.key < other.key

class MinHeap:
    @classmethod
    def new_heap(cls) -> 'MinHeap':
        self = cls.__new__(cls)
        self.heap: list[MinHeapElem] = []
        self.checkRep()
        return self

    def __init__(self) -> None:
        raise Exception("[MinHeap] Use a classmethod instead")

    def heapify_up(self, idx: int) -> None:
        while idx > 0:
            par = (idx - 1) // 2
            if self.heap[idx] < self.heap[par]:
                self.heap[par], self.heap[idx] = self.heap[idx], self.heap[par]
                self.heap[idx].idx = idx
                self.heap[par].idx = par
                idx = par
            else:
                break
        self.checkRep()
    
    def heapify_down(self, idx: int) -> None:
        while idx < len(self.heap):
            left = 2 * idx + 1
            right = 2 * idx + 2
            if right < len(self.heap) and self.heap[right] < self.heap[idx] and self.heap[right] < self.heap[left]:
                self.heap[right], self.heap[idx] = self.heap[idx], self.heap[right]
                self.heap[idx].idx = idx
                self.heap[right].idx = right
                idx = right
            elif left < len(self.heap) and self.heap[left] < self.heap[idx]:
                self.heap[left], self.heap[idx] = self.heap[idx], self.heap[left]
                self.heap[idx].idx = idx
                self.heap[left].idx = left
                idx = left
            else:
                break
        self.checkRep()

    def decrease_key(self, elem: MinHeapElem, newKey: int) -> None:
        """
        Decreases the key of an element in the heap. Mutates the input elem to hold the new key
        """
        self.checkRep()
        assert newKey < elem.key, "[MinHeap::Decrease_Key] New key must be less than old key"

        elem.key = newKey
        self.heapify_up(elem.idx)
        self.checkRep()

    def push(self, key, val = None) -> MinHeapElem:
        self.checkRep()
        idx = len(self.heap)
        item = MinHeapElem.new(key, idx, val)

        self.heap.append(item)
        self.heap[idx].idx = idx

        self.heapify_up(idx)
        self.checkRep()
        return item

    def pop(self) -> Optional[MinHeapElem]:
        self.checkRep()
        if len(self.heap) == 0:
            self.checkRep()
            return None

        ret = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap[0].idx = 0
        self.heap.pop()

        self.heapify_down(0)

        self.checkRep()
        return ret

    def peek(self) -> Optional[MinHeapElem]:
        self.checkRep()
        return self.heap[0] if self.heap else None

    def __len__(self):
        self.checkRep()
        return len(self.heap)
    
    def checkRep(self):
        for i in range(len(self.heap)):
            assert self.heap[i].idx == i
            if i > 0:
                par = (i - 1) // 2
                assert not (self.heap[i] < self.heap[par]), f"Heap property violated at index {i} with parent {par}"


#####################
# CLOSEST PAIR ELEM #
#####################

class ClosestPairElem:
    @classmethod
    def new_elem(cls, p1: Point, p2: Point) -> 'ClosestPairElem':
        self = cls.__new__(cls)
        self.p1 = p1
        self.p2 = p2
        self.dist = distance(p1, p2)
        return self

    @classmethod
    def new_empty_elem(cls) -> 'ClosestPairElem':
        self = cls.__new__(cls)
        self.p1 = None
        self.p2 = None
        self.dist = float('inf')
        return self

    def __init__(self) -> None:
        raise Exception("Use a classmethod instead")

    def __lt__(self, other) -> bool:
        return self.dist < other.dist
    
    def __str__(self) -> str:
        return f"ClosestPairElem({self.p1}, {self.p2} {self.dist})"
